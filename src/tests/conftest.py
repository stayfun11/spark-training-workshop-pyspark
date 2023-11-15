"""
Module to store project-scoped fixtures.
"""
import pytest
from pyspark.sql import SparkSession


@pytest.fixture(scope="session")
def spark() -> SparkSession:
    """
    Returns a test SparkSession object.
    """
    spark_session = SparkSession.builder.master("local").appName("TESTS_SUITE").getOrCreate()
    return spark_session
