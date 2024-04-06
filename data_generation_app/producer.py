import json
import threading
import time

from kafka import KafkaAdminClient, KafkaProducer
from kafka.admin import NewTopic

BOOTSTRAP_SERVERS = 'localhost:9092'


class Producer:

    def __init__(self):
        self._producer = KafkaProducer(bootstrap_servers=BOOTSTRAP_SERVERS,
                                       value_serializer=lambda v: json.dumps(v).encode('utf-8'))

    def run(self):
        with open("example_data.json") as file:
            data = file.read()
            print(data)
            data = json.loads(data)
        # data = json.loads("./data.json")

        for record in data:
            print("inserting record id", record["id"], '& text:', '"', record['text'], '"')
            self._producer.send(topic="mongodata", value=record)

        self._producer.close()


def main():
    new_topic = "mongodata"
    # Create 'my-topic' Kafka topic

    admin = KafkaAdminClient(bootstrap_servers=BOOTSTRAP_SERVERS)

    topic = NewTopic(name=new_topic,
                     num_partitions=1,
                     replication_factor=1)
    print(admin.list_topics())
    if new_topic not in admin.list_topics():
        admin.create_topics([topic], )

    Producer().run()


if __name__ == "__main__":
    main()
