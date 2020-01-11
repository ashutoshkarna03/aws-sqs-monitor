"""
Author: Ashutosh Karna
This module gets real time value of message recieved in sqs queue and then sets alarm accordingly
You need to create .env file with following structure:
AWS_ACCESS_KEY_ID=kyour_key
AWS_SECRET_ACCESS_KEY=your_secret_key
AWS_DEFAULT_REGION=your_region
QUEUE_NAME=your_queue_name
"""

import boto3
import os
from dotenv import load_dotenv
from pprint import pprint
from time import sleep

# load environment files
load_dotenv()

# Get the service resource
sqs = boto3.resource('sqs')

# Get the queue. This returns an SQS.Queue instance
queue = sqs.get_queue_by_name(QueueName=os.getenv('QUEUE_NAME'))


def get_queue_attributes(threshold_for_alarm):
    attribute = queue.attributes
    current_no_of_message = int(attribute['ApproximateNumberOfMessages'])
    print("ApproximateNumberOfMessages: ", current_no_of_message)
    print("----------------------------------------------------")
    if current_no_of_message > threshold_for_alarm:
        print("Alarm!!!")
        print("----------------------------------------------------")


if __name__ == '__main__':
    while True:
        get_queue_attributes(threshold_for_alarm=2)
        sleep(60)
