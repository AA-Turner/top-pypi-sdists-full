"""Published-package install helpers for agent VMs."""

from __future__ import annotations

import logging
import shlex
import time
from pathlib import Path

from plato.utils.fuse_binary import ENSURE_FUSE3_COMMAND as ENSURE_FUSE3_COMMAND
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
    base = f"UV_NO_SOURCES=1 uv pip install --python {VENV_PYTHON} --no-deps --no-build-isolation"
    cmds = []
    if sdk_paths:
        editables = " ".join(f"-e {p}" for p in sdk_paths)
        cmds.append(_with_vm_path(f"{base} {editables}"))
    if other_paths:
        editables = " ".join(f"-e {p}" for p in other_paths)
        cmds.append(_with_vm_path(f"{base} {editables}"))
    return cmds


# VM setup commands shared by the chronos dev and test runners.
# ENSURE_FUSE3_COMMAND lives in plato.utils.fuse_binary (also used by the
# direct agent-VM fuse transport, which cannot import plato.agents) and is
# re-exported here for the runners that historically imported it from this
# module.
DISCOVER_WORLD_PACKAGES_COMMAND = (
    'python3 -c "import importlib.metadata; '
    "eps = importlib.metadata.entry_points(group='plato.worlds'); "
    "print(' '.join(set(ep.dist.name for ep in eps)))\" 2>/dev/null || true"
)
CLEAN_WORLD_BUILD_ARTIFACTS_COMMAND = "rm -rf /world/dist /world/*.egg-info /world/src/*.egg-info /world/build"

WORLD_DEPS_REQUIREMENTS_PATH = "/tmp/plato-world-deps.txt"
WORLD_DEPS_CONSTRAINTS_PATH = "/tmp/plato-world-deps-constraints.txt"

# Never (re)install these from the world's dependency list: the editable /sdk
# install must not be replaced by a PyPI wheel.
_WORLD_DEPS_EXCLUDED = ("plato-sdk-v2", "plato-sdk")


def build_world_deps_sync_command(world_path: str = "/world") -> str:
    """Build a uv command that installs the world's declared runtime deps.

    Editable world installs use --no-deps (deps are pre-baked in the image),
    so a dependency added to pyproject.toml after the image was built is
    missing in dev mode. This reads the synced pyproject on the VM, drops
    plato-sdk packages, and installs the rest — a no-op when already
    satisfied.

    The install is constrained to the currently installed plato-sdk version
    so a transitive dependency on the SDK can't replace the editable /sdk
    (or silently upgrade a baked) install with a PyPI wheel; a genuinely
    conflicting transitive constraint fails the resolve loudly instead.
    """
    excluded = ", ".join(f"'{name}'" for name in _WORLD_DEPS_EXCLUDED)
    script = f"""
import re, tomllib, importlib.metadata
deps = tomllib.load(open('{world_path}/pyproject.toml', 'rb')).get('project', {{}}).get('dependencies', [])
name = lambda d: re.split(r'[\\[<>=!~;@ ]', d.strip(), maxsplit=1)[0].lower().replace('_', '-')
excluded = {{{excluded}}}
out = '\\n'.join(d for d in deps if name(d) not in excluded)
if out:
    print(out)
pins = []
for p in sorted(excluded):
    try:
        pins.append(p + '==' + importlib.metadata.version(p))
    except Exception:
        pass
open('{WORLD_DEPS_CONSTRAINTS_PATH}', 'w').write(''.join(p + '\\n' for p in pins))
"""
    return _with_vm_path(
        f"{VENV_PYTHON} -c {shlex.quote(script)} > {WORLD_DEPS_REQUIREMENTS_PATH} && "
        f"if test -s {WORLD_DEPS_REQUIREMENTS_PATH}; then "
        f"uv pip install --python {VENV_PYTHON} -r {WORLD_DEPS_REQUIREMENTS_PATH} "
        f"-c {WORLD_DEPS_CONSTRAINTS_PATH} -q; fi"
    )


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
            timeout=30,
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
