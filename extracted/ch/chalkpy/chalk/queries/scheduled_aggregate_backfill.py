from __future__ import annotations

import inspect
from datetime import datetime, timezone
from enum import Enum
from typing import TYPE_CHECKING, Collection

from chalk.queries._schedule_entity_name import validate_schedule_entity_name
from chalk.utils.duration import CronTab, Duration

if TYPE_CHECKING:
    from chalk.client.models import FeatureReference


class AggregateBackfillTarget(str, Enum):
    ONLINE = "ONLINE"
    OFFLINE = "OFFLINE"


class ScheduledAggregateBackfill:
    """Schedules a recurring aggregate backfill job.

    Args:
        name: Unique name for this backfill job.
        features: The aggregated features to backfill.
        schedule: A cron expression or duration controlling how often the backfill runs.
        target: Which store to backfill — ``AggregateBackfillTarget.ONLINE`` or
            ``AggregateBackfillTarget.OFFLINE``. Mutually exclusive with ``targets``.
        targets: Collection of stores to backfill. Mutually exclusive with ``target``.
        query_tags: Tags to attach to the backfill query for observability.
        resource_group: Resource group for the backfill job.
        lower_bound: Start of the backfill window (UTC). Defaults to the feature's lookback.
        upper_bound: End of the backfill window (UTC). Defaults to now.
        allow_empty_tiles: If ``False``, tiles with no data raise an error.
        planner_options: Planner options to apply when executing the backfill.
        num_shards: Maximum number of bucket-aligned, time-sharded jobs to split each
            run's window into. Must be > 1 when set. The server chooses the actual count (at most this many,
            based on its per-shard window-width policy). Useful when a single job over
            the run's window would run out of memory or disk. Unset preserves the
            single-job behavior.
        environment: If set, this backfill is only scheduled when deploying to the named
            environment. Deploying to any other environment silently skips it — the backfill
            is not planned or persisted anywhere. Unlike ``ScheduledQuery``'s
            ``environment_override`` (which relocates the query to run in another environment),
            this is a deploy-time gate: the backfill simply does not exist outside of the
            specified environment.
    """

    def __init__(
        self,
        *,
        name: str,
        features: Collection[FeatureReference],
        schedule: CronTab | Duration,
        target: AggregateBackfillTarget | None = None,
        targets: Collection[AggregateBackfillTarget] | None = None,
        query_tags: Collection[str] | None = None,
        resource_group: str | None = None,
        lower_bound: datetime | None = None,
        upper_bound: datetime | None = None,
        allow_empty_tiles: bool = True,
        planner_options: dict[str, str] | None = None,
        environment: str | None = None,
        num_shards: int | None = None,
    ):
        super().__init__()
        self.errors = []

        name_err = validate_schedule_entity_name(name, entity_noun="Scheduled aggregate backfill")
        if name_err is not None:
            self.errors.append(name_err)

        if name in SCHEDULED_AGGREGATE_BACKFILL_REGISTRY:
            self.errors.append(
                f"A scheduled aggregate backfill with name '{name}' already exists. Names must be unique."
            )

        if len(features) == 0:
            self.errors.append(
                f"Scheduled aggregate backfill '{name}' was instantiated with an empty set of features. At least one feature is required."
            )

        resolved_targets: Collection[AggregateBackfillTarget]
        if target is not None:
            resolved_targets = [target]
        elif targets is not None:
            resolved_targets = targets
        else:
            raise TypeError(
                "ScheduledAggregateBackfill requires exactly one of the keyword-only arguments 'target' or 'targets'"
            )

        if target is not None and targets is not None:
            raise TypeError(
                "ScheduledAggregateBackfill requires exactly one of the keyword-only arguments 'target' or 'targets', but got both"
            )
        elif targets is not None and len(targets) == 0:
            self.errors.append(
                f"Scheduled aggregate backfill '{name}' was instantiated with an empty targets list, but at least one of AggregateBackfillTarget.ONLINE or AggregateBackfillTarget.OFFLINE is required"
            )

        for t in resolved_targets:  # type: ignore
            if not isinstance(t, AggregateBackfillTarget):  # type: ignore[arg-type]
                self.errors.append(
                    f"Scheduled aggregate backfill '{name}' was instantiated with invalid target '{target}'. Use AggregateBackfillTarget.ONLINE or AggregateBackfillTarget.OFFLINE."
                )

        if AggregateBackfillTarget.OFFLINE not in resolved_targets:
            # the if is added because older servers (pre 2026-05-28) were failing validation on
            # store_offline=False and allow_empty_tiles=True combination
            # (and now allow_empty_tiles=True is the default)
            # TODO remove this after a reasonable grace period
            allow_empty_tiles = False

        if num_shards is not None and num_shards <= 1:
            self.errors.append(
                f"Scheduled aggregate backfill '{name}' was instantiated with num_shards={num_shards}, but num_shards must be > 1 when set; omit it to run each run as a single job"
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
        self.targets = resolved_targets
        self.query_tags = list(query_tags) if query_tags is not None else None
        self.resource_group = resource_group
        self.lower_bound = lower_bound
        self.upper_bound = upper_bound
        self.allow_empty_tiles = allow_empty_tiles
        self.planner_options = {k: str(v) for k, v in planner_options.items()} if planner_options else None
        self.environment = environment
        self.num_shards = num_shards
        self.filename = caller_filename

        SCHEDULED_AGGREGATE_BACKFILL_REGISTRY[name] = self


SCHEDULED_AGGREGATE_BACKFILL_REGISTRY: dict[str, ScheduledAggregateBackfill] = {}


__all__ = (
    "AggregateBackfillTarget",
    "SCHEDULED_AGGREGATE_BACKFILL_REGISTRY",
    "ScheduledAggregateBackfill",
)
