"""
Configuration utilities for telemetry system.

This module provides functionality to download and cache telemetry configuration
from a remote server.
"""

from __future__ import annotations

import logging
import os

from typing import Any, Dict

import requests
from tabpfn_common_utils.utils import ttl_cache


logger = logging.getLogger(__name__)


@ttl_cache(ttl_seconds=60 * 60)
def download_config() -> Dict[str, Any]:
    """Download the configuration from server.

    If the configuration cannot be fetched or parsed (network error, non-200
    response, malformed JSON) the function returns a fail-closed default of
    ``{"enabled": False}`` so that telemetry is not emitted from clients that
    cannot reach the public configuration endpoint.

    Returns:
        Dict[str, Any]: The configuration.
    """
    # Fail-closed default: when we can't reach or parse the remote
    # configuration, treat telemetry as disabled. Respects users on restrictive
    # networks (firewalls, air-gapped environments) and avoids emitting events
    # under any state other than an explicit, server-confirmed enable.
    default = {"enabled": False}

    # This is a public URL anyone can and should read from
    url = os.environ.get(
        "TABPFN_TELEMETRY_CONFIG_URL",
        "https://storage.googleapis.com/prior-labs-tabpfn-public/config/telemetry.json",
    )
    try:
        # We use a very short timeout to avoid blocking the main thread
        resp = requests.get(url, timeout=0.25)
    except Exception:
        logger.debug(f"Failed to download telemetry config: {url}")
        return default

    if resp.status_code != 200:
        logger.debug(f"Failed to download telemetry config: {resp.status_code}")
        return default

    try:
        config = resp.json()
    except ValueError:
        logger.debug(f"Failed to parse telemetry config JSON from: {url}")
        return default

    # Validate the shape: anything other than a dict containing "enabled" would
    # cause a TypeError/KeyError in downstream `config["enabled"]` access. Fail
    # closed so a malformed remote response cannot crash the host process.
    if not isinstance(config, dict) or "enabled" not in config:
        logger.debug(
            f"Telemetry config from {url} is malformed or missing 'enabled' key"
        )
        return default

    return config
