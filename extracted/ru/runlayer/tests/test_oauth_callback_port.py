"""Tests for OAuth callback port handling."""

import errno
import socket
import sys
from unittest.mock import MagicMock

import anyio
import pytest

from runlayer_cli.oauth import OAuth, _callback_listener


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


def test_windows_callback_rejects_shared_occupied_port(monkeypatch):
    """Model Winsock sharing at the socket boundary on every test host."""
    exclusive = getattr(socket, "SO_EXCLUSIVEADDRUSE", -5)
    options = set()
    listener = MagicMock()
    listener.__enter__.return_value = listener
    listener.setsockopt.side_effect = lambda level, option, value: options.add(option)
    collision = OSError(errno.EADDRINUSE, "occupied test port")

    def bind(address):
        # An existing SO_REUSEADDR owner can share unless we request exclusivity.
        if exclusive in options:
            raise collision

    listener.bind.side_effect = bind
    with monkeypatch.context() as patch:
        patch.setattr(sys, "platform", "win32")
        patch.setattr(socket, "SO_EXCLUSIVEADDRUSE", exclusive, raising=False)
        patch.setattr(socket, "socket", lambda *args: listener)
        with pytest.raises(RuntimeError, match="already in use") as exc_info:
            with _callback_listener(8765):
                pass

    assert exc_info.value.__cause__ is collision
    assert socket.SO_REUSEADDR not in options


@pytest.mark.asyncio
@pytest.mark.parametrize("listening", [True, False], ids=["listening", "bound-only"])
@pytest.mark.parametrize(
    "owner_reuse",
    [
        False,
        pytest.param(
            True,
            marks=pytest.mark.skipif(
                sys.platform != "win32", reason="Winsock port-sharing contract"
            ),
        ),
    ],
)
async def test_callback_handler_raises_actionable_error_when_port_busy(
    tmp_path, listening, owner_reuse
):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as listener:
        if owner_reuse:
            listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        try:
            listener.bind(("127.0.0.1", 0))
        except PermissionError as e:
            pytest.skip(f"Loopback bind unavailable in this environment: {e}")
        if listening:
            listener.listen(1)
        port = listener.getsockname()[1]
        oauth = OAuth(
            mcp_url="https://example.com/mcp",
            token_storage_cache_dir=tmp_path,
            callback_port=port,
        )

        with anyio.fail_after(5), pytest.raises(RuntimeError) as exc_info:
            await oauth.callback_handler()

    message = str(exc_info.value)
    assert f"OAuth callback port {port} is already in use" in message
    assert "--oauth-callback-port" in message
    assert "http://localhost:<port>/callback" in message
    assert isinstance(exc_info.value.__cause__, OSError)
    assert exc_info.value.__cause__.errno == errno.EADDRINUSE


@pytest.mark.asyncio
@pytest.mark.parametrize(
    ("operation", "error_number"),
    [
        ("setsockopt", errno.ENOPROTOOPT),
        ("bind", errno.EPERM),
        ("bind", errno.EACCES),
        ("bind", errno.EADDRNOTAVAIL),
        ("listen", errno.EOPNOTSUPP),
    ],
)
async def test_callback_socket_failure_preserves_safe_diagnostics(
    tmp_path, monkeypatch, operation, error_number
):
    original_error = OSError(error_number, "untrusted diagnostic detail")
    sockets = []

    class FailingSocket(socket.socket):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            sockets.append(self)

        def bind(self, address):
            # The injected listen failure does not need to occupy a real port.
            pass

    def fail_operation(self, *args, **kwargs):
        raise original_error

    setattr(FailingSocket, operation, fail_operation)
    oauth = OAuth(
        mcp_url="https://mcp.example.test/mcp",
        token_storage_cache_dir=tmp_path,
        callback_port=8765,
    )
    with monkeypatch.context() as patch:
        patch.setattr(socket, "socket", FailingSocket)
        with pytest.raises(RuntimeError) as exc_info:
            await oauth.callback_handler()

    message = str(exc_info.value)
    assert exc_info.value.__cause__ is original_error
    assert errno.errorcode[error_number] in message
    assert ("socket" if operation == "setsockopt" else operation) in message
    assert "already in use" not in message
    assert "--oauth-callback-port" not in message
    assert "untrusted diagnostic detail" not in message
    assert sockets and all(sock.fileno() == -1 for sock in sockets)
