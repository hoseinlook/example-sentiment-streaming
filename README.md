# Introduction
It is a simple spark streaming application to process some data using a simple sentiment model and produce result to a kafka topic.


# How To Deploy With Docker
To install and deploy, we have provided a `docker-compose.yaml` that contains services such as kafka,mongodb and spark.
Also, to run in local you should consider the python version must be 3.8
### Note
Please consider that you should create a `.env` file, you can use `.env.example` file as an example.
```bash
cp .env.example .env
```

To deploy use this command:
```bash
sudo docker-compose up
```

# Submit an application to run
```bash
cd spark_sentiment_app/
zip -r your_project.zip .
cd ../
spark-submit --master spark://localhost:7077  --packages org.mongodb.spark:mongo-spark-connector_2.12:10.2.2,org.apache.spark:spark-sql-kafka-0-10_2.12:3.2.4   --py-files spark_sentiment_app/your_project.zip   spark_sentiment_app/main.py

```

# Initial
To write new data to kafka use `producer.py`

# Run
```bash
python3 spark_sentiment_app/main.py
```


# Improvement
To improve code and structure there are some advice:
+ To define schema instead of hard coding we can use schema registry connection
+ To deploy spark we can use spark on kuber(to have a better isolation) or spark on yarn (to have better data locality)
+ 

# Note
+ Latest mongodb-spark-connector supports spark 3.2.4
+ Java version must be 8 or 11