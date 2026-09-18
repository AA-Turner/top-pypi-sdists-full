"""One driver for a release and a hotfix, and a release that says what it covered.

Two halves of the same correction, and the second only became reachable once the
first had happened.

**The driver.** A hotfix was driven by thirty lines beside a release's hundred
and fifty, and the gap was not need -- it was neglect. Everything the release
gained after they were split was gained by one of them: the server-assembled
brief, so a *preview* stopped needing a personal GitHub token; the ticket
picture; the reporter, so the spinner is put away before the report and the
`[y/N]` prompt are printed; the line afterwards saying how to actually tag. The
hotfix driver was never even handed `config`, `org_id` or `project_id`, so it
could not have asked InnoDay what the release contained if it had wanted to.

**The coverage.** A release records which repositories it covered, and the
server worked that out by reading the project's live repository links. That is
right for a release and wrong for every narrowed hotfix: `--repo bps-ui-v2` tags
one repository and was recorded as covering all seven, so the next release read
a coverage shrink that never happened and a revert had nothing telling it which
repository to clean up. The engine knows what it tagged; it now says so, and the
server believes it.

Fixtures are local rather than shared: the sibling test modules for the proxy
and the releases router are being edited on other branches, and a shared fixture
is the thing that makes two of those collide.
"""

import argparse
import asyncio
import json
from types import SimpleNamespace
from unittest.mock import AsyncMock, MagicMock, patch
from uuid import uuid4

import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session

from src.api.app import app
from src.cli.commands.release_proxy import ReleaseProxyCommands
from src.database import get_session
from src.domain.organization import Organization
from src.domain.project import Project, ProjectRepository
from src.domain.release import Release as ReleaseRow
from src.domain.repository import Repository
from src.domain.user import User, UserRole
from tests.auth_helpers import bearer_for
from tests.db_helpers import build_test_engine

# --------------------------------------------------------------------------- #
# The driver
# --------------------------------------------------------------------------- #

#: What `/release/content` hands back. Only ever passed through here -- nothing
#: in these tests renders it -- so it carries the one field the brief requires
#: and nothing else.
CONTENT = {"repos": ["web", "api"], "included": [], "outstanding": []}


def cli_args(**overrides):
    """The namespace `innoday blastoff` builds, with a hotfix's defaults."""
    defaults = dict(
        hotfix=True,
        dry_run=False,
        do_release=False,
        assume_yes=False,
        topics=None,
        repo=None,
        commit=None,
        branch=None,
        org_id="org-1",
        project_id="proj-1",
        token="a-token",  # so the `gh` offer never enters the picture here
        github_org=None,
        summary=None,
        commits=False,
        as_json=False,
        generate_summary=False,
        dir=None,
    )
    defaults.update(overrides)
    return argparse.Namespace(**defaults)


def cli_store(*, last_released="v1.3.0", picture=(4, 1)):
    """A store that has already answered the version question.

    `next_version` and `last_released_version` are deliberately on different
    minor lines: a hotfix that read the first would tag v1.4.1, which is a patch
    on a version that has not shipped.
    """
    store = MagicMock()
    store.load_org_config.return_value = SimpleNamespace(
        next_version="v1.4.0",
        last_released_version=last_released,
        last_released="2026-07-01T00:00:00Z",
        topics=["pf"],
    )
    store.ticket_picture.return_value = picture
    return store


class Reporter:
    """A spinner that remembers when it was put away.

    The hotfix driver was never handed one, so on that path the animation kept
    drawing over the engine's report and over the question asking whether to
    tag. `stopped_before_the_engine` is the whole assertion.
    """

    def __init__(self):
        self.stopped = False
        self.stopped_before_the_engine = None
        self.updates = []

    def update(self, text):
        self.updates.append(text)

    def stop(self):
        self.stopped = True


def drive(*, content=CONTENT, store=None, reporter=None, **arg_overrides):
    """Run the driver, returning what reached the engine.

    `_fetch_content` is stubbed rather than mocked at the HTTP layer: every
    assertion here is about what the driver hands over, not about how the
    content was obtained.
    """
    store = store or cli_store()
    captured = {"argv": None, "brief": None, "asked_the_server": False}

    def fake_invoke(app_cls, argv, st, stdin=None, confirm=None):
        captured["argv"] = argv
        captured["brief"] = json.loads(stdin) if stdin else None
        captured["engine"] = app_cls
        if reporter is not None:
            reporter.stopped_before_the_engine = reporter.stopped
        return 0

    async def fake_content(*a, **k):
        captured["asked_the_server"] = True
        captured["content_kwargs"] = k
        return content

    with (
        patch.object(
            ReleaseProxyCommands, "_invoke_blastoff", staticmethod(fake_invoke)
        ),
        patch.object(
            ReleaseProxyCommands, "_fetch_content", staticmethod(fake_content)
        ),
    ):
        captured["code"] = asyncio.run(
            ReleaseProxyCommands._drive_release(
                cli_args(**arg_overrides),
                store,
                "pf",
                "havilandsoftware",
                ["pf"],
                MagicMock(),
                "org-1",
                "proj-1",
                hotfix=arg_overrides.get("hotfix", True),
                reporter=reporter,
            )
        )
    return captured


class TestAHotfixIsDrivenLikeARelease:
    """Everything a release gained while the hotfix driver stood still."""

    def test_it_gets_the_assembled_brief(self):
        """**The one that matters.** The content is fetched server-side with the
        organisation's own credential, so a hotfix *preview* stops asking
        whoever ran it for a personal GitHub token."""
        result = drive()
        assert result["asked_the_server"] is True
        assert result["brief"]["content"] == CONTENT
        assert result["argv"][:2] == ["--brief", "-"]

    def test_it_gets_the_ticket_picture(self):
        """The half blastoff structurally cannot provide: it decides what is in
        a release from GitHub merge dates and has no idea tickets exist."""
        result = drive()
        assert result["brief"]["ticket_count"] == 4
        assert result["brief"]["open_ticket_count"] == 1

    def test_it_patches_the_line_that_shipped(self):
        """v1.3.0 released and v1.4.0 planned patches to v1.3.1. Reading
        `next_version` -- which is what a brief supplies unless told otherwise
        -- would tag v1.4.1: a patch on a version nobody has seen."""
        result = drive()
        assert result["brief"]["version"] == "v1.3.1"

    def test_a_release_still_cuts_the_planned_version(self):
        result = drive(hotfix=False)
        assert result["brief"]["version"] == "v1.4.0"
        assert "--hotfix" not in result["argv"]

    def test_the_window_starts_at_the_last_release(self):
        result = drive()
        assert result["brief"]["previous_version"] == "v1.3.0"
        assert result["brief"]["previous_released_at"] == "2026-07-01T00:00:00Z"
        assert result["content_kwargs"]["since"] == "2026-07-01T00:00:00Z"
        assert result["content_kwargs"]["version"] == "v1.3.1"

    def test_the_spinner_is_put_away_before_the_engine_prints(self):
        """It runs over the report and over the `[y/N]` prompt otherwise, which
        is the exact thing the rocket was added to prevent."""
        reporter = Reporter()
        drive(reporter=reporter)
        assert reporter.stopped_before_the_engine is True

    def test_it_says_how_to_actually_tag(self, capsys):
        """A report that stops without saying how to proceed reads as a
        failure, and the obvious guess -- run it again -- finds nothing."""
        drive()
        assert "Report only" in capsys.readouterr().out

    def test_nothing_released_is_refused_before_anything_runs(self, capsys):
        """No line to patch. Inventing v0.0.1 would claim there was one."""
        result = drive(store=cli_store(last_released=None))
        assert result["code"] == 1
        assert result["argv"] is None
        assert "nothing to patch" in capsys.readouterr().out


class TestTheNarrowingReachesTheEngine:
    """`--repo`, `--commit` and `--branch` are the hotfix's whole point."""

    def test_the_flag_itself(self):
        assert "--hotfix" in drive()["argv"]

    def test_one_repository(self):
        argv = drive(repo="bps-ui-v2")["argv"]
        assert argv[argv.index("--repo") + 1] == "bps-ui-v2"

    def test_one_commit(self):
        argv = drive(repo="web", commit="abc1234")["argv"]
        assert argv[argv.index("--commit") + 1] == "abc1234"

    def test_one_branch(self):
        argv = drive(repo="web", branch="hotfix/leak")["argv"]
        assert argv[argv.index("--branch") + 1] == "hotfix/leak"

    def test_a_narrowed_hotfix_does_not_use_content_it_cannot_narrow(self):
        """The assembled window has no end and covers every repository. Handing
        it to a run bounded by `--commit` would render work the tag does not
        contain, so that run reads GitHub itself -- as it always has."""
        result = drive(repo="web", commit="abc1234")
        assert result["asked_the_server"] is False
        assert "content" not in result["brief"]


class TestTheReportFlagsAreForwarded:
    """Declared on this parser *and* forwarded, or they are unreachable."""

    def test_summary(self):
        argv = drive(summary="Fixes the leak")["argv"]
        assert argv[argv.index("--summary") + 1] == "Fixes the leak"

    def test_commits(self):
        assert "--commits" in drive(commits=True)["argv"]

    def test_json(self):
        assert "--json" in drive(as_json=True)["argv"]

    def test_generate_summary(self):
        assert "--generate-summary" in drive(generate_summary=True)["argv"]


class TestTheCommandLineStillWorks:
    """`innoday hotfix` is what people type, and it has to keep resolving."""

    @staticmethod
    def _parse(argv):
        parser = argparse.ArgumentParser()
        ReleaseProxyCommands.setup_parser(parser, "hotfix")
        return parser.parse_args(argv)

    def test_the_narrowing_switches_are_declared(self):
        """An undeclared flag is rejected by argparse before blastoff is ever
        reached, so a switch the engine defines is unreachable through the
        proxy until it is repeated here."""
        args = self._parse(["--repo", "web", "--branch", "hotfix/leak"])
        assert args.repo == "web"
        assert args.branch == "hotfix/leak"

    def test_the_alias_dispatches_to_a_hotfix(self):
        from src.cli import main as cli_main

        seen = {}

        async def fake_execute(args, config):
            seen["repo"] = args.repo
            seen["branch"] = args.branch
            return 0

        with (
            patch.object(
                cli_main, "CLIConfig", return_value=MagicMock(legacy_context_error=None)
            ),
            patch.object(cli_main, "_prime_org_id", new=AsyncMock()),
            patch.object(
                cli_main, "_prime_project_id", new=AsyncMock(return_value=None)
            ),
            patch.object(
                cli_main.ReleaseProxyCommands,
                "execute_hotfix",
                staticmethod(fake_execute),
            ),
        ):
            code = cli_main.main(["hotfix", "--repo", "web", "--branch", "hotfix/leak"])
        assert code == 0
        assert seen == {"repo": "web", "branch": "hotfix/leak"}


class TestNarrowingARelease:
    """A release covers the project, so it may not be narrowed -- and the
    refusal happens here, before the report, where stopping is free."""

    @staticmethod
    def _scope(hotfix, **overrides):
        return ReleaseProxyCommands._check_scope(cli_args(**overrides), hotfix)

    @pytest.mark.parametrize("flag", ["repo", "commit", "branch"])
    def test_every_narrowing_switch_is_hotfix_only(self, flag):
        message = self._scope(False, **{flag: "x"})
        assert message is not None
        assert f"--{flag} is only for a hotfix" in message

    @pytest.mark.parametrize("flag", ["commit", "branch"])
    def test_an_end_to_the_window_needs_a_repository(self, flag):
        message = self._scope(True, **{flag: "x"})
        assert message is not None
        assert f"--{flag} needs --repo" in message

    def test_two_ends_are_refused(self):
        message = self._scope(True, repo="web", commit="abc", branch="hotfix/leak")
        assert message is not None
        assert "two ways to say the same thing" in message

    def test_a_whole_project_hotfix_is_fine(self):
        assert self._scope(True) is None


# --------------------------------------------------------------------------- #
# The MCP tool
# --------------------------------------------------------------------------- #


class TestTheMcpToolMakesOneCall:
    """It built a brief and then threw it away on the hotfix side.

    And it appended `--json` to every preview while the hotfix engine defined no
    such switch, so an MCP hotfix preview failed on its own arguments before it
    reached anything at all. Both faults were the split itself.
    """

    @staticmethod
    def _call(**kwargs):
        import src.mcp.server as mcp_module

        captured = {}

        def fake_invoke(app_cls, argv, store, stdin=None, confirm=None):
            captured["engine"] = app_cls
            captured["argv"] = argv
            captured["brief"] = json.loads(stdin) if stdin else None
            print(json.dumps({"version": "v1.3.1"}))
            return 0

        api = MagicMock()
        api.resolve_org.return_value = "org-1"
        api.resolve_project.return_value = "proj-1"

        store = cli_store()

        with (
            patch.object(mcp_module, "_api", api),
            patch.object(mcp_module, "build_cli_config", MagicMock()),
            patch(
                "src.cli.commands.release_proxy._resolve_release_target",
                AsyncMock(return_value=("pf", "havilandsoftware", ["pf"])),
            ),
            # The tool builds its own client straight from `src.cli.client`,
            # not through the proxy module, so that is where it has to be
            # replaced.
            patch("src.cli.client.InnoDayAPIClient", MagicMock()),
            patch("src.cli.commands.release_proxy._build_store", return_value=store),
            patch.object(
                ReleaseProxyCommands, "_invoke_blastoff", staticmethod(fake_invoke)
            ),
        ):
            call = dict(
                release=False,
                hotfix=False,
                summary=None,
                topics=None,
                repo=None,
                commit=None,
                organization_id=None,
                project_id=None,
            )
            call.update(kwargs)
            captured["result"] = asyncio.run(mcp_module.blastoff(**call))
        return captured

    def test_a_hotfix_preview_sends_the_brief(self):
        captured = self._call(hotfix=True)
        assert captured["argv"][:2] == ["--brief", "-"]
        assert captured["brief"]["version"] == "v1.3.1"
        assert "--hotfix" in captured["argv"]

    def test_it_no_longer_drives_a_second_engine(self):
        from blastoff.release import Release

        assert self._call(hotfix=True)["engine"] is Release
        assert self._call(hotfix=False)["engine"] is Release

    def test_the_preview_switch_is_one_the_engine_defines(self):
        """`--json` was appended to every preview, and the hotfix engine had no
        such switch. It is the release engine's, and that is now the only engine
        there is."""
        from blastoff.release import Release

        assert "--json" in self._call(hotfix=True)["argv"]
        assert hasattr(Release, "_json"), "the switch the preview relies on"

    def test_the_narrowing_is_passed_through(self):
        argv = self._call(hotfix=True, repo="web", commit="abc1234")["argv"]
        assert argv[argv.index("--repo") + 1] == "web"
        assert argv[argv.index("--commit") + 1] == "abc1234"


# --------------------------------------------------------------------------- #
# What the release records that it covered
# --------------------------------------------------------------------------- #


@pytest.fixture
def db_engine():
    return build_test_engine()


@pytest.fixture
def db_session(db_engine):
    with Session(db_engine) as session:
        yield session


@pytest.fixture
def client(db_engine):
    def override_get_session():
        with Session(db_engine) as session:
            yield session

    app.dependency_overrides[get_session] = override_get_session
    with patch("src.api.app._assert_schema_at_head"):
        with TestClient(app) as c:
            yield c
    app.dependency_overrides.clear()


@pytest.fixture
def org(db_session):
    o = Organization(id=str(uuid4()), name="Coverage Org")
    db_session.add(o)
    db_session.commit()
    db_session.refresh(o)
    return o


@pytest.fixture
def project(db_session, org):
    p = Project(
        id=str(uuid4()),
        organization_id=org.id,
        alias=f"C{str(uuid4())[:6]}".upper(),
        name="Coverage Project",
        description="Coverage project",
    )
    db_session.add(p)
    db_session.commit()
    db_session.refresh(p)
    return p


@pytest.fixture
def linked_repos(db_session, org, project):
    """Three repositories on the project -- the set the server would infer."""
    names = ["bps-api", "bps-ui-v2", "auditagent"]
    for index, name in enumerate(names):
        repo = Repository(
            id=f"{9000 + index}",
            organization_id=org.id,
            name=name,
            full_name=f"havilandsoftware/{name}",
            url=f"https://github.com/havilandsoftware/{name}",
        )
        db_session.add(repo)
        db_session.add(
            ProjectRepository(
                id=str(uuid4()),
                project_id=project.id,
                repository_id=repo.id,
                is_active=True,
            )
        )
    db_session.commit()
    return sorted(names)


@pytest.fixture
def auth_headers(db_session, org):
    user = User(
        id=str(uuid4()),
        email=f"{uuid4()}@example.com",
        full_name="Coverage User",
        role=UserRole.MEMBER,
        is_platform_member=True,
    )
    db_session.add(user)
    db_session.commit()
    return bearer_for(db_session, user.id)


def _row(db_session, release_id):
    db_session.expire_all()
    return db_session.get(ReleaseRow, release_id)


class TestTheCallerSaysWhatItCovered:
    """Told beats inferred; inferred beats nothing."""

    def test_a_supplied_list_is_what_is_recorded(
        self, client, org, project, linked_repos, db_session, auth_headers
    ):
        """The narrowed hotfix: one repository tagged out of three linked."""
        response = client.post(
            f"/api/v1/organizations/{org.id}/releases",
            json={
                "version": "v1.3.1",
                "project_id": project.id,
                "status": "released",
                "repo_names": ["bps-ui-v2"],
            },
            headers=auth_headers,
        )
        assert response.status_code == 201
        assert _row(db_session, response.json()["id"]).repo_names == ["bps-ui-v2"]

    def test_saying_nothing_still_infers(
        self, client, org, project, linked_repos, db_session, auth_headers
    ):
        """An older engine, or a person marking a release shipped by hand. An
        inferred record is worse than a true one and much better than none."""
        response = client.post(
            f"/api/v1/organizations/{org.id}/releases",
            json={
                "version": "v1.4.0",
                "project_id": project.id,
                "status": "released",
            },
            headers=auth_headers,
        )
        assert response.status_code == 201
        assert _row(db_session, response.json()["id"]).repo_names == linked_repos

    def test_a_planned_release_records_no_coverage_yet(
        self, client, org, project, linked_repos, db_session, auth_headers
    ):
        """It has not covered anything -- it has not happened."""
        response = client.post(
            f"/api/v1/organizations/{org.id}/releases",
            json={"version": "v1.5.0", "project_id": project.id, "status": "planned"},
            headers=auth_headers,
        )
        assert response.status_code == 201
        assert _row(db_session, response.json()["id"]).repo_names is None

    def test_a_patch_that_ships_says_so(
        self, client, org, project, linked_repos, db_session, auth_headers
    ):
        """The engine's own path: create the row, then PATCH it to released --
        which is what a re-run of a release that already recorded itself does."""
        created = client.post(
            f"/api/v1/organizations/{org.id}/releases",
            json={"version": "v1.6.0", "project_id": project.id, "status": "planned"},
            headers=auth_headers,
        )
        release_id = created.json()["id"]

        response = client.patch(
            f"/api/v1/organizations/{org.id}/releases/{release_id}",
            json={"status": "released", "repo_names": ["auditagent"]},
            headers=auth_headers,
        )
        assert response.status_code == 200
        assert _row(db_session, release_id).repo_names == ["auditagent"]

    def test_a_patch_that_says_nothing_infers(
        self, client, org, project, linked_repos, db_session, auth_headers
    ):
        created = client.post(
            f"/api/v1/organizations/{org.id}/releases",
            json={"version": "v1.7.0", "project_id": project.id, "status": "planned"},
            headers=auth_headers,
        )
        release_id = created.json()["id"]

        response = client.patch(
            f"/api/v1/organizations/{org.id}/releases/{release_id}",
            json={"status": "released"},
            headers=auth_headers,
        )
        assert response.status_code == 200
        assert _row(db_session, release_id).repo_names == linked_repos


class TestTheStoreSendsWhatWasTagged:
    """The engine reports its coverage; the store has to pass it on."""

    @staticmethod
    def _record(**kwargs):
        from src.integrations.innoday_version_store import InnoDayVersionStore

        store = InnoDayVersionStore(
            api_client=MagicMock(),
            org_id="org-1",
            project_id="proj-1",
            github_org="havilandsoftware",
            topics=["pf"],
        )
        sent = {}

        async def fake_create_or_update(body):
            sent["body"] = body

        with patch.object(store, "_create_or_update_release", fake_create_or_update):
            store.record_release(
                SimpleNamespace(alias="pf"),
                "v1.3.1",
                released_at="2026-09-01",
                **kwargs,
            )
        return sent["body"]

    def test_the_repositories_reach_the_body(self):
        body = self._record(repo_names=["bps-ui-v2"])
        assert body["repo_names"] == ["bps-ui-v2"]

    def test_the_order_is_the_order_they_were_tagged(self):
        body = self._record(repo_names=["web", "api", "data"])
        assert body["repo_names"] == ["web", "api", "data"]

    def test_saying_nothing_leaves_the_server_to_infer(self):
        """Not an empty list. That would overwrite the server's inference with
        a claim that the release covered no repository at all."""
        assert "repo_names" not in self._record()
        assert "repo_names" not in self._record(repo_names=[])
