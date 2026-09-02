"""
Tests for the two-step board summary flow (HS-297).

The old flow called Anthropic directly server-side inside the `/summarize`
endpoint using a per-org CLAUDE_API_KEY. That is being replaced with:

  1. GET  .../boards/{board_id}/summary-data  -- assembles the same
     structured ticket/stats data the old endpoint built, but never calls
     Claude. Intended to be consumed by a calling Claude Code session,
     which writes the actual summary text itself.
  2. POST .../boards/{board_id}/summaries -- persists a summary that was
     written externally (by Claude Code) into the same table/shape the old
     endpoint wrote to, so `get_board_summaries` / `get_latest_summary` keep
     working transparently. PF-398 renamed that table `board_summaries` ->
     `summaries` and widened it; this path is unchanged by that and
     TestBoardPathSurvivesTheWidening pins it.

These tests assert:
  - summary-data returns the right structured shape and never touches
    ClaudeAPI/summarize_conversation.
  - POST .../summaries persists correctly and is immediately visible via
    the existing list/latest endpoints.
"""

from datetime import datetime, timedelta, timezone
from unittest.mock import AsyncMock, MagicMock, patch
from uuid import uuid4

import pytest

from src.domain.board import BoardRegistration, BoardType
from src.domain.summary import SummaryType
from src.domain.ticket import Ticket, TicketStatus


@pytest.fixture
def board_registration(db_session, org, project):
    b = BoardRegistration(
        id=str(uuid4()),
        organization_id=org.id,
        project_id=project.id,
        board_name="Test Board",
        board_type=BoardType.JIRA,
        board_url="https://example.atlassian.net",
        board_external_id="1",
    )
    db_session.add(b)
    db_session.commit()
    db_session.refresh(b)
    return b


def _make_ticket(
    org_id,
    project_id,
    board_id,
    *,
    status,
    completed_at=None,
    updated_at=None,
    assignee=None,
):
    t = Ticket(
        organization_id=org_id,
        project_id=project_id,
        board_registration_id=board_id,
        summary="Test ticket",
        status=status,
        completed_at=completed_at,
        assignee=assignee,
    )
    if updated_at is not None:
        t.updated_at = updated_at
    return t


@pytest.fixture
def seeded_tickets(db_session, org, project, board_registration):
    now = datetime.now(timezone.utc)
    tickets = [
        _make_ticket(
            org.id,
            project.id,
            board_registration.id,
            status=TicketStatus.IN_PROGRESS,
            assignee="alice",
            updated_at=now - timedelta(days=1),
        ),
        _make_ticket(
            org.id,
            project.id,
            board_registration.id,
            status=TicketStatus.DONE,
            completed_at=now - timedelta(days=1),
        ),
    ]
    db_session.add_all(tickets)
    db_session.commit()
    return tickets


class TestSummaryDataEndpoint:
    """GET .../boards/{board_id}/summary-data"""

    @pytest.mark.asyncio
    async def test_returns_structured_data_without_calling_claude(
        self, db_session, org, board_registration, seeded_tickets
    ):
        from src.routers.boards import get_board_summary_data

        current_user = MagicMock()
        current_user.id = "test-user"

        with (
            patch("src.routers.boards.require_org_role"),
            patch("src.api.claude_api.ClaudeAPI") as mock_claude_cls,
        ):
            result = await get_board_summary_data(
                organization_id=org.id,
                board_id=board_registration.id,
                summary_type=SummaryType.STATUS,
                since_version=None,
                github_org=None,
                session=db_session,
                current_user=current_user,
            )

        # Never touches ClaudeAPI -- this endpoint has no Anthropic call at all.
        mock_claude_cls.assert_not_called()

        assert result["stats"]["total_tickets"] == 2
        assert result["stats"]["in_progress"] == 1
        assert result["stats"]["completed_7d"] == 1
        assert result["board_name"] == "Test Board"
        assert result["summary_type"] == SummaryType.STATUS
        assert isinstance(result["active_tickets"], list)
        assert isinstance(result["recent_completions"], list)
        # Structured context + prompt so a calling Claude Code session has
        # everything it needs to write the summary itself.
        assert "messages" in result
        assert isinstance(result["messages"], list)
        assert "prompt" in result and result["prompt"]

    @pytest.mark.asyncio
    async def test_declares_the_org_membership_dependency(self):
        """A regression that drops the membership check here must fail a test.

        This used to assert `verify_org_membership(...)` was *called* with the right
        arguments. The check is now a declared FastAPI dependency, so the equivalent
        guarantee is that the parameter is present: a dependency cannot be called with
        the wrong arguments, it either gates the route or it doesn't. Without this,
        mocking the check out everywhere else in this file would let a dropped guard
        slide through silently.
        """
        import inspect

        from src.routers.boards import get_board_summary_data

        deps = [
            p.default.dependency
            for p in inspect.signature(get_board_summary_data).parameters.values()
            if hasattr(p.default, "dependency")
        ]
        assert any(
            "require_org_role" in getattr(d, "__qualname__", "") for d in deps
        ), "get_board_summary_data no longer declares Depends(require_org_role())"

    @pytest.mark.asyncio
    async def test_404_when_board_not_found(self, db_session, org):
        from fastapi import HTTPException

        from src.routers.boards import get_board_summary_data

        current_user = MagicMock()
        current_user.id = "test-user"

        with (
            patch("src.routers.boards.require_org_role"),
            pytest.raises(HTTPException) as exc_info,
        ):
            await get_board_summary_data(
                organization_id=org.id,
                board_id="does-not-exist",
                summary_type=SummaryType.STATUS,
                since_version=None,
                github_org=None,
                session=db_session,
                current_user=current_user,
            )
        assert exc_info.value.status_code == 404

    @pytest.mark.asyncio
    async def test_404_when_no_tickets(self, db_session, org, board_registration):
        from fastapi import HTTPException

        from src.routers.boards import get_board_summary_data

        current_user = MagicMock()
        current_user.id = "test-user"

        with patch("src.routers.boards.require_org_role"):
            with pytest.raises(HTTPException) as exc_info:
                await get_board_summary_data(
                    organization_id=org.id,
                    board_id=board_registration.id,
                    summary_type=SummaryType.STATUS,
                    since_version=None,
                    github_org=None,
                    session=db_session,
                    current_user=current_user,
                )
        assert exc_info.value.status_code == 404


class TestReleaseSummaryGitHubCredential:
    """#554: the release summary must not fetch commits with the operator's token.

    `github_token = os.getenv("GITHUB_TOKEN")` handed the process-wide token to
    `_fetch_commits_since_tag`, and that helper treats a falsy token as
    *anonymous* -- so an unconfigured tenant got a silent partial summary (missing
    private repos) with nothing in the response saying so, while a configured
    deployment leaked the operator's read access into every tenant's summary.

    Both tests set `GITHUB_TOKEN` to a sentinel and patch the resolver at its
    import location in the router, so what is asserted is the token that reached
    the boundary -- not merely that an env read disappeared, which a resolver
    returning `None` on every backend would also satisfy.
    """

    OPERATOR_TOKEN = "ghp_operator_must_never_be_used"
    TENANT_TOKEN = "ghp_tenant_token"

    async def _release_summary(self, db_session, org, board_id, **overrides):
        from src.routers.boards import get_board_summary_data

        kwargs = dict(
            organization_id=org.id,
            board_id=board_id,
            summary_type=SummaryType.RELEASE,
            since_version="v1.4.0",
            github_org=None,
            session=db_session,
            current_user=MagicMock(id="test-user"),
        )
        kwargs.update(overrides)
        with patch("src.routers.boards.require_org_role"):
            return await get_board_summary_data(**kwargs)

    @pytest.mark.asyncio
    async def test_vault_token_reaches_the_commit_fetch(
        self, db_session, org, board_registration, seeded_tickets, monkeypatch
    ):
        monkeypatch.setenv("GITHUB_TOKEN", self.OPERATOR_TOKEN)

        fetch = AsyncMock(return_value={})
        with (
            patch(
                "src.routers.boards.get_github_credentials",
                return_value={"token": self.TENANT_TOKEN, "github_org": "tenant-gh"},
            ),
            patch("src.routers.boards._fetch_commits_since_tag", new=fetch),
        ):
            await self._release_summary(db_session, org, board_registration.id)

        fetch.assert_awaited_once()
        assert fetch.await_args.kwargs["token"] == self.TENANT_TOKEN
        assert fetch.await_args.kwargs["token"] != self.OPERATOR_TOKEN

    @pytest.mark.asyncio
    async def test_unconfigured_org_says_so_instead_of_fetching_anonymously(
        self, db_session, org, board_registration, seeded_tickets, monkeypatch
    ):
        """The fail-closed twin: no fetch at all, and the caller is told why.

        A commit-less release summary that looks like "no commits since v1.4.0" is
        indistinguishable from a correct one, which is why the message matters as
        much as the skipped call.
        """
        monkeypatch.setenv("GITHUB_TOKEN", self.OPERATOR_TOKEN)

        fetch = AsyncMock(return_value={})
        with (
            patch("src.routers.boards.get_github_credentials", return_value=None),
            patch("src.routers.boards._fetch_commits_since_tag", new=fetch),
        ):
            result = await self._release_summary(db_session, org, board_registration.id)

        fetch.assert_not_awaited()
        joined = "\n".join(result["messages"])
        assert "not connected" in joined.lower()
        assert "github" in joined.lower()

    @pytest.mark.asyncio
    async def test_github_org_comes_from_the_project_aware_resolver(
        self, db_session, org, project, board_registration, seeded_tickets, monkeypatch
    ):
        """`org.alias` was only ever right by coincidence.

        Which InnoDay org owns a project and which GitHub org hosts its repos are
        independent (#550), and `board_reg.project_id` is NOT NULL -- so the
        per-project `settings['github_orgs']` override is available here and must
        win over the alias.
        """
        monkeypatch.setenv("GITHUB_TOKEN", self.OPERATOR_TOKEN)
        org.settings = {"github_orgs": {project.alias: "hosting-gh-org"}}
        db_session.add(org)
        db_session.commit()

        fetch = AsyncMock(return_value={})
        with (
            patch(
                "src.routers.boards.get_github_credentials",
                return_value={"token": self.TENANT_TOKEN},
            ),
            patch("src.routers.boards._fetch_commits_since_tag", new=fetch),
        ):
            await self._release_summary(db_session, org, board_registration.id)

        assert fetch.await_args.kwargs["github_org"] == "hosting-gh-org"
        assert fetch.await_args.kwargs["github_org"] != org.alias

    @pytest.mark.asyncio
    async def test_an_explicit_github_org_query_param_still_wins(
        self, db_session, org, project, board_registration, seeded_tickets, monkeypatch
    ):
        monkeypatch.setenv("GITHUB_TOKEN", self.OPERATOR_TOKEN)
        org.settings = {"github_orgs": {project.alias: "hosting-gh-org"}}
        db_session.add(org)
        db_session.commit()

        fetch = AsyncMock(return_value={})
        with (
            patch(
                "src.routers.boards.get_github_credentials",
                return_value={"token": self.TENANT_TOKEN},
            ),
            patch("src.routers.boards._fetch_commits_since_tag", new=fetch),
        ):
            await self._release_summary(
                db_session, org, board_registration.id, github_org="caller-said-this"
            )

        assert fetch.await_args.kwargs["github_org"] == "caller-said-this"


class TestSaveBoardSummaryEndpoint:
    """POST .../boards/{board_id}/summaries -- persist an externally-written summary."""

    @pytest.mark.asyncio
    async def test_persists_summary_with_expected_shape(
        self, db_session, org, board_registration
    ):
        from src.routers.boards import (
            SaveSummaryRequest,
            get_latest_summary,
            save_board_summary,
        )

        current_user = MagicMock()
        current_user.id = "test-user"

        request = SaveSummaryRequest(
            summary_type=SummaryType.STATUS,
            summary="Claude Code wrote this summary from the structured data.",
            stats={"total_tickets": 5, "in_progress": 2},
            highlights=["Shipped feature X"],
            concerns=["Ticket ABC-1 stuck for 5 days"],
        )

        with patch("src.routers.boards.require_org_role"):
            result = await save_board_summary(
                organization_id=org.id,
                board_id=board_registration.id,
                request=request,
                session=db_session,
                current_user=current_user,
            )

        assert result.summary == request.summary
        assert result.stats["total_tickets"] == 5
        assert result.highlights == ["Shipped feature X"]
        assert result.concerns == ["Ticket ABC-1 stuck for 5 days"]

        # A subsequent list/latest call must see it transparently -- same
        # table/shape as the old Anthropic-backed write path.
        with patch("src.routers.boards.require_org_role"):
            latest = await get_latest_summary(
                organization_id=org.id,
                board_id=board_registration.id,
                session=db_session,
                current_user=current_user,
            )

        assert latest["summary"] == request.summary
        assert latest["stats"]["total_tickets"] == 5

    @pytest.mark.asyncio
    async def test_never_calls_claude_api(self, db_session, org, board_registration):
        from src.routers.boards import SaveSummaryRequest, save_board_summary

        current_user = MagicMock()
        current_user.id = "test-user"

        request = SaveSummaryRequest(
            summary_type=SummaryType.DAILY,
            summary="Written externally by Claude Code.",
            stats={},
        )

        with (
            patch("src.routers.boards.require_org_role"),
            patch("src.api.claude_api.ClaudeAPI") as mock_claude_cls,
        ):
            await save_board_summary(
                organization_id=org.id,
                board_id=board_registration.id,
                request=request,
                session=db_session,
                current_user=current_user,
            )

        mock_claude_cls.assert_not_called()

    @pytest.mark.asyncio
    async def test_declares_the_org_membership_dependency(self):
        """Same guarantee as the read endpoint's, for the write endpoint.

        See the note on TestSummaryDataEndpoint's version: the check moved from a
        body call to a declared dependency, so the assertion moved with it.
        """
        import inspect

        from src.routers.boards import save_board_summary

        deps = [
            p.default.dependency
            for p in inspect.signature(save_board_summary).parameters.values()
            if hasattr(p.default, "dependency")
        ]
        assert any(
            "require_org_role" in getattr(d, "__qualname__", "") for d in deps
        ), "save_board_summary no longer declares Depends(require_org_role())"

    @pytest.mark.asyncio
    async def test_404_when_board_not_found(self, db_session, org):
        from fastapi import HTTPException

        from src.routers.boards import SaveSummaryRequest, save_board_summary

        current_user = MagicMock()
        current_user.id = "test-user"

        request = SaveSummaryRequest(
            summary_type=SummaryType.STATUS,
            summary="Some summary",
            stats={},
        )

        with pytest.raises(HTTPException) as exc_info:
            await save_board_summary(
                organization_id=org.id,
                board_id="does-not-exist",
                request=request,
                session=db_session,
                current_user=current_user,
            )
        assert exc_info.value.status_code == 404


class TestBoardPathSurvivesTheWidening:
    """PF-398 renamed and widened the table underneath these endpoints.

    The board-scoped flow predates project/user scoping and windows entirely,
    so the risk of the rename was never the rename -- it was the new NOT NULL
    `project_id` and the new live-uniqueness indexes quietly changing what this
    path is allowed to write. These assertions pin both.
    """

    @pytest.mark.asyncio
    async def test_repeated_saves_still_accumulate_as_history(
        self, db_session, org, board_registration
    ):
        """Three status summaries for one board, all listed, newest latest.

        A summary with no window carries `window_spec = ''`, which both
        uniqueness indexes exclude -- so appending to a board's history is
        still allowed, exactly as it was before the widening.
        """
        from src.routers.boards import (
            SaveSummaryRequest,
            get_board_summaries,
            get_latest_summary,
            save_board_summary,
        )

        current_user = MagicMock()
        current_user.id = "test-user"

        for n in range(3):
            with patch("src.routers.boards.require_org_role"):
                await save_board_summary(
                    organization_id=org.id,
                    board_id=board_registration.id,
                    request=SaveSummaryRequest(
                        summary_type=SummaryType.STATUS,
                        summary=f"summary {n}",
                        stats={"n": n},
                    ),
                    session=db_session,
                    current_user=current_user,
                )

        with patch("src.routers.boards.require_org_role"):
            listed = await get_board_summaries(
                organization_id=org.id,
                board_id=board_registration.id,
                summary_type=None,
                limit=10,
                session=db_session,
                current_user=current_user,
            )
            latest = await get_latest_summary(
                organization_id=org.id,
                board_id=board_registration.id,
                session=db_session,
                current_user=current_user,
            )

        assert listed["count"] == 3
        assert latest["summary"] == "summary 2"

    @pytest.mark.asyncio
    async def test_the_summary_inherits_the_boards_project(
        self, db_session, org, project, board_registration
    ):
        """`project_id` is NOT NULL now, and the board is where it comes from."""
        from src.routers.boards import SaveSummaryRequest, save_board_summary

        current_user = MagicMock()
        current_user.id = "test-user"

        with patch("src.routers.boards.require_org_role"):
            saved = await save_board_summary(
                organization_id=org.id,
                board_id=board_registration.id,
                request=SaveSummaryRequest(
                    summary_type=SummaryType.STATUS,
                    summary="written externally",
                    stats={},
                ),
                session=db_session,
                current_user=current_user,
            )

        from src.domain.summary import Summary

        stored = db_session.get(Summary, saved.id)
        assert stored.project_id == project.id
        assert stored.board_registration_id == board_registration.id
        assert stored.user_id is None
        assert stored.window_spec == ""
        assert stored.superseded_by_id is None
        assert stored.body_markdown == "written externally"
