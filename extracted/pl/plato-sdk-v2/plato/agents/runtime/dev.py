"""Editable dev-mode sync helpers for agent VMs."""

from __future__ import annotations

import logging
import shlex
import time
from pathlib import Path

from plato.agents.runtime.install import build_editable_sdk_install_command
from plato.transports.rsync import rsync_to
from plato.utils.pypi_index import plato_token_simple_index
from plato.utils.subprocess import run_ssh

logger = logging.getLogger(__name__)


async def sync_dev_code(
    ssh_key: Path,
    hostname: str,
    agent_code_path: Path | None,
    package_name: str | None = None,
    version: str | None = None,
) -> bool:
    """Sync SDK + agent code to VM and install in editable mode (dev mode)."""
    t_total = time.monotonic()
    sdk_path = Path("/sdk")
    editable_paths: list[str] = []
    agent_synced = False

    t0 = time.monotonic()
    logger.info("Syncing SDK to %s: %s -> /sdk", hostname, sdk_path)
    await rsync_to(ssh_key, sdk_path, "/sdk", hostname)
    logger.info("SDK rsync to %s took %.1fs", hostname, time.monotonic() - t0)
    editable_paths.append("/sdk")

    if agent_code_path and agent_code_path.exists():
        t0 = time.monotonic()
        logger.info("Syncing agent code to %s: %s -> /app", hostname, agent_code_path)
        await rsync_to(ssh_key, agent_code_path, "/app", hostname)
        logger.info("Agent rsync to %s took %.1fs", hostname, time.monotonic() - t0)
        editable_paths.append("/app")
        agent_synced = True
    elif agent_code_path:
        logger.warning(
            "Explicit dev agent code path does not exist: %s. "
            "SDK will be editable-only and runtime should install the production agent package.",
            agent_code_path,
        )
    else:
        logger.info(
            "No explicit dev agent code path provided; "
            "SDK will be editable-only and runtime should install the production agent package.",
        )

    editables = " ".join(f"-e {p}" for p in editable_paths)
    store_idx = plato_token_simple_index("pypi-store")
    pip_cmd = f"uv pip install --system --index-url {shlex.quote(store_idx)} {editables}"
    t0 = time.monotonic()
    logger.info("Installing editable packages on %s: %s", hostname, editable_paths)
    exit_code, stdout, stderr = await run_ssh(ssh_key, hostname, pip_cmd, timeout=300)
    logger.info("Editable pip install on %s took %.1fs", hostname, time.monotonic() - t0)
    if exit_code != 0:
        raise RuntimeError(f"Failed to install packages: {stderr or stdout}")

    # Also update the plato CLI tool so agent VMs have the latest CLI commands
    # (the base image may have an old version baked in).
    # Include the agent package (--with -e /app) so entry points are discoverable
    # by plato-agent-runner in the tool's isolated environment.
    tool_cmd = f"uv tool install -e /sdk --force --python 3.12 --index-url {shlex.quote(store_idx)}"
    if agent_synced:
        tool_cmd += " --with-editable /app"
    elif package_name and version:
        tool_cmd = build_editable_sdk_install_command(package_name, version)
    t0 = time.monotonic()
    logger.info("Updating plato CLI tool on %s", hostname)
    exit_code, stdout, stderr = await run_ssh(
        ssh_key,
        hostname,
        tool_cmd,
        timeout=120,
    )
    logger.info("Plato CLI tool install on %s took %.1fs", hostname, time.monotonic() - t0)
    if exit_code != 0:
        logger.warning("Failed to update plato CLI tool: %s", stderr or stdout)

    logger.info("sync_dev_code total on %s: %.1fs", hostname, time.monotonic() - t_total)
    return agent_synced
