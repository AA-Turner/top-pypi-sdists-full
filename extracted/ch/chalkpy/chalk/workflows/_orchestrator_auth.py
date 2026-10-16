"""Bearer tokens for authenticated workflow orchestrators, kept fresh on long-lived clients.

A shared orchestrator authenticates every Temporal RPC with `authorization: Bearer <token>`
metadata. The token comes from one of two places, both of which expire:

- In-cluster, a projected Kubernetes service-account token in the file named by
  CHALK_WORKFLOW_ORCHESTRATOR_TOKEN_FILE. The kubelet rewrites it before it expires, so
  the file is re-read every minute.
- Outside the cluster, the `accessToken` the Chalk API server returns with the connection
  details: a JWT valid for an hour, fetched again shortly before its `exp`.

Orchestrators that return neither (hosted, per-environment ones) are dialed as before.
"""

from __future__ import annotations

import asyncio
import base64
import binascii
import contextlib
import json
import logging
import time
from typing import TYPE_CHECKING, Any, AsyncIterator, Callable, Mapping, Protocol

if TYPE_CHECKING:
    from temporalio.client import Client

_logger = logging.getLogger(__name__)

TOKEN_FILE_ENV_VAR = "CHALK_WORKFLOW_ORCHESTRATOR_TOKEN_FILE"

# The contract requires a re-read at least every 5 minutes; reading a small file is cheap.
_TOKEN_FILE_REREAD_SECONDS = 60.0
# Access tokens are fetched again this long before they expire.
_ACCESS_TOKEN_REFRESH_MARGIN_SECONDS = 300.0
# Floor between refresh attempts, so a failing refresh of an expiring token retries
# periodically rather than in a tight loop.
_MIN_REFRESH_DELAY_SECONDS = 30.0


class OrchestratorToken(Protocol):
    """The current bearer token for an orchestrator, and how to replace it."""

    @property
    def token(self) -> str: ...

    def seconds_until_refresh(self) -> float | None:
        """How long the current token can be used before `refresh`; None if it never needs one."""
        ...

    def refresh(self) -> bool:
        """Replace the token, blocking. Returns whether it changed.

        Raises if no new token could be obtained, leaving the last good token current.
        """
        ...


class TokenFile:
    """A token read from a file that something else (the kubelet) keeps current."""

    def __init__(self, path: str) -> None:
        super().__init__()
        self._path = path
        try:
            self._token = self._read()
        except (OSError, ValueError) as e:
            raise RuntimeError(f"Cannot read the workflow orchestrator token from {TOKEN_FILE_ENV_VAR}: {e}") from e

    @property
    def token(self) -> str:
        return self._token

    def _read(self) -> str:
        with open(self._path, encoding="utf-8") as f:
            token = f.read().strip()
        if not token:
            raise ValueError(f"{self._path} is empty")
        return token

    def seconds_until_refresh(self) -> float | None:
        return _TOKEN_FILE_REREAD_SECONDS

    def refresh(self) -> bool:
        token = self._read()
        changed = token != self._token
        self._token = token
        return changed


class AccessToken:
    """A JWT from the Chalk API server, fetched again through `fetch` before its `exp`."""

    def __init__(self, token: str, fetch: Callable[[], str | None]) -> None:
        super().__init__()
        self._token = token
        self._fetch = fetch

    @property
    def token(self) -> str:
        return self._token

    def seconds_until_refresh(self) -> float | None:
        exp = jwt_expiry(self._token)
        if exp is None:
            return None
        return exp - _ACCESS_TOKEN_REFRESH_MARGIN_SECONDS - time.time()

    def refresh(self) -> bool:
        token = self._fetch()
        if not token:
            raise RuntimeError("the Chalk API server returned no workflow orchestrator access token")
        changed = token != self._token
        self._token = token
        return changed


def jwt_expiry(token: str) -> float | None:
    """The `exp` claim of a JWT, read without verifying the signature; None if it has none."""
    parts = token.split(".")
    if len(parts) != 3:
        return None
    payload = parts[1]
    try:
        claims = json.loads(base64.urlsafe_b64decode(payload + "=" * (-len(payload) % 4)))
    except (binascii.Error, UnicodeDecodeError, ValueError):
        return None
    exp = claims.get("exp") if isinstance(claims, dict) else None  # pyright: ignore[reportUnknownMemberType]
    if isinstance(exp, bool) or not isinstance(exp, (int, float)):
        return None
    return float(exp)


def orchestrator_token(
    *,
    token_file: str | None,
    access_token: str | None,
    fetch_access_token: Callable[[], str | None],
) -> OrchestratorToken | None:
    """The token to authenticate with, or None for an orchestrator that takes none."""
    if token_file:
        return TokenFile(token_file)
    if access_token:
        return AccessToken(access_token, fetch_access_token)
    return None


class _HasRpcMetadata(Protocol):
    """`temporalio.client.Client`'s metadata property; its value type varies across versions."""

    @property
    def rpc_metadata(self) -> Mapping[str, Any]: ...

    @rpc_metadata.setter
    def rpc_metadata(self, value: Mapping[str, Any]) -> None: ...


async def keep_token_fresh(client: _HasRpcMetadata, token: OrchestratorToken) -> None:
    """Refresh `token` on its schedule until cancelled, updating the client's `authorization` metadata.

    Setting `Client.rpc_metadata` (temporalio >= 1.7) replaces the headers of the connection
    that the client and every worker created from it share, so each later RPC, worker polls
    included, carries the new token.
    """
    while True:
        delay = token.seconds_until_refresh()
        if delay is None:
            return
        await asyncio.sleep(max(delay, _MIN_REFRESH_DELAY_SECONDS))
        try:
            if await asyncio.to_thread(token.refresh):
                client.rpc_metadata = {**client.rpc_metadata, "authorization": f"Bearer {token.token}"}
        except Exception as e:
            # The last good token may still be valid; the next attempt comes after the delay floor.
            _logger.warning("Keeping the current workflow orchestrator token; refreshing it failed: %s", e)


@contextlib.asynccontextmanager
async def connect_with_token(
    address: str,
    namespace: str,
    *,
    use_tls: bool,
    bearer_token: str | None,
    environment_id: str | None,
    token: OrchestratorToken | None,
) -> AsyncIterator[Client]:
    """Connect to the orchestrator, authenticating with `token` (kept fresh while the context is
    open) when there is one, and with `bearer_token` otherwise."""
    from chalk.workflows._temporal import connect_workflow_orchestrator

    client = await connect_workflow_orchestrator(
        address,
        namespace,
        use_tls=use_tls,
        bearer_token=token.token if token is not None else bearer_token,
        environment_id=environment_id,
    )
    if token is None:
        yield client
        return
    refresher = asyncio.create_task(keep_token_fresh(client, token))
    try:
        yield client
    finally:
        refresher.cancel()
        with contextlib.suppress(asyncio.CancelledError):
            await refresher
