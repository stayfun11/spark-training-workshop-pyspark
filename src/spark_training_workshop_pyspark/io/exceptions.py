"""
Exceptions used by the catalog module.
"""


class InvalidConfigException(Exception):
    """
    Raised when a configuration file cannot be loaded, for instance
    due to wrong syntax or poor formatting.
    """


class InvalidCatalogError(InvalidConfigException):
    """
    Raised when the catalog config is ill-formatted.
    """
