import json
import threading
import time

from kafka import KafkaAdminClient, KafkaProducer
from kafka.admin import NewTopic


class Producer(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.stop_event = threading.Event()

    def stop(self):
        self.stop_event.set()

    def run(self):
        producer = KafkaProducer(bootstrap_servers='localhost:9092',
                                 value_serializer=lambda v: json.dumps(v).encode('utf-8'))

        with open("example_data.json") as file:
            data = file.read()
            print(data)
            data = json.loads(data)
        # data = json.loads("./data.json")

        for record in data:
            print("inserting record id", record["id"], '& text:', '"', record['text'], '"')
            producer.send(topic="mongodata", value=record)
        # while not self.stop_event.is_set():
        #     last_query_time = 0
        #     while True:
        #         now = time.time()
        #         cursor = mydb.geodb.find({'date': {'$gt': last_query_time}})
        #         last_query_time = now
        #         for document in cursor:
        #             print(document)
        #             document['_id'] = str(document['_id'])
        #             producer.send(Topic, document)
        #             time.sleep(1)
        #         time.sleep(1)
        producer.close()


def main():
    # Create 'my-topic' Kafka topic
    try:
        admin = KafkaAdminClient(bootstrap_servers='localhost:9092')

        topic = NewTopic(name="mongodata",
                         num_partitions=1,
                         replication_factor=1)
        admin.create_topics([topic])
    except Exception:
        pass

    tasks = [
        Producer(),
    ]

    # Start threads of a publisher/producer and a subscriber/consumer to 'my-topic' Kafka topic
    for t in tasks:
        t.start()

    time.sleep(3)
    # Stop threads
    for task in tasks:
        task.stop()
    for task in tasks:
        task.join()


if __name__ == "__main__":
    main()
