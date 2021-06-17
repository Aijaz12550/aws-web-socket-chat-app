import json
import boto3
import os

dynamodb = boto3.client('dynamodb')

def handle(event, context):
    connectionId = event['requestContext']['connectionId']

    print("connectionId",connectionId)

    # Delete connectionId from the database
    dynamodb.delete_item(TableName=os.environ['SOCKET_CONNECTION_TABLE_NAME'], Key={'connectionId': {'S': connectionId}})

    return {}