from datetime import datetime
from dateutil import tz
import boto3
import os

schedules = os.environ.get("schedule", "")

DB_AVAILABLE_STATUS   = "available"
DB_UNAVAILABLE_STATUS = "stopped"

CLIENT      = boto3.client('rds')
OFF_OP      = "OFF"
ON_OP       = "ON"
TIME_FORMAT = '%H:%M:%S'
TIME_NOW    = datetime.now()
HOUR        = TIME_NOW.hour
MINUTES     = TIME_NOW.minute


def handleRDSAvailability(dbIdentifier, atime, btime, action, callback):

    def stringToDatetime(timeString):
        return datetime.strptime(timeString, TIME_FORMAT)


    def isParamsTimeInBetween():
        return stringToDatetime("%s:00" % atime) <= stringToDatetime("%s:%s:00" % (HOUR, MINUTES)) and \
            stringToDatetime("%s:00" % btime) >= stringToDatetime("%s:%s:00" % (HOUR, MINUTES))


    def shouldTurnOffDatabase(dbStatus):
        return isParamsTimeInBetween() and dbStatus == DB_AVAILABLE_STATUS


    def shouldTurnOnDatabase(dbStatus):
        return (not isParamsTimeInBetween()) and dbStatus == DB_UNAVAILABLE_STATUS


    if action in ["OFF", "ON"]:
        for page in CLIENT.get_paginator('describe_db_instances').paginate():
            for db in page.get("DBInstances"):

                if (dbIdentifier == db.get("DBInstanceIdentifier")):

                    if action == OFF_OP:
                        if shouldTurnOffDatabase(db.get("DBInstanceStatus")):
                            CLIENT.stop_db_instance(DBInstanceIdentifier=dbIdentifier)
                            callback({"isOff": True})

                    if action == ON_OP:
                        if shouldTurnOnDatabase(db.get("DBInstanceStatus")):
                            CLIENT.start_db_instance(DBInstanceIdentifier=dbIdentifier)
                            callback({"isOn": True})


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
        
