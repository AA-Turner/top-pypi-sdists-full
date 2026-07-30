from dataclasses import dataclass, field
from datetime import datetime, timedelta, timezone
from typing import List, Optional, Set, Tuple

from acryl_datahub_cloud.periodic_analytics.config import (
    RestateConfig,
    RollupSourceConfig,
)
from acryl_datahub_cloud.periodic_analytics.constants import Layer
from acryl_datahub_cloud.periodic_analytics.partitions import (
    DAY_KEY_FORMAT,
    HOUR_KEY_FORMAT,
    DayPartition,
    HourPartition,
    MonthPartition,
    hours_between,
)
from acryl_datahub_cloud.periodic_analytics.watermark import WatermarkStore

PLANNING_LOOKBACK_DAYS = 7


def scheduled_events_start(now: datetime) -> datetime:
    """Earliest UTC instant covered by a scheduled/catch_up rollup plan.

    Always covers the current calendar month (so mid-month first enablement can
    reach day-1 watermarks) and retains the rolling 7-day lookback when that
    window extends into the prior month near month start.
    """
    now_utc = now.astimezone(timezone.utc)
    month_start = datetime(now_utc.year, now_utc.month, 1, tzinfo=timezone.utc)
    lookback_start = now_utc - timedelta(days=PLANNING_LOOKBACK_DAYS)
    return min(month_start, lookback_start)


def _parse_restate_key(key: str) -> Tuple[str, Optional[int]]:
    """Returns (YYYY-MM-DD, hour-or-None). hour is None for day-precision keys."""
    try:
        parsed = datetime.strptime(key, HOUR_KEY_FORMAT)
        return parsed.strftime(DAY_KEY_FORMAT), parsed.hour
    except ValueError:
        pass
    try:
        datetime.strptime(key, DAY_KEY_FORMAT)
    except ValueError:
        raise ValueError(f"unparseable restate partition key: {key!r}") from None
    return key, None


def _hour_range(
    start_date: str, start_hour: int, end_date: str, end_hour: int
) -> List[HourPartition]:
    start = HourPartition(start_date, start_hour).start
    end = HourPartition(end_date, end_hour).end
    return hours_between(start, end)


def _days_between(start_date: str, end_date: str) -> List[DayPartition]:
    cursor = datetime.strptime(start_date, DAY_KEY_FORMAT)
    end = datetime.strptime(end_date, DAY_KEY_FORMAT)
    days: List[DayPartition] = []
    while cursor <= end:
        days.append(DayPartition(cursor.strftime(DAY_KEY_FORMAT)))
        cursor += timedelta(days=1)
    return days


def _months_between(start_date: str, end_date: str) -> List[MonthPartition]:
    year, month = int(start_date[:4]), int(start_date[5:7])
    end_year, end_month = int(end_date[:4]), int(end_date[5:7])
    months: List[MonthPartition] = []
    while (year, month) <= (end_year, end_month):
        months.append(MonthPartition(f"{year:04d}-{month:02d}"))
        month += 1
        if month == 13:
            month, year = 1, year + 1
    return months


@dataclass
class RollupPlan:
    hourly: List[HourPartition] = field(default_factory=list)
    daily: List[DayPartition] = field(default_factory=list)
    monthly: List[MonthPartition] = field(default_factory=list)
    deferred_hours: List[HourPartition] = field(default_factory=list)
    blocked_days: List[Tuple[DayPartition, List[str]]] = field(default_factory=list)
    # Populated only by plan_restate(pipeline_mode=True): months that were
    # touched by the restated range but excluded from `monthly` because not
    # every day of the month will be complete post-run. Each entry is
    # (month, missing_day_count).
    skipped_months: List[Tuple[MonthPartition, int]] = field(default_factory=list)


class RollupPlanner:
    def __init__(
        self,
        config: RollupSourceConfig,
        hourly_wm: WatermarkStore,
        daily_wm: WatermarkStore,
        monthly_wm: WatermarkStore,
    ):
        self.config = config
        self.hourly_wm = hourly_wm
        self.daily_wm = daily_wm
        self.monthly_wm = monthly_wm

    def plan(self, now: datetime, events_start: datetime) -> RollupPlan:
        # Disabling a grain (config.grains) skips planning it entirely for
        # this recipe — readiness for the other grains still comes only from
        # persisted watermarks, so e.g. a daily-only recipe correctly plans
        # a day whose 24 hourly watermarks were written by a separate
        # hourly-only recipe run.
        plan = RollupPlan()
        completed = set(self.hourly_wm.completed_keys())
        if "hourly" in self.config.grains:
            self._plan_hourly(plan, now, events_start, completed)
        post_run: Set[str] = completed | {h.key for h in plan.hourly}

        today = now.astimezone(timezone.utc).strftime("%Y-%m-%d")
        daily_done = self.daily_wm.completed_keys()
        candidate_days = sorted({h.day for h in hours_between(events_start, now)})
        if "daily" in self.config.grains:
            self._plan_daily(plan, candidate_days, today, daily_done, post_run)
        post_run_days = daily_done | {d.key for d in plan.daily}

        if "monthly" in self.config.grains:
            self._plan_monthly(plan, candidate_days, today, post_run_days)
        return plan

    def _plan_hourly(
        self,
        plan: RollupPlan,
        now: datetime,
        events_start: datetime,
        completed: Set[str],
    ) -> None:
        lag = timedelta(minutes=self.config.input_lag.hourly_minutes)
        candidates = [
            h for h in hours_between(events_start, now) if h.key not in completed
        ]
        for hour in candidates:
            if now < hour.end + lag:
                plan.deferred_hours.append(hour)
            elif len(plan.hourly) < self.config.max_partitions_per_run:
                plan.hourly.append(hour)

    def _plan_daily(
        self,
        plan: RollupPlan,
        candidate_days: List[DayPartition],
        today: str,
        daily_done: Set[str],
        post_run: Set[str],
    ) -> None:
        for day in candidate_days:
            if day.key >= today or day.key in daily_done:
                continue
            missing = [h.key for h in day.hours if h.key not in post_run]
            if missing:
                plan.blocked_days.append((day, missing))
            else:
                plan.daily.append(day)

    def _plan_monthly(
        self,
        plan: RollupPlan,
        candidate_days: List[DayPartition],
        today: str,
        post_run_days: Set[str],
    ) -> None:
        this_month = today[:7]
        monthly_done = self.monthly_wm.completed_keys()
        for month in sorted({d.month for d in candidate_days}):
            if month.key >= this_month or month.key in monthly_done:
                continue
            if all(d.key in post_run_days for d in month.days):
                plan.monthly.append(month)

    def plan_restate(
        self, restate: RestateConfig, pipeline_mode: bool = False
    ) -> RollupPlan:
        """Operator-invoked recompute: enumerates the requested range for each
        target layer, ignoring watermarks entirely (unlike ``plan()``). No
        deferral/input-lag/max_partitions_per_run bound applies — the explicit
        range given by the operator is the bound.

        ``pipeline_mode`` (set only for RunMode.PIPELINE_RESTATE) makes
        monthly inclusion conditional: a touched month is planned only if
        every day of that month will be complete post-run, mirroring the
        scheduled planner's post-run-state check in ``_plan_monthly``.
        Incomplete touched months are reported via ``skipped_months`` instead.
        Explicit-target restate (pipeline_mode=False) keeps the strict
        behavior of always planning every touched month, letting monthly
        compaction fail loudly on an incomplete month.
        """
        start_date, start_hour = _parse_restate_key(restate.start_partition)
        end_date, end_hour = _parse_restate_key(restate.end_partition)
        start_hour_eff = start_hour if start_hour is not None else 0
        end_hour_eff = end_hour if end_hour is not None else 23
        if (end_date, end_hour_eff) < (start_date, start_hour_eff):
            raise ValueError(
                f"restate end_partition {restate.end_partition!r} precedes "
                f"start_partition {restate.start_partition!r}"
            )

        plan = RollupPlan()
        targets = set(restate.targets)
        if Layer.HOURLY in targets:
            plan.hourly = _hour_range(
                start_date, start_hour_eff, end_date, end_hour_eff
            )
        if Layer.DAILY_ADDITIVE in targets or Layer.DAILY_DISTINCT in targets:
            plan.daily = _days_between(start_date, end_date)
        if Layer.MONTHLY in targets:
            months = _months_between(start_date, end_date)
            if pipeline_mode:
                plan.monthly, plan.skipped_months = self._split_complete_months(
                    months, plan.daily
                )
            else:
                plan.monthly = months
        return plan

    def _split_complete_months(
        self, months: List[MonthPartition], planned_days: List[DayPartition]
    ) -> Tuple[List[MonthPartition], List[Tuple[MonthPartition, int]]]:
        post_run_days = self.daily_wm.completed_keys() | {d.key for d in planned_days}
        complete: List[MonthPartition] = []
        skipped: List[Tuple[MonthPartition, int]] = []
        for month in months:
            missing = [d for d in month.days if d.key not in post_run_days]
            if missing:
                skipped.append((month, len(missing)))
            else:
                complete.append(month)
        return complete, skipped
