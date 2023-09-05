from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StructField, IntegerType, DoubleType, StringType

# Define the schema for the data
schema1 = StructType([
    StructField("name1", StringType(), nullable=False),
    StructField("specversion", IntegerType(), nullable=False),
    StructField("baseWagerAmount", IntegerType(), nullable=False),
    StructField("customerWagerAmount", IntegerType(), nullable=False)
])

schema = StructType([
    StructField("specversion", IntegerType(), nullable=False),
    StructField("baseWagerAmount", IntegerType(), nullable=False),
    StructField("customerWagerAmount", IntegerType(), nullable=False)
])

# Initialize SparkSession
spark = SparkSession.builder \
    .appName("RabbitMQ Stream") \
    .config("spark.jars", "/spark/jars/rabbitmq-connector-1.0-all.jar") \
    .getOrCreate()

# Define RabbitMQ connection configuration
rabbitmq_connection_config = {
    "host": "rabbitmq",
    "port": "5672",
    "username": "guest",
    "password": "guest",
    "queue_name": "sportsbook",
    "exchange":"",
    "virtual_host": "/",
    "time_limit": "2000", # in millis
    "max_messages_per_partition": 200
}

# Read from RabbitMQ topic using your custom data source
dataStreamReader = (spark.readStream
  .format("rabbitmq")
  .options(**rabbitmq_connection_config)
  .schema(schema1)
  .load()
)

# specify connection data
options = {}
options["spark.starrocks.conf"] = "write"
options["spark.starrocks.write.fe.urls.http"] = "starrock-app:8030"
options["spark.starrocks.write.fe.urls.jdbc"] = "jdbc:mysql://starrock-app:9030/test"
options["spark.starrocks.write.database"] = "test"
options["spark.starrocks.write.table"] = "transactions1"
options["spark.starrocks.write.username"] = "root"
options["spark.starrocks.write.password"] = ""

# specify columns and types
options["spark.starrocks.write.columns"] = "name1,specversion,baseWagerAmount,customerWagerAmount"
#options["spark.starrocks.write.columns"] = "specversion,baseWagerAmount,customerWagerAmount"
options["spark.starrocks.write.column.name1.type"] = "string"
options["spark.starrocks.write.column.specversion.type"] = "integer"
options["spark.starrocks.write.column.baseWagerAmount.type"] = "integer"
options["spark.starrocks.write.column.customerWagerAmount.type"] = "integer"
options["spark.starrocks.infer.columns"] = "name1,specversion,baseWagerAmount,customerWagerAmount"
#options["spark.starrocks.infer.columns"] = "specversion,baseWagerAmount,customerWagerAmount"
options["spark.starrocks.write.column.name1.type"] = "string"
options["spark.starrocks.infer.column.specversion.type"] = "integer"
options["spark.starrocks.infer.column.baseWagerAmount.type"] = "integer"
options["spark.starrocks.infer.column.customerWagerAmount.type"] = "integer"
options["checkpointLocation"] = "/tmp/"

use_csv = False

if use_csv:
    options["spark.starrocks.write.properties.format"] = "csv"
    options["spark.starrocks.write.properties.columnSeparator"] =","
    options["spark.starrocks.write.properties.column_separator"] =","
else:
    options["spark.starrocks.write.properties.format"] = "json"

options["spark.starrocks.write.ctl.enable-transaction"] = True
#dataStreamReader.writeStream.format("starrocks_writer").options(**options).start().awaitTermination()
#dataStreamReader.writeStream.format("console").start().awaitTermination()
def write_to_console(batch_df, batch_id):
    batch_df.cache()  # Cache the DataFrame
    batch_df.show(truncate=False)
    num_rows = batch_df.count()
    print(f"-------------------------Number of rows: {num_rows}")
    batch_df.unpersist()  # Unpersist the DataFrame to free up memory

# Escribe los datos en la consola utilizando foreachBatch
dataStreamReader.writeStream.foreachBatch(write_to_console).trigger(processingTime="1 second").start().awaitTermination()
#dataStreamReader.writeStream.format("console").trigger(processingTime="1 second").outputMode("append").start().awaitTermination()

spark.stop()