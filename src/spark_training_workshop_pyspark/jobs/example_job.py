"""
Module containing the example job entrypoint of the project
"""
import argparse

from spark_training_workshop_pyspark.config import ConfigLoader
from spark_training_workshop_pyspark.io.core import Dataset
from spark_training_workshop_pyspark.logging import build_logger
from spark_training_workshop_pyspark.session import build_spark_session
from spark_training_workshop_pyspark.transform.flights import compute_aggregated_flight

JOB_NAME = "example_job"


def main():
    """Main entry point of the project

    Parse the arguments and encapsulates the job's main logic.
    """
    # Parse arguments
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--spark-master",
        type=str,
        default=None,
        dest="spark_master",
        help="The `master` passed to the spark session builder",
    )
    parser.add_argument(
        "--confs-dir",
        type=str,
        default="confs",
        dest="confs_dir",
        help="Path to the root directory containing the conf files."
        "This directory should contain a subdirectory for each environment (e.g. local, dev, prod, etc.)",
    )
    parser.add_argument(
        "--env",
        type=str,
        default="local",
        help="Path to the directory containing the conf files." "Must be a subdirectory of the `confs-dir` directory",
    )
    parser.add_argument(
        "--log-level",
        type=str,
        default="INFO",
        dest="log_level",
        help=(
            "The desired log level."
            'Can be one of "ALL", "DEBUG", "ERROR", "FATAL", "INFO", "OFF", "TRACE", or "WARN".'
            'Defaults to "INFO"'
        ),
    )
    args = parser.parse_args()

    # Load configuration
    config_loader = ConfigLoader(confs_dir=args.confs_dir, env=args.env)
    params = config_loader.get("params.yml")
    spark_params = config_loader.get("spark.yml")
    catalog: dict = config_loader.get("catalog.yml")[JOB_NAME]  # pylint: disable=unsubscriptable-object

    # Build spark session
    spark = build_spark_session(
        app_name=JOB_NAME, spark_master=args.spark_master, spark_params=spark_params, log_level=args.log_level
    )

    # Build logger
    logger = build_logger(spark=spark, log_level=args.log_level)

    # Run the ETL job
    logger.info(f"Starting job {JOB_NAME} ...")

    # Load inputs and outputs catalog configuration
    inputs = catalog["inputs"]
    outputs = catalog["outputs"]

    # Read the inputs data
    flights = Dataset(spark=spark, config=inputs["flights"]).read()

    # Apply state-of-the-art computation
    aggregated_flights = compute_aggregated_flight(flights, exclude_countries=params.get("exclude_countries", []))

    # Write results in outputs dir
    Dataset(spark=spark, config=outputs["aggregated_flights"]).write(aggregated_flights)
    logger.info(f"{JOB_NAME} completed !")


if __name__ == "__main__":
    main()
