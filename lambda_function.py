from datetime import datetime, timedelta
from dateutil import tz
import boto3
import os

schedules = os.environ.get("schedule", "")
paramZone = os.environ.get("zone", "America/New_York")

DB_AVAILABLE_STATUS   = "available"
DB_UNAVAILABLE_STATUS = "stopped"

ZONE   = tz.gettz(paramZone)
client = boto3.client('rds')

OFF_OP = "OFF"
ON_OP  = "ON"
NOW    = datetime.now().utcnow().astimezone(ZONE)


def handleRDSAvailability(dbIdentifier, atime, btime, action, callback):

    def stringToDatetime(timeString):
        return datetime.strptime(timeString, '%H:%M:%S')


    def isParamsTimeInBetween():
        hour = NOW.hour
        minute = NOW.minute
        return stringToDatetime("%s:00" % atime) <  stringToDatetime("%s:%s:00" % (hour, minute)) and \
            stringToDatetime("%s:00" % btime) > stringToDatetime("%s:%s:00" % (hour, minute))


    def shouldTurnOffDatabase(dbStatus):
        return isParamsTimeInBetween() and dbStatus == DB_AVAILABLE_STATUS


    def shouldTurnOnDatabase(dbStatus):
        return (not isParamsTimeInBetween()) and dbStatus == DB_UNAVAILABLE_STATUS


    if action in [OFF_OP, ON_OP]:
        for page in client.get_paginator('describe_db_instances').paginate():
            for db in page.get("DBInstances"):

                if (dbIdentifier == db.get("DBInstanceIdentifier")):

                    if action == OFF_OP:
                        if shouldTurnOffDatabase(db.get("DBInstanceStatus")):
                            client.stop_db_instance(DBInstanceIdentifier=dbIdentifier)

                    if action == ON_OP:
                        if shouldTurnOnDatabase(db.get("DBInstanceStatus")):
                            client.start_db_instance(DBInstanceIdentifier=dbIdentifier)
                    
                    callback({"action": action})


# here you may send notification to Slack...
def callback(response):

    if response.get("isOn"):
        print("notify with on param")

    if response.get("isOff"):
        print("notify with off param")


# entrypoint
def lambda_handler(event, context):

    for schedule in schedules.split(","):
        try:
            handleRDSAvailability(*schedule.split("::"), callback)
        except TypeError:
            pass
        
