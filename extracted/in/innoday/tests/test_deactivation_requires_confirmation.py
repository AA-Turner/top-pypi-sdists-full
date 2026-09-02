"""A repo is deactivated only when GitHub says its tag is actually gone.

`sync` used to infer it: "this run's topic search did not return the repo".
That is a different statement from "the tag was removed", and the code could not
tell them apart. A wrong `github_orgs` override, a renamed GitHub org or a token
that lost org scope all return **HTTP 200 with zero repos** — so every attached
repo looked retired, and the next `refresh` archived its directory.

The mass-deactivation guard caught the loud version (≥50% of ≥3 repos) but
exempted small projects: S4C has 2 repos, BLASTOFF has 1. Confirming per repo is
correct at any size, which is why the guard's threshold stops being load-bearing.
"""

from unittest.mock import AsyncMock, MagicMock

import pytest

from src.services.github_connect_service import GitHubConnectService


class _Link:
    def __init__(self, repository_id, is_active=True):
        self.repository_id = repository_id
        self.is_active = is_active


class _Repo:
    def __init__(self, full_name, organization_id="org-1", name=None):
        self.full_name = full_name
        self.organization_id = organization_id
        self.name = name or (full_name.split("/")[-1] if full_name else "?")


def _service(repos, topics_by_repo=None, raises=None):
    """A service whose session returns `repos` and whose GitHub client answers
    `topics_by_repo` (or raises)."""
    session = MagicMock()
    session.get.side_effect = lambda model, rid: repos.get(rid)

    svc = GitHubConnectService(session)

    api = MagicMock()
    if raises is not None:
        api.get_repository_topics = AsyncMock(side_effect=raises)
    else:

        async def topics(owner, name):
            return (topics_by_repo or {}).get(f"{owner}/{name}", [])

        api.get_repository_topics = AsyncMock(side_effect=topics)
    svc._client_for_org = lambda org_id: api
    return svc, api


@pytest.mark.asyncio
class TestRetainStillTagged:
    async def test_a_repo_that_lost_the_tag_is_not_retained(self):
        """The case the feature exists for — deactivation must still happen."""
        repos = {"1": _Repo("acme/gone")}
        svc, _ = _service(repos, topics_by_repo={"acme/gone": ["something-else"]})
        retained = await svc._retain_still_tagged([_Link("1")], ["s4c"])
        assert retained == {}

    async def test_a_repo_that_still_carries_the_tag_is_retained(self):
        """The bug: discovery missed a repo that is still tagged."""
        repos = {"1": _Repo("acme/still-tagged")}
        svc, _ = _service(repos, topics_by_repo={"acme/still-tagged": ["s4c", "web"]})
        retained = await svc._retain_still_tagged([_Link("1")], ["s4c"])
        assert list(retained) == ["1"]

    async def test_a_failed_lookup_retains(self):
        """Absence of evidence is not evidence of removal, and the cost is
        asymmetric — a wrongly retired repo also leaves the developer's disk."""
        repos = {"1": _Repo("acme/unreachable")}
        svc, _ = _service(repos, raises=RuntimeError("502"))
        retained = await svc._retain_still_tagged([_Link("1")], ["s4c"])
        assert list(retained) == ["1"]

    async def test_a_repo_with_no_full_name_retains(self):
        repos = {"1": _Repo("")}
        svc, _ = _service(repos)
        retained = await svc._retain_still_tagged([_Link("1")], ["s4c"])
        assert list(retained) == ["1"]

    async def test_matching_is_case_insensitive(self):
        repos = {"1": _Repo("acme/r")}
        svc, _ = _service(repos, topics_by_repo={"acme/r": ["S4C"]})
        retained = await svc._retain_still_tagged([_Link("1")], ["s4c"])
        assert list(retained) == ["1"]

    async def test_any_of_several_topics_counts(self):
        """BPAI carries both `bp-ai` and `brightpower`; either is enough."""
        repos = {"1": _Repo("acme/r")}
        svc, _ = _service(repos, topics_by_repo={"acme/r": ["brightpower"]})
        retained = await svc._retain_still_tagged(
            [_Link("1")], ["bp-ai", "brightpower"]
        )
        assert list(retained) == ["1"]

    async def test_no_candidates_costs_no_calls(self):
        """The normal case. One call per candidate, and candidates are usually
        zero — the check must be free when nothing is at stake."""
        svc, api = _service({})
        assert await svc._retain_still_tagged([], ["s4c"]) == {}
        api.get_repository_topics.assert_not_called()

    async def test_it_checks_every_candidate_not_just_the_first(self):
        repos = {"1": _Repo("acme/a"), "2": _Repo("acme/b")}
        svc, api = _service(repos, topics_by_repo={"acme/a": [], "acme/b": ["s4c"]})
        retained = await svc._retain_still_tagged([_Link("1"), _Link("2")], ["s4c"])
        assert list(retained) == ["2"]
        assert api.get_repository_topics.await_count == 2

    async def test_the_retained_name_is_reportable(self):
        """The refusal names repos, so a person can go and look at them."""
        repos = {"1": _Repo("acme/still-tagged")}
        svc, _ = _service(repos, topics_by_repo={"acme/still-tagged": ["s4c"]})
        retained = await svc._retain_still_tagged([_Link("1")], ["s4c"])
        assert retained["1"] == "acme/still-tagged"


class TestSmallProjectsAreNoLongerExempt:
    """The guard needs ≥3 active repos. S4C has 2, BLASTOFF has 1 — for those a
    wrong-org sync deactivated everything silently."""

    def test_the_guard_thresholds_are_unchanged(self):
        from src.services.github_connect_service import (
            _MASS_DEACTIVATION_MIN_ACTIVE,
            _MASS_DEACTIVATION_THRESHOLD,
        )

        assert _MASS_DEACTIVATION_MIN_ACTIVE == 3
        assert _MASS_DEACTIVATION_THRESHOLD == 0.5

    @pytest.mark.asyncio
    async def test_a_single_repo_project_is_protected_by_confirmation(self):
        """BLASTOFF's shape: 1 repo, below the guard, still tagged."""
        repos = {"1": _Repo("havilandsoftware/innoday-blastoff")}
        svc, _ = _service(
            repos, topics_by_repo={"havilandsoftware/innoday-blastoff": ["blastoff"]}
        )
        retained = await svc._retain_still_tagged([_Link("1")], ["blastoff"])
        assert list(retained) == ["1"]
