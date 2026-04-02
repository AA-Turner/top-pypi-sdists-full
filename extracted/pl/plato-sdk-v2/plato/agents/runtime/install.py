"""Published-package install helpers for agent VMs."""

from __future__ import annotations

import logging
import shlex
import time
from pathlib import Path

from plato.utils.pypi_index import plato_token_simple_index
from plato.utils.subprocess import run_ssh

logger = logging.getLogger(__name__)


def parse_image_url(image: str) -> tuple[str, str]:
    """Extract package name and version from a Docker image URL."""
    last_part = image.split("/")[-1]
    if ":" in last_part:
        name, version = last_part.rsplit(":", 1)
        return name, version
    return last_part, "latest"


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
        f"--prerelease allow --force"
    )


def build_editable_sdk_install_command(package_name: str, version: str, sdk_path: str = "/sdk") -> str:
    """Build the uv command to install editable SDK plus a published agent package."""
    store_url = plato_token_simple_index("pypi-store")
    agents_url = plato_token_simple_index("agents")
    return (
        f"uv tool install -e {shlex.quote(sdk_path)} --python 3.12 "
        f"--with '{package_name}=={version}' "
        f"--default-index {shlex.quote(store_url)} "
        f"--index {shlex.quote(agents_url)} "
        f"--prerelease allow --force"
    )


async def install_production_agent(
    ssh_key: Path,
    hostname: str,
    package_name: str,
    version: str,
) -> None:
    """Install agent package from PyPI on VM."""
    logger.info("Installing agent package: %s==%s on %s", package_name, version, hostname)

    is_dev_version = ".dev" in version

    # Check if the agent package is already pre-baked into the VM image.
    # The Dockerfile stamps /opt/plato-agent-version with "package==version".
    # Dev publishes often reuse an existing image tag via `--skip-docker`, so
    # they must always reinstall from the package registry instead of trusting
    # the image stamp.
    if not is_dev_version:
        expected = f"{package_name}=={version}"
        check_rc, check_out, _ = await run_ssh(
            ssh_key, hostname, "cat /opt/plato-agent-version 2>/dev/null || true", timeout=5
        )
        if check_rc == 0 and check_out.strip() == expected:
            logger.info("Agent package %s already pre-baked on %s, skipping install", expected, hostname)
            return

    install_cmd = build_agent_install_command(package_name, version)

    t0 = time.monotonic()
    exit_code, stdout, stderr = await run_ssh(ssh_key, hostname, install_cmd, user="root", timeout=300)
    elapsed = time.monotonic() - t0
    if exit_code == 0:
        logger.info(
            "Agent install succeeded on %s: %.1fs\n%s",
            hostname,
            elapsed,
            (stderr or stdout or "").strip()[-500:],
        )
        return
    raise RuntimeError(f"Failed to install agent package: {stderr or stdout}")
