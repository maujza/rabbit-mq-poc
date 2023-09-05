Run:
    - docker-compose up -d

Make sure you copy the rabbitMQ/starrock connector jar to the spark master/worker nodes using this commands:
    - docker cp  spark/jars/starrocks-spark3_2.12-1.0.0.jar spark-master:/spark/jars/
    - docker cp  ./spark/jars/rabbitmq-connector-1.0-all.jar spark-master:/spark/jars/
    - docker cp  spark/jars/starrocks-spark3_2.12-1.0.0.jar spark-worker:/spark/jars/
    - docker cp  ./spark/jars/rabbitmq-connector-1.0-all.jar spark-worker:/spark/jars/
    # Please make sure you execute this command from correct 

Once system is up and running execute:
    - docker exec -it spark-master /bin/bash /spark/jobs/start.sh
    - docker exec -it spark-worker /bin/bash /spark/jobs/start.sh
    # Both commands need to be executed since it is a cluster.

Once all commands are executed, execute the following command to create database and table on starrocks:
    - docker exec -it starrock-app /bin/bash /jobs/start.sh
    
Create Rabbit QUEUE:
    - docker exec -it rabbitmq rabbitmqadmin declare queue name=sportsbook durable=true

Execute spark Job:
    - docker exec -it spark-master /spark/bin/spark-submit --master spark://spark-master:7077 /spark/jobs/insert_rabbit_json_starrocks.py

Execute Python job to send data to rabbit:
    - docker exec -it spark-master  python3  /spark/jobs/faking_trans.py

    ## Execute it as many times as needed to test rabbitMQ connector, change amount of data to send, as needed by test scenarios

Connect to the Data base and check transaction table to view insert:
    - docker exec -it starrock-app mysql -P9030 -h127.0.0.1 -uroot
    - use test;
    - select count(*) from transactions;

#Note : All jars must be loaded on spark jobs for cluster execution