import os
import boto3
import json 
from collections import defaultdict
import sys


rdsData = boto3.client('rds-data')
cluster_arn = os.environ['DB_AURORA'] 
secret_arn =  os.environ['SECRET_ARN']


def Format_ans(response):
    items = {}
    items["Item"] = [] #comentar para solo 1 registro
    for record in response["records"]:
        item = {}
        item["id"] = record[0]["longValue"]
        item["FirstName"] = record[1]["stringValue"]
        item["LastName"] = record[2]["stringValue"]
        item["Email"] = record[3]["stringValue"]
        print(item)
        items["Item"].append(item) #comentar para solo 1 registro
        #items["Item"] = item
    return items
    

def lambda_handler(event, context):
    TableName = os.environ['TABLE_NAME']
    #sql_text = 'INSERT INTO {0} (FirstName, LastName, Email) VALUES ("{1}", "{2}", "{3}" )'.format(TableName, event["FirstName"], event["LastName"], event["Email"] )
    #event_ID = event["pathParameters"]
    #sql_text = 'select * from {0} where id = "{1}"'.format(TableName, event_ID["id"])
    sql_text = 'select * from {}'.format(TableName)
    #try:
    response1 = rdsData.execute_statement(
                resourceArn = cluster_arn, 
                secretArn = secret_arn, 
                database = 'Auroradb', 
                sql = sql_text)
    print (response1)
    data = Format_ans(response1)
        #print(json.dumps(response1["records"][0][1]))
    
        #print(items)
    responseBody = json.dumps(data["Item"])
    response = {
        'statusCode': 200,
        'headers': {
            "content-type": "application/json",
            "access-control-allow-origin": "*"
            
        },
        'body': responseBody
    }
    return response
    
#def lambda_handler(event, context):
    # TODO implement
    #return {
     #   'statusCode': 200,
      #  'body': json.dumps('Hello from Lambda!')
    #}
