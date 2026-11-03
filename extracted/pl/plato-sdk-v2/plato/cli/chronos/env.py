"""Chronos analyzer-env resolution utilities.

Fetches ``chronos:analyzer-env`` settings (org + user scope) from the
Chronos API and substitutes ``${VAR}`` placeholders in config dicts.
This mirrors the server-side resolution done in the Chronos backend
launch flow (``api/jobs.py``).
"""

from __future__ import annotations

import logging
import re
from typing import Any

import httpx

from plato.chronos.api.settings import get_setting
from plato.cli.chronos.settings import get_settings

logger = logging.getLogger(__name__)

_ENV_VAR_PATTERN = re.compile(r"\$\{([A-Za-z_][A-Za-z0-9_]*)\}")


def substitute_env_vars(obj: Any, values: dict[str, str]) -> Any:
    """Replace ``${VAR}`` placeholders in all string values of a nested object.

    Returns a new object — does not mutate the input.
    """
    if isinstance(obj, str):
        return _ENV_VAR_PATTERN.sub(lambda m: values.get(m.group(1), m.group(0)), obj)
    if isinstance(obj, list):
        return [substitute_env_vars(item, values) for item in obj]
    if isinstance(obj, dict):
        return {k: substitute_env_vars(v, values) for k, v in obj.items()}
    return obj


async def fetch_analyzer_env(api_key: str | None = None) -> dict[str, str]:
    """Fetch analyzer-env settings from Chronos (org + user scope, merged).

    Returns a dict of ``{VAR_NAME: value}`` for use with :func:`substitute_env_vars`.
    """
    settings = get_settings()
    env_values: dict[str, str] = {}

    async with httpx.AsyncClient(
        base_url=settings.chronos_url.rstrip("/"),
        timeout=30.0,
        headers={"X-API-Key": api_key} if api_key else {},
    ) as client:
        for scope in ("org", "user"):
            try:
                resp = await get_setting.asyncio(client, key="chronos:analyzer-env", scope=scope)
                if resp.value and isinstance(resp.value, dict):
                    env_values.update({k: str(v) for k, v in resp.value.items()})
            except Exception:
                logger.debug("Could not fetch analyzer-env (scope=%s)", scope)

    return env_values


async def resolve_config_env_vars(config: dict[str, Any], api_key: str | None = None) -> None:
    """Fetch analyzer-env from Chronos and substitute ``${VAR}`` placeholders in-place.

    Mirrors the Chronos backend launch flow. Mutates ``config`` in-place.
    """
    env_values = await fetch_analyzer_env(api_key)
    if not env_values:
        return

    logger.info(
        "Resolved %d env vars from Chronos: %s",
        len(env_values),
        ", ".join(sorted(env_values.keys())),
    )

    substituted = substitute_env_vars(config, env_values)
    if isinstance(substituted, dict):
        config.clear()
        config.update(substituted)
