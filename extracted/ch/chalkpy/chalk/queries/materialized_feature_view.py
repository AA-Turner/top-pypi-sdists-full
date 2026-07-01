from __future__ import annotations

import inspect
from datetime import datetime, timezone
from typing import TYPE_CHECKING, Type

from chalk.utils.duration import CronTab, Duration

if TYPE_CHECKING:
    from chalk.features.feature_set import Features


class MaterializedFeatureView:
    """Declares materialization scheduling and time-resolution config for one feature namespace.

    Args:
        namespace: The feature class (decorated with ``@features``) or its namespace string.
        time_resolution: Bucket duration for time-series materialization, e.g. ``"1s"``.
        update_cadence: How often to refresh materialized data — a cron expression or duration.
        lower_bound: Earliest timestamp to materialize from. Defaults to ``None``, which materializes from the beginning of time.
        lookback_retention_period: How far back to retain materialized data. Defaults to ``None``, which retains data indefinitely.
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
