import json
import boto3
import os

dynamodb = boto3.client('dynamodb')


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
    
    # testing secondary indexing
    table = dynamodb.Table(table_name)
    response = table.query(
    IndexName='video_id-index',
    KeyConditionExpression=Key('video_id').eq(video_id)
)

    return {}