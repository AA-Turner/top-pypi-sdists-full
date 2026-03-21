"""Registry client for fetching world/agent schemas from PyPI."""

from __future__ import annotations

import logging
import os
from typing import Any

import httpx

logger = logging.getLogger(__name__)

REGISTRY_URL = "https://plato.so"


def _get_registry_url() -> str:
    """Get registry URL from environment or default."""
    return os.environ.get("PLATO_REGISTRY_URL", REGISTRY_URL)


def _get_api_key() -> str | None:
    """Get API key from environment."""
    return os.environ.get("PLATO_API_KEY")


async def get_world_schema(
    package_name: str,
    version: str | None = None,
    world_name: str | None = None,
) -> dict[str, Any]:
    """Fetch world schema from the registry.

    Args:
        package_name: World package name (e.g., "plato-world-structured-execution")
        version: Optional version. If not specified, uses latest.
        world_name: Optional world name for multi-world packages.

    Returns:
        Schema dict with keys: name, version, config_schema, secrets_schema, image

    Raises:
        RuntimeError: If schema cannot be fetched
    """
    api_key = _get_api_key()
    if not api_key:
        raise RuntimeError("PLATO_API_KEY required to fetch world schema")

    base_url = _get_registry_url()

    # Build URL with optional version
    url = f"{base_url}/api/v2/pypi/worlds/packages/{package_name}/schema"
    if version:
        url += f"?version={version}"

    headers = {"X-API-Key": api_key}

    async with httpx.AsyncClient(timeout=30.0) as client:
        response = await client.get(url, headers=headers)
        if response.status_code == 404:
            raise RuntimeError(f"World package not found: {package_name}")
        response.raise_for_status()
        data = response.json()

        # Handle catalog format: {"worlds": {"name": {schema...}}}
        if "worlds" in data and isinstance(data["worlds"], dict):
            worlds = data["worlds"]
            # If world_name specified, use it directly
            if world_name and world_name in worlds:
                return worlds[world_name]
            if len(worlds) == 1:
                return next(iter(worlds.values()))
            # Multiple worlds — find the primary (non-review) world
            for _name, schema in worlds.items():
                if schema.get("type", "world") != "review":
                    return schema
            return next(iter(worlds.values()))

        return data


async def get_agent_schema(package_name: str, version: str | None = None) -> dict[str, Any]:
    """Fetch agent schema from the registry.

    Args:
        package_name: Agent package name (e.g., "claude-code")
        version: Optional version. If not specified, uses latest.

    Returns:
        Schema dict with keys: name, version, config_schema, secrets_schema, image

    Raises:
        RuntimeError: If schema cannot be fetched
    """
    api_key = _get_api_key()
    if not api_key:
        raise RuntimeError("PLATO_API_KEY required to fetch agent schema")

    base_url = _get_registry_url()

    # Build URL with optional version
    url = f"{base_url}/api/v2/pypi/agents/packages/{package_name}/schema"
    if version:
        url += f"?version={version}"

    headers = {"X-API-Key": api_key}

    async with httpx.AsyncClient(timeout=30.0) as client:
        response = await client.get(url, headers=headers)
        if response.status_code == 404:
            raise RuntimeError(f"Agent package not found: {package_name}")
        response.raise_for_status()
        return response.json()


def parse_package_string(package_string: str) -> tuple[str, str | None]:
    """Parse package:version string into (package, version) tuple.

    Args:
        package_string: Package string like "plato-world-foo:0.1.0" or just "plato-world-foo"

    Returns:
        Tuple of (package_name, version) where version may be None
    """
    if ":" in package_string:
        name, version = package_string.split(":", 1)
        if not version or version == "latest":
            return name, None
        return name, version
    return package_string, None
