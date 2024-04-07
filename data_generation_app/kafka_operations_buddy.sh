#!/bin/bash

# Functions for Kafka operations

create_topic() {
    echo "Enter the name of the topic to create:"
    read topic_name
    echo "Enter the replication factor:"
    read replication_factor
    echo "Enter the partition count:"
    read partition_count
    kafka_2.12-3.0.0/bin/kafka-topics.sh --bootstrap-server localhost:9093 --create --topic $topic_name --partitions $partition_count --replication-factor $replication_factor
}
list_topics() {
    kafka_2.12-3.0.0/bin/kafka-topics.sh --bootstrap-server localhost:9093 --list
}

produce_topic() {
    echo "Enter the name of the topic to produce to:"
    read topic_name
    kafka_2.12-3.0.0/bin/kafka-console-producer.sh --bootstrap-server localhost:9093 --topic $topic_name
}

consume_topic() {
    echo "Enter the name of the topic to consume from:"
    read topic_name
    kafka_2.12-3.0.0/bin/kafka-console-consumer.sh --bootstrap-server localhost:9093 --topic $topic_name --from-beginning --property print.key=true --property print.value=true
}


# Main menu
while true; do
    echo "Select an operation:"
    echo "1. Create Topic"
    echo "2. List Topics"
    echo "3. Produce Topic"
    echo "4. Consume Topic"
    echo "5. Exit"
    read choice

    case $choice in
        1) create_topic ;;
        2) list_topics ;;
        3) produce_topic ;;
        4) consume_topic ;;
        5) echo "Exiting..."; exit ;;
        *) echo "Invalid choice";;
    esac
done
