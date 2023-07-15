from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StructField, IntegerType, DoubleType

# Define the schema for the data
schema = StructType([
    StructField("key", IntegerType(), nullable=False),
    StructField("value", DoubleType(), nullable=False)
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
    "virtual_host": "/"
}

# Read from RabbitMQ topic using your custom data source
dataStreamWriter = (spark.readStream
  .format("rabbitmq")
  .options(**rabbitmq_connection_config)
  .schema(schema)
  .load()
  .writeStream
  .format("console")
  .trigger(processingTime="10 second")
  .outputMode("append")
)
# run the query
query = dataStreamWriter.start()

query.awaitTermination()
