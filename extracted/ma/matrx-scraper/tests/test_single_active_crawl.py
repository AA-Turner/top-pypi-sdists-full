"""One ACTIVE site-wide crawl per site.

`prepare_start` refuses a new full/list crawl while a live one exists
(pre-check → 409 "already active"), and a create-then-re-list election
settles the race two concurrent starts can win against the pre-check. These
tests pin the pure judgment helpers; the endpoint mapping mirrors resume's
409 contract in `crawl_router.py`.
"""

from __future__ import annotations

from datetime import UTC, datetime, timedelta
from types import SimpleNamespace

import pytest

from matrx_scraper.web_crawl.persistence import STALE_SESSION_AFTER
from matrx_scraper.web_crawl.service import (
    _losing_start_conflict,
    _session_blocks_new_crawl,
    _start_race_key,
)

NOW = datetime(2026, 8, 8, 12, 0, 0, tzinfo=UTC)


def _session(
    *,
    mode: str = "full",
    status: str = "queued",
    updated_ago: timedelta = timedelta(seconds=10),
    lease: dict | None = None,
    session_id: str = "s-1",
    created_at: datetime | None = None,
) -> SimpleNamespace:
    return SimpleNamespace(
        id=session_id,
        scope={"mode": mode},
        status=status,
        updated_at=NOW - updated_ago,
        created_at=created_at or (NOW - updated_ago),
        metadata={"run_lease": lease} if lease else {},
    )


# ---------------------------------------------------------------------------
# Which sessions block a new full/list start
# ---------------------------------------------------------------------------


def test_fresh_queued_full_session_blocks() -> None:
    assert _session_blocks_new_crawl(_session(), now=NOW)


def test_fresh_running_leased_session_blocks() -> None:
    session = _session(
        status="running",
        lease={"owner": "tok", "heartbeat_at": (NOW - timedelta(seconds=5)).isoformat()},
    )
    assert _session_blocks_new_crawl(session, now=NOW)


def test_stale_sessions_do_not_block() -> None:
    """A session past STALE_SESSION_AFTER without a heartbeat is a crash the
    reaper owns — it must never block a legitimate new start."""
    stale = STALE_SESSION_AFTER + timedelta(minutes=1)
    assert not _session_blocks_new_crawl(_session(updated_ago=stale), now=NOW)
    dead_run = _session(
        status="running",
        updated_ago=stale,
        lease={"owner": "tok", "heartbeat_at": (NOW - stale).isoformat()},
    )
    assert not _session_blocks_new_crawl(dead_run, now=NOW)


@pytest.mark.parametrize(
    "mode",
    ["homepage", "initialization", "page_fetch", "sitemap_sync", "gsc_sync"],
)
def test_non_site_wide_modes_never_block(mode: str) -> None:
    assert not _session_blocks_new_crawl(_session(mode=mode), now=NOW)


def test_list_mode_blocks_like_full() -> None:
    assert _session_blocks_new_crawl(_session(mode="list"), now=NOW)


def test_queued_with_unreadable_updated_at_fails_closed() -> None:
    session = _session()
    session.updated_at = None
    assert _session_blocks_new_crawl(session, now=NOW)


def test_terminal_statuses_never_block() -> None:
    for status in ("complete", "partial", "failed", "cancelled"):
        assert not _session_blocks_new_crawl(_session(status=status), now=NOW)


# ---------------------------------------------------------------------------
# Race election — exactly one of two mutually visible racers loses
# ---------------------------------------------------------------------------


def test_younger_racer_yields_to_older() -> None:
    older = _session(session_id="a", created_at=NOW - timedelta(seconds=2))
    younger = _session(session_id="b", created_at=NOW - timedelta(seconds=1))
    assert _losing_start_conflict(younger, [older]) is older
    assert _losing_start_conflict(older, [younger]) is None


def test_equal_created_at_breaks_tie_on_id() -> None:
    a = _session(session_id="aaaa", created_at=NOW)
    b = _session(session_id="bbbb", created_at=NOW)
    assert _losing_start_conflict(b, [a]) is a
    assert _losing_start_conflict(a, [b]) is None
    # A total order guarantees exactly one loser.
    assert (_start_race_key(a) < _start_race_key(b)) is True
