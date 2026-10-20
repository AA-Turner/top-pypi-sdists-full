"""Background crawls get a time budget too, and a site too big for one budget is CONTINUED, not restarted.

The pieces: the rescrape request carries a budget (so a pinned default preset - the no-body path - is bounded),
a scheduled crawl reads its budget from a knob, and a session that stopped at its budget is resumable.
"""

from __future__ import annotations

from datetime import UTC, datetime, timedelta
from types import SimpleNamespace

import pytest
from pydantic import ValidationError

from matrx_scraper.parser.knobs import configure_parser_knobs
from matrx_scraper.web_crawl import schedules as sched
from matrx_scraper.web_crawl.contracts import CrawlStartRequest, RecrawlRequest
from matrx_scraper.web_crawl.service import (
    CONTINUE_TIME_BUDGET_LOOKBACK,
    _assert_session_resumable,
    continuable_after_time_budget,
    stopped_at_time_budget,
    with_time_budget,
)

NOW = datetime(2026, 10, 16, 12, 0, tzinfo=UTC)


def _session(**over: object) -> SimpleNamespace:
    base: dict[str, object] = {
        "status": "partial",
        "stats": {"stop_reason": "time_budget", "remaining_queue_depth": 40},
        "scope": {"mode": "full", "request": {"max_pages": 500}},
        "metadata": {},
        "created_at": NOW - timedelta(hours=3),
    }
    base.update(over)
    return SimpleNamespace(**base)


def test_the_rescrape_request_carries_a_time_budget() -> None:
    assert RecrawlRequest(time_budget_seconds=600).time_budget_seconds == 600
    assert RecrawlRequest().time_budget_seconds is None
    assert RecrawlRequest().continue_time_budget_partial is False
    assert RecrawlRequest(continue_time_budget_partial=True).continue_time_budget_partial is True
    with pytest.raises(ValidationError):
        RecrawlRequest(time_budget_seconds=0)


def test_a_budget_tightens_a_preset_never_loosens_it() -> None:
    # A pinned default preset resolves to a config with no budget: the caller's budget lands on it.
    assert with_time_budget(CrawlStartRequest(), 900).time_budget_seconds == 900
    # A preset that already has a tighter budget keeps it; a looser one is tightened.
    assert with_time_budget(CrawlStartRequest(time_budget_seconds=300), 900).time_budget_seconds == 300
    assert with_time_budget(CrawlStartRequest(time_budget_seconds=3600), 900).time_budget_seconds == 900
    # No budget asked: the config is untouched.
    assert with_time_budget(CrawlStartRequest(), None).time_budget_seconds is None
    assert with_time_budget(CrawlStartRequest(), 0).time_budget_seconds is None


def test_only_a_budget_stop_with_work_left_is_continuable() -> None:
    assert stopped_at_time_budget(_session())
    assert continuable_after_time_budget(_session(), NOW)
    assert not continuable_after_time_budget(_session(stats={"stop_reason": "rate_limited", "remaining_queue_depth": 9}), NOW)
    assert not continuable_after_time_budget(_session(stats={"stop_reason": "time_budget", "remaining_queue_depth": 0}), NOW)
    assert not continuable_after_time_budget(_session(status="complete"), NOW)
    assert not continuable_after_time_budget(_session(scope={"mode": "list"}), NOW)
    assert not continuable_after_time_budget(_session(metadata={"cancel_request": {"requested": True}}), NOW)
    stale = _session(created_at=NOW - CONTINUE_TIME_BUDGET_LOOKBACK - timedelta(minutes=1))
    assert not continuable_after_time_budget(stale, NOW)


def test_the_resume_gate_accepts_a_budget_partial_and_still_refuses_other_finished_runs() -> None:
    assert _assert_session_resumable(_session()) == {"max_pages": 500}
    for status, stats in (
        ("complete", {}),
        ("partial", {"stop_reason": "rate_limited", "remaining_queue_depth": 9}),
        ("partial", {}),
    ):
        with pytest.raises(ValueError, match="already finished"):
            _assert_session_resumable(_session(status=status, stats=stats))


@pytest.mark.asyncio
async def test_a_scheduled_crawl_reads_its_budget_from_the_knob() -> None:
    claim = SimpleNamespace(organization_id="o1", created_by="u1", site_id="s1")
    seen: list[object] = []

    async def scoped(keys: list[str], scope: object) -> dict[str, object]:
        seen.append(scope)
        return {sched.SCHEDULED_TIME_BUDGET_KNOB: 45}

    configure_parser_knobs(lambda key: 999, scoped_reader=scoped)
    try:
        assert await sched.scheduled_time_budget_seconds(claim) == 45 * 60
        assert seen[0].site_id == "s1" and seen[0].organization_id == "o1"

        async def off(keys: list[str], scope: object) -> dict[str, object]:
            return {sched.SCHEDULED_TIME_BUDGET_KNOB: 0}

        configure_parser_knobs(lambda key: 999, scoped_reader=off)
        assert await sched.scheduled_time_budget_seconds(claim) is None  # 0 = no budget
    finally:
        configure_parser_knobs(None)
    # No host bound: the declared mirror, never "no budget".
    assert await sched.scheduled_time_budget_seconds(claim) == sched.SCHEDULED_TIME_BUDGET_MIRROR * 60
