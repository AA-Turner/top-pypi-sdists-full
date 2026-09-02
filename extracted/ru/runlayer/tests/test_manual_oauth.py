from pathlib import Path

import pytest
from mcp.shared.auth import OAuthClientInformationFull, OAuthToken

from runlayer_cli.models import ServerDetails
from runlayer_cli.oauth import FileTokenStorage, OAuth


def test_server_details_parses_manual_oauth_configuration() -> None:
    details = ServerDetails.model_validate(
        {
            "id": "server-id",
            "name": "Manual OAuth server",
            "url": "https://example.com/mcp",
            "transport_type": "streaming-http",
            "requires_manual_oauth_setup": True,
            "manual_oauth_client_id": "configured-client",
            "manual_oauth_client_secret": "configured-secret",
            "preferred_token_endpoint_auth_method": "client_secret_basic",
        }
    )

    assert details.requires_manual_oauth_setup is True
    assert details.manual_oauth_client_id == "configured-client"
    assert details.manual_oauth_client_secret == "configured-secret"
    assert details.preferred_token_endpoint_auth_method == "client_secret_basic"


@pytest.mark.asyncio
async def test_manual_client_seeds_client_info_and_invalidates_changed_client_tokens(
    tmp_path: Path,
) -> None:
    storage = FileTokenStorage("https://example.com/mcp", tmp_path)
    await storage.set_client_info(
        OAuthClientInformationFull(
            client_id="old-client",
            client_secret="old-secret",
            redirect_uris=["http://localhost:49123/callback"],
        )
    )
    await storage.set_tokens(OAuthToken(access_token="old-token", token_type="Bearer"))

    oauth = OAuth(
        mcp_url="https://example.com/mcp",
        token_storage_cache_dir=tmp_path,
        manual_client_id="configured-client",
        manual_client_secret="configured-secret",
        token_endpoint_auth_method="client_secret_basic",
    )
    await oauth._initialize()

    assert oauth.redirect_port == 49123
    assert oauth.context.client_info is not None
    assert oauth.context.client_info.client_id == "configured-client"
    assert oauth.context.client_info.client_secret == "configured-secret"
    assert oauth.context.client_info.token_endpoint_auth_method == "client_secret_basic"
    assert oauth.context.current_tokens is None
    assert await storage.get_tokens() is None


@pytest.mark.asyncio
async def test_non_manual_client_reuses_cached_callback_port(tmp_path: Path) -> None:
    storage = FileTokenStorage("https://example.com/mcp", tmp_path)
    await storage.set_client_info(
        OAuthClientInformationFull(
            client_id="dynamically-registered-client",
            redirect_uris=["http://localhost:49125/callback"],
        )
    )

    oauth = OAuth(
        mcp_url="https://example.com/mcp",
        token_storage_cache_dir=tmp_path,
    )

    assert oauth.redirect_port == 49125


@pytest.mark.asyncio
async def test_dynamic_registration_remains_available_without_manual_client(
    tmp_path: Path,
) -> None:
    oauth = OAuth(
        mcp_url="https://example.com/mcp",
        token_storage_cache_dir=tmp_path,
        callback_port=49124,
    )

    await oauth._initialize()

    assert oauth.context.client_info is None


def test_public_manual_client_defaults_auth_method_none(tmp_path: Path) -> None:
    """A manual client with no secret is a public PKCE client: the token
    endpoint must not expect client authentication."""
    oauth = OAuth(
        mcp_url="https://example.com/mcp",
        token_storage_cache_dir=tmp_path,
        manual_client_id="public-client",
    )

    assert oauth.manual_client_info is not None
    assert oauth.manual_client_info.client_secret is None
    assert oauth.manual_client_info.token_endpoint_auth_method == "none"


def test_confidential_manual_client_defaults_auth_method_post(
    tmp_path: Path,
) -> None:
    oauth = OAuth(
        mcp_url="https://example.com/mcp",
        token_storage_cache_dir=tmp_path,
        manual_client_id="confidential-client",
        manual_client_secret="secret",
    )

    assert oauth.manual_client_info is not None
    assert (
        oauth.manual_client_info.token_endpoint_auth_method == "client_secret_post"
    )


def test_secret_less_client_overrides_confidential_method(tmp_path: Path) -> None:
    """A stored confidential preference without a secret can only fail the
    token exchange — the missing secret wins and forces "none"."""
    oauth = OAuth(
        mcp_url="https://example.com/mcp",
        token_storage_cache_dir=tmp_path,
        manual_client_id="public-client",
        token_endpoint_auth_method="client_secret_post",
    )

    assert oauth.manual_client_info is not None
    assert oauth.manual_client_info.token_endpoint_auth_method == "none"


def test_empty_string_secret_treated_as_public_client(tmp_path: Path) -> None:
    """An empty-string secret (possible via API/MCP-tool creates, which the
    backend's truthiness rule accepts) must classify as public, not as a
    confidential client authenticating with an empty secret."""
    oauth = OAuth(
        mcp_url="https://example.com/mcp",
        token_storage_cache_dir=tmp_path,
        manual_client_id="public-client",
        manual_client_secret="",
    )

    assert oauth.manual_client_info is not None
    assert oauth.manual_client_info.client_secret is None
    assert oauth.manual_client_info.token_endpoint_auth_method == "none"
