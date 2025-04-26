import datetime
import enum
from typing import Tuple

import attrs
from google.protobuf.duration_pb2 import Duration
from typeguard import typechecked

from tecton_core.errors import TectonValidationError
from tecton_core.time_utils import timedelta_to_proto
from tecton_core.time_utils import to_human_readable_str
from tecton_proto.args.feature_view__client_pb2 import TimeWindow as TimeWindowArgs
from tecton_proto.args.feature_view__client_pb2 import TimeWindowSeries as TimeWindowSeriesArgs
from tecton_proto.common.time_window__client_pb2 import LifetimeWindow
from tecton_proto.common.time_window__client_pb2 import RelativeTimeWindow
from tecton_proto.common.time_window__client_pb2 import TimeWindow
from tecton_proto.common.time_window__client_pb2 import TimeWindowSeries


__all__ = [
    "LifetimeWindowSpec",
    "RelativeTimeWindowSpec",
    "TimeWindowSpec",
    "create_time_window_spec_from_data_proto",
    "window_spec_to_window_data_proto",
]


class _WindowSortEnum(enum.IntEnum):
    TIME_WINDOW = 1
    LIFETIME = 2
    TIME_WINDOW_SERIES = 3


_TimeWindowSortKey = Tuple[_WindowSortEnum, tuple]


class TimeWindowSpec:
    def window_duration_string(self) -> str:
        """Window duration for use in aggregation name construction."""
        raise NotImplementedError

    def to_string(self) -> str:
        """Full name specification for use in secondary key aggregation output column."""
        raise NotImplementedError

    def to_sort_tuple(self) -> _TimeWindowSortKey:
        """Tuple for sorting time windows.

        This should start with the appropriate _WindowSortEnum, and then use any attributes for the specific window type for sorting.
        This approach ensures that we have a multi-layer sort where each sub-type is collocated together.
        """
        raise NotImplementedError


@attrs.frozen
class LifetimeWindowSpec(TimeWindowSpec):
    def to_proto(self) -> LifetimeWindow:
        return LifetimeWindow()

    def to_string(self) -> str:
        return "lifetime"

    def offset_string(self) -> str:
        return ""

    def window_duration_string(self) -> str:
        return "lifetime"

    def to_sort_tuple(self) -> _TimeWindowSortKey:
        return (_WindowSortEnum.LIFETIME, ())


@attrs.frozen(order=True)
class RelativeTimeWindowSpec(TimeWindowSpec):
    # window_end represents the offset (negative or zero)
    # window_start represents the offset - window_duration (negative)
    window_start: datetime.timedelta
    window_end: datetime.timedelta

    @classmethod
    @typechecked
    def from_data_proto(cls, proto: RelativeTimeWindow) -> "RelativeTimeWindowSpec":
        return cls(
            window_start=proto.window_start.ToTimedelta(),
            window_end=proto.window_end.ToTimedelta(),
        )

    @classmethod
    @typechecked
    def from_args_proto(cls, proto: TimeWindowArgs) -> "RelativeTimeWindowSpec":
        return cls(
            window_start=Duration(
                seconds=proto.offset.seconds - proto.window_duration.seconds,
                nanos=proto.offset.nanos - proto.window_duration.nanos,
            ).ToTimedelta(),
            window_end=Duration(seconds=proto.offset.seconds, nanos=proto.offset.nanos).ToTimedelta(),
        )

    def to_data_proto(self) -> RelativeTimeWindow:
        return RelativeTimeWindow(
            window_start=timedelta_to_proto(self.window_start),
            window_end=timedelta_to_proto(self.window_end),
        )

    @property
    def window_duration(self) -> datetime.timedelta:
        return self.window_end - self.window_start

    @property
    def offset(self) -> datetime.timedelta:
        return self.window_end

    def to_args_proto(self) -> TimeWindowArgs:
        return TimeWindowArgs(
            window_duration=timedelta_to_proto(self.window_duration),
            offset=timedelta_to_proto(self.offset),
        )

    def to_string(self) -> str:
        offset_name = self.offset_string()
        if offset_name:
            offset_name = f"_{self.offset_string()}"
        return f"{self.window_duration_string()}{offset_name}"

    def to_sort_tuple(self) -> _TimeWindowSortKey:
        return (_WindowSortEnum.TIME_WINDOW, (self.window_start, self.window_end))

    def offset_string(self) -> str:
        return "offset_" + to_human_readable_str(-self.offset) if self.offset.total_seconds() < 0 else ""

    def window_duration_string(self) -> str:
        return to_human_readable_str(self.window_duration)


@attrs.frozen(order=True)
class TimeWindowSeriesSpec(TimeWindowSpec):
    # time_windows represent the tuple of relative time windows - we use a tuple so this can be hashable for secondary key aggregate sorting
    time_windows: Tuple[RelativeTimeWindowSpec]

    @classmethod
    @typechecked
    def from_data_proto(cls, proto: TimeWindowSeries) -> "TimeWindowSeriesSpec":
        time_window_specs = ()
        for time_window in proto.time_windows:
            time_window_specs += (RelativeTimeWindowSpec.from_data_proto(time_window),)
        return cls(time_windows=time_window_specs)

    @classmethod
    @typechecked
    def from_args_proto(cls, proto: TimeWindowSeriesArgs) -> "TimeWindowSeriesSpec":
        # If we don't have at least one window in this time range then downstream functions for local development will fail
        time_window_specs = ()
        for i in range(
            proto.series_start.seconds,
            (proto.series_end.seconds - proto.window_duration.seconds) + 1,
            proto.step_size.seconds,
        ):
            time_window_specs += (
                RelativeTimeWindowSpec.from_data_proto(
                    RelativeTimeWindow(
                        window_start=Duration(seconds=i),
                        window_end=Duration(seconds=(i + proto.window_duration.seconds)),
                    )
                ),
            )
        # We need this assertion to ensure that NDD dependencies on this function do not break
        if len(time_window_specs) < 2:
            msg = "Time window series must have at least two windows"
            raise TectonValidationError(msg)
        return cls(time_windows=time_window_specs)

    def to_args_proto(self) -> TimeWindowSeriesArgs:
        return TimeWindowSeriesArgs(
            window_duration=timedelta_to_proto(self.window_duration),
            series_start=timedelta_to_proto(self.window_series_start),
            series_end=timedelta_to_proto(self.window_series_end),
            step_size=timedelta_to_proto(self.step_size),
        )

    def to_data_proto(self) -> TimeWindowSeries:
        return TimeWindowSeries(
            time_windows=[window.to_data_proto() for window in self.time_windows],
        )

    @property
    def window_duration(self) -> datetime.timedelta:
        return self.time_windows[0].window_duration

    @property
    def window_series_start(self) -> datetime.timedelta:
        return self.time_windows[0].window_start

    @property
    def step_size(self) -> datetime.timedelta:
        # At least two windows are guaranteed during validation
        return abs(self.time_windows[1].window_start - self.time_windows[0].window_start)

    @property
    def window_series_end(self) -> datetime.timedelta:
        return self.time_windows[-1].window_end

    def window_series_start_string(self) -> str:
        return to_human_readable_str(abs(self.window_series_start))

    def window_series_end_string(self) -> str:
        return to_human_readable_str(abs(self.window_series_end))

    def step_size_string(self) -> str:
        return to_human_readable_str(self.step_size)

    def window_duration_string(self) -> str:
        return to_human_readable_str(self.window_duration)

    def to_string(self) -> str:
        return f"{self.window_duration_string()}_series_{self.window_series_start_string()}_{self.window_series_end_string()}_{self.step_size_string()}"

    def to_sort_tuple(self) -> _TimeWindowSortKey:
        return (
            _WindowSortEnum.TIME_WINDOW_SERIES,
            (self.window_series_start, self.window_series_end, self.window_duration, self.step_size),
        )


def window_spec_to_window_data_proto(window_spec: TimeWindowSpec) -> TimeWindow:
    if isinstance(window_spec, RelativeTimeWindowSpec):
        return TimeWindow(relative_time_window=window_spec.to_data_proto())
    elif isinstance(window_spec, TimeWindowSeriesSpec):
        return TimeWindow(time_window_series=window_spec.to_data_proto())
    elif isinstance(window_spec, LifetimeWindowSpec):
        return TimeWindow(lifetime_window=window_spec.to_proto())
    else:
        msg = f"Unexpected time window type: {type(window_spec)}"
        raise ValueError(msg)


def create_time_window_spec_from_data_proto(proto: TimeWindow) -> TimeWindowSpec:
    if proto.HasField("time_window_series"):
        return TimeWindowSeriesSpec.from_data_proto(proto.time_window_series)
    elif proto.HasField("relative_time_window"):
        return RelativeTimeWindowSpec.from_data_proto(proto.relative_time_window)
    elif proto.HasField("lifetime_window"):
        return LifetimeWindowSpec()
    else:
        msg = f"Unexpected time window type: {proto}"
        raise ValueError(msg)
