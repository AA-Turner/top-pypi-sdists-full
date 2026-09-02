"""Server half of a repeatable `innoday refresh`.

Covers the two server-side behaviours the CLI now depends on:

* `removed_repos` reports only repos a sync positively recorded as having lost
  the project's GitHub topic — the one sanctioned basis for archiving.
* `POST /onboarding/context` stores a workspace's context, with the generated
  half gated on a template version so an older CLI cannot regress a newer one.

Sync itself is unchanged. An earlier draft added a guard refusing to deactivate
every link when discovery returned nothing, on the theory that an expired token
produces the same empty result as a genuine removal. It does not:
`GitHubAPI.search_organization_repositories` raises `GitHubAPIError` on any
non-200 and `discover_project_repositories` re-raises it, so an empty list means
"GitHub returned zero repos" and nothing else. The guard only broke the real
case of a single-repo project legitimately losing its topic —
`tests/test_github_repo_sync_reconciliation.py` caught it.
"""

from datetime import datetime, timezone
from unittest.mock import AsyncMock, patch
from uuid import uuid4

from sqlmodel import Session

from src.domain.cli_token import CLIToken, generate_cli_token, hash_cli_token
from src.domain.organization import (
    Organization,
    OrganizationMembership,
    OrganizationRole,
)
from src.domain.project import Project, ProjectRepository
from src.domain.repository import Repository
from src.domain.user import User


def _user_with_token(session, **kw):
    user = User(
        id=str(uuid4()),
        email=kw.pop("email", f"{uuid4().hex[:8]}@example.com"),
        full_name="U",
        **kw,
    )
    session.add(user)
    raw = generate_cli_token()
    session.add(CLIToken(user_id=user.id, token_hash=hash_cli_token(raw)))
    session.commit()
    session.refresh(user)
    return user, raw


def _org_and_project(session, alias="acme", palias="prod"):
    org = Organization(id=str(uuid4()), name="Acme", alias=alias)
    session.add(org)
    session.commit()
    proj = Project(
        id=str(uuid4()),
        organization_id=org.id,
        name="Prod",
        alias=palias,
        description="d",
    )
    session.add(proj)
    session.commit()
    session.refresh(proj)
    return org, proj


def _link_repo(session, project, name, *, active=True, removed_at=None):
    repo = Repository(
        id=str(uuid4()),
        name=name,
        full_name=f"acme/{name}",
        url=f"https://github.com/acme/{name}",
        organization_id=project.organization_id,
    )
    session.add(repo)
    session.commit()
    session.add(
        ProjectRepository(
            id=str(uuid4()),
            project_id=project.id,
            repository_id=repo.id,
            is_active=active,
            removed_at=removed_at,
        )
    )
    session.commit()
    return repo


class TestRemovedReposReporting:
    def test_only_inactive_links_are_reported(self, db_engine):
        from src.services.workspace_onboard import WorkspaceOnboardService

        with Session(db_engine) as s:
            _, proj = _org_and_project(s)
            _link_repo(s, proj, "still-here", active=True)
            _link_repo(
                s,
                proj,
                "label-removed",
                active=False,
                removed_at=datetime(2026, 8, 1, tzinfo=timezone.utc),
            )
            names = [r["name"] for r in WorkspaceOnboardService(s).removed_repos(proj)]

        assert names == ["label-removed"]

    def test_removed_at_is_carried_through(self, db_engine):
        """The client shows it; a removal with no date is not evidence of much."""
        from src.services.workspace_onboard import WorkspaceOnboardService

        with Session(db_engine) as s:
            _, proj = _org_and_project(s)
            _link_repo(
                s,
                proj,
                "gone",
                active=False,
                removed_at=datetime(2026, 8, 1, tzinfo=timezone.utc),
            )
            rows = WorkspaceOnboardService(s).removed_repos(proj)

        assert rows[0]["removed_at"].startswith("2026-08-01")

    def test_newest_removal_is_first_and_undated_last(self, db_engine):
        """The docstring said newest-first while the sort ran oldest-first."""
        from src.services.workspace_onboard import WorkspaceOnboardService

        with Session(db_engine) as s:
            _, proj = _org_and_project(s)
            _link_repo(
                s,
                proj,
                "older",
                active=False,
                removed_at=datetime(2026, 1, 1, tzinfo=timezone.utc),
            )
            _link_repo(
                s,
                proj,
                "newer",
                active=False,
                removed_at=datetime(2026, 8, 1, tzinfo=timezone.utc),
            )
            _link_repo(s, proj, "undated", active=False, removed_at=None)
            names = [r["name"] for r in WorkspaceOnboardService(s).removed_repos(proj)]

        assert names == ["newer", "older", "undated"]

    def test_no_project_means_no_removals(self, db_engine):
        from src.services.workspace_onboard import WorkspaceOnboardService

        with Session(db_engine) as s:
            assert WorkspaceOnboardService(s).removed_repos(None) == []


class TestContextPush:
    def _push(self, client, token, **body):
        return client.post(
            "/api/v1/onboarding/context",
            json=body,
            headers={"Authorization": f"Bearer {token}"},
        )

    def test_stores_both_halves(self, client, db_engine):
        with Session(db_engine) as s:
            _, token = _user_with_token(s, is_platform_member=True)
            _, proj = _org_and_project(s)
            pid = proj.id

        r = self._push(
            client,
            token,
            org="acme",
            project="prod",
            project_context="# generated",
            template_version=1,
            additional_context="## Mine\n\nnote",
        )
        assert r.status_code == 200, r.text
        assert r.json()["project_context_written"] is True

        with Session(db_engine) as s:
            p = s.get(Project, pid)
            assert p.project_context == "# generated"
            assert p.project_context_version == 1
            assert p.additional_context == "## Mine\n\nnote"

    def test_older_template_cannot_regress_a_newer_one(self, client, db_engine):
        """The whole reason the version column exists.

        Two people refresh the same project from CLIs of different vintages.
        Whoever ran last must not decide which generation the UI shows.
        """
        with Session(db_engine) as s:
            _, token = _user_with_token(s, is_platform_member=True)
            _, proj = _org_and_project(s)
            pid = proj.id

        self._push(
            client,
            token,
            org="acme",
            project="prod",
            project_context="NEW",
            template_version=5,
        )
        r = self._push(
            client,
            token,
            org="acme",
            project="prod",
            project_context="OLD",
            template_version=2,
        )

        assert r.status_code == 200
        assert r.json()["project_context_written"] is False
        with Session(db_engine) as s:
            p = s.get(Project, pid)
            assert p.project_context == "NEW"
            assert p.project_context_version == 5

    def test_equal_version_does_overwrite(self, client, db_engine):
        """Same template, re-rendered: accepting it keeps a changed repo list fresh."""
        with Session(db_engine) as s:
            _, token = _user_with_token(s, is_platform_member=True)
            _, proj = _org_and_project(s)
            pid = proj.id

        self._push(
            client,
            token,
            org="acme",
            project="prod",
            project_context="FIRST",
            template_version=3,
        )
        r = self._push(
            client,
            token,
            org="acme",
            project="prod",
            project_context="SECOND",
            template_version=3,
        )

        assert r.json()["project_context_written"] is True
        with Session(db_engine) as s:
            assert s.get(Project, pid).project_context == "SECOND"

    def test_omitting_additional_context_leaves_it_alone(self, client, db_engine):
        """None is silence; "" is a deliberate clear. They must differ."""
        with Session(db_engine) as s:
            _, token = _user_with_token(s, is_platform_member=True)
            _, proj = _org_and_project(s)
            pid = proj.id

        self._push(
            client,
            token,
            org="acme",
            project="prod",
            additional_context="## Keep\n\nme",
        )
        self._push(
            client,
            token,
            org="acme",
            project="prod",
            project_context="g",
            template_version=1,
        )

        with Session(db_engine) as s:
            assert s.get(Project, pid).additional_context == "## Keep\n\nme"

    def test_empty_string_clears_it(self, client, db_engine):
        """This is what --replace-context sends after deleting every note."""
        with Session(db_engine) as s:
            _, token = _user_with_token(s, is_platform_member=True)
            _, proj = _org_and_project(s)
            pid = proj.id

        self._push(client, token, org="acme", project="prod", additional_context="x")
        self._push(client, token, org="acme", project="prod", additional_context="")

        with Session(db_engine) as s:
            assert s.get(Project, pid).additional_context == ""

    def test_non_member_is_refused(self, client, db_engine):
        with Session(db_engine) as s:
            _, token = _user_with_token(s, is_platform_member=False)
            _org_and_project(s)

        r = self._push(
            client, token, org="acme", project="prod", additional_context="x"
        )
        assert r.status_code == 403

    def test_member_may_push(self, client, db_engine):
        """A developer reads the project; they must be able to contribute notes."""
        with Session(db_engine) as s:
            user, token = _user_with_token(s, is_platform_member=False)
            org, _ = _org_and_project(s)
            s.add(
                OrganizationMembership(
                    id=str(uuid4()),
                    user_id=user.id,
                    organization_id=org.id,
                    role=OrganizationRole.DEVELOPER,
                    is_active=True,
                )
            )
            s.commit()

        r = self._push(
            client, token, org="acme", project="prod", additional_context="x"
        )
        assert r.status_code == 200, r.text

    def test_unknown_project_is_404(self, client, db_engine):
        with Session(db_engine) as s:
            _, token = _user_with_token(s, is_platform_member=True)
            _org_and_project(s)

        r = self._push(
            client, token, org="acme", project="nope", additional_context="x"
        )
        assert r.status_code == 404


class TestResolveCarriesRefreshState:
    def test_removed_repos_and_context_are_returned(self, client, db_engine):
        with Session(db_engine) as s:
            _, token = _user_with_token(s, is_platform_member=True)
            _, proj = _org_and_project(s)
            proj.additional_context = "## Notes\n\nfrom the server"
            proj.project_context_version = 4
            s.add(proj)
            _link_repo(
                s,
                proj,
                "dropped",
                active=False,
                removed_at=datetime(2026, 8, 1, tzinfo=timezone.utc),
            )
            s.commit()

        with patch(
            "src.services.workspace_onboard.WorkspaceOnboardService.discover_repos",
            new=AsyncMock(return_value=[]),
        ):
            r = client.get(
                "/api/v1/onboarding/resolve",
                params={"org": "acme", "project": "prod"},
                headers={"Authorization": f"Bearer {token}"},
            )

        assert r.status_code == 200, r.text
        data = r.json()
        assert [x["name"] for x in data["removed_repos"]] == ["dropped"]
        assert data["additional_context"] == "## Notes\n\nfrom the server"
        assert data["project_context_version"] == 4

    def test_generated_context_is_never_sent_back(self, client, db_engine):
        """A client writes the template it ships with. Handing it a newer
        generation would leave a file it cannot itself reproduce."""
        with Session(db_engine) as s:
            _, token = _user_with_token(s, is_platform_member=True)
            _, proj = _org_and_project(s)
            proj.project_context = "SERVER GENERATED BODY"
            s.add(proj)
            s.commit()

        with patch(
            "src.services.workspace_onboard.WorkspaceOnboardService.discover_repos",
            new=AsyncMock(return_value=[]),
        ):
            r = client.get(
                "/api/v1/onboarding/resolve",
                params={"org": "acme", "project": "prod"},
                headers={"Authorization": f"Bearer {token}"},
            )

        assert "SERVER GENERATED BODY" not in r.text
