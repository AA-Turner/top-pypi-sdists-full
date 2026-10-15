"""A crawl that keeps PROGRESSING is resumed after every worker stop.

Live case, 2026-10-14: Sightglass Coffee's full crawl (session 2d579de4) was
stopped by three releases (`CancelledError: crawler worker stopped before
completion`), resumed three times, captured 236 of 500 pages — and then the
old cap ("resumed 3 times → never again") refused the fourth resume. Releases
land about every 30 minutes; a full crawl runs for hours. The cap now counts
consecutive lives that captured NOTHING new; a hard ceiling bounds total lives.

The frontier side of resume (no lost, no duplicated page after a kill) is
proven by `test_crawl_chaos_resume.py` and `test_resume_carries_the_frontier.py`.
"""

from __future__ import annotations

from types import SimpleNamespace

import pytest

from matrx_scraper.web_crawl.persistence import CrawlPersistenceState, _cumulative_progress, next_stalled_count
from matrx_scraper.web_crawl.service import (
    RESUME_HARD_CAP,
    RESUME_MAX_ATTEMPTS,
    _assert_resume_budget,
    _assert_session_resumable,
    _rebuild_resume_request,
)


def _session(resume: dict | None) -> SimpleNamespace:
    return SimpleNamespace(
        status="failed",
        scope={"mode": "full", "request": {"max_pages": 500}},
        metadata={"resume": resume} if resume is not None else {},
    )


def _claim(resume: dict, pages_done: int) -> dict:
    """What `claim_run_lease(is_resume=True, pages_done=…)` writes into metadata.resume."""
    resume = dict(resume)
    resume["attempts"] = int(resume.get("attempts") or 0) + 1
    resume["stalled"] = next_stalled_count(resume, pages_done)
    resume["progress_mark"] = pages_done
    return resume


def test_the_sightglass_session_is_resumable_again() -> None:
    # Exactly the live row: 3 resumes under the old rule, no progress mark, 236 pages captured.
    session = _session({"attempts": 3, "last_resumed_at": "2026-10-14T10:53:42+00:00"})
    with pytest.raises(ValueError):
        _assert_session_resumable(session)  # the OLD rule refuses it — the bug
    _assert_session_resumable(session, check_attempts=False)
    _assert_resume_budget(session, pages_done=236)  # the new rule continues it


def test_many_deploy_stops_with_progress_never_exhaust_the_cap() -> None:
    resume: dict = {}
    pages = 0
    for _ in range(RESUME_MAX_ATTEMPTS * 4):
        pages += 40  # each life captured more before the next release stopped it
        _assert_resume_budget(_session(resume), pages_done=pages)
        resume = _claim(resume, pages)
        assert resume["stalled"] == 0
    assert resume["attempts"] == RESUME_MAX_ATTEMPTS * 4


def test_lives_that_capture_nothing_still_hit_the_cap() -> None:
    resume = _claim({}, 120)  # one productive life
    for _ in range(RESUME_MAX_ATTEMPTS):
        _assert_resume_budget(_session(resume), pages_done=120)
        resume = _claim(resume, 120)  # died again with nothing new
    assert resume["stalled"] == RESUME_MAX_ATTEMPTS
    with pytest.raises(ValueError, match="without capturing a new page"):
        _assert_resume_budget(_session(resume), pages_done=120)
    # …and progress clears the streak.
    _assert_resume_budget(_session(resume), pages_done=121)


def test_a_session_that_never_captured_anything_keeps_the_old_cap() -> None:
    with pytest.raises(ValueError):
        _assert_resume_budget(_session({"attempts": RESUME_MAX_ATTEMPTS}), pages_done=0)


def test_hard_ceiling_bounds_total_lives() -> None:
    with pytest.raises(ValueError, match="hard cap"):
        _assert_resume_budget(_session({"attempts": RESUME_HARD_CAP, "stalled": 0, "progress_mark": 1}), pages_done=9)


def test_page_budget_shrinks_by_every_life_not_the_last_one() -> None:
    # stats are per life (the last life fetched 158); the durable count is 236.
    request = _rebuild_resume_request({"max_pages": 500}, {"pages_fetched": 236})
    assert request.max_pages == 264


def test_progress_is_cumulative_across_lives() -> None:
    state = CrawlPersistenceState(
        site_id="s", session_id="x", user_id="u", organization_id="o", file_owner_id="u",
        coverage_qualified=True, prior_pages_done=236, page_budget=500,
    )
    assert _cumulative_progress(state, fetched=10, remaining=30) == {"pages_done_total": 246, "pages_total": 276}
    # never above the session's page budget
    assert _cumulative_progress(state, fetched=10, remaining=900)["pages_total"] == 500
