"""cvc.auth — authentication helpers (Firebase user auth + provider OAuth).

This package wraps two distinct concerns under one namespace:

* User auth (Firebase login_flow / logout / get_current_user) — re-exported
  from ``cvc.auth._firebase`` for backwards compatibility with the legacy
  ``cvc/auth.py`` module.
* Provider OAuth (e.g. ``cvc.auth.copilot_auth``) — GitHub Copilot device-code
  flow ported verbatim from upstream.
"""
from cvc.auth._firebase import (  # noqa: F401  re-export
    FIREBASE_CONFIG,
    AUTH_FILE,
    AuthHandler,
    update_user_firestore,
    login_flow,
    logout,
    get_current_user,
)

__all__ = [
    "FIREBASE_CONFIG",
    "AUTH_FILE",
    "AuthHandler",
    "update_user_firestore",
    "login_flow",
    "logout",
    "get_current_user",
]
