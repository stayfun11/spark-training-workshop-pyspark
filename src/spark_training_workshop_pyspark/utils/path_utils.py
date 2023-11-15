"""
Module to handle path-related utilities
"""
from datetime import datetime
from typing import Tuple


def extract_date_parts_from_str(ds_str: str, ds_format: str = "%Y-%m-%d") -> Tuple[str, str, str]:
    """
    Extract year, month, and day parts from a date string in the specified format.

    Args:
        ds_str (str): A date string in the specified format.
        ds_format (str): The format of the date string (default: '%Y-%m-%d').

    Returns:
        Tuple[str, str, str]: A tuple containing the year, month, and day parts
        extracted from the date string. The year, month, and day parts are returned
        as strings with leading zeros if necessary to ensure fixed-length output.

    Examples:
        >>> extract_date_parts_from_str("2022-03-01")
        ('2022', '03', '01')

        >>> extract_date_parts_from_str("20220502", format="%Y%m%d")
        ('2022', '05', '02')
    """
    datestamp: datetime = datetime.strptime(ds_str, ds_format)
    year: str = str(datestamp.year)
    month: str = str(datestamp.month).zfill(2)
    day: str = str(datestamp.day).zfill(2)
    return year, month, day


def extract_ts_parts_from_str(ts_str: str, ts_format: str = "%Y-%m-%d-%H-%M-%S") -> Tuple[str, str, str, str, str, str]:
    """
    Extract year, month, day, hour, minute, and second parts from a timestamp string in the specified format.

    Args:
        ts_str (str): A timestamp string in the specified format.
        ts_format (str): The format of the timestamp string (default: '%Y-%m-%d-%H-%M-%S').

    Returns:
        Tuple[str, str, str, str, str, str]: A tuple containing the year, month, day, hour, minute, and second parts
        extracted from the timestamp string. The year, month, day, hour, minute, and second parts are returned
        as strings with leading zeros if necessary to ensure fixed-length output.

    Examples:
        >>> extract_ts_parts_from_str("2022-04-01-16-23-02")
        ('2022', '04', '01', '16', '23', '02')

        >>> extract_ts_parts_from_str("2022-05-02T23:59:05", format="%Y-%m-%dT%H:%M:%S")
        ('2022', '05', '02', '23', '59', '05')
    """
    timestamp = datetime.strptime(ts_str, ts_format)
    year = str(timestamp.year)
    month = str(timestamp.month).zfill(2)
    day = str(timestamp.day).zfill(2)
    hour = str(timestamp.hour).zfill(2)
    minute = str(timestamp.minute).zfill(2)
    second = str(timestamp.second).zfill(2)

    return year, month, day, hour, minute, second


def get_date_filepath(ds_str: str, ds_format: str = "%Y-%m-%d") -> str:
    """
    Convert a date string into a directory path that is compatible with partitioning.

    Example: '2022-08-28' -> 'year=2022/month=2022-08/day=2022-08-28'

    Args:
        ds_str (str): A date string in the specified format.
        ds_format (str): The format of the date string (default: '%Y-%m-%d').

    Returns:
        str: A directory path that is compatible with partitioning.

    Examples:
        >>> get_date_filepath("2022-08-28")
        'year=2022/month=2022-08/day=2022-08-28'
    """
    datestamps: datetime = datetime.strptime(ds_str, ds_format)
    year: str = str(datestamps.year)
    month: str = str(datestamps.month).zfill(2)
    day: str = str(datestamps.day).zfill(2)
    ds_as_filepath: str = f"year={year}/month={year}-{month}/day={year}-{month}-{day}"
    return ds_as_filepath


def get_date_time_filepath(ts_str: str, ts_format: str = "%Y-%m-%d-%H-%M-%S") -> str:
    """
    Convert a timestamp string into a directory path that is compatible with partitioning.

    Example:
        '2022-08-28-15-22-59' -> 'year=2022/month=2022-08/day=2022-08-28/hour=2022-08-28-15/ts_str=2022-08-28-15-22-59'

    Args:
        ts_str (str): A timestamp string in the specified format.
        ts_format (str): The format of the timestamp string (default: '%Y-%m-%d-%H-%M-%S').

    Returns:
        str: A directory path that is compatible with partitioning.

    Examples:
        >>> get_date_time_filepath("2022-08-28-15-22-59")
        'year=2022/month=2022-08/day=2022-08-28/hour=2022-08-28-15/ts_str=2022-08-28-15-22-59'
    """
    timestamp = datetime.strptime(ts_str, ts_format)
    year = str(timestamp.year)
    month = str(timestamp.month).zfill(2)
    day = str(timestamp.day).zfill(2)
    hour = str(timestamp.hour).zfill(2)
    minute = str(timestamp.minute).zfill(2)
    second = str(timestamp.second).zfill(2)
    ts_as_filepath: str = (
        f"year={year}"
        f"/month={year}-{month}"
        f"/day={year}-{month}-{day}"
        f"/hour={year}-{month}-{day}-{hour}"
        f"/ts_str={year}-{month}-{day}-{hour}-{minute}-{second}"
    )
    return ts_as_filepath


def get_versioned_filepath(base_path: str, ds_str: str = None, ts_str: str = None) -> str:
    """
    Add a partition-friendly versioned path to the base URI or directory path.

    Note that when using Delta as the data format, versioning is handled
    automatically, and it is not necessary to add a version to the URI/directory path.

    Example of partition-friendly path added to the base path:
    'year=2022/month=2022-08/day=2022-08-28'

    Either `ds_str` or `ts_str` must be set, but not both.

    Args:
        base_path (str): The base URI or directory path.
        ds_str (str, optional): A date string in the specified format (default: None).
        ts_str (str, optional): A timestamp string in the specified format (default: None).

    Returns:
        str: A partition-friendly URI or directory path.

    Raises:
        ValueError: If either `ds_str` or `ts_str` is not set.

    Examples:
        >>> get_versioned_filepath("products", "2022-08-28")
        'products/year=2022/month=2022-08/day=2022-08-28'

        >>> get_versioned_filepath("products", ts_str="2022-08-28-11-15-45")
        'products/year=2022/month=2022-08/day=2022-08-28/hour=2022-08-28-11/ts_str=2022-08-28-11-15-45'
    """
    if ds_str:
        ds_as_filepath: str = get_date_filepath(ds_str=ds_str)
        versioned_path = f"{base_path}/{ds_as_filepath}"

    elif ts_str:
        ts_as_filepath: str = get_date_time_filepath(ts_str=ts_str)
        versioned_path = f"{base_path}/{ts_as_filepath}"

    else:
        err_msg: str = (
            f"Error - Either date ({ds_str}), for input data, "
            f"or ts_str ({ts_str}), for output data, must be set "
            "(not null/None)"
        )
        raise ValueError(err_msg)

    return versioned_path
