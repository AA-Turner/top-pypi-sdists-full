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

import contextlib
import json
import threading
import os
import re
import shutil
import subprocess
import sys
import dataclasses
from dataclasses import dataclass
from collections.abc import Callable
from pathlib import Path

import httpx

from probe._shared import handoff, installs, kimi_live
from probe.cli import claude_cli, plugin_cli, service_calls
from probe.cli.capabilities import (
    DAEMON_PLUGIN_NAME,
    TAP_PLUGIN_ID,
    TAP_PLUGIN_NAME,
    TRACKING_PLUGIN_NAME,
    tracking_plugin_name,
)
from probe.cli.versions import _LEGACY_TAP_PLUGINS
from probe.core import adopt as _adopt
from probe.harness import get_registry
from probe.sdk import session_marker
from probe.sdk.redaction import scrub_text
# Loaded here, not when `service_calls.recorders` asks: the update report reads
# the service's recorders AFTER the CLI upgrade replaced this tree (see above).
from probe.service import client as _service_client  # noqa: F401
from probe.service import protocol as _service_protocol  # noqa: F401
from probe.sdk.tls import ssl_context

# H8: `scrub_text` imports this lazily, and it runs AFTER the CLI upgrade has
# replaced the installed tree. Loaded here so that import finds it in memory.
from probe.tap_core import secrets as _secrets  # noqa: F401

# Resolved once, at import (H8): `is_newer` runs AFTER the tree is replaced, and a
# deferred `import packaging` there could fail; loading it now keeps it in memory.
try:
    from packaging.version import Version as _Version  # type: ignore
except Exception:  # pragma: no cover - packaging is a transitive dep, usually present
    _Version = None

DIST = "probe-research"
LEGACY_DIST = "probe-agent"  # pre-2026-07-15 name; owns the same `probe` binary
PLUGIN_ID = "probe-research@research-os-agent"
# Imported, NOT redefined: capabilities.py already owns this identity and
# actions.py/capture.py use it from there. A second literal here would be a
# second source of truth for the same plugin — the exact thing that lets one
# copy drift after a rename. (The PLUGIN_ID literal above predates this and
# duplicates capabilities.PLUGIN_ID; left alone rather than silently widened.)
#
# The tap ships from the same marketplace as a SEPARATE plugin, so
# `claude plugin update probe-research@…` never touched it. Leaving it out made
# `probe update` a command that reports success while the component whose
# staleness is invisible (a stale tap captures nothing and says nothing) stays
# behind. Updated alongside, and `claude` failing on it is NOT fatal: `probe
# capture off --uninstall` removes the tap while leaving the CLI and plugin in
# place, so "not installed" is a SUPPORTED state that `claude plugin update`
# reports as an error. What IS a failure is an installed tap still behind the
# manifest after the run: that one used to pass in silence (`tap_verdict`).
MARKETPLACE = "research-os-agent"
MARKETPLACE_REPO = "prbe-ai/research-os-agent"
#: Codex's `marketplace upgrade` refusal for a name with no config entry.
_CODEX_NOT_CONFIGURED = "is not configured as a git marketplace"

_UPGRADE_TIMEOUT_S = 300.0
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
    from probe import version_policy

    if version_policy.UV_TOOL_MARK in s or installs.running_from_versions(s):
        # A side-by-side version env (`probe._shared.installs`, plan D6) is the
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


# -- version compare + manifest ---------------------------------------------
def _triplet(v: str):
    if not v:
        return None
    v = str(v).strip().split()[-1]
    for sep in ("+", "-"):
        v = v.split(sep, 1)[0]
    try:
        nums = [int(p) for p in v.split(".")]
    except ValueError:
        return None
    while len(nums) < 3:
        nums.append(0)
    return tuple(nums[:3])


def is_newer(candidate: str | None, base: str | None) -> bool:
    """True iff `candidate` is strictly newer than `base`."""
    if not candidate or not base:
        return False
    if _Version is not None:
        try:
            return _Version(str(candidate)) > _Version(str(base))
        except Exception:
            pass
    c, b = _triplet(candidate), _triplet(base)
    return bool(c and b and c > b)


def fetch_latest(base_url: str) -> dict:
    """GET the public client-version manifest. Raises on network/HTTP error."""
    with httpx.Client(
        base_url=base_url.rstrip("/"),
        timeout=_HTTP_TIMEOUT_S,
        verify=ssl_context(),
    ) as client:
        resp = client.get(
            "/v1/client-version",
            headers={"Accept": "application/json"},
        )
    resp.raise_for_status()
    data = resp.json()
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


# -- plugin (installed) version, for the H1 post-condition ------------------
def _ledger_version(plugin_id: str) -> str | None:
    """The newest version Claude Code's install ledger records for `plugin_id`."""
    path = Path.home() / ".claude" / "plugins" / "installed_plugins.json"
    try:
        data = json.loads(path.read_text())
        entries = (data.get("plugins") or {}).get(plugin_id) or []
        best: str | None = None
        for entry in entries:
            v = entry.get("version") if isinstance(entry, dict) else None
            if v and (best is None or is_newer(v, best)):
                best = v
        return best
    except Exception:
        return None


def tracking_plugin_id(source: str = "claude_code") -> str:
    """`PLUGIN_ID`, or the lean `probe-research-daemon@…` for an agent whose
    "Who records" is the daemon: an update must move the plugin the profile
    installed, never put the other one back."""
    return f"{tracking_plugin_name(source)}@{MARKETPLACE}"


def installed_plugin_version() -> str | None:
    return _ledger_version(tracking_plugin_id())


def installed_tap_version() -> str | None:
    """The tap Claude Code has DOWNLOADED (its ledger), which is what an update
    moves. `versions.local_versions` prefers the copy that last RAN, which an
    update cannot move until a session restarts, so it grades this number
    whenever it is the newer of the two."""
    return _ledger_version(TAP_PLUGIN_ID)


#: Probe plugin names an update can meet. A ledger entry under one of these
#: names but NOT under `MARKETPLACE`, or under a retired name, is a copy no
#: `claude plugin update <name>@research-os-agent` will ever move.
_PROBE_PLUGIN_NAMES = (TRACKING_PLUGIN_NAME, DAEMON_PLUGIN_NAME, TAP_PLUGIN_NAME)

#: The shape the server accepts for a reported plugin id. A ledger key outside it
#: (an uppercase marketplace, a local path) is left out of the report rather than
#: refusing the whole report over it.
_REPORTABLE_PLUGIN_ID = re.compile(
    r"^(?:probe|prbe)-[a-z0-9-]{1,60}(?:@[a-z0-9][a-z0-9._-]{0,63})?$"
)


def _ledger_readable() -> bool:
    """Claude Code's install ledger can be read: absent (nothing installed) or
    a JSON object. `_ledger_version` reads an unreadable one as "not
    installed", which `nothing_installed` must not take at its word."""
    path = Path.home() / ".claude" / "plugins" / "installed_plugins.json"
    try:
        data = json.loads(path.read_text())
    except FileNotFoundError:
        return True
    except Exception:  # noqa: BLE001 - permissions, a half-written file, bad JSON
        return False
    return isinstance(data, dict) and isinstance(data.get("plugins") or {}, dict)


def _ledger_ids() -> list[str]:
    path = Path.home() / ".claude" / "plugins" / "installed_plugins.json"
    try:
        plugins = json.loads(path.read_text()).get("plugins") or {}
    except Exception:
        return []
    return [key for key, entries in plugins.items() if isinstance(key, str) and entries]


def legacy_plugin_ids(names: list[str] | None = None) -> tuple[str, ...]:
    """Probe plugins installed under an id an update does not move.

    Two kinds: a RETIRED name (`prbe-cc-tap-plugin`, `prbe-codex-tap-plugin`,
    the tap's ids before the rename), and a current name from ANOTHER
    marketplace. Either one can be the copy actually running -- and capturing --
    on a machine where the update reports the tap "not installed".

    Observation only: nothing here migrates them. `names` is Codex's installed
    list (bare names); without it, Claude Code's ledger is read.
    """
    found: list[str] = []
    for key in _ledger_ids() if names is None else names:
        name, _, marketplace = key.partition("@")
        retired = name in _LEGACY_TAP_PLUGINS
        elsewhere = name in _PROBE_PLUGIN_NAMES and bool(marketplace) and marketplace != MARKETPLACE
        if (retired or elsewhere) and _REPORTABLE_PLUGIN_ID.match(key):
            found.append(key)
    return tuple(dict.fromkeys(found))[:8]


def legacy_tap_ids(ids: tuple[str, ...]) -> tuple[str, ...]:
    """The tap among `legacy_plugin_ids`: a retired tap name, or the tap's own
    name from another marketplace."""
    return tuple(
        key for key in ids if key.partition("@")[0] in (*_LEGACY_TAP_PLUGINS, TAP_PLUGIN_NAME)
    )


# -- upgrade actions --------------------------------------------------------
@dataclass
class CliResult:
    ran: bool
    ok: bool  # the CLI is at (or past) the target after the attempt — VERIFIED
    changed: bool  # the installed version actually moved
    before: str | None
    after: str | None
    message: str
    #: The package manager this install needs (`uv`, `pipx`) is not on this
    #: process's PATH. An observation for the server's update report only.
    missing_binary: bool = False


def _run(cmd: list[str], timeout: float) -> subprocess.CompletedProcess | None:
    try:
        return subprocess.run(cmd, timeout=timeout)  # inherit stdio: show progress
    except FileNotFoundError:
        return None
    except subprocess.TimeoutExpired:
        return subprocess.CompletedProcess(cmd, returncode=124)


def _installed_cli_version() -> str | None:
    """The CLI version after an upgrade, read FRESH -- the running process keeps
    its own stale __version__.

    The upgraded environment's own version first. The `probe` on PATH can be a
    different install entirely (a conda or pipx copy ahead of the uv tool), and
    grading that one reported "CLI upgraded" for an install nobody touched, or
    a failure for one that did move. PATH is the fallback for the one upgrade
    that deletes this environment: the legacy probe-agent reinstall.
    """
    return env_cli_version() or _path_cli_version()


def _path_cli_version() -> str | None:
    """Version of the `probe` on PATH, read via a fresh subprocess."""
    probe_bin = shutil.which("probe") or "probe"
    try:
        r = subprocess.run([probe_bin, "--version"], capture_output=True, text=True, timeout=15)
        if r.returncode == 0 and (r.stdout or "").strip():
            return r.stdout.strip().split()[-1]  # "probe 0.8.2" -> "0.8.2"
    except Exception:
        return None
    return None


def env_cli_version() -> str | None:
    """The CLI version now installed in THIS interpreter's own environment.

    Read by a fresh interpreter from the dist metadata on disk, because this
    process's own `__version__` is whatever it imported before the upgrade.
    None when that environment is gone (the legacy reinstall deletes it) or
    unreadable.
    """
    try:
        r = subprocess.run(  # noqa: S603 - our own interpreter, no shell
            [
                sys.executable,
                "-c",
                f"from importlib.metadata import version; print(version({DIST!r}))",
            ],
            capture_output=True,
            text=True,
            stdin=subprocess.DEVNULL,
            timeout=15,
            check=False,
        )
    except (OSError, subprocess.SubprocessError):
        return None
    out = (r.stdout or "").strip()
    return out if r.returncode == 0 and out else None


def _finalize(before: str | None, target: str | None, tool: str) -> CliResult:
    """Post-condition — the CLI's H1: trust the observed version, not the upgrade's
    exit code. A no-op upgrade (e.g. a ``uv tool install ==X`` version pin) exits 0
    while changing nothing; only re-reading the version catches that."""
    after = _installed_cli_version()
    if is_newer(after, before):
        return CliResult(True, True, True, before, after, f"CLI upgraded {before} → {after}")
    if target and after and not is_newer(target, after):
        return CliResult(True, True, False, before, after, f"CLI already at the latest ({after})")
    return CliResult(
        True,
        False,
        False,
        before,
        after,
        f"`{tool}` reported success but the CLI is still {after or before} "
        "(it may be version-pinned, or that release was yanked)",
    )


def _dist(extras: tuple[str, ...] = ()) -> str:
    """The distribution to (re)install: always with the `all` extra (plan 2.11 --
    the CLI's and MCP server's dependencies leave core in the next release, so
    every install must have asked for them by then), plus `daemon` when this
    environment has the daemon's AI libraries, so an upgrade never strips them,
    or when it is a tool install and the daemon records for a coding agent here
    (`_daemon_wanted_here`), so an update puts them back after something else
    stripped them, plus ``extras`` (the ones the install already records)."""
    wanted = {"all", *extras}
    try:
        # The daemon's own harness, not `pydantic_ai`: a project environment with
        # its own Pydantic AI must not be handed the daemon's pinned stack.
        import pydantic_ai_harness  # noqa: F401
    except ImportError:
        if _daemon_wanted_here():
            wanted.add("daemon")
    else:
        wanted.add("daemon")
    return f"{DIST}[{','.join(sorted(wanted))}]"


#: Installs whose environment is the one the daemon's worker runs from: a tool
#: install (uv or pipx), or a launcher's temporary copy reinstalling one. A pip
#: install lives in a project or training environment that pinning the daemon's
#: AI stack could break, so it gets the libraries only when someone asks
#: (`probe daemon install`).
_DAEMON_HEAL_METHODS = frozenset({Method.UV_TOOL, Method.UV_TOOL_LEGACY, Method.PIPX, Method.EPHEMERAL})


def _daemon_wanted_here() -> bool:
    """Does the daemon record for a coding agent on this machine, and is this a
    tool install that runs it? (2026-10-12: a bare `uv tool install --force
    probe-research` dropped the `daemon` extra, and every update after restated
    `[all]` alone because `_dist` only asked whether the libraries imported.)"""
    try:
        if detect_install().method not in _DAEMON_HEAL_METHODS:
            return False
        return any(
            session_marker.recorder(harness.id) == session_marker.RECORDER_DAEMON
            for harness in get_registry().installable()
        )
    except Exception:  # noqa: BLE001 - an unreadable config keeps today's spec
        return False


@dataclass(frozen=True)
class KeptInstall:
    """What a reinstall must carry over from the install it replaces (#2043
    review): the extras it records beyond ours, the packages the user added
    beside it (`uv tool install --with`, `pipx inject`), and its Python.
    `dropped` names what the receipt records that a reinstall cannot restate
    (an editable `--with`, constraints, a receipt it could not read): left out,
    and said, rather than holding every update back (plan A4)."""

    extras: tuple[str, ...] = ()
    with_packages: tuple[str, ...] = ()
    python: str | None = None
    dropped: tuple[str, ...] = ()


#: uv-receipt.toml requirement keys a reinstall can restate. An entry with any
#: other key (an editable path) is left out of the reinstall and named.
_RECEIPT_REQUIREMENT_KEYS = frozenset({"name", "extras", "specifier", "url", "directory", "git"})


def _receipt_requirement(entry: dict) -> str | None:
    """One uv-receipt requirement as the PEP 508 string `--with` takes, or None
    when it has a shape this cannot restate faithfully."""
    if not isinstance(entry, dict) or set(entry) - _RECEIPT_REQUIREMENT_KEYS:
        return None
    name = entry.get("name")
    if not isinstance(name, str) or not name:
        return None
    extras = entry.get("extras") or []
    text = name + (f"[{','.join(extras)}]" if extras else "")
    sources = [k for k in ("url", "directory", "git") if entry.get(k)]
    if len(sources) > 1:
        return None
    if sources:
        where = str(entry[sources[0]])
        if sources[0] == "directory":
            where = Path(where).resolve().as_uri()
        elif sources[0] == "git" and not where.startswith("git+"):
            where = "git+" + where
        return f"{text} @ {where}"
    return text + str(entry.get("specifier") or "")


def kept_from_uv_receipt(prefix: str | Path | None = None) -> KeptInstall | None:
    """What this uv tool install records beside `probe-research`, read from
    its `uv-receipt.toml` (empty when there is none). `uv tool install`
    REPLACES the receipt, so an update that restated only
    `probe-research[all]` uninstalled every `--with` package (`probe import
    wandb` needs one).

    What it cannot restate faithfully (an entry with keys it does not know,
    constraints or overrides, a receipt it cannot read) is left out and named
    in `dropped`: it used to make the whole receipt unrestatable, which held
    every later update on the in-place path for good (plan A4). None only
    for probe-research itself from a path or URL: a checkout or a build of
    someone's own, which no update from the index may replace."""
    from probe._compat import tomllib

    path = Path(prefix if prefix is not None else sys.prefix) / "uv-receipt.toml"
    dropped: list[str] = []
    try:
        text = path.read_text(encoding="utf-8")
    except FileNotFoundError:
        return KeptInstall()  # no receipt: nothing recorded, nothing to lose
    except OSError as exc:
        text = ""
        dropped.append(f"the uv receipt (unreadable: {type(exc).__name__})")
    try:
        tool = tomllib.loads(text).get("tool") or {}
    except ValueError:
        tool = {}
        dropped.append("the uv receipt (not valid TOML)")
    for key in ("constraints", "overrides", "build-constraint-dependencies"):
        if tool.get(key):
            dropped.append(f"its {key}")
    extras: tuple[str, ...] = ()
    with_packages: list[str] = []
    for entry in tool.get("requirements") or []:
        if isinstance(entry, dict) and entry.get("name") in (DIST, LEGACY_DIST):
            if set(entry) - {"name", "extras", "specifier"}:
                return None  # probe itself from a path or URL: not ours to restate
            extras = tuple(e for e in entry.get("extras") or [] if isinstance(e, str))
            continue
        requirement = _receipt_requirement(entry)
        if requirement is None:
            name = entry.get("name") if isinstance(entry, dict) else None
            dropped.append(f"--with {name}" if isinstance(name, str) and name else "a --with entry")
            continue
        with_packages.append(requirement)
    python = tool.get("python")
    if not isinstance(python, str) or not python or (os.path.isabs(python) and not os.path.exists(python)):
        python = _env_interpreter(path.parent)
    return KeptInstall(extras=extras, with_packages=tuple(with_packages), python=python, dropped=tuple(dropped))


def faithful_kept_from_uv_receipt(prefix: str | Path | None = None) -> KeptInstall | None:
    """`kept_from_uv_receipt`, or None when it would leave anything out: for
    what reinstalls the RUNNING environment in place (the in-place update,
    `npx probe-research`, `probe daemon install`), where nothing stays to
    switch back to and a dropped package is gone. Only a side-by-side install,
    which keeps the running version, goes ahead without what it cannot restate."""
    kept = kept_from_uv_receipt(prefix)
    return None if kept is None or kept.dropped else kept


def dropped_note(kept: KeptInstall | None) -> str:
    """"; not carried over from the uv receipt: ..." for what a reinstall left
    out (`KeptInstall.dropped`), or ""."""
    if kept is None or not kept.dropped:
        return ""
    return (f"; not carried over from the uv receipt (it cannot be restated): {', '.join(kept.dropped)}. "
            "Add it back with your own `uv tool install` if you need it")


def _env_interpreter(prefix: Path) -> str | None:
    """The exact interpreter this tool environment runs on (`pyvenv.cfg`'s
    `home` + `pythonX.Y`), or None. A receipt that records no Python lets uv
    choose one: `--force`, and a plain install on uv before 0.10, rebuild the
    environment on the NEWEST Python uv has, deleting `lib/pythonX.Y` under every
    running `probe` (2026-10-12: 3.13 -> 3.14 under a live daemon worker). Only
    the exact path keeps it: `--python 3.12` let uv pick its managed 3.12 over the
    system one the environment ran on, and rebuild just the same."""
    try:
        text = (prefix / "pyvenv.cfg").read_text(encoding="utf-8")
    except OSError:
        return None
    fields = {}
    for line in text.splitlines():
        key, sep, value = line.partition("=")
        if sep:
            fields[key.strip()] = value.strip()
    home = fields.get("home")
    if not home:
        return None
    found = re.match(r"(\d+)\.(\d+)", fields.get("version_info") or fields.get("version") or "")
    if not found:
        return None
    # Only the versioned name: a bare `python3` there may be another version by
    # now. Without it (Windows' `python.exe` among them) no pin, as before.
    candidate = Path(home) / f"python{found.group(1)}.{found.group(2)}"
    return str(candidate) if candidate.exists() else None


def uv_tool_install_command(
    kept: KeptInstall,
    *,
    force: bool = False,
    version: str = "",
    legacy: bool = False,
    refresh: bool = False,
) -> list[str]:
    """`uv tool install` of `probe-research[all,...]` that keeps ``kept``.
    ``version`` is appended to the spec (`@latest`, `==1.2.3`). A legacy
    probe-agent install's extras are its own, so only its packages carry.
    ``refresh`` re-reads the package index for probe-research instead of uv's
    cached copy, which can predate a release by minutes."""
    command = ["uv", "tool", "install"]
    if force:
        command.append("--force")
    if refresh:
        command += ["--refresh-package", DIST]
    command.append(_dist(() if legacy else kept.extras) + version)
    for requirement in kept.with_packages:
        command += ["--with", requirement]
    if kept.python:
        command += ["--python", kept.python]
    return command


def _pipx_metadata(prefix: str | Path | None = None) -> dict:
    path = Path(prefix if prefix is not None else sys.prefix) / "pipx_metadata.json"
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return {}
    return data if isinstance(data, dict) else {}


def pipx_injected(prefix: str | Path | None = None) -> list[str]:
    """Packages injected beside this pipx install (`pipx inject`), from its
    `pipx_metadata.json`: `pipx install --force` drops them."""
    injected = _pipx_metadata(prefix).get("injected_packages") or {}
    out = []
    for name, record in injected.items():
        spec = (record or {}).get("package_or_url") if isinstance(record, dict) else None
        out.append(str(spec or name))
    return out


def pipx_extras(prefix: str | Path | None = None) -> tuple[str, ...]:
    """The extras this pipx install was installed with (its recorded spec):
    `pipx install --force probe-research[all]` would record `[all]` alone."""
    main = _pipx_metadata(prefix).get("main_package") or {}
    spec = str(main.get("package_or_url") or "") if isinstance(main, dict) else ""
    found = re.match(r"^\s*probe-research\s*\[([^\]]*)\]", spec)
    if not found:
        return ()
    return tuple(e.strip() for e in found.group(1).split(",") if e.strip())


def upgrade_cli(install: Install, current: str | None, target: str | None) -> CliResult:
    m = install.method
    if m == Method.EDITABLE:
        return CliResult(
            False,
            False,
            False,
            current,
            current,
            "editable/source install — update with git, not a package manager",
        )
    if m == Method.MANAGED:
        return CliResult(
            False,
            False,
            False,
            current,
            current,
            "probe-research is a dependency of this project — bump it with your "
            "dependency manager (e.g. `uv add probe-research@latest`) so the lockfile stays in sync",
        )
    if m == Method.UNKNOWN:
        return CliResult(
            False,
            False,
            False,
            current,
            current,
            "could not tell how probe was installed — update via your package manager",
        )
    from probe._shared import uninstall_barrier

    refused = uninstall_barrier.refusal()
    if refused:
        # Every in-place path below replaces the env under the uninstall (the
        # side-by-side one refuses in `installs` too).
        return CliResult(True, False, False, current, current, f"the CLI was not updated: {refused}")
    if m == Method.UV_TOOL_LEGACY:
        # H3: the old probe-agent tool owns `probe`; uninstall it, install the new.
        # The packages added beside it come along (read before the uninstall).
        kept = kept_from_uv_receipt() or KeptInstall()
        try:
            with _install_lock():
                refused = uninstall_barrier.refusal()  # written while this waited for the lock
                if refused:
                    return CliResult(True, False, False, current, current, f"the CLI was not updated: {refused}")
                if _run(["uv", "tool", "uninstall", LEGACY_DIST], _UPGRADE_TIMEOUT_S) is None:
                    return CliResult(
                        False, False, False, current, current, "`uv` not found on PATH",
                        missing_binary=True,
                    )
                _run(uv_tool_install_command(kept, force=True, legacy=True), _UPGRADE_TIMEOUT_S)
        except handoff.LockBusy:
            return CliResult(True, False, False, current, current, LOCK_BUSY_MESSAGE)
        return _finalize(current, target, "uv")
    if m == Method.PIPX:
        # `install --force`, not `upgrade`: pipx upgrade keeps the spec the tool
        # was first installed with, and that spec must now carry `[all]`. It
        # drops `pipx inject`-ed packages, so those go back in after.
        injected = pipx_injected()
        if _run(["pipx", "install", "--force", _dist(pipx_extras())], _UPGRADE_TIMEOUT_S) is None:
            return CliResult(
                False, False, False, current, current, "`pipx` not found on PATH",
                missing_binary=True,
            )
        if injected:
            _run(["pipx", "inject", DIST, *injected], _UPGRADE_TIMEOUT_S)
        return _finalize(current, target, "pipx")
    if m == Method.PIP:
        _run([sys.executable, "-m", "pip", "install", "-U", _dist()], _UPGRADE_TIMEOUT_S)
        return _finalize(current, target, "pip")

    # Method.UV_TOOL
    side = upgrade_side_by_side(current, target)
    if side is not None:
        return side
    if os.environ.get(REQUIRE_SIDE_BY_SIDE_ENV) == "1":
        # The service let runs and workers go on through this update; in place
        # would replace their files under them. The next cycle tries again.
        return CliResult(
            True, False, False, current, current,
            "the CLI was not updated: it can only be updated beside the running version now, "
            "and that was not possible (see above); the next update tries again",
        )
    if not target and _side_by_side_machine():
        # No release could be read (the manifest, nor the hand-off's PyPI
        # fallback): this machine updates beside the running version, never in
        # place (plan A4). The next update tries again.
        return CliResult(
            True, False, False, current, current,
            "the CLI was not updated: the newest release could not be read; the next update tries again",
        )
    try:
        with _install_lock():
            refused = uninstall_barrier.refusal()  # written while this waited for the lock
            if refused:
                return CliResult(True, False, False, current, current, f"the CLI was not updated: {refused}")
            return _upgrade_in_place(current, target)
    except handoff.LockBusy:
        return CliResult(True, False, False, current, current, LOCK_BUSY_MESSAGE)


#: Another update (the hand-off, the lifeboat, the service's child) holds the install lock.
LOCK_BUSY_MESSAGE = "another update is installing the CLI now (it holds the install lock); the next update tries again"


def _install_lock():
    """The one install lock (`handoff.install_lock`), for the in-place paths;
    nothing when its folder cannot be told."""
    try:
        root = installs.versions_root()
    except Exception:  # noqa: BLE001
        return contextlib.nullcontext()
    return handoff.install_lock(root)


def _side_by_side_machine() -> bool:
    """Does this uv tool install update beside the running version (the
    layout is usable here, the receipt names probe-research from its index),
    unless a person asked for in place (IN_PLACE_ENV)?"""
    if os.environ.get(IN_PLACE_ENV) == "1":
        return False
    try:
        return kept_from_uv_receipt() is not None and installs.usable(installs.tool_dir())
    except Exception:  # noqa: BLE001 -- unknown: as before
        return False


def _upgrade_in_place(current: str | None, target: str | None) -> CliResult:
    """The uv tool update before side-by-side installs, under the install lock."""
    # `[all]` is restated FIRST (plan 2.11): `uv tool upgrade` re-resolves the
    # requirement the tool was first installed with, so upgrading a bare
    # receipt onto the release that drops these dependencies from core would
    # strip `probe` -- restating after that upgrade left exactly that window
    # (#2043 review). `uv tool install` REPLACES the receipt, so everything
    # else it records (`--with` packages, extras, the Python) is restated too.
    # In place there is no version to switch back to: a receipt it cannot
    # restate whole is left alone (`faithful_kept_from_uv_receipt`).
    kept = faithful_kept_from_uv_receipt()
    unrecorded = ""
    if kept is not None:
        restated = _run(uv_tool_install_command(kept), _UPGRADE_TIMEOUT_S)
        if restated is None:
            return CliResult(
                False, False, False, current, current, "`uv` not found on PATH",
                missing_binary=True,
            )
        if restated.returncode != 0:
            return CliResult(
                True, False, False, current, current,
                "could not record `probe-research[all]` in this uv tool install "
                f"(`uv tool install` exited {restated.returncode}); the CLI was not upgraded",
            )
    else:
        # A receipt this cannot restate faithfully (an editable `--with`,
        # constraints, probe-research itself from a path) is left alone rather
        # than stripped -- but then `[all]` is not recorded, and the release
        # after this one needs it.
        unrecorded = (
            "; `probe-research[all]` is NOT recorded in this install's uv receipt, which "
            "has entries the wizard's Update cannot restate. Before the next release, run "
            f"`uv tool install '{_dist()}'` with your own `--with` packages"
        )
    if _run(["uv", "tool", "upgrade", DIST], _UPGRADE_TIMEOUT_S) is None:
        return CliResult(
            False, False, False, current, current, "`uv` not found on PATH",
            missing_binary=True,
        )
    res = _finalize(current, target, "uv")
    if not res.ok:
        # `uv tool upgrade` no-ops on a version-pinned install (exits 0, changes
        # nothing), and on uv's cached index when that predates the release
        # (`uv tool upgrade` takes no refresh flag): install the latest from a
        # FRESH index, then re-verify (R9). Not `--force`: a plain install of a
        # new requirement upgrades the environment in place, while `--force`
        # deletes and rebuilds it -- on the newest Python uv has, unless told --
        # under every running `probe` (2026-10-12: a daemon worker crashed
        # reading its own files from the deleted lib/python3.13).
        _run(
            uv_tool_install_command(kept or KeptInstall(), version="@latest", refresh=True),
            _UPGRADE_TIMEOUT_S,
        )
        res = _finalize(current, target, "uv")
    if unrecorded:
        res = dataclasses.replace(res, message=res.message + unrecorded)
    return res


#: Set to 1 to update the uv tool env in place, as before side-by-side installs.
IN_PLACE_ENV = "PROBE_UPDATE_IN_PLACE"
#: Set by the Probe service (`probe.service.updater.SIDE_BY_SIDE_ENV`) when it did
#: not wait for runs and daemon workers: the CLI is updated beside them or not at all.
REQUIRE_SIDE_BY_SIDE_ENV = "PROBE_UPDATE_SIDE_BY_SIDE"


def upgrade_side_by_side(current: str | None, target: str | None) -> CliResult | None:
    """The uv tool update of plan D6: install `target` as its own environment
    beside the running one, check it starts (the service's start path, the
    CLI's import), then switch the tool path to it in one rename and point
    `runtime.json` at it. The running version stays, for the switch back (D5).
    Nothing is changed unless all of that worked: a failed install leaves the
    machine on `current`.

    None when this layout cannot be used here (no target version known,
    probe-research itself installed from a path or URL, another filesystem,
    or IN_PLACE_ENV): the caller decides (`upgrade_cli`: never in place on a
    machine that updates side by side, when it is only the target that is
    unknown). A receipt entry it cannot restate is left out and said
    (`KeptInstall.dropped`); a pinned Python uv cannot use, and `--with`
    packages that will not resolve, are retried without (plan A4)."""
    if not target or os.environ.get(IN_PLACE_ENV) == "1":
        return None
    kept = kept_from_uv_receipt()
    if kept is None:
        return None
    try:
        tools = installs.tool_dir()
        if not installs.usable(tools):
            return None
    except Exception:  # noqa: BLE001 -- unknown: update in place, as before
        return None
    if current and not is_newer(target, current):
        return CliResult(True, True, False, current, current, f"CLI already at the latest ({current})")
    if target in installs.rejected(tools):
        return CliResult(
            True, False, False, current, current,
            f"CLI {target} failed its check on this machine and was switched back; staying on "
            f"{current} for up to {installs.REJECT_TTL_S // 3600} h, or until a newer release",
        )
    handed = _stage1_said(target)
    if handed is not None:
        return dataclasses.replace(handed, before=current, after=current)
    spec = _dist(kept.extras) + f"=={target}"
    try:
        env, dropped = _install_with_fallbacks(target, spec, kept, tools)
    except subprocess.TimeoutExpired as exc:
        return CliResult(True, False, False, current, current,
                         f"could not install CLI {target}: `uv tool install` timed out after {exc.timeout:.0f} s; "
                         "nothing changed, and the next update tries again")
    except (RuntimeError, OSError, subprocess.SubprocessError) as exc:
        return CliResult(True, False, False, current, current, f"could not install CLI {target}; nothing changed: {exc}")
    problem = installs.selftest(env)
    if problem:
        installs.discard(env)
        return CliResult(
            True, False, False, current, current, f"CLI {target} installed but does not start ({problem}); nothing changed"
        )
    try:
        installs.activate(env, tools=tools)
    except (RuntimeError, OSError) as exc:
        return CliResult(True, False, False, current, current, f"could not switch to CLI {target}; nothing changed: {exc}")
    try:
        from probe.service import client

        client.write_runtime(str(installs.env_python(env)), target)
    except Exception:  # noqa: BLE001 -- the service falls back to the tool path, which is this version now
        pass
    missing, pin = [], None
    with contextlib.suppress(Exception):
        missing, pin = record_left_out(kept, env, tools, list(dropped))
    installs.prune(tools)
    note = dropped_note(kept)
    if missing or pin:
        left = [*(f"--with {item}" for item in missing), *([f"--python {pin}"] if pin else [])]
        note += (f"; left out {', '.join(left)}, which would not install beside it "
                 "(`probe doctor` shows how to add them back)")
    return CliResult(
        True, True, True, current, target,
        f"CLI upgraded {current} → {target} (beside {current}, which stays for a switch back){note}",
    )


def dropped_with_command(prefix: str | Path | None = None) -> tuple[list[str], str] | None:
    """`(what is left out, command)`: the `--with` packages an update had to
    leave out (`active.json` `dropped_with`) that the running version env
    still lacks, and the exact Python pin it ran on before (`dropped_python`)
    when it runs on another now, with the exact `uv tool install` that puts
    them back, with everything it has now. None when there is nothing (or
    this is not a version env)."""
    import shlex

    from probe import __version__

    root = installs.versions_root_of(None if prefix is None else str(prefix))
    if root is None:
        return None
    try:
        record = json.loads((root / installs.ACTIVE_NAME).read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return None
    if not isinstance(record, dict):
        return None
    dropped = record.get("dropped_with") if isinstance(record.get("dropped_with"), list) else []
    pin = record.get("dropped_python") if isinstance(record.get("dropped_python"), str) else None
    kept = kept_from_uv_receipt(prefix) or KeptInstall()
    present = {handoff.requirement_name(requirement) for requirement in kept.with_packages}
    missing = [str(item) for item in dropped if handoff.requirement_name(str(item)) not in present]
    pin = pin if pin and pin != kept.python else None
    if not missing and not pin:
        return None
    command = ["uv", "tool", "install", f"{_dist(kept.extras)}=={__version__}"]
    for requirement in (*kept.with_packages, *missing):
        command += ["--with", requirement]
    if pin or kept.python:
        command += ["--python", pin or kept.python]
    return [*missing, *([f"Python {pin}"] if pin else [])], shlex.join(command)


def _stage1_said(target: str) -> CliResult | None:
    """The hand-off's stage 1 already tried this update in this process
    (`probe.core.adopt`) and could not: its reason, rather than a second
    install that fails the same way. None when it did not, or went fine."""
    try:
        answer = _adopt.stage1_answer() or {}
    except Exception:  # noqa: BLE001
        return None
    result = answer.get("result")
    if result == handoff.Result.BUSY:
        return CliResult(True, False, False, None, None, LOCK_BUSY_MESSAGE)
    if result == handoff.Result.UNCHECKED and answer.get("latest") == target:
        # Installed; its check timed out (a loaded machine). Never switched to
        # by this (old) code: the next update checks it again and hands over.
        return CliResult(
            True, False, False, None, None,
            f"CLI {target} is installed, but its check timed out; nothing changed, and the next update "
            f"tries again ({clean_reason(answer.get('detail'))})",
        )
    if result == handoff.Result.INSTALL_FAILED and answer.get("latest") == target:
        return CliResult(
            True, False, False, None, None,
            f"could not install CLI {target}; nothing changed: {clean_reason(answer.get('detail'))}",
        )
    return None


def record_left_out(old: KeptInstall | None, new_env: Path, tools: Path, dropped: list) -> tuple[list, str | None]:
    """What a switch to `new_env` leaves out of the install it replaces,
    derived from the receipts, never from what one install remembered: the
    `--with` packages the old receipt (`old`) had, earlier records
    (`installs.dropped_with`) and this install's own drops (`dropped`), less
    what `new_env`'s receipt has; and the old exact Python pin when
    `new_env` runs on another. Recorded (`installs.record_dropped_with`): an
    entry goes only once the new receipt has it again (an env kept from an
    earlier install whose drops were never recorded loses nothing). Returns
    `(packages left out, Python pin left out)`."""
    new = kept_from_uv_receipt(new_env) or KeptInstall()
    present = {handoff.requirement_name(item) for item in new.with_packages}
    missing: dict = {}
    for item in [*(old.with_packages if old else ()), *installs.dropped_with(tools), *dropped]:
        name = handoff.requirement_name(item)
        if name not in present:
            missing.setdefault(name, item)
    pin = None
    for candidate in ((old.python if old else None), installs.dropped_python(tools)):
        if isinstance(candidate, str) and candidate and candidate != new.python:
            pin = candidate
            break
    installs.record_dropped_with(list(missing.values()), tools, python=pin)
    return list(missing.values()), pin


def _install_with_fallbacks(target: str, spec: str, kept: KeptInstall, tools: Path, *,
                            rebuild: bool = False) -> tuple[Path, tuple]:
    """`installs.install` tried in the hand-off's order (`handoff.attempts`,
    plan A4): as recorded with the `--with` packages an earlier install left
    out (`installs.dropped_with`) again first, then without the Python pin (a
    new env needs none), then without those, then without any `--with` --
    the last resort on any failure -- within `handoff.INSTALL_BUDGET_S`. A uv
    that times out ends it at once (`subprocess.TimeoutExpired` rises: the
    machine or the network, not the package set). `rebuild`: the version's
    env there is broken (`installs.install`). `(env, the --with packages left
    out)`; the last failure raises."""
    import time

    tries = handoff.attempts(list(kept.with_packages), installs.dropped_with(tools), kept.python)
    every = tries[0][0]
    budget_ends = time.monotonic() + handoff.INSTALL_BUDGET_S
    failure: Exception | None = None
    for packages, python in tries:
        left = min(_UPGRADE_TIMEOUT_S, budget_ends - time.monotonic())
        if left <= 0:
            break
        try:
            env = installs.install(target, spec, with_packages=tuple(packages), python=python, tools=tools,
                                   timeout=left, **({"rebuild": True} if rebuild else {}))
        except (handoff.LockBusy, subprocess.TimeoutExpired):
            raise
        except (RuntimeError, OSError, subprocess.SubprocessError) as exc:
            failure = exc
            continue
        return env, tuple(item for item in every if item not in packages)
    raise failure or RuntimeError(f"the install ran out of its {handoff.INSTALL_BUDGET_S:g} s")


@dataclass
class PluginResult:
    attempted: bool
    confirmed: bool  # plugin is at/past the target — trusted, NOT from claude's exit code
    changed: bool  # the version actually moved this run (vs already-current)
    before: str | None
    after: str | None
    message: str
    # The transcript tap, read before and after the same run. None after means
    # not installed, a supported state (`probe capture off --uninstall`); see
    # `tap_verdict` for how the pair reads against the manifest.
    tap_before: str | None = None
    tap_after: str | None = None
    # WHY the tap did not move, when it did not: the failed command and what it
    # said (`_failed`; the marketplace refresh's own when that failed first), or
    # the in-session no-op the plugin's own branch names. Empty when it moved.
    tap_detail: str = ""
    # Git itself cannot run on this machine (`git_blocker`), so the manual
    # commands would fail the same way and `perform_update` leaves them off.
    # The fix is already in `message` or `tap_detail`, whichever is shown.
    git_blocked: bool = False
    # OBSERVATIONS, never inputs to what this run installs: they say how it
    # ended, for the server's update report (`update_report`) and for whether
    # it failed (`nothing_installed`). Each separates a cause the message alone
    # could only say in prose:
    #: the coding agent's own CLI is not on this process's PATH -- the
    #: detached updater's PATH, not the user's shell.
    missing_binary: bool = False
    #: the marketplace refresh failed, so nothing new could be installed.
    refresh_failed: bool = False
    #: a refresh, update or install command did not complete.
    command_failed: bool = False
    #: the agent's own list of installed plugins could not be read, before or
    #: after the run: nothing listed is then not nothing installed.
    list_unreadable: bool = False
    #: Probe plugins installed under an id this update does not move
    #: (`legacy_plugin_ids`).
    legacy_ids: tuple[str, ...] = ()
    #: The tap version each live capture daemon of this agent still runs, for
    #: every one older than `tap_after` (`stale_tap_daemons`): sessions that
    #: started before the tap was updated. Set by `perform_update`.
    tap_running_stale: tuple[str, ...] = ()
    #: Open sessions follow this update with no restart
    #: (`follows_without_restart`). Set by `perform_update`.
    follows: bool = False


#: The tap's counterpart of the plugin's "returned success but did not advance".
TAP_NOOP = (
    "`claude` returned success but the tap version did not advance "
    "(it may have run inside a Claude Code session, which no-ops)"
)
CODEX_TAP_NOOP = "the Codex reinstall returned success but the tap version did not advance"


def tap_verdict(result: PluginResult, target: str | None) -> tuple[str, bool]:
    """`(line, behind)` for the tap after an update run.

    `behind` is True for an INSTALLED tap still older than the manifest's
    `tap.latest` once the update ran -- the stale tap that capture relies on and
    that nothing reported -- and for a tap the run REMOVED (installed before,
    gone after: capture stops at the next session start). Either fails the
    plugin half. A tap that was never installed is a skip, not a failure. A
    behind line carries the reason (`tap_detail`), the way the plugin's own
    failure does, or "same failure as above" when it IS the plugin's failure,
    printed just above.
    """
    after = result.tap_after
    # A tap that failed with the plugin's own failure (a failed refresh, or any
    # Codex failure) is printed right under it: saying it twice doubled the
    # longest thing on the screen.
    detail = "same failure as above" if result.tap_detail == result.message else result.tap_detail
    if not after:
        if result.tap_before:
            # The no-op sentences ("did not advance") are not what happened. A
            # list that could not be read (Codex) cannot say it is gone.
            seen = "could not be confirmed" if result.list_unreadable else "is gone"
            line = f"transcript tap {result.tap_before} {seen} after the update"
            real = detail if detail not in (TAP_NOOP, CODEX_TAP_NOOP) else ""
            return (f"{line}: {real}" if real else line, True)
        return ("transcript tap not installed (skipped)", False)
    if target and is_newer(target, after):
        line = f"transcript tap is still {after}, behind the latest {target}"
        return (f"{line}: {detail}" if detail else line, True)
    if is_newer(after, result.tap_before):
        line = f"transcript tap updated to {after}"
    elif target:
        line = f"transcript tap already at the latest ({after})"
    else:
        line = f"transcript tap at {after}"
    # Not "behind": the update did its part, and the manual commands would not
    # help. What is left the line says.
    note = running_stale_note(result)
    return (f"{line}; {note}" if note else line, False)


def running_stale_note(result: PluginResult) -> str:
    """One sentence for live capture daemons still on an older tap, or "".

    Where open sessions follow the update (`result.follows`), they move by
    themselves: the plugin's prompt hook hands a watcher from before tap
    0.10.13 to the Probe service at its session's next prompt
    (`hooks/tap_handover.py`), a newer one hands itself over, and the service
    records on the newest installed tap. Anywhere else, a restart."""
    stale = result.tap_running_stale
    if not stale or not result.tap_after:
        return ""
    count = len(stale)
    versions = ", ".join(dict.fromkeys(stale))
    sessions = "1 session" if count == 1 else f"{count} sessions"
    run, them = ("runs", "it") if count == 1 else ("run", "them")
    if result.follows:
        moves = "moves" if count == 1 else "move"
        return (
            f"{sessions} started before the update still {run} tap {versions}; "
            f"{'it' if count == 1 else 'they'} {moves} to {result.tap_after} at the next prompt, no restart needed"
        )
    return (
        f"{sessions} started before the update still {run} tap {versions}; "
        f"restart {them} to switch to {result.tap_after}"
    )


#: The sentence `running_stale_note` stores in an update record, as this
#: release words it ("... move to X at the next prompt, no restart needed") and
#: as every release before 0.304.0 did ("... restart them to switch to X"),
#: with the agent `merged` put before it when the update ran for several.
_STALE_NOTE = re.compile(
    r"(?:(?P<agent>[A-Z][A-Za-z ]{0,30}): )?"
    r"(?:1 session|\d+ sessions) started before the update still runs? tap "
    r"[0-9][0-9A-Za-z.+-]*(?:, [0-9][0-9A-Za-z.+-]*)*; "
    r"(?:restart (?:it|them) to switch to (?P<to>[0-9][0-9A-Za-z.+-]*[0-9A-Za-z+-])"
    r"|(?:it|they) moves? to (?P<moved_to>[0-9][0-9A-Za-z.+-]*[0-9A-Za-z+-]) at the next prompt, no restart needed)"
)


def settle_stale_notes(detail: str, *, plugin_after: Callable[[str], str | None] | None = None) -> str:
    """An update record's plugin detail with each "sessions started before the
    update still run tap X; ..." sentence brought to what is true NOW. The
    record keeps the sentence as the update wrote it; `probe doctor` prints it
    as the state of the machine, and every release before 0.304.0 wrote
    "restart them" whatever was true, so doctor told people to restart sessions
    that move by themselves, long after they had.

    For the agent the sentence names (`merged` puts it first when the update
    ran for several), or, with no name (a record of one pass, whichever agent
    it was), for every agent that captures:
      * no live session runs a tap older than the one the sentence names
        (`stale_tap_sessions`): the sentence is taken out;
      * some still do, and every one of them moves by itself at its next
        prompt (`follows_without_restart` for its agent, on the state now:
        `plugin_after(agent)` is that agent's installed Probe plugin, None
        when it has none): the sentence says so, counted afresh;
      * otherwise, and whenever a look could not be made: the sentence stays
        word for word.
    Never raises: the detail as it was."""
    if not detail or "started before the update" not in detail:
        return detail
    try:
        harnesses = [h for h in get_registry().all() if getattr(h, "capture", None) is not None]
        by_label = {h.label: h.id for h in harnesses if getattr(h, "label", None)}

        def settle(match: re.Match) -> str:
            target = match["to"] or match["moved_to"]
            if match["agent"]:
                source = by_label.get(match["agent"])
                if source is None:
                    return match[0]
                candidates = [source]
            else:
                candidates = [h.id for h in harnesses]
            stale: dict[str, tuple[str, ...]] = {}
            for source in candidates:
                found = stale_tap_sessions(source, target)
                if found is None:
                    return match[0]  # could not look: never "none left"
                if found:
                    stale[source] = found
            if not stale:
                return ""
            follows = all(
                follows_without_restart(source, PluginResult(
                    True, True, False, None, plugin_after(source) if plugin_after else None, "",
                    tap_after=target, tap_running_stale=found))
                for source, found in stale.items()
            )
            if not follows:
                return match[0]
            versions = tuple(sorted((v for found in stale.values() for v in found),
                                    key=lambda v: _triplet(v) or (0, 0, 0)))
            note = running_stale_note(PluginResult(True, True, False, None, None, "", tap_after=target,
                                                   tap_running_stale=versions, follows=True))
            return f"{match['agent']}: {note}" if match["agent"] else note

        settled = _STALE_NOTE.sub(settle, detail)
        if settled == detail:
            return detail
        # The separators the taken sentences leave behind.
        settled = re.sub(r"(?:;\s*){2,}", "; ", settled)
        return re.sub(r"^\s*;\s*|\s*;\s*$", "", settled).strip()
    except Exception:  # noqa: BLE001 - see docstring
        return detail


# -- live capture daemons ---------------------------------------------------
#
# An update moves the tap a coding agent INSTALLS; it cannot move the daemon a
# running session already started. Each session runs its own capture daemon for
# as long as the session lives, the server shows a machine's OLDEST live tap,
# and researchers keep sessions alive for days. So a machine whose update
# worked can still report the old tap: anthrogen's dev pod and new-workspace's
# laptop both read tap 0.9.3 on 2026-10-07, each with a session born on 10-04
# (before its tap moved) still uploading, while the dev pod's own update report
# said its tap was current at 0.9.14. These find those daemons, so the report
# says why beside "current": the tap's detail, the printed line, `probe doctor`.

#: A capture daemon as `hooks/session-start.sh` spawns it:
#: `<python> -m tap watch --session-id <id> --cwd <dir> --plugin-root <root>
#: --transcript <path>` (`--transcript-dir <dir>` for Codex). Its wrapper's own
#: command line carries the same words with `"$SID"` quoted, which the id's
#: character class refuses. `tap start` spawns without `--plugin-root`, from the
#: tap installed now, so it is never the stale one this looks for.
_TAP_DAEMON = re.compile(
    r"-m tap watch --session-id (?P<sid>[A-Za-z0-9_.:-]+) (?:.*? )?"
    r"--plugin-root (?P<root>.+?) --transcript"
)
_VERSION_DIR = re.compile(r"^\d+\.\d+\.\d+$")


@dataclass(frozen=True)
class TapDaemon:
    session_id: str
    #: The plugin root it was started from (it may no longer exist: Codex
    #: replaces a plugin's folder when it updates it).
    root: str
    version: str | None


def _process_commands() -> list[str]:
    """This user's processes' full command lines: `ps`, else Linux's `/proc`.
    Empty when neither can be read (Windows, a sandbox)."""
    if not hasattr(os, "getuid"):
        return []
    uid = os.getuid()
    try:
        listing = subprocess.run(  # noqa: S603 - fixed binary, no shell
            ["ps", "-ww", "-U", str(uid), "-o", "command="],
            capture_output=True, text=True, stdin=subprocess.DEVNULL, timeout=5, check=False,
        )
        if listing.returncode == 0:
            return [line.strip() for line in listing.stdout.splitlines() if line.strip()]
    except (OSError, subprocess.SubprocessError):
        pass
    commands: list[str] = []
    try:
        entries = [entry for entry in os.scandir("/proc") if entry.name.isdigit()]
    except OSError:
        return []
    for entry in entries:
        try:
            if entry.stat().st_uid != uid:
                continue
            with open(os.path.join(entry.path, "cmdline"), "rb") as handle:
                raw = handle.read()
        except OSError:
            continue  # exited between the listing and the read
        text = raw.replace(b"\0", b" ").decode(errors="replace").strip()
        if text:
            commands.append(text)
    return commands


def _daemon_version(session_id: str, root: str) -> str | None:
    """The tap a daemon runs: its marketplace folder's name (Claude Code and
    Codex keep one folder per version), else the record its spawner left beside
    its pid file (taps 0.9.16+), else the manifest in its root."""
    name = Path(root).name
    if _VERSION_DIR.match(name):
        return name
    from probe.cli import capture_state

    harnesses = [h for h in get_registry().all() if h.capture is not None]
    for harness in harnesses:
        record = capture_state._watcher_dir(harness.id) / f"{harness.capture.watcher_prefix}-watcher-{session_id}.version"  # noqa: SLF001
        try:
            text = record.read_text(encoding="utf-8").strip()
        except OSError:
            continue
        if text:
            return text
    for harness in harnesses:
        manifest_dir = (harness.plugin or {}).get("manifest_dir")
        if not manifest_dir:
            continue
        try:
            version = json.loads((Path(root) / manifest_dir / "plugin.json").read_text())["version"]
        except (OSError, ValueError, KeyError, TypeError):
            continue
        if isinstance(version, str):
            return version
    return None


def tap_daemons(commands: list[str] | None = None) -> list[TapDaemon]:
    """Every live capture daemon this user runs, one per session and root
    (from `commands`, a process listing already read, else `_process_commands`)."""
    found: dict[tuple[str, str], TapDaemon] = {}
    for command in _process_commands() if commands is None else commands:
        match = _TAP_DAEMON.search(command)
        if match is None:
            continue
        key = (match["sid"], match["root"])
        if key not in found:
            found[key] = TapDaemon(key[0], key[1], _daemon_version(*key))
    return list(found.values())


def hosted_taps(source: str) -> dict[str, str]:
    """`{session id: tap version}` for each session of `source` the Probe
    service records now: the tap the service LOADED, which every one of its
    recorders runs, whatever tap the session named when it asked. It loads one
    tap and keeps it until a session names a newer one, so after an update its
    sessions keep the old tap, and no `tap watch` command line shows it.

    From `service.status` alone (`recorders[].tap_version`, `harness`): a
    service too old to say which tap it loaded, or a recorder that names no
    agent, is left out rather than guessed at. Empty when no service answers:
    then nothing is recorded there."""
    rows = service_calls.recorders()
    found: dict[str, str] = {}
    for row in rows or []:
        sid, agent, version = row.get("sid"), row.get("harness"), row.get("tap_version")
        if row.get("alive") is False or agent != source:
            continue
        if isinstance(sid, str) and isinstance(version, str) and version:
            found[sid] = version
    return found


def stale_tap_daemons(source: str, installed: str | None) -> tuple[str, ...]:
    """The version each live capture daemon of `source` runs, for every one
    older than the tap `installed` now, oldest first: each session's own `tap
    watch` (a daemon is `source`'s when it was started from a folder under
    that agent's home), and each session the Probe service records on the tap
    it loaded (`hosted_taps`), one per session. NEVER RAISES: an observation
    for the report, never a reason an update fails (what could not be looked
    at counts as none here)."""
    return _stale(source, installed, strict=False) or ()


def stale_tap_sessions(source: str, installed: str | None) -> tuple[str, ...] | None:
    """`stale_tap_daemons`, or None when this process could not look: no
    process listing could be read (this process is always in one, so an empty
    listing is an unreadable one: Windows, a sandbox without `ps` or `/proc`),
    the agent's home is unknown, or the look failed. For a claim made to a
    person (`settle_stale_notes`, doctor's warning), where "could not look"
    must never read as "none left". Never raises."""
    return _stale(source, installed, strict=True)


def _stale(source: str, installed: str | None, *, strict: bool) -> tuple[str, ...] | None:
    if not installed:
        return ()
    try:
        harness = get_registry().get(source)
        home = harness.home_dir() if harness is not None else None
        if home is None:
            return None if strict else ()
        home = home.resolve()
        commands = _process_commands()
        if strict and not commands:
            return None
        running: dict[str, str] = {}
        stale = []
        for daemon in tap_daemons(commands):
            if daemon.version and Path(daemon.root).resolve().is_relative_to(home):
                running.setdefault(daemon.session_id, daemon.version)
                if is_newer(installed, daemon.version):
                    stale.append(daemon.version)
        try:
            hosted = hosted_taps(source)
        except Exception:  # noqa: BLE001 - the daemons above are still worth reporting
            if strict:
                return None
            hosted = {}
        for sid, version in hosted.items():
            # A session whose own `tap watch` still holds it is counted above
            # (the service's recorder waits for that one to let go).
            if sid not in running and is_newer(installed, version):
                stale.append(version)
        return tuple(sorted(stale, key=lambda v: _triplet(v) or (0, 0, 0)))
    except Exception:  # noqa: BLE001 - see the docstrings
        return None if strict else ()


def tap_changed(result: PluginResult) -> bool:
    return is_newer(result.tap_after, result.tap_before)


#: The first tap whose `tap watch` hands its session to the Probe service
#: (`hooks/tap_handover.py` HANDBACK_TAP), and the first on protocol 2, which
#: the prompt hook can move at all (PROTOCOL2_TAP).
HANDBACK_TAP = "0.10.13"
PROTOCOL2_TAP = "0.4.5"
def _harness_can(source: str, capability: str) -> bool:
    """Does the registry row `source` names have `capability`? False for a
    name the registry does not know."""
    harness = get_registry().find(source)
    return harness is not None and harness.can(capability)


def _ledger_user_scope(plugin_ids: tuple[str, ...]) -> bool:
    """Is every install Claude Code's ledger records for these plugins user
    scope, with the first of them installed at all? A project-scoped install
    serves its project only, and an open session's hooks never hand over to
    it (`dispatch.installed_root`)."""
    path = Path.home() / ".claude" / "plugins" / "installed_plugins.json"
    try:
        plugins = json.loads(path.read_text()).get("plugins") or {}
        if not plugins.get(plugin_ids[0]):
            return False
        return all(
            isinstance(entry, dict) and entry.get("scope") == "user"
            for plugin_id in plugin_ids
            for entry in plugins.get(plugin_id) or []
        )
    except Exception:  # noqa: BLE001 - unreadable: unproven, so the restart line
        return False


def _windows() -> bool:
    return os.name == "nt"


def _recording_now() -> set:
    """The sessions the running Probe service records now: its recorders whose
    loop holds the session's claim (`service.status`). Empty when none answers."""
    rows = service_calls.recorders()
    return {r["sid"] for r in rows or [] if r.get("alive") is True and r.get("recording") is True and r.get("sid")}


def follows_without_restart(
    source: str, result: PluginResult, tap_after: str | None = None, *, predicting: bool = False
) -> bool:
    """Do this agent's open sessions follow the update with no restart, so
    "no restart needed" is true? Only for an agent whose open sessions follow
    updates (the registry's `follows_updates`: Claude Code, Codex, Kimi Code;
    one that keeps its manifest from its start, `loaded_records`, only when every
    live process's record proves it loaded what is installed now:
    `kimi_live.sessions_follow`), not on
    Windows (the prompt hook leaves its sessions alone: no Git Bash pid can be
    proven there, `tap_handover.watchers_movable`), every install at user scope
    where the agent's ledger has scopes (`scoped_installs`: Claude Code's), a
    tap that hands its sessions
    to the Probe service (`tap_after`, default the one installed now:
    HANDBACK_TAP or later, or none at all) and every session still on an
    older tap on protocol 2 (PROTOCOL2_TAP), which the prompt hook can move:
    that hook ships in the Probe plugin (`result.after`), so a watcher from
    before the hand-back follows only where it is installed (a session the
    service records moves with the service). Anything else keeps the restart
    line. `predicting`: asked before the release is installed (the manual
    update line); an agent whose proof reads what is installed now
    (`loaded_records`, and pi's pins) then never follows. Never raises."""
    try:
        from probe.harness.registry import (
            CAPABILITY_FOLLOWS_UPDATES,
            CAPABILITY_LOADED_RECORDS,
            CAPABILITY_SCOPED_INSTALLS,
            FAMILY_EXTENSION,
        )

        if not _harness_can(source, CAPABILITY_FOLLOWS_UPDATES) or _windows():
            return False
        harness_row = get_registry().find(source)
        if harness_row is not None and harness_row.family == FAMILY_EXTENSION:
            # pi: its shim switches to the pinned version at a session's next
            # turn; proven per live pi process from its shim's record.
            from probe.cli import pi_pins

            if predicting or not pi_pins.sessions_follow((harness_row.binary,)):
                return False
        if _harness_can(source, CAPABILITY_LOADED_RECORDS):
            if predicting:
                return False
            harness = get_registry().find(source)
            titles = (getattr(harness, "process_title", None), getattr(harness, "binary", None))
            if harness is None or not kimi_live.sessions_follow(harness.id, titles, recorded=_recording_now()):
                return False
        if _harness_can(source, CAPABILITY_SCOPED_INSTALLS) and not _ledger_user_scope(
            (tracking_plugin_id(source), TAP_PLUGIN_ID)
        ):
            return False
        tap = result.tap_after if tap_after is None else tap_after
        if tap and is_newer(HANDBACK_TAP, tap):
            return False
        stale = result.tap_running_stale
        if not result.after and any(is_newer(HANDBACK_TAP, version) for version in stale):
            return False
        return not any(is_newer(PROTOCOL2_TAP, version) for version in stale)
    except Exception:  # noqa: BLE001 - see docstring
        return False


def listed_version(listing: str | None, name: str) -> str | None:
    """`name`'s version out of Codex/Kimi's `a=1.0, b=2.0` listing; a bare
    version (Claude's) passes through."""
    if not listing:
        return None
    if "=" not in listing:
        return listing
    for part in listing.split(","):
        key, _, value = part.strip().partition("=")
        if key == name:
            return value or None
    return None


def nothing_installed(result: PluginResult, source: str) -> bool:
    """True when an attempted run found none of Probe's plugins in `source`'s
    agent -- neither the tracking plugin nor the tap, before the run or after
    it, by a list it could read. The update had nothing to move, so whatever its
    commands said (a `claude plugin update` of a plugin that is not there fails,
    as does a refresh of a marketplace never added), it is NOT a failed update:
    the same reading as an agent that is not on PATH at all.

    THE ONE RULE for both readings of a run: whether the plugin half failed
    (`upgrading._perform_update`'s `plugin_ok`, the local record and the
    report's outcome) and what the report's plugin component says
    (`update_report.plugin_component`, `not_installed`). They used to disagree:
    a machine with Claude Code or Codex but no Probe plugin in it reported a
    failed update on every session start, with nothing in the report failing.
    """
    if not result.attempted or result.confirmed or result.list_unreadable:
        return False
    name = tracking_plugin_name(source)
    return not (
        listed_version(result.before, name)
        or listed_version(result.after, name)
        or result.tap_before
        or result.tap_after
    )


def update_plugin(target_latest: str | None) -> PluginResult:
    """Update the Claude Code plugin via `claude`, then VERIFY it actually advanced (H1).

    The child is spawned with no TTY and captured output (H2) so a raw-mode TUI
    crash writes to a pipe, never the parent terminal. A zero exit is NOT trusted;
    we confirm by re-reading the installed plugin version.
    """
    claude = shutil.which("claude")
    if not claude:
        # The ledger is a file, readable without `claude`: what is installed
        # rides along, so a report can say "tap 0.9.3, and `claude` was not on
        # PATH" rather than just the second half.
        tap = installed_tap_version()
        return PluginResult(
            False, False, False, None, None, "`claude` not found on PATH (skipping plugin update)",
            tap_before=tap, tap_after=tap, missing_binary=True,
            legacy_ids=legacy_plugin_ids(),
        )

    before = installed_plugin_version()
    tap_before = installed_tap_version()
    readable_before = _ledger_readable()
    # Both go through claude_cli, which carries the DEVNULL this step always
    # needed -- no TTY -> no raw-mode on the parent terminal. The refresh goes
    # through plugin_cli so it gets the same REFRESH_TIMEOUT_S every other
    # refresh does; it had its own 90s here, which cut off a slow clone 30s
    # before Claude's own 120s bound would have.
    refresh = plugin_cli.refresh_marketplace(plugin_cli.CLAUDE, MARKETPLACE)
    failed_run = None if refresh.ok else refresh
    if failed_run is None:
        result = claude_cli.run(
            ["plugin", "update", tracking_plugin_id()], timeout=claude_cli.CAPTURE_TIMEOUT_S
        )
        failed_run = None if result.ok else result
    failure = _failed(failed_run) if failed_run is not None else ""
    completed = failed_run is None

    # The tap, best-effort and deliberately OUTSIDE `completed`: it is a
    # separate plugin that many users do not have, so `claude` failing here
    # means "not installed" far more often than "update broken". Letting that
    # flip `completed` would report the whole update as failed to everyone
    # without a tap. It is only the install step, so it is skipped when the
    # refresh failed: there is nothing new to install, and a dead network
    # would cost a second timeout for nothing. Its OUTCOME is not discarded:
    # the versions read on either side of it, and why it did not move, go back
    # on the result, and `perform_update` prints them and fails loudly on a tap
    # left behind the manifest (`tap_verdict`). Reading nothing back is how a
    # stale tap went unreported.
    #
    # A failed refresh is the tap's reason too. With the plugin already
    # current, the plugin's own line never mentions the refresh, and a bare
    # "skipped" left the reason, and a blocked git's fix, off the screen.
    tap_detail = failure
    if refresh.ok:
        tap_run = claude_cli.run(
            ["plugin", "update", TAP_PLUGIN_ID], timeout=claude_cli.CAPTURE_TIMEOUT_S
        )
        tap_detail = "" if tap_run.ok else _failed(tap_run)
    tap_after = installed_tap_version()
    if not tap_detail and not is_newer(tap_after, tap_before):
        # Exit 0 and nothing moved: the same reading the plugin's `completed`
        # branch gives its own version below.
        tap_detail = TAP_NOOP
    tap = {
        "tap_before": tap_before,
        "tap_after": tap_after,
        "tap_detail": tap_detail,
        # Only the refresh runs git, and its failure is on screen wherever the
        # manual commands would be: the plugin's line when that is unconfirmed,
        # the tap's when it is behind. Keyed on a later step, a plugin already
        # current could hide the commands with the fix nowhere in sight.
        "git_blocked": not refresh.ok and bool(git_blocker(refresh.detail)),
        "refresh_failed": not refresh.ok,
        "command_failed": not completed,
        "list_unreadable": not (readable_before and _ledger_readable()),
        "legacy_ids": legacy_plugin_ids(),
    }

    after = installed_plugin_version()
    changed = is_newer(after, before)
    # H1: trust the observed version, not claude's exit code. "Confirmed" = the plugin
    # is at (or past) the target, or it strictly advanced this run.
    at_target = bool(target_latest and after and not is_newer(target_latest, after))
    if at_target or changed:
        msg = f"plugin updated to {after}" if changed else f"plugin already at the latest ({after})"
        return PluginResult(True, True, changed, before, after, msg, **tap)
    if completed:
        return PluginResult(
            True,
            False,
            False,
            before,
            after,
            "`claude` returned success but the plugin version did not advance "
            "(it may have run inside a Claude Code session, which no-ops)",
            **tap,
        )
    return PluginResult(True, False, False, before, after, failure, **tap)


_REASON_MAX = 500
#: Codex opens with "WARNING: proceeding, even though we could not create PATH
#: aliases" on some machines, whatever the actual failure was.
_NOISE_PREFIX = "WARNING:"
#: Complete CSI (colour) and OSC sequences. Removed whole: dropping only the ESC
#: byte leaves `[31m` glued to the next word, which hides it from the scrubber.
_TERMINAL_SEQUENCE = re.compile(r"\x1b\[[0-?]*[ -/]*[@-~]|\x1b\][^\x07\x1b]*(?:\x07|\x1b\\)")


#: The interactive form, not `-license accept`: `probe doctor` replays this
#: inside agent sessions, and accepting Apple's license is the person's call.
_LICENSE_FIX = (
    "git on this Mac is blocked until the Xcode license is accepted. "
    "Run `sudo xcodebuild -license` in a terminal and agree to it, then try again."
)
#: Never installed or removed by an OS upgrade (`--install`), or pointing at
#: an Xcode that was moved or deleted (`--reset`).
_TOOLS_FIX = (
    "git on this Mac cannot find the Xcode command line tools. Run "
    "`xcode-select --install`, or `sudo xcode-select --reset` if they are already "
    "installed, then try again."
)
#: Machine problems that stop git itself, and so every marketplace refresh,
#: before `claude` or `codex` get anywhere: macOS runs `git` through an Xcode
#: shim that refuses until its license is accepted and its tools are in place.
#: Both CLIs pass that on as a paragraph that buries the one command that fixes
#: it, and the manual commands printed after a failure would hit the same wall.
#: Keyed on lowercased fragments of Apple's own sentences, which it rewords:
#: "You have not agreed to the Xcode license agreements", "... to the Xcode
#: and Apple SDKs license", "Agreeing to the Xcode/iOS license requires admin
#: privileges", "Agreeing to the Xcode and Apple SDKs license requires ...".
_GIT_BLOCKERS = {
    "xcodebuild -license": _LICENSE_FIX,
    "not agreed to the xcode": _LICENSE_FIX,
    "xcode and apple sdks license": _LICENSE_FIX,
    "xcode/ios license": _LICENSE_FIX,
    # "invalid active developer path (…)", "active developer path (…) does not
    # exist", and the shim on a Mac that never had them.
    "active developer path": _TOOLS_FIX,
    "no developer tools were found": _TOOLS_FIX,
}


def git_blocker(text: str | None) -> str:
    """The fix for a machine problem that stopped git, or "" for any other failure.

    A line carrying what the git SERVER sent (`remote: …` wherever a CLI
    wrapped it, or git's own `fatal: remote error: …` for an ERR packet) is
    never read: a server quoting Apple's wording must not stand in for the
    real error, which this replaces.
    """
    for line in _TERMINAL_SEQUENCE.sub("", text or "").lower().splitlines():
        if "remote:" in line or "remote error:" in line:
            continue
        for key, fix in _GIT_BLOCKERS.items():
            if key in line:
                return fix
    return ""


def _failed(result: claude_cli.Result) -> str:
    """Which command failed and everything it said about why, on one line.

    A known machine problem is said as its fix instead. The raw output is
    matched, not the cleaned reason, which can lose its middle.
    """
    fix = git_blocker(result.detail)
    if fix:
        return f"not updated: {fix}"
    return f"`{result.command}` did not complete: {clean_reason(result.detail)}"


def clean_reason(text: str | None) -> str:
    """A child's output as one line that is safe to print, store and replay.

    Printing only "did not complete" left a researcher with nothing to act on
    and nothing to report: the child's own error was captured and dropped, and
    `probe doctor` recorded the same empty sentence.

    NOT the last line. Codex puts the reason first and ends on a bare "Error: 1
    upgrade failure(s) occurred."; Claude splits one error over its own summary
    and git's `fatal:` line. So every line is kept, bar Codex's WARNING noise
    (unless that is all there is), and an over-long one loses its MIDDLE: the
    deciding line can be either end.

    It is printed, stored in the update record and replayed by `probe doctor`,
    which agents run inside captured sessions. So credentials in a git URL and
    home paths are scrubbed from the RAW text first (the scanner recognises a
    token by what surrounds it, and a colour code glued on defeats that), then
    terminal sequences and control characters go, then it is scrubbed again in
    case removing them joined a token back together. The scrubber raises on
    input it cannot bound; that withholds the text rather than crashing the
    update before it records its outcome.
    """
    try:
        text = _TERMINAL_SEQUENCE.sub("", scrub_text(text or ""))
        lines = [
            "".join(ch for ch in line.replace("\t", " ") if ch.isprintable()).strip()
            for line in text.splitlines()
        ]
        lines = [line for line in lines if line]
        lines = [line for line in lines if not line.startswith(_NOISE_PREFIX)] or lines
        reason = scrub_text(" · ".join(lines))
    except Exception:  # noqa: BLE001 - see the docstring: withhold, never crash
        return "output withheld: it could not be scrubbed"
    if not reason:
        return "no output"
    if len(reason) > _REASON_MAX:
        keep = (_REASON_MAX - 3) // 2
        reason = f"{reason[:keep]} … {reason[-keep:]}"
    return reason


#: Why this thread's last `_codex_plugin_versions` read nothing, for the
#: update's failure line ("" when it read the list).
_codex_list = threading.local()


def _codex_plugin_versions(_codex: str | None = None) -> dict[str, str] | None:
    """Codex's installed plugins, `{name: version}`. None when the list could
    not be read (the command failed, or printed something that is not its JSON
    object): that is not an empty list, and `nothing_installed` must not read
    it as one. Why it could not is `_codex_list.problem`."""
    _codex_list.problem = ""
    result = plugin_cli.list_plugins(plugin_cli.CODEX)
    if not result.ok:
        _codex_list.problem = clean_reason(result.detail or "it failed with no output")
        return None
    try:
        body = json.loads(result.detail)
    except ValueError:
        _codex_list.problem = f"it printed something that is not JSON: {clean_reason(result.detail)[:120]!r}"
        return None
    if not isinstance(body, dict):
        _codex_list.problem = "it printed JSON that is not an object"
        return None
    return {
        row["name"]: row["version"]
        for row in body.get("installed") or []
        if isinstance(row, dict)
        and isinstance(row.get("name"), str)
        and isinstance(row.get("version"), str)
    }


def _codex_versions_on_disk() -> dict[str, str] | None:
    """`codex_config.installed_plugin_versions` for Probe's marketplace; None
    when it cannot be read."""
    from probe.cli import codex_config

    try:
        return codex_config.installed_plugin_versions(MARKETPLACE)
    except Exception:  # noqa: BLE001 - a second opinion that cannot answer is no answer
        return None


def _listed_summary(versions: dict[str, str]) -> str:
    """How many plugins a Codex list read, naming Probe's."""
    probe = sorted(name for name in versions if name.startswith("probe-"))
    named = f": {', '.join(f'{name}={versions[name]}' for name in probe)}" if probe else ""
    return f"{len(versions)} plugin{'' if len(versions) == 1 else 's'}{named}"


def update_codex_plugins() -> PluginResult:
    """Refresh and re-add both Codex plugins, then verify the installed list.

    Codex has no separate ``plugin update`` command. Re-adding an installed
    plugin is its idempotent reinstall path and moves it to the refreshed
    marketplace snapshot without first removing the working copy.
    """
    codex = shutil.which("codex")
    if not codex:
        return PluginResult(
            False, False, False, None, None, "`codex` not found on PATH (skipping plugin update)",
            missing_binary=True,
        )
    names = (tracking_plugin_name("codex"), "probe-research-tap")
    listed_before = _codex_plugin_versions(codex)
    before_versions = listed_before if listed_before is not None else _codex_versions_on_disk() or {}
    failed_run = None
    result = plugin_cli.refresh_marketplace(plugin_cli.CODEX, MARKETPLACE)
    if not result.ok and _CODEX_NOT_CONFIGURED in (result.detail or "").lower():
        # The config entry is gone (a hand-edited or deleted config.toml),
        # so `upgrade` can never succeed again. Re-add it -- which also clears
        # a stale checkout left behind -- and refresh once more.
        added = plugin_cli.add_marketplace(plugin_cli.CODEX, MARKETPLACE_REPO, name=MARKETPLACE)
        result = plugin_cli.refresh_marketplace(plugin_cli.CODEX, MARKETPLACE) if added.ok else added
    refresh_failed = not result.ok
    if not result.ok:
        failed_run = result
    for name in names:
        if failed_run is not None:
            break
        result = plugin_cli.install(plugin_cli.CODEX, f"{name}@{MARKETPLACE}")
        if not result.ok:
            failed_run = result
    failure = _failed(failed_run) if failed_run is not None else ""
    listed_after = _codex_plugin_versions(codex)
    list_problem = getattr(_codex_list, "problem", "")
    after_versions = listed_after or {}
    read_from_files = False
    if listed_after is None and not failure:
        # The list could not answer (a timeout, on a Mac): Codex's own files
        # say what it installed (`codex_config.installed_plugin_versions`).
        on_disk = _codex_versions_on_disk()
        if on_disk and all(on_disk.get(name) for name in names):
            after_versions, read_from_files = on_disk, True
    missing = [name for name in names if not after_versions.get(name)]
    confirmed = not failure and not missing
    changed = confirmed and any(
        before_versions.get(name) != after_versions.get(name) for name in names
    )
    before = (
        ", ".join(f"{name}={version}" for name, version in sorted(before_versions.items())) or None
    )
    # Unconfirmed, still what IS listed: a first install that added the
    # tracking plugin and then failed on the tap left Probe in Codex, and
    # reading None here made that "nothing installed" (`nothing_installed`).
    after = (
        ", ".join(f"{name}={after_versions.get(name)}" for name in names)
        if confirmed
        else ", ".join(f"{name}={after_versions[name]}" for name in names if after_versions.get(name))
        or None
    )
    tap_before = before_versions.get("probe-research-tap")
    tap_after = after_versions.get("probe-research-tap")
    tap = {
        "tap_before": tap_before,
        "tap_after": tap_after,
        "tap_detail": failure
        or ("" if is_newer(tap_after, tap_before) else CODEX_TAP_NOOP),
        "git_blocked": failed_run is not None and bool(git_blocker(failed_run.detail)),
        "refresh_failed": refresh_failed,
        "command_failed": failed_run is not None,
        "list_unreadable": listed_before is None or listed_after is None,
        "legacy_ids": legacy_plugin_ids(sorted({*before_versions, *after_versions})),
    }
    if confirmed:
        message = f"Codex plugins {'updated' if changed else 'verified'} ({after})"
        if read_from_files:
            message += f"; read from Codex's plugin files (`codex plugin list --json`: {list_problem})"
        message += _approve_codex_hooks()
        return PluginResult(True, True, changed, before, after, message, **tap)
    return PluginResult(
        True,
        False,
        False,
        before,
        after,
        # Not "does not show": the list may be the thing that failed
        # (`list_unreadable` says which; the sentence is true either way).
        failure
        or (
            f"could not confirm {' or '.join(missing)}: `codex plugin list --json` could not be read "
            f"after reinstalling ({problem})"
            if listed_after is None and (problem := list_problem)
            else f"could not confirm {' or '.join(missing)} in `codex plugin list --json` after reinstalling"
            # What it does list: none at all is a list Probe could not parse.
            f" (it lists {_listed_summary(after_versions)})"
        ),
        **tap,
    )


def _approve_codex_hooks() -> str:
    """Approve Probe's hooks in Codex after an update, and say so. Codex skips an
    entry whose text changed until it is approved again, and a machine set up
    before the wizard approved them has never had them approved. Empty when
    nothing waited or Codex could not be asked (status and doctor still say)."""
    from probe.cli import codex_hooks

    try:
        outcome = codex_hooks.approve()
    except Exception:  # noqa: BLE001 - approve never raises; an update never fails on it either way
        return ""
    if outcome is None:
        return ""
    count = len(outcome.approved)
    said = f"; approved {count} Probe hook{'s' if count != 1 else ''} in Codex" if count else ""
    if not outcome.done:
        said += f"; Probe's hooks still wait for approval in Codex ({outcome.error or 'a Probe hook still waits'}): type /hooks there"
    return said


def update_kimi_plugins() -> PluginResult:
    """Re-copy every Probe plugin Kimi Code has installed (Kimi has no update
    command; `kimi_config.install_plugin` replaces the copy in place), then
    verify the versions from the copies themselves."""
    from probe.cli import kimi_config

    if not kimi_config.binary_available():
        return PluginResult(
            False, False, False, None, None, "`kimi` not found on PATH (skipping plugin update)",
            missing_binary=True,
        )
    listed = plugin_cli.list_plugins(plugin_cli.KIMI)
    if not listed.ok:
        # Unread, not empty: a failure, never "nothing installed".
        return PluginResult(
            True, False, False, None, None,
            listed.detail or "could not read Kimi Code's plugin list",
            command_failed=True, list_unreadable=True,
        )
    installed = [
        line.split()[0]
        for line in listed.detail.splitlines()
        if line.split() and line.split()[0] in kimi_config.PLUGIN_IDS
    ]
    before_versions = {name: kimi_config.plugin_version(name) for name in installed}
    failed_run = None
    for name in installed:
        result = plugin_cli.install(plugin_cli.KIMI, name)
        if not result.ok:
            failed_run = result
            break
    failure = _failed(failed_run) if failed_run is not None else ""
    after_versions = {name: kimi_config.plugin_version(name) for name in installed}
    confirmed = not failure and all(after_versions.values())
    changed = confirmed and any(before_versions[n] != after_versions[n] for n in installed)
    before = ", ".join(f"{n}={v}" for n, v in sorted(before_versions.items())) or None
    after = ", ".join(f"{n}={after_versions[n]}" for n in installed) if confirmed else None
    tap = {
        "tap_before": before_versions.get("probe-research-tap"),
        "tap_after": after_versions.get("probe-research-tap"),
        "tap_detail": failure,
        "git_blocked": False,
        "command_failed": failed_run is not None,
    }
    if not installed:
        return PluginResult(False, False, False, None, None, "no Probe plugins installed in Kimi Code", **tap)
    if confirmed:
        message = f"Kimi Code plugins {'updated' if changed else 'verified'} ({after})"
        return PluginResult(True, True, changed, before, after, message, **tap)
    return PluginResult(True, False, False, before, after, failure or "could not confirm the Kimi Code plugins", **tap)


def manual_kimi_plugin_commands() -> str:
    from probe.cli import kimi_config

    return "\n".join(
        f"/plugins install {kimi_config.managed_dir(name)}   # inside Kimi Code"
        for name in ("probe-research", "probe-research-tap")
    )


def manual_plugin_commands() -> str:
    return (
        f"claude plugin marketplace update {MARKETPLACE}\n"
        f"claude plugin update {tracking_plugin_id()}\n"
        f"claude plugin update {TAP_PLUGIN_ID}  # skip if you do not have the tap"
    )


def manual_codex_plugin_commands() -> str:
    return (
        f"codex plugin marketplace upgrade {MARKETPLACE}\n"
        f"codex plugin add {tracking_plugin_id('codex')}\n"
        f"codex plugin add probe-research-tap@{MARKETPLACE}"
    )
