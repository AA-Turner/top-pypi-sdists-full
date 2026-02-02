from datetime import datetime, timedelta
from types import SimpleNamespace

import pytest

from auth.google_auth import handle_auth_callback, start_auth_flow
import time
from fastmcp.server.auth import AccessToken

from auth.oauth21_session_store import (
    OAuth21SessionStore,
    ensure_session_from_access_token,
    set_auth_provider,
)


class DummyFlow:
    """Lightweight stub that mimics google_auth_oauthlib.flow.Flow."""

    def __init__(self, credentials_factory):
        self._credentials_factory = credentials_factory
        self.credentials = None

    def authorization_url(self, access_type="offline", prompt="consent"):
        return "https://example.com/auth", None

    def fetch_token(self, authorization_response):
        self.credentials = self._credentials_factory()


class DummyCredentialStore:
    def __init__(self):
        self.saved = None

    def store_credential(self, user_email, credentials):
        self.saved = (user_email, credentials)


def _dummy_credentials():
    expiry = datetime.utcnow() + timedelta(hours=1)
    return SimpleNamespace(
        token="token",
        refresh_token="refresh",
        token_uri="https://token",
        client_id="client",
        client_secret="secret",
        scopes=["scope"],
        expiry=expiry,
        valid=True,
        id_token=None,
    )


@pytest.mark.asyncio
async def test_start_auth_flow_persists_state(monkeypatch):
    store = OAuth21SessionStore()
    monkeypatch.setattr("auth.google_auth.get_oauth21_session_store", lambda: store)
    monkeypatch.setattr(
        "auth.google_auth.get_fastmcp_session_id", lambda: "session-123"
    )
    monkeypatch.setattr("auth.google_auth.os", "urandom", lambda n: b"\x01" * n)
    monkeypatch.setattr("auth.google_auth.get_current_scopes", lambda: ["scope"])
    monkeypatch.setattr(
        "auth.google_auth.create_oauth_flow",
        lambda scopes, redirect_uri, state: DummyFlow(_dummy_credentials),
    )

    await start_auth_flow(
        user_google_email="user@example.com",
        service_name="Test Service",
        redirect_uri="http://localhost/callback",
    )

    state_value = "01" * 16
    state_info = store.validate_and_consume_oauth_state(
        state_value, session_id="session-123"
    )
    assert state_info["session_id"] == "session-123"


def test_handle_auth_callback_validates_state(monkeypatch):
    store = OAuth21SessionStore()
    state = "securestate"
    store.store_oauth_state(state, session_id="session-abc")

    credential_store = DummyCredentialStore()
    captured_state = {}

    monkeypatch.setattr("auth.google_auth.get_oauth21_session_store", lambda: store)
    monkeypatch.setattr(
        "auth.google_auth.get_credential_store", lambda: credential_store
    )
    monkeypatch.setattr(
        "auth.google_auth.get_user_info",
        lambda credentials: {"email": "user@example.com"},
    )

    def fake_flow_factory(scopes, redirect_uri, state=None):
        captured_state["value"] = state
        return DummyFlow(_dummy_credentials)

    monkeypatch.setattr("auth.google_auth.create_oauth_flow", fake_flow_factory)

    user_email, credentials = handle_auth_callback(
        scopes=["scope"],
        authorization_response=f"http://localhost/callback?code=abc&state={state}",
        redirect_uri="http://localhost/callback",
        session_id="session-abc",
    )

    assert user_email == "user@example.com"
    assert credential_store.saved[0] == "user@example.com"
    assert captured_state["value"] == state
    with pytest.raises(ValueError):
        store.validate_and_consume_oauth_state(state, session_id="session-abc")


def test_handle_auth_callback_rejects_unknown_state(monkeypatch):
    store = OAuth21SessionStore()
    monkeypatch.setattr("auth.google_auth.get_oauth21_session_store", lambda: store)

    with pytest.raises(ValueError):
        handle_auth_callback(
            scopes=["scope"],
            authorization_response="http://localhost/callback?code=abc&state=unknown",
            redirect_uri="http://localhost/callback",
        )


def test_handle_auth_callback_rejects_missing_state(monkeypatch):
    store = OAuth21SessionStore()
    monkeypatch.setattr("auth.google_auth.get_oauth21_session_store", lambda: store)

    with pytest.raises(ValueError):
        handle_auth_callback(
            scopes=["scope"],
            authorization_response="http://localhost/callback?code=abc",
            redirect_uri="http://localhost/callback",
        )


def test_ensure_session_from_access_token(monkeypatch):
    store = OAuth21SessionStore()
    monkeypatch.setattr("auth.oauth21_session_store._global_store", store)

    access_token = AccessToken(
        token="ya29.test",
        client_id="client",
        scopes=["openid", "scope"],
        expires_at=int(time.time()) + 3600,
    )

    class DummySecret:
        def get_secret_value(self):
            return "secret"

    class DummyProvider:
        def __init__(self):
            self._upstream_client_id = "client"
            self._upstream_client_secret = DummySecret()
            self._access_tokens = {access_token.token: access_token}
            self._access_to_refresh = {access_token.token: "refresh-token"}
            self._refresh_tokens = {
                "refresh-token": SimpleNamespace(token="refresh-token")
            }

    set_auth_provider(DummyProvider())

    credentials = ensure_session_from_access_token(
        access_token,
        "user@example.com",
        "mcp-session",
    )

    assert credentials.token == "ya29.test"
    assert credentials.refresh_token == "refresh-token"
    stored = store.get_credentials("user@example.com")
    assert stored.refresh_token == "refresh-token"
    mapped = store.get_credentials_by_mcp_session("mcp-session")
    assert mapped.refresh_token == "refresh-token"

    set_auth_provider(None)
