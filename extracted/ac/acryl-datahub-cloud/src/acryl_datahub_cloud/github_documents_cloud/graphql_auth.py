"""Mint GitHub App installation access tokens via a GMS GraphQL proxy.

The ingestion executor never holds the GitHub App signing key. Instead it asks
GMS for a short-lived installation access token; GMS proxies the request to the
integrations service, which signs and brokers it with cloud-router. This keeps
all GitHub credentials server-side.
"""

from __future__ import annotations

import logging
import threading
import time
from datetime import datetime
from typing import TYPE_CHECKING, Optional, Tuple

if TYPE_CHECKING:
    from datahub.ingestion.graph.client import DataHubGraph

logger = logging.getLogger(__name__)

# Refresh tokens before GitHub's ~1h expiry so long runs never use an expired
# token mid-request.
TOKEN_REFRESH_BUFFER_SECONDS = 300

_GET_TOKEN_QUERY = """
query getGitHubInstallationAccessToken {
  getGitHubInstallationAccessToken {
    token
    expiresAt
  }
}
"""


class GraphQLTokenError(Exception):
    """DataHub failed to return a GitHub installation access token."""


class GraphQLInstallationTokenProvider:
    """``GitHubTokenProvider`` backed by the GMS ``getGitHubInstallationAccessToken`` query.

    Implements the OSS ``GitHubTokenProvider`` protocol (``get_token()``) so it
    drops into the OSS ``GitHubApiClient`` unchanged. Tokens are cached until
    shortly before expiry to avoid a GraphQL round-trip per GitHub request.
    """

    def __init__(self, graph: "DataHubGraph") -> None:
        self._graph = graph
        self._lock = threading.Lock()
        self._cached_token: Optional[str] = None
        self._expires_at_epoch: float = 0.0

    def get_token(self) -> str:
        with self._lock:
            now = time.time()
            if (
                self._cached_token is not None
                and now < self._expires_at_epoch - TOKEN_REFRESH_BUFFER_SECONDS
            ):
                return self._cached_token

            token, expires_at_epoch = self._request_token()
            self._cached_token = token
            self._expires_at_epoch = expires_at_epoch
            return token

    def _request_token(self) -> Tuple[str, float]:
        try:
            data = self._graph.execute_graphql(query=_GET_TOKEN_QUERY)
        except Exception as exc:
            raise GraphQLTokenError(
                "Failed to obtain a GitHub installation access token from DataHub. "
                "Ensure the GitHub App is installed for this tenant and that the "
                "ingestion executor has the 'Manage Connections' privilege. "
                f"Underlying error: {exc}"
            ) from exc

        result = (data or {}).get("getGitHubInstallationAccessToken") or {}
        token = result.get("token")
        if not token:
            raise GraphQLTokenError(
                "DataHub returned no GitHub installation access token. Verify the "
                "GitHub App is installed for this tenant (Settings > Integrations "
                "> GitHub)."
            )
        expires_at_epoch = _parse_github_expires_at(result.get("expiresAt"))
        logger.debug("Fetched GitHub installation access token from DataHub GraphQL")
        return token, expires_at_epoch


def _parse_github_expires_at(expires_at: Optional[str]) -> float:
    """Parse GitHub's ISO-8601 expiry; fall back to a 1h window if absent."""
    if not expires_at:
        return time.time() + 3600
    try:
        normalized = expires_at.replace("Z", "+00:00")
        return datetime.fromisoformat(normalized).timestamp()
    except ValueError:
        return time.time() + 3600
