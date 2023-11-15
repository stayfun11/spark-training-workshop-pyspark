"""
This module contains functions for building a logging.Logger object using PySpark's SparkSession.
"""
import logging
import typing as T

import pyspark.sql
from py4j.java_gateway import JavaPackage


@T.no_type_check  # spark._jvm.org.apache.log4j is not typed
def build_logger(
    spark: pyspark.sql.SparkSession,
    log_level: str = "INFO",
) -> logging.Logger:
    """
    Build a logging.Logger object using the org.apache.log4j package from PySpark's SparkSession.

    Args:
        spark (pyspark.sql.SparkSession): The SparkSession object to use for logging.
        log_level (str, optional): The desired log level.
            Can be one of "ALL", "DEBUG", "ERROR", "FATAL", "INFO", "OFF", "TRACE", or "WARN".
            Defaults to "INFO".

    Returns:
        logging.Logger: The Logger object created.
    """
    # Retrieve the Java-based logger object
    log_4j_package: JavaPackage = spark._jvm.org.apache.log4j  # pylint: disable=protected-access
    app_name = spark.sparkContext.getConf().get("spark.app.name")
    logger = log_4j_package.LogManager.getLogger(app_name)

    # Convert the log level string into the corresponding integer/enumeration
    log_level = getattr(log_4j_package.Level, log_level.upper())
    logger.setLevel(log_level)

    return logger
