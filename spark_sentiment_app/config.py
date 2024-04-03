import os
from pathlib import Path

from dotenv import load_dotenv

try:
    load_dotenv()
except:
    pass

BASE_PATH = Path(__file__)
STORAGE_PATH = BASE_PATH.parent.parent.joinpath("storage")

DEBUG = os.getenv("DEBUG", "True").lower() == "true"

# Mongodb
MONGODB_URI = F'mongodb://{os.getenv("MONGODB_HOST")}:{os.getenv("MONGODB_PORT")}/{os.getenv("MONGODB_DB")}.{os.getenv("MONGODB_COLLECTION")}?authSource=admin'
# MONGODB_URI = F'mongodb://admin:admin@{os.getenv("MONGODB_HOST")}:{os.getenv("MONGODB_PORT")}/test.test?authSource=admin'

KAFKA_HOST = os.getenv("KAFKA_HOST", "localhost")
TOPIC_NAME = "mongodata"
KAFKA_CONFIG_READ = {
    'kafka.bootstrap.servers': f'{KAFKA_HOST}:9092',
    'subscribe': TOPIC_NAME,
    'groupIdPrefix': "spark_app",
    'maxOffsetsPerTrigger': 10,
    'startingOffsets': 'latest',
    'failOnDataLoss': 'false',
    'minPartitions': '5',
    # 'fetch.max.bytes': '10485760',
}

SPARK_CHECKPOINT_LOCATION = STORAGE_PATH.joinpath("checkpoints").joinpath(TOPIC_NAME)
