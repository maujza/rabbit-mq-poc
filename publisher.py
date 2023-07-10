import pika
import time
import random
import json

def random_message():
    return json.dumps({
        "key": random.randint(1, 1000),
        "value": random.random(),
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
    time.sleep(1)

connection.close()