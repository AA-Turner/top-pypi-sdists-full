"""
Tests for JiraBoardAdapter.

Two bugs fixed together here, both confirmed live against a real Jira Cloud
board:
1. _init_project_config read config["location"]["projectKey"], but the real
   /rest/agile/1.0/board/{id}/configuration response has the project key at
   location.key -- projectKey doesn't exist in the response shape at all, so
   self.project_key was always None.
2. _init_project_config also tried to persist the resolved key into
   self.board_registration.metadata["project_key"] = ... -- but
   BoardRegistration has no `metadata` field, so this silently resolved to
   SQLAlchemy's own Base.metadata class attribute and crashed with
   "'MetaData' object does not support item assignment" (swallowed by a
   bare except). Fixed by removing the broken persistence attempt --
   self.project_key already caches it for the adapter instance's lifetime.
"""

from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from src.adapters.jira_adapter import JiraBoardAdapter
from src.api.jira_api import JiraAPI
from src.domain.board import BoardRegistration, BoardType


def make_registration():
    reg = MagicMock(spec=BoardRegistration)
    reg.id = "reg-1"
    reg.board_external_id = "80"
    reg.board_type = BoardType.JIRA
    reg.organization_id = "org-1"
    reg.board_name = "TEST Board"
    return reg


@pytest.mark.asyncio
async def test_init_project_config_reads_location_key_not_project_key():
    api = MagicMock(spec=JiraAPI)
    adapter = JiraBoardAdapter(api, make_registration())

    with patch.object(
        adapter,
        "_get_board_config",
        new=AsyncMock(return_value={"location": {"key": "ITPT", "projectKey": None}}),
    ):
        await adapter._init_project_config()

    assert adapter.project_key == "ITPT"


@pytest.mark.asyncio
async def test_init_project_config_does_not_raise_on_plain_registration_mock():
    """
    Regression test: previously crashed with "'MetaData' object does not
    support item assignment" because board_registration.metadata isn't a
    real field -- it resolves to SQLAlchemy's internal Base.metadata. Using
    a bare MagicMock (no `metadata` attribute stubbed) would surface that
    crash immediately if the broken assignment were still present.
    """
    api = MagicMock(spec=JiraAPI)
    reg = make_registration()
    adapter = JiraBoardAdapter(api, reg)

    with patch.object(
        adapter,
        "_get_board_config",
        new=AsyncMock(return_value={"location": {"key": "ITPT"}}),
    ):
        await adapter._init_project_config()

    assert adapter.project_key == "ITPT"


@pytest.mark.asyncio
async def test_create_ticket_uses_explicit_project_key_over_cached():
    api = MagicMock(spec=JiraAPI)
    # Basic Auth mode: adapter._is_oauth_mode() checks self.api.auth is None.
    api.auth = ("me@example.com", "token123")
    api.base_url = "https://example.atlassian.net"
    api.headers = {"Accept": "application/json"}
    api.create_ticket = AsyncMock(return_value=MagicMock())
    adapter = JiraBoardAdapter(api, make_registration())
    adapter.project_key = "CACHED"

    await adapter.create_ticket("80", {"summary": "New", "project_key": "EXPLICIT"})

    api.create_ticket.assert_called_once()
    assert api.create_ticket.call_args.kwargs["project_key"] == "EXPLICIT"


@pytest.mark.asyncio
async def test_create_ticket_falls_back_to_cached_project_key():
    """
    Regression test: when no explicit project_key is passed (the normal
    case -- board_ticket_creation_service.py only sets it when the caller
    provided one, since board_external_id is a numeric board ID like "80",
    not a project key like "ITPT"), the adapter must fall back to its own
    resolved self.project_key rather than raising or using a board ID.
    """
    api = MagicMock(spec=JiraAPI)
    # Basic Auth mode: adapter._is_oauth_mode() checks self.api.auth is None.
    api.auth = ("me@example.com", "token123")
    api.base_url = "https://example.atlassian.net"
    api.headers = {"Accept": "application/json"}
    api.create_ticket = AsyncMock(return_value=MagicMock())
    adapter = JiraBoardAdapter(api, make_registration())
    adapter.project_key = "ITPT"

    await adapter.create_ticket("80", {"summary": "New"})

    assert api.create_ticket.call_args.kwargs["project_key"] == "ITPT"


class TestJiraBoardAdapterOAuthPath:
    """
    JiraBoardAdapter's raw-httpx call sites (_get_board_config,
    _get_project_statuses, _get_issue, _update_issue, _get_transitions,
    _do_transition) each independently reach into self.api.auth /
    self.api.base_url. When the underlying JiraAPI is in OAuth mode, they
    must route through ensure_fresh_jira_token instead of the static
    Basic Auth tuple -- exercised here for _get_board_config since it's
    representative of the shared pattern across all 6 methods.
    """

    @pytest.mark.asyncio
    async def test_get_board_config_uses_bearer_token_in_oauth_mode(self):
        api = JiraAPI(access_token="access-abc", cloud_id="cloud-123")
        reg = make_registration()
        adapter = JiraBoardAdapter(api, reg)

        config_response = MagicMock(status_code=200)
        config_response.json.return_value = {"location": {"key": "ITPT"}}

        with (
            patch(
                "src.adapters.jira_adapter.ensure_fresh_jira_token",
                new=AsyncMock(return_value=("fresh-access-token", "cloud-123")),
            ),
            patch("httpx.AsyncClient.get", new_callable=AsyncMock) as mock_get,
        ):
            mock_get.return_value = config_response
            result = await adapter._get_board_config()

        assert result == {"location": {"key": "ITPT"}}
        call_kwargs = mock_get.call_args.kwargs
        assert call_kwargs["headers"]["Authorization"] == "Bearer fresh-access-token"
        called_url = mock_get.call_args.args[0]
        assert called_url.startswith("https://api.atlassian.com/ex/jira/cloud-123/")

    @pytest.mark.asyncio
    async def test_get_board_config_basic_auth_mode_makes_no_oauth_refresh_call(self):
        """Dual-mode: Basic Auth adapters must be completely unaffected --
        no extra DB calls, no attempt to refresh a token that doesn't
        exist for this board."""
        api = MagicMock(spec=JiraAPI)
        api.auth = ("me@example.com", "token123")
        api.base_url = "https://example.atlassian.net"
        api.headers = {"Accept": "application/json"}
        reg = make_registration()
        adapter = JiraBoardAdapter(api, reg)

        config_response = MagicMock(status_code=200)
        config_response.json.return_value = {"location": {"key": "ITPT"}}

        with (
            patch(
                "src.adapters.jira_adapter.ensure_fresh_jira_token",
                new=AsyncMock(),
            ) as mock_ensure_fresh,
            patch("httpx.AsyncClient.get", new_callable=AsyncMock) as mock_get,
        ):
            mock_get.return_value = config_response
            result = await adapter._get_board_config()

        assert result == {"location": {"key": "ITPT"}}
        mock_ensure_fresh.assert_not_called()
        call_kwargs = mock_get.call_args.kwargs
        assert call_kwargs["auth"] == ("me@example.com", "token123")


class TestJiraBoardAdapterDelegatedMethodsOAuthPath:
    """
    Unlike the six methods above (which build their own httpx calls inside
    the adapter and read (base_url, auth, headers) from
    _jira_request_context() directly), get_tickets/create_ticket/add_comment
    delegate straight to JiraAPI.get_tickets_by_board /
    JiraAPI.create_ticket / JiraAPI.add_comment, which build their *own*
    httpx calls reading self.base_url/self.auth/self.headers off the
    JiraAPI instance -- values fixed once at JiraAPI.__init__ time. In OAuth
    mode these three delegated calls previously bypassed
    ensure_fresh_jira_token entirely, so a sync running longer than the
    access token's lifetime (or started after the stored token already
    expired) would silently 401 even though board-config validation moments
    earlier succeeded. These tests prove the adapter refreshes the token
    and updates the underlying JiraAPI instance before delegating, so the
    actual outbound HTTP call carries the refreshed Bearer token, not the
    stale construction-time one.
    """

    @pytest.mark.asyncio
    async def test_get_tickets_refreshes_token_before_delegating_in_oauth_mode(self):
        api = JiraAPI(access_token="stale-access-token", cloud_id="cloud-123")
        adapter = JiraBoardAdapter(api, make_registration())

        issues_response = MagicMock(status_code=200)
        issues_response.json.return_value = {
            "issues": [
                {
                    "key": "ITPT-1",
                    "fields": {
                        "summary": "Test issue",
                        "status": {"name": "To Do"},
                        "created": "2024-01-01T00:00:00.000+0000",
                        "updated": "2024-01-01T00:00:00.000+0000",
                    },
                }
            ],
            "total": 1,
        }

        with (
            patch(
                "src.adapters.jira_adapter.ensure_fresh_jira_token",
                new=AsyncMock(return_value=("fresh-access-token", "cloud-123")),
            ) as mock_ensure_fresh,
            patch("httpx.AsyncClient.get", new_callable=AsyncMock) as mock_get,
        ):
            mock_get.return_value = issues_response
            tickets = await adapter.get_tickets("80")

        assert len(tickets) == 1
        assert tickets[0].external_ticket_id == "ITPT-1"

        mock_ensure_fresh.assert_called_once()
        call_kwargs = mock_get.call_args.kwargs
        assert call_kwargs["headers"]["Authorization"] == "Bearer fresh-access-token"
        called_url = mock_get.call_args.args[0]
        assert called_url.startswith("https://api.atlassian.com/ex/jira/cloud-123/")

        # The underlying JiraAPI instance must have been mutated in place --
        # not just a local variable inside the adapter -- since
        # get_tickets_by_board reads self.base_url/self.headers off `api`
        # itself.
        assert api.headers["Authorization"] == "Bearer fresh-access-token"
        assert api.base_url == "https://api.atlassian.com/ex/jira/cloud-123"

    @pytest.mark.asyncio
    async def test_create_ticket_refreshes_token_before_delegating_in_oauth_mode(self):
        api = JiraAPI(access_token="stale-access-token", cloud_id="cloud-123")
        adapter = JiraBoardAdapter(api, make_registration())
        adapter.project_key = "ITPT"

        create_response = MagicMock(status_code=201)
        create_response.json.return_value = {"key": "ITPT-100"}

        issue_response = MagicMock(status_code=200)
        issue_response.json.return_value = {
            "key": "ITPT-100",
            "fields": {
                "summary": "New Jira Issue",
                "status": {"name": "To Do"},
                "created": "2024-01-01T00:00:00.000+0000",
                "updated": "2024-01-01T00:00:00.000+0000",
            },
        }

        with (
            patch(
                "src.adapters.jira_adapter.ensure_fresh_jira_token",
                new=AsyncMock(return_value=("fresh-access-token", "cloud-123")),
            ) as mock_ensure_fresh,
            patch("httpx.AsyncClient.post", new_callable=AsyncMock) as mock_post,
            patch("httpx.AsyncClient.get", new_callable=AsyncMock) as mock_get,
        ):
            mock_post.return_value = create_response
            mock_get.return_value = issue_response

            result = await adapter.create_ticket("80", {"summary": "New Jira Issue"})

        assert result.external_ticket_id == "ITPT-100"

        mock_ensure_fresh.assert_called_once()
        post_kwargs = mock_post.call_args.kwargs
        assert post_kwargs["headers"]["Authorization"] == "Bearer fresh-access-token"
        called_url = mock_post.call_args.args[0]
        assert called_url.startswith("https://api.atlassian.com/ex/jira/cloud-123/")
        assert api.headers["Authorization"] == "Bearer fresh-access-token"

    @pytest.mark.asyncio
    async def test_add_comment_refreshes_token_before_delegating_in_oauth_mode(self):
        api = JiraAPI(access_token="stale-access-token", cloud_id="cloud-123")
        adapter = JiraBoardAdapter(api, make_registration())

        ticket = MagicMock()
        ticket.external_ticket_id = "ITPT-1"

        comment_response = MagicMock(status_code=201)

        with (
            patch(
                "src.adapters.jira_adapter.ensure_fresh_jira_token",
                new=AsyncMock(return_value=("fresh-access-token", "cloud-123")),
            ) as mock_ensure_fresh,
            patch("httpx.AsyncClient.post", new_callable=AsyncMock) as mock_post,
        ):
            mock_post.return_value = comment_response
            result = await adapter.add_comment(ticket, "This is a test comment")

        assert result is True

        mock_ensure_fresh.assert_called_once()
        post_kwargs = mock_post.call_args.kwargs
        assert post_kwargs["headers"]["Authorization"] == "Bearer fresh-access-token"
        called_url = mock_post.call_args.args[0]
        assert called_url.startswith("https://api.atlassian.com/ex/jira/cloud-123/")
        assert api.headers["Authorization"] == "Bearer fresh-access-token"

    @pytest.mark.asyncio
    async def test_get_tickets_basic_auth_mode_makes_no_oauth_refresh_call(self):
        """Dual-mode regression: Basic Auth adapters delegating to
        get_tickets_by_board must be completely unaffected -- no refresh
        call, no mutation of self.api's static auth/base_url/headers."""
        api = MagicMock(spec=JiraAPI)
        api.auth = ("me@example.com", "token123")
        api.base_url = "https://example.atlassian.net"
        api.headers = {"Accept": "application/json"}
        api.get_tickets_by_board = AsyncMock(return_value=["ticket-stub"])
        adapter = JiraBoardAdapter(api, make_registration())

        with patch(
            "src.adapters.jira_adapter.ensure_fresh_jira_token",
            new=AsyncMock(),
        ) as mock_ensure_fresh:
            result = await adapter.get_tickets("80")

        assert result == ["ticket-stub"]
        mock_ensure_fresh.assert_not_called()
        api.get_tickets_by_board.assert_called_once_with("80")
        # Unmutated -- still the static Basic Auth values.
        assert api.auth == ("me@example.com", "token123")
        assert api.base_url == "https://example.atlassian.net"

    @pytest.mark.asyncio
    async def test_create_ticket_basic_auth_mode_makes_no_oauth_refresh_call(self):
        """Dual-mode regression: Basic Auth adapters delegating to
        create_ticket must be completely unaffected."""
        api = MagicMock(spec=JiraAPI)
        api.auth = ("me@example.com", "token123")
        api.base_url = "https://example.atlassian.net"
        api.headers = {"Accept": "application/json"}
        created = MagicMock()
        api.create_ticket = AsyncMock(return_value=created)
        adapter = JiraBoardAdapter(api, make_registration())
        adapter.project_key = "ITPT"

        with patch(
            "src.adapters.jira_adapter.ensure_fresh_jira_token",
            new=AsyncMock(),
        ) as mock_ensure_fresh:
            result = await adapter.create_ticket("80", {"summary": "New"})

        assert result is created
        mock_ensure_fresh.assert_not_called()
        api.create_ticket.assert_called_once()
        assert api.auth == ("me@example.com", "token123")
        assert api.base_url == "https://example.atlassian.net"

    @pytest.mark.asyncio
    async def test_add_comment_basic_auth_mode_makes_no_oauth_refresh_call(self):
        """Dual-mode regression: Basic Auth adapters delegating to
        add_comment must be completely unaffected."""
        api = MagicMock(spec=JiraAPI)
        api.auth = ("me@example.com", "token123")
        api.base_url = "https://example.atlassian.net"
        api.headers = {"Accept": "application/json"}
        api.add_comment = AsyncMock(return_value=True)
        adapter = JiraBoardAdapter(api, make_registration())

        ticket = MagicMock()
        ticket.external_ticket_id = "ITPT-1"

        with patch(
            "src.adapters.jira_adapter.ensure_fresh_jira_token",
            new=AsyncMock(),
        ) as mock_ensure_fresh:
            result = await adapter.add_comment(ticket, "This is a test comment")

        assert result is True
        mock_ensure_fresh.assert_not_called()
        api.add_comment.assert_called_once_with("ITPT-1", "This is a test comment")
        assert api.auth == ("me@example.com", "token123")
        assert api.base_url == "https://example.atlassian.net"
