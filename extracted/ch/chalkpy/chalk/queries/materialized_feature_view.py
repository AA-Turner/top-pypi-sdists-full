from __future__ import annotations

import inspect
import re
from datetime import datetime, timedelta, timezone
from typing import TYPE_CHECKING, Type

from chalk.utils.duration import CronTab, Duration, parse_chalk_duration

if TYPE_CHECKING:
    from chalk.features.feature_set import Features

_MIN_UPDATE_CADENCE = timedelta(minutes=10)
_CRON_FIELD_RE = re.compile(r"^[0-9*/,\-]+$")


def _is_cron_expression(s: str) -> bool:
    parts = s.split()
    return len(parts) == 5 and all(_CRON_FIELD_RE.match(p) for p in parts)


def _cron_min_interval_minutes(cron_expr: str) -> int:
    """Returns the minimum possible interval in minutes between firings of a cron expression."""
    minute_field = cron_expr.split()[0]
    values: set[int] = set()
    for part in minute_field.split(","):
        if part == "*":
            return 1
        if "/" in part:
            base, step_str = part.split("/", 1)
            step = int(step_str)
            if base == "*":
                start, end = 0, 59
            elif "-" in base:
                start, end = map(int, base.split("-", 1))
            else:
                start, end = int(base), 59
            values.update(range(start, end + 1, step))
        elif "-" in part:
            start, end = map(int, part.split("-", 1))
            values.update(range(start, end + 1))
        else:
            values.add(int(part))

    if len(values) <= 1:
        return 60
    sorted_vals = sorted(values)
    min_gap = min(b - a for a, b in zip(sorted_vals, sorted_vals[1:]))
    wrap_gap = sorted_vals[0] + 60 - sorted_vals[-1]
    return min(min_gap, wrap_gap)


class MaterializedFeatureView:
    """Declares materialization scheduling and time-resolution config for one feature namespace.

    Args:
        namespace: The feature class (decorated with ``@features``) or its namespace string.
        time_resolution: Bucket duration for time-series materialization, e.g. ``"1s"``.
        update_cadence: How often to refresh materialized data, as a cron expression or
            duration. Any finite cadence must be at least 10 minutes; more frequent
            updates are not supported.
        lower_bound: Fixed, inclusive lower bound on the feature times of observations
            included in the materialized feature view. Observations with earlier feature
            times continue to be retained in the observation tables, but are not copied
            to the view. Queries using wide table acceleration are therefore not aware
            of these observations. Defaults to ``None``, which applies no fixed lower
            bound.
        lookback_retention_period: Moving retention window on the feature times of
            observations included in the materialized feature view, measured back from
            the current execution time. Observations outside this window are deleted
            from the view. As with observations earlier than ``lower_bound``, they
            continue to be retained in the observation tables, but queries using wide
            table acceleration are not aware of them. When both retention parameters
            are set, the later lower bound applies. Defaults to ``None``, which applies
            no moving retention window, and therefore retains data indefinitely.
    """

    def __init__(
        self,
        namespace: "Type[Features] | str",
        *,
        time_resolution: Duration,
        update_cadence: "CronTab | Duration",
        lower_bound: datetime | None = None,
        lookback_retention_period: Duration | None = None,
    ):
        super().__init__()

        from chalk.features.feature_set import is_features_cls

        namespace_str: str
        if is_features_cls(namespace):
            namespace_str = namespace.__chalk_namespace__  # type: ignore[union-attr]
        elif isinstance(namespace, str):
            namespace_str = namespace
        else:
            raise TypeError(
                f"MaterializedFeatureView 'namespace' must be a @features class or a string, got {type(namespace).__name__!r}"
            )

        if lower_bound is not None and lower_bound.tzinfo is not None:
            lower_bound = lower_bound.astimezone(tz=timezone.utc)

        if isinstance(update_cadence, timedelta):
            if update_cadence < _MIN_UPDATE_CADENCE:
                raise ValueError(f"MaterializedFeatureView 'update_cadence' must be at least 10 minutes, but got {update_cadence!r}.")
        elif update_cadence not in ("infinity", "all"):
            if _is_cron_expression(update_cadence):
                min_interval = _cron_min_interval_minutes(update_cadence)
                if min_interval < 10:
                    raise ValueError(f"MaterializedFeatureView 'update_cadence' cron '{update_cadence}' can fire as frequently as every {min_interval} minute(s); the minimum allowed interval is 10 minutes.")
            else:
                td = parse_chalk_duration(update_cadence)
                if td < _MIN_UPDATE_CADENCE:
                    raise ValueError(f"MaterializedFeatureView 'update_cadence' must be at least 10 minutes, but got {update_cadence!r}.")

        from chalk.utils.object_inspect import get_source_object_starting

        source_line_start: int | None = None
        source_line_end: int | None = None
        source_code: str | None = None
        frame = inspect.currentframe()
        assert frame is not None, "Failed to get current frame"
        caller_frame = frame.f_back
        assert caller_frame is not None, "Failed to get caller frame"
        caller_filename = caller_frame.f_code.co_filename
        try:
            source_code, source_line_start, source_line_end = get_source_object_starting(caller_frame)
        except Exception:
            source_line_start = caller_frame.f_lineno
        del frame

        self.namespace = namespace_str
        self.time_resolution = time_resolution
        self.update_cadence = update_cadence
        self.lower_bound = lower_bound
        self.lookback_retention_period = lookback_retention_period
        self.filename = caller_filename
        self.source_line_start = source_line_start
        self.source_line_end = source_line_end
        self.code = source_code

        if namespace_str in MATERIALIZED_FEATURE_VIEW_REGISTRY:
            raise ValueError(
                f"A MaterializedFeatureView for namespace '{namespace_str}' already exists. Only one is allowed per namespace."
            )
        MATERIALIZED_FEATURE_VIEW_REGISTRY[namespace_str] = self

    def __repr__(self) -> str:
        return (
            f"MaterializedFeatureView("
            f"namespace={self.namespace!r}, "
            f"time_resolution={self.time_resolution!r}, "
            f"update_cadence={self.update_cadence!r}"
            f")"
        )

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, MaterializedFeatureView):
            return NotImplemented
        return (
            self.namespace == other.namespace
            and self.time_resolution == other.time_resolution
            and self.update_cadence == other.update_cadence
            and self.lower_bound == other.lower_bound
            and self.lookback_retention_period == other.lookback_retention_period
        )


MATERIALIZED_FEATURE_VIEW_REGISTRY: dict[str, MaterializedFeatureView] = {}


__all__ = (
    "MATERIALIZED_FEATURE_VIEW_REGISTRY",
    "MaterializedFeatureView",
)
