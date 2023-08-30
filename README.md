# RabbitMQ / Spark POC

## Description
This project sets up a Docker Compose environment for publishing messages to a RabbitMQ queue and consuming them using Apache Spark with a custom Spark connector (https://github.com/maujza/rabbitmq-connector) built using the v2 Data Source API to finally save them in a CSV.

### Important Note

At this time, only micro-batching is supported by the custom Spark connector. By default, the connector is set with a maximum of 1000 messages per micro-batch and a 2-second time limit for default, this can be changes in the script

Warning: RabbitMQ does not handle offsets, which means once a message is consumed from the queue, it cannot be re-read. Be cautious when performing actions in your Spark jobs that could consume the data, as you cannot recompute or re-read input data. This is particularly important if you call multiple actions (e.g., count(), show()) on the same DataFrame in your Spark script. In summary, avoid calling multiple actions on the same DataFrame within the foreachBatch function unless you cache it first. If you must call multiple actions, consider using cache() to persist the DataFrame.

## Project Structure
The project has the following structure:

- Dockerfile.publisher: Dockerfile for building the Python publisher container that publishes messages to RabbitMQ.
- Dockerfile.spark: Dockerfile for building the Apache Spark container used for consuming messages from RabbitMQ.
- docker-compose.yaml: Docker Compose configuration file defining the services and their dependencies.
- output/: Directory containing files used by the Spark job and Python publisher.
    - pyspark-script.py: The custom Spark connector script that consumes messages from RabbitMQ using the v2 Data Source API.
    - rabbitmq-connector-1.0-all.jar: JAR file for the custom Spark connector.
- publisher.py: Python script for the publisher application that sends messages to RabbitMQ.
- requirements.txt: Python dependencies required for the Python publisher.

## Usage

1. Clone the repository to your local machine:

```
git clone https://github.com/maujza/rabbit-mq-poc.git
cd rabbit-mq-poc
```

2. Build and run the Docker Compose environment:

```
docker-compose up --build
```

This command will create and start the RabbitMQ, Python publisher, and Apache Spark containers as defined in the `docker-compose.yaml` file. The Python publisher will publish messages to the RabbitMQ queue, and the Spark container will consume and process those messages using the custom Spark connector.

3. To run the Spark job defined in our `pyspark-script.py` located in the "output/" folder, we must first access the Spark master container:

```bash
docker exec -it spark-master-container /bin/bash
```

4. Once inside the container, submit the Spark job using the following command:

```bash
spark-submit --jars output/rabbitmq-connector-1.0-all.jar output/pyspark-script.py
```

Please note that running the Spark job will generate a lot of partitioned CSV files in the "output/" folder.

5. To stop and remove all containers, networks, and volumes created by Docker Compose, run:

```
docker-compose down --volumes --rmi all
```

This command will stop and remove all containers and clean up any associated volumes and images.

## Custom Spark Connector

The custom Spark connector is implemented in the `pyspark-script.py` file and utilized by the Apache Spark container to consume messages from RabbitMQ. The `rabbitmq-connector-1.0-all.jar` is the JAR file for the custom connector. Source code can be found here https://github.com/maujza/rabbitmq-connector
```