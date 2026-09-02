"""Assembling a release here, so cutting one needs no credential out there.

The engine used to find the release itself, from wherever it was running — about
thirty-five GitHub calls across a seven-repository project — so whoever ran it
had to supply a GitHub token. The nearest one to hand is a *personal* login,
which is the wrong credential for a release and carries whatever scopes that
account happens to have. Someone did exactly that, and it also buried the real
gap: the credential a release should use was already stored here.
"""

from __future__ import annotations

import asyncio
import contextlib
from datetime import datetime, timedelta, timezone

import pytest

from src.services.release_content import NoGitHubCredential, ReleaseContentService

NOW = datetime(2026, 8, 21, tzinfo=timezone.utc)
SINCE = NOW - timedelta(days=30)


class _Repo:
    def __init__(self, name, full_name=None, archived=False, deleted=False):
        self.name = name
        self.full_name = full_name or f"an-org/{name}"
        self.archived = archived
        self.deleted = deleted
        self.id = name


def _pr(
    number,
    title,
    *,
    merged_at=None,
    state="open",
    author="someone",
    branch=None,
):
    """A pull request shaped the way GitHub actually sends one.

    `head.ref` and `html_url` are on every real payload, and the branch is the
    only field that ties a pull request to a ticket -- so a fixture that omitted
    them would let the service drop them again without a test noticing.
    """
    return {
        "number": number,
        "title": title,
        "merged_at": merged_at,
        "state": state,
        "user": {"login": author},
        "head": {"ref": branch or f"branch-{number}"},
        "html_url": f"https://github.com/an-org/web/pull/{number}",
    }


class _Api:
    """Stands in for GitHubAPI, splitting by `state` the way GitHub does.

    The split matters: the service asks for closed and open pull requests in two
    separate calls with two different windows, and a fake that returned
    everything to both would let a bug that mixes the buckets pass.
    """

    def __init__(self, prs=None, commits=0, explode=False, truncated=False):
        self.since = None
        self.commits_until = None
        self._prs = prs or []
        self._commits = commits
        self._explode = explode
        self._truncated = truncated

    async def list_pull_requests(
        self, owner, name, state="all", since=None, max_pages=10
    ):
        self.since = since
        if self._explode:
            raise RuntimeError("github is down")
        if state == "open":
            selected = [pr for pr in self._prs if pr.get("state") == "open"]
        elif state == "closed":
            selected = [pr for pr in self._prs if pr.get("state") != "open"]
        else:
            selected = list(self._prs)
        return selected, self._truncated

    async def count_commits(self, owner, name, since=None, until=None):
        if self._explode:
            raise RuntimeError("github is down")
        # Recorded, not just accepted: the closing boundary has to reach the
        # commit count as well as the pull requests, or the two halves of one
        # report describe different windows.
        self.commits_until = until
        return self._commits


class _NoRows:
    def all(self):
        return []

    def first(self):
        return None

    def one_or_none(self):
        return None


class _NoSession:
    """A session that answers nothing, for the tests that touch no rows.

    These used to pass a bare `object()`. That worked only while a broad
    `except Exception` in the people index swallowed the resulting
    AttributeError -- the same broad except that was hiding a real bug. With it
    narrowed to database errors, a stand-in has to actually behave like a
    session, which is the honest arrangement anyway.
    """

    def begin_nested(self):
        return contextlib.nullcontext()

    def exec(self, *_args, **_kwargs):
        return _NoRows()

    def get(self, *_args, **_kwargs):
        return None


def _service(api, repos, design=(), tickets=()):
    """The pull-request half of the service, with the database half stubbed.

    These tests are about what comes back from GitHub and how it is bucketed.
    The ticket join needs a real database and is exercised in
    `tests/test_release_ticket_view.py`, against real rows.
    """
    svc = ReleaseContentService(_NoSession(), client_factory=lambda _org: api)
    svc.repositories = lambda _project_id: repos  # type: ignore[assignment]
    svc.design_repositories = lambda _project_id: set(design)  # type: ignore[assignment]
    svc.release_tickets = lambda _p, _v: list(tickets)  # type: ignore[assignment]
    svc.project_tickets = lambda _p: list(tickets)  # type: ignore[assignment]
    return svc


class _Project:
    id = "proj-1"
    alias = "PROJ"


def _assemble(api, repos, since=SINCE, label="since v1.0.0"):
    return asyncio.run(
        _service(api, repos).assemble(
            project=_Project(),
            organization_id="org-1",
            since=since,
            window_label=label,
        )
    )


class TestNoCredentialIsNotAnEmptyRelease:
    """The distinction the whole service turns on."""

    def test_a_missing_credential_raises(self):
        """ "Nothing shipped" and "we cannot see GitHub" must never render as the
        same report. The first is a quiet release; the second is a setup
        problem, and a release built on it would confidently claim an empty
        window."""
        svc = ReleaseContentService(object(), client_factory=lambda _org: None)
        with pytest.raises(NoGitHubCredential):
            asyncio.run(
                svc.assemble(project=_Project(), organization_id="org-1", since=SINCE)
            )

    def test_a_project_with_no_repositories_raises(self):
        """Also not an empty release — there is nothing attached to tag."""
        with pytest.raises(NoGitHubCredential):
            _assemble(_Api(), [])


class TestWhatGoesIn:
    def test_a_merged_pull_request_is_included(self):
        api = _Api(
            prs=[_pr(1, "Shipped", merged_at="2026-08-10T00:00:00Z", state="closed")],
            commits=3,
        )
        content = _assemble(api, [_Repo("web")])
        assert content["included"] == [
            {
                "repo": "web",
                "commit_count": 3,
                "prs": [
                    {
                        "number": 1,
                        "title": "Shipped",
                        "author": "someone",
                        "branch": "branch-1",
                        "url": "https://github.com/an-org/web/pull/1",
                    }
                ],
            }
        ]

    def test_an_open_pull_request_is_outstanding_not_included(self):
        api = _Api(prs=[_pr(2, "Still going")])
        content = _assemble(api, [_Repo("web")])
        assert content["included"] == []
        assert content["outstanding"][0]["prs"][0]["number"] == 2

    def test_an_abandoned_pull_request_is_neither_shipped_nor_outstanding(self):
        """Closed without merging shipped nothing, and counting it would put
        work in a release that never had it."""
        api = _Api(prs=[_pr(3, "Given up on", state="closed")])
        content = _assemble(api, [_Repo("web")])
        assert content["included"] == []
        assert content["outstanding"] == []

    def test_an_abandoned_pull_request_is_still_reported(self):
        """It shipped nothing, but it is not nothing.

        A ticket whose only pull request was abandoned and a ticket nobody wrote
        any code for used to be indistinguishable -- both simply had no pull
        request anywhere in the payload. They need different conversations, so
        the abandoned one is reported rather than dropped on the floor.
        """
        api = _Api(prs=[_pr(3, "Given up on", state="closed")])
        content = _assemble(api, [_Repo("web")])
        assert [e["repo"] for e in content["abandoned"]] == ["web"]
        assert [pr["number"] for pr in content["abandoned"][0]["prs"]] == [3]


class TestTheFieldsThatUsedToBeDropped:
    def test_the_branch_is_kept(self):
        """The branch is the only field on a pull request that names a ticket.

        GitHub sends it on every payload, and it was being thrown away -- which
        is why a release could not tie a pull request to a ticket at all.
        """
        api = _Api(
            prs=[
                _pr(
                    1,
                    "Shipped",
                    merged_at="2026-08-10T00:00:00Z",
                    state="closed",
                    branch="BPAI-402-jurisdiction",
                )
            ]
        )
        content = _assemble(api, [_Repo("web")])
        assert content["included"][0]["prs"][0]["branch"] == "BPAI-402-jurisdiction"

    def test_the_url_is_kept(self):
        """A reference nobody can click is a reference nobody checks."""
        api = _Api(
            prs=[_pr(7, "Shipped", merged_at="2026-08-10T00:00:00Z", state="closed")]
        )
        content = _assemble(api, [_Repo("web")])
        assert content["included"][0]["prs"][0]["url"].endswith("/pull/7")

    def test_an_outstanding_pull_request_carries_them_too(self):
        """`render_outstanding` had no author to show because nothing sent one."""
        api = _Api(prs=[_pr(9, "Still going", state="open", branch="PF-1-wip")])
        pr = _assemble(api, [_Repo("web")])["outstanding"][0]["prs"][0]
        assert pr["author"] == "someone"
        assert pr["branch"] == "PF-1-wip"


class TestTruncationIsNotSilence:
    def test_a_truncated_repository_is_named(self):
        """A short list presented as a complete one is the worst failure here.

        The report's whole job is to say what a release contains. Naming the
        repository rather than counting them is deliberate: a number says the
        report is short, a name says where to go and look.
        """
        api = _Api(
            prs=[_pr(1, "Shipped", merged_at="2026-08-10T00:00:00Z", state="closed")],
            truncated=True,
        )
        content = _assemble(api, [_Repo("web")])
        assert content["truncated_repos"] == ["web"]

    def test_a_complete_fetch_says_nothing(self):
        """The key is absent, not present-and-empty -- silence is the normal case."""
        api = _Api(
            prs=[_pr(1, "Shipped", merged_at="2026-08-10T00:00:00Z", state="closed")]
        )
        assert "truncated_repos" not in _assemble(api, [_Repo("web")])

    def test_a_pull_request_merged_before_the_window_is_excluded(self):
        """It belongs to the previous release. Counting it here is the
        double-counting this seam keeps producing."""
        api = _Api(
            prs=[_pr(4, "Last time", merged_at="2026-01-01T00:00:00Z", state="closed")]
        )
        assert _assemble(api, [_Repo("web")])["included"] == []

    def test_an_unbounded_window_takes_every_merge(self):
        api = _Api(
            prs=[_pr(5, "Ancient", merged_at="2020-01-01T00:00:00Z", state="closed")]
        )
        content = _assemble(api, [_Repo("web")], since=None)
        assert content["included"][0]["prs"][0]["number"] == 5


class TestEveryRepositoryIsNamed:
    def test_a_quiet_repository_is_still_in_repos(self):
        """It still gets tagged, so a report that omitted it would understate
        what the release touches."""
        content = _assemble(_Api(), [_Repo("web"), _Repo("api")])
        assert content["repos"] == ["web", "api"]
        assert content["included"] == []


class TestOneRepositoryFailingDoesNotLoseTheRelease:
    def test_it_renders_as_quiet_rather_than_raising(self):
        """Wrong, but visible next to its siblings. An exception here would show
        nothing at all."""
        content = _assemble(_Api(explode=True), [_Repo("web")])
        assert content["repos"] == ["web"]
        assert content["included"] == []
        assert content["commit_count"] == 0


class TestTheShapeMatchesWhatTheEngineConsumes:
    def test_it_is_a_valid_brief_content_block(self):
        """The point of the exercise: this goes straight into a brief, and the
        engine renders it without touching GitHub. If the shape drifts, the
        release silently falls back to needing a token."""
        from blastoff.brief import from_dict

        content = _assemble(
            _Api(
                prs=[
                    _pr(9, "A change", merged_at="2026-08-10T00:00:00Z", state="closed")
                ],
                commits=2,
            ),
            [_Repo("web")],
        )
        brief = from_dict(
            {
                "github_org": "an-org",
                "topics": ["t"],
                "version": "v1.1.0",
                "content": content,
            }
        )
        assert brief.content is not None
        assert brief.content.repos == ["web"]
        assert brief.content.window_label == "since v1.0.0"


class TestTheProxyStopsAskingForAToken:
    """End to end at the seam: assembled content reaches the brief.

    This is the whole point. Without it the engine goes looking for the release
    itself and demands a credential from whoever ran the command.
    """

    @staticmethod
    def _drive(content):
        import json as _json
        from unittest.mock import MagicMock, patch

        from src.cli.commands.release_proxy import ReleaseProxyCommands
        from tests.test_innoday_version_store import TestReleaseProxyCLI

        cli = TestReleaseProxyCLI()
        captured = {}

        def fake_invoke(app_cls, argv, st, stdin=None, confirm=None):
            captured["brief"] = _json.loads(stdin) if stdin else None
            captured["argv"] = argv
            return 0

        async def fake_content(*a, **k):
            return content

        with (
            patch.object(
                ReleaseProxyCommands, "_invoke_blastoff", staticmethod(fake_invoke)
            ),
            patch.object(
                ReleaseProxyCommands, "_fetch_content", staticmethod(fake_content)
            ),
        ):
            asyncio.run(
                ReleaseProxyCommands._drive_release(
                    cli._args(),
                    cli._store(),
                    "pf",
                    "havilandsoftware",
                    ["pf"],
                    MagicMock(),
                    "org-1",
                    "proj-1",
                )
            )
        return captured

    def test_assembled_content_reaches_the_brief(self):
        content = {
            "window_label": "since v1.0.0",
            "commit_count": 3,
            "repos": ["web"],
            "included": [],
            "outstanding": [],
        }
        brief = self._drive(content)["brief"]
        assert brief["content"] == content

    def test_no_content_leaves_the_brief_as_it_was(self):
        """The fallback has to stay intact: an org with no GitHub connection
        still gets a release, it just needs a token for it."""
        brief = self._drive(None)["brief"]
        assert "content" not in brief
        assert brief["github_org"] == "havilandsoftware"


class TestDescriptionsDoNotTravel:
    """`body` is matching input, not report content.

    It is the third place a pull request names its ticket, and it is routinely
    thousands of words of checklist. Emitting it would bury the report it exists
    to inform.
    """

    def test_the_body_is_stripped_from_every_bucket(self):
        api = _Api(
            prs=[
                _pr(1, "Shipped", merged_at="2026-08-10T00:00:00Z", state="closed"),
                _pr(2, "Open", state="open"),
                _pr(3, "Abandoned", state="closed"),
            ]
        )
        content = _assemble(api, [_Repo("web")])
        for bucket in ("included", "outstanding", "abandoned"):
            for entry in content[bucket]:
                for pr in entry["prs"]:
                    assert "body" not in pr, bucket

    def test_it_is_still_used_for_matching(self):
        """Stripping it from the output must not stop it reaching the matcher."""
        from src.services.release_content import _entry

        assert "body" in _entry({"number": 1, "body": "Closes BPAI-414"})
