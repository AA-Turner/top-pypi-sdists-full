"""Mock session state for simulating OAuth login in mock mode.

Tracks per-provider authentication state so that mock mode can simulate
the full login/logout flow without real OAuth infrastructure.

State is stored in module-level globals, so it is shared across all
requests within a single server process and is not isolated per client
or per worker. This is intentional: mock mode targets single-user local
development, not multi-tenant production use.
"""

from __future__ import annotations

MOCK_EMAIL = "mock-user@airbyte.io"
MOCK_BEARER_TOKEN = "mock-bearer-token"

_oauth_authenticated: bool = False
_google_authenticated: bool = False


def mock_oauth_is_authenticated() -> bool:
    """Return `True` when the mock Airbyte OAuth session is active."""
    return _oauth_authenticated


def mock_google_is_authenticated() -> bool:
    """Return `True` when the mock Google OAuth session is active."""
    return _google_authenticated


def mock_oauth_login() -> dict[str, object]:
    """Simulate Airbyte OAuth login and return authenticated state dict."""
    global _oauth_authenticated
    _oauth_authenticated = True
    return {
        "auth_bearer_token": MOCK_BEARER_TOKEN,
        "admin_user_email": MOCK_EMAIL,
        "oauth_authenticated": True,
        "oauth_user_email": MOCK_EMAIL,
        "oauth_status": f"Signed in as {MOCK_EMAIL}",
    }


def mock_oauth_logout() -> dict[str, object]:
    """Simulate Airbyte OAuth logout and return signed-out state dict."""
    global _oauth_authenticated
    _oauth_authenticated = False
    return {
        "auth_bearer_token": "",
        "admin_user_email": "",
        "oauth_authenticated": False,
        "oauth_user_email": "",
        "oauth_status": "Signed out.",
    }


def mock_oauth_session_state() -> dict[str, object]:
    """Return current mock Airbyte OAuth state dict."""
    if _oauth_authenticated:
        return mock_oauth_login()
    return {
        "auth_bearer_token": "",
        "admin_user_email": "",
        "oauth_authenticated": False,
        "oauth_user_email": "",
        "oauth_status": "",
    }


def mock_google_login() -> dict[str, object]:
    """Simulate Google OAuth login and return authenticated state dict."""
    global _google_authenticated
    _google_authenticated = True
    return {
        "google_authenticated": True,
        "google_user_email": MOCK_EMAIL,
        "google_access_token": "mock-google-access-token",
        "google_status": f"Signed in as {MOCK_EMAIL}",
    }


def mock_google_logout() -> dict[str, object]:
    """Simulate Google OAuth logout and return signed-out state dict."""
    global _google_authenticated
    _google_authenticated = False
    return {
        "google_authenticated": False,
        "google_user_email": "",
        "google_access_token": "",
        "google_status": "Signed out of Google.",
    }


def mock_google_session_state() -> dict[str, object]:
    """Return current mock Google OAuth state dict."""
    if _google_authenticated:
        return mock_google_login()
    return {
        "google_authenticated": False,
        "google_user_email": "",
        "google_access_token": "",
        "google_status": "",
    }
