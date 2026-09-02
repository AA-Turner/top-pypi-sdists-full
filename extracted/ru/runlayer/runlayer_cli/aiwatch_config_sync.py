"""Best-effort settings reconciliation for the privileged hook scheduler."""

from __future__ import annotations

import httpx

from runlayer_cli.aiwatch_config_cache import write_backend_config
from runlayer_cli.api import RunlayerClient


def sync_backend_config(*, host: str, org_api_key: str) -> bool:
    """Fetch and persist desired settings without breaking local reconciliation."""
    try:
        config = RunlayerClient(
            hostname=host,
            secret=org_api_key,
        ).get_aiwatch_config()
        if config is None:
            return False
        return write_backend_config(config, org_api_key)
    except (httpx.HTTPError, OSError, ValueError):
        return False
