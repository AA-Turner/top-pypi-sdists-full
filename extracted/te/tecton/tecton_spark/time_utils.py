import datetime
from typing import Union

import pytimeparse
from pyspark.sql import functions
from pyspark.sql.functions import expr

import tecton_core.tecton_pendulum as pendulum
from tecton_core.errors import TectonValidationError
from tecton_core.spark_type_annotations import PySparkColumn
from tecton_core.spark_type_annotations import is_pyspark_column
from tecton_core.time_utils import nanos_to_seconds
from tecton_core.time_utils import strict_pytimeparse
from tecton_proto.data.feature_store__client_pb2 import FeatureStoreFormatVersion


WINDOW_UNBOUNDED_PRECEDING = "unbounded_preceding"


def assert_valid_time_string(time_str: str, allow_unbounded: bool = False) -> None:
    if allow_unbounded:
        if time_str.lower() != WINDOW_UNBOUNDED_PRECEDING and pytimeparse.parse(time_str) is None:
            msg = f"Time string {time_str} must either be `tecton.WINDOW_UNBOUNDED_PRECEDING` or a valid time string."
            raise TectonValidationError(msg)
    else:
        strict_pytimeparse(time_str)


def subtract_seconds_from_timestamp(
    timestamp: Union[PySparkColumn, datetime.datetime], delta_seconds: int
) -> Union[PySparkColumn, datetime.datetime]:
    """
    Subtract seconds from timestamp
    Timestamp can be in Column[Timestamp] or just Timestamp
    :param timestamp: seconds
    :param delta_seconds: seconds
    :return:
    """
    td = datetime.timedelta(seconds=delta_seconds)
    if is_pyspark_column(timestamp):
        return timestamp - expr(f"INTERVAL {td.days} DAYS") - expr(f"INTERVAL {td.seconds} SECONDS")
    else:
        return timestamp - td


def add_seconds_to_timestamp(
    timestamp: Union[PySparkColumn, datetime.datetime], delta_seconds: int
) -> Union[PySparkColumn, datetime.datetime]:
    """
    Add seconds to timestamp
    Timestamp can be in Column[Timestamp] or just Timestamp
    :param timestamp:  seconds
    :param delta_seconds: seconds
    :return:
    """
    if is_pyspark_column(timestamp):
        td = datetime.timedelta(seconds=delta_seconds)
        return timestamp + expr(f"INTERVAL {td.days} DAYS") + expr(f"INTERVAL {td.seconds} SECONDS")
    else:
        td = datetime.timedelta(seconds=delta_seconds)
        return timestamp + td


def convert_timestamp_to_epoch(
    timestamp: Union[PySparkColumn, datetime.datetime], version: int
) -> Union[PySparkColumn, int]:
    """
    Convert timestamp to epoch
    Timestamp can be in Column[Timestamp] or just Timestamp
    V0 Return Epoch in seconds
    V1 Return Epoch in nanoseconds
    :param timestamp: Datetime / Datetime column
    :param version: Feature Store Format Version
    :return:
    """
    if version == FeatureStoreFormatVersion.FEATURE_STORE_FORMAT_VERSION_DEFAULT:
        return get_timestamp_in_seconds(timestamp)
    else:
        return get_timestamp_in_nanos(timestamp)


def convert_epoch_to_datetime(
    epoch: Union[PySparkColumn, int], version: int
) -> Union[PySparkColumn, pendulum.datetime]:
    """
    Convert epoch to datetime
    V0 epoch is in seconds
    V1 epoch is in nanoseconds -> convert to seconds
    :param epoch: Epoch based on version
    :param version: Feature Store Format Version
    :return:
    """
    if is_pyspark_column(epoch):
        return convert_epoch_to_timestamp_column(epoch, version)
    else:
        epoch_float = float(epoch)
        if version >= FeatureStoreFormatVersion.FEATURE_STORE_FORMAT_VERSION_TIME_NANOSECONDS:
            epoch_float = nanos_to_seconds(epoch)
        return pendulum.from_timestamp(epoch_float)


def get_timestamp_in_seconds(timestamp: Union[PySparkColumn, datetime.datetime]) -> Union[PySparkColumn, int]:
    """
    Converts a given timestamp to epoch total seconds
    Timestamp can be in Column[Timestamp] or just Timestamp
    If its a column we need to use a UDF.
    :param timestamp: Datetime / Datetime column
    :return: Timestamp / Timestamp column
    """
    if is_pyspark_column(timestamp):
        # For Spark >= 3.4 converting TIMESTAMP_NTZ to TIMESTAMP first (depends on session timezone)
        return timestamp.cast("timestamp").cast("int")
    else:
        return int(timestamp.timestamp())


def get_timestamp_in_nanos(timestamp: Union[PySparkColumn, datetime.datetime]) -> Union[PySparkColumn, int]:
    """
    Converts a given timestamp to epoch total nano seconds
    Timestamp could be a column of timestamp type or
    an actual timestamp. If its a column we need to use
    a UDF.
    :param timestamp: Datetime / Datetime column
    :return: Timestamp / Timestamp column
    """
    if is_pyspark_column(timestamp):
        # For Spark >= 3.4 converting TIMESTAMP_NTZ to TIMESTAMP first (depends on session timezone)
        timestamp = timestamp.cast("timestamp")
        return ((timestamp.cast("double") * 1e6).cast("long")) * 1000
    else:
        return (int(timestamp.timestamp() * 1e6)) * 1000


def convert_epoch_to_timestamp_column(epoch: PySparkColumn, version: int) -> PySparkColumn:
    """
    Converts an epoch column to a timestamp column
    :param epoch: Epoch Column [V0 : Seconds, V1 : Nanoseconds]
    :param version: Feature Store Format Version
    :return:
    """
    if version == FeatureStoreFormatVersion.FEATURE_STORE_FORMAT_VERSION_DEFAULT:
        return functions.to_timestamp(epoch)
    else:
        return functions.to_timestamp(epoch / functions.lit(1e9))
