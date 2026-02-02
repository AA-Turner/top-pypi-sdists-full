import pytest
from types import SimpleNamespace

from auth.auth_info_middleware import AuthInfoMiddleware
from auth.oauth21_session_store import OAuth21SessionStore


class DummyFastMCPContext:
    def __init__(self):
        self._state = {}
        self.session_id = None

    def get_state(self, key):
        return self._state.get(key)

    def set_state(self, key, value):
        self._state[key] = value


@pytest.mark.asyncio
async def test_stdio_single_session_fallback(monkeypatch):
    """Ensure stdio mode falls back to the only stored OAuth session."""
    store = OAuth21SessionStore()
    store.store_session(
        user_email="user@example.com",
        access_token="token",
        refresh_token="refresh",
        scopes=["scope"],
    )

    # Patch dependencies to simulate stdio environment with one session
    monkeypatch.setattr("auth.auth_info_middleware.get_http_headers", lambda: {})
    monkeypatch.setattr("core.config.get_transport_mode", lambda: "stdio")
    monkeypatch.setattr(
        "auth.auth_info_middleware.get_oauth21_session_store", lambda: store
    )

    fastmcp_context = DummyFastMCPContext()
    middleware_context = SimpleNamespace(
        fastmcp_context=fastmcp_context,
        arguments={},
    )

    middleware = AuthInfoMiddleware()
    await middleware._process_request_for_auth(middleware_context)

    assert fastmcp_context.get_state("authenticated_user_email") == "user@example.com"
    assert fastmcp_context.get_state("authenticated_via") == "stdio_single_session"
