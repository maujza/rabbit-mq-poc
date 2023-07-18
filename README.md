# RabbitMQ / Spark POC

## Description
This project sets up a Docker Compose environment for publishing messages to a RabbitMQ queue and consuming them using Apache Spark with a custom Spark connector built using the v2 Data Source API to finally save them in a CSV.

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

3. To stop and remove all containers, networks, and volumes created by Docker Compose, run:

```
docker-compose down --volumes --rmi all
```

This command will stop and remove all containers and clean up any associated volumes and images.

## Custom Spark Connector

The custom Spark connector is implemented in the `pyspark-script.py` file and utilized by the Apache Spark container to consume messages from RabbitMQ. The `rabbitmq-connector-1.0-all.jar` is the JAR file for the custom connector.