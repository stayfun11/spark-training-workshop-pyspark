"""
Module that handles the creation of SparkSession objects
"""
from typing import Any, Dict

import pyspark.sql
from pyspark import SparkConf


def build_spark_session(
    app_name: str,
    spark_master: str = None,
    spark_params: Dict[str, Any] = None,
    log_level: str = "INFO",
) -> pyspark.sql.SparkSession:
    """
    Returns a SparkSession object with the given application name and Spark configuration parameters.

    Args:
        app_name (str): The name of the Spark application.
        spark_master (str, optional): The Spark master URL to connect to. If not specified,
            the default master will be used.
        spark_params (Dict[str, Any], optional): A dictionary containing additional
            Spark configuration parameters to set
        log_level (str, optional): The desired log level.
            Can be one of "ALL", "DEBUG", "ERROR", "FATAL", "INFO", "OFF", "TRACE", or "WARN".

    Returns:
        SparkSession: A SparkSession object with the specified configuration.

    Raises:
        None

    Examples:
        >>> spark = build_spark_session('my_app')
        >>> df = spark.read.csv('data.csv')
    """
    spark_conf = SparkConf()

    if spark_params:
        spark_param_list = [item for item in spark_params.items()]  # pylint: disable=unnecessary-comprehension
        spark_conf = spark_conf.setAll(spark_param_list)

    builder = pyspark.sql.SparkSession.builder.appName(app_name).config(conf=spark_conf).enableHiveSupport()
    if spark_master:
        builder = builder.master(spark_master)

    spark_session = builder.getOrCreate()
    spark_session.sparkContext.setLogLevel(log_level)

    return spark_session
