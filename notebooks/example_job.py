# Databricks notebook source
# DBTITLE 1,Install dependencies
# MAGIC %sh
# MAGIC cd ..
# MAGIC pip install poetry==1.5.1
# MAGIC poetry build
# MAGIC export VERSION=$(cat VERSION)
# MAGIC pip install dist/spark_training_workshop_pyspark-$VERSION-py3-none-any.whl

# COMMAND ----------

# DBTITLE 1,Add the project to PythonPath 
import sys
from pathlib import Path

SOURCES = '../src/'
if SOURCES not in sys.path:
    print('Adding sources to sys.path ...')
    sys.path.insert(0, SOURCES)
    print('DONE')

# COMMAND ----------

# DBTITLE 1,Load And Edit configuration example
import imp
from spark_training_workshop_pyspark.conf.config import ConfigLoader, MissingConfigException

# If you apply changes on a module, you need to reload it to take those changes in account
imp.reload(spark_training_workshop_pyspark.conf.config)

JOB_NAME = "example_job"

config_loader = ConfigLoader(confs_dir="../confs", env="dev")
params = config_loader.get("params.yml")
catalog: dict = config_loader.get("catalog.yml")[JOB_NAME]  # pylint: disable=unsubscriptable-object

# Load inputs and outputs catalog configuration
inputs = catalog["inputs"]
outputs = catalog["outputs"]

# you have to resolve a relative paths and add the prefix file:// in order to refer your data in the current workspace
inputs["flights"]['path']='file://' + str(Path('../data/inputs/flights/*').resolve())

# COMMAND ----------

# DBTITLE 1,Read your input data using the class Dataset
from spark_training_workshop_pyspark.io.core import Dataset
flights = Dataset(spark=spark, config=inputs["flights"]).read()

# COMMAND ----------

flights.display()
