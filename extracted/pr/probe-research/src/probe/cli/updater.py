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

import json
import os
import re
import shutil
import subprocess
import sys
import dataclasses
from dataclasses import dataclass
from pathlib import Path

import httpx

from probe.cli import claude_cli, plugin_cli
from probe.cli.capabilities import TAP_PLUGIN_ID, tracking_plugin_name
from probe.sdk.redaction import scrub_text
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

    if "/uv/tools/probe-research/" in s:
        return Install(Method.UV_TOOL)
    if "/uv/tools/probe-agent/" in s:
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


# -- upgrade actions --------------------------------------------------------
@dataclass
class CliResult:
    ran: bool
    ok: bool  # the CLI is at (or past) the target after the attempt — VERIFIED
    changed: bool  # the installed version actually moved
    before: str | None
    after: str | None
    message: str


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
    plus ``extras`` (the ones the install already records)."""
    wanted = {"all", *extras}
    try:
        import pydantic_ai  # noqa: F401
    except ImportError:
        pass
    else:
        wanted.add("daemon")
    return f"{DIST}[{','.join(sorted(wanted))}]"


@dataclass(frozen=True)
class KeptInstall:
    """What a reinstall must carry over from the install it replaces (#2043
    review): the extras it records beyond ours, the packages the user added
    beside it (`uv tool install --with`, `pipx inject`), and its Python."""

    extras: tuple[str, ...] = ()
    with_packages: tuple[str, ...] = ()
    python: str | None = None


#: uv-receipt.toml requirement keys a reinstall can restate. Anything else
#: (an editable path, constraints) and the receipt is not rewritten at all.
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
    its `uv-receipt.toml` (empty when there is none). None when the receipt
    cannot be restated faithfully: the caller then leaves it alone instead of
    dropping something from it. `uv tool install` REPLACES the receipt, so an update
    that restated only `probe-research[all]` uninstalled every `--with`
    package (`probe import wandb` needs one)."""
    from probe._compat import tomllib

    path = Path(prefix if prefix is not None else sys.prefix) / "uv-receipt.toml"
    try:
        text = path.read_text(encoding="utf-8")
    except FileNotFoundError:
        return KeptInstall()  # no receipt: nothing recorded, nothing to lose
    except OSError:
        return None
    try:
        tool = tomllib.loads(text).get("tool") or {}
    except ValueError:
        return None
    if any(tool.get(key) for key in ("constraints", "overrides", "build-constraint-dependencies")):
        return None
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
            return None
        with_packages.append(requirement)
    python = tool.get("python")
    return KeptInstall(
        extras=extras,
        with_packages=tuple(with_packages),
        python=python if isinstance(python, str) and python else None,
    )


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
    if m == Method.UV_TOOL_LEGACY:
        # H3: the old probe-agent tool owns `probe`; uninstall it, install the new.
        # The packages added beside it come along (read before the uninstall).
        kept = kept_from_uv_receipt() or KeptInstall()
        if _run(["uv", "tool", "uninstall", LEGACY_DIST], _UPGRADE_TIMEOUT_S) is None:
            return CliResult(False, False, False, current, current, "`uv` not found on PATH")
        _run(uv_tool_install_command(kept, force=True, legacy=True), _UPGRADE_TIMEOUT_S)
        return _finalize(current, target, "uv")
    if m == Method.PIPX:
        # `install --force`, not `upgrade`: pipx upgrade keeps the spec the tool
        # was first installed with, and that spec must now carry `[all]`. It
        # drops `pipx inject`-ed packages, so those go back in after.
        injected = pipx_injected()
        if _run(["pipx", "install", "--force", _dist(pipx_extras())], _UPGRADE_TIMEOUT_S) is None:
            return CliResult(False, False, False, current, current, "`pipx` not found on PATH")
        if injected:
            _run(["pipx", "inject", DIST, *injected], _UPGRADE_TIMEOUT_S)
        return _finalize(current, target, "pipx")
    if m == Method.PIP:
        _run([sys.executable, "-m", "pip", "install", "-U", _dist()], _UPGRADE_TIMEOUT_S)
        return _finalize(current, target, "pip")

    # Method.UV_TOOL
    # `[all]` is restated FIRST (plan 2.11): `uv tool upgrade` re-resolves the
    # requirement the tool was first installed with, so upgrading a bare
    # receipt onto the release that drops these dependencies from core would
    # strip `probe` -- restating after that upgrade left exactly that window
    # (#2043 review). `uv tool install` REPLACES the receipt, so everything
    # else it records (`--with` packages, extras, the Python) is restated too.
    kept = kept_from_uv_receipt()
    unrecorded = ""
    if kept is not None:
        restated = _run(uv_tool_install_command(kept), _UPGRADE_TIMEOUT_S)
        if restated is None:
            return CliResult(False, False, False, current, current, "`uv` not found on PATH")
        if restated.returncode != 0:
            return CliResult(
                True, False, False, current, current,
                "could not record `probe-research[all]` in this uv tool install "
                f"(`uv tool install` exited {restated.returncode}); the CLI was not upgraded",
            )
    else:
        # A receipt this cannot restate faithfully (an editable `--with`,
        # constraints) is left alone rather than stripped -- but then `[all]`
        # is not recorded, and the release after this one needs it.
        unrecorded = (
            "; `probe-research[all]` is NOT recorded in this install's uv receipt, which "
            "has entries the wizard's Update cannot restate. Before the next release, run "
            "`uv tool install --force 'probe-research[all]'` with your own `--with` packages"
        )
    if _run(["uv", "tool", "upgrade", DIST], _UPGRADE_TIMEOUT_S) is None:
        return CliResult(False, False, False, current, current, "`uv` not found on PATH")
    res = _finalize(current, target, "uv")
    if not res.ok:
        # `uv tool upgrade` no-ops on a version-pinned install (exits 0, changes
        # nothing), and on uv's cached index when that predates the release
        # (`uv tool upgrade` takes no refresh flag): force a clean reinstall of
        # the latest from a FRESH index, then re-verify (R9).
        _run(
            uv_tool_install_command(kept or KeptInstall(), force=True, version="@latest", refresh=True),
            _UPGRADE_TIMEOUT_S,
        )
        res = _finalize(current, target, "uv")
    if unrecorded:
        res = dataclasses.replace(res, message=res.message + unrecorded)
    return res


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


#: The tap's counterpart of the plugin's "returned success but did not advance".
TAP_NOOP = (
    "`claude` returned success but the tap version did not advance "
    "(it may have run inside a Claude Code session, which no-ops)"
)
CODEX_TAP_NOOP = "the Codex reinstall returned success but the tap version did not advance"


def tap_verdict(result: PluginResult, target: str | None) -> tuple[str, bool]:
    """`(line, behind)` for the tap after an update run.

    `behind` is True only for an INSTALLED tap still older than the manifest's
    `tap.latest` once the update ran: the stale tap that capture relies on and
    that nothing reported. A missing tap is a skip, not a failure. A behind line
    carries the reason (`tap_detail`), the way the plugin's own failure does, or
    "same failure as above" when it IS the plugin's failure, printed just above.
    """
    after = result.tap_after
    if not after:
        return ("transcript tap not installed (skipped)", False)
    if target and is_newer(target, after):
        line = f"transcript tap is still {after}, behind the latest {target}"
        # A tap that failed with the plugin's own failure (a failed refresh, or
        # any Codex failure) is printed right under it: saying it twice doubled
        # the longest thing on the screen.
        detail = (
            "same failure as above" if result.tap_detail == result.message else result.tap_detail
        )
        return (f"{line}: {detail}" if detail else line, True)
    if is_newer(after, result.tap_before):
        return (f"transcript tap updated to {after}", False)
    if target:
        return (f"transcript tap already at the latest ({after})", False)
    return (f"transcript tap at {after}", False)


def tap_changed(result: PluginResult) -> bool:
    return is_newer(result.tap_after, result.tap_before)


def update_plugin(target_latest: str | None) -> PluginResult:
    """Update the Claude Code plugin via `claude`, then VERIFY it actually advanced (H1).

    The child is spawned with no TTY and captured output (H2) so a raw-mode TUI
    crash writes to a pipe, never the parent terminal. A zero exit is NOT trusted;
    we confirm by re-reading the installed plugin version.
    """
    claude = shutil.which("claude")
    if not claude:
        return PluginResult(
            False, False, False, None, None, "`claude` not found on PATH (skipping plugin update)"
        )

    before = installed_plugin_version()
    tap_before = installed_tap_version()
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


def _codex_plugin_versions(_codex: str | None = None) -> dict[str, str]:
    result = plugin_cli.list_plugins(plugin_cli.CODEX)
    if not result.ok:
        return {}
    try:
        body = json.loads(result.detail)
    except ValueError:
        return {}
    if not isinstance(body, dict):
        return {}
    return {
        row["name"]: row["version"]
        for row in body.get("installed") or []
        if isinstance(row, dict)
        and isinstance(row.get("name"), str)
        and isinstance(row.get("version"), str)
    }


def update_codex_plugins() -> PluginResult:
    """Refresh and re-add both Codex plugins, then verify the installed list.

    Codex has no separate ``plugin update`` command. Re-adding an installed
    plugin is its idempotent reinstall path and moves it to the refreshed
    marketplace snapshot without first removing the working copy.
    """
    codex = shutil.which("codex")
    if not codex:
        return PluginResult(
            False, False, False, None, None, "`codex` not found on PATH (skipping plugin update)"
        )
    names = (tracking_plugin_name("codex"), "probe-research-tap")
    before_versions = _codex_plugin_versions(codex)
    failed_run = None
    result = plugin_cli.refresh_marketplace(plugin_cli.CODEX, MARKETPLACE)
    if not result.ok:
        failed_run = result
    for name in names:
        if failed_run is not None:
            break
        result = plugin_cli.install(plugin_cli.CODEX, f"{name}@{MARKETPLACE}")
        if not result.ok:
            failed_run = result
    failure = _failed(failed_run) if failed_run is not None else ""
    after_versions = _codex_plugin_versions(codex)
    missing = [name for name in names if not after_versions.get(name)]
    confirmed = not failure and not missing
    changed = confirmed and any(
        before_versions.get(name) != after_versions.get(name) for name in names
    )
    before = (
        ", ".join(f"{name}={version}" for name, version in sorted(before_versions.items())) or None
    )
    after = ", ".join(f"{name}={after_versions.get(name)}" for name in names) if confirmed else None
    tap_before = before_versions.get("probe-research-tap")
    tap_after = after_versions.get("probe-research-tap")
    tap = {
        "tap_before": tap_before,
        "tap_after": tap_after,
        "tap_detail": failure
        or ("" if is_newer(tap_after, tap_before) else CODEX_TAP_NOOP),
        "git_blocked": failed_run is not None and bool(git_blocker(failed_run.detail)),
    }
    if confirmed:
        message = f"Codex plugins {'updated' if changed else 'verified'} ({after})"
        return PluginResult(True, True, changed, before, after, message, **tap)
    return PluginResult(
        True,
        False,
        False,
        before,
        after,
        # Not "does not show": `_codex_plugin_versions` returns nothing when the
        # list itself failed, so this cannot tell missing from unreadable.
        failure
        or f"could not confirm {' or '.join(missing)} in `codex plugin list --json` after reinstalling",
        **tap,
    )


def update_kimi_plugins() -> PluginResult:
    """Re-copy every Probe plugin Kimi Code has installed (Kimi has no update
    command; `kimi_config.install_plugin` replaces the copy in place), then
    verify the versions from the copies themselves."""
    from probe.cli import kimi_config

    if not kimi_config.binary_available():
        return PluginResult(
            False, False, False, None, None, "`kimi` not found on PATH (skipping plugin update)"
        )
    listed = plugin_cli.list_plugins(plugin_cli.KIMI)
    if not listed.ok:
        return PluginResult(True, False, False, None, None, listed.detail)
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
