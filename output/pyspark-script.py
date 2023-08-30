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
    "exchange": "",
    "virtual_host": "/",
    # "time_limit": "2000",  # in millis, optional
    # "max_messages_per_partition": 2000 # optional
}

def write_to_console(batch_df, batch_id):
    batch_df.cache()  # Cache the DataFrame
    batch_df.show(truncate=False)
    num_rows = batch_df.count()
    batch_df.unpersist()  # Unpersist the DataFrame to free up memory

# Read from RabbitMQ topic using your custom data source
dataStream = (spark.readStream
  .format("rabbitmq")
  .options(**rabbitmq_connection_config)
  .schema(schema)
  .load()
)

dataStream.writeStream.foreachBatch(write_to_console).outputMode("append").start().awaitTermination()
