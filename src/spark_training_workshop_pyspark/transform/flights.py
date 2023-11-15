"""
Module for computing aggregated flight data.
"""
from typing import List

from pyspark.sql.dataframe import DataFrame


def compute_aggregated_flight(flights: DataFrame, exclude_countries: List[str]) -> DataFrame:
    """
    Compute the sum of flights aggregated by ``DEST_COUNTRY_NAME``.

    Args:
        flights: The transactions dataframe
        exclude_countries: The list of countries to exclude from the computation

    Returns:
        Dataframe of flights counts aggregated by destination.
    """
    filtered_flights = flights.filter(~flights.DEST_COUNTRY_NAME.isin(exclude_countries))
    flights_count_by_destination = (
        filtered_flights.groupby("DEST_COUNTRY_NAME").sum("count").withColumnRenamed("sum(count)", "TOTAL_COUNT")
    )
    return flights_count_by_destination
