"""Recurring crawls — the canonical `web.crawl_schedule` dispatcher.

A **schedule** is a site saying "crawl me again, on this cadence". It carries
almost nothing: a `cadence`, a `timezone`, and an optional `preset_id`. It does
NOT carry crawl knobs. What a scheduled crawl RUNS is resolved by exactly the
same function a human clicking "Rescrape" goes through —
`presets.derive_recrawl_config` (named preset → the site's pinned default
preset → the last full/list session's persisted request → `CrawlStartRequest()`
defaults) — so a schedule can never drift into being a second, weaker copy of
the crawl config system.

**Crash-safety is structural, not hopeful** (the durable work-queue standard,
`common-docs/policies/durable-work-queue-standard.md`):

- The DB is the only frontier. `next_run_at` is the queue; nothing about a due
  occurrence lives in process memory.
- Workers claim with `UPDATE ... WHERE id IN (SELECT ... FOR UPDATE SKIP
  LOCKED)` (`Model.claim_batch`) and hold a short **lease**
  (`claim_token` + `claim_expires_at`). Two app servers draining at the same
  instant get disjoint rows; neither blocks the other.
- A dispatcher that dies mid-claim strands nothing: the next drain releases any
  lease whose `claim_expires_at` has passed and the occurrence fires again.
- Delivery is therefore **at-least-once**, and the re-delivery is harmless
  because the crawler itself is the idempotency guard: `prepare_start` refuses
  a second site-wide crawl while one is active (409 "already active"), which
  this dispatcher records as a **skip**, never a failure.

The crawl itself is detached after the schedule row is settled. Losing the
process mid-crawl is the crawler's own recovery problem, already solved — the
session is durable, the frontier is durable, and the boot/interval crash-resume
sweep (`WebCrawlService.resume_crashed_sessions`) continues it.
"""

from __future__ import annotations

import logging
from datetime import UTC, datetime, timedelta
from typing import Annotated, Any, Literal
from uuid import UUID, uuid4
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

from croniter import CroniterBadCronError, croniter
from pydantic import BaseModel, ConfigDict, Field, TypeAdapter, ValidationError

from matrx_connect import system_app_context
from matrx_orm import Compare, F, Is, Now
from matrx_utils import capture_error, detached_task, utcnow

from matrx_scraper.db.models_web import CrawlSchedule as WebCrawlSchedule
from matrx_scraper.web_crawl.service import PreparedCrawl, WebCrawlService, get_web_crawl_service

logger = logging.getLogger(__name__)

# CAPS constants — a code push to change, never env vars.
#
# The lease is short on purpose: it only has to cover "claim → create a crawl
# session → settle the row", which is a handful of queries. Everything after
# that is the crawl session's own durable problem.
CLAIM_LEASE_SECONDS = 300
# One drain handles this many due schedules. The system task runs every few
# minutes, so a backlog drains across ticks rather than stampeding N crawls.
DISPATCH_BATCH_LIMIT = 10
# Rows whose `next_run_at` was never seeded, fixed per drain.
SEED_BATCH_LIMIT = 100
# A schedule that fails this many times in a row is DISABLED — it needs a
# human, not another attempt every tick, forever.
MAX_CONSECUTIVE_FAILURES = 10
# The shortest cadence we will run. A crawl is expensive; anything under this
# is a mistake, not a preference.
MIN_INTERVAL_MINUTES = 15

DISPATCH_FEATURE = "web_crawl_schedule_dispatch"

_CLAIM_COLUMNS = [
    "id",
    "site_id",
    "organization_id",
    "created_by",
    "name",
    "preset_id",
    "cadence",
    "timezone",
    "next_run_at",
    "consecutive_failures",
    "claim_token",
]


# ---------------------------------------------------------------------------
# Cadence — the whole recurrence contract, typed
# ---------------------------------------------------------------------------


class CronCadence(BaseModel):
    """`{"kind": "cron", "expression": "0 3 * * *"}` — evaluated in the
    schedule's own `timezone`, so "3am daily" stays 3am across DST."""

    model_config = ConfigDict(extra="forbid")

    kind: Literal["cron"] = "cron"
    expression: str


class IntervalCadence(BaseModel):
    """`{"kind": "interval", "minutes": 1440}` — a fixed gap after the
    occurrence that just fired (never after "now", so a slow drain does not
    make the schedule drift later and later)."""

    model_config = ConfigDict(extra="forbid")

    kind: Literal["interval"] = "interval"
    minutes: int = Field(ge=MIN_INTERVAL_MINUTES)


# ---------------------------------------------------------------------------
# The frequency floor — COMPUTED, never inferred from the shape of the string
# ---------------------------------------------------------------------------
#
# ``MIN_INTERVAL_MINUTES`` was enforced on ``IntervalCadence`` only, so
# ``{"kind": "cron", "expression": "*/10 * * * *"}`` sailed straight through and
# dispatched a full site crawl six times an hour — the exact frequency of the
# 2026-08 runaway-crawl incident
# (``docs/handoffs/runaway-crawl-loop-and-repeat-guards.md``). A cron field is
# not readable by eye: ``0 */6 * * *`` is legal and ``0,5 * * * *`` is not, and
# no prefix or substring test separates them. So the expression is EXPANDED and
# the smallest gap it can ever produce is computed.
#
# THE SAME ALGORITHM EXISTS THREE TIMES ON PURPOSE, at three layers that fail
# independently (root ``CLAUDE.md`` § "Extinction is layered"):
#
#   1. ``web.crawl_cadence_min_gap_minutes`` + the
#      ``web_crawl_schedule_cadence_floor`` trigger in Postgres — the ONLY layer
#      that binds a row written straight to Supabase by the browser, an agent,
#      or a human at a psql prompt. It refuses the write.
#   2. this module — binds the dispatcher, so a row that predates the trigger is
#      DISABLED loudly (and alarmed, below) instead of firing.
#   3. ``matrx-frontend/features/marketing/crawler/crawl-cadence.ts`` — explains
#      the refusal before the save, so a database error is never the first thing
#      the user hears about it.
#
# Parity between 1 and 2 is a guard, not a hope:
# ``aidream/scripts/check_crawl_cadence_floor_parity.py``.
#
# There is deliberately NO clamp. Silently rounding a 10-minute cron up to 15
# leaves the user believing they configured something they did not — named a
# defect in its own right by
# ``docs/handoffs/crawler-throughput-and-visual-capture.md`` vision point 8.

# Names (``MON``), ``L``, ``W``, ``#``, ``?`` and the 6-field second-granularity
# form are REFUSED rather than guessed at: an expression we cannot expand is an
# expression we cannot bound, and this guard fails closed.
_CRON_FIELD_COUNT = 5
_CRON_FIELD_RANGES: tuple[tuple[int, int], ...] = (
    (0, 59),  # minute
    (0, 23),  # hour
    (1, 31),  # day of month
    (1, 12),  # month
    (0, 7),  # day of week (7 == Sunday == 0)
)
# Every month length a day-of-month cadence can meet. All four matter: February
# is what stops `0 3 1,29 * *` being credited with a 28-day gap it does not have
# in a leap year, and a 31-day month is what exposes `0 3 */2 * *` firing on the
# 31st and then again the next day.
_MONTH_LENGTHS: tuple[int, ...] = (28, 29, 30, 31)
_MINUTES_PER_DAY = 1440


def _expand_cron_field(field: str, low: int, high: int) -> tuple[list[int], bool]:
    """Every value ``field`` can take, plus whether it is the unrestricted ``*``.

    Accepts only the numeric grammar — ``*``, ``*/s``, ``a``, ``a-b``, ``a-b/s``
    and comma lists of those. Raises ``ValueError`` on anything else.
    """

    text = field.strip()
    if not text:
        raise ValueError("empty cron field")
    values: set[int] = set()
    unrestricted = True
    for raw_term in text.split(","):
        term = raw_term.strip()
        step = 1
        if "/" in term:
            base, _, step_text = term.partition("/")
            if not step_text.strip().isdigit() or int(step_text) < 1:
                raise ValueError(f"unsupported cron step {raw_term!r}")
            step = int(step_text)
            term = base.strip()
            unrestricted = False
        if term == "*":
            start, end = low, high
        elif "-" in term:
            unrestricted = False
            start_text, _, end_text = term.partition("-")
            if not start_text.strip().isdigit() or not end_text.strip().isdigit():
                raise ValueError(f"unsupported cron range {raw_term!r}")
            start, end = int(start_text), int(end_text)
        elif term.isdigit():
            unrestricted = False
            start = end = int(term)
        else:
            raise ValueError(f"unsupported cron term {raw_term!r}")
        if start < low or end > high or start > end:
            raise ValueError(f"cron term {raw_term!r} is outside {low}-{high}")
        values.update(range(start, end + 1, step))
    if not values:
        raise ValueError(f"cron field {field!r} matches nothing")
    return sorted(values), unrestricted


def _min_within_gap(values: list[int]) -> int | None:
    """Smallest step between two consecutive values, or None for a single value."""

    return min((b - a for a, b in zip(values, values[1:], strict=False)), default=None)


def _min_day_of_week_gap(values: list[int]) -> int:
    """Closest two firing days, in days, for a restricted day-of-week field."""

    days = sorted({0 if day == 7 else day for day in values})
    within = _min_within_gap(days)
    wrap = 7 - days[-1] + days[0]
    return max(1, min(within, wrap) if within is not None else wrap)


def _min_day_of_month_gap(values: list[int]) -> int:
    """Closest two firing days, in days, for a restricted day-of-month field.

    The wrap is evaluated against EVERY month length, not just the shortest.
    `*/2` fires on the 29th and 31st and then again on the 1st — a one-day gap
    that only exists because some months have 31 days, and that a single-cycle
    wrap silently rounds up to two.
    """

    within = _min_within_gap(values)
    wraps = []
    for length in _MONTH_LENGTHS:
        inside = [value for value in values if value <= length]
        if inside:
            wraps.append(length - inside[-1] + values[0])
    wrap = min(wraps) if wraps else max(_MONTH_LENGTHS)
    return max(1, min(within, wrap) if within is not None else wrap)


def _cron_min_gap_minutes(expression: str) -> int:
    """The shortest interval in minutes between two firings of ``expression``.

    The minute and hour fields give the times a firing day contains; the day
    fields give how close two firing days can be. The smallest gap is either
    between two times on one day or ACROSS the day boundary — ``23:59`` →
    ``00:00`` is one minute, which no per-field check would ever notice.
    """

    fields = expression.split()
    if len(fields) != _CRON_FIELD_COUNT:
        raise ValueError(
            f"cron expression {expression!r} has {len(fields)} field(s); exactly "
            f"{_CRON_FIELD_COUNT} (minute hour day-of-month month day-of-week) are "
            "supported. A seconds field can never satisfy the frequency floor."
        )
    minutes, _ = _expand_cron_field(fields[0], *_CRON_FIELD_RANGES[0])
    hours, _ = _expand_cron_field(fields[1], *_CRON_FIELD_RANGES[1])
    days_of_month, dom_any = _expand_cron_field(fields[2], *_CRON_FIELD_RANGES[2])
    _months, _ = _expand_cron_field(fields[3], *_CRON_FIELD_RANGES[3])
    days_of_week, dow_any = _expand_cron_field(fields[4], *_CRON_FIELD_RANGES[4])

    if dom_any and dow_any:
        day_gap_days = 1
    elif not dom_any and not dow_any:
        # cron ORs a restricted day-of-month with a restricted day-of-week, so
        # the firing days are a union we do not try to resolve — the closest
        # they can be is adjacent, and this guard rounds toward refusing.
        day_gap_days = 1
    elif dow_any:
        day_gap_days = _min_day_of_month_gap(days_of_month)
    else:
        day_gap_days = _min_day_of_week_gap(days_of_week)

    times = sorted({hour * 60 + minute for hour in hours for minute in minutes})
    across_days = day_gap_days * _MINUTES_PER_DAY - times[-1] + times[0]
    within_day = min(
        (b - a for a, b in zip(times, times[1:], strict=False)),
        default=across_days,
    )
    return min(within_day, across_days)


def minimum_gap_minutes(cadence: CronCadence | IntervalCadence) -> int:
    """The shortest gap this cadence can ever produce, in whole minutes."""

    if isinstance(cadence, IntervalCadence):
        return cadence.minutes
    return _cron_min_gap_minutes(cadence.expression)


class CadenceTooFrequent(ValueError):
    """The cadence parsed perfectly and asks for a crawl too often.

    A distinct type, not a string to sniff: this is the runaway-crawl shape
    specifically, and the alarm sink escalates it above a merely malformed
    cadence. Still a `ValueError`, so every existing caller that disables a
    schedule on an unusable cadence keeps working unchanged.
    """

    def __init__(self, message: str, *, gap_minutes: int) -> None:
        super().__init__(message)
        self.gap_minutes = gap_minutes


def _is_frequency_refusal(exc: BaseException) -> bool:
    return isinstance(exc, CadenceTooFrequent)


def assert_cadence_frequency_allowed(cadence: CronCadence | IntervalCadence) -> int:
    """Raise unless ``cadence`` stays at or above the floor; return its gap.

    Refuses; never clamps. The message names the computed gap and the floor,
    because "your schedule was adjusted" is how a user ends up believing the
    system is doing something it is not.
    """

    gap = minimum_gap_minutes(cadence)
    if gap < MIN_INTERVAL_MINUTES:
        raise CadenceTooFrequent(
            f"crawl cadence fires every {gap} minute(s), under the "
            f"{MIN_INTERVAL_MINUTES}-minute floor. A site crawl is expensive, so "
            "this frequency is refused rather than quietly adjusted.",
            gap_minutes=gap,
        )
    return gap


CrawlCadence = Annotated[CronCadence | IntervalCadence, Field(discriminator="kind")]
_CADENCE_ADAPTER: TypeAdapter[CronCadence | IntervalCadence] = TypeAdapter(CrawlCadence)


def parse_cadence(raw: Any) -> CronCadence | IntervalCadence:
    """Parse a stored `cadence` jsonb, floor included.

    Raises `ValueError` naming the problem — an unparseable OR too-frequent
    cadence disables its schedule rather than being guessed at or clamped. This
    is the door every stored row goes through (`seed_missing_next_run_at`,
    `settle_dispatch`), which is what makes a row that predates the database
    trigger refuse to fire instead of quietly crawling every ten minutes.
    """

    try:
        cadence = _CADENCE_ADAPTER.validate_python(raw)
    except ValidationError as exc:
        raise ValueError(f"unusable crawl cadence {raw!r}: {exc.error_count()} problem(s)") from exc
    assert_cadence_frequency_allowed(cadence)
    return cadence


# ---------------------------------------------------------------------------
# The alarm seam — a refusal a human never sees is a refusal that did not happen
# ---------------------------------------------------------------------------


class CadenceRefusal(BaseModel):
    """A `web.crawl_schedule` row disabled because its cadence is unusable.

    Arman's ruling on this class (`docs/handoffs/runaway-crawl-loop-and-repeat-guards.md`)
    is that stopping the crawl is only half of it: "all kinds of alarms should go
    off, and administrators should be notified". An ERROR log is not an alarm —
    nobody watches the firehose. The host registers a sink
    (aidream: `observability/crawl_cadence_sink.py`) that turns this into a
    durable `/ops-triage` record; standalone, the log line is all there is and
    that is honest rather than pretend.
    """

    model_config = ConfigDict(extra="forbid")

    schedule_id: str
    site_id: str | None = None
    organization_id: str | None = None
    name: str | None = None
    cadence: dict[str, Any] | None = None
    timezone: str | None = None
    reason: str
    # True when the cadence parsed fine and was refused for FREQUENCY — the
    # runaway-crawl shape specifically, as opposed to a malformed cadence.
    under_floor: bool = False


def _announce_cadence_refusal(refusal: CadenceRefusal) -> None:
    """Log loudly, then hand the event to the host's alarm sink if one exists.

    Never raises: an observability failure must not stop a schedule being
    disabled, which is the part that actually protects the crawled site.
    """

    logger.error(
        "[crawl-cadence-floor] crawl schedule %s (%s) DISABLED — %s (cadence=%r, site=%s)",
        refusal.schedule_id,
        refusal.name,
        refusal.reason,
        refusal.cadence,
        refusal.site_id,
    )
    try:
        from matrx_scraper._ext import get_ext, has_ext

        if has_ext("crawl_cadence_refusal_sink"):
            get_ext("crawl_cadence_refusal_sink")(refusal)
    except Exception:  # noqa: BLE001 — the alarm is best-effort by contract
        logger.exception(
            "[crawl-cadence-floor] alarm sink failed for schedule %s — the schedule "
            "is still disabled, but nobody has been told.",
            refusal.schedule_id,
        )


def next_occurrence(
    cadence: CronCadence | IntervalCadence,
    *,
    after: datetime,
    timezone: str = "UTC",
) -> datetime:
    """The next UTC instant this cadence fires strictly after `after`."""

    anchor = after if after.tzinfo else after.replace(tzinfo=UTC)
    if isinstance(cadence, IntervalCadence):
        return (anchor + timedelta(minutes=cadence.minutes)).astimezone(UTC)
    try:
        zone = ZoneInfo(timezone or "UTC")
    except (ZoneInfoNotFoundError, ValueError) as exc:
        raise ValueError(f"unknown schedule timezone {timezone!r}") from exc
    try:
        local = croniter(cadence.expression, anchor.astimezone(zone)).get_next(datetime)
    except (CroniterBadCronError, KeyError, TypeError, ValueError) as exc:
        raise ValueError(f"invalid cron expression {cadence.expression!r}: {exc}") from exc
    if local.tzinfo is None:
        local = local.replace(tzinfo=zone)
    return local.astimezone(UTC)


# ---------------------------------------------------------------------------
# Claim + settle
# ---------------------------------------------------------------------------


class ClaimedCrawlSchedule(BaseModel):
    """One due occurrence held by this dispatcher's compare-and-set lease."""

    model_config = ConfigDict(extra="ignore")

    id: UUID
    site_id: UUID
    organization_id: UUID
    created_by: UUID
    name: str
    preset_id: UUID | None = None
    cadence: dict[str, Any]
    timezone: str = "UTC"
    scheduled_for: datetime
    consecutive_failures: int = 0
    claim_token: UUID


class CrawlScheduleDispatchResult(BaseModel):
    """What one drain did. Every schedule lands in exactly one bucket."""

    seeded: int = 0
    claimed: int = 0
    started: int = 0
    skipped: int = 0
    failed: int = 0
    disabled: int = 0
    errors: list[str] = Field(default_factory=list)


async def seed_missing_next_run_at(
    *, limit: int = SEED_BATCH_LIMIT, now: datetime | None = None
) -> int:
    """Give enabled schedules with no `next_run_at` their first occurrence.

    A row inserted without one would sit enabled and silently never fire — the
    exact class of dead-on-arrival failure this whole module replaces. An
    unusable cadence disables the row loudly instead of being retried forever.
    """

    current = now or utcnow()
    rows = await (
        WebCrawlSchedule.filter(enabled=True, next_run_at__isnull=True, deleted_at__isnull=True)
        .limit(limit)
        .all(use_cache=False)
    )
    seeded = 0
    for row in rows:
        try:
            cadence = parse_cadence(row.cadence)
            due = next_occurrence(cadence, after=current, timezone=row.timezone or "UTC")
        except ValueError as exc:
            await WebCrawlSchedule.update_where(
                {"id": row.id},
                enabled=False,
                last_outcome="failed",
                last_error=str(exc)[:2000],
            )
            _announce_cadence_refusal(
                CadenceRefusal(
                    schedule_id=str(row.id),
                    site_id=str(row.site_id) if row.site_id else None,
                    organization_id=(str(row.organization_id) if row.organization_id else None),
                    name=row.name,
                    cadence=row.cadence if isinstance(row.cadence, dict) else None,
                    timezone=row.timezone,
                    reason=str(exc),
                    under_floor=_is_frequency_refusal(exc),
                )
            )
            continue
        result = await WebCrawlSchedule.update_where(
            {"id": row.id, "next_run_at__isnull": True},
            next_run_at=due,
        )
        seeded += int(bool(result.rows_affected))
    return seeded


async def claim_due_schedules(
    *,
    limit: int = DISPATCH_BATCH_LIMIT,
    lease_seconds: int = CLAIM_LEASE_SECONDS,
    now: datetime | None = None,
) -> list[ClaimedCrawlSchedule]:
    """Atomically claim disjoint due rows across any number of dispatchers.

    Expired leases are released FIRST — a dispatcher that died holding a claim
    must not park its occurrence forever — and the claim itself is one
    `FOR UPDATE SKIP LOCKED` statement, so concurrent drains can neither
    double-claim a row nor block on each other.
    """

    current = now or utcnow()
    await WebCrawlSchedule.filter(
        claim_token__isnull=False,
        claim_expires_at__lte=current,
    ).update(claim_token=None, claim_expires_at=None)

    token = uuid4()
    rows = await WebCrawlSchedule.claim_batch(
        set_fields={
            "claim_token": token,
            "claim_expires_at": current + timedelta(seconds=lease_seconds),
        },
        filters={"enabled": True, "claim_token": None, "deleted_at": None},
        order_by="next_run_at",
        limit=limit,
        alias="schedule",
        predicate=(
            Is(F("schedule.next_run_at"), None, negated=True)
            & Compare(F("schedule.next_run_at"), "<=", Now())
            # A schedule with no creator has no identity to crawl as. It cannot
            # be dispatched, so it must not be claimed.
            & Is(F("schedule.created_by"), None, negated=True)
        ),
        returning=_CLAIM_COLUMNS,
    )
    return [ClaimedCrawlSchedule(**{**row, "scheduled_for": row["next_run_at"]}) for row in rows]


async def settle_dispatch(
    claim: ClaimedCrawlSchedule,
    *,
    outcome: Literal["started", "skipped", "failed"],
    session_id: str | None = None,
    error: str | None = None,
    now: datetime | None = None,
) -> bool:
    """Release the lease and advance the schedule to its next occurrence.

    A compare-and-swap on `(id, claim_token)`: if this dispatcher's lease was
    already reclaimed by someone else, the write lands on zero rows and returns
    False rather than clobbering the newer claimant's state.

    The three outcomes are deliberately different:

    - `started` — a crawl session exists. Stamps `last_run_at` /
      `last_session_id` and CLEARS the failure streak.
    - `skipped` — nothing was wrong; the site was already crawling. The failure
      streak is untouched (a skip must never disable a schedule) and
      `last_run_at` is left alone, because nothing ran.
    - `failed` — increments the streak, and disables the schedule once it hits
      `MAX_CONSECUTIVE_FAILURES`.
    """

    current = now or utcnow()
    updates: dict[str, Any] = {
        "claim_token": None,
        "claim_expires_at": None,
        "last_outcome": outcome,
    }
    if outcome == "started":
        updates["last_run_at"] = current
        updates["last_session_id"] = session_id
        updates["last_error"] = None
        updates["consecutive_failures"] = 0
    elif outcome == "skipped":
        updates["last_error"] = (error or "")[:2000] or None
    else:
        failures = claim.consecutive_failures + 1
        updates["last_error"] = (error or "dispatch failed")[:2000]
        updates["consecutive_failures"] = failures
        if failures >= MAX_CONSECUTIVE_FAILURES:
            updates["enabled"] = False
            logger.error(
                "crawl schedule %s (%s) disabled after %s consecutive failures: %s",
                claim.id,
                claim.name,
                failures,
                updates["last_error"],
            )

    try:
        cadence = parse_cadence(claim.cadence)
        updates["next_run_at"] = next_occurrence(
            cadence,
            after=max(current, claim.scheduled_for),
            timezone=claim.timezone,
        )
    except ValueError as exc:
        # A schedule we cannot advance would re-fire on the same instant every
        # tick forever. Stop it, and say why on the row itself.
        _announce_cadence_refusal(
            CadenceRefusal(
                schedule_id=str(claim.id),
                site_id=str(claim.site_id),
                organization_id=str(claim.organization_id),
                name=claim.name,
                cadence=claim.cadence,
                timezone=claim.timezone,
                reason=str(exc),
                under_floor=_is_frequency_refusal(exc),
            )
        )
        updates["enabled"] = False
        updates["next_run_at"] = None
        updates["last_outcome"] = "failed"
        updates["last_error"] = str(exc)[:2000]

    result = await WebCrawlSchedule.update_where(
        {"id": claim.id, "claim_token": claim.claim_token},
        **updates,
    )
    if not result.rows_affected:
        logger.error(
            "crawl schedule %s lost its dispatch lease before settling (%s)",
            claim.id,
            outcome,
        )
        return False
    return True


# ---------------------------------------------------------------------------
# The drain
# ---------------------------------------------------------------------------


async def _run_scheduled_crawl(
    service: WebCrawlService,
    claim: ClaimedCrawlSchedule,
    prepared: PreparedCrawl,
) -> None:
    """Run an already-prepared scheduled crawl in its own context.

    Detached: it starts with EMPTY contextvars, so it establishes its own
    `system_app_context` as the schedule's owner. Failure here is the crawl
    session's own terminal state (`run_prepared` writes it) — the schedule row
    was already settled as `started`, which is true: a session was created.
    """

    session_id = prepared.session_id
    try:
        async with system_app_context(
            DISPATCH_FEATURE,
            user_id=str(claim.created_by),
            organization_id=str(claim.organization_id),
            source_app="matrx-scraper",
            label=f"scheduled-crawl:{session_id[:8]}",
        ) as ctx:
            await service.run_prepared(ctx.emitter, prepared)
    except Exception as exc:  # noqa: BLE001 — a detached run must never take the loop down
        logger.exception("scheduled crawl session %s (schedule %s) failed", session_id, claim.id)
        await capture_error(
            exc,
            kind="scheduled_crawl_failed",
            context={"session_id": session_id, "schedule_id": str(claim.id)},
        )


async def _dispatch_one(
    service: WebCrawlService,
    claim: ClaimedCrawlSchedule,
    result: CrawlScheduleDispatchResult,
) -> None:
    prepared: PreparedCrawl | None = None
    try:
        async with system_app_context(
            DISPATCH_FEATURE,
            user_id=str(claim.created_by),
            organization_id=str(claim.organization_id),
            source_app="matrx-scraper",
            label=f"crawl-schedule:{str(claim.id)[:8]}",
        ) as ctx:
            prepared = await service.prepare_rescrape(
                ctx,
                str(claim.site_id),
                preset_id=str(claim.preset_id) if claim.preset_id else None,
                trigger="scheduled",
            )
    except RuntimeError as exc:
        # The site is already crawling. That is the single-active-crawl rule
        # doing its job, not a fault of this schedule: record it, advance, and
        # do NOT count it against the failure streak.
        if "already active" in str(exc):
            result.skipped += 1
            logger.info(
                "crawl schedule %s (%s) skipped — site %s is already crawling: %s",
                claim.id,
                claim.name,
                claim.site_id,
                exc,
            )
            await settle_dispatch(claim, outcome="skipped", error=str(exc))
            return
        await _settle_failure(claim, exc, result)
        return
    except Exception as exc:  # noqa: BLE001 — one bad schedule cannot strand the batch
        await _settle_failure(claim, exc, result)
        return

    # Settle BEFORE the crawl detaches. The session already exists and is
    # durable, so stamping it now is honest even if this process dies in the
    # next microsecond — and it is what stops the occurrence from firing twice.
    settled = await settle_dispatch(claim, outcome="started", session_id=prepared.session_id)
    result.started += 1
    if not settled:
        result.errors.append(
            f"{claim.id}: crawl session {prepared.session_id} started but the "
            "schedule row could not be stamped (lease lost)"
        )
    detached_task(
        _run_scheduled_crawl(service, claim, prepared),
        name=f"scheduled-crawl-{prepared.session_id[:8]}",
    )


async def _settle_failure(
    claim: ClaimedCrawlSchedule,
    exc: BaseException,
    result: CrawlScheduleDispatchResult,
) -> None:
    sample = f"{claim.id}: {type(exc).__name__}: {exc}"
    result.failed += 1
    result.errors.append(sample[:500])
    logger.exception("crawl schedule dispatch failed for %s (%s)", claim.id, claim.name)
    await capture_error(
        exc,
        kind="crawl_schedule_dispatch_failed",
        context={"schedule_id": str(claim.id), "site_id": str(claim.site_id)},
    )
    if claim.consecutive_failures + 1 >= MAX_CONSECUTIVE_FAILURES:
        result.disabled += 1
    try:
        await settle_dispatch(claim, outcome="failed", error=f"{type(exc).__name__}: {exc}")
    except Exception as settle_exc:  # noqa: BLE001 — preserve the original batch failure
        logger.exception("crawl schedule %s could not be settled after failure", claim.id)
        await capture_error(
            settle_exc,
            kind="crawl_schedule_settlement_failed",
            context={"schedule_id": str(claim.id)},
        )


async def dispatch_due_crawl_schedules(
    *,
    limit: int = DISPATCH_BATCH_LIMIT,
    service: WebCrawlService | None = None,
) -> CrawlScheduleDispatchResult:
    """Claim every due `web.crawl_schedule` and start its canonical crawl.

    The one entry point. The aidream `web_crawl_schedule_dispatch` system task
    is a thin caller of this; there is no second way to fire a recurring crawl.
    """

    crawler = service or get_web_crawl_service()
    result = CrawlScheduleDispatchResult()
    result.seeded = await seed_missing_next_run_at()
    claims = await claim_due_schedules(limit=limit)
    result.claimed = len(claims)
    for claim in claims:
        await _dispatch_one(crawler, claim, result)
    return result


__all__ = [
    "CLAIM_LEASE_SECONDS",
    "ClaimedCrawlSchedule",
    "CrawlCadence",
    "CadenceRefusal",
    "CadenceTooFrequent",
    "CrawlScheduleDispatchResult",
    "CronCadence",
    "DISPATCH_BATCH_LIMIT",
    "IntervalCadence",
    "MAX_CONSECUTIVE_FAILURES",
    "MIN_INTERVAL_MINUTES",
    "assert_cadence_frequency_allowed",
    "claim_due_schedules",
    "dispatch_due_crawl_schedules",
    "minimum_gap_minutes",
    "next_occurrence",
    "parse_cadence",
    "seed_missing_next_run_at",
    "settle_dispatch",
]
