"""
This module contains the core classes to read and write data from/to different sources.
"""
from importlib import import_module
from typing import Any, Dict

import pyspark.sql

from spark_training_workshop_pyspark.io.exceptions import InvalidCatalogError


class Dataset:
    """
    Class to handle input/output data for Spark processing.
    Args:
        spark: A SparkSession instance.
        config: A dictionary with dataset configuration options. The options are:
            * `path`: The URI or directory path for the input/output data.
            * `table`: The name of the table to read from the metastore.
            * `read_args`: A dictionary with arguments to pass to the Spark DataFrameReader.load() method.
            * `write_args`: A dictionary with arguments to pass to the Spark DataFrameWriter.save() method.
            * `schema`: A string with the fully qualified name of the schema class to use when reading or writing
              data.
    """

    def __init__(self, spark: pyspark.sql.SparkSession, config: Dict[str, Any]) -> None:
        """
        Initialize a new Dataset instance.
        """
        self.spark = spark
        self.config = {**config}  # Make a deep copy
        self.schema = None
        self.use_metastore = bool(self.config.get("table", None))

        self._validate_config()
        self._read_schema()

    def read(self):
        """
        Read data from the input source.
        Returns:
            A Spark DataFrame instance.
        """
        read_args = {**self.config.get("read_args", {})}
        if self.schema:
            read_args.update({"schema": self.schema})

        if self.use_metastore:
            # No options nor format to pass when using glue to read data
            return self.spark.read.table(self.config["table"])

        return self.spark.read.load(
            self.config["path"],
            **read_args,
        )

    def write(self, dataframe: pyspark.sql.DataFrame):
        """
        Write data to the output source.
        Args:
            dataframe: A Spark DataFrame instance to write.
        """
        write_args = {**self.config.get("write_args", {})}
        if self.schema:
            write_args.update({"schema": self.schema})

        if self.use_metastore:
            dataframe.write.saveAsTable(self.config["table"], **write_args)
        else:
            dataframe.write.save(self.config["path"], **write_args)

    def _validate_config(self):
        """
        Validate the configuration options.
        """
        if self.config.get("table", None) is None and self.config.get("path", None) is None:
            raise InvalidCatalogError("You need to define either one valid ``table`` or ``path`` parameter.")

        if self.config.get("table", None) is not None and self.config.get("path", None) is not None:
            raise InvalidCatalogError(
                "You cannot define a ``path`` and a ``table`` param simultaneously. "
                "Choose ``path`` for raw files input, ``table`` to use the metastore."
            )

    def _read_schema(self):
        """
        Read the schema from the configuration options.
        """
        schema = self.config.get("schema", None)
        if schema:
            module_name, schema_name = schema.rsplit(".", 1)
            module = import_module(module_name)
            self.schema = getattr(module, schema_name)
