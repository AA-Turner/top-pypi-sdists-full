import logging
from dataclasses import dataclass, field
from datetime import datetime, timedelta, timezone
from typing import Callable, Dict, Iterable, List, Optional, Set, Type, Union

from acryl_datahub_cloud.periodic_analytics.billing_sync.close_writer import (
    read_latest_close,
)
from acryl_datahub_cloud.periodic_analytics.config import RollupSourceConfig
from acryl_datahub_cloud.periodic_analytics.constants import (
    ROLLUP_SOURCE_KIND,
    Layer,
    RunMode,
)
from acryl_datahub_cloud.periodic_analytics.partitions import (
    DayPartition,
    HourPartition,
    MonthPartition,
    hours_between,
)
from acryl_datahub_cloud.periodic_analytics.registry import MetricRegistry
from acryl_datahub_cloud.periodic_analytics.rollup.daily import (
    run_compact_daily_additive,
    run_compact_daily_distinct,
)
from acryl_datahub_cloud.periodic_analytics.rollup.hourly import run_hourly_rollup
from acryl_datahub_cloud.periodic_analytics.rollup.monthly import run_compact_monthly
from acryl_datahub_cloud.periodic_analytics.rollup.planner import (
    RollupPlan,
    RollupPlanner,
    scheduled_events_start,
)
from acryl_datahub_cloud.periodic_analytics.run_lock import (
    LockClient,
    RunLock,
    RunLockOwnershipLostError,
    build_run_lock,
)
from acryl_datahub_cloud.periodic_analytics.storage import ObjectStore
from acryl_datahub_cloud.periodic_analytics.watermark import WatermarkStore
from datahub.ingestion.api.common import PipelineContext
from datahub.ingestion.api.decorators import (
    SupportStatus,
    config_class,
    platform_name,
    support_status,
)
from datahub.ingestion.api.source import Source, SourceReport
from datahub.ingestion.api.workunit import MetadataWorkUnit
from datahub.ingestion.api.workunit_processor import WorkunitProcessor
from datahub.ingestion.workunit_processors.auto_workunits_reporter import (
    AutoWorkunitsReporterProcessor,
)

logger = logging.getLogger(__name__)

_PIPELINE_RESTATE_TARGETS = [
    Layer.HOURLY,
    Layer.DAILY_ADDITIVE,
    Layer.DAILY_DISTINCT,
    Layer.MONTHLY,
]


@dataclass
class _FamilyContext:
    metric_family: str
    hourly_wm: WatermarkStore
    daily_wm: WatermarkStore
    monthly_wm: WatermarkStore
    planner: RollupPlanner


@dataclass
class PeriodicAnalyticsRollupReport(SourceReport):
    hours_planned: int = 0
    hours_rolled: int = 0
    hours_zero_initialized: int = 0
    hours_archived_backlog: int = 0
    days_compacted: int = 0
    months_compacted: int = 0
    partitions_deferred: int = 0
    partitions_failed: int = 0
    families_run: List[str] = field(default_factory=list)


@platform_name(id="datahub", platform_name="datahub")
@config_class(RollupSourceConfig)
@support_status(SupportStatus.INCUBATING)
class DataHubPeriodicAnalyticsRollupSource(Source):
    def __init__(
        self,
        ctx: PipelineContext,
        config: RollupSourceConfig,
        now_fn: Callable[[], datetime] = lambda: datetime.now(timezone.utc),
        lock_client: Optional[LockClient] = None,
    ):
        super().__init__(ctx)
        self.config = config
        self.report = PeriodicAnalyticsRollupReport()
        self.report.event_not_produced_warn = False
        self.job_run_id = ctx.run_id
        self.now_fn = now_fn
        # Test-only override — bypasses provider dispatch in build_run_lock
        # so source-level lock tests don't need real S3/boto3.
        self._lock_client_override = lock_client
        # Set in get_workunits_internal once the lock is built, so
        # _verify_lock_ownership_or_abort can re-check the SAME lease object
        # right before each watermark commit.
        self._run_lock: Optional[RunLock] = None
        self._families: List[_FamilyContext] = []

        if config.object_storage is None:
            # Bootstrap values env var unset — see config._object_storage_is_unset.
            # Configure cleanly and no-op in get_workunits_internal rather than
            # failing every SYSTEM-source run on an instance that hasn't set up
            # periodic analytics yet.
            return

        self.store = ObjectStore(config.object_storage)
        self.registry = MetricRegistry.load(config.metric_registry_override)
        for family in config.metric_families:
            hourly_wm = WatermarkStore(self.store, family, Layer.HOURLY)
            # R11 split-brain fix: HOURLY/HOURLY_DISTINCT already share a single
            # watermark; DAILY_ADDITIVE/DAILY_DISTINCT used to have two separate
            # manifests over the same source data, letting one layer's watermark
            # advance while the other's didn't. Unify daily the same way as
            # hourly — one watermark, marked only once both layers succeed.
            daily_wm = WatermarkStore(self.store, family, Layer.DAILY_ADDITIVE)
            monthly_wm = WatermarkStore(self.store, family, Layer.MONTHLY)
            self._families.append(
                _FamilyContext(
                    metric_family=family,
                    hourly_wm=hourly_wm,
                    daily_wm=daily_wm,
                    monthly_wm=monthly_wm,
                    planner=RollupPlanner(
                        config=config,
                        hourly_wm=hourly_wm,
                        daily_wm=daily_wm,
                        monthly_wm=monthly_wm,
                    ),
                )
            )

    def get_report(self) -> SourceReport:
        return self.report

    def close(self) -> None:
        store = getattr(self, "store", None)
        if store is not None:
            store.close()
        super().close()

    def get_allowed_workunit_processors(
        self,
    ) -> Optional[List[Union[str, Type[WorkunitProcessor]]]]:
        return [AutoWorkunitsReporterProcessor]

    def get_workunits_internal(self) -> Iterable[MetadataWorkUnit]:
        if self.config.object_storage is None:
            self.report.warning(
                title="Periodic analytics rollup not configured",
                message="object_storage uri/bucket/customer_id/instance_id are unset "
                "— skipping this run (no-op) until "
                "DATAHUB_PERIODIC_ANALYTICS_ROLLUP_BOOTSTRAP_VALUES is set "
                "(or DATAHUB_OBJECT_STORAGE_URI + BILLING_* env fallback)",
            )
            return

        now = self.now_fn()
        logger.info(
            "planning rollup work for %s/%s families=%s run_mode=%s",
            self.config.object_storage.customer_id,
            self.config.object_storage.instance_id,
            self.config.metric_families,
            self.config.run_mode.value,
        )
        is_restate = self.config.run_mode in (RunMode.RESTATE, RunMode.PIPELINE_RESTATE)
        for family_ctx in self._families:
            family = family_ctx.metric_family
            self._run_lock = self._build_run_lock(family)
            with self._run_lock as acquired:
                if not acquired:
                    # Mirrors the object_storage-unconfigured no-op above: the run
                    # succeeds with zero workunits rather than failing, since a
                    # concurrent run already owns this tenant+layer's work.
                    self.report.warning(
                        title="Rollup skipped — run lock held",
                        message="another run of this source is already in progress "
                        "for this tenant; skipping this family (no-op)",
                        context=self.store.lock_key(ROLLUP_SOURCE_KIND, family),
                    )
                    continue
                self._run_family(family_ctx, now, is_restate)
        yield from []

    def _build_run_lock(self, metric_family: str) -> RunLock:
        # Only called after get_workunits_internal's object_storage check, so
        # self.store (set in __init__ in that same branch) is always present.
        if self._lock_client_override is not None:
            return RunLock(
                client=self._lock_client_override,
                key=self.store.lock_key(ROLLUP_SOURCE_KIND, metric_family),
                run_id=self.job_run_id,
                lease_minutes=self.config.lock_lease_minutes,
                report=self.report,
                now_fn=self.now_fn,
                steal_skew_minutes=self.config.lock_steal_skew_minutes,
            )
        return build_run_lock(
            self.store,
            ROLLUP_SOURCE_KIND,
            metric_family,
            self.job_run_id,
            self.config.lock_lease_minutes,
            self.report,
            now_fn=self.now_fn,
            steal_skew_minutes=self.config.lock_steal_skew_minutes,
        )

    def _verify_lock_ownership_or_abort(self, context: str) -> None:
        # Called immediately before each watermark commit below. An
        # overrunning run (lock_lease_minutes too short for this tenant's
        # real run time) can have its lease stolen mid-run; without this
        # check the old run would keep marking watermarks complete after the
        # steal winner already owns the tenant, corrupting the very
        # single-writer guarantee the lock exists to provide.
        # self._run_lock is only None when _run/_execute_* are exercised
        # directly in a test, bypassing get_workunits_internal (which always
        # sets it before _run) -- nothing to verify there, same as the
        # client=None "no lock backend" case.
        if self._run_lock is None or self._run_lock.verify_ownership():
            return
        message = (
            "the run lock lease was stolen while this run was still "
            "executing (lock_lease_minutes too short for this run) -- "
            "another run now owns this tenant. Aborting before this "
            "commit rather than writing state the new owner also owns."
        )
        self.report.failure(
            title="Run lock ownership lost mid-run", message=message, context=context
        )
        raise RunLockOwnershipLostError(message)

    def _run_family(
        self, family_ctx: _FamilyContext, now: datetime, is_restate: bool
    ) -> None:
        family = family_ctx.metric_family
        zero_initialized = 0
        if not is_restate:
            zero_initialized = self._initialize_leading_empty_hours(family_ctx, now)
        plan = self._plan_for_mode(family_ctx, now)
        if is_restate:
            self._refuse_if_finalized(family, plan)

        # Cache the per-day events check: plan.hourly commonly holds many
        # hours of the same day, and each check is an object-store listing.
        day_has_events: Dict[str, bool] = {}
        for hour in plan.hourly:
            if hour.day.key not in day_has_events:
                day_has_events[hour.day.key] = self.store.day_has_event_files(
                    family, hour.day
                )
        archived_backlog = sum(
            1 for hour in plan.hourly if day_has_events[hour.day.key]
        )
        self.report.hours_archived_backlog += archived_backlog

        logger.info(
            "rollup plan family=%s: hourly=%d daily=%d monthly=%d deferred=%d "
            "blocked=%d skipped_months=%d zero_initialized=%d archived_backlog=%d",
            family,
            len(plan.hourly),
            len(plan.daily),
            len(plan.monthly),
            len(plan.deferred_hours),
            len(plan.blocked_days),
            len(plan.skipped_months),
            zero_initialized,
            archived_backlog,
        )

        self.report.partitions_deferred += len(plan.deferred_hours)
        # Steady state plans 1-few due hours on a day that already has events
        # — that is healthy, not backlog. Only warn when this wake is actually
        # catching up: the plan is saturated at the partition cap, or the same
        # run had to zero-initialize leading hours (first enablement).
        backlog_is_catch_up = (
            archived_backlog >= self.config.max_partitions_per_run
            or zero_initialized > 0
        )
        if archived_backlog and backlog_is_catch_up:
            self.report.warning(
                title="Archived event backlog",
                message=(
                    "hour(s) with archived events are queued for rollup; "
                    "progress is bounded by max_partitions_per_run each wake"
                ),
                context=f"{family}: {archived_backlog} hour(s) this run",
            )
        # TG-3: daily compaction requires all 24 hourly watermarks — a day
        # short even one hour cannot be safely summed.
        for day, missing in plan.blocked_days:
            self.report.warning(
                title="Day blocked by missing hours",
                message="daily compaction requires all 24 hourly watermarks",
                context=f"{family}/{day.key}: missing {missing}",
            )
        for month, missing_day_count in plan.skipped_months:
            self.report.warning(
                title="Monthly rollup skipped",
                message=(
                    "month is not fully compacted yet; monthly recomputes when "
                    "all days are complete"
                ),
                context=(
                    f"{family}/{month.key}: {missing_day_count} day(s) not yet complete"
                ),
            )

        self._execute_plan(family_ctx, plan, is_restate)
        self.report.families_run.append(family)

    def _leading_empty_hours_to_initialize(
        self, family: str, now: datetime, completed: Set[str]
    ) -> List[HourPartition]:
        """Eligible incomplete hours before the first day that has archived events.

        Stops at the first day with event parquet so activation-forward hours
        still go through normal (capped) rollup. Hours after that boundary that
        lack events are not treated as leading and keep the ordinary empty-hour
        rollup path.

        Emptiness is judged by the absence of archived parquet, and the
        upstream archiver may land a day's events well after input_lag. A day
        is therefore only batch-sealed as zero once it has been fully elapsed
        for max(input_lag, zero_init_archive_grace_hours); more recent days
        stop the walk and stay on the ordinary rollup path.
        """
        events_start = scheduled_events_start(now)
        now_utc = now.astimezone(timezone.utc)
        lag = timedelta(minutes=self.config.input_lag.hourly_minutes)
        archive_grace = max(
            lag, timedelta(hours=self.config.zero_init_archive_grace_hours)
        )
        leading: List[HourPartition] = []
        seen_days: List[DayPartition] = []
        for hour in hours_between(events_start, now_utc):
            if not seen_days or seen_days[-1].key != hour.day.key:
                seen_days.append(hour.day)

        for day in seen_days:
            if now_utc < day.hours[-1].end + archive_grace:
                return leading
            if self.store.day_has_event_files(family, day):
                break
            for hour in day.hours:
                if hour.start < events_start:
                    continue
                if now_utc < hour.end + lag:
                    return leading
                if hour.key not in completed:
                    leading.append(hour)
        return leading

    def _initialize_leading_empty_hours(
        self, family_ctx: _FamilyContext, now: datetime
    ) -> int:
        """Zero-initialize event-free leading hours; returns the count sealed.

        Mid-month first enablement: billing-sync requires contiguous hourly
        watermarks from month start, but scheduled rollup previously only
        looked back 7 days. Confirm event-free leading hours, write empty
        hourly outputs (daily compaction requires parquet), then batch the
        watermark so pre-activation time is explicitly zero without waiting
        for dozens of capped wakes.
        """
        if "hourly" not in self.config.grains:
            return 0
        family = family_ctx.metric_family
        completed = set(family_ctx.hourly_wm.completed_keys())
        leading = self._leading_empty_hours_to_initialize(family, now, completed)
        if not leading:
            return 0

        context = f"{family}/leading-empty:{leading[0].key}..{leading[-1].key}"
        self._verify_lock_ownership_or_abort(context)
        for hour in leading:
            hour_context = f"{family}/{hour.key}"
            self._verify_lock_ownership_or_abort(hour_context)
            self._clear_targets(family, hour=hour)
            try:
                run_hourly_rollup(
                    self.store,
                    self.registry,
                    family,
                    hour,
                    self.job_run_id,
                )
            except Exception as exc:
                self.report.partitions_failed += 1
                self.report.failure(
                    title="Leading empty-hour initialization failed",
                    message=str(exc),
                    context=hour_context,
                )
                logger.exception(
                    "leading empty-hour init failed for family=%s hour=%s",
                    family,
                    hour.key,
                )
                return 0

        self._verify_lock_ownership_or_abort(context)
        family_ctx.hourly_wm.mark_complete_many(
            [hour.key for hour in leading], self.job_run_id
        )
        self.report.hours_zero_initialized += len(leading)
        logger.info(
            "rollup family=%s: zero-initialized %d leading empty hour(s) (%s .. %s)",
            family,
            len(leading),
            leading[0].key,
            leading[-1].key,
        )
        self.report.warning(
            title="Leading empty hours initialized",
            message=(
                "watermarked hour(s) with no archived events before the first "
                "day of activity so month-start contiguity can advance after "
                "mid-month billing enablement — not a missing-data failure"
            ),
            context=f"{family}: {len(leading)} hour(s)",
        )
        return len(leading)

    def _plan_for_mode(self, family_ctx: _FamilyContext, now: datetime) -> RollupPlan:
        planner = family_ctx.planner
        if self.config.run_mode == RunMode.PIPELINE_RESTATE:
            assert self.config.restate is not None  # enforced by config validator
            # pipeline_restate always regenerates the full hourly->daily->monthly
            # chain — the configured targets are ignored, since dependency order
            # is inherent in the existing execution order in _execute_plan.
            restate = self.config.restate.model_copy(
                update={"targets": _PIPELINE_RESTATE_TARGETS}
            )
            return planner.plan_restate(restate, pipeline_mode=True)
        if self.config.run_mode == RunMode.RESTATE:
            assert self.config.restate is not None  # enforced by config validator
            return planner.plan_restate(self.config.restate)
        # v1: catch_up and scheduled intentionally share planning here —
        # auto_catch_up already drains any gaps via plan(), so catch_up does
        # not yet need a distinct code path. Window covers current month plus
        # the rolling 7-day lookback when that extends into the prior month.
        return planner.plan(now=now, events_start=scheduled_events_start(now))

    def _execute_plan(
        self, family_ctx: _FamilyContext, plan: RollupPlan, is_restate: bool
    ) -> None:
        for hour in plan.hourly:
            self.report.hours_planned += 1
            self._execute_hourly(family_ctx, hour)
        for day in plan.daily:
            self._execute_daily(family_ctx, day, is_restate)
        for month in plan.monthly:
            self._execute_monthly(family_ctx, month)

    def _touched_periods(self, plan: RollupPlan) -> Set[str]:
        periods: Set[str] = set()
        periods.update(hour.day.month.key for hour in plan.hourly)
        periods.update(day.month.key for day in plan.daily)
        periods.update(month.key for month in plan.monthly)
        return periods

    def _refuse_if_finalized(self, metric_family: str, plan: RollupPlan) -> None:
        # R12/R14: a finalized billing close is a promise already made to the
        # customer — restating the layers it was computed from would silently
        # invalidate a number that's already gone out. Refuse before touching
        # any storage.
        finalized_periods: List[str] = []
        for period in sorted(self._touched_periods(plan)):
            snapshot = read_latest_close(self.store, metric_family, period)
            if snapshot is not None and snapshot.finalized:
                finalized_periods.append(period)
        if finalized_periods:
            message = (
                f"restate refused for family={metric_family}: period(s) already "
                f"finalized: {finalized_periods}"
            )
            self.report.failure(
                title="Restate refused — period already finalized",
                message=message,
                context=str(finalized_periods),
            )
            raise ValueError(message)

    def _clear_targets(
        self,
        metric_family: str,
        hour: Optional[HourPartition] = None,
        day_additive: Optional[DayPartition] = None,
        day_distinct: Optional[DayPartition] = None,
        month: Optional[MonthPartition] = None,
    ) -> None:
        # C1: called unconditionally at the top of each _execute_* method, in
        # both scheduled and restate paths, so re-executing a partition never
        # leaves a prior generation's parquet files beside the new ones (the
        # double-counting-on-retry bug). Scheduled/catch_up only ever hits an
        # already-populated dir here when a prior partial failure left
        # orphaned output; restate hits one on purpose. Daily clears one
        # layer at a time (not both together) so a distinct-only re-run never
        # touches the already-committed additive generation.
        if hour is not None:
            self.store.delete_dir_contents(
                self.store.hour_dir(metric_family, Layer.HOURLY, hour)
            )
            self.store.delete_dir_contents(
                self.store.hour_dir(metric_family, Layer.HOURLY_DISTINCT, hour)
            )
        if day_additive is not None:
            self.store.delete_dir_contents(
                self.store.day_dir(metric_family, Layer.DAILY_ADDITIVE, day_additive)
            )
        if day_distinct is not None:
            self.store.delete_dir_contents(
                self.store.day_dir(metric_family, Layer.DAILY_DISTINCT, day_distinct)
            )
        if month is not None:
            self.store.delete_dir_contents(
                self.store.period_dir(metric_family, Layer.MONTHLY, month.key)
            )

    def _execute_hourly(self, family_ctx: _FamilyContext, hour: HourPartition) -> None:
        family = family_ctx.metric_family
        logger.info(
            "rolling up events -> hourly_buckets for family=%s hour=%s",
            family,
            hour.key,
        )
        # C1/Critical-1: verify BEFORE clearing or writing, not just before
        # the watermark commit below. A run that already lost the lease must
        # not wipe this partition's existing (winner-owned) output nor write
        # a fresh stale generation beside it -- catching the loss only at
        # commit time is too late for those two side effects.
        self._verify_lock_ownership_or_abort(f"{family}/{hour.key}")
        self._clear_targets(family, hour=hour)
        try:
            result = run_hourly_rollup(
                self.store,
                self.registry,
                family,
                hour,
                self.job_run_id,
            )
        except Exception as exc:
            # TG-8: the hourly watermark must NOT advance on failure — leave
            # this hour due again next run rather than mark it complete on a
            # partial or missing write.
            self.report.partitions_failed += 1
            self.report.failure(
                title="Hourly rollup failed",
                message=str(exc),
                context=f"{family}/{hour.key}",
            )
            logger.exception(
                "hourly rollup failed for family=%s hour=%s", family, hour.key
            )
            return
        if result.unregistered_rows:
            self.report.warning(
                title="Unregistered metric_name(s) skipped",
                message=(
                    "events rows with a metric_name absent from the metric "
                    "registry were skipped from hourly aggregation"
                ),
                context=f"{family}/{hour.key}: {result.unregistered_rows} row(s)",
            )
        self.report.hours_rolled += 1
        self._verify_lock_ownership_or_abort(f"{family}/{hour.key}")
        family_ctx.hourly_wm.mark_complete(hour.key, self.job_run_id)

    def _execute_daily(
        self, family_ctx: _FamilyContext, day: DayPartition, is_restate: bool
    ) -> None:
        family = family_ctx.metric_family
        logger.info(
            "compacting hourly -> daily_buckets for family=%s dt=%s",
            family,
            day.key,
        )

        # R11: additive and distinct share ONE watermark (see __init__) —
        # two separate manifests over the same source data is a split-brain
        # risk (one layer's watermark could advance while the other's
        # doesn't). Clear both dirs and recompute both every time the day is
        # due; a partial failure just leaves the watermark unmarked so both
        # are cleared and redone next run — idempotent, no doubling.
        if is_restate or not family_ctx.daily_wm.is_complete(day.key):
            # C1/Critical-1: verify before clearing/writing (see
            # _execute_hourly) -- a lease already lost by this point must not
            # wipe or double-write this day's output.
            self._verify_lock_ownership_or_abort(f"{family}/{day.key}")
            self._clear_targets(family, day_additive=day, day_distinct=day)
            try:
                run_compact_daily_additive(
                    self.store,
                    family,
                    day,
                    self.job_run_id,
                    family_ctx.hourly_wm,
                )
                run_compact_daily_distinct(
                    self.store,
                    family,
                    day,
                    self.job_run_id,
                    family_ctx.hourly_wm,
                )
            except Exception as exc:
                self.report.partitions_failed += 1
                self.report.failure(
                    title="Daily compaction failed",
                    message=str(exc),
                    context=f"{family}/{day.key}",
                )
                logger.exception(
                    "daily compaction failed for family=%s dt=%s", family, day.key
                )
                return
            # TG-8: the daily watermark must NOT advance until both layers
            # have succeeded.
            self._verify_lock_ownership_or_abort(f"{family}/{day.key}")
            family_ctx.daily_wm.mark_complete(day.key, self.job_run_id)

        self.report.days_compacted += 1

    def _execute_monthly(
        self, family_ctx: _FamilyContext, month: MonthPartition
    ) -> None:
        family = family_ctx.metric_family
        logger.info(
            "compacting daily -> monthly_buckets for family=%s period=%s",
            family,
            month.key,
        )
        # C1/Critical-1: verify before clearing/writing (see _execute_hourly).
        self._verify_lock_ownership_or_abort(f"{family}/{month.key}")
        self._clear_targets(family, month=month)
        try:
            run_compact_monthly(
                self.store,
                family,
                month,
                self.job_run_id,
                family_ctx.daily_wm,
            )
        except Exception as exc:
            self.report.partitions_failed += 1
            self.report.failure(
                title="Monthly compaction failed",
                message=str(exc),
                context=f"{family}/{month.key}",
            )
            logger.exception(
                "monthly compaction failed for family=%s period=%s",
                family,
                month.key,
            )
            return
        self.report.months_compacted += 1
        self._verify_lock_ownership_or_abort(f"{family}/{month.key}")
        family_ctx.monthly_wm.mark_complete(month.key, self.job_run_id)
