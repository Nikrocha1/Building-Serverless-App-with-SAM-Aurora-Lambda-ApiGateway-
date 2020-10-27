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
    #event_body = json.loads(event["body"]) #misma funcion que JSON.parse
    event_ID = event["pathParameters"]
    sql_text = 'DELETE FROM {} WHERE id = "{}"'.format(TableName, event_ID["id"])
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
        'body': "Number of Records Deleted: {}".format(responseBody)
        }
     return response
        #return response1
    except:
     print("Unexpected error:", sys.exc_info()[0])
     responseBody =  "Unable to delete user data"
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