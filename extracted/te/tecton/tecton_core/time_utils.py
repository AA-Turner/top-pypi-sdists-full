import datetime
import re
from typing import TYPE_CHECKING
from typing import Optional
from typing import TypeVar
from typing import Union

import pandas
import pytimeparse
from google.protobuf import duration_pb2
from google.protobuf import timestamp_pb2
from pypika.terms import Term
from typeguard import typechecked

import tecton_core.tecton_pendulum as pendulum
from tecton_core.errors import TectonValidationError
from tecton_proto.data import feature_store__client_pb2 as feature_store_pb2


if TYPE_CHECKING:
    from tecton_core.feature_definition_wrapper import FeatureDefinitionWrapper


# 10,000 years which is less than but still close to the max duration proto amount, and a digestable number of years to
# a user
_MAX_PROTO_DURATION_SECONDS = 10_000 * 365 * 24 * 60 * 60

_TIME_RANGE_REGEX = r"^(?:(\d+)d)?(?:(\d+)h)?(?:(\d+)m)?(?:(\d+)s)?$"

TERM_OR_INT = TypeVar("TERM_OR_INT", int, Term)


def timedelta_to_duration(td: datetime.timedelta) -> pendulum.Duration:
    return pendulum.duration(days=td.days, seconds=td.seconds, microseconds=td.microseconds)


def proto_to_duration(proto_duration: duration_pb2.Duration) -> pendulum.Duration:
    return timedelta_to_duration(proto_duration.ToTimedelta())


def timedelta_to_proto(td: Optional[datetime.timedelta]) -> Optional[duration_pb2.Duration]:
    if td is None:
        return None

    if td.total_seconds() > _MAX_PROTO_DURATION_SECONDS:
        msg = "'Timedelta value must be lower than max value of 10000 years'"
        raise TectonValidationError(msg)

    # negative timedeltas represented in pendulum.Duration are converted incorrectly when converted directly to proto
    # so if td is type pendulum.Duration, convert to timedelta first
    if isinstance(td, pendulum.Duration):
        td = td.as_timedelta()

    proto = duration_pb2.Duration()
    proto.FromTimedelta(td)
    return proto


def to_positive_proto(proto_duration: duration_pb2.Duration) -> duration_pb2.Duration:
    return duration_pb2.Duration(seconds=abs(duration_pb2.Duration.seconds), nanos=abs(duration_pb2.Duration.nanos))


def datetime_to_proto(dt: Optional[datetime.datetime]) -> Optional[timestamp_pb2.Timestamp]:
    if dt is None:
        return None
    proto = timestamp_pb2.Timestamp()
    proto.FromDatetime(dt)
    return proto


@typechecked
def to_human_readable_str(duration: Union[duration_pb2.Duration, datetime.timedelta]) -> str:
    """
    Replicate the backend logic that converts durations to feature strings, e.g. `column_sum_1h30m_30m`.

    Backend logic: https://github.com/tecton-ai/tecton/blob/e3c04e28066c21fa4ed9b459ece458c084766b6e/java/com/tecton/common/utils/TimeUtils.kt#L80
    """

    if isinstance(duration, duration_pb2.Duration):
        duration = proto_to_duration(duration)
    elif isinstance(duration, datetime.timedelta):
        duration = timedelta_to_duration(duration)
    else:
        msg = f"Invalid input duration type: {type(duration)}"
        raise TypeError(msg)

    duration_str_list = []
    if duration.days > 0:
        duration_str_list.append(f"{duration.days}d")
    if duration.hours > 0:
        duration_str_list.append(f"{duration.hours}h")
    if duration.minutes > 0:
        duration_str_list.append(f"{duration.minutes}m")
    if duration.remaining_seconds > 0:
        duration_str_list.append(f"{duration.remaining_seconds}s")

    return "0s" if len(duration_str_list) == 0 else "".join(duration_str_list)


@typechecked
def parse_to_timedelta(time_string: str) -> datetime.timedelta:
    """Parse a string with format '{days}d{hours}h{minutes}m{seconds}s' into a timedelta object.

    Each time component is optional, but at least one value must be provided, e.g. "" is invalid but "0s" is valid.
    """
    if time_string == "":
        msg = "Cannot use an empty string for a time range. Use '0d', '0s', etc. instead."
        raise ValueError(msg)

    match = re.match(_TIME_RANGE_REGEX, time_string)
    if not match:
        msg = f"The time range string '{time_string}' is not in the correct format. Should be of the form '[days]d[hours]h[minutes]m[seconds]s', e.g. `1d12h`."
        raise ValueError(msg)

    # Extract time components from the matched groups, substituting 0 where no component is found
    days, hours, minutes, seconds = [int(g) if g else 0 for g in match.groups()]

    # Create a timedelta object with the extracted time components
    return datetime.timedelta(days=days, hours=hours, minutes=minutes, seconds=seconds)


def assert_is_round_seconds(d: pendulum.Duration) -> pendulum.Duration:
    if d % pendulum.Duration(seconds=1):
        msg = f"{d.in_words()} is not a round number of seconds"
        raise ValueError(msg)
    return d


def strict_pytimeparse(time_str: str) -> Union[int, float]:
    parsed = pytimeparse.parse(time_str)
    if parsed is None:
        msg = f'Could not parse time string "{time_str}"'
        raise TectonValidationError(msg)
    else:
        return parsed


def nanos_to_seconds(nanos: int) -> float:
    """
    :param nanos: Nanoseconds
    :return: Converts nanoseconds to seconds
    """
    return nanos / float(1e9)


def seconds_to_nanos(seconds: float) -> int:
    """
    :param seconds: Seconds
    :return: Converts seconds to nanoseconds
    """
    return int(seconds * 1e9)


def convert_duration_to_seconds(duration: int, version: int) -> int:
    """Convert a duration to seconds according to the version.

    If V0, the duration is already in seconds; if V1, the duration must be converted from nanos to seconds.
    """
    if version == feature_store_pb2.FEATURE_STORE_FORMAT_VERSION_DEFAULT:
        return duration
    else:
        return int(nanos_to_seconds(duration))


def convert_timedelta_for_version(duration: datetime.timedelta, version: int) -> int:
    """
    Convert pendulum duration according to version
    VO -> Return Seconds
    V1 -> Return Nanoseconds
    :param duration: Pendulum Duration
    :param version: Feature Store Format Version
    :return:
    """
    assert duration.microseconds == 0
    interval = duration.total_seconds()
    if version == feature_store_pb2.FEATURE_STORE_FORMAT_VERSION_DEFAULT:
        return int(interval)
    else:
        return seconds_to_nanos(interval)


def convert_epoch_to_datetime(epoch: int, version: int) -> pendulum.datetime:
    """
    Converts an epoch to a datetime.
    """
    if version == feature_store_pb2.FeatureStoreFormatVersion.FEATURE_STORE_FORMAT_VERSION_DEFAULT:
        return pendulum.from_timestamp(epoch)
    else:
        return pendulum.from_timestamp(epoch / 1e9)


def convert_timestamp_for_version(timestamp: datetime.datetime, version: int) -> int:
    if version == feature_store_pb2.FeatureStoreFormatVersion.FEATURE_STORE_FORMAT_VERSION_DEFAULT:
        return int(timestamp.timestamp())
    else:
        return seconds_to_nanos(timestamp.timestamp())


def convert_proto_duration_for_version(duration: duration_pb2.Duration, version: int) -> int:
    return convert_timedelta_for_version(duration.ToTimedelta(), version)


def align_time_downwards(time: datetime.datetime, alignment: datetime.timedelta) -> datetime.datetime:
    excess_seconds = time.timestamp() % alignment.total_seconds()
    aligned_timestamp = time.timestamp() - excess_seconds
    return datetime.datetime.fromtimestamp(aligned_timestamp, tz=datetime.timezone.utc)


def align_epoch_downwards(int_timestamp_col: int, window_size: int) -> int:
    return int_timestamp_col - (int_timestamp_col % window_size)


def align_time_upwards(time: datetime.datetime, alignment: datetime.timedelta) -> datetime.datetime:
    excess_seconds = time.timestamp() % alignment.total_seconds()
    offset = 0 if excess_seconds == 0 else alignment.total_seconds() - excess_seconds
    aligned_timestamp = time.timestamp() + offset
    return datetime.datetime.fromtimestamp(aligned_timestamp, tz=datetime.timezone.utc)


def get_timezone_aware_datetime(time: Optional[datetime.datetime]) -> Optional[datetime.datetime]:
    """
    Check and get timezone aware datetime
    :param time: Time to convert to timezone aware
    """
    if time is None:
        return None
    if time.tzinfo is None:
        return time.replace(tzinfo=pendulum.timezone("UTC"))
    else:
        return time


def convert_pandas_df_for_snowflake_upload(pandas_df: pandas.DataFrame) -> None:
    """
    Converts a pandas dataframe's timestamp columns to ensure expected behavior when uploading to Snowflake.

    Snowflake's `write_pandas` logic only writes TIMESTAMP_NTZ timestamps correctly if we
    pretend the input timestamps are UTC. Providing another time zone (e.g. 11PM PST) will convert
    this to UTC time (6AM UTC), and then drop the timezone info + load as a TIMESTAMP_NTZ column (6AM).
    """
    # TODO(TEC-16678): Revert this once a fix is upstreamed to Snowflake
    for col in pandas_df.columns:
        if pandas.core.dtypes.common.is_datetime64_dtype(pandas_df[col]):
            pandas_df[col] = pandas_df[col].dt.tz_localize(None)
            pandas_df[col] = pandas_df[col].dt.tz_localize(pendulum.timezone("UTC"))


def convert_to_effective_timestamp(
    timestamp_col: TERM_OR_INT, batch_schedule_seconds: int, data_delay_seconds: int
) -> TERM_OR_INT:
    """
    Converts a timestamp col term or integer and converts it into an effective timestamp by aligning on the interval
    and adding the interval and data delay.

    The effective timestamp represents the time when the feature is available in the online store to be used.
    """
    return timestamp_col - (timestamp_col % batch_schedule_seconds) + batch_schedule_seconds + data_delay_seconds


def get_nearest_anchor_time(
    timestamp: pendulum.DateTime,
    max_source_data_delay: pendulum.Duration,
    batch_materialization_schedule: pendulum.Duration,
    min_scheduling_interval: pendulum.Duration,
) -> pendulum.DateTime:
    """
    Returns the nearest anchor time (start of tile), such that the feature values as of this time would have the
    effective timestamp `timestamp`
    """
    timestamp = timestamp - max_source_data_delay - batch_materialization_schedule

    if min_scheduling_interval.total_seconds() > 0:
        timestamp = align_time_downwards(timestamp, min_scheduling_interval)

    return pendulum.instance(timestamp)


def align_left(timestamp: pendulum.DateTime, min_scheduling_interval: pendulum.Duration) -> pendulum.DateTime:
    # min scheduling interval may be zero for continuous
    if min_scheduling_interval and min_scheduling_interval.total_seconds() > 0:
        timestamp = align_time_downwards(timestamp, min_scheduling_interval)
    return pendulum.instance(timestamp)


def align_right(timestamp: pendulum.DateTime, min_scheduling_interval: pendulum.Duration) -> pendulum.DateTime:
    """Aligns timestamp to the end of the scheduling interval. If it's already aligned,
    adds scheduling interval's length.

    This function does not take allowed lateness into account.

    :param timestamp: The timestamp in python datetime format
    :return: The timestamp of the greatest aligned time <= timestamp, in seconds.
    """
    aligned_left = align_left(timestamp, min_scheduling_interval)

    # input timestamp is already aligned
    if aligned_left == timestamp:
        return timestamp

    return aligned_left + min_scheduling_interval


def temporal_fv_get_feature_data_time_limits(
    fd: "FeatureDefinitionWrapper",
    spine_time_limits: pendulum.Period,
    max_lookback: Optional[datetime.timedelta],
) -> pendulum.Period:
    """Feature data time limits for a non aggregate feature view.

    Accounts for:
      * serving ttl
      * batch schedule
      * data delay

    Does NOT account for:
      * batch vs streaming

    NOTE: for historical reasons, this is not an exact filter but a more permissive one.
    """

    start_time = spine_time_limits.start
    end_time = spine_time_limits.end

    if max_lookback:
        start_time = start_time - max_lookback
    elif fd.serving_ttl:
        # Subtract by `serving_ttl` to accommodate for enough feature data for the feature expiration
        # We need to account for the data delay + ttl when determining the feature data time limits from the spine.
        start_time = start_time - fd.serving_ttl - fd.max_source_data_delay
    else:
        start_time = pendulum.from_timestamp(0)

    # Respect feature_start_time if it's set.
    if fd.feature_start_timestamp:
        start_time = max(start_time, fd.feature_start_timestamp)

    start_time = align_left(start_time, fd.min_scheduling_interval)

    # Since feature data time interval is open on the right, we need to always strictly align right so that
    # with `batch_schedule = 1h`, time end `04:00:00` will be aligned to `05:00:00`.
    # NOTE: This may be more permissive than 'max_source_data_delay' would allow,
    # but that's okay from a correctness perspective since our as-of join
    # should account for this.
    end_time = align_right(end_time, fd.min_scheduling_interval)

    # It is possible for the start time to be greater than the end time, for example if the feature start time is later
    # than the spine end time. If this happens, we simply set the start time to equal the end time.
    if start_time > end_time:
        start_time = end_time
    return pendulum.Period(start_time, end_time)


def get_feature_data_time_limits(
    fd: "FeatureDefinitionWrapper",
    spine_time_limits: pendulum.Period,
) -> pendulum.Period:
    """Returns the feature data time limits based on the spine time limits, taking aggregations into account.

    To get the raw data time limits, you need to use additional information that is on your FilteredSource or other data source inputs.

    Args:
        fd: The feature view for which to compute feature data time limits.
        spine_time_limits: The time limits of the spine; the start time is inclusive and the end time is exclusive.
    """
    if fd.is_feature_table:
        return _feature_table_get_feature_data_time_limits(fd, spine_time_limits)
    elif fd.is_temporal:
        return temporal_fv_get_feature_data_time_limits(fd, spine_time_limits, None)
    elif fd.is_temporal_aggregate:
        return _temporal_agg_fv_get_feature_data_time_limits(fd, spine_time_limits)

    # Should never happen!
    msg = "Feature definition must be a feature table, temporal FV, or temporal agg FV"
    raise Exception(msg)


def _feature_table_get_feature_data_time_limits(
    fd: "FeatureDefinitionWrapper",
    spine_time_limits: pendulum.Period,
) -> pendulum.Period:
    """Feature data time limits for a feature table.

    This is `[spine_start_time - ttl, spine_end_time)`
    """
    start_time = spine_time_limits.start
    end_time = spine_time_limits.end

    # Subtract by `serving_ttl` to accommodate for enough feature data for the feature expiration
    if fd.serving_ttl:
        start_time = start_time - fd.serving_ttl
    else:
        start_time = pendulum.from_timestamp(0)

    return end_time - start_time


# TODO(TEC-17311): replace pendulum with stanard datetime + support 'unbounded'/None times
def _temporal_agg_fv_get_feature_data_time_limits(
    fd: "FeatureDefinitionWrapper",
    spine_time_limits: pendulum.Period,
) -> pendulum.Period:
    """Feature data time limits for an aggregate feature view.

    Accounts for:
      * aggregation tile interval
      * data delay
      * batch sawtooth tile size

    Does NOT account for:
      * batch vs streaming

    NOTE: for historical reasons, this is not an exact filter but a more permissive one.
    """
    start_time = spine_time_limits.start
    end_time = spine_time_limits.end

    # Respect feature_start_time if it's set.
    if fd.feature_start_timestamp:
        start_time = max(start_time, fd.feature_start_timestamp)

    start_time = align_left(start_time - fd.max_source_data_delay, fd.min_scheduling_interval)
    if fd.get_max_batch_sawtooth_tile_size():
        start_time = align_left(start_time, fd.get_max_batch_sawtooth_tile_size())

    # Account for final aggregation needing aggregation window prior to earliest timestamp
    if fd.has_lifetime_aggregate:
        start_time = pendulum.from_timestamp(0)
    else:
        earliest_window_start = fd.earliest_window_start
        start_time = start_time + timedelta_to_duration(earliest_window_start)

    if fd.materialization_start_timestamp:
        start_time = max(start_time, fd.materialization_start_timestamp)

    # Since feature data time interval is open on the right, we need to always strictly align right so that
    # with `batch_schedule = 1h`, time end `04:00:00` will be aligned to `05:00:00`.
    # NOTE: This may be more permissive than 'max_source_data_delay' would allow,
    # but that's okay from a correctness perspective since our as-of join
    # should account for this.
    end_time = align_right(end_time, fd.min_scheduling_interval)
    if fd.get_max_batch_sawtooth_tile_size():
        end_time = align_right(end_time, fd.get_max_batch_sawtooth_tile_size())

    # It is possible for the start time to be greater than the end time, for example if the feature start time is later
    # than the spine end time. If this happens, we simply set the start time to equal the end time.
    if start_time > end_time:
        start_time = end_time
    return pendulum.Period(start_time, end_time)


def get_feature_data_time_limits_for_lookback(
    fd: "FeatureDefinitionWrapper",
    spine_time_limits: pendulum.Period,
    max_lookback_duration: pendulum.Duration,
) -> pendulum.Period:
    """Aligns the spine time limits on the left to the lookback duration, and on the right to the nearest batch schedule/aggregation interval.

    Accounts for:
      * feature start time
      * data delay
      * materialization start time
      * look back duration parameter
      * batch schedule
      * batch sawtooth tile size

    Does NOT account for:
      * ttl
      * aggregation tile interval
      * aggregation window size
    """
    start_time = spine_time_limits.start
    end_time = spine_time_limits.end

    # Respect feature_start_time if it's set.
    if fd.feature_start_timestamp:
        start_time = max(start_time, fd.feature_start_timestamp)

    start_time = align_left(start_time - fd.max_source_data_delay - max_lookback_duration, fd.min_scheduling_interval)
    if fd.get_max_batch_sawtooth_tile_size():
        start_time = align_left(start_time, fd.get_max_batch_sawtooth_tile_size())

    if fd.materialization_start_timestamp:
        start_time = max(start_time, fd.materialization_start_timestamp)

    end_time = align_right(end_time, fd.min_scheduling_interval)
    if fd.get_max_batch_sawtooth_tile_size():
        end_time = align_right(end_time, fd.get_max_batch_sawtooth_tile_size())
    # It is possible for the start time to be greater than the end time, for example if the feature start time is later
    # than the spine end time. If this happens, we simply set the start time to equal the end time.
    if start_time > end_time:
        start_time = end_time
    return pendulum.Period(start_time, end_time)
