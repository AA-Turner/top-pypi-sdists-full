"""Internals for `probe update`: install detection, CLI upgrade, plugin update.

Kept in its own module, imported at the TOP of cli/main.py, so the whole call
graph is loaded before `probe update` spawns the CLI upgrade (H8). `uv tool
upgrade` replaces the installed tree, and Python does not hold deferred `.py`
imports open — so anything imported lazily AFTER the upgrade would
`ModuleNotFoundError`. Everything used here is imported at module top.

Detection is by the RUNNING interpreter's own `probe` package path (resolved
through symlinks), never `which probe` (shadowing) and never the CWD (a lockfile
in the current directory says nothing about how `probe` itself was installed).
"""

from __future__ import annotations
import os
from dataclasses import dataclass
from pathlib import Path

import httpx

from probe.shared.updates import installs
from probe.foundation.tls.tls import ssl_context

# Loaded here, not when `service_calls.recorders` asks: the update report reads
# the service's recorders AFTER the CLI upgrade replaced this tree (see above).
#: Every piece of the old client and protocol by name: their package's door loads none by itself.
from probe.foundation.service_api import calls as _service_calls  # noqa: F401
from probe.foundation.service_api import cli as _service_cli  # noqa: F401
from probe.foundation.service_api import env as _service_env  # noqa: F401
from probe.foundation.service_api import params as _service_params  # noqa: F401
from probe.foundation.service_api import service_api as _service_client  # noqa: F401
from probe.foundation.service_api import start as _service_start  # noqa: F401
from probe.foundation.service_api import vocabularies as _service_vocabularies  # noqa: F401
from probe.foundation.service_api import wire as _service_protocol  # noqa: F401

# H8: `scrub_text` imports this lazily, and it runs AFTER the CLI upgrade has
# replaced the installed tree. Loaded here so that import finds it in memory.
from probe.tap_core import secrets as _secrets  # noqa: F401

DIST = "probe-research"
LEGACY_DIST = "probe-agent"  # pre-2026-07-15 name; owns the same `probe` binary
_HTTP_TIMEOUT_S = 5.0

# `probe update --check` exit codes, distinct from main()'s 1=RosError / 2=usage.
# Scripts gate on BEHIND explicitly (`probe update --check; [ $? -eq 10 ] && …`), NOT
# `|| probe update` — a network error is 1 (nonzero) but must not read as "behind".
CHECK_CURRENT = 0
CHECK_BEHIND = 10
CHECK_ERROR = 1


# -- install detection ------------------------------------------------------
class Method:
    UV_TOOL = "uv-tool"
    UV_TOOL_LEGACY = "uv-tool-legacy"  # installed under the old probe-agent name (H3)
    PIPX = "pipx"
    PIP = "pip"
    EPHEMERAL = "ephemeral"  # uvx / pipx run cache -- nothing to upgrade, no pip
    EDITABLE = "editable"  # -e / source checkout (H5)
    MANAGED = "managed"  # pip dep in a project with a lockfile (H6)
    UNKNOWN = "unknown"


@dataclass(frozen=True)
class Install:
    method: str
    root: Path | None = None
    detail: str = ""


def _probe_pkg_dir() -> Path:
    """The directory the RUNNING `probe` package is imported from, symlinks resolved."""
    import probe  # already loaded; this is the running interpreter's copy

    return Path(probe.__file__).resolve().parent


def _venv_root(site_packages_pkg: Path) -> Path | None:
    """Walk up from .../site-packages/probe to the environment root.

    Handles both the Unix ``<venv>/lib/pythonX.Y/site-packages`` layout and the
    Windows ``<venv>/Lib/site-packages`` layout (one level shallower).
    """
    for parent in site_packages_pkg.parents:
        if parent.name in ("site-packages", "dist-packages"):
            # parent == .../site-packages. Its parent is `lib` directly on Windows
            # (`Lib/site-packages`, 2 up), or `pythonX.Y` on Unix (3 up).
            if parent.parent.name.lower() == "lib":
                return parent.parent.parent
            return parent.parent.parent.parent
    return None


_MANAGED_LOCKFILES = ("uv.lock", "poetry.lock", "Pipfile.lock", "pdm.lock")
# Poetry / Pipenv / PDM keep venvs OUTSIDE the project by default, so their lockfile
# is never adjacent to the venv; recognize their well-known cache dirs instead.
_MANAGED_VENV_MARKERS = ("/pypoetry/virtualenvs/", "/virtualenvs/", "/pdm/venvs/")


def _is_editable(pkg_dir: Path) -> bool:
    """True if `probe` is imported from a source checkout rather than an install."""
    s = str(pkg_dir).replace(os.sep, "/")
    if "/site-packages/" not in s and "/dist-packages/" not in s:
        return True  # imported straight from a source tree
    # editable installs can still land a finder in site-packages; look for markers
    for parent in pkg_dir.parents:
        if parent.name in ("site-packages", "dist-packages"):
            if list(parent.glob("__editable__.probe_research*")) or list(
                parent.glob("probe*.egg-link")
            ):
                return True
            break
    return False


def _is_managed_project(venv_root: Path | None) -> bool:
    """True if this venv belongs to a lockfile-managed project, where `pip install -U`
    would desync the lockfile (H6).

    Checked from the VENV, never the CWD. Covers uv's in-project ``.venv/`` (lockfile
    at venv.parent) AND out-of-project poetry/pipenv/pdm venvs (their lockfile is not
    adjacent to the venv, so they're matched by their cache dirs / active-env signals).
    """
    if venv_root is None:
        return False
    marker = str(venv_root).replace(os.sep, "/") + "/"
    if any(m in marker for m in _MANAGED_VENV_MARKERS):
        return True
    project = venv_root.parent
    if any((project / name).exists() for name in _MANAGED_LOCKFILES):
        return True
    return bool(os.environ.get("POETRY_ACTIVE") or os.environ.get("PIPENV_ACTIVE"))


def detect_install() -> Install:
    try:
        pkg = _probe_pkg_dir()
    except Exception:
        return Install(Method.UNKNOWN)
    s = str(pkg).replace(os.sep, "/")
    # The marks the auto-update default reads too (`version_policy.managed_cli`):
    # these two kinds are the machine's managed CLI, on by default (plan C2).
    from probe.shared.updates import version_policy

    if version_policy.UV_TOOL_MARK in s or installs.running_from_versions(s):
        # A side-by-side version env (`probe.shared.updates.installs`, plan D6) is the
        # same uv tool install, one version of it.
        return Install(Method.UV_TOOL)
    if version_policy.LEGACY_UV_TOOL_MARK in s:
        return Install(Method.UV_TOOL_LEGACY, detail="installed under the legacy probe-agent name")
    # `npx probe-research` runs us through `uv tool run`, whose environment
    # lives in the uv CACHE and has no pip. Without this it falls through to
    # Method.PIP and the upgrade dies with "No module named pip" -- while there
    # is nothing to upgrade anyway, because the env is thrown away on exit.
    if "/uv/archive-v0/" in s or "/.cache/uv/" in s or "/pipx/.cache/" in s:
        return Install(
            Method.EPHEMERAL,
            detail="running from a temporary uvx/pipx environment",
        )
    pipx_home = os.environ.get("PIPX_HOME")
    if "/pipx/venvs/" in s or (
        pipx_home and s.startswith(str(Path(pipx_home).resolve()).replace(os.sep, "/"))
    ):
        return Install(Method.PIPX)
    if _is_editable(pkg):
        return Install(Method.EDITABLE, root=pkg.parent, detail="editable / source checkout")

    venv = _venv_root(pkg)
    if _is_managed_project(venv):
        return Install(Method.MANAGED, root=venv, detail="project dependency (lockfile present)")
    if venv is not None:
        return Install(Method.PIP, root=venv)
    return Install(Method.UNKNOWN)


def fetch_latest(base_url: str) -> dict:
    """GET the public client-version manifest. Raises on network/HTTP error."""
    with httpx.Client(
        base_url=base_url.rstrip("/"),
        timeout=_HTTP_TIMEOUT_S,
        verify=ssl_context(),
    ) as client:
        response = client.get(
            "/v1/client-version",
            headers={"Accept": "application/json"},
        )
    response.raise_for_status()
    data = response.json()
    if not isinstance(data, dict):
        raise ValueError("manifest is not a JSON object")
    return data


def _latest(manifest: dict, key: str) -> str | None:
    info = manifest.get(key)
    return info.get("latest") if isinstance(info, dict) else None


def cli_latest(manifest: dict) -> str | None:
    return _latest(manifest, "cli")


def plugin_latest(manifest: dict) -> str | None:
    return _latest(manifest, "plugin")


def tap_latest(manifest: dict) -> str | None:
    return _latest(manifest, "tap")


def cli_update_available(manifest: dict, current: str) -> str | None:
    latest = _latest(manifest, "cli")
    return latest if is_newer(latest, current) else None
from probe.shared.harness.plugin_update import is_newer  # noqa: E402 -- pieces need each other; the front door loads this one first
