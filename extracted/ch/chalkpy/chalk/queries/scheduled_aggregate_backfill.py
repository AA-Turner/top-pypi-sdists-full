from __future__ import annotations

import inspect
from datetime import datetime, timezone
from enum import Enum
from typing import TYPE_CHECKING, Collection

from chalk.utils.duration import CronTab, Duration

if TYPE_CHECKING:
    from chalk.client.models import FeatureReference


class AggregateBackfillTarget(str, Enum):
    ONLINE = "ONLINE"
    OFFLINE = "OFFLINE"


class ScheduledAggregateBackfill:
    def __init__(
        self,
        *,
        name: str,
        features: Collection[FeatureReference],
        schedule: CronTab | Duration,
        target: AggregateBackfillTarget,
        query_tags: Collection[str] | None = None,
        resource_group: str | None = None,
        lower_bound: datetime | None = None,
        upper_bound: datetime | None = None,
    ):
        super().__init__()
        self.errors = []

        if name in SCHEDULED_AGGREGATE_BACKFILL_REGISTRY:
            self.errors.append(
                f"A scheduled aggregate backfill with name '{name}' already exists. Names must be unique."
            )

        if len(features) == 0:
            self.errors.append(
                f"Scheduled aggregate backfill '{name}' was instantiated with an empty set of features. At least one feature is required."
            )

        if not isinstance(target, AggregateBackfillTarget):  # type: ignore[arg-type]
            self.errors.append(
                f"Scheduled aggregate backfill '{name}' was instantiated with invalid target '{target}'. Use AggregateBackfillTarget.ONLINE or AggregateBackfillTarget.OFFLINE."
            )

        if lower_bound is not None:
            lower_bound = lower_bound.astimezone(tz=timezone.utc)
        if upper_bound is not None:
            upper_bound = upper_bound.astimezone(tz=timezone.utc)

        caller_filename = None
        frame = inspect.currentframe()
        assert frame is not None, "Failed to get current frame"
        caller_frame = frame.f_back
        assert caller_frame is not None, "Failed to get caller frame"
        caller_filename = caller_frame.f_code.co_filename
        del frame

        self.name = name
        self.features = list(dict.fromkeys(str(feature) for feature in features))
        self.schedule = schedule
        self.target = target
        self.query_tags = list(query_tags) if query_tags is not None else None
        self.resource_group = resource_group
        self.lower_bound = lower_bound
        self.upper_bound = upper_bound
        self.filename = caller_filename

        SCHEDULED_AGGREGATE_BACKFILL_REGISTRY[name] = self


SCHEDULED_AGGREGATE_BACKFILL_REGISTRY: dict[str, ScheduledAggregateBackfill] = {}


__all__ = (
    "AggregateBackfillTarget",
    "SCHEDULED_AGGREGATE_BACKFILL_REGISTRY",
    "ScheduledAggregateBackfill",
)
