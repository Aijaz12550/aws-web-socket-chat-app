import json
import boto3
import os
from boto3.dynamodb.conditions import Key
dynamodb = boto3.client('dynamodb')
dynamodb_r = boto3.resource('dynamodb')

def message_handler(event, context):
    
    print("event", event)

    message = json.loads(event['body'])['message']
    
    paginator = dynamodb.get_paginator('scan')
    
    connectionIds = []

    apigatewaymanagementapi = boto3.client('apigatewaymanagementapi', 
    endpoint_url = "https://" + event["requestContext"]["domainName"] + "/" + event["requestContext"]["stage"])

    table_name = os.environ['SOCKET_CONNECTION_TABLE_NAME']
    # Retrieve all connectionIds from the database

    for page in paginator.paginate(TableName= table_name):
        connectionIds.extend(page['Items'])

    # Emit the recieved message to all the connected devices
    for connectionId in connectionIds:
        apigatewaymanagementapi.post_to_connection(
            Data=message,
            ConnectionId=connectionId['connectionId']['S']
        )
    

    return {}