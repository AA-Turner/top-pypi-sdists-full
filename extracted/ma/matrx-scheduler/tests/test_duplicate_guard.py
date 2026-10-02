"""THE DUPLICATE GUARD's predicate, proven against the shape that caused it.

The anchor case is real: "Human Baseline Schedule" existed twice in
``scheduler.sch_task`` (515dcc49-… and da07e6c6-…), created 36 seconds apart,
identical in every field that decides what runs, both enabled, both firing
hourly for five days. Every test below is a shape from that live table, and the
false-positive cases are the ones that table actually contains — notably the two
DISTINCT schedules both titled "Weekly Marketing Recap", which must never be
grouped together.
"""

from __future__ import annotations

import pytest

from matrx_scheduler import duplicate_guard
from matrx_scheduler.duplicate_guard import (
    DuplicateFinding,
    fingerprint_from_rows,
    group_duplicates,
    note_duplicate,
    task_fingerprint,
)

HOURLY = {"type": "cron", "config": {"expression": "0 * * * *"}, "enabled": True}
AGENT = "11111111-1111-4111-8111-111111111111"


def _fp(**overrides):
    base = dict(
        kind="agent",
        queue="default",
        agent_id=AGENT,
        prompt="Summarize the week.",
        variables={},
        triggers=[HOURLY],
    )
    base.update(overrides)
    return task_fingerprint(**base)


# ── The incident ─────────────────────────────────────────────────────────


def test_the_incident_pair_shares_a_fingerprint():
    """The two live rows differed only in id and created_at. Same fingerprint."""
    assert _fp() == _fp()


def test_title_is_not_part_of_identity():
    """Two schedules doing the same work at the same time cost the same whether
    or not someone renamed one of them. The fingerprint takes no title at all —
    this proves the row-level entry point ignores it too."""
    task_a = {"kind": "agent", "queue": "default", "title": "Morning Brief"}
    task_b = {"kind": "agent", "queue": "default", "title": "Daily Summary"}
    agent = {"agent_id": AGENT, "prompt": "Summarize the week.", "variables": {}}
    assert fingerprint_from_rows(task_a, agent, [HOURLY]) == fingerprint_from_rows(
        task_b, agent, [HOURLY]
    )


# ── What must NOT collapse ───────────────────────────────────────────────


@pytest.mark.parametrize(
    "overrides",
    [
        {"agent_id": "22222222-2222-4222-8222-222222222222"},
        {"prompt": "Summarize the month."},
        {"queue": "priority"},
        {"kind": "tool"},
        {"variables": {"depth": "deep"}},
        {"triggers": [{"type": "cron", "config": {"expression": "0 9 * * *"}}]},
        {"triggers": []},
    ],
)
def test_a_real_difference_is_a_different_schedule(overrides):
    """Anything that changes WHAT runs or WHEN makes it a different schedule.
    A guard that collapsed these would block legitimate creates — a worse bug
    than the duplicate it set out to prevent."""
    assert _fp(**overrides) != _fp()


def test_distinct_schedules_sharing_a_title_are_not_duplicates():
    """The live table holds two separate 'Weekly Marketing Recap' schedules.
    A title-based check would have wrongly merged them."""
    rows = [
        {"id": "a", "user_id": "u1", "title": "Weekly Marketing Recap",
         "fingerprint": _fp()},
        {"id": "b", "user_id": "u1", "title": "Weekly Marketing Recap",
         "fingerprint": _fp(prompt="Recap the marketing numbers.")},
    ]
    assert group_duplicates(rows) == []


def test_duplicates_are_never_grouped_across_users():
    """Two customers running the same public agent on the same cron is two
    customers, not a duplicate. Merging across that line is a leak-shaped bug."""
    rows = [
        {"id": "a", "user_id": "u1", "title": "X", "fingerprint": _fp()},
        {"id": "b", "user_id": "u2", "title": "X", "fingerprint": _fp()},
    ]
    assert group_duplicates(rows) == []


# ── Normalization ────────────────────────────────────────────────────────


def test_noise_that_a_double_submit_can_introduce_is_normalized():
    """Whitespace, case, and JSON key order do not change what runs."""
    assert _fp(prompt="  Summarize   the WEEK.  ") == _fp()
    assert _fp(variables={"b": 1, "a": 2}) == _fp(variables={"a": 2, "b": 1})


def test_trigger_order_does_not_matter():
    daily = {"type": "cron", "config": {"expression": "0 9 * * *"}}
    assert _fp(triggers=[HOURLY, daily]) == _fp(triggers=[daily, HOURLY])


def test_a_disabled_trigger_is_not_part_of_identity():
    """A trigger that cannot fire costs nothing, so pausing one of a pair is a
    real resolution — the paused row stops matching its twin."""
    task = {"kind": "agent", "queue": "default"}
    agent = {"agent_id": AGENT, "prompt": "Summarize the week.", "variables": {}}
    live = fingerprint_from_rows(task, agent, [HOURLY])
    paused = fingerprint_from_rows(task, agent, [{**HOURLY, "enabled": False}])
    assert live != paused
    assert paused == fingerprint_from_rows(task, agent, [])


# ── Grouping ─────────────────────────────────────────────────────────────


def test_group_is_ordered_oldest_first_and_counts_the_redundant_ones():
    rows = [
        {"id": "newer", "user_id": "u1", "title": "Human Baseline Schedule",
         "created_at": "2026-08-09T16:04:32", "fingerprint": _fp()},
        {"id": "older", "user_id": "u1", "title": "Human Baseline Schedule",
         "created_at": "2026-08-09T16:03:56", "fingerprint": _fp()},
    ]
    (finding,) = group_duplicates(rows)
    assert finding.task_ids == ("older", "newer")  # the original comes first
    assert finding.redundant_count == 1
    assert "Human Baseline Schedule" in (finding.reason or "")


def test_schedules_that_cannot_fire_are_never_duplicates():
    """A paused or trigger-less schedule bills nothing, so it duplicates nothing.
    Caught by an existing API test: two `ping` tasks with NO trigger at all were
    being grouped, which would have blocked a legitimate second create."""
    rows = [
        {"id": "a", "user_id": "u1", "fingerprint": _fp(), "can_fire": False},
        {"id": "b", "user_id": "u1", "fingerprint": _fp(), "can_fire": False},
    ]
    assert group_duplicates(rows) == []


def test_one_live_schedule_and_one_paused_twin_is_resolved():
    """This is what pausing an extra achieves — the group stops being a finding."""
    rows = [
        {"id": "a", "user_id": "u1", "fingerprint": _fp(), "can_fire": True},
        {"id": "b", "user_id": "u1", "fingerprint": _fp(), "can_fire": False},
    ]
    assert group_duplicates(rows) == []


@pytest.mark.parametrize(
    ("task", "triggers", "expected"),
    [
        ({"enabled": True}, [HOURLY], True),
        ({"enabled": False}, [HOURLY], False),          # task paused
        ({"enabled": True}, [], False),                  # nothing to fire it
        ({"enabled": True}, [{**HOURLY, "enabled": False}], False),  # trigger paused
    ],
)
def test_can_fire_predicate(task, triggers, expected):
    assert duplicate_guard.can_fire(task, triggers) is expected


def test_a_lone_schedule_is_never_a_finding():
    rows = [{"id": "a", "user_id": "u1", "title": "X", "fingerprint": _fp()}]
    assert group_duplicates(rows) == []


def test_rows_without_an_identity_are_skipped_not_grouped():
    """A row missing its user or fingerprint cannot be judged; grouping such
    rows together would invent a duplicate out of missing data."""
    rows = [
        {"id": "a", "user_id": "", "fingerprint": ""},
        {"id": "b", "user_id": "", "fingerprint": ""},
    ]
    assert group_duplicates(rows) == []


# ── The alarm ────────────────────────────────────────────────────────────


def _finding() -> DuplicateFinding:
    return DuplicateFinding(
        fingerprint=_fp(), user_id="u1", task_ids=("older", "newer"), reason="two of them"
    )


@pytest.mark.asyncio
async def test_no_sink_still_screams_and_never_raises(monkeypatch, caplog):
    monkeypatch.setattr(duplicate_guard, "get_optional_ext", lambda _k: None)
    await note_duplicate(_finding())
    assert "no escalation_sink is registered" in caplog.text


@pytest.mark.asyncio
async def test_the_finding_reaches_the_sink(monkeypatch):
    seen: list[DuplicateFinding] = []

    async def sink(finding):
        seen.append(finding)

    monkeypatch.setattr(duplicate_guard, "get_optional_ext", lambda _k: sink)
    await note_duplicate(_finding())
    assert [f.task_ids for f in seen] == [("older", "newer")]


@pytest.mark.asyncio
async def test_a_broken_sink_never_breaks_the_caller(monkeypatch):
    """The alarm is never allowed to become a new way for a create to fail."""

    async def sink(_finding):
        raise RuntimeError("assists table is down")

    monkeypatch.setattr(duplicate_guard, "get_optional_ext", lambda _k: sink)
    await note_duplicate(_finding())  # must not raise
