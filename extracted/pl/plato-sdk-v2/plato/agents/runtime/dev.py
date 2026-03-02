"""Dev mode code sync helpers for agent VMs."""

from __future__ import annotations

import logging
import os
from pathlib import Path

from plato.agents.runtime.workspace import rsync_to
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

    # If only one agent, use it
    if len(agent_dirs) == 1:
        return agent_dirs[0]

    # Multiple agents: match by package name from image URL
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

    # Fallback to first
    return agent_dirs[0]


async def sync_dev_code(
    ssh_key: Path,
    hostname: str,
    agent_code_path: Path | None,
    package_name: str | None = None,
) -> None:
    """Sync SDK + agent code to VM and install in editable mode (dev mode)."""
    sdk_path = Path("/sdk")
    editable_paths: list[str] = []

    logger.debug(f"Syncing SDK: {sdk_path} -> /sdk")
    await rsync_to(ssh_key, sdk_path, "/sdk", hostname, chown="superman:superman")
    editable_paths.append("/sdk")

    # Find the right agent code directory
    agent_code_path = _find_agent_code(agent_code_path, package_name)

    if agent_code_path and agent_code_path.exists():
        logger.debug(f"Syncing agent code: {agent_code_path} -> /app")
        await rsync_to(ssh_key, agent_code_path, "/app", hostname, chown="superman:superman")
        editable_paths.append("/app")

    editables = " ".join(f"-e {p}" for p in editable_paths)
    logger.debug(f"Installing packages in editable mode: {editable_paths}")
    exit_code, stdout, stderr = await run_ssh(ssh_key, hostname, f"uv pip install --system {editables}", timeout=300)
    if exit_code != 0:
        raise RuntimeError(f"Failed to install packages: {stderr or stdout}")


async def install_production_agent(
    ssh_key: Path,
    hostname: str,
    package_name: str,
    version: str,
) -> None:
    """Install agent package from PyPI on VM (production mode)."""
    logger.debug(f"Installing agent package: {package_name}=={version}")

    # Fix uv cache/tools ownership (may have been created by root)
    await run_ssh(
        ssh_key,
        hostname,
        "rm -rf /home/superman/.cache/uv /home/superman/.local/share/uv && "
        "mkdir -p /home/superman/.cache/uv /home/superman/.local/share/uv /home/superman/.local/bin && "
        "chown -R superman:superman /home/superman/.cache /home/superman/.local",
        timeout=30,
    )

    api_key = os.environ.get("PLATO_API_KEY", "")
    pypi_url = f"https://__token__:{api_key}@plato.so/api/v2/pypi/agents/simple/"

    install_cmd = (
        f"uv tool install plato-sdk-v2 --python 3.12 "
        f"--with '{package_name}=={version}' "
        f"--index-url 'https://pypi.org/simple/' "
        f"--extra-index-url '{pypi_url}' "
        f"--index-strategy unsafe-best-match --prerelease allow --refresh --force"
    )
    exit_code, stdout, stderr = await run_ssh(ssh_key, hostname, install_cmd, user="superman", timeout=300)
    if exit_code != 0:
        raise RuntimeError(f"Failed to install agent package: {stderr or stdout}")
