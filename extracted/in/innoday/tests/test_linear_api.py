"""Tests for LinearAPI GraphQL client."""

from datetime import datetime
from unittest.mock import AsyncMock, patch

import pytest


@pytest.mark.asyncio
async def test_get_team_success():
    """get_team returns parsed team data when API responds correctly."""
    from src.api.linear_api import LinearAPI

    api = LinearAPI(api_key="lin_api_test123")
    mock_response = {
        "data": {
            "team": {
                "id": "team-abc",
                "name": "Engineering",
                "key": "ENG",
                "description": "Engineering team",
            }
        }
    }

    with patch.object(api, "_execute", new_callable=AsyncMock) as mock_exec:
        mock_exec.return_value = mock_response
        result = await api.get_team("team-abc")

    assert result["id"] == "team-abc"
    assert result["name"] == "Engineering"


@pytest.mark.asyncio
async def test_get_team_issues_basic():
    """get_team_issues returns list of issue dicts."""
    from src.api.linear_api import LinearAPI

    api = LinearAPI(api_key="lin_api_test123")
    mock_response = {
        "data": {
            "team": {
                "issues": {
                    "nodes": [
                        {
                            "id": "issue-1",
                            "identifier": "ENG-1",
                            "title": "Fix login bug",
                            "description": "Users cannot log in",
                            "state": {"name": "In Progress"},
                            "priority": 2,
                            "url": "https://linear.app/eng/issue/ENG-1",
                            "assignee": {"name": "Alice"},
                            "parent": None,
                            "updatedAt": "2026-05-01T10:00:00.000Z",
                        }
                    ],
                    "pageInfo": {"hasNextPage": False, "endCursor": None},
                }
            }
        }
    }

    with patch.object(api, "_execute", new_callable=AsyncMock) as mock_exec:
        mock_exec.return_value = mock_response
        results = await api.get_team_issues("team-abc")

    assert len(results) == 1
    assert results[0]["identifier"] == "ENG-1"
    assert results[0]["title"] == "Fix login bug"


@pytest.mark.asyncio
async def test_get_team_issues_with_since():
    """get_team_issues passes updatedAt filter when since is provided."""
    from src.api.linear_api import LinearAPI

    api = LinearAPI(api_key="lin_api_test123")
    since = datetime(2026, 5, 1, 0, 0, 0)

    with patch.object(api, "_execute", new_callable=AsyncMock) as mock_exec:
        mock_exec.return_value = {
            "data": {
                "team": {
                    "issues": {
                        "nodes": [],
                        "pageInfo": {"hasNextPage": False, "endCursor": None},
                    }
                }
            }
        }
        await api.get_team_issues("team-abc", updated_after=since)

    call_variables = mock_exec.call_args[0][1]
    assert "updatedAfter" in call_variables
    assert "2026-05-01" in call_variables["updatedAfter"]


@pytest.mark.asyncio
async def test_auth_header_format():
    """LinearAPI sends API key without Bearer prefix."""
    from src.api.linear_api import LinearAPI

    api = LinearAPI(api_key="lin_api_mykey123")
    assert api.headers["Authorization"] == "lin_api_mykey123"
    assert "Bearer" not in api.headers["Authorization"]


@pytest.mark.asyncio
async def test_create_issue():
    """create_issue posts mutation and returns issue dict."""
    from src.api.linear_api import LinearAPI

    api = LinearAPI(api_key="lin_api_test123")
    mock_response = {
        "data": {
            "issueCreate": {
                "success": True,
                "issue": {
                    "id": "new-issue-id",
                    "identifier": "ENG-42",
                    "title": "New task",
                    "description": "Do the thing",
                    "state": {"name": "Todo"},
                    "priority": 0,
                    "url": "https://linear.app/eng/issue/ENG-42",
                    "assignee": None,
                    "parent": None,
                    "updatedAt": "2026-05-13T00:00:00.000Z",
                },
            }
        }
    }

    with patch.object(api, "_execute", new_callable=AsyncMock) as mock_exec:
        mock_exec.return_value = mock_response
        result = await api.create_issue(
            "team-abc", {"title": "New task", "description": "Do the thing"}
        )

    assert result["identifier"] == "ENG-42"


@pytest.mark.asyncio
async def test_add_comment():
    """add_comment returns True on success."""
    from src.api.linear_api import LinearAPI

    api = LinearAPI(api_key="lin_api_test123")
    mock_response = {"data": {"commentCreate": {"success": True}}}

    with patch.object(api, "_execute", new_callable=AsyncMock) as mock_exec:
        mock_exec.return_value = mock_response
        result = await api.add_comment("issue-1", "Nice work!")

    assert result is True


class TestIsUuid:
    """
    Regression coverage for is_uuid(): a team's URL exposes its short key
    (e.g. "UI"), but Linear's GraphQL mutations require the real UUID.
    Confirmed live: a board registered from a /team/<key>/... URL sent the
    key as teamId to issueCreate, which 400'd with "Argument Validation
    Error" since teamId must be a UUID.
    """

    def test_uuid_is_recognized(self):
        from src.api.linear_api import is_uuid

        assert is_uuid("d5bbb23a-95fe-4d3a-bf61-85d0a606e211") is True

    def test_team_key_is_not_a_uuid(self):
        from src.api.linear_api import is_uuid

        assert is_uuid("UI") is False
        assert is_uuid("PF") is False


@pytest.mark.asyncio
async def test_resolve_team_id_by_key_returns_first_match():
    """resolve_team_id_by_key looks up a team's UUID from its short key."""
    from src.api.linear_api import LinearAPI

    api = LinearAPI(api_key="lin_api_test123")
    mock_response = {
        "data": {"teams": {"nodes": [{"id": "team-uuid-1", "key": "UI", "name": "UI"}]}}
    }

    with patch.object(api, "_execute", new_callable=AsyncMock) as mock_exec:
        mock_exec.return_value = mock_response
        result = await api.resolve_team_id_by_key("UI")

    assert result == "team-uuid-1"
    mock_exec.assert_called_once()
    _, variables = mock_exec.call_args[0]
    assert variables == {"key": "UI"}


@pytest.mark.asyncio
async def test_resolve_team_id_by_key_returns_none_when_no_match():
    from src.api.linear_api import LinearAPI

    api = LinearAPI(api_key="lin_api_test123")
    mock_response = {"data": {"teams": {"nodes": []}}}

    with patch.object(api, "_execute", new_callable=AsyncMock) as mock_exec:
        mock_exec.return_value = mock_response
        result = await api.resolve_team_id_by_key("NONEXISTENT")

    assert result is None
