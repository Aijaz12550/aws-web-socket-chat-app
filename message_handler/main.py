import json
import boto3
import os
from boto3.dynamodb.conditions import Key


dynamodb = boto3.client('dynamodb')
resource = boto3.resource('dynamodb')
table_re = resource.Table(os.environ['SOCKET_CONNECTION_TABLE_NAME'])

def message_handler(event, context):
    
    print("event", event)

    print("table",table_re)

    message = json.loads(event['body'])['message']
    
    paginator = dynamodb.get_paginator('scan')
    
    connectionIds = []

    apigatewaymanagementapi = boto3.client('apigatewaymanagementapi', 
    endpoint_url = "https://" + event["requestContext"]["domainName"] + "/" + event["requestContext"]["stage"])

    table_name = os.environ['SOCKET_CONNECTION_TABLE_NAME']

    # querying to global Index
    dsi_data = table_re.query(
        IndexName='user_name_index',
        KeyConditionExpression=Key('user_name').eq('aijaz')
    )

    print("dsi_data",dsi_data)

    


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