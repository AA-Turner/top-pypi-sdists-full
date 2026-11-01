"""the first switch from uv's own folder and repairing the layout after a crash or reinstall."""

from __future__ import annotations
import os
import shutil
import time
from pathlib import Path

from .. import handoff


# -- switching -------------------------------------------------------------------


def needs_migration(tools: Path | None = None) -> bool:
    """Is the tool path still the folder uv made (no switch has happened)?
    The first switch moves it, and every process started from it reads its
    files through that path, so it is made only on a quiet machine (the
    in-place update's own checks); every later switch is a link."""
    env = tool_env(tools)
    return env.is_dir() and not is_link(env)


def _migrate(tools: Path) -> Path | None:
    """The first switch: move the folder uv made at the tool path into
    `probe-versions/<its version>/` so it is a version to switch back to.
    Returns where it went, or None when there was nothing to move. Recorded
    first (`migrating`), so a switch cut short is put back (`recover`)."""
    env = tool_env(tools)
    if is_link(env) or not env.is_dir():
        return None
    version = env_version(env) or f"unknown-{int(time.time())}"
    dest = version_env(version, tools) if _VERSION.match(version) else versions_root(tools) / version / DIST
    if dest.exists() or dest.parent.exists():
        # That version's folder is there already (a `uv tool install` over the
        # link, or after `uv tool uninstall`, made uv's folder again): the next
        # generation's, never a name that reads as another version.
        dest = (generation_env(version, next_generation(version, tools), tools) if _VERSION.match(version)
                else versions_root(tools) / f"{version}-{int(time.time())}" / DIST)
    dest.parent.mkdir(parents=True, exist_ok=True)
    data = record(tools)
    data["migrating"] = {"from": str(env), "to": str(dest), "at": time.time()}
    _write_record(data, tools)
    os.rename(env, dest)
    return dest


def recover(tools: Path | None = None) -> bool:
    """A first switch cut short between moving the folder and linking the
    tool path (a crash, a full disk): move the folder back. True when it did.
    Never raises."""
    tools = tools or tool_dir()
    try:
        data = record(tools)
        moving = data.get("migrating")
        if not isinstance(moving, dict):
            return False
        env, dest = Path(str(moving.get("from"))), Path(str(moving.get("to")))
        done = False
        if not env.exists() and not is_link(env) and dest.is_dir():
            os.rename(dest, env)
            done = True
        data.pop("migrating", None)
        _write_record(data, tools)
        return done
    except OSError:
        return False


# -- repairing the layout (plan clean-uninstall-reinstall R-T1, R-T2) -------------


class ToolPath:
    """What is at the tool path (`<uv tool dir>/probe-research`)."""

    #: Nothing: a fresh machine, or `uv tool uninstall` took the link away
    #: (it removes the link and the shims; the versions stay).
    MISSING = "missing"
    #: uv's own folder: no switch yet, or `uv tool install --force` (or a
    #: reinstall after `uv tool uninstall`) made it again over the layout.
    PLAIN = "plain"
    #: Our link, to an env with an interpreter.
    LINKED = "linked"
    #: Our link, to nothing usable (its env deleted).
    DANGLING = "dangling"
    #: A file, or something else that is not a folder.
    OTHER = "other"


def adopt_plain(tools: Path | None = None) -> Path | None:
    """The first switch to the env uv made itself (a reinstall by hand over the
    layout, or a machine that never switched): move it into the versions
    folder (`_migrate`: the next generation when its version's folder is
    taken) and link the tool path to it. The moved env, or None when the tool
    path is no plain folder. Under the install lock; a failure puts it back."""
    tools = tools or tool_dir()
    refuse_while_uninstalling()
    with handoff.install_lock(versions_root(tools), wait_s=LOCK_WAIT_S):
        if tool_state(tools) != ToolPath.PLAIN:
            return None
        env = tool_env(tools)
        moved = _migrate(tools)
        if moved is None:
            return None
        try:
            _make_link(moved, env)
        except OSError:
            recover(tools)
            raise
        bins = bin_dir(tools)
        fix_receipt(moved, bins)
        data = record(tools)
        data.pop("migrating", None)
        data.update({"active": str(moved), "switched_at": time.time(), "tools": str(tools), "bin": str(bins)})
        if isinstance(data.get("previous"), str) and _same(Path(data["previous"]), moved):
            data.pop("previous", None)
        _write_record(data, tools)
        return moved


def tool_state(tools: Path | None = None) -> str:
    env = tool_env(tools)
    if is_link(env):
        try:
            target = env.resolve(strict=True)
        except OSError:
            return ToolPath.DANGLING
        return ToolPath.LINKED if env_python(target).exists() else ToolPath.DANGLING
    if env.is_dir():
        return ToolPath.PLAIN
    if env.exists():
        return ToolPath.OTHER
    return ToolPath.MISSING


def fix_record(tools: Path | None = None) -> list[str]:
    """Make `active.json` say what is (R-T2): `active` the env the tool path
    names now (none while it names none), `previous` only an env with an
    interpreter that is not the active one, `tools` this folder. Returns what
    it changed, one line each. Never raises."""
    tools = tools or tool_dir()
    try:
        data = record(tools)
        if not data:
            return []
        said = []
        now = active(tools)
        recorded = data.get("active")
        if now is not None and (not isinstance(recorded, str) or not _same(Path(recorded), now)):
            said.append(f"active.json named {recorded or 'nothing'} as the active version; the tool path names {now}")
            data["active"] = str(now)
        elif now is None and recorded is not None:
            said.append(f"active.json named {recorded} as the active version; the tool path names no version env")
            data.pop("active", None)
        prior = data.get("previous")
        if isinstance(prior, str) and (not env_python(Path(prior)).exists()
                                       or (now is not None and _same(Path(prior), now))):
            said.append(f"active.json named {prior} to switch back to; it is gone or the active one")
            data.pop("previous", None)
        if data.get("tools") != str(tools) and now is not None:
            data["tools"] = str(tools)
            said.append(f"active.json's tool folder is {tools} now")
        if said:
            _write_record(data, tools)
        return said
    except OSError:
        return []


def cleanup(tools: Path | None = None, *, now: float | None = None) -> list[Path]:
    """After a switch (R-T2): delete what a crash or an older release left in
    the versions folder that nothing uses -- migration leftovers
    (`<version>-<unix time>`) and unfinished installs (no interpreter or no
    uv receipt) -- never the active, the previous, an interrupted
    migration's or one a process here or on another machine runs from
    (`protected`, the marks of `prune`); then `prune`. Under the install lock
    (an unfinished install is no other installer's then). Returns what was
    deleted. Never raises."""
    tools = tools or tool_dir()
    now = time.time() if now is None else now
    removed: list[Path] = []
    try:
        with handoff.install_lock(versions_root(tools), wait_s=LOCK_WAIT_S):
            commands = _commands()
            for folder in _folders(tools):
                _version, _generation, leftover = folder_parts(folder.name)
                env = folder / DIST
                unfinished = not env_python(env).exists() or not (env / RECEIPT).is_file()
                if not (leftover or unfinished):
                    continue
                if protected(folder, tools, commands=commands) or _used_elsewhere(folder, now):
                    continue
                shutil.rmtree(folder, ignore_errors=True)
                if not folder.exists():
                    removed.append(folder)
            removed += prune(tools, now=now)
    except (OSError, RuntimeError):
        pass
    return removed
from probe.shared.updates.installs.active_record import _write_record, active, record  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.shared.updates.installs.env_checks import env_version  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.shared.updates.installs.installs import LOCK_WAIT_S, _same, protected, refuse_while_uninstalling  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.shared.updates.installs.layout import (  # noqa: E402 -- pieces need each other; the front door loads this one first
    DIST,
    _VERSION,
    _folders,
    folder_parts,
    generation_env,
    next_generation,
    tool_dir,
    tool_env,
    version_env,
    versions_root,
)
from probe.shared.updates.installs.link import _make_link, env_python, is_link  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.shared.updates.installs.pruning import _commands, _used_elsewhere, prune  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.shared.updates.installs.shims import RECEIPT, bin_dir, fix_receipt  # noqa: E402 -- pieces need each other; the front door loads this one first
