import pika
import time
import random
import json

import random
import string

def generate_random_string(length):
    letters = string.ascii_letters
    result_str = ''.join(random.choice(letters) for i in range(length))
    return result_str

def random_message():
    return json.dumps({
        "key": random.randint(1, 1000),
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
    message = random_message()
    channel.basic_publish(
        exchange='', routing_key=queue_name, body=message
    )
    print(" [x] Sent %r" % (message,))
    time.sleep(.001)

connection.close()