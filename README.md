# Introduction
It is a simple spark streaming application to process some data using a simple sentiment model and produce result to a kafka topic.


# How To Deploy With Docker
To install and deploy, we have provided a `docker-compose.yaml` that contains services such as kafka,mongodb and spark.
### Note
Please consider that you should create a `.env` file, you can use `.env.example` file as an example.
```bash
cp .env.example .env
```

To deploy use this command:
```bash
sudo docker-compose up
```



