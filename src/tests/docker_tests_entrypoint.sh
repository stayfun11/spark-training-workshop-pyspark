#
# Source: https://github.com/dktunited/spark-training-workshop-pyspark/blob/main/src/tests/docker_tests_entrypoint.sh
#

# Entry point to run the tests from docker container

# PySpark should not be installed in the Docker image for the worker nodes.
# Here, it can be installed because it is for testing purpose on the master
# node only
SPARK_VERSION="3.3.0"

python3 -mpip install pyspark==${SPARK_VERSION}
python3 -mpip install pytest pyspark_test

export PYSPARK_PYTHON="python3"
export PYSPARK_DRIVER_PYTHON="python3"

pytest .
