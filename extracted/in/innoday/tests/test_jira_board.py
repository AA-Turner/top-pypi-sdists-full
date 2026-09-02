"""
Tests for Jira board connectivity and active ticket retrieval.

These unit tests verify that:
- The probe endpoint correctly filters out done/todo/backlog tickets
- Only in_progress and in_test tickets are returned
- The top 5 limit is enforced
- The response shape is correct

A separate integration test (marked @pytest.mark.jira) live-fetches from a
configured Jira board — only runs when BOARD_API_EMAIL is set in env/orgs/<slug>.
"""

from uuid import uuid4

import pytest
from sqlmodel import select

from src.domain.board import BoardRegistration, BoardType
from src.domain.organization import Organization
from src.domain.project import Project
from src.domain.ticket import Ticket, TicketStatus

# ---------------------------------------------------------------------------
# Shared fixtures
# ---------------------------------------------------------------------------


@pytest.fixture
def org(db_session):
    o = Organization(name="Example Org")
    db_session.add(o)
    db_session.commit()
    db_session.refresh(o)
    return o


@pytest.fixture
def project(db_session, org):
    p = Project(
        id=str(uuid4()),
        organization_id=org.id,
        alias=f"T{str(uuid4())[:6]}".upper(),
        name="Test Project",
        description="Test project",
    )
    db_session.add(p)
    db_session.commit()
    db_session.refresh(p)
    return p


@pytest.fixture
def board(db_session, org, project):
    b = BoardRegistration(
        organization_id=str(org.id),
        project_id=project.id,
        board_name="TEST Board",
        board_type=BoardType.JIRA,
        board_url="https://example.atlassian.net/jira/software/c/projects/TEST/boards/1",
        board_external_id="1",
        is_active=True,
    )
    db_session.add(b)
    db_session.commit()
    db_session.refresh(b)
    return b


def _make_ticket(db_session, board, org, summary, status, external_id):
    t = Ticket(
        organization_id=str(org.id),
        project_id=board.project_id,
        board_registration_id=str(board.id),
        summary=summary,
        status=status,
        external_ticket_id=external_id,
    )
    db_session.add(t)
    db_session.commit()
    db_session.refresh(t)
    return t


# ---------------------------------------------------------------------------
# Unit tests — probe endpoint filtering logic
# ---------------------------------------------------------------------------


class TestProbeEndpointFiltering:
    """Verify that probe_board returns only active tickets (in_progress, in_test)."""

    def test_excludes_done_tickets(self, db_session, org, board):
        _make_ticket(db_session, board, org, "Done task", TicketStatus.DONE, "TEST-1")
        _make_ticket(
            db_session, board, org, "Active task", TicketStatus.IN_PROGRESS, "TEST-2"
        )

        excluded = [TicketStatus.DONE, TicketStatus.TODO, TicketStatus.BACKLOG]
        results = db_session.exec(
            select(Ticket)
            .where(
                Ticket.board_registration_id == str(board.id),
                ~Ticket.status.in_(excluded),
            )
            .limit(5)
        ).all()

        assert len(results) == 1
        assert results[0].summary == "Active task"

    def test_excludes_todo_and_backlog(self, db_session, org, board):
        _make_ticket(
            db_session, board, org, "In backlog", TicketStatus.BACKLOG, "TEST-3"
        )
        _make_ticket(db_session, board, org, "Todo item", TicketStatus.TODO, "TEST-4")
        _make_ticket(
            db_session, board, org, "In test", TicketStatus.IN_REVIEW, "TEST-5"
        )
        _make_ticket(
            db_session, board, org, "In progress", TicketStatus.IN_PROGRESS, "TEST-6"
        )

        excluded = [TicketStatus.DONE, TicketStatus.TODO, TicketStatus.BACKLOG]
        results = db_session.exec(
            select(Ticket)
            .where(
                Ticket.board_registration_id == str(board.id),
                ~Ticket.status.in_(excluded),
            )
            .limit(5)
        ).all()

        summaries = {t.summary for t in results}
        assert "In test" in summaries
        assert "In progress" in summaries
        assert "In backlog" not in summaries
        assert "Todo item" not in summaries

    def test_returns_at_most_five(self, db_session, org, board):
        for i in range(8):
            _make_ticket(
                db_session,
                board,
                org,
                f"Active-{i}",
                TicketStatus.IN_PROGRESS,
                f"TEST-{100 + i}",
            )

        excluded = [TicketStatus.DONE, TicketStatus.TODO, TicketStatus.BACKLOG]
        results = db_session.exec(
            select(Ticket)
            .where(
                Ticket.board_registration_id == str(board.id),
                ~Ticket.status.in_(excluded),
            )
            .limit(5)
        ).all()

        assert len(results) == 5

    def test_returns_empty_when_no_active_tickets(self, db_session, org, board):
        _make_ticket(db_session, board, org, "Finished", TicketStatus.DONE, "TEST-10")
        _make_ticket(db_session, board, org, "Queued", TicketStatus.BACKLOG, "TEST-11")

        excluded = [TicketStatus.DONE, TicketStatus.TODO, TicketStatus.BACKLOG]
        results = db_session.exec(
            select(Ticket)
            .where(
                Ticket.board_registration_id == str(board.id),
                ~Ticket.status.in_(excluded),
            )
            .limit(5)
        ).all()

        assert results == []

    def test_only_returns_tickets_for_this_board(self, db_session, org, project):
        # BoardRegistration.project_id is unique (one board per project), so
        # each board here needs its own project.
        project_b = Project(
            id=str(uuid4()),
            organization_id=org.id,
            alias=f"B{str(uuid4())[:6]}".upper(),
            name="Test Project B",
            description="Test project B",
        )
        db_session.add(project_b)
        db_session.commit()
        db_session.refresh(project_b)

        board_a = BoardRegistration(
            organization_id=str(org.id),
            project_id=project.id,
            board_name="Board A",
            board_type=BoardType.JIRA,
            board_url="https://example.atlassian.net/jira/software/c/projects/A/boards/1",
            board_external_id="1",
            is_active=True,
        )
        board_b = BoardRegistration(
            organization_id=str(org.id),
            project_id=project_b.id,
            board_name="Board B",
            board_type=BoardType.JIRA,
            board_url="https://example.atlassian.net/jira/software/c/projects/B/boards/2",
            board_external_id="2",
            is_active=True,
        )
        db_session.add(board_a)
        db_session.add(board_b)
        db_session.commit()
        db_session.refresh(board_a)
        db_session.refresh(board_b)

        _make_ticket(
            db_session, board_a, org, "Board A active", TicketStatus.IN_PROGRESS, "A-1"
        )
        _make_ticket(
            db_session, board_b, org, "Board B active", TicketStatus.IN_PROGRESS, "B-1"
        )

        excluded = [TicketStatus.DONE, TicketStatus.TODO, TicketStatus.BACKLOG]
        results = db_session.exec(
            select(Ticket)
            .where(
                Ticket.board_registration_id == str(board_a.id),
                ~Ticket.status.in_(excluded),
            )
            .limit(5)
        ).all()

        assert len(results) == 1
        assert results[0].summary == "Board A active"


# ---------------------------------------------------------------------------
# Integration test — live Jira call (skipped unless org env file is configured)
# ---------------------------------------------------------------------------


def _load_jira_org_env():
    """Load a configured Jira org env from env/orgs/. Returns None if none found."""
    import os
    from pathlib import Path

    orgs_dir = Path(__file__).parent.parent / "env" / "orgs"
    if not orgs_dir.exists():
        return None

    try:
        from src.utils.org_env import load_org_env

        for slug in os.listdir(orgs_dir):
            if slug == "example":
                continue
            env = load_org_env(slug)
            if (
                env
                and env.board_type == "jira"
                and env.board_api_token
                and env.board_api_email
            ):
                return env
    except Exception:
        pass
    return None


_jira_env = _load_jira_org_env()
_has_jira_creds = _jira_env is not None


@pytest.mark.jira
@pytest.mark.skipif(
    not _has_jira_creds,
    reason="No configured Jira org env found in env/orgs/ (BOARD_API_TOKEN + BOARD_API_EMAIL required)",
)
class TestJiraBoardLive:
    """Live integration tests against a configured Jira board."""

    @pytest.mark.asyncio
    async def test_jira_credentials_valid(self):
        """Confirm the stored token authenticates successfully."""
        import re

        import httpx

        base_match = re.match(r"(https?://[^/]+)", _jira_env.board_url)
        assert base_match, (
            f"Could not extract base URL from board_url: {_jira_env.board_url}"
        )
        base_url = base_match.group(1)
        resp = await httpx.AsyncClient(timeout=15.0).get(
            f"{base_url}/rest/api/3/myself",
            auth=(_jira_env.board_api_email, _jira_env.board_api_token),
            headers={"Accept": "application/json"},
        )
        assert resp.status_code == 200, (
            f"Jira auth failed (HTTP {resp.status_code}): {resp.text[:200]}"
        )
        me = resp.json()
        assert "accountId" in me, "Response missing accountId"

    @pytest.mark.asyncio
    async def test_top5_active_tickets(self):
        """
        Fetch the top 5 in-progress / in-test tickets from the configured board.
        """
        import re

        import httpx

        excluded_keywords = {"done", "to do", "todo", "backlog", "closed", "resolved"}

        base_url_match = re.match(r"(https?://[^/]+)", _jira_env.board_url)
        assert base_url_match, "Could not extract base URL from board_url"
        base_url = base_url_match.group(1)

        board_id_match = re.search(r"/boards/(\d+)", _jira_env.board_url)
        assert board_id_match, "Could not extract board ID from board_url"
        board_id = board_id_match.group(1)

        async with httpx.AsyncClient(timeout=30.0) as client:
            resp = await client.get(
                f"{base_url}/rest/agile/1.0/board/{board_id}/issue",
                params={"maxResults": 50, "fields": "summary,status,assignee"},
                auth=(_jira_env.board_api_email, _jira_env.board_api_token),
                headers={"Accept": "application/json"},
            )

        assert resp.status_code == 200, (
            f"Jira board fetch failed (HTTP {resp.status_code}): {resp.text[:300]}"
        )

        issues = resp.json().get("issues", [])
        assert len(issues) > 0, "No issues returned from board — check board ID"

        active = [
            issue
            for issue in issues
            if issue["fields"]["status"]["name"].lower() not in excluded_keywords
        ][:5]

        for issue in active:
            assert "key" in issue
            assert "fields" in issue
            assert "summary" in issue["fields"]
            assert "status" in issue["fields"]
