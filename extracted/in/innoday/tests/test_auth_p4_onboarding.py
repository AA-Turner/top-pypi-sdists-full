"""P4 auth: onboarding resolve endpoint, POST /users lockdown, workspace helpers.

The git-clone side of onboarding is not exercised here (it shells out to real
git); we test the resolution endpoint (mocking GitHub discovery), the users
lockdown, and the pure project.yml writer.
"""

import asyncio
from pathlib import Path
from unittest.mock import AsyncMock, MagicMock, patch
from uuid import uuid4

import pytest
import yaml
from sqlmodel import Session

from src.domain.cli_token import CLIToken, generate_cli_token, hash_cli_token
from src.domain.organization import (
    Organization,
    OrganizationMembership,
    OrganizationRole,
)
from src.domain.project import Project
from src.domain.user import User

# db_engine + client fixtures are provided by tests/conftest.py.


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


class TestResolveEndpoint:
    def test_platform_user_resolves_any_org(self, client, db_engine):
        with Session(db_engine) as s:
            _, token = _user_with_token(s, is_platform_member=True)
            org = Organization(id=str(uuid4()), name="Acme", alias="acme")
            s.add(org)
            s.commit()
            proj = Project(
                id=str(uuid4()),
                organization_id=org.id,
                name="Prod",
                alias="prod",
                description="d",
            )
            s.add(proj)
            s.commit()

        with patch(
            "src.services.workspace_onboard.WorkspaceOnboardService.discover_repos",
            new=AsyncMock(
                return_value=[
                    {
                        "name": "repo-a",
                        "clone_url": "https://github.com/acme/repo-a.git",
                        "ssh_url": "git@github.com:acme/repo-a.git",
                        "default_branch": "main",
                    }
                ]
            ),
        ):
            r = client.get(
                "/api/v1/onboarding/resolve",
                params={"org": "acme", "project": "prod"},
                headers={"Authorization": f"Bearer {token}"},
            )
        assert r.status_code == 200, r.text
        data = r.json()
        assert data["org"]["alias"] == "acme"
        assert data["project"]["alias"] == "prod"
        assert data["github_topic"] == "prod"
        assert data["repos"][0]["name"] == "repo-a"

    def test_non_member_cannot_resolve(self, client, db_engine):
        with Session(db_engine) as s:
            _, token = _user_with_token(s, is_platform_member=False)
            org = Organization(id=str(uuid4()), name="Other", alias="other")
            s.add(org)
            s.commit()

        r = client.get(
            "/api/v1/onboarding/resolve",
            params={"org": "other"},
            headers={"Authorization": f"Bearer {token}"},
        )
        assert r.status_code == 403

    def test_member_can_resolve_own_org(self, client, db_engine):
        with Session(db_engine) as s:
            user, token = _user_with_token(s)
            org = Organization(id=str(uuid4()), name="Mine", alias="mine")
            s.add(org)
            s.commit()
            s.add(
                OrganizationMembership(
                    user_id=user.id,
                    organization_id=org.id,
                    role=OrganizationRole.MEMBER,
                    is_active=True,
                )
            )
            s.commit()

        with patch(
            "src.services.workspace_onboard.WorkspaceOnboardService.discover_repos",
            new=AsyncMock(return_value=[]),
        ):
            r = client.get(
                "/api/v1/onboarding/resolve",
                params={"org": "mine"},
                headers={"Authorization": f"Bearer {token}"},
            )
        assert r.status_code == 200

    def test_unknown_org_404(self, client, db_engine):
        with Session(db_engine) as s:
            _, token = _user_with_token(s, is_platform_member=True)
        r = client.get(
            "/api/v1/onboarding/resolve",
            params={"org": "ghost"},
            headers={"Authorization": f"Bearer {token}"},
        )
        assert r.status_code == 404

    def test_aliases_resolve_case_insensitively(self, client, db_engine):
        """Users type `hs/pf` while stored aliases may be `HS`/`PF`; an exact
        match made a correct alias 404 purely on casing."""
        with Session(db_engine) as s:
            _, token = _user_with_token(s, is_platform_member=True)
            org = Organization(id=str(uuid4()), name="Haviland", alias="HS")
            s.add(org)
            s.commit()
            s.add(
                Project(
                    id=str(uuid4()),
                    organization_id=org.id,
                    name="PF",
                    alias="PF",
                    description="d",
                )
            )
            s.commit()

        with patch(
            "src.services.workspace_onboard.WorkspaceOnboardService.discover_repos",
            new=AsyncMock(return_value=[]),
        ):
            r = client.get(
                "/api/v1/onboarding/resolve",
                params={"org": "hs", "project": "pf"},
                headers={"Authorization": f"Bearer {token}"},
            )
        assert r.status_code == 200
        body = r.json()
        assert body["org"]["alias"] == "HS"
        assert body["project"]["alias"] == "PF"


class TestUsersLockdown:
    def test_non_platform_cannot_create_user(self, client, db_engine):
        with Session(db_engine) as s:
            _, token = _user_with_token(s, is_platform_member=False)
        r = client.post(
            "/api/v1/users",
            json={"email": "new@x.com", "full_name": "New"},
            headers={"Authorization": f"Bearer {token}"},
        )
        assert r.status_code == 403

    def test_platform_can_create_user(self, client, db_engine, stub_supabase_invite):
        with Session(db_engine) as s:
            _, token = _user_with_token(s, is_platform_member=True)
        r = client.post(
            "/api/v1/users",
            json={"email": "new@x.com", "full_name": "New"},
            headers={"Authorization": f"Bearer {token}"},
        )
        assert r.status_code == 201, r.text

    def test_anonymous_cannot_create_user(self, client):
        r = client.post("/api/v1/users", json={"email": "a@b.com", "full_name": "A"})
        assert r.status_code == 401


class TestUsersTeamSecretGate:
    """POST /users carries an EXPLICIT route-level team-secret requirement
    (defense-in-depth on top of TeamSecretMiddleware). When TEAM_ACCESS_SECRET
    is set, the request must present a matching X-Team-Secret header even with
    a valid platform-member Bearer token; unset, the gate is a no-op."""

    def test_missing_team_secret_is_401_when_configured(
        self, client, db_engine, monkeypatch
    ):
        monkeypatch.setenv("TEAM_ACCESS_SECRET", "correct-secret")
        with Session(db_engine) as s:
            _, token = _user_with_token(s, is_platform_member=True)
        r = client.post(
            "/api/v1/users",
            json={"email": "new@x.com", "full_name": "New"},
            headers={"Authorization": f"Bearer {token}"},
        )
        assert r.status_code == 401
        assert "X-Team-Secret" in r.json()["detail"]

    def test_invalid_team_secret_is_401_when_configured(
        self, client, db_engine, monkeypatch
    ):
        monkeypatch.setenv("TEAM_ACCESS_SECRET", "correct-secret")
        with Session(db_engine) as s:
            _, token = _user_with_token(s, is_platform_member=True)
        r = client.post(
            "/api/v1/users",
            json={"email": "new@x.com", "full_name": "New"},
            headers={
                "Authorization": f"Bearer {token}",
                "X-Team-Secret": "wrong",
            },
        )
        assert r.status_code == 401

    def test_valid_team_secret_passes_the_gate(
        self, client, db_engine, monkeypatch, stub_supabase_invite
    ):
        monkeypatch.setenv("TEAM_ACCESS_SECRET", "correct-secret")
        with Session(db_engine) as s:
            _, token = _user_with_token(s, is_platform_member=True)
        r = client.post(
            "/api/v1/users",
            json={"email": "new@x.com", "full_name": "New"},
            headers={
                "Authorization": f"Bearer {token}",
                "X-Team-Secret": "correct-secret",
            },
        )
        assert r.status_code == 201, r.text

    def test_gate_is_noop_when_secret_unset(
        self, client, db_engine, monkeypatch, stub_supabase_invite
    ):
        # No TEAM_ACCESS_SECRET => local-dev posture, gate must not fire
        monkeypatch.delenv("TEAM_ACCESS_SECRET", raising=False)
        with Session(db_engine) as s:
            _, token = _user_with_token(s, is_platform_member=True)
        r = client.post(
            "/api/v1/users",
            json={"email": "new@x.com", "full_name": "New"},
            headers={"Authorization": f"Bearer {token}"},
        )
        assert r.status_code == 201, r.text


class TestProjectYmlWriter:
    def test_writes_and_preserves_release_configs(self, tmp_path):
        from src.cli.commands.workspace import _write_project_yml

        ws = tmp_path / "ws"
        (ws / ".innoday").mkdir(parents=True)
        # pre-existing project.yml with release_configs
        (ws / ".innoday" / "project.yml").write_text(
            yaml.safe_dump({"release_configs": [{"label": "pixelfuel"}]})
        )

        resolved = {
            "org": {
                "id": "o1",
                "alias": "hs",
                "name": "HS",
                "github_org": "havilandsoftware",
            },
            "project": {"id": "p1", "alias": "pf", "name": "PixelFuel"},
            "github_topic": "pixelfuel",
            "repos": [{"name": "innoday"}, {"name": "pixelfuel-cms"}],
        }
        path = _write_project_yml(ws, resolved)
        data = yaml.safe_load(Path(path).read_text())

        assert data["org"]["alias"] == "hs"
        assert "slug" not in data["org"]  # legacy key no longer written
        assert data["schema_version"] == 2  # format is stamped
        assert data["generated_by"].startswith("innoday ")
        assert data["project"]["github_topic"] == "pixelfuel"
        assert [r["name"] for r in data["repos"]] == ["innoday", "pixelfuel-cms"]
        # release_configs preserved across the rewrite
        assert data["release_configs"] == [{"label": "pixelfuel"}]


def _resolved(repos):
    return {
        "org": {
            "id": "o1",
            "alias": "hs",
            "name": "HS",
            "github_org": "havilandsoftware",
        },
        "project": {"id": "p1", "alias": "pf", "name": "PixelFuel"},
        "github_topic": "pixelfuel",
        "repos": [{"name": n} for n in repos],
    }


class TestOnboardRefreshAlgorithm:
    def test_dict_release_configs_preserves_only_blastoff_fields(self, tmp_path):
        """PF-318: preserve blastoff version fields, repair org/label, drop other
        projects' entries."""
        from src.cli.commands.workspace import _write_project_yml

        ws = tmp_path / "ws"
        (ws / ".innoday").mkdir(parents=True)
        (ws / ".innoday" / "project.yml").write_text(
            yaml.safe_dump(
                {
                    "release_configs": {
                        "pf": {
                            "organization": "STALE",
                            "label": "STALE",
                            "next_version": "v1.2.0",
                            "last_released_version": "v1.1.0",
                            "junk_field": "should-be-dropped",
                        }
                    }
                }
            )
        )
        path = _write_project_yml(ws, _resolved(["innoday"]))
        rc = yaml.safe_load(Path(path).read_text())["release_configs"]["pf"]
        assert rc["next_version"] == "v1.2.0"  # blastoff field preserved
        assert rc["last_released_version"] == "v1.1.0"
        assert rc["organization"] == "hs"  # repaired fresh
        assert rc["label"] == "pixelfuel"  # repaired to resolved topic
        assert "junk_field" not in rc  # non-blastoff field dropped

    def test_archive_prior_context(self, tmp_path):
        from src.cli.commands.workspace import _archive_prior_context

        ws = tmp_path / "ws"
        (ws / ".innoday").mkdir(parents=True)
        (ws / ".innoday" / "project.yml").write_text("old: yaml")
        (ws / "CLAUDE.md").write_text("old claude")

        _archive_prior_context(ws)

        archive = ws / ".innoday" / "archive"
        names = [p.name for p in archive.iterdir()]
        assert any(n.startswith("project.yml.") for n in names)
        assert any(n.startswith("CLAUDE.md.") for n in names)

    def test_archive_prior_context_noop_when_fresh(self, tmp_path):
        from src.cli.commands.workspace import _archive_prior_context

        ws = tmp_path / "ws"
        ws.mkdir()
        _archive_prior_context(ws)  # nothing to archive
        assert not (ws / ".innoday" / "archive").exists()

    def test_archive_removed_repos_moves_to_archived(self, tmp_path):
        from src.cli.commands.workspace import _archive_removed_repos

        ws = tmp_path / "ws"
        # simulate a cloned repo dir that's no longer in the topic
        (ws / "gone-repo").mkdir(parents=True)
        (ws / "gone-repo" / "file.txt").write_text("x")
        (ws / "kept-repo").mkdir()

        # Only what the SERVER reported as removed is archived. "kept-repo"
        # is simply absent from the list, which is no longer grounds for
        # touching it.
        archived = _archive_removed_repos(ws, ["gone-repo"])
        assert archived == ["gone-repo"]
        assert (ws / "archived" / "gone-repo" / "file.txt").exists()
        assert not (ws / "gone-repo").exists()
        assert (ws / "kept-repo").exists()  # still present

    def test_write_workspace_claude_md_is_regeneratable(self, tmp_path):
        from src.cli.commands.workspace import (
            CUSTOM_SECTION_SENTINEL,
            _write_workspace_claude_md,
        )

        ws = tmp_path / "ws"
        ws.mkdir()
        path, _ = _write_workspace_claude_md(
            ws, _resolved(["innoday", "pixelfuel-cms"]), ""
        )
        text = Path(path).read_text()
        assert "auto-generated by `innoday init`/`refresh`" in text
        assert "innoday" in text and "pixelfuel-cms" in text
        assert "hs/pf" in text
        # The generated half is delimited: everything below the marker is the
        # user's and is carried across refreshes. See
        # tests/cli/commands/test_workspace_claude_md_carryforward.py.
        assert CUSTOM_SECTION_SENTINEL in text

    def test_refresh_detected_from_existing_yml(self, tmp_path):
        """init/run_algorithm detects refresh mode when project.yml exists."""
        from src.cli.commands.workspace import _load_existing_yml

        ws = tmp_path / "ws"
        assert _load_existing_yml(ws) == {}  # fresh
        (ws / ".innoday").mkdir(parents=True)
        (ws / ".innoday" / "project.yml").write_text(
            yaml.safe_dump({"org": {"slug": "hs"}})
        )
        assert _load_existing_yml(ws)  # refresh

    def test_claude_md_always_includes_dev_workflow_standard(self, tmp_path):
        """Every generated workspace CLAUDE.md must route dev work through
        build-rockets, so an agent landing here doesn't edit main directly."""
        from src.cli.commands.workspace import _write_workspace_claude_md

        ws = tmp_path / "ws"
        ws.mkdir()
        path, _ = _write_workspace_claude_md(ws, _resolved(["innoday"]), "")
        text = Path(path).read_text()
        assert "/pixelfuel:build-rockets" in text
        assert "Never code on `main`" in text
        assert "PR" in text

    def test_empty_resolve_preserves_existing_repo_list(self, tmp_path):
        """A resolve that discovers 0 repos is ambiguous (bad topic/token vs.
        genuinely empty) — it must not blank a populated repo inventory."""
        from src.cli.commands.workspace import _write_project_yml

        ws = tmp_path / "ws"
        (ws / ".innoday").mkdir(parents=True)
        (ws / ".innoday" / "project.yml").write_text(
            yaml.safe_dump({"repos": [{"name": "innoday"}, {"name": "pixelfuel-cms"}]})
        )
        path = _write_project_yml(ws, _resolved([]))
        repos = yaml.safe_load(Path(path).read_text())["repos"]
        assert [r["name"] for r in repos] == ["innoday", "pixelfuel-cms"]

    def test_nonempty_resolve_still_replaces_repo_list(self, tmp_path):
        """The preservation guard must not freeze the list — a real resolve wins."""
        from src.cli.commands.workspace import _write_project_yml

        ws = tmp_path / "ws"
        (ws / ".innoday").mkdir(parents=True)
        (ws / ".innoday" / "project.yml").write_text(
            yaml.safe_dump({"repos": [{"name": "old-repo"}]})
        )
        path = _write_project_yml(ws, _resolved(["innoday"]))
        repos = yaml.safe_load(Path(path).read_text())["repos"]
        assert [r["name"] for r in repos] == ["innoday"]

    def test_legacy_slug_only_file_upgrades_to_alias(self, tmp_path, monkeypatch):
        """`innoday refresh` must upgrade a pre-alias (org.slug-only) file in
        place rather than dead-ending the user into a from-scratch init."""
        import argparse

        from src.cli.commands.workspace import WorkspaceCommands

        ws = tmp_path / "ws"
        (ws / ".innoday").mkdir(parents=True)
        (ws / ".innoday" / "project.yml").write_text(
            yaml.safe_dump(
                {
                    "org": {"name": "Haviland Software", "slug": "hs"},
                    "project": {"name": "PixelFuel", "alias": "pf"},
                }
            )
        )
        monkeypatch.chdir(ws)

        seen = {}

        async def fake_onboard(config, org_alias, project_alias, path, *a, **kw):
            seen["org"] = org_alias
            seen["project"] = project_alias
            return 0

        monkeypatch.setattr(WorkspaceCommands, "_onboard", fake_onboard)
        args = argparse.Namespace(no_clone=True, no_hooks=True)
        rc = asyncio.run(WorkspaceCommands.execute_refresh(args, None))

        assert rc == 0  # upgraded, not refused
        assert seen["org"] == "hs"  # legacy slug used as the alias
        assert seen["project"] == "pf"

    def test_refresh_strips_dead_slug_fields(self, tmp_path):
        """slug is dead data and must not survive a refresh: the org one was
        renamed to alias, the project one was removed outright."""
        from src.cli.commands.workspace import _write_project_yml

        ws = tmp_path / "ws"
        (ws / ".innoday").mkdir(parents=True)
        (ws / ".innoday" / "project.yml").write_text(
            yaml.safe_dump(
                {
                    "org": {"name": "Haviland", "slug": "hs"},
                    "project": {"name": "PixelFuel", "innoday_slug": "pixelfuel"},
                    "repos": [{"name": "innoday"}],
                }
            )
        )
        text = Path(_write_project_yml(ws, _resolved(["innoday"]))).read_text()
        assert "slug" not in text
        assert yaml.safe_load(text)["org"]["alias"] == "hs"

    def test_refresh_ignores_legacy_project_slug_as_alias(self, tmp_path, monkeypatch):
        """A legacy project `slug`/`innoday_slug` is NOT an alias — sending it
        just 404s, so refresh must fall through to the org default project."""
        import argparse

        from src.cli.commands.workspace import WorkspaceCommands

        ws = tmp_path / "ws"
        (ws / ".innoday").mkdir(parents=True)
        (ws / ".innoday" / "project.yml").write_text(
            yaml.safe_dump(
                {
                    "org": {"name": "Haviland", "slug": "hs"},
                    "project": {"name": "PixelFuel", "innoday_slug": "pixelfuel"},
                }
            )
        )
        monkeypatch.chdir(ws)

        seen = {}

        async def fake_onboard(config, org_alias, project_alias, path, *a, **kw):
            seen["org"] = org_alias
            seen["project"] = project_alias
            return 0

        monkeypatch.setattr(WorkspaceCommands, "_onboard", fake_onboard)
        rc = asyncio.run(
            WorkspaceCommands.execute_refresh(
                argparse.Namespace(no_clone=True, no_hooks=True), None
            )
        )
        assert rc == 0
        assert seen["org"] == "hs"  # org slug still upgrades
        assert seen["project"] is None  # dead project slug NOT used as an alias


class TestGithubTopicLowercasing:
    """GitHub topics are lowercase by definition; project aliases are stored
    UPPERCASE (they double as the ticket prefix). Returning a raw alias made the
    case-sensitive match find nothing and silently report zero repos."""

    def _svc(self):
        from src.services.workspace_onboard import WorkspaceOnboardService

        return WorkspaceOnboardService(session=MagicMock(), github_token="t")

    def _org(self, settings=None):
        org = MagicMock()
        org.settings = settings
        return org

    def _project(self, alias):
        proj = MagicMock()
        proj.alias = alias
        return proj

    def test_uppercase_alias_is_lowercased(self):
        assert self._svc().github_topic(self._org({}), self._project("PF")) == "pf"

    def test_override_is_lowercased_and_alias_kept(self):
        topic = self._svc().github_topic(
            self._org({"github_topics": {"PF": "PixelFuel"}}), self._project("PF")
        )
        assert topic == "pf,pixelfuel"

    def test_override_key_matches_either_casing(self):
        topic = self._svc().github_topic(
            self._org({"github_topics": {"pf": "pixelfuel"}}), self._project("PF")
        )
        assert topic == "pf,pixelfuel"

    def test_no_project_means_no_topic(self):
        assert self._svc().github_topic(self._org({}), None) is None

    @pytest.mark.asyncio
    async def test_discover_matches_topic_case_insensitively(self):
        from src.api.github_api import GitHubAPI

        repos = [
            {"name": "innoday", "topics": ["innoday", "PixelFuel"], "archived": False},
            {"name": "other", "topics": ["unrelated"], "archived": False},
            {"name": "old", "topics": ["pixelfuel"], "archived": True},
        ]
        with patch.object(
            GitHubAPI,
            "get_organization_repositories",
            new=AsyncMock(side_effect=[repos, []]),
        ):
            found = await self._svc().discover_repos(
                self._org(), "havilandsoftware", "pixelfuel"
            )
        assert [r["name"] for r in found] == ["innoday"]


class TestMultipleTopicsPerProject:
    """A project can span several topics (bp's BPAI repos carry `bp-ai` AND
    `brightpower`), stored comma-separated. A repo matching ANY entry belongs."""

    def _svc(self):
        from src.services.workspace_onboard import WorkspaceOnboardService

        return WorkspaceOnboardService(session=MagicMock(), github_token="t")

    def _org(self, settings):
        org = MagicMock()
        org.settings = settings
        return org

    def _project(self, alias):
        proj = MagicMock()
        proj.alias = alias
        return proj

    def test_comma_list_splits_into_topics(self):
        topics = self._svc().github_topics(
            self._org({"github_topics": {"BPAI": "bp-ai,brightpower"}}),
            self._project("BPAI"),
        )
        assert topics == ["bpai", "bp-ai", "brightpower"]

    def test_whitespace_dupes_and_case_normalised(self):
        topics = self._svc().github_topics(
            self._org({"github_topics": {"X": " Bp-AI , brightpower ,bp-ai, "}}),
            self._project("X"),
        )
        assert topics == ["x", "bp-ai", "brightpower"]

    def test_override_extends_rather_than_replaces_alias(self):
        """A repo tagged with only the alias must still be found once an
        override is configured for the project."""
        topics = self._svc().github_topics(
            self._org({"github_topics": {"PF": "pixelfuel"}}), self._project("PF")
        )
        assert topics == ["pf", "pixelfuel"]

    def test_no_override_falls_back_to_lowercased_alias(self):
        assert self._svc().github_topics(self._org({}), self._project("MB")) == ["mb"]

    def test_no_project_returns_empty(self):
        assert self._svc().github_topics(self._org({}), None) == []

    def test_github_topic_str_stays_backward_compatible(self):
        topic = self._svc().github_topic(
            self._org({"github_topics": {"BPAI": "bp-ai,brightpower"}}),
            self._project("BPAI"),
        )
        assert topic == "bpai,bp-ai,brightpower"

    @pytest.mark.asyncio
    async def test_discover_matches_any_topic(self):
        from src.api.github_api import GitHubAPI

        repos = [
            {"name": "bps-api", "topics": ["bp-ai", "brightpower"], "archived": False},
            {"name": "bps-ui-demo", "topics": ["bp-ai"], "archived": False},
            {"name": "esc", "topics": ["brightpower"], "archived": False},
            {"name": "unrelated", "topics": ["datateam"], "archived": False},
        ]
        with patch.object(
            GitHubAPI,
            "get_organization_repositories",
            new=AsyncMock(side_effect=[repos, []]),
        ):
            found = await self._svc().discover_repos(
                self._org({}), "havilandsoftware", ["bp-ai", "brightpower"]
            )
        assert sorted(r["name"] for r in found) == ["bps-api", "bps-ui-demo", "esc"]

    @pytest.mark.asyncio
    async def test_discover_accepts_comma_string(self):
        from src.api.github_api import GitHubAPI

        repos = [
            {"name": "a", "topics": ["bp-ai"], "archived": False},
            {"name": "b", "topics": ["nope"], "archived": False},
        ]
        with patch.object(
            GitHubAPI,
            "get_organization_repositories",
            new=AsyncMock(side_effect=[repos, []]),
        ):
            found = await self._svc().discover_repos(
                self._org({}), "havilandsoftware", "bp-ai,brightpower"
            )
        assert [r["name"] for r in found] == ["a"]


class TestResolveFailsClosedWithoutAVaultCredential:
    """#554: `WorkspaceOnboardService` must not fall back to `GITHUB_TOKEN`.

    `self.github_token = github_token or os.getenv("GITHUB_TOKEN")` meant the one
    live construction path -- `WorkspaceOnboardService(session)` in
    `routers/onboarding.py` -- discovered repos with the operator's token. Any
    authenticated member of any org therefore got a repo listing computed against
    the deployment's own GitHub access rather than their tenant's.

    `discover_repos` now takes the org positionally, so a caller cannot reach it
    without naming the tenant whose credential is to be used.

    The resolver is patched at its import location in `workspace_onboard`, and each
    assertion is about the token that reached `GitHubAPI` -- not about an env read
    disappearing, which a permanently-`None` resolver would also satisfy.
    """

    OPERATOR_TOKEN = "ghp_operator_must_never_be_used"
    TENANT_TOKEN = "ghp_tenant_token"

    def _seed(self, db_engine, alias="acme", project_alias="prod"):
        with Session(db_engine) as s:
            _, token = _user_with_token(s, is_platform_member=True)
            org = Organization(id=str(uuid4()), name="Acme", alias=alias)
            s.add(org)
            s.commit()
            s.add(
                Project(
                    id=str(uuid4()),
                    organization_id=org.id,
                    name="Prod",
                    alias=project_alias,
                    description="d",
                )
            )
            s.commit()
        return token

    def test_unconfigured_org_gets_an_actionable_4xx(
        self, client, db_engine, monkeypatch
    ):
        monkeypatch.setenv("GITHUB_TOKEN", self.OPERATOR_TOKEN)
        token = self._seed(db_engine)

        with patch(
            "src.services.workspace_onboard.get_github_credentials", return_value=None
        ):
            r = client.get(
                "/api/v1/onboarding/resolve",
                params={"org": "acme", "project": "prod"},
                headers={"Authorization": f"Bearer {token}"},
            )

        assert 400 <= r.status_code < 500, r.text
        detail = r.json()["detail"]
        assert "acme" in detail.lower()
        assert "connect github" in detail.lower()

    def test_the_operators_token_never_reaches_github(
        self, client, db_engine, monkeypatch
    ):
        """The fail-closed twin: GitHubAPI must not be constructed at all."""
        monkeypatch.setenv("GITHUB_TOKEN", self.OPERATOR_TOKEN)
        token = self._seed(db_engine, alias="closed", project_alias="cl")

        with (
            patch(
                "src.services.workspace_onboard.get_github_credentials",
                return_value=None,
            ),
            patch("src.services.workspace_onboard.GitHubAPI") as gh,
        ):
            client.get(
                "/api/v1/onboarding/resolve",
                params={"org": "closed", "project": "cl"},
                headers={"Authorization": f"Bearer {token}"},
            )

        gh.assert_not_called()

    def test_the_vault_token_is_what_github_is_called_with(
        self, client, db_engine, monkeypatch
    ):
        monkeypatch.setenv("GITHUB_TOKEN", self.OPERATOR_TOKEN)
        token = self._seed(db_engine, alias="open", project_alias="op")

        api = MagicMock()
        api.get_organization_repositories = AsyncMock(return_value=[])
        with (
            patch(
                "src.services.workspace_onboard.get_github_credentials",
                return_value={"token": self.TENANT_TOKEN, "github_org": "tenant-gh"},
            ),
            patch(
                "src.services.workspace_onboard.GitHubAPI", return_value=api
            ) as gh_cls,
        ):
            r = client.get(
                "/api/v1/onboarding/resolve",
                params={"org": "open", "project": "op"},
                headers={"Authorization": f"Bearer {token}"},
            )

        assert r.status_code == 200, r.text
        gh_cls.assert_called_once_with(token=self.TENANT_TOKEN)

    def test_the_service_still_constructs_with_one_argument(self, db_engine):
        """#550's resolver reaches `github_org()`/`github_topics()` through a
        token-less `WorkspaceOnboardService(session)` (github_connect_service.py
        :520 and :1365). Making `github_token` required there re-breaks the mass
        deactivation #550 fixed, so the single-arg form is pinned here.
        """
        from src.services.workspace_onboard import WorkspaceOnboardService

        with Session(db_engine) as s:
            svc = WorkspaceOnboardService(s)
        assert svc.github_token is None

    def test_no_env_fallback_is_baked_into_the_constructor(self, monkeypatch):
        """`GITHUB_TOKEN` in the environment must not populate the instance."""
        from src.services.workspace_onboard import WorkspaceOnboardService

        monkeypatch.setenv("GITHUB_TOKEN", self.OPERATOR_TOKEN)
        assert WorkspaceOnboardService(session=MagicMock()).github_token is None
