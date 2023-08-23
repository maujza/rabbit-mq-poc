from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StructField, IntegerType, DoubleType, StringType

# Define the schema for the data
schema = StructType([
    StructField("key", IntegerType(), nullable=False),
    StructField("value", DoubleType(), nullable=False),
    StructField("value_string", StringType(), nullable=False)
])

# Initialize SparkSession
spark = SparkSession.builder \
    .appName("RabbitMQ Stream") \
    .config("spark.jars", "/opt/bitnami/spark/output/rabbitmq-connector-1.0-all.jar") \
    .getOrCreate()

# Define RabbitMQ connection configuration
rabbitmq_connection_config = {
    "host": "rabbitmq",
    "port": "5672",
    "username": "guest",
    "password": "guest",
    "queue_name": "message_queue",
    "exchange":"",
    "virtual_host": "/",
    "time_limit": "2000", # in millis
    "max_messages_per_partition": 2000
}

# Read from RabbitMQ topic using your custom data source
dataStreamWriter = (spark.readStream
  .format("rabbitmq")
  .options(**rabbitmq_connection_config)
  .schema(schema)
  .load()
  .writeStream
  .format("csv")
  .option("path", "/opt/bitnami/spark/output")  # path where the csv files will be stored
  .option("checkpointLocation", "/opt/bitnami/spark/output/checkpoint") 
  .trigger(processingTime="13 milliseconds")
  .outputMode("append")
)
# run the query
query = dataStreamWriter.start()

query.awaitTermination()
