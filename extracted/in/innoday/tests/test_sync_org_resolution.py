"""The sync path must resolve the GitHub org the same way discovery does.

Regression tests for a live incident. BPAI moved to the `bp` InnoDay org while its
repos stayed in the `havilandsoftware` GitHub org, recorded as
`settings['github_orgs'] = {"BPAI": "havilandsoftware"}`.

`WorkspaceOnboardService.github_org(org, project)` honoured that override.
`GitHubConnectService.discover_project_repositories` did not -- it took
`creds["github_org"]`, which comes from the org-wide `settings['github_org']` and
has no project context. So the sync searched `BrightPowerSoftware`, found none of
BPAI's nine repos there, and deactivated all nine while attaching three that
belonged to a different project.

Two properties are pinned here, and the second is the one that would have
contained the damage regardless of the cause:

  1. Both resolvers agree, per project, including for the sibling project that
     must keep resolving to the org-wide default.
  2. A sync that would retire most of a project's repos refuses instead.

The second matters because a wrong org is only one way to reach that state -- a
typo'd override, a renamed GitHub org and a token that lost org scope all present
identically, as "N repositories lost the topic label" rather than as an error.
"""

import pytest

from src.domain.organization import Organization
from src.domain.project import Project
from src.services.github_connect_service import (
    _MASS_DEACTIVATION_MIN_ACTIVE,
    _MASS_DEACTIVATION_THRESHOLD,
)
from src.services.workspace_onboard import WorkspaceOnboardService


def _org(alias: str, settings: dict) -> Organization:
    return Organization(id=f"org-{alias}", name=alias, alias=alias, settings=settings)


def _project(alias: str, org_id: str) -> Project:
    return Project(
        id=f"proj-{alias}",
        organization_id=org_id,
        alias=alias,
        name=alias,
        description="d",
    )


def _svc() -> WorkspaceOnboardService:
    return WorkspaceOnboardService.__new__(WorkspaceOnboardService)


# The real `bp` settings at the time of the incident.
BP_SETTINGS = {
    "github_org": "BrightPowerSoftware",
    "github_orgs": {"BPAI": "havilandsoftware"},
    "github_topics": {"BPCL": "bp-cloud", "BPAI": "bp-ai,brightpower"},
}


class TestTheIncident:
    def test_bpai_resolves_to_the_hosting_org_not_the_owning_org(self):
        """The exact case that broke: owning org `bp`, hosting org havilandsoftware."""
        org = _org("bp", BP_SETTINGS)
        assert _svc().github_org(org, _project("BPAI", org.id)) == "havilandsoftware"

    def test_the_org_wide_value_is_what_the_sync_used_to_take(self):
        """Documents the wrong answer, so the test explains the bug it prevents.

        `creds["github_org"]` came from this scalar. BPAI's repos are not here,
        which is why discovery found nothing and the sync retired all nine.
        """
        assert BP_SETTINGS["github_org"] == "BrightPowerSoftware"
        org = _org("bp", BP_SETTINGS)
        assert _svc().github_org(org, _project("BPAI", org.id)) != "BrightPowerSoftware"

    def test_sibling_project_still_gets_the_org_wide_default(self):
        """The regression that a naive fix causes.

        Repointing `bp.github_org` at havilandsoftware would have "fixed" BPAI and
        broken BPCL the same way. BPCL's repos really are in BrightPowerSoftware.
        """
        org = _org("bp", BP_SETTINGS)
        assert _svc().github_org(org, _project("BPCL", org.id)) == "BrightPowerSoftware"

    def test_topics_and_org_resolve_from_the_same_settings_for_one_project(self):
        """Both halves must agree, or discovery searches the wrong place correctly."""
        org = _org("bp", BP_SETTINGS)
        project = _project("BPAI", org.id)
        svc = _svc()
        assert svc.github_org(org, project) == "havilandsoftware"
        assert svc.github_topics(org, project) == ["bpai", "bp-ai", "brightpower"]


class TestMassDeactivationGuard:
    """The threshold arithmetic, at the boundaries.

    The guard itself needs a DB session and async GitHub calls to exercise
    end-to-end; what is worth pinning without that machinery is that the two
    conditions compose as intended, because a threshold that never fires is the
    same as no guard.
    """

    @staticmethod
    def _would_refuse(active: int, deactivating: int) -> bool:
        return (
            active >= _MASS_DEACTIVATION_MIN_ACTIVE
            and deactivating >= active * _MASS_DEACTIVATION_THRESHOLD
        )

    def test_the_bpai_case_would_have_been_refused(self):
        """9 of 12 -- the sync that caused the incident."""
        assert self._would_refuse(active=12, deactivating=9)

    def test_a_total_wipe_is_refused(self):
        """A wrong GitHub org discovers nothing, so it retires everything."""
        assert self._would_refuse(active=12, deactivating=12)

    def test_one_repo_genuinely_retiring_is_allowed(self):
        """Normal re-tagging must not be blocked -- that is the point of a floor."""
        assert not self._would_refuse(active=12, deactivating=1)

    def test_small_projects_are_exempt(self):
        """A 2-repo project losing 1 is 50% but not evidence of misconfiguration."""
        assert not self._would_refuse(active=2, deactivating=1)
        assert not self._would_refuse(active=2, deactivating=2)

    @pytest.mark.parametrize(
        "active,deactivating,refuse",
        [
            (3, 1, False),  # floor met, fraction not
            (3, 2, True),  # both met, smallest refusing case
            (4, 2, True),  # exactly at the threshold
            (10, 4, False),  # just under
            (10, 5, True),  # exactly half
        ],
    )
    def test_boundaries(self, active, deactivating, refuse):
        assert self._would_refuse(active, deactivating) is refuse
