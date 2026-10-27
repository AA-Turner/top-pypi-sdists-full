"""One installer for the CLI (plan clean-uninstall-reinstall R-T1, R-T2, R-T3).

Every supported install entry -- `npx probe-research` (the bootstrap and the
wizard's install), `probe update` run from a temporary copy, `probe daemon
install`, `probe repair` -- puts the CLI on this machine through `install_cli`,
never a plain `uv tool install` through the side-by-side link (which upgraded
or downgraded the ACTIVE `probe-versions/<v>/` in place, under every running
`probe`, with no lock, no rejected check and no selftest: plan R2):

    refuse      while an uninstall's barrier is LIVE; a STALE one is cleared
                (`probe._shared.uninstall_barrier`); without uv, with the
                exact command (a pip or pipx install moves to `uv tool`, the
                managed install: `foreign_install`)
    recover     under the install lock: an interrupted first switch is put
                back (`installs.recover`), `active.json` is made to say what
                is (`installs.fix_record`), and a person's own request clears
                that version's rejection
    build       a healthy env of the version is reused (`installs.health`:
                its receipt, its update path's import, the service's start);
                else it is installed beside the active one -- in a new
                generation folder (`<version>+g<N>`) when the version's own
                folder is in use (the broken active env). A check that could
                not finish (a timeout, a kill by SIGKILL or SIGTERM) keeps the
                env in use as it is; any other such env is neither rebuilt
                nor switched to: checked again next time
    validate    `installs.health` again, on what was built
    switch      `installs.activate`; uv's own folder at the tool path (a
                reinstall by hand) is adopted into `probe-versions` only on a
                quiet machine (`adopt.first_switch_waits`, the first switch's
                rule); a missing or dangling tool path at once
    cleanup     the public scripts (`installs.ensure_shims`: an install into a
                version folder makes none), then migration leftovers and
                unfinished installs nothing uses, then `installs.prune`
                (the active, previous and in-use folders always stay)

Each step can be cut short and the next run finishes it: nothing is changed
before the build validated, the switch is one rename, and the record is
repaired at the next start (C7).
"""

from __future__ import annotations

import contextlib
import os
import shutil
import subprocess
import sys
from dataclasses import dataclass, field
from pathlib import Path

from probe._compat import StrEnum
from probe._shared import handoff, installs, uninstall_barrier

DIST = installs.DIST
#: The command that puts uv on a machine (what the npx launcher runs).
UV_INSTALL = "curl -LsSf https://astral.sh/uv/install.sh | sh"


class Mode(StrEnum):
    #: `npx probe-research`, the wizard's install: the version asked for.
    INSTALL = "install"
    #: `probe repair`: the version installed now, made to work.
    REPAIR = "repair"
    #: `probe daemon install`: the version installed now, with the `daemon` extra.
    DAEMON = "daemon"


@dataclass
class CliOutcome:
    """How `install_cli` ended."""

    #: A working CLI of the version asked for is what the tool path names now
    #: (or, on a busy machine, will be at the next quiet moment: `waiting`).
    ok: bool
    #: The env the tool path names at the end, and the version it holds (dist-info).
    env: Path | None = None
    version: str | None = None
    #: This run built or switched something.
    changed: bool = False
    #: What it did, one line each, for the person.
    lines: list[str] = field(default_factory=list)
    #: What keeps the install INCOMPLETE, one line each.
    problems: list[str] = field(default_factory=list)
    #: It refused before changing anything (an uninstall runs, no uv): why.
    refused: str = ""
    #: The switch waits for a quiet machine (the first switch's rule): why.
    #: Built and checked: it switches over then (`QUIET_SWITCH`), no failure.
    waiting: str = ""
    #: Another update holds the install lock: nothing was looked at (BUSY).
    busy: str = ""
    #: The side-by-side layout cannot be used here (Windows, another
    #: filesystem): the caller installs as before.
    unmanaged: bool = False


#: What a person reads when the switch waits for a quiet machine.
QUIET_SWITCH = "installed; switches over when this computer is quiet (within 24 h)"
#: What a person reads when another update holds the install lock.
BUSY = "an update is running; checked next time"
#: The oldest release whose env `installs.health` can judge (its update path,
#: `probe.core.adopt`, is what the check imports). Nothing older is rebuilt.
MIN_CHECKABLE = "0.328.0"


def refusal() -> str | None:
    """Why nothing may be installed now (an uninstall's barrier is LIVE), else
    None. A STALE barrier is no refusal: `clear_stale_barrier` clears it."""
    return uninstall_barrier.refusal()


def clear_stale_barrier(tools: Path | None = None) -> str | None:
    """Clear a STALE uninstall barrier, under the install lock (which a running
    uninstall holds from its first phase), never waiting for it: busy, it is
    left for the next run. The line to log, or None. Never raises."""
    try:
        root = installs.versions_root(tools)
    except Exception:  # noqa: BLE001
        return None
    try:
        with handoff.install_lock(root, wait_s=0):
            return uninstall_barrier.clear_stale()
    except Exception:  # noqa: BLE001 -- busy: the next run clears it
        return None


def clear_keeper_off() -> None:
    """An install, a sign-in or a configure starts: the OS keeper and the
    lifeboat may come back (R1: `keeper-off` from an earlier uninstall
    survived every reinstall that found its plugins present) -- never while an
    uninstall's barrier is LIVE (it wrote `keeper-off`). Never raises."""
    with contextlib.suppress(Exception):
        if uninstall_barrier.live():
            return
        from probe.service import keeper

        keeper.allow()


#: How long an install waits for the Probe service it started to answer.
SERVICE_START_WAIT_S = 10.0
#: What a person reads where the OS keeper's units cannot be installed.
NO_KEEPER = ("the OS keeper needs a systemd user session, which this machine has none of: "
             "each agent session starts the Probe service instead")


def start_service(*, wait_s: float = SERVICE_START_WAIT_S) -> str | None:
    """The end of every install entry (the wizard's configure and install, the
    npx bootstrap's among them, `probe daemon install`; `probe repair` has its
    own `repair_service`): the Probe service started the way an agent
    session's hooks start it (`client.ensure`), whose start installs the OS
    keeper and the lifeboat (`server._keep`). A fresh machine had no service,
    keeper or lifeboat until its first agent session (plan C5). Nothing while
    an uninstall's barrier is LIVE.

    Never a failure: where the service cannot start or does not answer (a
    no_new_privs pod, an agent's sandbox), the lifeboat is installed from here
    as `probe doctor` does, and one line says so; so it does where the keeper
    has no systemd user session. None when there is nothing to say. Never
    raises."""
    try:
        if uninstall_barrier.live():
            return None
        from probe.service import client

        outcome = client.ensure(wait=wait_s)
        if outcome == client.Ensured.RUNNING:
            return _keeper_note()
        why = {
            client.Ensured.CONFINED: "this process runs with no_new_privs, which a service it started would inherit",
            client.Ensured.UNAVAILABLE: "no CLI interpreter to start it with",
            client.Ensured.BACKOFF: "it was started 3 times in the last minute",
        }.get(outcome, f"it did not answer within {wait_s:g} s")
    except Exception as exc:  # noqa: BLE001 -- the install is done; the next session starts it
        why = f"{type(exc).__name__}: {exc}"[:200]
    with contextlib.suppress(Exception):
        from probe.service import keeper

        keeper.refresh_lifeboat()
    return f"the Probe service is not running yet ({why}); your next agent session starts it"


def _keeper_note() -> str | None:
    """NO_KEEPER on Linux without a systemd user session, else None."""
    with contextlib.suppress(Exception):
        from probe.service import keeper

        if sys.platform.startswith("linux") and keeper.wanted() and not keeper.systemd_manager():
            return NO_KEEPER
    return None


def checkable(version: str | None) -> bool:
    """Can `installs.check` judge an env of `version` (MIN_CHECKABLE or newer)?"""
    found, floor = handoff.release(version), handoff.release(MIN_CHECKABLE)
    return bool(found and floor and found >= floor)


def no_uv_message(version: str | None = None) -> str:
    spec = f"'{DIST}[all]" + (f"=={version}'" if version else "'")
    return (f"uv is not installed, and Probe installs its CLI with uv. Install uv: `{UV_INSTALL}`, "
            f"then `uv tool install {spec}` (or run `npx probe-research` again)")


def _uv() -> str | None:
    return shutil.which("uv")


def layout_usable(tools: Path) -> bool:
    """Can the CLI live in the side-by-side layout here (POSIX, the versions
    folder on the tool folder's filesystem)? The tool path may be missing."""
    if os.name == "nt":
        return False
    with contextlib.suppress(OSError):
        tools.mkdir(parents=True, exist_ok=True)
    return installs.same_filesystem(tools)


def _kept(tools: Path):
    """What the install records beside probe-research (its receipt): the tool
    path's env when it has one, else the newest env in the versions folder."""
    from probe.cli import updater

    for env in (installs.tool_env(tools), installs.active(tools), installs.previous(tools)):
        if env is not None and (Path(env) / installs.RECEIPT).is_file():
            kept = updater.kept_from_uv_receipt(env)
            if kept is not None:
                return kept
    return updater.KeptInstall()


def _extras_of(env: Path) -> set:
    from probe.cli import updater

    kept = updater.kept_from_uv_receipt(env)
    return set(kept.extras) if kept is not None else set()


def _candidates(version: str, tools: Path) -> list[Path]:
    """Envs that may already be `version`: the one the tool path names, then
    every generation of it in the versions folder, newest first."""
    found: list[Path] = []
    for env in (installs.active(tools), *installs.envs_of(version, tools)):
        if env is None:
            continue
        resolved = env.resolve() if env.exists() else env
        if all(resolved != (f.resolve() if f.exists() else f) for f in found):
            found.append(env)
    return found


def _quiet(tools: Path) -> str | None:
    """None when the first switch may move uv's folder now; else why it waits."""
    try:
        from probe.core import adopt

        return adopt.first_switch_waits(tools)
    except Exception as exc:  # noqa: BLE001 -- unknown: it waits, as an update would
        return f"the first switch waits: the machine's quiet check failed ({type(exc).__name__}: {exc})"


def adopt_plain(tools: Path) -> Path | None:
    """uv's own folder at the tool path, healthy and the version wanted: into
    the versions folder, the tool path linked to it (`installs.adopt_plain`)."""
    return installs.adopt_plain(tools)


def install_cli(
    version: str,
    *,
    mode: Mode = Mode.INSTALL,
    extras: tuple = (),
    person: bool = True,
    tools: Path | None = None,
    lock_wait_s: float | None = None,
) -> CliOutcome:
    """Make `version` of the CLI the working, active install (see the module
    docstring). `lock_wait_s`: how long to wait for another update's install
    lock (default `installs.LOCK_WAIT_S`); still held then, nothing is done
    and `busy` says so -- not a refusal. Never raises: every failure is an
    outcome."""
    out = CliOutcome(ok=False)
    said = refusal()
    if said:
        out.refused = said
        return out
    clear_keeper_off()
    if _uv() is None:
        out.refused = no_uv_message(version)
        return out
    try:
        tools = tools or installs.tool_dir()
    except Exception as exc:  # noqa: BLE001
        out.refused = f"uv's tool folder could not be told: {exc}"
        return out
    if not layout_usable(tools):
        out.unmanaged = True
        return out
    wait = installs.LOCK_WAIT_S if lock_wait_s is None else lock_wait_s
    try:
        with handoff.install_lock(installs.versions_root(tools), wait_s=wait):
            uninstall_barrier.check()  # written while this waited for the lock
            cleared = uninstall_barrier.clear_stale()  # under the lock: no uninstall runs now
            if cleared:
                out.lines.append(cleared)
            _install_locked(out, version, mode=mode, extras=tuple(extras), person=person, tools=tools)
    except uninstall_barrier.UninstallRunning as exc:
        out.refused = str(exc)
    except handoff.LockBusy:
        out.busy = BUSY
    except Exception as exc:  # noqa: BLE001 -- said, never a traceback over the wizard's screen
        out.problems.append(f"the CLI install failed: {type(exc).__name__}: {exc}"[:500])
        out.ok = False
    return out


def _install_locked(out: CliOutcome, version: str, *, mode: Mode, extras: tuple, person: bool,
                    tools: Path) -> None:
    from probe.cli import updater

    if installs.recover(tools):
        out.lines.append("put back a first switch an earlier run left half done")
    out.lines.extend(installs.fix_record(tools))
    if person and installs.clear_rejected(version, tools):
        out.lines.append(f"CLI {version} was marked rejected on this machine; you asked for it, so it is tried again")
    state = installs.tool_state(tools)
    kept = _kept(tools)
    wanted_extras = set(extras)
    if mode is Mode.DAEMON:
        wanted_extras.add("daemon")

    # Reuse a healthy env of the version (the active one first).
    target: Path | None = None
    unchecked: str | None = None
    plain = installs.tool_env(tools) if state == installs.ToolPath.PLAIN else None
    in_use = installs.active(tools)
    candidates = ([plain] if plain is not None else []) + _candidates(version, tools)
    for env in candidates:
        if not wanted_extras <= _extras_of(env):
            continue
        problem, broken = installs.check(env, version)
        if problem is None:
            target = env
            break
        if not broken:
            # A check that could not finish (a timeout on a loaded machine, a
            # kill by SIGKILL) says nothing against the env: never rebuilt for
            # it. The env in use stays as it is; any other is never switched
            # to unchecked (a `+gN` a run left could take the shared service).
            if env == plain or (in_use is not None and env.resolve() == in_use):
                out.lines.append(f"{env} could not be checked ({problem}); kept as it is, checked next time")
                target = env
                break
            unchecked = unchecked or problem
            continue
        if installs.env_version(env) == version:
            out.lines.append(f"{env} does not work: {problem}")

    if target is None and unchecked is not None:
        out.problems.append(f"CLI {version}'s check could not finish ({unchecked}); nothing was switched, "
                            "tried again next time")
        return

    if target is None:
        spec = updater._dist(tuple(sorted({*kept.extras, *wanted_extras}))) + f"=={version}"  # noqa: SLF001
        rebuild = bool(installs.envs_of(version, tools))
        try:
            env, dropped = updater._install_with_fallbacks(version, spec, kept, tools, rebuild=rebuild)  # noqa: SLF001
        except subprocess.TimeoutExpired as exc:
            out.problems.append(f"could not install CLI {version}: `uv tool install` timed out after "
                                f"{exc.timeout:.0f} s; nothing was switched")
            return
        except (RuntimeError, OSError, subprocess.SubprocessError) as exc:
            out.problems.append(f"could not install CLI {version}; nothing was switched: {exc}"[:800])
            return
        problem, broken = installs.check(env, version)
        if problem and broken:
            installs.discard(env, tools)
            out.problems.append(f"CLI {version} installed but does not work ({problem}); nothing was switched")
            return
        if problem:
            # Kept (the hand-off's UNCHECKED): checked, and switched to, next time.
            out.problems.append(f"CLI {version} is installed, but its check could not finish ({problem}); "
                                "nothing was switched, and the next run checks it again")
            return
        out.changed = True
        where = env.parent.name
        out.lines.append(f"installed CLI {version} in {where}" + (
            f" (beside the broken {version}, which stays until nothing uses it)" if "+g" in where else ""))
        if dropped:
            out.lines.append(f"left out --with {', '.join(dropped)}, which would not install beside it")
        target = env

    # Switch.
    if plain is not None:
        why = _quiet(tools)
        if why:
            out.waiting = why
            if target == plain:
                out.ok = True  # it works as it is; the next quiet moment adopts it
                out.env, out.version = plain, version
            return
        if target == plain:
            adopted = adopt_plain(tools)
            out.changed = True
            out.lines.append(f"moved uv's own folder into the versions folder ({adopted.parent.name if adopted else '?'})")
        else:
            installs.activate(target, tools=tools)
            out.changed = True
            out.lines.append(f"switched the CLI to {target.parent.name} (uv's own folder kept to switch back to)")
    else:
        current = installs.active(tools)
        if current is None or current != target.resolve():
            installs.activate(target, tools=tools)
            out.changed = True
            before = {installs.ToolPath.MISSING: "no CLI at the tool path",
                      installs.ToolPath.DANGLING: "a tool path naming a deleted env"}.get(state)
            out.lines.append(f"switched the CLI to {target.parent.name}" + (f" (was: {before})" if before else ""))

    if out.changed:
        _write_runtime(tools)

    # Cleanup.
    _drop_legacy_tool(tools, out)
    made, blocked = installs.ensure_shims(tools)
    if made:
        out.lines.append("put the `probe` command back: " + "; ".join(made))
    # A pipx install's own `probe` is what moving it to uv takes away
    # (`migrate_foreign`), never a reason this install failed.
    pipx = [line for line in blocked if PIPX_VENV_MARK in line]
    blocked = [line for line in blocked if PIPX_VENV_MARK not in line]
    out.lines.extend(f"`probe` on PATH is still pipx's until it moves: {line}" for line in pipx)
    out.problems.extend(f"`probe` on PATH: {line}" for line in blocked)
    out.lines.extend(installs.fix_record(tools))
    removed = installs.cleanup(tools)
    if removed:
        out.lines.append("removed what nothing uses: " + ", ".join(p.name for p in removed))
    active = installs.active(tools) or installs.tool_env(tools)
    out.env = active
    out.version = installs.env_version(active)
    out.ok = out.version == version and not blocked


def _write_runtime(tools: Path) -> None:
    """After a switch: runtime.json names the env the tool path names now, so
    a service started from it (or by a guard) never runs the env it replaced."""
    with contextlib.suppress(Exception):
        from probe.service import client

        active = installs.active(tools)
        if active is not None:
            client.write_runtime(str(installs.env_python(active)), installs.env_version(active) or "")


#: In a link that points into pipx's env of the CLI.
PIPX_VENV_MARK = f"/pipx/venvs/{DIST}/"
#: The CLI's tool name before it was `probe-research`: it owns the same `probe`.
LEGACY_TOOL = "probe-agent"


def _drop_legacy_tool(tools: Path, out: CliOutcome) -> None:
    """The old `probe-agent` uv tool owns the same `probe` command: it goes, as
    the bootstrap's install always took it away first."""
    if not (tools / LEGACY_TOOL).exists():
        return
    done = subprocess.run(["uv", "tool", "uninstall", LEGACY_TOOL], capture_output=True, text=True,
                          timeout=120, check=False)
    if done.returncode == 0:
        out.lines.append(f"removed the old `{LEGACY_TOOL}` tool, which owned the same `probe` command")


def foreign_install() -> tuple[str, str] | None:
    """A `probe` on this machine that a pip or pipx install owns (not uv's
    tool install, not a throwaway copy): `(method, path)`, else None."""
    from probe.cli import bootstrap

    binary = bootstrap._installed_binary()  # noqa: SLF001
    if binary is None:
        return None
    real = os.path.realpath(binary).replace(os.sep, "/")
    if f"/uv/tools/{DIST}/" in real or f"/{installs.VERSIONS_DIRNAME}/" in real:
        return None
    pipx_home = os.environ.get("PIPX_HOME")
    if "/pipx/venvs/" in real or (pipx_home and real.startswith(os.path.realpath(pipx_home).replace(os.sep, "/"))):
        return "pipx", binary
    return "pip", binary


def migrate_foreign(found: tuple[str, str]) -> list[str]:
    """After the uv tool install worked: take a pipx install's `probe` off
    PATH (`pipx uninstall`: pipx's env holds the CLI alone). A pip install is
    a project's or a researcher's environment (the SDK lives there): never
    touched, only named when its `probe` comes first on PATH. Lines to show."""
    from probe.cli import bootstrap

    method, binary = found
    if method == "pipx":
        if bootstrap._is_this_install(binary):  # noqa: SLF001
            # This very process runs from pipx's env: removing it under the
            # running wizard would break the rest of it.
            return [f"the CLI is installed with uv now; once this ends, run `pipx uninstall {DIST}` and then "
                    "`probe repair` to finish the move"]
        venv = Path(os.path.realpath(binary)).parent.parent
        if installs._in_use(venv):  # noqa: SLF001 -- a run, a daemon worker, a hook from pipx's env
            return ["the old pipx install is still in use; removed next time"]
        done = subprocess.run(["pipx", "uninstall", DIST], capture_output=True, text=True, timeout=120,
                              check=False) if shutil.which("pipx") else None
        if done is not None and done.returncode == 0:
            made, _blocked = installs.ensure_shims()
            return [f"moved the CLI from pipx to uv (the managed install): `pipx uninstall {DIST}` removed {binary}",
                    *(f"`probe` is uv's now: {line}" for line in made)]
        return [f"the pipx install of {DIST} ({binary}) is still there; run `pipx uninstall {DIST}`"]
    return [f"{binary} is a pip install's `probe` (left alone: its environment may be a project's); "
            "the managed CLI is uv's"]
