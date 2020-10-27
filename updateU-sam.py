import os
import boto3
from collections import defaultdict
import json
import sys

rdsData = boto3.client('rds-data')
cluster_arn = os.environ['DB_AURORA'] 
secret_arn =  os.environ['SECRET_ARN']


def lambda_handler(event, context):
    TableName = os.environ['TABLE_NAME']
    print(event)
    event_body = json.loads(event["body"]) #misma funcion que JSON.parse
    sql_text = 'UPDATE {0} SET FirstName = "{1}", LastName = "{2}", Email = "{3}" WHERE id = "{4}";'.format(TableName, event_body["FirstName"], event_body["LastName"], event_body["Email"], event_body["id"])
    #sql_text = 'select * from {0} where id = "{1}"'.format(TableName, event["id"])
    try:
     response1 = rdsData.execute_statement(
                resourceArn = cluster_arn, 
                secretArn = secret_arn, 
                database = 'Auroradb', 
                sql = sql_text)
        #data = Format_ans(response1)
        #print(json.dumps(response1["records"][0][1]))
     print(response1)
     responseBody = json.dumps(response1["numberOfRecordsUpdated"])
     response = {
        'statusCode': 204,
        'headers': {
            "content-type": "application/json",
            "access-control-allow-origin": "*"
            
        },
        'body': "Number of Records Updated: {}".format(responseBody)
        }
     return response
        #return response1
    except:
     print("Unexpected error:", sys.exc_info()[0])
     responseBody =  "Unable to update user data"
     response =  {
        'statusCode': 403,
        'headers': {
            "content-type": "application/json",
            "access-control-allow-origin": "*"
            
        },
        'body': responseBody
        }
     return response
     #   print("Unexpected error:", sys.exc_info()[0])