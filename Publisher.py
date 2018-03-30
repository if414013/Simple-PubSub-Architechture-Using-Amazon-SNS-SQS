import boto3
import time
import os

from base64 import b64decode
from urlparse import parse_qs

#set glob var
sns_client = boto3.client(
    'sns',
    aws_access_key_id='CHANGE_ME',
    aws_secret_access_key='CHANGE_ME'
)

sns_arn = "CHANGE_ME"

def publish_message(message):
    sns_client.publish(
        TopicArn=sns_arn,
        Message=message,
        MessageStructure='string'
    )

message_count = 0
while(True):
    start_time = time.time()
    publish_message("Message Test")
    end_time = time.time()
    message_count = message_count + 1
    print("Total Message Send   : " + str(message_count))
    print("Message Send Latency : " + str(end_time - start_time) + "ms")
    time.sleep(1)
    os.system('clear')

    
