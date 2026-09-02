"""Paging pull requests, so a busy repository is not silently cut off at 100.

`get_pull_requests` fetches one page. On a quiet repository that is the whole
answer, so the limit was invisible -- and on a busy one the hundred-and-first
pull request simply did not exist, in the report whose entire job is to say what
a release contains. A short list presented as a complete one is worse than an
error.
"""

from __future__ import annotations

import asyncio
from datetime import datetime, timezone

from src.api.github_api import GitHubAPI


def _pr(number, updated_at):
    return {"number": number, "updated_at": updated_at}


class _Recorder:
    """A GitHubAPI whose single-page fetch is replaced by a scripted one."""

    def __init__(self, pages):
        self.api = GitHubAPI(token="t")
        self.pages = pages
        self.requested = []

        async def fake(owner, repo, state="all", since=None, page=1, per_page=100):
            self.requested.append((state, page))
            return list(self.pages.get(page, []))

        self.api.get_pull_requests = fake  # type: ignore[assignment]

    def run(self, **kwargs):
        return asyncio.run(self.api.list_pull_requests("o", "r", **kwargs))


def _full_page(start, updated_at):
    return [_pr(n, updated_at) for n in range(start, start + 100)]


class TestItKeepsGoing:
    def test_a_second_page_is_fetched(self):
        rec = _Recorder(
            {
                1: _full_page(1, "2026-08-20T00:00:00Z"),
                2: [_pr(101, "2026-08-19T00:00:00Z")],
            }
        )
        prs, truncated = rec.run()
        assert [p["number"] for p in prs][-1] == 101
        assert len(prs) == 101
        assert truncated is False

    def test_a_short_page_ends_it(self):
        """Fewer than a full page means GitHub has no more to give."""
        rec = _Recorder({1: [_pr(1, "2026-08-20T00:00:00Z")]})
        prs, truncated = rec.run()
        assert len(prs) == 1
        assert truncated is False
        assert rec.requested == [("all", 1)]

    def test_an_empty_first_page_is_not_an_error(self):
        rec = _Recorder({})
        assert rec.run() == ([], False)


class TestItStopsEarlyWhenItCan:
    def test_paging_stops_once_a_page_ends_older_than_the_window(self):
        """Results are newest-updated first, so the rest cannot be in the window.

        This is what keeps paging cheap on a repository with years of history --
        without it, a thirty-day window would walk every pull request ever
        opened.
        """
        since = datetime(2026, 8, 1, tzinfo=timezone.utc)
        rec = _Recorder(
            {
                1: _full_page(1, "2026-08-20T00:00:00Z"),
                2: _full_page(101, "2026-07-01T00:00:00Z"),
                3: _full_page(201, "2026-06-01T00:00:00Z"),
            }
        )
        prs, truncated = rec.run(since=since)
        assert [pg for _state, pg in rec.requested] == [1, 2]
        assert len(prs) == 100
        assert truncated is False

    def test_entries_older_than_the_window_are_dropped_from_a_mixed_page(self):
        since = datetime(2026, 8, 1, tzinfo=timezone.utc)
        rec = _Recorder(
            {1: [_pr(1, "2026-08-20T00:00:00Z"), _pr(2, "2026-07-01T00:00:00Z")]}
        )
        prs, _ = rec.run(since=since)
        assert [p["number"] for p in prs] == [1]


class TestItAdmitsWhenItGaveUp:
    def test_running_out_of_pages_reports_truncated(self):
        """The caller has to be able to say the list is short.

        Returning the same shape whether or not everything was fetched is how a
        cap becomes invisible, which is the bug this method exists to fix.
        """
        rec = _Recorder(
            {n: _full_page(n * 100, "2026-08-20T00:00:00Z") for n in range(1, 12)}
        )
        prs, truncated = rec.run(max_pages=3)
        assert truncated is True
        assert len(prs) == 300

    def test_finishing_exactly_on_the_cap_is_not_truncation(self):
        """A repository with exactly `max_pages` pages was fully read.

        Guards the off-by-one that would cry truncation on a complete fetch --
        a false alarm on every release teaches people to ignore the real one.
        """
        rec = _Recorder(
            {
                1: _full_page(1, "2026-08-20T00:00:00Z"),
                2: [_pr(101, "2026-08-19T00:00:00Z")],
            }
        )
        prs, truncated = rec.run(max_pages=2)
        assert truncated is False
        assert len(prs) == 101


class TestTheStateIsPassedThrough:
    def test_open_and_closed_are_asked_for_separately(self):
        """The service asks twice with two different windows; this is that seam."""
        rec = _Recorder({1: [_pr(1, "2026-08-20T00:00:00Z")]})
        rec.run(state="closed")
        rec.run(state="open")
        assert [state for state, _page in rec.requested] == ["closed", "open"]
