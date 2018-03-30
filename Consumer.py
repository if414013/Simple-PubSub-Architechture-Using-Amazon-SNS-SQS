import boto3
import time
import os
import sys

from base64 import b64decode
from urlparse import parse_qs

#set glob var
sqs_client = boto3.client(
    'sqs',
    aws_access_key_id='CHANGE_ME',
    aws_secret_access_key='CHANGE_ME'
)
dead_letter_queue_url = "CHANGE_ME"
main_queue_url = "CHANGE_ME"

is_delete_message_enabled = True
queue_used = main_queue_url
if (len(sys.argv) < 2):
    print("Please specify which queue that we want to consume (maing_queue or dead_letter_queue) after python filename")
    print('Valid command was \"python Consumer.py [main_queue | dead_letter_queue]\"  or')
    print('Valid command was \"python Consumer.py [main_queue | dead_letter_queue] [True | False]\"')
    exit(0)
elif (sys.argv[1] != "main_queue" and sys.argv[1] != "dead_letter_queue"):
    print('Valid command was \"python Consumer.py [main_queue | dead_letter_queue]\"  or')
    print('Valid command was \"python Consumer.py [main_queue | dead_letter_queue] [True | False]\" ')
    exit(0)

if (sys.argv[1] == "dead_letter_queue"):
    queue_used = dead_letter_queue_url

if (len(sys.argv)==3 and (sys.argv[2]==True or sys.argv[2]==False)):
    is_delete_message_enabled = sys.argv[2]

total_message_count = 0
while(True):
    start_time = time.time()
    messages = sqs_client.receive_message(QueueUrl=queue_used,MaxNumberOfMessages=1) # adjust MaxNumberOfMessages if needed
    end_time = time.time()
    print("Consume message from " + sys.argv[1])
    print("Message Consumed Number     : " + str(total_message_count))
    print("Message Waiting Latency     : " + str(end_time - start_time))
    print("====================================================================================================================")
    print("\n\n")
    if 'Messages' in messages: 
        for message in messages['Messages']:
            total_message_count = total_message_count + 1
            # next, we delete the message from the queue so no one else will process it again
            # we need to set to false iw want to simulate the dead queue letter usage
            if(is_delete_message_enabled):
                sqs_client.delete_message(QueueUrl=queue_used,ReceiptHandle=message['ReceiptHandle'])
    else:
        print('Queue is now empty!!!')
    time.sleep(1)
    os.system('clear')
    

    
