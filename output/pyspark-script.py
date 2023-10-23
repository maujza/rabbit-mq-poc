from pyspark.sql import SparkSession
from pyspark.sql.types import (
    StructType,
    StructField,
    IntegerType,
    DoubleType,
    StringType,
)

# Define the schema for the data
schema = StructType(
    [
        StructField("customerid", StringType(), nullable=True),
        StructField("datacontenttype", StringType(), nullable=True),
        StructField("id", StringType(), nullable=True),
        StructField("producttype", StringType(), nullable=True),
        StructField("source", StringType(), nullable=True),
        StructField("specversion", StringType(), nullable=True),
        StructField("subject", StringType(), nullable=True),
        StructField("time", StringType(), nullable=True),
        StructField("traceid", StringType(), nullable=True),
        StructField("traceparent", StringType(), nullable=True),
        StructField("type", StringType(), nullable=True),
        StructField(
            "Transaction",
            StructType(
                [
                    StructField("BaseAmount", IntegerType(), nullable=True),
                    StructField("CustomerAmount", IntegerType(), nullable=True),
                    StructField("Date", StringType(), nullable=True),
                ]
            ),
            nullable=True,
        ),
    ]
)

# Initialize SparkSession
spark = (
    SparkSession.builder.appName("RabbitMQ Stream")
    .config("spark.jars", "/opt/bitnami/spark/output/rabbitmq-connector-1.0-all.jar")
    .getOrCreate()
)

rabbitmq_connection_config = {
    "hostname": "rabbitmq",
    "port": "5672",
    "username": "guest",
    "password": "guest",
    "queue": "message_queue",
    "exchange": "",
    "virtualHost": "/",
    "time_limit": "1000",  # in millis, optional
    # "max_messages_per_partition": 2000 # optional
}

def write_to_console(batch_df, batch_id):
    batch_df.cache()  # Cache the DataFrame
    batch_df.show(truncate=False)
    num_rows = batch_df.count()
    batch_df.unpersist()  # Unpersist the DataFrame to free up memory

# Read from RabbitMQ topic using your custom data source
dataStream = (
    spark.readStream.format("rabbitmq")
    .options(**rabbitmq_connection_config)
    .schema(schema)
    .load()
)

dataStream.writeStream.foreachBatch(write_to_console).outputMode(
    "append"
).start().awaitTermination()
