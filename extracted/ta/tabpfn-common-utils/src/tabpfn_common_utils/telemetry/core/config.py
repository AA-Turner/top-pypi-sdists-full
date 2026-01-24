"""
Configuration utilities for telemetry system.

This module provides functionality to download and cache telemetry configuration
from a remote server.
"""

from __future__ import annotations

import logging
import os

from datetime import datetime, timezone
from typing import Any, Dict

import requests
from tabpfn_common_utils.utils import ttl_cache


logger = logging.getLogger(__name__)


@ttl_cache(ttl_seconds=60 * 5)
def download_config() -> Dict[str, Any]:
    """Download the configuration from server.

    Returns:
        Dict[str, Any]: The configuration.
    """
    # Bust the cache
    params = {
        "timestamp": datetime.now(tz=timezone.utc).isoformat(),
    }

    # The default configuration
    default = {"enabled": False}

    # This is a public URL anyone can and should read from
    url = os.environ.get(
        "TABPFN_TELEMETRY_CONFIG_URL",
        "https://storage.googleapis.com/prior-labs-tabpfn-public/config/telemetry.json",
    )
    try:
        resp = requests.get(url, params=params)
    except Exception:
        logger.debug(f"Failed to download telemetry config: {url}")
        return default

    # Disable telemetry by default
    if resp.status_code != 200:
        logger.debug(f"Failed to download telemetry config: {resp.status_code}")
        return default

    return resp.json()
