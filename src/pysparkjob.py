#!/usr/bin/python

import sys
from pyspark.sql import SparkSession
from pyspark.sql.functions import *
from pyspark.sql.types import *
from datetime import datetime, timedelta

#get data source from bash
data_source = sys.argv[1]
# data_source = '../Data/' 

# spark = SparkSession \
#   .builder \
#   .master('yarn') \
#   .appName('spark-bigquery-demo') \
#   .getOrCreate()

spark = SparkSession.builder.getOrCreate()

# Use the Cloud Storage bucket for temporary BigQuery export data used
# by the connector. 
spark.conf.set('temporaryGcsBucket', 'gs://${PROJECT_ID}/temporary_file/')

#extract data from data input (data_source on gcs)
data = spark.read.json(data_source)

#transform data
#in json file, "airline_code" field is string type so we need to change it into integer
data = data.withColumn("airline_code", data.airline_code.cast(IntegerType()))

#create function to create new column actual date for depart or arrival datetime
def actual_datetime(date, time, addminute):
    date = date.split('-')
    year = int(date[0])
    month = int(date[1])
    day = int(date[2])
    time = str(time)
    try:
        hour = int(time[-4:-2])
    except:
        hour = 0
    minute = int(time[-2:])
    date = datetime(year, month, day, hour, minute)
    return date + timedelta(minutes=addminute)

#define udf(user defined function to call function actual_datetime)
convert = udf(actual_datetime, TimestampType())

#applying actual_datetime function on new column
data = data.withColumn("actual_depart_datetime", convert(data.flight_date, data.departure_time, data.departure_delay))
data = data.withColumn("actual_arrive_datetime", convert(data.flight_date, data.arrival_time, data.arrival_delay))

#selecting data to load into BigQuery
data = data.select(col("id"), col("airline_code"), col("flight_num"),
                   col("source_airport"), col("destination_airport"),
                   col("actual_depart_datetime"), col("actual_arrive_datetime"))

#load data into BigQuery
data.write.format('bigquery') \
  .option('table', 'week3.flight-actual-date') \
  .mode('append') \
  .save()