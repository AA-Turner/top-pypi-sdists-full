from __future__ import annotations

from datetime import datetime
from datetime import timedelta
from datetime import timezone
from enum import Enum
from typing import Optional

import attrs

from tecton_core.time_utils import datetime_to_proto
from tecton_core.time_utils import timedelta_to_proto
from tecton_proto.args import pipeline__client_pb2 as pipeline_pb2


# Lowest Pandas Timestamp
UNBOUNDED_PAST_TIMESTAMP = datetime(1677, 9, 22).replace(tzinfo=timezone.utc)

# Highest Pandas Timestamp
UNBOUNDED_FUTURE_TIMESTAMP = datetime(2262, 4, 11).replace(tzinfo=timezone.utc)


@attrs.define(frozen=True)
class FilterDateTime:
    """
    Represents a time reference for a FilteredSource. This can be a specific timestamp, or a time offset from a
    TectonTimeConstant.
    """

    time_reference: Optional[TectonTimeConstant] = None
    offset: Optional[timedelta] = timedelta(0)
    timestamp: Optional[datetime] = None

    def to_args_proto(self) -> pipeline_pb2.FilterDateTime:
        filter_date_time = pipeline_pb2.FilterDateTime()
        if self.time_reference:
            relative_time = pipeline_pb2.RelativeTime(
                time_reference=self.time_reference.to_args_proto(), offset=timedelta_to_proto(self.offset)
            )
            filter_date_time.relative_time.CopyFrom(relative_time)
        elif self.timestamp:
            filter_date_time.timestamp.CopyFrom(datetime_to_proto(self.timestamp))

        return filter_date_time

    @classmethod
    def from_proto(cls, proto: pipeline_pb2.FilterDateTime) -> FilterDateTime:
        if proto.HasField("relative_time"):
            time_reference = TectonTimeConstant.from_proto(proto.relative_time.time_reference)
            offset = proto.relative_time.offset.ToTimedelta()
            return FilterDateTime(time_reference=time_reference, offset=offset)
        elif proto.HasField("timestamp"):
            return FilterDateTime(timestamp=proto.timestamp.ToDatetime())
        else:
            msg = "FilterDateTime proto must have either relative_time or timestamp"
            raise ValueError(msg)

    def is_materialization_limit(self) -> bool:
        return self.time_reference is not None and self.time_reference.is_materialization_limit()

    def is_unbounded_limit(self) -> bool:
        return self.time_reference is not None and self.time_reference.is_unbounded_limit()

    def to_datetime(
        self, exact_reference_start: Optional[datetime] = None, exact_reference_end: Optional[datetime] = None
    ) -> Optional[datetime]:
        """
        Convert the FilterDateTime to a datetime object. Exact reference should be the
        materialization start or end time of the Feature View (if applicable).

        :param exact_reference_start: The Materialization start time of the Feature View which
        will be used when MATERIALIZATION_START_TIME is used as the time_reference.
        :param exact_reference_end: The Materialization end time of the Feature View which
        will be used when MATERIALIZATION_END_TIME is used as the time_reference.
        :return: A datetime object representing the FilterDateTime.
        """
        if self.time_reference:
            if self.time_reference == TectonTimeConstant.MATERIALIZATION_START_TIME:
                if exact_reference_start is None:
                    return None
                dt = exact_reference_start + self.offset
            elif self.time_reference == TectonTimeConstant.MATERIALIZATION_END_TIME:
                if exact_reference_end is None:
                    return None
                dt = exact_reference_end + self.offset
            elif self.time_reference == TectonTimeConstant.UNBOUNDED_PAST:
                # Close to `datetime.min` but can still be represented as a timestamp
                dt = UNBOUNDED_PAST_TIMESTAMP
            elif self.time_reference == TectonTimeConstant.UNBOUNDED_FUTURE:
                dt = UNBOUNDED_FUTURE_TIMESTAMP
            else:
                err = f"Unsupported TectonTimeConstant: {self.time_reference}"
                raise ValueError(err)
        elif self.timestamp:
            dt = self.timestamp
        else:
            err = "FilterDateTime must have a time_reference or timestamp"
            raise ValueError(err)

        return dt.replace(tzinfo=timezone.utc)


class TectonTimeConstant(Enum):
    """
    TectonTimeConstant is an enumeration of time constants used in Tecton that could be useful in defining time-based
    filters in Feature Views. These constants can be used in conjunction with timedelta to define time ranges for
    filters using DataSource.select_range().

    Example:
    ```
    @batch_feature_view(
        ...
        sources=[
            transactions_source.select_range(
                start_time=TectonTimeConstant.MATERIALIZATION_START_TIME - timedelta(days=7),
                end_time=TectonTimeConstant.MATERIALIZATION_END_TIME
            )
        ]
        ...
    )
    def my_feature_view(transactions_source):
        ...
    ```
    """

    MATERIALIZATION_START_TIME = 1
    MATERIALIZATION_END_TIME = 2
    UNBOUNDED_PAST = 3
    UNBOUNDED_FUTURE = 4

    def __add__(self, other: timedelta) -> FilterDateTime:
        if not isinstance(other, timedelta):
            err = "Can only add `timedelta` objects to a TectonTimeConstant"
            raise TypeError(err)
        if self == TectonTimeConstant.UNBOUNDED_PAST or self == TectonTimeConstant.UNBOUNDED_FUTURE:
            err = f"Cannot add a timedelta to {self}"
            raise ValueError(err)
        return FilterDateTime(time_reference=self, offset=other)

    def __sub__(self, other: timedelta) -> FilterDateTime:
        if not isinstance(other, timedelta):
            err = "Can only subtract `timedelta` objects from a TectonTimeConstant"
            raise TypeError(err)
        if self == TectonTimeConstant.UNBOUNDED_PAST or self == TectonTimeConstant.UNBOUNDED_FUTURE:
            err = f"Cannot add a timedelta offset to {self}"
            raise ValueError(err)
        return FilterDateTime(time_reference=self, offset=-other)

    def is_materialization_limit(self) -> bool:
        return self in [
            TectonTimeConstant.MATERIALIZATION_START_TIME,
            TectonTimeConstant.MATERIALIZATION_END_TIME,
        ]

    def is_unbounded_limit(self) -> bool:
        return self in [
            TectonTimeConstant.UNBOUNDED_PAST,
            TectonTimeConstant.UNBOUNDED_FUTURE,
        ]

    def to_args_proto(self) -> pipeline_pb2.TimeReference:
        if self == TectonTimeConstant.MATERIALIZATION_START_TIME:
            return pipeline_pb2.TimeReference.TIME_REFERENCE_MATERIALIZATION_START_TIME
        elif self == TectonTimeConstant.MATERIALIZATION_END_TIME:
            return pipeline_pb2.TimeReference.TIME_REFERENCE_MATERIALIZATION_END_TIME
        elif self == TectonTimeConstant.UNBOUNDED_PAST:
            return pipeline_pb2.TimeReference.TIME_REFERENCE_UNBOUNDED_PAST
        elif self == TectonTimeConstant.UNBOUNDED_FUTURE:
            return pipeline_pb2.TimeReference.TIME_REFERENCE_UNBOUNDED_FUTURE
        else:
            err = f"Unsupported TectonTimeConstant: {self}"
            raise ValueError(err)

    @classmethod
    def from_proto(cls, proto: pipeline_pb2.TimeReference) -> Optional[TectonTimeConstant]:
        if proto == pipeline_pb2.TimeReference.TIME_REFERENCE_MATERIALIZATION_START_TIME:
            return TectonTimeConstant.MATERIALIZATION_START_TIME
        elif proto == pipeline_pb2.TimeReference.TIME_REFERENCE_MATERIALIZATION_END_TIME:
            return TectonTimeConstant.MATERIALIZATION_END_TIME
        elif proto == pipeline_pb2.TimeReference.TIME_REFERENCE_UNBOUNDED_PAST:
            return TectonTimeConstant.UNBOUNDED_PAST
        elif proto == pipeline_pb2.TimeReference.TIME_REFERENCE_UNBOUNDED_FUTURE:
            return TectonTimeConstant.UNBOUNDED_FUTURE
        else:
            return None
