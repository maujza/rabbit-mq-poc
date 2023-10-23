import pika
import time
import json
import string
import random

# Define a global variable for the message key
message_key = 0


def generate_random_string(length):
    letters = string.ascii_letters
    result_str = "".join(random.choice(letters) for i in range(length))
    return result_str


def random_message():
    global message_key  # Declare the variable as global so we can modify it

    # Increment the message key by 1
    message_key += 1

    return json.dumps(
        {
            "customerid": "B3768689",
            "datacontenttype": "application/json",
            "id": "454364483-1\_002b0eab000092f80002",
            "producttype": "SportsBook",
            "source": "/SportsBook.Bet.Hydrate.Service",
            "specversion": "1.0",
            "subject": "BetEventResponseDto",
            "time": "2023-08-25T11:53:13.2627129Z",
            "traceid": "42735fd79e8d01d0b9f9d35132ca01f8",
            "traceparent": "00-42735fd79e8d01d0b9f9d35132ca01f8-361f8e4dd0d54ce6-01",
            "type": "bet-settled-reversal",
            "Transaction": {
                "BaseAmount": 0,
                "CustomerAmount": 0,
                "Date": "2023-08-25T11:53:13.2608732Z",
            },
        }
    )


connection = pika.BlockingConnection(pika.ConnectionParameters(host="rabbitmq"))
channel = connection.channel()

queue_name = "message_queue"
channel.queue_declare(queue=queue_name)

while True:
    time.sleep(5)
    message = random_message()
    channel.basic_publish(exchange="", routing_key=queue_name, body=message)
    print(" [x] Sent %r" % (message,))


connection.close()
