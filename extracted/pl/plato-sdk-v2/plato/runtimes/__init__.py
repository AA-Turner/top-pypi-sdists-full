"""Runtime backends for executing Plato worlds.

A runtime manages the lifecycle of a VM or container where a world runs.
Each runtime implements ``start``, ``stop``, and ``exec`` so the rest of the
system can provision, connect to, and tear down execution environments
uniformly.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

from plato.runtimes.base import Runtime, RuntimeInfo
from plato.runtimes.config import (
    AppleRuntimeConfig,
    RuntimeConfig,
    VMRuntimeConfig,
)
from plato.runtimes.settings import RuntimeSettings, get_settings

__all__ = [
    "AppleRuntimeConfig",
    "Runtime",
    "RuntimeConfig",
    "RuntimeInfo",
    "RuntimeSettings",
    "VMRuntimeConfig",
    "create_runtime",
    "get_settings",
]


def create_runtime(
    config: VMRuntimeConfig | AppleRuntimeConfig,
    *,
    session: Any = None,
    ssh_key_path: Path | None = None,
) -> Runtime:
    """Instantiate the right Runtime from a config.

    Args:
        config: A runtime config (vm or apple).
        session: Plato session (required for vm).
        ssh_key_path: SSH key path (required for vm).

    Returns:
        A Runtime instance ready to ``start()``.
    """
    if isinstance(config, VMRuntimeConfig):
        from plato.runtimes.vm import VMRuntime

        if session is None:
            raise ValueError("VMRuntimeConfig requires a session")
        if ssh_key_path is None:
            raise ValueError("VMRuntimeConfig requires ssh_key_path")
        return VMRuntime(
            config.image,
            session=session,
            ssh_key_path=ssh_key_path,
            cpus=config.cpus,
            memory=config.memory,
            disk=config.disk,
            timeout=config.timeout,
            heartbeat_timeout=config.heartbeat_timeout,
        )

    if isinstance(config, AppleRuntimeConfig):
        from plato.runtimes.apple import AppleRuntime

        if ssh_key_path is None:
            raise ValueError("AppleRuntimeConfig requires ssh_key_path")
        return AppleRuntime(
            config.image,
            cpus=config.cpus,
            memory=config.memory,
            ssh_key_path=ssh_key_path,
            server_url=config.server_url,
        )

    raise ValueError(f"Unknown runtime config type: {type(config)}")
