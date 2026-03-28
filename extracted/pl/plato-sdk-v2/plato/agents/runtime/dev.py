"""Dev mode code sync helpers for agent VMs."""

from __future__ import annotations

import logging
import shlex
from pathlib import Path

from plato.agents.runtime.transport import rsync_to
from plato.utils.pypi_index import plato_token_simple_index
from plato.utils.subprocess import run_ssh

logger = logging.getLogger(__name__)


def _find_agent_code(agent_code_path: Path | None, package_name: str | None) -> Path | None:
    """Find the agent code directory, matching by package name if multiple agents exist."""
    if agent_code_path:
        return agent_code_path

    agents_dir = Path("/agents")
    if not agents_dir.exists():
        return None

    agent_dirs = [d for d in agents_dir.iterdir() if d.is_dir() and (d / "pyproject.toml").exists()]
    if not agent_dirs:
        return None

    # Match by package name from image URL
    if package_name:
        import tomllib

        for d in agent_dirs:
            try:
                with open(d / "pyproject.toml", "rb") as f:
                    pyproject = tomllib.load(f)
                project_name = pyproject.get("project", {}).get("name", "")
                if project_name == package_name:
                    logger.debug(f"Matched agent code {d} by package name '{package_name}'")
                    return d
            except Exception:
                continue

    # If only one agent and no package_name filter, use it
    if len(agent_dirs) == 1 and not package_name:
        return agent_dirs[0]

    return None


async def sync_dev_code(
    ssh_key: Path,
    hostname: str,
    agent_code_path: Path | None,
    package_name: str | None = None,
) -> bool:
    """Sync SDK + agent code to VM and install in editable mode (dev mode)."""
    sdk_path = Path("/sdk")
    editable_paths: list[str] = []
    agent_synced = False

    logger.debug(f"Syncing SDK: {sdk_path} -> /sdk")
    await rsync_to(ssh_key, sdk_path, "/sdk", hostname)
    editable_paths.append("/sdk")

    # Find the right agent code directory
    agent_code_path = _find_agent_code(agent_code_path, package_name)

    if agent_code_path and agent_code_path.exists():
        logger.debug(f"Syncing agent code: {agent_code_path} -> /app")
        await rsync_to(ssh_key, agent_code_path, "/app", hostname)
        editable_paths.append("/app")
        agent_synced = True
    else:
        logger.info(
            "No synced dev agent code found under /agents for package '%s'; "
            "SDK will be editable-only and runtime should install production agent package.",
            package_name or "",
        )

    editables = " ".join(f"-e {p}" for p in editable_paths)
    logger.debug(f"Installing packages in editable mode: {editable_paths}")
    store_idx = plato_token_simple_index("pypi-store")
    pip_cmd = f"uv pip install --system --index-url {shlex.quote(store_idx)} {editables}"
    exit_code, stdout, stderr = await run_ssh(ssh_key, hostname, pip_cmd, timeout=300)
    if exit_code != 0:
        raise RuntimeError(f"Failed to install packages: {stderr or stdout}")

    # Also update the plato CLI tool so agent VMs have the latest CLI commands
    # (the base image may have an old version baked in).
    # Include the agent package (--with -e /app) so entry points are discoverable
    # by plato-agent-runner in the tool's isolated environment.
    tool_cmd = f"uv tool install -e /sdk --force --python 3.12 --index-url {shlex.quote(store_idx)}"
    if agent_synced:
        tool_cmd += " --with-editable /app"
    exit_code, stdout, stderr = await run_ssh(
        ssh_key,
        hostname,
        tool_cmd,
        timeout=120,
    )
    if exit_code != 0:
        logger.warning("Failed to update plato CLI tool: %s", stderr or stdout)

    return agent_synced


def build_agent_install_command(package_name: str, version: str) -> str:
    """Build the uv command to install an agent package on a VM.

    Uses ``--default-index`` for pypi-store (SDK + public PyPI deps) and
    ``--index`` for the agents registry (checked first so agent packages
    take priority over any public PyPI name collision).
    ``unsafe-best-match`` is intentionally omitted so uv uses first-match
    strategy — each package resolves from the first index that has it.
    """
    store_url = plato_token_simple_index("pypi-store")
    agents_url = plato_token_simple_index("agents")
    return (
        f"uv tool install plato-sdk-v2 --python 3.12 "
        f"--with '{package_name}=={version}' "
        f"--default-index {shlex.quote(store_url)} "
        f"--index {shlex.quote(agents_url)} "
        f"--prerelease allow --refresh --force"
    )


async def install_production_agent(
    ssh_key: Path,
    hostname: str,
    package_name: str,
    version: str,
    max_retries: int = 3,
    retry_delay: float = 10.0,
) -> None:
    """Install agent package from PyPI on VM (production mode)."""
    logger.debug(f"Installing agent package: {package_name}=={version}")
    # UV_HTTP_TIMEOUT: bump from default 30s — the plato.so PyPI index
    # intermittently takes longer to respond, causing uv's internal retries
    # to exhaust before a response arrives.
    install_cmd = f"UV_HTTP_TIMEOUT=90 {build_agent_install_command(package_name, version)}"

    last_error = ""
    for attempt in range(1, max_retries + 1):
        exit_code, stdout, stderr = await run_ssh(ssh_key, hostname, install_cmd, user="root", timeout=300)
        if exit_code == 0:
            return
        last_error = stderr or stdout
        if attempt < max_retries:
            logger.warning(
                "Agent install failed (attempt %d/%d), retrying in %.0fs: %s",
                attempt,
                max_retries,
                retry_delay,
                last_error.strip(),
            )
            import asyncio

            await asyncio.sleep(retry_delay)

    raise RuntimeError(f"Failed to install agent package after {max_retries} attempts: {last_error}")
