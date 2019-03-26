## How to use it

Just copy and paste this code into your new AWS Lambda function.
Pass in your schedule using ENV variables:
1. `ZONE` this will defile a time zone
2. `SCHEDULE` this has to be in a format, such as: `rds-db1::23:00::8:00::OFF,rds-db2::13:00::18:00::OFF,rds-db2::8:00::23:00::ON` to:

With the `SCHEDULE` above, the Lambda:

1) will stop database with identifier "rds-db1" from 11:00PM to 8:00AM
2) will stop database with indentifier "rds-db2" from 1:00PM to 6:00PM
3) will start database with indentifier "rds-db3" from 8:00AM to 23:00AM 
