"""The GitHub half of the summary engine, tested without GitHub (PF-398).

`CodeActivityFetcher.fetch` was stubbed in all 40 engine tests, so the shaping
underneath it -- window bounding, ref extraction from three sources, folding
commits into the PR that owns them, `merged_at` beating `state` -- had no cover
at all. None of it needs a network or a fixture: `_to_activities` is a static
method over plain dicts, and `get_commits`' error handling needs one mocked
response. The "commits are fetched on the default branch only" finding is
exactly the class of bug these reach.
"""

from __future__ import annotations

from datetime import datetime, timedelta, timezone
from typing import Optional
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from src.api.github_api import GITHUB_COMMITS_MAX_PAGES, GitHubAPI, GitHubAPIError
from src.services.code_activity import (
    CodeActivityFetcher,
    extract_ticket_ref,
    ticket_ref_pattern,
)

NOW = datetime(2026, 8, 5, 12, 0, tzinfo=timezone.utc)
SINCE = NOW - timedelta(days=3)
PATTERN = ticket_ref_pattern("PF")


def commit(
    sha: str,
    *,
    when: Optional[datetime] = None,
    subject: str = "some work",
    login: Optional[str] = "ada",
    name: str = "Ada Lovelace",
) -> dict:
    """A commit in the shape GitHub's `/repos/{o}/{r}/commits` returns."""
    return {
        "sha": sha,
        "commit": {
            "message": subject,
            "author": {
                "date": (when or NOW - timedelta(hours=1)).isoformat(),
                "name": name,
            },
        },
        "author": ({"login": login} if login else None),
    }


def pull(
    number: int,
    *,
    branch: str = "PF-1-thing",
    title: str = "Do the thing",
    state: str = "open",
    merged_at: Optional[str] = None,
    updated: Optional[datetime] = None,
    login: str = "ada",
) -> dict:
    return {
        "number": number,
        "head": {"ref": branch},
        "title": title,
        "state": state,
        "merged_at": merged_at,
        "html_url": f"https://github.com/x/y/pull/{number}",
        "user": {"login": login},
        "updated_at": (updated or NOW - timedelta(hours=2)).isoformat(),
    }


def shape(prs, commits, pattern=PATTERN, since=SINCE, until=NOW):
    return CodeActivityFetcher._to_activities(
        "innoday", prs, commits, pattern, since, until
    )


class TestRefExtraction:
    def test_a_ref_is_read_from_branch_title_or_commit_subject(self):
        assert extract_ticket_ref("pf-398-summary-engine", PATTERN) == "PF-398"
        assert extract_ticket_ref("Fix the gate (PF-398)", PATTERN) == "PF-398"
        assert extract_ticket_ref("PF_398 tidy up", PATTERN) == "PF-398"
        assert extract_ticket_ref("no reference here", PATTERN) is None

    def test_another_projects_ref_is_not_this_projects_work(self):
        assert extract_ticket_ref("HS-412-add-thing", PATTERN) is None

    def test_two_aliases_are_matched_because_a_ticket_has_two_names(self):
        """The board key is prefixed by the *project* alias; the display number
        `{org alias}-{n}` by the **organisation's**. The two aliases differ, so
        both have to be matched -- a ticket genuinely has two names.

        The org alias stays the display prefix even though the number itself is
        now unique per `(project_id, project_ref_number)`: the prefix is how
        people refer to tickets out loud, and re-prefixing them would renumber
        every existing reference."""
        pattern = ticket_ref_pattern("PF", "hs")
        assert extract_ticket_ref("PF-398-engine", pattern) == "PF-398"
        assert extract_ticket_ref("hs-42-fix", pattern) == "HS-42"

    def test_an_empty_alias_matches_nothing_rather_than_everything(self):
        """An empty alternation `\\b()[-_ ]?(\\d+)\\b` matches every bare number."""
        pattern = ticket_ref_pattern("", None)
        assert extract_ticket_ref("branch-123", pattern) is None
        assert extract_ticket_ref("42", pattern) is None


class TestWindowBounding:
    def test_a_commit_before_the_window_is_dropped(self):
        activities = shape([], [commit("old", when=SINCE - timedelta(days=1))])
        assert activities == []

    def test_a_commit_after_the_window_is_dropped(self):
        activities = shape([], [commit("future", when=NOW + timedelta(hours=1))])
        assert activities == []

    def test_a_commit_inside_the_window_is_kept(self):
        activities = shape([], [commit("abc", when=NOW - timedelta(hours=5))])
        assert [a.commit_shas for a in activities] == [("abc",)]

    def test_a_pr_outside_the_window_is_dropped(self):
        activities = shape([pull(1, updated=SINCE - timedelta(days=2))], [])
        assert activities == []

    def test_an_undated_commit_is_kept_rather_than_guessed_away(self):
        """No date means GitHub told us nothing, not that it fell outside."""
        raw = commit("undated")
        raw["commit"]["author"]["date"] = None
        assert [a.commit_shas for a in shape([], [raw])] == [("undated",)]

    def test_a_commit_with_no_sha_is_skipped(self):
        assert shape([], [{"sha": "", "commit": {}}]) == []


class TestFoldingCommitsIntoPRs:
    def test_a_pr_and_its_commits_are_one_row_not_six(self):
        prs = [pull(7, branch="PF-1-thing")]
        commits = [
            commit(f"sha{n}", subject=f"PF-1 step {n}", when=NOW - timedelta(hours=n))
            for n in range(1, 6)
        ]

        activities = shape(prs, commits)

        assert len(activities) == 1
        row = activities[0]
        assert row.ticket_ref == "PF-1"
        assert row.pr_url == "https://github.com/x/y/pull/7"
        assert sorted(row.commit_shas) == ["sha1", "sha2", "sha3", "sha4", "sha5"]

    def test_a_ref_no_pr_claimed_still_stands_on_its_own(self):
        """Merged straight to the default branch is still work."""
        activities = shape(
            [], [commit("direct", subject="PF-2 hotfix", when=NOW - timedelta(hours=1))]
        )
        assert len(activities) == 1
        assert activities[0].ticket_ref == "PF-2"
        assert activities[0].pr_url is None

    def test_a_commit_with_no_ref_is_loose_not_lost(self):
        activities = shape([], [commit("loose", subject="tidy imports")])
        assert len(activities) == 1
        assert activities[0].ticket_ref is None
        assert activities[0].commit_shas == ("loose",)

    def test_the_ref_comes_from_the_title_when_the_branch_has_none(self):
        activities = shape([pull(3, branch="tidy-up", title="Fix PF-9 at last")], [])
        assert [a.ticket_ref for a in activities] == ["PF-9"]

    def test_the_branch_wins_over_the_title(self):
        activities = shape([pull(3, branch="PF-1-x", title="also PF-2")], [])
        assert [a.ticket_ref for a in activities] == ["PF-1"]

    def test_an_open_pr_carries_no_shas_which_is_the_whole_problem(self):
        """`get_commits` is called with no `sha`, so GitHub answers on the
        default branch only -- an unmerged branch's commits are simply absent.
        Pinned here because the fingerprint has to compensate for it."""
        activities = shape([pull(4, branch="PF-3-wip", state="open")], [])
        assert activities[0].commit_shas == ()
        assert activities[0].pr_state == "open"


class TestPRState:
    def test_merged_beats_closed(self):
        """GitHub reports a merged PR as "closed", which reads as abandoned."""
        activities = shape(
            [pull(5, state="closed", merged_at="2026-08-04T10:00:00Z")], []
        )
        assert activities[0].pr_state == "merged"

    def test_a_genuinely_closed_pr_stays_closed(self):
        activities = shape([pull(6, state="closed", merged_at=None)], [])
        assert activities[0].pr_state == "closed"


class TestAuthorship:
    def test_the_github_login_is_preferred_over_the_commit_name(self):
        activities = shape([], [commit("a", login="ada", name="Ada Lovelace")])
        assert activities[0].author_handle == "ada"

    def test_the_commit_name_is_the_fallback_for_an_unlinked_author(self):
        """A commit whose email GitHub cannot match to an account has no login."""
        activities = shape([], [commit("a", login=None, name="Ada Lovelace")])
        assert activities[0].author_handle == "Ada Lovelace"


class TestGetCommitsErrorHandling:
    """404/409 mean "no commits to report", not a fault.

    An empty repo answers 409 and a missing branch 404. A summary must not fail
    because one repo in the project is a stub.
    """

    @staticmethod
    def _client(*responses):
        client = MagicMock()
        client.__aenter__ = AsyncMock(return_value=client)
        client.__aexit__ = AsyncMock(return_value=False)
        client.get = AsyncMock(side_effect=list(responses))
        return client

    @staticmethod
    def _response(status_code, payload=None, text=""):
        response = MagicMock()
        response.status_code = status_code
        response.json = MagicMock(return_value=payload if payload is not None else [])
        response.text = text
        return response

    @pytest.mark.asyncio
    @pytest.mark.parametrize("status_code", [404, 409])
    async def test_an_empty_or_missing_repo_answers_with_no_commits(self, status_code):
        api = GitHubAPI("tok")
        with patch(
            "src.api.github_api.httpx.AsyncClient",
            return_value=self._client(self._response(status_code)),
        ):
            assert await api.get_commits("o", "r") == []

    @pytest.mark.asyncio
    async def test_any_other_failure_is_raised_not_swallowed(self):
        """A 401 is a broken credential; reporting it as "no commits" would
        make an expired token look like a quiet week."""
        api = GitHubAPI("tok")
        with patch(
            "src.api.github_api.httpx.AsyncClient",
            return_value=self._client(self._response(401, text="Bad credentials")),
        ):
            with pytest.raises(GitHubAPIError) as caught:
                await api.get_commits("o", "r")
        assert caught.value.status_code == 401
        assert caught.value.is_auth_error is True

    @pytest.mark.asyncio
    async def test_a_full_page_is_followed_rather_than_silently_truncated(self):
        """One `per_page=100` request dropped everything past the first page and
        reported the remainder as nothing having happened."""
        api = GitHubAPI("tok")
        page_one = [commit(f"a{n}") for n in range(100)]
        page_two = [commit(f"b{n}") for n in range(7)]
        with patch(
            "src.api.github_api.httpx.AsyncClient",
            return_value=self._client(
                self._response(200, page_one), self._response(200, page_two)
            ),
        ):
            got = await api.get_commits("o", "r")
        assert len(got) == 107

    @pytest.mark.asyncio
    async def test_pagination_stops_at_the_stated_ceiling(self):
        """The bound is explicit and logged, not an accident of `per_page`."""
        api = GitHubAPI("tok")
        pages = [
            self._response(200, [commit(f"p{p}-{n}") for n in range(100)])
            for p in range(GITHUB_COMMITS_MAX_PAGES + 2)
        ]
        with patch(
            "src.api.github_api.httpx.AsyncClient", return_value=self._client(*pages)
        ):
            got = await api.get_commits("o", "r")
        assert len(got) == 100 * GITHUB_COMMITS_MAX_PAGES
