"""Published-package install helpers for agent VMs."""

from __future__ import annotations

import logging
import shlex
import time
from pathlib import Path

from plato.utils.pypi_index import plato_token_simple_index
from plato.utils.subprocess import VM_PATH_EXPORT, VM_VENV_PYTHON, run_ssh

logger = logging.getLogger(__name__)


VENV_PYTHON = VM_VENV_PYTHON


def _with_vm_path(command: str) -> str:
    return f"{VM_PATH_EXPORT}; {command}"


def _pip_package_spec(package_name: str, version: str | None) -> str:
    """Build a pip package specifier, omitting the version pin when unresolved."""
    if version:
        return f"'{package_name}=={version}'"
    return f"'{package_name}'"


def build_agent_install_command(package_name: str, version: str | None, *, upgrade_sdk: bool = True) -> str:
    """Build the uv commands to install an agent package on a VM.

    The base image has plato-sdk-v2 and all dependencies pre-installed in
    /opt/plato-venv. At runtime we:
    1. Optionally upgrade plato-sdk-v2 to latest from real PyPI.
    2. Install the agent package with --no-deps from the agents index.
    """
    agents_url = plato_token_simple_index("agents")
    pkg_spec = _pip_package_spec(package_name, version)
    commands: list[str] = []
    if upgrade_sdk:
        commands.append(f"uv pip install --python {VENV_PYTHON} plato-sdk-v2 --upgrade")
    commands.append(
        f"uv pip install --python {VENV_PYTHON} --no-deps "
        f"{pkg_spec} "
        f"--index-url {shlex.quote(agents_url)} "
        f"--prerelease allow --force-reinstall"
    )
    return _with_vm_path(" && ".join(commands))


def build_editable_install_commands(editable_paths: list[str]) -> list[str]:
    """Build uv commands to install editable packages into the pre-baked venv.

    SDK is installed first (other packages' build hooks import from plato).
    Uses --no-deps (deps pre-baked) and --no-build-isolation (hatchling pre-baked).

    Returns a list of shell commands to run sequentially.
    """
    sdk_paths = [p for p in editable_paths if "sdk" in p]
    other_paths = [p for p in editable_paths if "sdk" not in p]
    base = f"uv pip install --python {VENV_PYTHON} --no-deps --no-build-isolation"
    cmds = []
    if sdk_paths:
        editables = " ".join(f"-e {p}" for p in sdk_paths)
        cmds.append(_with_vm_path(f"{base} {editables}"))
    if other_paths:
        editables = " ".join(f"-e {p}" for p in other_paths)
        cmds.append(_with_vm_path(f"{base} {editables}"))
    return cmds


def build_editable_sdk_install_command(package_name: str, version: str | None, sdk_path: str = "/sdk") -> str:
    """Build the uv commands to install editable SDK plus a published agent package.

    Two separate installs because:
    - The SDK editable install needs PyPI for build deps (hatchling).
    - The agent install uses --no-deps from the agents-only index.
    """
    agents_url = plato_token_simple_index("agents")
    pkg_spec = _pip_package_spec(package_name, version)
    return _with_vm_path(
        f"uv pip install --python {VENV_PYTHON} "
        f"-e {shlex.quote(sdk_path)} --force-reinstall && "
        f"uv pip install --python {VENV_PYTHON} --no-deps "
        f"{pkg_spec} "
        f"--index-url {shlex.quote(agents_url)} "
        f"--prerelease allow --force-reinstall"
    )


async def install_production_agent(
    ssh_key: Path,
    hostname: str,
    package_name: str,
    version: str | None,
    *,
    upgrade_sdk: bool = True,
) -> None:
    """Install agent package from PyPI on VM."""
    logger.info("Installing agent package: %s==%s on %s", package_name, version or "latest", hostname)

    is_dev_version = version is not None and ".dev" in version

    # Check if the agent package is already pre-baked into the VM image.
    # The Dockerfile stamps /opt/plato-agent-version with "package==version".
    # Dev publishes often reuse an existing image tag via `--skip-docker`, so
    # they must always reinstall from the package registry instead of trusting
    # the image stamp.
    # Skip pre-bake check when version is unresolved (None) — we can't match.
    if version and not is_dev_version:
        expected = f"{package_name}=={version}"
        check_rc, check_out, _ = await run_ssh(
            ssh_key,
            hostname,
            "cat /opt/plato-agent-version 2>/dev/null || true",
            timeout=5,
        )
        if check_rc == 0 and check_out.strip() == expected:
            logger.info("Agent package %s already pre-baked on %s, skipping install", expected, hostname)
            if upgrade_sdk:
                sdk_cmd = f"uv pip install --python {VENV_PYTHON} plato-sdk-v2 --upgrade"
                await run_ssh(ssh_key, hostname, sdk_cmd, user="root", timeout=300)
                logger.info("Upgraded plato-sdk-v2 on %s (agent was pre-baked)", hostname)
            return

    install_cmd = build_agent_install_command(package_name, version, upgrade_sdk=upgrade_sdk)

    t0 = time.monotonic()
    exit_code, stdout, stderr = await run_ssh(
        ssh_key,
        hostname,
        install_cmd,
        user="root",
        timeout=300,
    )
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
