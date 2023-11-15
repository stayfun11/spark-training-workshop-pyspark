"""
Module to store aggregated flights schema.
"""
from pyspark.sql.types import LongType, StringType, StructField, StructType

SCHEMA = StructType(
    [StructField("DEST_COUNTRY_NAME", StringType(), True), StructField("TOTAL_COUNT", LongType(), True)]
)
