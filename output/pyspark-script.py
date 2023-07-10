from pyspark.sql import SparkSession

# Initialize SparkSession
spark = SparkSession.builder \
    .appName("RabbitMQ Stream") \
    .getOrCreate()

# Define RabbitMQ connection configuration
rabbitmq_connection_config = {
    "host": "rabbitmq", # your RabbitMQ host
    "port": "5672", # your RabbitMQ port
    "username": "guest", # your RabbitMQ username
    "password": "guest", # your RabbitMQ password
    "queueName": "message_queue" # your RabbitMQ topic
}

# Read from RabbitMQ topic using your custom data source
df = spark \
    .readStream \
    .format("com.github.maujza.RabbitMQTableProvider") \
    .options(**rabbitmq_connection_config) \
    .load()

# Write stream data into a file
df.writeStream \
    .outputMode("append") \
    .format("csv") \
    .option("path", "output") \
    .option("checkpointLocation", "/output/checkpoints") \
    .start() \
    .awaitTermination()
