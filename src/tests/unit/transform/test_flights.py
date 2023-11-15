"""
Unit tests for the flights transform module.
"""
from pyspark.sql import Row, SparkSession
from pyspark_test import assert_pyspark_df_equal

from spark_training_workshop_pyspark.io.schemas.aggregated_flights import SCHEMA as AGGREGATED_FLIGHT_SCHEMA
from spark_training_workshop_pyspark.io.schemas.flights import SCHEMA as FLIGHT_SCHEMA
from spark_training_workshop_pyspark.transform.flights import compute_aggregated_flight


def test_compute_aggregated_flight(spark: SparkSession):
    """
    Test that the compute_aggregated_flight function returns the expected result.
    """
    # Create a test dataframe
    rows = [
        Row(DEST_COUNTRY_NAME="United States", ORIGIN_COUNTRY_NAME="Romania", count=10),
        Row(DEST_COUNTRY_NAME="United States", ORIGIN_COUNTRY_NAME="Ireland", count=5),
        Row(DEST_COUNTRY_NAME="United States", ORIGIN_COUNTRY_NAME="India", count=20),
        Row(DEST_COUNTRY_NAME="Egypt", ORIGIN_COUNTRY_NAME="United States", count=15),
    ]

    flights = spark.createDataFrame(rows, schema=FLIGHT_SCHEMA)
    result = compute_aggregated_flight(flights, exclude_countries=[])

    # Create manually the expected result dataframe
    expected_rows = [
        Row(DEST_COUNTRY_NAME="United States", TOTAL_COUNT=35),
        Row(DEST_COUNTRY_NAME="Egypt", TOTAL_COUNT=15),
    ]
    expected_result = spark.createDataFrame(expected_rows, schema=AGGREGATED_FLIGHT_SCHEMA)

    assert_pyspark_df_equal(result, expected_result)
