# Copyright (c) 2025 Airbyte, Inc., all rights reserved.
"""Common utilities for interacting with 1Password via the `op` CLI.

Provides reusable helpers for creating share links and other vault
operations.  Requires the `op` CLI to be installed and
`OP_SERVICE_ACCOUNT_TOKEN` set in the environment.

Environment variables:
    `OP_SERVICE_ACCOUNT_TOKEN` — 1Password service account token with
    access to the target vault.
"""

from __future__ import annotations

import json
import logging
import subprocess

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

DEFAULT_VAULT_NAME = "devin-on-demand-secrets"
"""Default 1Password vault for on-demand secret sharing."""

DEFAULT_SHARE_EXPIRY = "5m"
"""Default expiry duration for share links."""


# ---------------------------------------------------------------------------
# Vault item listing
# ---------------------------------------------------------------------------


def list_vault_items(
    *,
    vault: str = DEFAULT_VAULT_NAME,
) -> list[str]:
    """List all item titles in a 1Password vault via the `op` CLI.

    Args:
        vault: Name of the 1Password vault to list items from.

    Returns:
        Sorted list of item titles available in the vault.

    Raises:
        RuntimeError: If `op item list` fails.
        subprocess.TimeoutExpired: If the `op` command exceeds the
            30-second timeout.
    """
    result = subprocess.run(
        [
            "op",
            "item",
            "list",
            "--vault",
            vault,
            "--format=json",
        ],
        capture_output=True,
        text=True,
        check=False,
        timeout=30,
    )
    if result.returncode != 0:
        raise RuntimeError(
            f"op item list failed (exit {result.returncode}): {result.stderr.strip()}"
        )
    try:
        items = json.loads(result.stdout)
    except json.JSONDecodeError as exc:
        raise RuntimeError(
            f"op item list returned invalid JSON: {exc}. stdout={result.stdout[:200]!r}"
        ) from exc
    titles = sorted(item["title"] for item in items if "title" in item)
    logger.info("Listed %d items in vault '%s'", len(titles), vault)
    return titles


# ---------------------------------------------------------------------------
# Share link creation
# ---------------------------------------------------------------------------


def create_share_link(
    secret_alias: str,
    *,
    vault: str = DEFAULT_VAULT_NAME,
    expiry: str = DEFAULT_SHARE_EXPIRY,
) -> str:
    """Create a time-limited 1Password share link via the `op` CLI.

    Runs `op item share` with `--expires-in` to produce a link that
    is automatically invalidated after the expiry duration.

    Note:
        `--view-once` is *not* used because the `op` CLI (when
        authenticated via a service-account token) rejects combining
        `--view-once` with `--expires-in`.  A short expiry window
        (default 5 minutes) limits exposure instead.

    Args:
        secret_alias: The title of the 1Password item to share.  Must
            exactly match an item in the target vault.
        vault: Name of the 1Password vault containing the item.
        expiry: How long the link remains valid (e.g. `"5m"`,
            `"1h"`).  Defaults to `"5m"`.

    Returns:
        The share link URL.

    Raises:
        RuntimeError: If `op item share` fails or returns empty
            output.
        subprocess.TimeoutExpired: If the `op` command exceeds the
            30-second timeout.
    """
    result = subprocess.run(
        [
            "op",
            "item",
            "share",
            secret_alias,
            "--vault",
            vault,
            "--expires-in",
            expiry,
        ],
        capture_output=True,
        text=True,
        check=False,
        timeout=30,
    )
    if result.returncode != 0:
        raise RuntimeError(
            f"op item share failed (exit {result.returncode}): {result.stderr.strip()}"
        )
    share_link = result.stdout.strip()
    if not share_link:
        raise RuntimeError("op item share returned empty output.")

    logger.info(
        "Created share link for '%s' (vault=%s, expires=%s)",
        secret_alias,
        vault,
        expiry,
    )
    return share_link
