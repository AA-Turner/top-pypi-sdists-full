"""Tests for the shared board-adapter factory (#417 consolidation).

The point of the factory is that both board sync and ticket creation get the
*same* capabilities. Before it there were three copies of the BoardType switch
and they had drifted: ticket creation rejected OAuth Jira and Notion outright, so
a board could be synced but no ticket could be created on it.
"""

from unittest.mock import AsyncMock, MagicMock, patch
from uuid import uuid4

import pytest

from src.adapters import (
    JiraBoardAdapter,
    LinearBoardAdapter,
    NotionBoardAdapter,
    TrelloBoardAdapter,
)
from src.domain.board import BoardRegistration, BoardType
from src.services.board_adapter_factory import (
    build_board_adapter,
    is_oauth_jira,
)
from src.services.board_credential_service import OAUTH_TOKEN_SENTINEL


def _reg(board_type, board_url="https://example.atlassian.net/jira/x"):
    return BoardRegistration(
        id=str(uuid4()),
        organization_id="org-1",
        project_id="proj-1",
        board_name="B",
        board_type=board_type,
        board_url=board_url,
        board_external_id="EXT",
    )


class TestIsOAuthJira:
    def test_true_only_for_jira_with_the_sentinel(self):
        assert is_oauth_jira(_reg(BoardType.JIRA), OAUTH_TOKEN_SENTINEL) is True

    def test_false_for_jira_with_a_real_token(self):
        assert is_oauth_jira(_reg(BoardType.JIRA), "me@x.com:tok") is False

    def test_false_for_another_board_type_even_with_the_sentinel(self):
        assert is_oauth_jira(_reg(BoardType.LINEAR), OAUTH_TOKEN_SENTINEL) is False


class TestBoardTypeDispatch:
    @pytest.mark.asyncio
    async def test_trello_colon_joined(self):
        adapter = await build_board_adapter(
            _reg(BoardType.TRELLO), "key:token", MagicMock()
        )
        assert isinstance(adapter, TrelloBoardAdapter)

    @pytest.mark.asyncio
    async def test_linear(self):
        adapter = await build_board_adapter(
            _reg(BoardType.LINEAR), "lin_api_key", MagicMock()
        )
        assert isinstance(adapter, LinearBoardAdapter)

    @pytest.mark.asyncio
    async def test_notion(self):
        """Ticket creation used to reject Notion outright; sync accepted it."""
        adapter = await build_board_adapter(
            _reg(BoardType.NOTION), "secret_abc", MagicMock()
        )
        assert isinstance(adapter, NotionBoardAdapter)

    @pytest.mark.asyncio
    async def test_jira_basic_auth(self):
        adapter = await build_board_adapter(
            _reg(BoardType.JIRA), "me@example.com:api-token", MagicMock()
        )
        assert isinstance(adapter, JiraBoardAdapter)

    @pytest.mark.asyncio
    async def test_unsupported_board_type_raises(self):
        reg = _reg(BoardType.JIRA)
        reg.board_type = "carrier_pigeon"
        with pytest.raises(ValueError, match="Unsupported board type"):
            await build_board_adapter(reg, "tok", MagicMock())


class TestJiraOAuth:
    """The gap the factory closes."""

    @pytest.mark.asyncio
    async def test_sentinel_resolves_an_oauth_credential(self):
        reg = _reg(BoardType.JIRA)
        with patch(
            "src.services.board_adapter_factory.ensure_fresh_jira_token",
            new=AsyncMock(return_value=("access-tok", "cloud-123")),
        ) as mocked:
            adapter = await build_board_adapter(reg, OAUTH_TOKEN_SENTINEL, MagicMock())

        mocked.assert_awaited_once()
        assert isinstance(adapter, JiraBoardAdapter)
        # JiraAPI's OAuth path leaves .auth None -- that is what
        # JiraBoardAdapter._is_oauth_mode() keys on to keep refreshing.
        assert adapter.api.auth is None

    @pytest.mark.asyncio
    async def test_basic_auth_does_not_touch_the_oauth_path(self):
        with patch(
            "src.services.board_adapter_factory.ensure_fresh_jira_token",
            new=AsyncMock(),
        ) as mocked:
            await build_board_adapter(
                _reg(BoardType.JIRA), "me@example.com:tok", MagicMock()
            )
        mocked.assert_not_awaited()


class TestJiraBaseUrl:
    """Ticket creation used to allow base_url=None; sync raised. Sync was right."""

    @pytest.mark.asyncio
    async def test_missing_board_url_raises_clearly(self):
        with pytest.raises(ValueError, match="board_url is required"):
            await build_board_adapter(
                _reg(BoardType.JIRA, board_url=None), "a@b.c:tok", MagicMock()
            )

    @pytest.mark.asyncio
    async def test_unparseable_board_url_raises_clearly(self):
        with pytest.raises(ValueError, match="Cannot extract base URL"):
            await build_board_adapter(
                _reg(BoardType.JIRA, board_url="not-a-url"), "a@b.c:tok", MagicMock()
            )

    @pytest.mark.asyncio
    async def test_base_url_is_scheme_and_host_only(self):
        adapter = await build_board_adapter(
            _reg(BoardType.JIRA, board_url="https://acme.atlassian.net/jira/boards/1"),
            "a@b.c:tok",
            MagicMock(),
        )
        assert adapter.api.base_url == "https://acme.atlassian.net"


class TestATokenIsTheWholeCredential:
    """There is no second store to consult when a token looks incomplete.

    A `legacy_credentials` keyword used to accept a `~/.innoday`/OS-keyring
    lookup, and three tests here covered it: a bare Trello token being completed
    from the keyring, and the same for Jira. #525 phase 3 deleted the parameter,
    so those cases no longer exist to test -- what survives is the behaviour that
    was always sync's, and is now everyone's.
    """

    @pytest.mark.asyncio
    async def test_a_bare_trello_token_is_used_for_both_halves(self):
        """Unchanged: this is what sync did, since sync never passed a lookup."""
        adapter = await build_board_adapter(
            _reg(BoardType.TRELLO), "bare-token", MagicMock()
        )
        assert isinstance(adapter, TrelloBoardAdapter)
        assert adapter.api.api_key == "bare-token"
        assert adapter.api.token == "bare-token"

    @pytest.mark.asyncio
    async def test_jira_without_a_colon_raises(self):
        """Half a Basic Auth credential is not a credential. Fail, don't guess."""
        with pytest.raises(ValueError, match="Expected email:api_token"):
            await build_board_adapter(_reg(BoardType.JIRA), "bare-token", MagicMock())

    def test_the_factory_exposes_no_legacy_credential_seam(self):
        """Re-adding the convenience means re-adding a named parameter."""
        import inspect

        from src.services import board_adapter_factory

        params = inspect.signature(build_board_adapter).parameters
        assert "legacy_credentials" not in params
        assert not hasattr(board_adapter_factory, "LegacyCredentialLookup")
