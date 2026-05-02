"""Unit tests for AzureUsers.get_modified_users() fix.

Verifies that the /users/delta endpoint is called WITHOUT $filter
(which caused HTTP 400 Request_UnsupportedQuery) and that results
are filtered locally by createdDateTime instead.
"""
import pytest
from unittest.mock import AsyncMock, patch, MagicMock

from flowtask.components.AzureUsers import AzureUsers


# --- Fixtures ---

DELTA_RESPONSE_USERS = [
    {
        "id": "user-1",
        "displayName": "Recent User",
        "createdDateTime": "2025-06-15T10:00:00Z",
    },
    {
        "id": "user-2",
        "displayName": "Old User",
        "createdDateTime": "2024-01-01T00:00:00Z",
    },
    {
        "id": "user-3",
        "displayName": "Modified User No Date",
        # No createdDateTime — delta returned it because it was modified
    },
    {
        "id": "user-4",
        "displayName": "Boundary User",
        "createdDateTime": "2025-06-01T00:00:00Z",
    },
]


def _make_component() -> AzureUsers:
    """Create a minimal AzureUsers instance with mocked internals."""
    with patch.object(AzureUsers, "__init__", lambda self, **kw: None):
        comp = AzureUsers.__new__(AzureUsers)
    comp.users_info = "https://graph.microsoft.com/v1.0/users"
    comp.method = "GET"
    return comp


# --- Tests ---

pytestmark = pytest.mark.asyncio


class TestGetModifiedUsersNoFilter:
    """The delta URL must NOT contain $filter=createdDateTime."""

    async def test_delta_url_has_no_filter(self):
        comp = _make_component()
        captured_urls = []

        async def fake_fetch(url: str) -> list:
            captured_urls.append(url)
            return DELTA_RESPONSE_USERS

        comp._fetch_all_pages = fake_fetch

        await comp.get_modified_users("2025-06-01T00:00:00Z")

        assert len(captured_urls) == 1
        url = captured_urls[0]
        assert url.endswith("/delta"), f"Expected URL ending with /delta, got: {url}"
        assert "$filter" not in url, (
            f"Delta URL must NOT contain $filter (causes HTTP 400): {url}"
        )


class TestGetModifiedUsersLocalFiltering:
    """Results are filtered locally by createdDateTime >= since."""

    async def test_filters_old_users(self):
        comp = _make_component()
        comp._fetch_all_pages = AsyncMock(return_value=DELTA_RESPONSE_USERS)

        result = await comp.get_modified_users("2025-06-01T00:00:00Z")

        result_ids = {u["id"] for u in result}
        # user-1 (2025-06-15) — after cutoff, included
        assert "user-1" in result_ids
        # user-2 (2024-01-01) — before cutoff, excluded
        assert "user-2" not in result_ids
        # user-3 (no date) — included because delta returned it
        assert "user-3" in result_ids
        # user-4 (2025-06-01) — exactly at cutoff, included (>=)
        assert "user-4" in result_ids

    async def test_result_count(self):
        comp = _make_component()
        comp._fetch_all_pages = AsyncMock(return_value=DELTA_RESPONSE_USERS)

        result = await comp.get_modified_users("2025-06-01T00:00:00Z")
        assert len(result) == 3  # user-1, user-3, user-4

    async def test_empty_delta_response(self):
        comp = _make_component()
        comp._fetch_all_pages = AsyncMock(return_value=[])

        result = await comp.get_modified_users("2025-06-01T00:00:00Z")
        assert result == []


class TestMergeUsers:
    """_merge_users deduplicates by id, modified takes precedence."""

    def test_deduplication(self):
        comp = _make_component()
        created = [
            {"id": "u1", "displayName": "Created Version"},
            {"id": "u2", "displayName": "Only Created"},
        ]
        modified = [
            {"id": "u1", "displayName": "Modified Version"},
            {"id": "u3", "displayName": "Only Modified"},
        ]
        result = comp._merge_users(created, modified)
        by_id = {u["id"]: u for u in result}

        assert len(by_id) == 3
        assert by_id["u1"]["displayName"] == "Modified Version"
        assert by_id["u2"]["displayName"] == "Only Created"
        assert by_id["u3"]["displayName"] == "Only Modified"
