"""
Module for testing the ConfigLoader class.
"""
import pytest

from spark_training_workshop_pyspark.config import ConfigLoader


def test_error_is_raised_when_file_path_does_not_exist():
    """
    Test that an error is raised when the file path does not exist.
    """
    config_loader = ConfigLoader(confs_dir="/path/which/does/not/exist", env="env-which-does-not-exist")
    with pytest.raises(FileNotFoundError):
        config_loader.get("parameters.yml")
