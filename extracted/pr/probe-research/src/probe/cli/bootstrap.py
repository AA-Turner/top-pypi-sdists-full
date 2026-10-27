"""Make sure the wizard leaves a real `probe` behind.

`npx probe-research` resolves the CLI through `uv tool run` / `pipx run`, both
of which are EPHEMERAL: they fetch, execute, and leave nothing installed. That
is the right way to *launch* a wizard and completely wrong as an end state,
because everything the wizard sets up depends on a persistent binary afterwards:

  * the wizard's own closing line tells you to run `probe doctor`
  * the tracking plugin's SessionStart hook resolves PROBE_BIN from PATH or
    ~/.local/bin to do its version check
  * the MCP config's headersHelper shells out to fetch the stored token, so
    with no binary the MCP has no credential

Without this the only path that worked end to end was the one where `probe` was
already installed — the re-run case, not onboarding. Exactly backwards.

So: if we are running ephemerally, install ourselves properly before doing
anything else, and say so.
"""

from __future__ import annotations

import os
import re
import shutil
import subprocess
from dataclasses import dataclass
from pathlib import Path

DIST = "probe-research"
#: What an install ASKS for (plan 2.11, D29): the package with the `all` extra,
#: which carries the CLI's and the MCP server's dependencies. They still sit in
#: core in this release; the next release removes them from core, and an
#: install recorded without `[all]` would then lose `probe` on its next upgrade.
INSTALL_SPEC = f"{DIST}[all]"
LEGACY_DIST = "probe-agent"
_INSTALL_TIMEOUT_S = 300.0


@dataclass(frozen=True)
class BootstrapResult:
    installed: bool
    """True only when THIS run performed a persistent install."""
    already_persistent: bool
    message: str
    refused: bool = False
    """Nothing was installed on purpose: an uninstall runs (its barrier is
    LIVE), or uv is missing (the message says the exact command)."""
    waiting: bool = False
    """Installed and checked beside uv's own folder, which the first switch
    moves only on a quiet machine: the `probe` on PATH is the old one until
    then. Never "already installed": nothing is checked against the old one."""


def _launcher_caches() -> tuple[str, ...]:
    """Where uv and pipx park a copy they are about to throw away.

    Read from the environment first, because both tools let the cache move and
    a hardcoded path would quietly stop matching for anyone who moved it --
    which is the same silent-wrong-answer this whole function exists to stop.
    """
    roots = [os.environ.get("UV_CACHE_DIR")]
    xdg = os.environ.get("XDG_CACHE_HOME")
    roots.append(os.path.join(xdg, "uv") if xdg else None)
    home = os.path.expanduser("~")
    roots += [
        f"{home}/.cache/uv",
        f"{home}/.cache/pipx",
        f"{home}/.local/pipx/.cache",
    ]
    pipx_home = os.environ.get("PIPX_HOME")
    if pipx_home:
        roots.append(os.path.join(pipx_home, ".cache"))
    return tuple(os.path.realpath(r) for r in roots if r)


def _is_throwaway(path: str) -> bool:
    """Whether this `probe` is a launcher's temporary copy rather than an install.

    THE BUG THIS EXISTS FOR: `npx probe-research` runs us through `uv tool run`,
    which unpacks the CLI into its cache and puts that cache's `bin` on our
    PATH. So `shutil.which("probe")` finds a `probe` on every from-zero run --
    THIS process -- and the caller concluded a real install was already present
    and skipped the one it exists to perform. Measured on a fresh machine:
    `which("probe")` returned `~/.cache/uv/archive-v0/<hash>/bin/probe`, the
    version matched, and the wizard reported success while leaving no `probe`
    behind at all. Every instruction that follows -- `probe doctor`, the
    plugin's SessionStart hook, the MCP headers helper -- then had no binary.

    Tested on the LOCATION, not on `realpath` and not on `sys.prefix`. Both of
    those look identical for a real install: `~/.local/bin/probe` is a symlink
    INTO `~/.local/share/uv/tools/probe-research`, which is also that process's
    own `sys.prefix`. Judging by either would call a healthy install throwaway
    and reinstall it on every single run.
    """
    real = os.path.realpath(path)
    return any(real.startswith(root + os.sep) for root in _launcher_caches())


def _installed_binary() -> str | None:
    """A `probe` a future shell (or a plugin hook) could actually find.

    PATH alone is not enough: Claude Code launched from the dock sources no
    profile, so ~/.local/bin may be missing from its environment even though the
    binary is there. The plugin hook checks those same fallbacks, so we must
    agree with it or we would reinstall on every run.

    PATH is also too MUCH, which is the other half: a launcher's own cache is on
    it while we run. A hit there is skipped and the durable candidates below are
    consulted instead -- so a from-zero run correctly finds nothing.
    """
    found = shutil.which("probe")
    if found and not _is_throwaway(found):
        return found
    home = os.path.expanduser("~")
    for candidate in (
        f"{home}/.local/bin/probe",
        f"{home}/.local/share/uv/tools/{DIST}/bin/probe",
    ):
        if os.path.isfile(candidate) and os.access(candidate, os.X_OK):
            return candidate
    return None


def _version_of(binary: str) -> str | None:
    try:
        completed = subprocess.run(  # noqa: S603 - resolved path, no shell
            [binary, "--version"], capture_output=True, text=True, timeout=20, check=False
        )
    except (OSError, subprocess.SubprocessError):
        return None
    if completed.returncode != 0:
        return None
    import re

    match = re.search(r"(\d+\.\d+\.\d+(?:\.\d+)?)", completed.stdout)
    return match.group(1) if match else None


def _at_least(found: str, wanted: str) -> bool:
    fa = [int(x) for x in found.split(".") if x.isdigit()]
    wa = [int(x) for x in wanted.split(".") if x.isdigit()]
    for i in range(max(len(fa), len(wa))):
        a, b = (fa[i] if i < len(fa) else 0), (wa[i] if i < len(wa) else 0)
        if a != b:
            return a > b
    return True


def _resolves_on_path() -> bool:
    """Whether a GOOD ENOUGH `probe` is installed.

    Existence is not enough. A machine with an old `probe` -- every existing
    user -- would otherwise keep it forever: the wizard runs the new version
    ephemerally through uvx, decides nothing needs installing, and the user's
    shell stays on the old one indefinitely. Same trap the npx launcher fell
    into.
    """
    from probe import __version__

    binary = _installed_binary()
    if binary is None:
        return False
    if _is_this_install(binary):
        # The persistent `probe` IS this process (the common case: someone ran
        # `probe wizard`), so its version is ours. Asking it with a subprocess
        # cost ~0.9s on every wizard launch.
        return True
    found = _version_of(binary)
    return bool(found and _at_least(found, __version__))


def _is_this_install(binary: str) -> bool:
    """Whether `binary` is the entry point of THIS interpreter's environment
    (`<env>/bin/probe`, or `<env>\\Scripts\\probe.exe`), through any symlink
    (`~/.local/bin/probe` -> the uv or pipx tool env)."""
    import sys

    try:
        return Path(os.path.realpath(binary)).parent.parent == Path(os.path.realpath(sys.prefix))
    except OSError:
        return False


def installed_version() -> str | None:
    """The version of the persistent `probe`, or None when there is none."""
    binary = _installed_binary()
    return _version_of(binary) if binary else None


def ensure_persistent_install(*, dry_run: bool = False, target: str | None = None) -> BootstrapResult:
    """Install the CLI for real if this process is an ephemeral one.

    Through the one installer (`install_pipeline.install_cli`: side by side,
    under the install lock, checked before the switch), with uv. A pipx
    install moves to uv's (the managed install); without uv it refuses with
    the exact command. Deliberately never a bare `pip install`: on a
    researcher's machine that usually means a conda or system environment,
    and silently mutating it is how you break a training run three days
    later. Never while an uninstall runs (its barrier is LIVE).
    """
    from . import install_pipeline

    said = install_pipeline.refusal()
    if said:
        return BootstrapResult(installed=False, already_persistent=False, message=f"! {said}", refused=True)
    foreign = None if dry_run else _foreign_to_move()
    if foreign is None and _resolves_on_path():
        note = "" if dry_run else _repair_layout()
        return BootstrapResult(
            installed=False,
            already_persistent=True,
            message=note,
        )

    if dry_run:
        return BootstrapResult(
            installed=False,
            already_persistent=False,
            message=f"would install {DIST} persistently",
        )
    from probe import __version__

    behind = installed_version()
    if behind is None:
        return install_persistent()
    # `target`: the newest version the caller knows of (`probe update` passes
    # the manifest's), so a stale throwaway copy never pins the install to
    # itself when a newer one exists.
    want = target if target and _at_least(target, __version__) else __version__
    if foreign is not None and _at_least(behind, want):
        want = behind  # moving a pipx install to uv's: never a downgrade
    # An installed copy THIS run is newer than: `npx probe-research` runs the
    # latest CLI in a throwaway environment exactly when the installed one is
    # behind. Bring it to this version, read from a fresh index. Unpinned, uv
    # satisfied the reinstall from its cache with the very version it replaced:
    # a 0.206.0 wizard left 0.205.4 installed (2026-10-02), so every agent kept
    # calling the old CLI -- pi never saw the daemon its wizard had just set.
    result = install_persistent(f"{INSTALL_SPEC}=={want}")
    if result.waiting:
        return result  # the old `probe` answers until the switch: nothing to compare yet, nothing to move
    if result.installed and foreign is not None:
        from . import install_pipeline

        moved = install_pipeline.migrate_foreign(foreign)
        result = BootstrapResult(result.installed, result.already_persistent,
                                 " ".join([result.message, *moved]).strip())
    after = installed_version()
    if result.installed and not (after and _at_least(after, want)):
        return BootstrapResult(
            installed=False,
            already_persistent=False,
            message=(
                f"! the installed `probe` is still {after or behind} after installing {want}, "
                "so your coding agents keep calling the old one. "
                f"Run: {_fix_command(want)}"
            ),
        )
    if result.installed:
        return BootstrapResult(
            installed=True,
            already_persistent=False,
            message=f"Updated the installed `probe` {behind} → {after}.",
        )
    return result


def _shadowing_pip() -> tuple[str, str | None] | None:
    """A pip install's `probe` that comes first on PATH, ahead of uv's: `(its
    path, the Python that owns it)` -- that Python from the script's own `#!`
    line, None when it cannot be read. Probe never runs the uninstall: that
    env may be a project's, and the SDK lives there. None when there is none."""
    from . import install_pipeline

    try:
        found = shutil.which("probe")
        if not found or _is_throwaway(found):
            return None
        method = install_pipeline.foreign_install()
        if method is None or method[0] != "pip" or os.path.realpath(method[1]) != os.path.realpath(found):
            return None
        return found, _script_python(found)
    except Exception:  # noqa: BLE001
        return None


#: pip's launcher for an interpreter path a `#!` line cannot hold (a space, too
#: long): `#!/bin/sh`, then this line naming the Python.
_SH_EXEC = re.compile(r"""^'''exec' (?:"([^"]+)"|(\S+)) "\$0" "\$@"$""")


def _script_python(script: str) -> str | None:
    """The Python a pip-installed console script runs: its `#!` line, or the
    exec line of pip's `/bin/sh` launcher. None when the script cannot be
    read or names no Python by its path (`#!/usr/bin/env python3` runs
    whichever comes first on PATH)."""
    try:
        with open(script, "rb") as handle:
            head = handle.read(4096).decode("utf-8", "replace").splitlines()
    except OSError:
        return None
    if not head or not head[0].startswith("#!"):
        return None
    line = head[0][2:].strip()
    quoted = re.match(r'"([^"]+)"', line)
    python = quoted.group(1) if quoted else (line.split() or [""])[0]
    if os.path.basename(python) == "sh":
        launcher = _SH_EXEC.match(head[1].strip()) if len(head) > 1 else None
        python = (launcher.group(1) or launcher.group(2)) if launcher else ""
    if not os.path.isabs(python) or not os.path.basename(python).lower().startswith(("python", "pypy")):
        return None
    return python


def _fix_command(version: str) -> str:
    """What a person runs when the install did not take: `probe repair` where
    the side-by-side layout is used (a `uv tool install --force` through its
    link replaces it with a plain folder: plan R4), else the plain install.
    When a pip install's `probe` comes first on PATH, that is the fix: its
    path and the exact uninstall for its env (which Probe never runs)."""
    from . import install_pipeline

    shadow = _shadowing_pip()
    if shadow is not None:
        path, python = shadow
        how = (f"`{python} -m pip uninstall {DIST}`" if python
               else f"`pip uninstall {DIST}` run by the Python that owns {path}")
        return (f"`{path}` (a pip install) comes first on PATH; remove it with {how} "
                "(Probe does not run that for you), or put ~/.local/bin ahead of it on PATH")
    if shutil.which("uv") is None:
        return install_pipeline.UV_INSTALL + "; then npx probe-research repair"
    try:
        from probe._shared import installs

        if install_pipeline.layout_usable(installs.tool_dir()):
            return "npx probe-research repair"
    except Exception:  # noqa: BLE001
        pass
    return f"uv tool install --force '{INSTALL_SPEC}=={version}'"


def _foreign_to_move() -> tuple[str, str] | None:
    """A pipx install of the CLI, which the managed (uv) install replaces
    (plan R-T1); a pip install only when this run is a throwaway one (`npx`):
    run from a pip environment, that environment is the person's own choice
    (a project's, the SDK's), and stays. None when there is nothing to move."""
    from . import install_pipeline, updater

    try:
        found = install_pipeline.foreign_install()
    except Exception:  # noqa: BLE001
        return None
    if found is None:
        return None
    if found[0] == "pip" and updater.detect_install().method != updater.Method.EPHEMERAL:
        return None
    return found


def _repair_layout() -> str:
    """The cheap part of a same-version check, on every run that finds the
    install current (no process started): the public scripts, `active.json`,
    a stale uninstall barrier. A line for what it put right, else ""."""
    from . import install_pipeline

    try:
        from probe._shared import handoff, installs

        lines = []
        tools = installs.tool_dir()
        if os.name == "nt" or installs.tool_state(tools) not in (installs.ToolPath.LINKED, installs.ToolPath.PLAIN):
            cleared = install_pipeline.clear_stale_barrier(tools)
            return cleared or ""
        if not installs.versions_root(tools).is_dir():
            return ""
        with handoff.install_lock(installs.versions_root(tools), wait_s=0):
            from probe._shared import uninstall_barrier

            cleared = uninstall_barrier.clear_stale()  # under the lock: no uninstall runs now
            if cleared:
                lines.append(cleared)
            if uninstall_barrier.live():
                return " ".join(lines)
            lines.extend(installs.fix_record(tools))
            made, _blocked = installs.ensure_shims(tools)
            if made:
                lines.append("put the `probe` command back: " + "; ".join(made))
        return " ".join(lines)
    except Exception:  # noqa: BLE001 -- busy (another update holds the lock), or unreadable: next time
        return ""


def verify_installed() -> BootstrapResult | None:
    """A same-version reinstall (the wizard's install over a current CLI): a
    health check of the active env -- its receipt, its update path's import,
    the service's start -- and of the layout, repairing what fails (plan
    clean-uninstall-reinstall R-T3: a broken active env is rebuilt in a new
    generation folder and switched to). None where the side-by-side layout is
    not used here, or nothing is installed through it."""
    if os.name == "nt" or shutil.which("uv") is None:
        return None
    from probe import __version__

    from . import install_pipeline

    try:
        from probe._shared import installs

        tools = installs.tool_dir()
        state = installs.tool_state(tools)
        if state not in (installs.ToolPath.LINKED, installs.ToolPath.PLAIN, installs.ToolPath.DANGLING):
            return None
        env = installs.active(tools) or (installs.tool_env(tools) if state == installs.ToolPath.PLAIN else None)
        version = (installs.env_version(env) if env is not None else None) or __version__
    except Exception:  # noqa: BLE001
        return None
    if not install_pipeline.checkable(version):
        return None  # too old for the check (it imports `probe.core.adopt`): the update brings it forward
    # Never waits for another update's lock: one running is checked next time.
    out = install_pipeline.install_cli(version, mode=install_pipeline.Mode.INSTALL, lock_wait_s=0)
    if out.unmanaged:
        return None
    if out.refused:
        return BootstrapResult(False, False, f"! {out.refused}", refused=True)
    if out.busy:
        return BootstrapResult(False, True, out.busy)
    if out.waiting and not out.ok:
        return BootstrapResult(False, True, f"Repaired `probe` {version}: {install_pipeline.QUIET_SWITCH} "
                               f"({out.waiting})", waiting=True)
    if not out.ok:
        return BootstrapResult(False, False, "could not repair the installed `probe`: " + "; ".join(
            out.problems or ["it did not end up working"]))
    # The rest of a same-version check (R-T3): the OS keeper and lifeboat,
    # runtime.json, and a service still on the env the switch replaced.
    from . import repair

    keeper = repair.repair_keeper(out)
    service = repair.repair_service(out) if out.changed else repair.Part()
    news = [line for line in keeper.lines if not line.endswith(": current")]
    said = "; ".join([*out.lines, *([out.waiting] if out.waiting else []), *news, *service.lines,
                      *(f"! {line}" for line in [*keeper.problems, *service.problems])])
    if out.changed:
        return BootstrapResult(True, False, f"Repaired the installed `probe` {out.version}: {said}")
    return BootstrapResult(False, True, said)


def _latest_release() -> str | None:
    """The newest CLI the release manifest names, or None (offline, no route)."""
    try:
        from probe import version_policy

        from . import updater

        return updater.cli_latest(updater.fetch_latest(version_policy.base_url()))
    except Exception:  # noqa: BLE001
        return None


def _install_managed(version: str) -> BootstrapResult | None:
    """`install_pipeline.install_cli` for `version` (`==X`, `@latest` or ""
    for this run's own), as a BootstrapResult. None where the side-by-side
    layout is not used (Windows, the versions folder on another filesystem)
    and no link is at the tool path: the caller installs as before. Without
    uv: refused, with the exact command (plan R-T1)."""
    from probe import __version__

    from . import install_pipeline

    if os.name == "nt":
        return None
    wanted = version[2:] if version.startswith("==") else __version__ if not version else None
    if shutil.which("uv") is None:
        return BootstrapResult(False, False, f"! could not install `probe`: {install_pipeline.no_uv_message(wanted)}",
                               refused=True)
    try:
        from probe._shared import installs

        tools = installs.tool_dir()
        usable = install_pipeline.layout_usable(tools)
        linked = installs.is_link(installs.tool_env(tools))
    except Exception:  # noqa: BLE001 -- unknown: as before
        return None
    if not usable:
        return None
    if wanted is None:
        if not linked:
            return None  # `@latest` over uv's own folder (or none): no link for `uv tool install` to write through
        wanted = _latest_release()
        if wanted is None:
            return BootstrapResult(False, False, "could not install `probe`: the newest release could not be "
                                   "read (offline?); run `npx probe-research repair` once you are online")
    out = install_pipeline.install_cli(wanted, mode=install_pipeline.Mode.INSTALL)
    if out.refused:
        return BootstrapResult(False, False, f"! could not install `probe`: {out.refused}", refused=True)
    if out.unmanaged:
        return None
    if out.busy:
        return BootstrapResult(False, False, f"`probe` {wanted} was not installed now: {out.busy}")
    if out.waiting and not out.ok:
        # Installed, never "already installed": configure would check the old
        # `probe` as if nothing happened, and say nothing of the switch.
        return BootstrapResult(True, False, f"`probe` {wanted} is {install_pipeline.QUIET_SWITCH} ({out.waiting})",
                               waiting=True)
    if not out.ok:
        reasons = "; ".join(out.problems) or "it did not end up working"
        return BootstrapResult(False, False, f"could not install `probe` {wanted}: {reasons}")
    note = "" if shutil.which("probe") else " Add ~/.local/bin to your PATH to use it in this shell."
    if out.waiting:
        note += f" ({out.waiting})"
    if not out.changed:
        return BootstrapResult(False, True, "; ".join(out.lines) + note if out.lines else note.strip())
    return BootstrapResult(True, False, f"Installed `probe` {out.version} (uv, beside any running one).{note}")


def installs_offline() -> bool:
    """uv runs offline (`UV_OFFLINE`, any value uv reads as true)."""
    from probe._shared import installs

    return installs.uv_offline()


def _persistent_tool_env(command: list[str], name: str) -> str | None:
    """The directory of the persistent install ``name`` under a tool manager,
    from the manager itself (`uv tool dir`, `pipx environment`), or None."""
    try:
        done = subprocess.run(  # noqa: S603 - fixed binary, no shell
            command, capture_output=True, text=True, check=False, timeout=30
        )
    except (OSError, subprocess.SubprocessError):
        return None
    root = (done.stdout or "").strip().splitlines()
    if done.returncode != 0 or not root:
        return None
    path = os.path.join(root[-1].strip(), name)
    return path if os.path.isdir(path) else None


def install_persistent(spec: str = INSTALL_SPEC) -> BootstrapResult:
    """Install `spec` as the persistent CLI, replacing whatever is there.

    `spec` is `probe-research[all]@latest` (or `==<version>`) when an existing
    install is known to be behind: a launcher that served a stale cached copy
    would otherwise resolve the same stale version here too. Either suffix also
    re-reads the index for probe-research.
    """
    version = "@latest" if spec.endswith("@latest") else (
        "==" + spec.split("==", 1)[1] if "==" in spec else ""
    )
    managed = _install_managed(version)
    if managed is not None:
        return managed
    injected: list[str] = []
    dropped = ""
    if shutil.which("uv"):
        # The legacy distribution owns the same `probe` executable, so it has to
        # go FIRST or the old build keeps answering. Removing it afterwards
        # deletes the shared binary out from under the new install.
        subprocess.run(  # noqa: S603 - fixed binary, no shell
            ["uv", "tool", "uninstall", LEGACY_DIST],
            capture_output=True,
            check=False,
            timeout=_INSTALL_TIMEOUT_S,
        )
        # `--force` replaces the permanent install's receipt: restate what it
        # records -- extras, `--with` packages, its Python -- or an update run
        # from `npx`/`uvx` strips them (#2043 review: `--with six` gone, Python
        # 3.10 became 3.13). The same restatement `probe update` makes.
        from . import updater

        existing = _persistent_tool_env(["uv", "tool", "dir"], DIST)
        kept = updater.faithful_kept_from_uv_receipt(existing) if existing else updater.KeptInstall()
        if kept is None:
            # Unlike `probe update`, which leaves such a receipt alone, this is
            # a (re)install: it goes ahead -- but says what it could not carry.
            dropped = (
                " The previous install's uv receipt had entries this cannot restate (an "
                "editable or local `--with` package, constraints); they were NOT carried over. "
                f"Re-add them with `uv tool install '{updater._dist()}' --with ...`."
            )
        # A pinned or @latest reinstall re-reads the index (uv's cached copy can
        # predate the release) -- unless uv is offline, which refuses a refresh.
        # `--force` only to take `probe` over from a first install: over an
        # existing tool environment a plain install upgrades it in place, while
        # `--force` deletes and rebuilds it under every running `probe`.
        command = updater.uv_tool_install_command(
            kept or updater.KeptInstall(),
            force=existing is None,
            version=version,
            refresh=bool(version) and not installs_offline(),
        )
    elif shutil.which("pipx") and os.name == "nt":
        # pipx has no `@latest`; a plain install already resolves the newest.
        # Windows only: elsewhere a machine without uv is refused with the
        # command (`_install_managed`), and a pipx install moves to uv's.
        # Its recorded extras stay in the spec; injected packages go back in
        # after (`install --force` drops them).
        from . import updater

        existing = _persistent_tool_env(["pipx", "environment", "--value", "PIPX_LOCAL_VENVS"], DIST)
        extras = updater.pipx_extras(existing) if existing else ()
        injected = updater.pipx_injected(existing) if existing else []
        pinned = version if version.startswith("==") else ""
        command = ["pipx", "install", "--force", updater._dist(extras) + pinned]
    else:
        return BootstrapResult(
            installed=False,
            already_persistent=False,
            message=(
                "could not install `probe` persistently: neither uv nor pipx is "
                "available. The wizard will still finish, but `probe doctor` and "
                "the plugin's version check will not work until you install it."
            ),
        )

    try:
        completed = subprocess.run(  # noqa: S603 - fixed binary, no shell
            command,
            capture_output=True,
            text=True,
            check=False,
            timeout=_INSTALL_TIMEOUT_S,
        )
    except (OSError, subprocess.SubprocessError) as exc:
        return BootstrapResult(False, False, f"could not install `probe`: {exc}")

    if completed.returncode != 0:
        detail = (completed.stderr or completed.stdout).strip().splitlines()
        return BootstrapResult(
            installed=False,
            already_persistent=False,
            message=f"could not install `probe`: {detail[-1] if detail else 'unknown error'}",
        )
    if command[0] == "pipx" and injected:
        subprocess.run(  # noqa: S603 - fixed binary, no shell
            ["pipx", "inject", DIST, *injected],
            capture_output=True,
            check=False,
            timeout=_INSTALL_TIMEOUT_S,
        )

    note = ""
    if not shutil.which("probe"):
        # Installed, but this shell will not see it. Saying so beats letting the
        # user discover it when `probe doctor` fails.
        note = " Add ~/.local/bin to your PATH to use it in this shell."
    return BootstrapResult(
        installed=True,
        already_persistent=False,
        message=f"Installed `probe` ({' '.join(command[:2])}).{note}{dropped}",
    )
