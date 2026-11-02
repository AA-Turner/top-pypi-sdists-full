"""CliInstallMethod protocol and its registry keyed by Method; upgrade_cli picks the method's implementation under the install lock."""

from __future__ import annotations

import contextlib
import os
import sys

from probe.shared.updates import handoff, installs
from probe.shared.updates import step as update_step
from probe.foundation.harness_registry import get_registry
from probe.sdk import session_marker
from probe.cli.install.updater.updater import DIST, Install, LEGACY_DIST, Method, detect_install

_UPGRADE_TIMEOUT_S = 300.0


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
    from probe.shared.updates import uninstall_barrier

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
#: Set by the Probe service (`probe.service.updater.settings.SIDE_BY_SIDE_ENV`) when it did
#: not wait for runs and daemon workers: the CLI is updated beside them or not at all.
REQUIRE_SIDE_BY_SIDE_ENV = update_step.SIDE_BY_SIDE_ENV
from probe.cli.install.updater.cli_installs.pipx import pipx_extras, pipx_injected  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.cli.install.updater.cli_installs.uv_tool import _side_by_side_machine, _upgrade_in_place, upgrade_side_by_side  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.cli.install.updater.cli_versions import CliResult, _finalize, _run  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.cli.install.updater.uv_receipt import KeptInstall, kept_from_uv_receipt, uv_tool_install_command  # noqa: E402 -- pieces need each other; the front door loads this one first
