"""
Module to store flights schema.
"""
from pyspark.sql.types import LongType, StringType, StructField, StructType

SCHEMA = StructType(
    [
        StructField("DEST_COUNTRY_NAME", StringType(), True),
        StructField("ORIGIN_COUNTRY_NAME", StringType(), True),
        StructField("count", LongType(), True),
    ]
)
