## How to use it

Just copy and paste this code into your new AWS Lambda function.

Pass in your `schedule` using ENV variables, such as:
1. "rds-db1::23:00::8:00::OFF,rds-db2::13:00::18:00::OFF,rds-db2::8:00::23:00::ON"
2. env variable `zone` allows you to configure time zone. fallback to "America/New_York"

With the `schedule` above, the Lambda will make sure that:

1) database with identifier "rds-db1" is in "stopped" state from 11:00PM to 8:00AM
2) database with identifier "rds-db2" is in "stopped" state from 1:00PM to 6:00PM
3) database with identifier "rds-db3" is in "available" state from 8:00AM to 23:00AM 

## ToDo:

~1. Make it timezone friendly~
2. improve scheduling mechanizm
3. package with `pip`
4. add hooks

