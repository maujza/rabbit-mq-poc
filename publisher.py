import pika
import time
import json
import string
import random

# Define a global variable for the message key
message_key = 0

def generate_random_string(length):
    letters = string.ascii_letters
    result_str = ''.join(random.choice(letters) for i in range(length))
    return result_str

def random_message():
    global message_key  # Declare the variable as global so we can modify it

    # Increment the message key by 1
    message_key += 1

    return json.dumps({
        "key": message_key,
        "value": random.random(),
        "value_string": generate_random_string(10)
    })

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='rabbitmq')
)
channel = connection.channel()

queue_name = "message_queue"
channel.queue_declare(queue=queue_name)

while True:
    time.sleep(60)
    message = random_message()
    channel.basic_publish(
        exchange='', routing_key=queue_name, body=message
    )
    print(" [x] Sent %r" % (message,))
    

connection.close()
