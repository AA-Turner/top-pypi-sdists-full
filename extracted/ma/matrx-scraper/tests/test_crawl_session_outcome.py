"""A crawl execution left `running` after its session ended is settled to the session's outcome.

Live 2026-11-01: three crawl sessions ended `partial` (time budget) on 2026-10-28 and were later
deleted; their executions were never settled, so 599 frontier items stayed `pending` forever.
`crawl_session_outcome` is the reader a host reconciliation uses to settle them.
"""

from __future__ import annotations

from datetime import UTC, datetime
from types import SimpleNamespace

import pytest

from matrx_scraper.web_crawl import runtime_queue as rq


def _execution(link_id: str = "s1", link_kind: str = rq.CRAWL_SESSION_LINK_KIND) -> SimpleNamespace:
    return SimpleNamespace(id="e1", link_kind=link_kind, link_id=link_id)


@pytest.fixture
def sessions(monkeypatch: pytest.MonkeyPatch) -> dict:
    rows: dict = {}

    class _Sessions:
        @staticmethod
        async def get_or_none(**kw):
            return rows.get(kw.get("id"))

    import matrx_scraper.db.models_web as models_web

    monkeypatch.setattr(models_web, "CrawlSession", _Sessions)
    return rows


@pytest.mark.asyncio
@pytest.mark.parametrize(
    ("status", "deleted", "expected"),
    [
        ("running", False, None),  # live: the crash-resume sweep owns it
        ("queued", False, None),
        ("running", True, "cancelled"),  # deleted while live: nobody resumes it
        ("partial", True, "completed"),  # the 2026-10-28 shape
        ("partial", False, "completed"),
        ("complete", False, "completed"),
        ("failed", False, "failed"),
        ("cancelled", False, "cancelled"),
    ],
)
async def test_the_session_decides(sessions: dict, status: str, deleted: bool, expected: str | None) -> None:
    sessions["s1"] = SimpleNamespace(status=status, deleted_at=datetime.now(UTC) if deleted else None)
    assert await rq.crawl_session_outcome(_execution()) == expected


@pytest.mark.asyncio
async def test_a_missing_session_cancels_and_a_foreign_link_is_left_alone(sessions: dict) -> None:
    assert await rq.crawl_session_outcome(_execution(link_id="gone")) == "cancelled"
    assert await rq.crawl_session_outcome(_execution(link_kind="something_else")) is None
