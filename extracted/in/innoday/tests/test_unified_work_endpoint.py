"""Tests for GET /organizations/{org_id}/work unified endpoint."""

from datetime import datetime
from unittest.mock import MagicMock, patch

import pytest


def make_ticket(
    id=1,
    summary="Fix bug",
    status="in progress",
    source_platform="jira",
    priority="high",
    url="https://jira.example.com/ENG-1",
    external_ticket_id="ENG-1",
    organization_id="org-1",
):
    t = MagicMock()
    t.id = id
    t.summary = summary
    t.description = "desc"
    t.status = MagicMock()
    t.status.value = status
    t.source_platform = source_platform
    t.priority = priority
    t.url = url
    t.external_ticket_id = external_ticket_id
    t.assignee = "alice"
    t.parent_external_id = None
    t.created_at = datetime(2026, 5, 1)
    t.updated_at = datetime(2026, 5, 10)
    t.organization_id = organization_id
    return t


def make_repo_issue(
    id="issue-uuid-1",
    title="Open GitHub issue",
    is_open=True,
    github_url="https://github.com/org/repo/issues/1",
    github_issue_id=1,
):
    i = MagicMock()
    i.id = id
    i.title = title
    i.body = "issue body"
    i.is_open = is_open
    i.github_url = github_url
    i.github_issue_id = github_issue_id
    i.created_at = datetime(2026, 5, 1)
    i.updated_at = datetime(2026, 5, 10)
    return i


def _mock_user():
    u = MagicMock()
    u.id = "user-1"
    return u


@pytest.mark.asyncio
async def test_unified_work_returns_tickets():
    """get_unified_work() returns tickets as UnifiedWorkItem objects."""
    from src.routers.tickets import get_unified_work

    mock_session = MagicMock()
    mock_org = MagicMock()
    mock_session.get.return_value = mock_org

    tickets = [make_ticket()]

    with (
        patch("src.routers.tickets.require_org_role"),
        patch("src.routers.tickets.get_org_tickets", return_value=tickets),
        patch("src.routers.tickets.get_org_github_issues", return_value=[]),
    ):
        result = await get_unified_work(
            organization_id="org-1",
            current_user=_mock_user(),
            session=mock_session,
            limit=100,
            offset=0,
        )

    assert len(result) == 1
    assert result[0].type == "ticket"
    assert result[0].summary == "Fix bug"
    assert result[0].source_platform == "jira"
    assert result[0].priority == "high"


# ─── Filtering, ordering and bounding now happen in SQL ──────────────────────
#
# These used to patch out `get_org_tickets` and assert that the *endpoint*
# filtered the rows in Python. It no longer does — the query does — so a mocked
# loader proved nothing about the filter. They now run against a real session,
# which is what actually exercises the SQL.


def _real_ticket(session, org, project, **kw):
    from src.domain.ticket import Ticket, TicketStatus

    defaults = dict(
        summary="t",
        organization_id=org.id,
        project_id=project.id,
        status=TicketStatus.BACKLOG,
        source_platform="jira",
        priority="high",
        assignee="alice",
    )
    defaults.update(kw)
    t = Ticket(**defaults)
    session.add(t)
    session.commit()
    session.refresh(t)
    return t


class TestQueryLevelFiltering:
    def test_filters_by_source_platform(self, db_session, org, project):
        from src.routers.tickets import get_org_tickets

        _real_ticket(db_session, org, project, source_platform="jira")
        _real_ticket(db_session, org, project, source_platform="linear")

        rows = get_org_tickets(db_session, org.id, source_platform="linear")
        assert [r.source_platform for r in rows] == ["linear"]

    def test_filters_by_priority(self, db_session, org, project):
        from src.routers.tickets import get_org_tickets

        _real_ticket(db_session, org, project, priority="urgent")
        _real_ticket(db_session, org, project, priority="low")

        rows = get_org_tickets(db_session, org.id, priority="urgent")
        assert [r.priority for r in rows] == ["urgent"]

    def test_filters_by_assignee(self, db_session, org, project):
        from src.routers.tickets import get_org_tickets

        _real_ticket(db_session, org, project, assignee="alice")
        _real_ticket(db_session, org, project, assignee="bob")

        rows = get_org_tickets(db_session, org.id, assignee="bob")
        assert [r.assignee for r in rows] == ["bob"]

    def test_unknown_source_platform_matches_null_and_empty(
        self, db_session, org, project
    ):
        """ "unknown" is the API's label for a ticket with no platform recorded."""
        from src.routers.tickets import get_org_tickets

        _real_ticket(db_session, org, project, source_platform=None)
        _real_ticket(db_session, org, project, source_platform="")
        _real_ticket(db_session, org, project, source_platform="jira")

        rows = get_org_tickets(db_session, org.id, source_platform="unknown")
        assert len(rows) == 2
        assert all(not r.source_platform for r in rows)

    def test_soft_deleted_tickets_are_excluded(self, db_session, org, project):
        from datetime import timezone

        from src.routers.tickets import get_org_tickets

        _real_ticket(db_session, org, project, summary="live")
        _real_ticket(
            db_session,
            org,
            project,
            summary="gone",
            deleted_at=datetime.now(timezone.utc),
        )

        rows = get_org_tickets(db_session, org.id)
        assert [r.summary for r in rows] == ["live"]

    def test_max_rows_bounds_the_result(self, db_session, org, project):
        from src.routers.tickets import get_org_tickets

        for i in range(5):
            _real_ticket(db_session, org, project, summary=f"t{i}")

        assert len(get_org_tickets(db_session, org.id, max_rows=2)) == 2

    def test_newest_first_orders_by_updated_at_desc(self, db_session, org, project):
        from src.routers.tickets import get_org_tickets

        old = _real_ticket(
            db_session, org, project, summary="old", updated_at=datetime(2026, 1, 1)
        )
        new = _real_ticket(
            db_session, org, project, summary="new", updated_at=datetime(2026, 6, 1)
        )

        rows = get_org_tickets(db_session, org.id, newest_first=True)
        assert [r.summary for r in rows] == ["new", "old"]
        assert rows[0].id == new.id and rows[1].id == old.id


class TestPageWindow:
    """Each source is capped at offset+limit — the most that can contribute."""

    @pytest.mark.asyncio
    async def test_each_source_is_bounded_to_the_window(self):
        from src.routers.tickets import get_unified_work

        mock_session = MagicMock()
        mock_session.get.return_value = MagicMock()
        captured = {}

        def fake_tickets(session, org_id, **kw):
            captured["tickets"] = kw
            return []

        def fake_issues(session, org_id, **kw):
            captured["issues"] = kw
            return []

        with (
            patch("src.routers.tickets.require_org_role"),
            patch("src.routers.tickets.get_org_tickets", side_effect=fake_tickets),
            patch("src.routers.tickets.get_org_github_issues", side_effect=fake_issues),
        ):
            await get_unified_work(
                organization_id="org-1",
                current_user=_mock_user(),
                session=mock_session,
                limit=25,
                offset=50,
            )

        assert captured["tickets"]["max_rows"] == 75, "offset + limit"
        assert captured["issues"]["max_rows"] == 75
        assert captured["tickets"]["newest_first"] is True
        assert captured["issues"]["newest_first"] is True

    @pytest.mark.asyncio
    async def test_filters_are_pushed_down_not_applied_in_python(self):
        from src.routers.tickets import get_unified_work

        mock_session = MagicMock()
        mock_session.get.return_value = MagicMock()
        captured = {}

        def fake_tickets(session, org_id, **kw):
            captured.update(kw)
            return []

        with (
            patch("src.routers.tickets.require_org_role"),
            patch("src.routers.tickets.get_org_tickets", side_effect=fake_tickets),
            patch("src.routers.tickets.get_org_github_issues", return_value=[]),
        ):
            await get_unified_work(
                organization_id="org-1",
                source_platform="linear",
                priority="urgent",
                assignee="bob",
                current_user=_mock_user(),
                session=mock_session,
                limit=10,
                offset=0,
            )

        assert captured["source_platform"] == "linear"
        assert captured["priority"] == "urgent"
        assert captured["assignee"] == "bob"

    @pytest.mark.asyncio
    async def test_repo_issues_are_skipped_when_a_ticket_only_filter_is_set(self):
        """A repo issue records no priority/assignee, so those exclude the branch."""
        from src.routers.tickets import get_unified_work

        mock_session = MagicMock()
        mock_session.get.return_value = MagicMock()
        issues_called = []

        with (
            patch("src.routers.tickets.require_org_role"),
            patch("src.routers.tickets.get_org_tickets", return_value=[]),
            patch(
                "src.routers.tickets.get_org_github_issues",
                side_effect=lambda *a, **k: issues_called.append(1) or [],
            ),
        ):
            await get_unified_work(
                organization_id="org-1",
                priority="urgent",
                current_user=_mock_user(),
                session=mock_session,
                limit=10,
                offset=0,
            )

        assert issues_called == [], "the repo-issue query should not have run"


@pytest.mark.asyncio
async def test_unified_work_item_has_required_fields():
    """UnifiedWorkItem has all required fields."""
    from src.routers.tickets import get_unified_work

    mock_session = MagicMock()
    mock_session.get.return_value = MagicMock()

    with (
        patch("src.routers.tickets.require_org_role"),
        patch("src.routers.tickets.get_org_tickets", return_value=[make_ticket()]),
        patch("src.routers.tickets.get_org_github_issues", return_value=[]),
    ):
        result = await get_unified_work(
            organization_id="org-1",
            current_user=_mock_user(),
            session=mock_session,
            limit=100,
            offset=0,
        )

    item = result[0]
    assert item.type == "ticket"
    assert item.id is not None
    assert item.summary is not None
    assert item.source_platform is not None
