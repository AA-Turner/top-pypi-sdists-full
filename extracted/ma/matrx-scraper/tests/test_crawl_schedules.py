"""Recurring canonical crawls — cadence, claim exclusion, and the three outcomes.

The load-bearing test here is `test_two_concurrent_dispatchers_cannot_both_claim`:
a recurring crawl that two app servers both start is not a cosmetic bug, it is
two full site crawls billed and written at once. Exclusion is proved twice, at
two independent layers:

1. **The statement is atomic** — the dispatcher's claim renders as ONE
   `UPDATE ... WHERE id IN (SELECT ... FOR UPDATE SKIP LOCKED)` gated on
   `claim_token IS NULL`. Rendered through the REAL `matrx_orm.claim_batch`
   against a capturing connection, so a refactor that degrades it to
   SELECT-then-UPDATE fails here.
2. **Our usage of it excludes** — two dispatchers race against one shared table
   whose claim is atomic, and exactly one of them comes away with the row.
"""

from __future__ import annotations

import asyncio
from datetime import UTC, datetime, timedelta
from types import SimpleNamespace
from typing import Any
from uuid import UUID, uuid4

import pytest

from matrx_orm.operations.queue_claim import claim_batch as orm_claim_batch
from matrx_scraper.db.models_web import CrawlSchedule as WebCrawlSchedule
from matrx_scraper.web_crawl import schedules as sched
from matrx_scraper.web_crawl.schedules import (
    MAX_CONSECUTIVE_FAILURES,
    ClaimedCrawlSchedule,
    CronCadence,
    IntervalCadence,
    claim_due_schedules,
    dispatch_due_crawl_schedules,
    next_occurrence,
    parse_cadence,
    settle_dispatch,
)

NOW = datetime(2026, 8, 9, 12, 0, tzinfo=UTC)
SCHEDULE_ID = UUID("11111111-1111-1111-1111-111111111111")
SITE_ID = UUID("22222222-2222-2222-2222-222222222222")
ORG_ID = UUID("33333333-3333-3333-3333-333333333333")
OWNER_ID = UUID("44444444-4444-4444-4444-444444444444")
PRESET_ID = UUID("55555555-5555-5555-5555-555555555555")


def _claim(**overrides: Any) -> ClaimedCrawlSchedule:
    values: dict[str, Any] = {
        "id": SCHEDULE_ID,
        "site_id": SITE_ID,
        "organization_id": ORG_ID,
        "created_by": OWNER_ID,
        "name": "nightly",
        "preset_id": PRESET_ID,
        "cadence": {"kind": "cron", "expression": "0 3 * * *"},
        "timezone": "UTC",
        "scheduled_for": NOW,
        "consecutive_failures": 0,
        "claim_token": uuid4(),
    }
    values.update(overrides)
    return ClaimedCrawlSchedule.model_validate(values)


# ---------------------------------------------------------------------------
# Cadence
# ---------------------------------------------------------------------------


def test_cron_cadence_fires_in_the_schedules_own_timezone() -> None:
    cadence = parse_cadence({"kind": "cron", "expression": "0 3 * * *"})
    assert isinstance(cadence, CronCadence)
    # 03:00 New York on 2026-08-09 (EDT, UTC-4) is 07:00 UTC — a UTC-only
    # evaluation would answer 03:00 UTC and crawl at 11pm local.
    assert next_occurrence(cadence, after=NOW, timezone="America/New_York") == datetime(
        2026, 8, 10, 7, 0, tzinfo=UTC
    )
    assert next_occurrence(cadence, after=NOW, timezone="UTC") == datetime(
        2026, 8, 10, 3, 0, tzinfo=UTC
    )


def test_interval_cadence_advances_from_the_occurrence_that_fired() -> None:
    cadence = parse_cadence({"kind": "interval", "minutes": 1440})
    assert isinstance(cadence, IntervalCadence)
    assert next_occurrence(cadence, after=NOW) == NOW + timedelta(days=1)


# ---------------------------------------------------------------------------
# The frequency floor
# ---------------------------------------------------------------------------
#
# `MIN_INTERVAL_MINUTES` was enforced on the INTERVAL cadence only, so a cron
# cadence of `*/10 * * * *` was stored and dispatched a full site crawl six
# times an hour — the exact frequency of the 2026-08 runaway-crawl incident.
# These cases are the ones that make an eyeball check impossible: a legal
# expression that HAS a `*/` prefix, an illegal one that has none, and the
# one-minute gap that exists only across midnight.
FLOOR_CASES: list[tuple[str, int]] = [
    ("*/10 * * * *", 10),
    ("*/5 * * * *", 5),
    ("* * * * *", 1),
    ("0,5 * * * *", 5),
    ("0,20,40 * * * *", 20),
    ("0,59 0,23 * * *", 1),
    ("15,45 8-17 * * 1-5", 30),
    ("*/15 * * * *", 15),
    ("0 * * * *", 60),
    ("0 */6 * * *", 360),
    ("0 3 * * *", 1440),
    ("0 3 * * 1", 10080),
    ("0 3 1 * *", 40320),
    ("0 3 1,15 * *", 20160),
    ("0 3 */2 * *", 1440),
    ("0 3 29-31 * *", 1440),
    ("30 2 * * 1,3", 2880),
]


@pytest.mark.parametrize(("expression", "gap"), FLOOR_CASES)
def test_the_minimum_gap_is_computed_not_guessed_from_the_string(expression: str, gap: int) -> None:
    assert sched.minimum_gap_minutes(sched.CronCadence(expression=expression)) == gap


@pytest.mark.parametrize(
    "expression",
    [expression for expression, gap in FLOOR_CASES if gap < sched.MIN_INTERVAL_MINUTES],
)
def test_a_cron_under_the_floor_is_refused_by_the_one_door(expression: str) -> None:
    with pytest.raises(sched.CadenceTooFrequent) as excinfo:
        sched.parse_cadence({"kind": "cron", "expression": expression})
    # The message names the computed frequency: a user who is told "too often"
    # and not "how often" cannot tell what to change.
    assert "minute(s)" in str(excinfo.value)
    assert str(sched.MIN_INTERVAL_MINUTES) in str(excinfo.value)


@pytest.mark.parametrize(
    "expression",
    [expression for expression, gap in FLOOR_CASES if gap >= sched.MIN_INTERVAL_MINUTES],
)
def test_a_legal_cron_still_parses(expression: str) -> None:
    assert sched.parse_cadence({"kind": "cron", "expression": expression}).kind == "cron"


def test_the_floor_refuses_it_never_clamps() -> None:
    """Rounding 10 minutes up to 15 would leave the user believing they had
    configured something they did not — a defect in its own right."""

    with pytest.raises(sched.CadenceTooFrequent):
        sched.parse_cadence({"kind": "cron", "expression": "*/10 * * * *"})


@pytest.mark.parametrize(
    "expression",
    [
        "0 3 * * MON",  # a name we cannot expand
        "0 0 3 * * *",  # six fields: a seconds cron can never satisfy the floor
        "0 3 * *",  # four fields
        "0 3 L * *",
        "0 3 * * 1#2",
        "*/0 * * * *",
        "70 * * * *",
    ],
)
def test_an_unexpandable_expression_fails_closed(expression: str) -> None:
    """A field we cannot expand is a field we cannot bound. It is refused, never
    assumed harmless."""

    with pytest.raises(ValueError):
        sched.parse_cadence({"kind": "cron", "expression": expression})


def test_a_stored_row_under_the_floor_alarms_as_a_frequency_problem() -> None:
    """The alarm sink must be able to tell the runaway-crawl shape apart from a
    merely malformed cadence — they are different severities, and sniffing the
    message string is how that distinction rots."""

    with pytest.raises(sched.CadenceTooFrequent) as fast:
        sched.parse_cadence({"kind": "cron", "expression": "*/10 * * * *"})
    with pytest.raises(ValueError) as broken:
        sched.parse_cadence({"kind": "cron", "expression": "nonsense"})
    assert sched._is_frequency_refusal(fast.value) is True
    assert sched._is_frequency_refusal(broken.value) is False


def test_unusable_cadences_are_loud_not_guessed() -> None:
    with pytest.raises(ValueError, match="unusable crawl cadence"):
        parse_cadence({})
    with pytest.raises(ValueError, match="unusable crawl cadence"):
        parse_cadence({"kind": "interval", "minutes": 1})  # below the floor
    with pytest.raises(ValueError, match="invalid cron expression"):
        next_occurrence(CronCadence(expression="not cron"), after=NOW)
    with pytest.raises(ValueError, match="unknown schedule timezone"):
        next_occurrence(CronCadence(expression="0 3 * * *"), after=NOW, timezone="Mars/Olympus")


# ---------------------------------------------------------------------------
# Layer 1 — the claim statement itself
# ---------------------------------------------------------------------------


class _CaptureConn:
    def __init__(self) -> None:
        self.calls: list[tuple[str, tuple[Any, ...]]] = []

    async def fetch(self, sql: str, *params: Any) -> list[dict[str, Any]]:
        self.calls.append((sql, params))
        return []


@pytest.mark.asyncio
async def test_claim_renders_one_skip_locked_statement(monkeypatch: pytest.MonkeyPatch) -> None:
    """The claim must stay ONE atomic statement. A SELECT-then-UPDATE rewrite
    reintroduces exactly the double-start race this dispatcher exists to make
    impossible."""

    conn = _CaptureConn()
    captured: dict[str, Any] = {}

    class _FakeQuery:
        async def update(self, **updates: Any) -> SimpleNamespace:
            captured["lease_recovery"] = updates
            return SimpleNamespace(rows_affected=0)

    monkeypatch.setattr(WebCrawlSchedule, "filter", classmethod(lambda cls, **kwargs: _FakeQuery()))
    monkeypatch.setattr(
        WebCrawlSchedule,
        "claim_batch",
        classmethod(lambda cls, **kwargs: orm_claim_batch(cls, connection=conn, **kwargs)),
    )

    assert await claim_due_schedules(now=NOW) == []

    # An expired lease is released before claiming — a dispatcher that died
    # holding a claim must not park its occurrence forever.
    assert captured["lease_recovery"] == {"claim_token": None, "claim_expires_at": None}

    sql, _params = conn.calls[0]
    assert "FOR UPDATE SKIP LOCKED" in sql
    assert sql.count("UPDATE web.crawl_schedule") == 1
    # Gated on: unclaimed, enabled, not deleted, actually due, has an owner.
    assert "claim_token IS NULL" in sql
    assert "deleted_at IS NULL" in sql
    assert "schedule.next_run_at <= NOW()" in sql
    assert "schedule.created_by IS NOT NULL" in sql


# ---------------------------------------------------------------------------
# Layer 2 — two dispatchers, one due row
# ---------------------------------------------------------------------------


class _SharedScheduleTable:
    """One `web.crawl_schedule` row behind an atomic claim.

    `claim_batch` is modelled the way Postgres executes it: the read of
    `claim_token IS NULL` and the write of the new token happen in ONE
    indivisible step. Everything else (the `await` before it, the two
    dispatchers interleaving) is free to race.
    """

    def __init__(self) -> None:
        self.row: dict[str, Any] = {
            "id": SCHEDULE_ID,
            "site_id": SITE_ID,
            "organization_id": ORG_ID,
            "created_by": OWNER_ID,
            "name": "nightly",
            "preset_id": PRESET_ID,
            "cadence": {"kind": "interval", "minutes": 1440},
            "timezone": "UTC",
            "next_run_at": NOW - timedelta(minutes=1),
            "consecutive_failures": 0,
            "claim_token": None,
            "claim_expires_at": None,
            "enabled": True,
            "deleted_at": None,
        }

    async def claim_batch(self, **kwargs: Any) -> list[dict[str, Any]]:
        await asyncio.sleep(0)  # maximise the interleaving window
        if self.row["claim_token"] is not None or not self.row["enabled"]:
            return []
        self.row.update(kwargs["set_fields"])
        return [dict(self.row)]

    async def release_expired(self, **updates: Any) -> SimpleNamespace:
        return SimpleNamespace(rows_affected=0)


@pytest.mark.asyncio
async def test_two_concurrent_dispatchers_cannot_both_claim(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    table = _SharedScheduleTable()

    class _FakeQuery:
        async def update(self, **updates: Any) -> SimpleNamespace:
            return await table.release_expired(**updates)

    monkeypatch.setattr(WebCrawlSchedule, "filter", classmethod(lambda cls, **kwargs: _FakeQuery()))
    monkeypatch.setattr(
        WebCrawlSchedule,
        "claim_batch",
        classmethod(lambda cls, **kwargs: table.claim_batch(**kwargs)),
    )

    first, second = await asyncio.gather(
        claim_due_schedules(now=NOW),
        claim_due_schedules(now=NOW),
    )

    winners = [claim for batch in (first, second) for claim in batch]
    assert len(winners) == 1, "the same due schedule was claimed twice"
    assert winners[0].id == SCHEDULE_ID
    # The winner's token is the one now stamped on the row — the loser saw
    # nothing and cannot settle it.
    assert table.row["claim_token"] == winners[0].claim_token


# ---------------------------------------------------------------------------
# Settling — started / skipped / failed are three different things
# ---------------------------------------------------------------------------


def _capture_update(monkeypatch: pytest.MonkeyPatch, rows_affected: int = 1) -> dict[str, Any]:
    captured: dict[str, Any] = {}

    async def _update_where(filters: dict[str, Any], **updates: Any) -> SimpleNamespace:
        captured["filters"] = filters
        captured["updates"] = updates
        return SimpleNamespace(rows_affected=rows_affected)

    monkeypatch.setattr(
        WebCrawlSchedule,
        "update_where",
        classmethod(lambda cls, filters, **updates: _update_where(filters, **updates)),
    )
    return captured


@pytest.mark.asyncio
async def test_started_stamps_the_session_and_clears_the_failure_streak(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    captured = _capture_update(monkeypatch)
    claim = _claim(consecutive_failures=3)

    assert await settle_dispatch(claim, outcome="started", session_id="sess-1", now=NOW)

    # Compare-and-swap on the lease: a reclaimed row is never clobbered.
    assert captured["filters"] == {"id": claim.id, "claim_token": claim.claim_token}
    updates = captured["updates"]
    assert updates["last_session_id"] == "sess-1"
    assert updates["last_run_at"] == NOW
    assert updates["consecutive_failures"] == 0
    assert updates["last_error"] is None
    assert updates["claim_token"] is None
    assert updates["next_run_at"] > NOW


@pytest.mark.asyncio
async def test_skip_is_not_a_failure(monkeypatch: pytest.MonkeyPatch) -> None:
    """A schedule firing into an already-running crawl is the single-active-crawl
    rule working. It must not touch the failure streak, must not stamp a run
    that did not happen, and must still advance."""

    captured = _capture_update(monkeypatch)
    claim = _claim(consecutive_failures=2)

    assert await settle_dispatch(
        claim, outcome="skipped", error="crawl session x is already active", now=NOW
    )

    updates = captured["updates"]
    assert updates["last_outcome"] == "skipped"
    assert "consecutive_failures" not in updates
    assert "last_run_at" not in updates
    assert "last_session_id" not in updates
    assert updates["next_run_at"] > NOW


@pytest.mark.asyncio
async def test_repeated_failure_eventually_disables(monkeypatch: pytest.MonkeyPatch) -> None:
    captured = _capture_update(monkeypatch)

    await settle_dispatch(_claim(consecutive_failures=0), outcome="failed", error="boom", now=NOW)
    assert captured["updates"]["consecutive_failures"] == 1
    assert "enabled" not in captured["updates"]

    await settle_dispatch(
        _claim(consecutive_failures=MAX_CONSECUTIVE_FAILURES - 1),
        outcome="failed",
        error="boom",
        now=NOW,
    )
    assert captured["updates"]["enabled"] is False


@pytest.mark.asyncio
async def test_an_unadvanceable_cadence_disables_instead_of_spinning(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """A schedule we cannot compute a next occurrence for would re-fire on the
    same instant every tick, forever. It stops, and says why on the row."""

    captured = _capture_update(monkeypatch)
    claim = _claim(cadence={"kind": "cron", "expression": "nonsense"})

    await settle_dispatch(claim, outcome="started", session_id="sess-1", now=NOW)

    updates = captured["updates"]
    assert updates["enabled"] is False
    assert updates["next_run_at"] is None
    assert updates["last_outcome"] == "failed"
    # The floor's field-count check reads the expression first now, so a
    # single-token nonsense value is named as such instead of surfacing
    # croniter's wording. Either way the row stops and says why.
    assert "has 1 field(s)" in updates["last_error"]


@pytest.mark.asyncio
async def test_a_stored_under_floor_row_is_disabled_AND_alarmed(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """The end-to-end of layer 2: a `*/10` schedule that predates the database
    trigger must not fire, must stop permanently, and must TELL somebody.

    Stopping it silently would leave the site being spared and nobody knowing a
    row got past the trigger — which is itself the finding.
    """

    from matrx_scraper._ext import _registry

    captured = _capture_update(monkeypatch)
    alarms: list[Any] = []
    monkeypatch.setitem(_registry, "crawl_cadence_refusal_sink", alarms.append)
    claim = _claim(cadence={"kind": "cron", "expression": "*/10 * * * *"})

    await settle_dispatch(claim, outcome="started", session_id="sess-1", now=NOW)

    updates = captured["updates"]
    assert updates["enabled"] is False
    assert updates["next_run_at"] is None
    assert "10 minute(s)" in updates["last_error"]

    assert len(alarms) == 1
    # `under_floor` is what makes this CRITICAL rather than merely broken: it
    # means a row reached the database the floor trigger should have refused.
    assert alarms[0].under_floor is True
    assert alarms[0].schedule_id == str(claim.id)
    assert alarms[0].site_id == str(claim.site_id)
    assert alarms[0].organization_id == str(claim.organization_id)


@pytest.mark.asyncio
async def test_the_alarm_sink_failing_never_keeps_a_bad_schedule_alive(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Observability is best-effort; stopping the crawl is not."""

    from matrx_scraper._ext import _registry

    captured = _capture_update(monkeypatch)

    def _explode(_refusal: Any) -> None:
        raise RuntimeError("ops-triage is down")

    monkeypatch.setitem(_registry, "crawl_cadence_refusal_sink", _explode)
    claim = _claim(cadence={"kind": "cron", "expression": "*/10 * * * *"})

    await settle_dispatch(claim, outcome="started", session_id="sess-1", now=NOW)

    assert captured["updates"]["enabled"] is False


@pytest.mark.asyncio
async def test_a_lost_lease_is_reported_not_clobbered(monkeypatch: pytest.MonkeyPatch) -> None:
    _capture_update(monkeypatch, rows_affected=0)
    assert await settle_dispatch(_claim(), outcome="started", session_id="s", now=NOW) is False


# ---------------------------------------------------------------------------
# The drain
# ---------------------------------------------------------------------------


class _FakeService:
    def __init__(self, outcome: Exception | str) -> None:
        self.outcome = outcome
        self.calls: list[dict[str, Any]] = []

    async def prepare_rescrape(
        self, ctx: Any, site_id: str, *, preset_id: str | None = None, trigger: str = "manual"
    ) -> Any:
        self.calls.append({"site_id": site_id, "preset_id": preset_id, "trigger": trigger})
        if isinstance(self.outcome, Exception):
            raise self.outcome
        return SimpleNamespace(session_id=self.outcome, site_id=site_id)

    async def run_prepared(self, emitter: Any, prepared: Any) -> None:
        return None


async def _drain(
    monkeypatch: pytest.MonkeyPatch, service: _FakeService, claim: ClaimedCrawlSchedule
) -> tuple[Any, list[dict[str, Any]]]:
    settled: list[dict[str, Any]] = []

    async def _settle(c: ClaimedCrawlSchedule, **kwargs: Any) -> bool:
        settled.append(kwargs)
        return True

    monkeypatch.setattr(sched, "seed_missing_next_run_at", lambda **_: _zero())
    monkeypatch.setattr(sched, "claim_due_schedules", lambda **_: _one(claim))
    monkeypatch.setattr(sched, "settle_dispatch", _settle)
    monkeypatch.setattr(sched, "detached_task", lambda coro, name=None: coro.close())
    result = await dispatch_due_crawl_schedules(service=service)  # type: ignore[arg-type]
    return result, settled


async def _zero() -> int:
    return 0


async def _one(claim: ClaimedCrawlSchedule) -> list[ClaimedCrawlSchedule]:
    return [claim]


@pytest.mark.asyncio
async def test_drain_starts_a_scheduled_crawl_through_the_canonical_path(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    service = _FakeService("sess-9")
    result, settled = await _drain(monkeypatch, service, _claim())

    # It runs the SAME derivation a human clicking Rescrape runs, with the
    # schedule's preset — never a second config resolution.
    assert service.calls == [
        {"site_id": str(SITE_ID), "preset_id": str(PRESET_ID), "trigger": "scheduled"}
    ]
    assert result.started == 1 and result.skipped == 0 and result.failed == 0
    assert settled == [{"outcome": "started", "session_id": "sess-9"}]


@pytest.mark.asyncio
async def test_drain_records_an_already_active_site_as_a_skip(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    service = _FakeService(RuntimeError("crawl session abc is already active for this site"))
    result, settled = await _drain(monkeypatch, service, _claim())

    assert result.skipped == 1 and result.failed == 0 and result.started == 0
    assert settled[0]["outcome"] == "skipped"


@pytest.mark.asyncio
async def test_drain_records_a_real_error_as_a_failure(monkeypatch: pytest.MonkeyPatch) -> None:
    service = _FakeService(RuntimeError("canonical S3 file pipeline is unavailable"))
    result, settled = await _drain(monkeypatch, service, _claim())

    assert result.failed == 1 and result.skipped == 0
    assert settled[0]["outcome"] == "failed"
    assert result.errors and "S3" in result.errors[0]
