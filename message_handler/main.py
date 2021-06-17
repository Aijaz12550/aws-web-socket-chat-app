import json
import boto3
import os
from boto3.dynamodb.conditions import Key
import _thread

dynamodb = boto3.client('dynamodb')
resource = boto3.resource('dynamodb')
table_re = resource.Table(os.environ['SOCKET_CONNECTION_TABLE_NAME'])


def message_handler(event, context):

    print("event", event)

    print("table", table_re)

    message = json.loads(event['body'])['message']

    # sender socket id
    sender_socket_id = event['requestContext']['connectionId']
    print("sender_socket_id", sender_socket_id)
    paginator = dynamodb.get_paginator('scan')

    connection_ids = []

    apigatewaymanagementapi = boto3.client('apigatewaymanagementapi',
                                           endpoint_url="https://" + event["requestContext"]["domainName"] + "/" + event["requestContext"]["stage"])

    table_name = os.environ['SOCKET_CONNECTION_TABLE_NAME']

    # querying to global Index
    dsi_data = table_re.query(
        IndexName='user_name_index',
        KeyConditionExpression=Key('user_name').eq('aijaz')
    )

    print("dsi_data", dsi_data)

    # Retrieve all connectionIds from the database

    for page in paginator.paginate(TableName=table_name):
        connection_ids.extend(page['Items'])

    def send_multi_message(message,test):
        for j in range(1000):
            apigatewaymanagementapi.post_to_connection(
                Data=f'{j}',
                ConnectionId=connection_id['connectionId']['S']
            )

    # Emit the recieved message to all the connected devices
    for connection_id in connection_ids:
        print("connection_id", connection_id)

        if sender_socket_id != connection_id["connectionId"]["S"]:
            _thread.start_new_thread(send_multi_message,("test","test"))
            apigatewaymanagementapi.post_to_connection(
                Data=message,
                ConnectionId=connection_id['connectionId']['S']
            )

    return {}
