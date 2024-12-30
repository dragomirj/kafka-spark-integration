# *****************************************************************************
#  Dragomir J. - Apache Spark Structured Streaming with Apache Kafka
# *****************************************************************************
from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StructField, TimestampType, FloatType, StringType
from pyspark.sql.functions import from_json, to_json, col, avg, window, round

# APACHE JAVA PACKAGES (IMPORTANT!)
packages = [
    'org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.0',
    'org.apache.kafka:kafka-clients:3.2.0'
]

spark = SparkSession.builder \
    .master('local[*]') \
    .appName('Kafka-Spark-Integration') \
    .config('spark.jars.packages', ',' . join(packages)) \
    .config('spark.streaming.stopGracefullyOnShutdown', True) \
    .getOrCreate()

# Data schema of our message on the Apache Kafka stream
schema = StructType([ 
    StructField('timestamp', TimestampType(), False), # NOT Nullable
    StructField('device_name', StringType(), False),  # NOT Nullable
    StructField('data', FloatType(), False)           # NOT Nullable
])

# Create a data frame from reading the Apache Kafka stream.
df = spark \
    .readStream \
    .format('kafka') \
    .option('kafka.bootstrap.servers', 'localhost:9092') \
    .option('subscribe', 'dj-kafka-spark-integration-input') \
    .option('startingOffsets', 'latest') \
    .option('failOnDataLoss', False) \
    .load() \
    .select(col('key').cast('string').alias('key'), # Key: [topic]/[device_name], Value: JSON string
        from_json(col('value').cast('string'), schema).alias('message')) \
    .select(col('key'), col('message.*')) # Convert all JSON keys to columns

# Create a data stream with the help of `withWatermark` and `window` functions
ds = df \
    .withWatermark('timestamp', '15 seconds') \
    .groupBy(col('device_name'), window(col('timestamp'), '15 seconds')) \
    .agg(avg(col('data')).alias('average')) # Calculate the mean value

# Round the average number to 3 decimals
ds = ds.withColumn('average', round(col('average'), 3))

# Write the data stream back to Apache Kafka
ds.selectExpr('to_json(struct(*)) AS value') \
    .writeStream \
    .format('kafka') \
    .outputMode('append') \
    .option('kafka.bootstrap.servers', 'localhost:9092') \
    .option('topic', 'dj-kafka-spark-integration-output') \
    .option('checkpointLocation', '/tmp/Apache_Spark') \
    .start() \
    .awaitTermination()