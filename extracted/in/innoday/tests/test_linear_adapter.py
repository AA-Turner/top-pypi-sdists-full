"""Tests for LinearBoardAdapter."""

from datetime import datetime
from unittest.mock import AsyncMock, MagicMock

import pytest

from src.domain.board import BoardRegistration, BoardType


def make_registration(team_id="team-abc"):
    reg = MagicMock(spec=BoardRegistration)
    reg.id = "reg-1"
    reg.board_external_id = team_id
    reg.board_type = BoardType.LINEAR
    reg.organization_id = "org-1"
    reg.board_name = "Engineering"
    return reg


def make_linear_issue(
    identifier="ENG-1",
    title="Fix bug",
    state_name="In Progress",
    priority=2,
    parent_id=None,
    labels=None,
):
    issue = {
        "id": f"issue-{identifier}",
        "identifier": identifier,
        "title": title,
        "description": "Some description",
        "state": {"name": state_name},
        "priority": priority,
        "url": f"https://linear.app/eng/issue/{identifier}",
        "assignee": {"name": "Alice"},
        "parent": {"id": parent_id, "identifier": "ENG-0"} if parent_id else None,
        "updatedAt": "2026-05-01T10:00:00.000Z",
    }
    if labels is not None:
        issue["labels"] = {"nodes": [{"name": name} for name in labels]}
    return issue


@pytest.mark.asyncio
async def test_initialize_fetches_workflow_states():
    from src.adapters.linear_adapter import LinearBoardAdapter
    from src.api.linear_api import LinearAPI

    api = MagicMock(spec=LinearAPI)
    api.get_team = AsyncMock(return_value={"id": "team-abc", "name": "Engineering"})
    api.get_team_workflow_states = AsyncMock(
        return_value=[
            {"id": "state-1", "name": "Todo", "type": "unstarted"},
            {"id": "state-2", "name": "In Progress", "type": "started"},
            {"id": "state-3", "name": "Done", "type": "completed"},
        ]
    )

    adapter = LinearBoardAdapter(api, make_registration())
    await adapter.initialize("lin_api_test")

    assert adapter._initialized is True
    assert "Todo" in adapter.state_name_to_id
    assert adapter.state_name_to_id["In Progress"] == "state-2"
    assert adapter.workflow_states["state-3"] == "Done"


@pytest.mark.asyncio
async def test_get_tickets_maps_issues_to_tickets():
    from src.adapters.linear_adapter import LinearBoardAdapter
    from src.api.linear_api import LinearAPI
    from src.domain.ticket import TicketStatus

    api = MagicMock(spec=LinearAPI)
    api.get_team_issues = AsyncMock(
        return_value=[make_linear_issue("ENG-1", "Fix bug", "In Progress", 2)]
    )

    adapter = LinearBoardAdapter(api, make_registration())
    adapter._initialized = True

    tickets = await adapter.get_tickets("team-abc")

    assert len(tickets) == 1
    t = tickets[0]
    assert t.summary == "Fix bug"
    assert t.external_ticket_id == "ENG-1"
    assert t.status == TicketStatus.IN_PROGRESS
    assert t.priority == "high"
    assert t.source_platform == "linear"
    assert t.url == "https://linear.app/eng/issue/ENG-1"
    assert t.assignee == "Alice"


@pytest.mark.asyncio
async def test_get_tickets_with_since_passes_updated_after():
    from src.adapters.linear_adapter import LinearBoardAdapter
    from src.api.linear_api import LinearAPI

    api = MagicMock(spec=LinearAPI)
    api.get_team_issues = AsyncMock(return_value=[])

    adapter = LinearBoardAdapter(api, make_registration())
    adapter._initialized = True

    since = datetime(2026, 5, 1)
    await adapter.get_tickets("team-abc", since=since)

    api.get_team_issues.assert_called_once_with("team-abc", updated_after=since)


@pytest.mark.asyncio
async def test_issue_to_ticket_maps_priority():
    from src.adapters.linear_adapter import LinearBoardAdapter
    from src.api.linear_api import LinearAPI

    api = MagicMock(spec=LinearAPI)
    adapter = LinearBoardAdapter(api, make_registration())

    assert adapter._map_priority(0) == "no_priority"
    assert adapter._map_priority(1) == "urgent"
    assert adapter._map_priority(2) == "high"
    assert adapter._map_priority(3) == "medium"
    assert adapter._map_priority(4) == "low"


@pytest.mark.asyncio
async def test_get_tickets_maps_parent_external_id():
    from src.adapters.linear_adapter import LinearBoardAdapter
    from src.api.linear_api import LinearAPI

    api = MagicMock(spec=LinearAPI)
    issue = make_linear_issue("ENG-2", parent_id="parent-issue-id")
    api.get_team_issues = AsyncMock(return_value=[issue])

    adapter = LinearBoardAdapter(api, make_registration())
    adapter._initialized = True

    tickets = await adapter.get_tickets("team-abc")
    assert tickets[0].parent_external_id == "ENG-0"


@pytest.mark.asyncio
async def test_update_ticket_status_resolves_state_id():
    from src.adapters.linear_adapter import LinearBoardAdapter
    from src.api.linear_api import LinearAPI
    from src.domain.ticket import Ticket, TicketStatus

    api = MagicMock(spec=LinearAPI)
    api.update_issue = AsyncMock(
        return_value=make_linear_issue("ENG-1", state_name="Done", priority=0)
    )

    adapter = LinearBoardAdapter(api, make_registration())
    adapter._initialized = True
    adapter.state_name_to_id = {"Done": "state-done-id", "Todo": "state-todo-id"}

    ticket = MagicMock(spec=Ticket)
    ticket.external_ticket_id = "ENG-1"
    ticket.status = TicketStatus.IN_PROGRESS

    result = await adapter.update_ticket_status(ticket, "Done")

    api.update_issue.assert_called_once_with("ENG-1", {"stateId": "state-done-id"})
    assert result.status == TicketStatus.DONE


@pytest.mark.asyncio
async def test_validate_connection_returns_true_when_team_found():
    from src.adapters.linear_adapter import LinearBoardAdapter
    from src.api.linear_api import LinearAPI

    api = MagicMock(spec=LinearAPI)
    api.get_team = AsyncMock(return_value={"id": "team-abc", "name": "Engineering"})

    adapter = LinearBoardAdapter(api, make_registration())
    result = await adapter.validate_connection()

    assert result is True


@pytest.mark.asyncio
async def test_validate_connection_returns_false_on_exception():
    from src.adapters.linear_adapter import LinearBoardAdapter
    from src.api.linear_api import LinearAPI

    api = MagicMock(spec=LinearAPI)
    api.get_team = AsyncMock(side_effect=Exception("Network error"))

    adapter = LinearBoardAdapter(api, make_registration())
    result = await adapter.validate_connection()

    assert result is False


@pytest.mark.asyncio
async def test_initialize_resolves_stale_team_key_to_uuid():
    """
    Regression test: boards registered before register_board started
    resolving Linear team keys to UUIDs kept board_id as a short key
    ("UI"). initialize() must self-heal this via resolve_team_id_by_key,
    or every subsequent mutation 400s with "teamId must be a UUID".
    """
    from src.adapters.linear_adapter import LinearBoardAdapter
    from src.api.linear_api import LinearAPI

    api = MagicMock(spec=LinearAPI)
    api.resolve_team_id_by_key = AsyncMock(return_value="resolved-uuid-1234")
    api.get_team = AsyncMock(return_value={"id": "resolved-uuid-1234", "name": "UI"})
    api.get_team_workflow_states = AsyncMock(return_value=[])

    adapter = LinearBoardAdapter(api, make_registration(team_id="UI"))
    await adapter.initialize("lin_api_test")

    api.resolve_team_id_by_key.assert_called_once_with("UI")
    assert adapter.board_id == "resolved-uuid-1234"
    api.get_team.assert_called_once_with("resolved-uuid-1234")


@pytest.mark.asyncio
async def test_initialize_skips_resolution_when_already_uuid():
    from src.adapters.linear_adapter import LinearBoardAdapter
    from src.api.linear_api import LinearAPI

    api = MagicMock(spec=LinearAPI)
    api.resolve_team_id_by_key = AsyncMock()
    api.get_team = AsyncMock(
        return_value={"id": "d5bbb23a-95fe-4d3a-bf61-85d0a606e211"}
    )
    api.get_team_workflow_states = AsyncMock(return_value=[])

    adapter = LinearBoardAdapter(
        api, make_registration(team_id="d5bbb23a-95fe-4d3a-bf61-85d0a606e211")
    )
    await adapter.initialize("lin_api_test")

    api.resolve_team_id_by_key.assert_not_called()


@pytest.mark.asyncio
async def test_create_ticket_uses_resolved_board_id_not_stale_parameter():
    """
    Regression test: create_ticket must use self.board_id (corrected by
    initialize()'s self-heal), not the board_id parameter callers pass --
    board_ticket_creation_service.py always passes the raw, unresolved
    board_registration.board_external_id. Confirmed live: without this fix,
    a resolved adapter still sent the stale key to Linear's create-issue
    mutation and 400'd.
    """
    from src.adapters.linear_adapter import LinearBoardAdapter
    from src.api.linear_api import LinearAPI

    api = MagicMock(spec=LinearAPI)
    api.create_issue = AsyncMock(return_value=make_linear_issue("ENG-9"))

    adapter = LinearBoardAdapter(api, make_registration(team_id="UI"))
    adapter._initialized = True
    adapter.board_id = "resolved-uuid-1234"  # simulate initialize()'s self-heal

    await adapter.create_ticket("UI", {"summary": "New ticket"})

    api.create_issue.assert_called_once_with(
        "resolved-uuid-1234", {"summary": "New ticket"}
    )


# ---------------------------------------------------------------------------
# Release auto-discovery from semver-shaped Linear labels (PF-372)
# ---------------------------------------------------------------------------


class TestReleaseFromLabels:
    """Unit tests for the _release_from_labels helper.

    Version grammar matches blastoff's SemanticVersion (v-prefixed
    vMAJOR.MINOR.PATCH[-pre[.N]]) so a discovered release is one the release
    engine / InnoDayVersionStore can also parse. Bare 1.0.0, v1.0, and
    uppercase V1.0.0 are intentionally rejected.
    """

    def test_picks_semver_label(self):
        from src.adapters.linear_adapter import _release_from_labels

        assert _release_from_labels(["Bug", "v1.0.0", "Feature"]) == "v1.0.0"

    def test_accepts_prerelease(self):
        from src.adapters.linear_adapter import _release_from_labels

        assert _release_from_labels(["v1.2.3-beta"]) == "v1.2.3-beta"
        assert _release_from_labels(["v1.2.3-rc.2"]) == "v1.2.3-rc.2"

    def test_no_semver_label_returns_none(self):
        from src.adapters.linear_adapter import _release_from_labels

        assert _release_from_labels(["Bug", "Feature", "Needs Review"]) is None

    def test_empty_or_blank_labels(self):
        from src.adapters.linear_adapter import _release_from_labels

        assert _release_from_labels([]) is None
        assert _release_from_labels(["", "   "]) is None

    def test_non_semver_shapes_rejected(self):
        from src.adapters.linear_adapter import _release_from_labels

        # bare (no v), partial, and uppercase-V are not blastoff-parseable
        assert _release_from_labels(["1.0.0"]) is None
        assert _release_from_labels(["v1.0"]) is None
        assert _release_from_labels(["V1.0.0"]) is None

    def test_first_semver_label_wins(self):
        from src.adapters.linear_adapter import _release_from_labels

        assert _release_from_labels(["v2.0.0", "v1.0.0"]) == "v2.0.0"


@pytest.mark.asyncio
async def test_issue_to_ticket_sets_release_from_semver_label():
    from src.adapters.linear_adapter import LinearBoardAdapter
    from src.api.linear_api import LinearAPI

    api = MagicMock(spec=LinearAPI)
    api.get_team_issues = AsyncMock(
        return_value=[make_linear_issue("ENG-1", labels=["Feature", "v1.0.0"])]
    )

    adapter = LinearBoardAdapter(api, make_registration())
    adapter._initialized = True

    tickets = await adapter.get_tickets("team-abc")
    assert tickets[0].release == "v1.0.0"


@pytest.mark.asyncio
async def test_issue_to_ticket_release_none_without_semver_label():
    from src.adapters.linear_adapter import LinearBoardAdapter
    from src.api.linear_api import LinearAPI

    api = MagicMock(spec=LinearAPI)
    # no labels key at all, and a labelled-but-non-semver issue
    api.get_team_issues = AsyncMock(
        return_value=[
            make_linear_issue("ENG-1"),
            make_linear_issue("ENG-2", labels=["Bug"]),
        ]
    )

    adapter = LinearBoardAdapter(api, make_registration())
    adapter._initialized = True

    tickets = await adapter.get_tickets("team-abc")
    assert tickets[0].release is None
    assert tickets[1].release is None


@pytest.mark.asyncio
async def test_issue_to_ticket_uses_linears_timestamps_not_now():
    """The bug that made every closed Linear ticket look freshly completed.

    `TimestampMixin` defaults `updated_at` to `now()`. The adapter never
    overwrote it, so `board_sync_service._ticket_to_dict` emitted
    `fields.updated = <sync time>`, `_completed_at_from` fell back to it, and
    every DONE ticket was stored as completed at the instant of the sync. The
    summary engine reads `completed_at` inside the window as a real terminal
    transition, so a project's whole closed backlog reported as work finished
    this week. Measured on BPAI's first import: 114 of 175 tickets stamped
    completed within the same microsecond.
    """
    from src.adapters.linear_adapter import LinearBoardAdapter
    from src.api.linear_api import LinearAPI

    api = MagicMock(spec=LinearAPI)
    adapter = LinearBoardAdapter(api, make_registration())

    issue = make_linear_issue(state_name="Done")
    issue["updatedAt"] = "2026-06-02T09:15:00.000Z"
    issue["completedAt"] = "2026-06-01T18:30:00.000Z"

    ticket = adapter._issue_to_ticket(issue)

    assert ticket.updated_at == datetime(2026, 6, 2, 9, 15)
    assert ticket.completed_at == datetime(2026, 6, 1, 18, 30)


@pytest.mark.asyncio
async def test_an_unfinished_issue_has_no_completion_time():
    from src.adapters.linear_adapter import LinearBoardAdapter
    from src.api.linear_api import LinearAPI

    api = MagicMock(spec=LinearAPI)
    adapter = LinearBoardAdapter(api, make_registration())

    ticket = adapter._issue_to_ticket(make_linear_issue(state_name="In Progress"))

    assert ticket.completed_at is None


@pytest.mark.asyncio
async def test_a_missing_updatedAt_leaves_the_default_rather_than_none():
    """`updated_at` is non-Optional, so it must never be written as None.

    Passing `None` through would violate the column and, on the test fixtures'
    permissive schema, insert a NULL that production rejects.
    """
    from src.adapters.linear_adapter import LinearBoardAdapter
    from src.api.linear_api import LinearAPI

    api = MagicMock(spec=LinearAPI)
    adapter = LinearBoardAdapter(api, make_registration())

    issue = make_linear_issue()
    del issue["updatedAt"]

    ticket = adapter._issue_to_ticket(issue)

    assert ticket.updated_at is not None


def test_the_issue_query_asks_for_completedAt():
    """The field has to be *requested* — GraphQL returns only what you name.

    Without it in `_ISSUE_FIELDS` the adapter reads `completedAt` from a dict
    that never contains it, silently falls back, and the bug above returns
    while every test on the mapping still passes.
    """
    from src.api.linear_api import _ISSUE_FIELDS

    assert "completedAt" in _ISSUE_FIELDS
    assert "updatedAt" in _ISSUE_FIELDS
