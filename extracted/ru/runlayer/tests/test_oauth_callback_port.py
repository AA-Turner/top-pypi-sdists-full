"""Tests for OAuth callback port handling."""

import socket

import pytest

from runlayer_cli.oauth import OAuth


def _redirect_uris(oauth: OAuth) -> list[str]:
    return [str(uri) for uri in oauth.context.client_metadata.redirect_uris or []]


def test_oauth_uses_fixed_callback_port(tmp_path):
    oauth = OAuth(
        mcp_url="https://example.com/mcp",
        token_storage_cache_dir=tmp_path,
        callback_port=8765,
    )

    assert oauth.redirect_port == 8765
    assert _redirect_uris(oauth) == ["http://localhost:8765/callback"]


def test_oauth_default_callback_port_matches_redirect_uri(tmp_path, monkeypatch):
    monkeypatch.setattr("runlayer_cli.oauth.get_free_port", lambda: 54321)

    oauth = OAuth(
        mcp_url="https://example.com/mcp",
        token_storage_cache_dir=tmp_path,
    )

    assert oauth.redirect_port == 54321
    assert _redirect_uris(oauth) == [f"http://localhost:{oauth.redirect_port}/callback"]


@pytest.mark.asyncio
async def test_callback_handler_raises_actionable_error_when_port_busy(tmp_path):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as listener:
        try:
            listener.bind(("127.0.0.1", 0))
        except PermissionError as e:
            pytest.skip(f"Loopback bind unavailable in this environment: {e}")
        listener.listen(1)
        port = listener.getsockname()[1]
        oauth = OAuth(
            mcp_url="https://example.com/mcp",
            token_storage_cache_dir=tmp_path,
            callback_port=port,
        )

        with pytest.raises(RuntimeError) as exc_info:
            await oauth.callback_handler()

    message = str(exc_info.value)
    assert f"OAuth callback port {port} is already in use" in message
    assert "--oauth-callback-port" in message
    assert "http://localhost:<port>/callback" in message
