"""OAuth-based service integrations (Gmail, GitHub, Calendar, etc.).

Framework for adding any OAuth-protected service in ~30 LOC each:

    sage integrate connect github    # OAuth flow → token stored
    sage integrate list              # all connected services
    sage integrate revoke github     # disconnect

Architecture:

    ServiceIntegration  — one connected account (service + token + scope)
    IntegrationStore    — persistent store at ~/.sage/integrations.json (mode 0600)
    GitHubIntegration   — concrete service. Pattern: build_authorize_url →
                          user clicks → exchange_code → ServiceIntegration

Adding a new service:
    1. Subclass the pattern in GitHubIntegration with the service's
       authorize_url / token_url / userinfo_url.
    2. Register in INTEGRATION_REGISTRY (this file).
    3. Done — `sage integrate connect <name>` works automatically.

Why one OAuth class per service rather than a generic adapter: real
OAuth providers differ in details (scope param naming, refresh-token
behavior, userinfo endpoint shape). A thin per-service class keeps the
quirks isolated and testable.
"""

from __future__ import annotations

import json
import logging
import os
import stat as stat_mod
import urllib.parse
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Protocol

logger = logging.getLogger("sage.service_integrations")


_DEFAULT_STATE_PATH = Path.home() / ".sage" / "integrations.json"


class OAuthCallbackError(RuntimeError):
    """OAuth provider rejected the code-exchange or returned an error.
    Carries the provider's error code + description for actionable feedback."""


# ── ServiceIntegration ───────────────────────────────────────────────────────


@dataclass(frozen=True)
class ServiceIntegration:
    """A connected service. Identified by (service, account_id) so a user
    can connect e.g. multiple GitHub accounts."""
    service: str            # "github" | "google" | "spotify" | ...
    access_token: str
    refresh_token: str | None
    expires_at: datetime | None
    scope: str              # space- or comma-separated scope string
    account_id: str         # provider's user ID (login, email, etc.)

    def is_expired(self, *, buffer_seconds: int = 60) -> bool:
        """True if the token is past its expiry (or within the buffer).
        Tokens without an explicit expiry never expire (e.g., GitHub's)."""
        if self.expires_at is None:
            return False
        return datetime.now(timezone.utc).timestamp() + buffer_seconds >= self.expires_at.timestamp()

    def to_dict(self) -> dict:
        return {
            "service": self.service,
            "access_token": self.access_token,
            "refresh_token": self.refresh_token,
            "expires_at": self.expires_at.isoformat() if self.expires_at else None,
            "scope": self.scope,
            "account_id": self.account_id,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "ServiceIntegration":
        return cls(
            service=data["service"],
            access_token=data["access_token"],
            refresh_token=data.get("refresh_token"),
            expires_at=(
                datetime.fromisoformat(data["expires_at"])
                if data.get("expires_at") else None
            ),
            scope=data.get("scope", ""),
            account_id=data["account_id"],
        )


# ── IntegrationStore ─────────────────────────────────────────────────────────


class IntegrationStore:
    """Persistent secure storage for OAuth tokens.

    Why JSON not OS keychain: keychain is heterogeneous across platforms
    (macOS Keychain, Linux gnome-keyring, Windows DPAPI). JSON with file
    perms 0600 gives consistent behavior + visibility. For higher
    sensitivity we'd reach for OS keychain — for now, 0600 is the bar.
    """

    def __init__(self, state_path: Path | None = None):
        self._state_path = Path(state_path or _DEFAULT_STATE_PATH)
        self._cache: dict[tuple[str, str], ServiceIntegration] | None = None

    # ── CRUD ─────────────────────────────────────────────────────────────

    def save(self, integration: ServiceIntegration) -> None:
        store = self._load_all()
        store[(integration.service, integration.account_id)] = integration
        self._write_all(store)

    def get(self, service: str, account_id: str) -> ServiceIntegration | None:
        return self._load_all().get((service, account_id))

    def remove(self, service: str, account_id: str) -> None:
        store = self._load_all()
        key = (service, account_id)
        if key in store:
            del store[key]
            self._write_all(store)

    def list(self) -> list[ServiceIntegration]:
        return list(self._load_all().values())

    # ── Persistence ──────────────────────────────────────────────────────

    def _load_all(self) -> dict[tuple[str, str], ServiceIntegration]:
        if self._cache is not None:
            return self._cache
        if not self._state_path.exists():
            self._cache = {}
            return self._cache
        try:
            raw = json.loads(self._state_path.read_text())
            self._cache = {
                (item["service"], item["account_id"]): ServiceIntegration.from_dict(item)
                for item in raw.get("integrations", [])
            }
        except Exception as exc:
            logger.warning("Could not load integrations from %s: %s", self._state_path, exc)
            self._cache = {}
        return self._cache

    def _write_all(self, store: dict[tuple[str, str], ServiceIntegration]) -> None:
        self._state_path.parent.mkdir(parents=True, exist_ok=True)
        tmp = self._state_path.with_suffix(self._state_path.suffix + ".tmp")
        payload = {"integrations": [si.to_dict() for si in store.values()]}
        tmp.write_text(json.dumps(payload, indent=2))
        # Tighten perms BEFORE replacing — protects against a brief window
        # where the file is world-readable.
        os.chmod(tmp, stat_mod.S_IRUSR | stat_mod.S_IWUSR)  # 0o600
        tmp.replace(self._state_path)
        self._cache = store


# ── HTTP-client protocol (for testability) ──────────────────────────────────


class _HttpClient(Protocol):
    def get(self, url: str, **kwargs: Any) -> Any: ...
    def post(self, url: str, **kwargs: Any) -> Any: ...


# ── GitHub: the first concrete integration ──────────────────────────────────


class GitHubIntegration:
    """OAuth-code flow against GitHub's API.

    Required GitHub OAuth App config:
      - Client ID + secret
      - Authorization callback URL: http://localhost:<port>/cb
        (sage spins up a one-shot local HTTP server during connect)
    """

    AUTHORIZE_URL = "https://github.com/login/oauth/authorize"
    TOKEN_URL = "https://github.com/login/oauth/access_token"
    USERINFO_URL = "https://api.github.com/user"
    DEFAULT_SCOPES = ("repo", "user")

    def __init__(
        self,
        client_id: str,
        client_secret: str,
        http_client: _HttpClient | None = None,
    ):
        self._client_id = client_id
        self._client_secret = client_secret
        # If no client provided, default to httpx — but lazy-import so test
        # environments without httpx still work.
        if http_client is None:
            import httpx  # noqa: WPS433 (intentional lazy import)
            http_client = httpx.Client(timeout=30.0)
        self._http = http_client

    # ── OAuth steps ──────────────────────────────────────────────────────

    def build_authorize_url(self, *, state: str, redirect_uri: str) -> str:
        """Step 1: send the user here. ``state`` is a CSRF token the
        caller validates on callback."""
        params = {
            "client_id": self._client_id,
            "redirect_uri": redirect_uri,
            "scope": " ".join(self.DEFAULT_SCOPES),
            "state": state,
        }
        return f"{self.AUTHORIZE_URL}?{urllib.parse.urlencode(params)}"

    def exchange_code(self, *, code: str, redirect_uri: str) -> ServiceIntegration:
        """Step 2: GitHub redirected to our callback with ?code=. Exchange
        for an access token, then fetch the user's login to populate
        account_id."""
        token_resp = self._http.post(
            self.TOKEN_URL,
            data={
                "client_id": self._client_id,
                "client_secret": self._client_secret,
                "code": code,
                "redirect_uri": redirect_uri,
            },
            headers={"Accept": "application/json"},
        )
        token_resp.raise_for_status()
        token_data = token_resp.json()

        if "error" in token_data:
            raise OAuthCallbackError(
                f"GitHub OAuth rejected the code: {token_data['error']} "
                f"({token_data.get('error_description', 'no description')})"
            )

        access_token = token_data["access_token"]
        scope = token_data.get("scope", " ".join(self.DEFAULT_SCOPES))

        # Step 3: fetch the user's profile so we know which account this
        # token belongs to. account_id = GitHub login (handle).
        user_resp = self._http.get(
            self.USERINFO_URL,
            headers={
                "Authorization": f"token {access_token}",
                "Accept": "application/json",
            },
        )
        user_resp.raise_for_status()
        user = user_resp.json()

        return ServiceIntegration(
            service="github",
            access_token=access_token,
            refresh_token=None,         # GitHub OAuth Apps don't issue refresh tokens
            expires_at=None,            # And the token doesn't expire by default
            scope=scope,
            account_id=user["login"],
        )

    # ── Authenticated requests ───────────────────────────────────────────

    def request(
        self,
        integration: ServiceIntegration,
        method: str,
        path: str,
        **kwargs: Any,
    ) -> Any:
        """Make an authenticated GitHub API call.

        ``path`` is appended to https://api.github.com. Pass kwargs through
        to the HTTP client for body/params.
        """
        url = f"https://api.github.com{path}"
        headers = kwargs.pop("headers", {}) | {
            "Authorization": f"token {integration.access_token}",
            "Accept": "application/vnd.github+json",
        }
        method = method.upper()
        if method == "GET":
            return self._http.get(url, headers=headers, **kwargs)
        if method == "POST":
            return self._http.post(url, headers=headers, **kwargs)
        raise ValueError(f"Unsupported HTTP method: {method}")


# ── Integration registry ─────────────────────────────────────────────────────
# Add new services here. Each entry maps a short name to a factory
# function that returns the integration class instance.

INTEGRATION_REGISTRY: dict[str, str] = {
    "github": "sage.core.service_integrations:GitHubIntegration",
    # Future:
    # "google":  "sage.core.service_integrations:GoogleIntegration",   # Gmail + Calendar
    # "spotify": "sage.core.service_integrations:SpotifyIntegration",
    # "slack":   "sage.core.service_integrations:SlackIntegration",
}


__all__ = [
    "ServiceIntegration",
    "IntegrationStore",
    "GitHubIntegration",
    "OAuthCallbackError",
    "INTEGRATION_REGISTRY",
]
