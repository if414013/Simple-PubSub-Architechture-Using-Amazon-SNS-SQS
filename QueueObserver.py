import boto3
import time
import os

from base64 import b64decode
from urlparse import parse_qs

#set glob var
sqs_client = boto3.resource(
    'sqs',
    aws_access_key_id='CHANGE_ME',
    aws_secret_access_key='CHANGE_ME'
)
dead_letter_queue_url = "CHANGE_ME"
main_queue_url = "CHANGE_ME"

while(True):
    dead_letter_queue = sqs_client.Queue(dead_letter_queue_url)
    main_queue = sqs_client.Queue(main_queue_url)
    print("================================================MAIN QUEUE STATUS===================================================")
    print("Message Available                 : " + main_queue.attributes['ApproximateNumberOfMessages'])
    print("In-Flight(Processing) Message     : " + main_queue.attributes['ApproximateNumberOfMessagesNotVisible'])
    print("====================================================================================================================")

    print("\n\n")

    print("============================================DEAD LETTER QUEUE STATUS================================================")
    print("Message Available                 : " + dead_letter_queue.attributes['ApproximateNumberOfMessages'])
    print("In-Flight(Processing) Message     : " + dead_letter_queue.attributes['ApproximateNumberOfMessagesNotVisible'])
    print("====================================================================================================================")
    time.sleep(1)
    os.system('clear')

    
