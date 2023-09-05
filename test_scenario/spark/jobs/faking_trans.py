import pika
import time
import random
import json
from faker import Faker
from datetime import datetime, timedelta

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='rabbitmq')
)
channel = connection.channel()

queue_name = "sportsbook"
channel.queue_declare(queue=queue_name, durable=True)

# Create an instance of the Faker class
fake = Faker()

# Define the range of dates to generate data for
start_date = datetime.now() - timedelta(days=365)
end_date = datetime.now()
i = 0
while i < 1:   
    data1 = {
    "name1": "Bruno Mars",   
    "specversion": 1,
    "baseWagerAmount": 10,
    "customerWagerAmount": 10
    }
    data = { 
    "specversion": 1,
    "baseWagerAmount": 10,
    "customerWagerAmount": 10
    }

    # Convert the Python dictionary to JSON format
    message = json.dumps(data1)
    
    channel.basic_publish(
        exchange='', routing_key=queue_name, body=message
    )
    print(" [x] Sent %r" % (message,))
    time.sleep(.001)
    i=i+1

connection.close()