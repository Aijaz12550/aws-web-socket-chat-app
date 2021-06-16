
import boto3
import json
import os

dynamodb = boto3.client('dynamodb')

def handle(event, ctx):

    print("event ==>", event)
    connectionId = event['requestContext']['connectionId']
    table_name = os.environ['SOCKET_CONNECTION_TABLE_NAME']

    res = dynamodb.put_item(TableName=table_name, Item={'connectionId': {"S": connectionId }} )

    print("res",res)
    return {
     "statusCode": 200,
     "body":"Hello from web socket"
    }
