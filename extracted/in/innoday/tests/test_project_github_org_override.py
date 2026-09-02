"""Per-project GitHub org resolution (`settings['github_orgs']`).

The InnoDay org that *owns* a project and the GitHub org that *hosts* its repos
are independent. Before this, `settings.github_org` was a single org-wide scalar,
so one InnoDay org could not own two projects whose repos live in different GitHub
accounts -- which is exactly the `bp` case: BPCL's repos are under
`BrightPowerSoftware`, BPAI's under `havilandsoftware`.

The regression these tests exist to catch is not "the override works" but **the
other project still resolving correctly once an override exists**. Pointing the
org-wide value at the incoming project's GitHub org is the tempting one-line
"fix", and it silently breaks every project already in that org: discovery
searches the wrong account and returns nothing rather than erroring.
"""

from src.domain.organization import Organization
from src.domain.project import Project
from src.services.workspace_onboard import WorkspaceOnboardService


def _org(alias: str, settings: dict | None = None) -> Organization:
    return Organization(id=f"org-{alias}", name=alias, alias=alias, settings=settings)


def _project(alias: str) -> Project:
    return Project(
        id=f"proj-{alias}",
        organization_id="org-x",
        alias=alias,
        name=alias,
        description="d",
    )


def _svc() -> WorkspaceOnboardService:
    return WorkspaceOnboardService.__new__(WorkspaceOnboardService)


class TestPerProjectOverride:
    def test_override_wins_over_org_wide(self):
        org = _org(
            "bp",
            {
                "github_org": "BrightPowerSoftware",
                "github_orgs": {"BPAI": "havilandsoftware"},
            },
        )
        assert _svc().github_org(org, _project("BPAI")) == "havilandsoftware"

    def test_sibling_project_still_resolves_org_wide(self):
        """The regression that matters: BPCL must not follow BPAI's override."""
        org = _org(
            "bp",
            {
                "github_org": "BrightPowerSoftware",
                "github_orgs": {"BPAI": "havilandsoftware"},
            },
        )
        assert _svc().github_org(org, _project("BPCL")) == "BrightPowerSoftware"

    def test_no_project_falls_back_to_org_wide(self):
        org = _org("bp", {"github_org": "BrightPowerSoftware"})
        assert _svc().github_org(org, None) == "BrightPowerSoftware"

    def test_absent_override_map_is_harmless(self):
        org = _org("hs", {"github_org": "havilandsoftware"})
        assert _svc().github_org(org, _project("PF")) == "havilandsoftware"

    def test_override_key_casing_tolerated(self):
        """Aliases are stored UPPERCASE; a hand-edited lowercase key is a typo,
        not a different project."""
        org = _org(
            "bp",
            {
                "github_org": "BrightPowerSoftware",
                "github_orgs": {"bpai": "havilandsoftware"},
            },
        )
        assert _svc().github_org(org, _project("BPAI")) == "havilandsoftware"

    def test_blank_override_does_not_shadow_org_wide(self):
        """An emptied-out settings entry must not resolve to "" and send
        discovery at nothing."""
        org = _org(
            "bp", {"github_org": "BrightPowerSoftware", "github_orgs": {"BPAI": "   "}}
        )
        assert _svc().github_org(org, _project("BPAI")) == "BrightPowerSoftware"

    def test_non_string_override_ignored(self):
        org = _org(
            "bp", {"github_org": "BrightPowerSoftware", "github_orgs": {"BPAI": None}}
        )
        assert _svc().github_org(org, _project("BPAI")) == "BrightPowerSoftware"


class TestTopicsUnaffected:
    """`github_topics` was refactored onto the shared `_project_setting` helper;
    its extend-not-replace behaviour must be unchanged."""

    def test_alias_always_included_and_extras_appended(self):
        org = _org("hs", {"github_topics": {"BPAI": "bp-ai,brightpower"}})
        assert _svc().github_topics(org, _project("BPAI")) == [
            "bpai",
            "bp-ai",
            "brightpower",
        ]

    def test_alias_only_when_no_override(self):
        org = _org("hs", {})
        assert _svc().github_topics(org, _project("PF")) == ["pf"]

    def test_topic_key_casing_tolerated(self):
        org = _org("hs", {"github_topics": {"pf": "pixelfuel"}})
        assert _svc().github_topics(org, _project("PF")) == ["pf", "pixelfuel"]

    def test_no_project_yields_no_topics(self):
        org = _org("hs", {"github_topics": {"PF": "pixelfuel"}})
        assert _svc().github_topics(org, None) == []


class TestAssociationIsIndependentOfOrgStampAndDiscovery:
    """Three mechanisms that must stay uncoupled.

    A repo belongs to a project via `project_repositories` (which carries no
    `organization_id`). `Repository.organization_id` is a separate InnoDay-org
    stamp, and `settings.github_org(s)`/`github_topics` are discovery inputs.

    An earlier docstring in `scripts/move_project_org.py` claimed repo-to-project
    association "is purely the `github_topics` map" -- describing discovery and
    ignoring the join that is the actual association. These assertions exist so a
    future change cannot quietly re-couple them and make that claim true.
    """

    def test_join_table_has_no_organization_column(self):
        """If this ever gains an org column, the move script must move it too."""
        from src.domain.project import ProjectRepository

        assert "organization_id" not in ProjectRepository.model_fields

    def test_repository_carries_its_own_org_stamp(self):
        """Distinct from the join -- and from the GitHub org that hosts the repo."""
        from src.domain.repository import Repository

        assert "organization_id" in Repository.model_fields
        assert "project_id" not in Repository.model_fields

    def test_discovery_settings_do_not_determine_association(self):
        """Resolution reads only org settings + project alias.

        It never consults `project_repositories`, so changing discovery settings
        cannot detach an already-attached repo.
        """
        org = _org(
            "bp",
            {
                "github_org": "BrightPowerSoftware",
                "github_orgs": {"BPAI": "havilandsoftware"},
                "github_topics": {"BPAI": "bp-ai"},
            },
        )
        svc = _svc()
        assert svc.github_org(org, _project("BPAI")) == "havilandsoftware"
        assert svc.github_topics(org, _project("BPAI")) == ["bpai", "bp-ai"]
