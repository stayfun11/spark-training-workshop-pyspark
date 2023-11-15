"""
Module for testing the example job.
"""
import sys

from spark_training_workshop_pyspark.config import ConfigLoader
from spark_training_workshop_pyspark.io.core import Dataset
from spark_training_workshop_pyspark.jobs import example_job
from spark_training_workshop_pyspark.session import build_spark_session


def test_example_job():
    """
    Test that the example job generates the expected results.
    """
    # Mock up the CLI arguments
    confs_dir = "src/tests/confs/"
    env = "tests"
    sys.argv = ["test_example_job", "--confs-dir", confs_dir, "--env", env, "--spark-master", "local"]

    # Run the job
    example_job.main()

    # Check the results
    spark = build_spark_session(app_name="test-example-job")
    config_loader = ConfigLoader(confs_dir=confs_dir, env=env)
    catalog = config_loader.get("catalog.yml")

    aggregated_flights = Dataset(spark=spark, config=catalog["example_job"]["outputs"]["aggregated_flights"]).read()

    # Write your business logic test suite, eg:
    # No empty
    assert aggregated_flights.count() > 0

    # Has value for country 'Anguilla'
    assert aggregated_flights.filter(aggregated_flights.DEST_COUNTRY_NAME.isin(["Anguilla"])).count() > 0

    # ...
