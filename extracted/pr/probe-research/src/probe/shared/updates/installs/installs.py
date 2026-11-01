"""Side-by-side installs of the CLI's uv tool environment, and the switch between them (plan D6, D5). Details: DESIGN.md."""

from __future__ import annotations

import contextlib
import os
import shutil
import subprocess
import time
from pathlib import Path

from .. import handoff, uninstall_barrier
#: How long an install or a switch waits for another live update's install lock.
LOCK_WAIT_S = handoff.LOCK_WAIT_S


def refuse_while_uninstalling() -> None:
    """Raise `uninstall_barrier.UninstallRunning` (a RuntimeError) while an
    uninstall's barrier is LIVE: no install or switch starts under it."""
    uninstall_barrier.check()


# -- installing ------------------------------------------------------------------


#: What uv reads as true in a boolean variable (any case).
_UV_TRUE = frozenset({"1", "true", "yes", "on", "t", "y"})


def uv_offline(env: dict | None = None) -> bool:
    """Does uv run offline (`UV_OFFLINE` set to any value uv reads as true)?
    uv refuses every refresh then."""
    value = (env if env is not None else os.environ).get("UV_OFFLINE", "")
    return value.strip().lower() in _UV_TRUE


def install_command(spec: str, *, with_packages: tuple = (), python: str | None = None) -> list[str]:
    # A fresh read of the index for probe-research (uv's cache can predate the
    # release) -- unless uv is offline, which refuses any refresh outright.
    refresh = [] if uv_offline() else ["--refresh-package", DIST]
    command = ["uv", "tool", "install", *refresh, spec]
    for requirement in with_packages:
        command += ["--with", requirement]
    if python:
        command += ["--python", python]
    return command


def install(
    version: str,
    spec: str,
    *,
    with_packages: tuple = (),
    python: str | None = None,
    tools: Path | None = None,
    timeout: float = 300.0,
    run=subprocess.run,
    rebuild: bool = False,
) -> Path:
    """Install `spec` (`probe-research[...]==<version>`) as its own env,
    `probe-versions/<version>/probe-research`, beside the active one. A
    complete env of that version already there is reused, unless `rebuild`
    (it is broken: `health`). A folder in use (`protected`) is never removed
    for it: the install goes in the next generation's folder
    (`<version>+g<N>`). Returns the env; raises RuntimeError (with what uv
    said) when it does not end up holding `version`. Under the install lock
    (raises `handoff.LockBusy`, a RuntimeError, when another live update keeps
    it); never while an uninstall runs (`refuse_while_uninstalling`)."""
    tools = tools or tool_dir()
    refuse_while_uninstalling()
    with handoff.install_lock(versions_root(tools), wait_s=LOCK_WAIT_S):
        refuse_while_uninstalling()  # written while this waited for the lock
        return _install(version, spec, with_packages=with_packages, python=python, tools=tools,
                        timeout=timeout, run=run, rebuild=rebuild)


def protected(folder: Path, tools: Path | None = None, *, commands: list[str] | None = None) -> bool:
    """Must `folder` (a version folder) stay as it is: the active env's, the
    one to switch back to, the record's interrupted migration, or one a
    process runs from? Unknown reads as yes."""
    try:
        resolved = folder.resolve()
    except OSError:
        return True
    keep = set()
    for env in (active(tools), previous(tools)):
        if env is not None:
            with contextlib.suppress(OSError):
                keep.add(env.parent.resolve())
    moving = record(tools).get("migrating")
    if isinstance(moving, dict) and isinstance(moving.get("to"), str):
        with contextlib.suppress(OSError):
            keep.add(Path(moving["to"]).parent.resolve())
    return resolved in keep or _in_use(folder, commands)


def _target(version: str, tools: Path, rebuild: bool) -> Path:
    """Where `install` puts `version`: its own folder, unless that is in use
    and incomplete (or to be rebuilt): then the next generation's."""
    env = version_env(version, tools)
    if not env.parent.exists():
        return env
    if not rebuild and handoff.complete(env, version):
        return env
    if protected(env.parent, tools):
        return generation_env(version, next_generation(version, tools), tools)
    return env


def _install(version: str, spec: str, *, with_packages: tuple, python: str | None, tools: Path,
             timeout: float, run, rebuild: bool = False) -> Path:
    env = _target(version, tools, rebuild)
    if not rebuild and handoff.complete(env, version):
        return env
    holder = env.parent
    if holder.exists():
        shutil.rmtree(holder, ignore_errors=True)  # a half-finished earlier try, or a broken one not in use
    holder.mkdir(parents=True, exist_ok=True)
    child_env = {
        **os.environ,
        "UV_TOOL_DIR": str(holder),
        # Its scripts go nowhere anyone runs them from: `~/.local/bin/probe`
        # keeps naming the tool path, which the switch points here.
        "UV_TOOL_BIN_DIR": str(holder / ".bin"),
    }
    done = run(
        install_command(spec, with_packages=with_packages, python=python),
        env=child_env,
        capture_output=True,
        text=True,
        timeout=timeout,
        check=False,
    )
    # Only an install uv says worked (exit 0) and finished (`handoff.complete`:
    # its receipt, written last, is there) counts, as for the hand-off's own.
    if done.returncode == 0 and handoff.complete(env, version):
        return env
    got = env_version(env)
    if got is None and env_python(env).exists():
        got = env_version(env, timeout=120.0)  # a loaded machine, not a failed install
    if done.returncode == 0 and got == version and (env / RECEIPT).is_file():
        return env
    said = ((done.stderr or "") + (done.stdout or "")).strip()[-1500:]
    unfinished = "" if got is None or (env / RECEIPT).is_file() else " (no uv receipt: unfinished)"
    shutil.rmtree(holder, ignore_errors=True)
    raise RuntimeError(
        f"`uv tool install {spec}` exited {done.returncode} and left {got or 'nothing'}{unfinished}: {said}")


def activate(target: Path, *, tools: Path | None = None) -> dict:
    """Point the tool path at `target` (a version env) in one rename. Returns
    the record: `{"active", "previous", "switched_at"}` (paths as strings).
    The first switch also moves the folder uv made (`_migrate`); a failure
    after that puts it back, so the CLI is never left without a tool path.
    Under the install lock (re-entrant: a hand-off's exec'd release holds it
    already); `handoff.LockBusy` (a RuntimeError) when another update keeps it;
    `uninstall_barrier.UninstallRunning` (a RuntimeError) while an uninstall
    runs: no switch, not even back (the guard's), starts under it."""
    tools = tools or tool_dir()
    refuse_while_uninstalling()
    with handoff.install_lock(versions_root(tools), wait_s=LOCK_WAIT_S):
        refuse_while_uninstalling()  # written while this waited for the lock
        return _activate(target, tools)


def _activate(target: Path, tools: Path) -> dict:
    env = tool_env(tools)
    if not env_python(target).exists():
        raise RuntimeError(f"{target} is not a complete environment")
    recover(tools)
    bins = bin_dir(tools)
    fix_receipt(target, bins)
    before = active(tools)
    # The link first: nothing has moved if it cannot be made.
    link = tools / f".{DIST}.switch-{os.getpid()}"
    with contextlib.suppress(FileNotFoundError, OSError):
        _drop_link(link)
    _make_link(target, link)
    try:
        migrated = _migrate(tools)
    except OSError:
        with contextlib.suppress(OSError):
            _drop_link(link)
        recover(tools)
        raise
    previous = before or migrated
    try:
        _swap_link(link, env)
    except OSError:
        with contextlib.suppress(OSError):
            _drop_link(link)
        recover(tools)
        raise
    data = record(tools)
    data.pop("migrating", None)
    data["bin"] = str(bins)
    data.update(
        {
            "active": str(target),
            "previous": str(previous) if previous is not None and not _same(Path(previous), target)
            else data.get("previous"),
            "switched_at": time.time(),
            # Where the tool path is, for a process running from a version env
            # that must not ask `uv tool dir` on every start.
            "tools": str(tools),
        }
    )
    _write_record(data, tools)
    return data


def _same(a: Path, b: Path) -> bool:
    try:
        return a.resolve() == b.resolve()
    except OSError:
        return a == b


def previous(tools: Path | None = None) -> Path | None:
    """The version to switch back to, if it is still complete."""
    prior = record(tools).get("previous")
    if not isinstance(prior, str):
        return None
    path = Path(prior)
    return path if env_python(path).exists() else None


def switch_back(tools: Path | None = None) -> dict | None:
    """Back to the previous version (D5). None when there is none to go to."""
    prior = previous(tools)
    if prior is None:
        return None
    return activate(prior, tools=tools)
from probe.shared.updates.installs.active_record import _write_record, active, record  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.shared.updates.installs.env_checks import env_version  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.shared.updates.installs.layout import (  # noqa: E402 -- pieces need each other; the front door loads this one first
    DIST,
    generation_env,
    next_generation,
    tool_dir,
    tool_env,
    version_env,
    versions_root,
)
from probe.shared.updates.installs.link import _drop_link, _make_link, _swap_link, env_python  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.shared.updates.installs.pruning import _in_use  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.shared.updates.installs.repair import _migrate, recover  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.shared.updates.installs.shims import RECEIPT, bin_dir, fix_receipt  # noqa: E402 -- pieces need each other; the front door loads this one first
