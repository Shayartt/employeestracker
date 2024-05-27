# First Level import :
import os 
import sys
import json

# Second level import
from DataAnalyzer import MyAnalyzer

# Third Level import :
from pyspark import SparkContext
from pyspark.rdd import RDD
from pyspark.sql import SparkSession, DataFrame as SparkDataFrame


if __name__ == "__main__":

    # Create Spark Application : 
    spark = SparkSession\
        .builder\
        .appName("Spark-Analyzer-Job")\
        .getOrCreate()
        
    # Set the logging level to INFO (or any other desired level)
    spark.sparkContext.setLogLevel("INFO")
    
    # Init Analyzer object : 
    analyzer = MyAnalyzer(spark)
    
    
    # Finish Spark Session : 
    spark.stop()