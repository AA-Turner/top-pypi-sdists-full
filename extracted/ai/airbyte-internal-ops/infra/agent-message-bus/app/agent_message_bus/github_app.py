# Copyright (c) 2025 Airbyte, Inc., all rights reserved.
"""GitHub App authentication for the Hydra handoff bot installation."""

from __future__ import annotations

import os
import threading
import time
from datetime import datetime, timedelta, timezone

import jwt
import requests

GITHUB_API_BASE = "https://api.github.com"
GITHUB_REPOSITORY = "airbytehq/airbyte"
_API_HEADERS = {
    "Accept": "application/vnd.github+json",
    "X-GitHub-Api-Version": "2022-11-28",
}
_token: str | None = None
_token_expires_at: datetime | None = None
_token_lock = threading.Lock()


def _create_app_jwt(app_id: str, private_key: str) -> str:
    """Create a short-lived GitHub App JWT."""
    now = int(time.time())
    return jwt.encode(
        {"iat": now - 60, "exp": now + 540, "iss": app_id},
        private_key,
        algorithm="RS256",
    )


def get_installation_token() -> str:
    """Return a cached Hydra handoff bot installation token or mint a new one."""
    global _token, _token_expires_at
    now = datetime.now(tz=timezone.utc)
    if _token and _token_expires_at and now < _token_expires_at:
        return _token

    with _token_lock:
        now = datetime.now(tz=timezone.utc)
        if _token and _token_expires_at and now < _token_expires_at:
            return _token

        app_id = os.environ.get("HYDRA_HANDOFF_BOT_APP_ID")
        private_key = os.environ.get("HYDRA_HANDOFF_BOT_PRIVATE_KEY")
        if not app_id or not private_key:
            raise ValueError(
                "HYDRA_HANDOFF_BOT_APP_ID and HYDRA_HANDOFF_BOT_PRIVATE_KEY must be configured."
            )

        app_jwt = _create_app_jwt(app_id, private_key)
        headers = {**_API_HEADERS, "Authorization": f"Bearer {app_jwt}"}
        installation_response = requests.get(
            f"{GITHUB_API_BASE}/repos/{GITHUB_REPOSITORY}/installation",
            headers=headers,
            timeout=10,
        )
        installation_response.raise_for_status()
        installation_id = installation_response.json()["id"]
        token_response = requests.post(
            f"{GITHUB_API_BASE}/app/installations/{installation_id}/access_tokens",
            headers=headers,
            json={
                "repositories": ["airbyte"],
                "permissions": {
                    "contents": "write",
                    "pull_requests": "read",
                    "metadata": "read",
                },
            },
            timeout=10,
        )
        token_response.raise_for_status()
        token_data = token_response.json()
        token_expires_at = datetime.fromisoformat(token_data["expires_at"].replace("Z", "+00:00"))
        _token = token_data["token"]
        _token_expires_at = token_expires_at - timedelta(minutes=5)
        return _token
