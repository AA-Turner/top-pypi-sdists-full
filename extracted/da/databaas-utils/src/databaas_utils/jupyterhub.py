"""The logged-in user's token, inside a JupyterHub singleuser pod.

The Databaas hub exposes ``GET /hub/api/oauth-token``: it exchanges the
user's stored Zitadel refresh token for a fresh access token and returns it.
JupyterHub injects ``JUPYTERHUB_API_URL`` and ``JUPYTERHUB_API_TOKEN`` (a
server token scoped to the owning user) into every singleuser pod, which is
all this needs. No credential of the user's own ever lands in the pod's
environment.

Every call to the endpoint rotates the refresh token at Zitadel, so the access
token is cached until shortly before its own ``exp`` rather than re-fetched
per request.
"""

from __future__ import annotations

import base64
import json
import os
import threading
import time
from collections.abc import Mapping
from dataclasses import dataclass, field
from typing import Any

import requests

from databaas_utils.errors import AuthenticationError, ConfigurationError

API_URL_VAR = "JUPYTERHUB_API_URL"
API_TOKEN_VAR = "JUPYTERHUB_API_TOKEN"
REQUEST_TIMEOUT = 10
# Refresh this many seconds before actual expiry, matching settings.py.
_EXPIRY_MARGIN = 60
# Used when the access token is not a JWT and carries no readable `exp`.
_FALLBACK_LIFETIME = 60
_HTTP_UNAUTHORIZED = 401
_JWT_PARTS = 3


def in_jupyterhub(env: Mapping[str, str] | None = None) -> bool:
    """Whether this process runs in a JupyterHub singleuser server."""
    source = env if env is not None else os.environ
    return bool(source.get(API_URL_VAR) and source.get(API_TOKEN_VAR))


@dataclass
class JupyterHubToken:
    """A ``TokenProvider`` that asks the hub for the user's access token.

    Most code should use ``databaas_utils.user`` instead of this directly.

    Args:
        api_url: The hub API URL (``JUPYTERHUB_API_URL``).
        api_token: The server's API token (``JUPYTERHUB_API_TOKEN``).
        timeout: Per-request timeout in seconds.
    """

    api_url: str
    api_token: str = field(repr=False)
    timeout: float = REQUEST_TIMEOUT
    _token: str | None = field(default=None, init=False, repr=False, compare=False)
    _expires_at: float = field(default=0.0, init=False, repr=False, compare=False)
    _lock: threading.Lock = field(
        default_factory=threading.Lock, init=False, repr=False, compare=False
    )

    @classmethod
    def from_env(cls, env: Mapping[str, str] | None = None) -> JupyterHubToken:
        """Build from ``JUPYTERHUB_API_URL`` and ``JUPYTERHUB_API_TOKEN``.

        Raises:
            ConfigurationError: If either variable is unset.
        """
        source = env if env is not None else os.environ
        api_url = source.get(API_URL_VAR)
        api_token = source.get(API_TOKEN_VAR)
        if not (api_url and api_token):
            raise ConfigurationError(
                f"{API_URL_VAR} / {API_TOKEN_VAR} are not set — this is not a "
                "JupyterHub singleuser server. Outside JupyterHub, log in with "
                "`databaas login` and use LakehouseSettings.from_profile()."
            )
        return cls(api_url=api_url, api_token=api_token)

    @property
    def endpoint(self) -> str:
        """The hub's ``oauth-token`` URL."""
        return f"{self.api_url.rstrip('/')}/oauth-token"

    def auth_header(self) -> str:
        """``Bearer <token>``, asking the hub only when the cached token is stale.

        Raises:
            AuthenticationError: If the hub cannot supply a token. A 401 means
                the user's login expired; log out of Jupyter and back in.
        """
        if self._token and time.monotonic() < self._expires_at:
            return f"Bearer {self._token}"
        with self._lock:
            if not (self._token and time.monotonic() < self._expires_at):
                self._token = self._fetch()
                self._expires_at = time.monotonic() + max(
                    _lifetime(self._token) - _EXPIRY_MARGIN, 0
                )
            return f"Bearer {self._token}"

    def invalidate(self) -> None:
        """Drop the cached token so the next call asks the hub again."""
        with self._lock:
            self._token = None
            self._expires_at = 0.0

    def _fetch(self) -> str:
        try:
            response = requests.get(
                self.endpoint,
                headers={"Authorization": f"token {self.api_token}"},
                timeout=self.timeout,
            )
        except requests.RequestException as exc:
            raise AuthenticationError(
                f"token request to {self.endpoint} failed: {exc}"
            ) from exc
        if response.status_code == _HTTP_UNAUTHORIZED:
            raise AuthenticationError(
                "the hub could not refresh your login (the Zitadel refresh token "
                "has probably expired). Log out of Jupyter and log back in."
            )
        try:
            response.raise_for_status()
        except requests.HTTPError as exc:
            raise AuthenticationError(
                f"token request to {self.endpoint} failed: {exc}"
            ) from exc
        token = response.json().get("access_token")
        if not token:
            raise AuthenticationError(f"{self.endpoint} returned no access_token")
        return str(token)


def _lifetime(token: str) -> float:
    """Seconds until the token's ``exp``, read without verifying it.

    Lakekeeper verifies the token; this only decides when to fetch a new one.
    """
    parts = token.split(".")
    if len(parts) != _JWT_PARTS:
        return _FALLBACK_LIFETIME
    try:
        padded = parts[1] + "=" * (-len(parts[1]) % 4)
        claims: dict[str, Any] = json.loads(base64.urlsafe_b64decode(padded))
        return float(claims["exp"]) - time.time()
    except (ValueError, KeyError, TypeError):
        return _FALLBACK_LIFETIME
