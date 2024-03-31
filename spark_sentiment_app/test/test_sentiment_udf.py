from pyspark.sql import SparkSession

from pyspark.sql import SparkSession

from spark_sentiment_app.config import MONGODB_URI
from spark_sentiment_app.sentiment_transformer import sentiment_calculate_udf

"""
./bin/pyspark --conf "spark.mongodb.read.connection.uri=mongodb://127.0.0.1/test.myCollection?readPreference=primaryPreferred" \
              --conf "spark.mongodb.write.connection.uri=mongodb://127.0.0.1/test.myCollection" \
              --packages org.mongodb.spark:mongo-spark-connector_2.12:10.2.2
"""

"""
Create Spark Session
"""

spark = SparkSession.builder \
    .master("local[*]") \
    .config("spark.app.name", "sentiment") \
    .config("spark.jars.packages", "org.apache.spark:spark-sql-kafka-0-10_2.12:3.1.1,org.mongodb.spark:mongo-spark-connector_2.12:10.2.2") \
    .config("spark.mongodb.read.connection.uri", MONGODB_URI) \
    .config("spark.mongodb.write.connection.uri", MONGODB_URI) \
    .getOrCreate()

df = spark.read.json("./example_data.json")

df = df.withColumn("sentiment_result", sentiment_calculate_udf("_id"))
df.show()
