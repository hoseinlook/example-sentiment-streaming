import pyspark.sql.functions as f
from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StructField, StringType, IntegerType

from spark_sentiment_app.config import DEBUG, MONGODB_URI, KAFKA_CONFIG_READ, SPARK_CHECKPOINT_LOCATION

"""
./bin/pyspark --conf "spark.mongodb.read.connection.uri=mongodb://127.0.0.1/test.myCollection?readPreference=primaryPreferred" \
              --conf "spark.mongodb.write.connection.uri=mongodb://127.0.0.1/test.myCollection" \
              --packages org.mongodb.spark:mongo-spark-connector_2.12:10.2.2
"""

"""
Create Spark Session
"""
if DEBUG:

    spark = SparkSession.builder \
        .master("local[*]") \
        .config("spark.app.name", "sentiment") \
        .config("spark.jars.packages", "org.apache.spark:spark-sql-kafka-0-10_2.12:3.1.1,org.mongodb.spark:mongo-spark-connector_2.12:10.2.2") \
        .config("spark.mongodb.read.connection.uri", MONGODB_URI) \
        .config("spark.mongodb.write.connection.uri", MONGODB_URI) \
        .getOrCreate()

else:
    spark = SparkSession.builder.getOrCreate()

# Create Schema
schema = StructType([
    StructField("Name", StringType(), True),
    StructField("Age", IntegerType(), True),
    StructField("City", StringType(), True)
])

# ReadStream from kafka
df = spark.readStream.format('kafka').options(**KAFKA_CONFIG_READ).load()
df = df.withColumn("data", f.from_json(f.col("value").cast("string"), schema=schema))
df = df.select("data.*")

# WriteStream to mongodb
query_mongo = df.writeStream.format("mongodb") \
    .outputMode("append") \
    .option("checkpointLocation", SPARK_CHECKPOINT_LOCATION) \
    .trigger(processingTime="1 seconds").start()

query_mongo.awaitTermination()
