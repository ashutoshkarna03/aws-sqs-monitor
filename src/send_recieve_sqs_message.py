import boto3
import os
from dotenv import load_dotenv
from pprint import pprint

# load environment files
load_dotenv()

# Get the service resource
sqs = boto3.resource('sqs')

# Get the queue. This returns an SQS.Queue instance
queue = sqs.get_queue_by_name(QueueName=os.getenv('QUEUE_NAME'))


def send_message(messages):
    """
    send message to the queue
    :param messages: list of messgaes to be sent. Example: ['a', 'b', 'c', ...]
    :return: true if messages were sent else false
    """
    # prepare list to be fed to send_message method of sqs
    payload = [
        dict(Id=str(i+1), MessageBody=messages[i])
        for i in range(len(messages))
    ]
    response = queue.send_messages(Entries=payload)
    if response['ResponseMetadata']['HTTPStatusCode'] == 200:
        if 'Successful' in response:
            if len(response['Successful']) == len(messages):
                return True
        else:
            return False
    else:
        return False


def recieve_message(with_attribute=False):
    # Process messages by printing out body and optional author name
    if with_attribute:
        for message in queue.receive_messages(MessageAttributeNames=['cool']):
            # Get the custom author message attribute if it was set
            author_text = ''
            if message.message_attributes is not None:
                author_name = message.message_attributes.get('cool').get('StringValue')
                if author_name:
                    author_text = ' ({0})'.format(author_name)

            # Print out the body and author (if set)
            print('Hello, {0}!{1}'.format(message.body, author_text))

            # Let the queue know that the message is processed
            # message.delete()
    else:
        print("##################")
        # print(type(queue.receive_messages()))
        # pprint(queue.receive_messages())
        print('=============')
        for message in queue.receive_messages():
            pprint(message.body)
            message.delete()
            print("---------------")
        print("##################")


if __name__ == '__main__':
    # recieve_message()
    result = send_message(['a', 'b'])
    print(result)
