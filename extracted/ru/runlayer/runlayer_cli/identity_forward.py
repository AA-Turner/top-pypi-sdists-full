"""Identity-forward header injection on the CLI local-proxy path.

For hosted servers the backend adds ``X-Runlayer-*`` identity headers when
it connects upstream. For ``deployment_mode = LOCAL`` servers the CLI owns
the upstream connection, so the backend instead hands the headers over on
the server-details read (``ServerDetails.identity_forward``) and this
module injects them client-side.

Invariants:

- A ``None`` bundle (stdio, toggles off, older backend) is a no-op.
- Refresh failures never kill the proxy; upstream just sees stale or
  missing identity headers, same as if the toggle were off.
- Only signed bundles refresh — unsigned headers don't expire.
- The refresh loop mutates the dict the transport was built with; fastmcp
  re-reads it at session (re)connect, so a fresh token lands on the next
  reconnect, not mid-session (INT-415).
"""

from __future__ import annotations

import time
from typing import TYPE_CHECKING

import anyio
import anyio.to_thread
import structlog

from runlayer_cli.models_api import IdentityForwardBundle

if TYPE_CHECKING:
    from runlayer_cli.api import RunlayerClient

logger = structlog.get_logger(__name__)

# Names the backend can mint (mirrors
# ``RESERVED_IDENTITY_HEADERS`` on the backend). Kept as an explicit
# lowercased set so refresh replaces exactly the previous mint and doesn't
# accidentally clobber unrelated ``X-Runlayer-*`` transport headers.
_RESERVED_HEADER_NAMES: frozenset[str] = frozenset(
    h.lower()
    for h in (
        "X-Runlayer-Subject-Type",
        "X-Runlayer-Org-Id",
        "X-Runlayer-User-Email",
        "X-Runlayer-User-Id",
        "X-Runlayer-Agent-Id",
        "X-Runlayer-Agent-Name",
        "X-Runlayer-Identity-Token",
    )
)

# Refresh a signed token this many seconds before its ``exp`` so an in-flight
# request never races the clock. TOKEN_TTL_SECONDS on the backend is 300s,
# so a 60s buffer leaves 240s between refreshes worst case.
_REFRESH_BUFFER_SECONDS = 60

# Bounds on the interval anyway. Guard against a pathologically short TTL
# (defensive; the backend fixes TTL) or a bundle that already expired at
# fetch time.
_MIN_REFRESH_SLEEP_SECONDS = 5
_MAX_REFRESH_SLEEP_SECONDS = 3600

# On refresh failure, back off with jitter. Fixed schedule (not exponential)
# because the token has already been minted; we're just trying to swap it
# before expiry. Short retries maximize the odds of getting a fresh one in
# the remaining window.
_REFRESH_RETRY_SLEEP_SECONDS = 15.0


def merge_bundle_into_headers(
    headers: dict[str, str], bundle: IdentityForwardBundle | None
) -> None:
    """Replace the reserved-name slice of ``headers`` with ``bundle``.

    Strip-then-add, so a previous mint can never linger next to a fresh
    one. ``None`` just strips.
    """
    for name in list(headers):
        if name.lower() in _RESERVED_HEADER_NAMES:
            del headers[name]
    if bundle is not None and bundle.applied:
        headers.update(bundle.headers)


def _fetch_bundle(client: RunlayerClient, server_id: str) -> IdentityForwardBundle:
    """Re-read the server details and pull out the bundle.

    An absent field (toggle turned off mid-session, downgraded backend)
    becomes an unapplied bundle so the loop's downgrade path covers both.
    """
    details = client.get_server_details(server_id)
    return details.identity_forward or IdentityForwardBundle()


def _seconds_until_refresh(expires_at: int) -> float:
    now = time.time()
    target = expires_at - _REFRESH_BUFFER_SECONDS
    remaining = max(target - now, _MIN_REFRESH_SLEEP_SECONDS)
    return min(remaining, _MAX_REFRESH_SLEEP_SECONDS)


async def refresh_loop(
    client: RunlayerClient,
    server_id: str,
    initial_bundle: IdentityForwardBundle,
    headers: dict[str, str],
) -> None:
    """Keep a signed identity token fresh for the proxy's lifetime.

    Runs in the proxy's task group; cancelled when the proxy exits.
    No-op unless the initial bundle carries an ``expires_at``.
    """
    if not initial_bundle.applied or initial_bundle.expires_at is None:
        return

    expires_at = initial_bundle.expires_at
    while True:
        await anyio.sleep(_seconds_until_refresh(expires_at))
        try:
            bundle = await anyio.to_thread.run_sync(_fetch_bundle, client, server_id)
        except Exception as exc:  # noqa: BLE001 — must never kill the proxy task group
            logger.warning(
                "identity_forward_refresh_failed",
                server_id=server_id,
                error=str(exc),
                error_type=type(exc).__name__,
            )
            await anyio.sleep(_REFRESH_RETRY_SLEEP_SECONDS)
            continue

        merge_bundle_into_headers(headers, bundle)
        if not bundle.applied or bundle.expires_at is None:
            # Admin turned the toggle off (or downgraded to unsigned-only)
            # mid-session. Stop refreshing — nothing to keep fresh.
            logger.info(
                "identity_forward_refresh_stopped",
                server_id=server_id,
                reason="bundle_no_longer_signed",
            )
            return
        expires_at = bundle.expires_at
        logger.debug(
            "identity_forward_refreshed",
            server_id=server_id,
            expires_at=expires_at,
        )
