"""Every update's first step, in release code: hand it to the newest release, or adopt it (plan A1, A2).

    begin(trigger)  what every update entry calls FIRST, before any other
                    updater code reads anything: the service's child
                    (`probe.core.actions.update`), `probe wizard --action
                    update` (terminal, `--yes`, `--json`), the menu's Update,
                    `probe update`, the detached auto-update
                    (`version_refresh --apply`). With PROBE_UPDATE_ADOPT set
                    (this process is the newest release, exec'd by a hand-off)
                    it adopts. Otherwise it runs the frozen hand-off's stage 1
                    (`probe._shared.handoff.stage1`), which either execs the
                    newest release (never returning) or answers, and the
                    update goes on here as before.

    adopt           the new release takes over: checks that it is the env it
                    was handed and that its own update path imports, waits for
                    a quiet machine when this is the first switch (uv's own
                    folder still at the tool path; the service's quiet check
                    and its 24 h limit), switches the tool path to itself
                    under the install lock the hand-off passed over (and lets
                    it go), points runtime.json at itself, then lets the update
                    go on with PROBE_UPDATE_SKIP_CLI (the CLI half is done:
                    `cli_result`). The lifeboat's env.json is the service's to
                    write, at every start (`probe.service.lifeboat`): the
                    service restarts onto this release after the update.

Old releases never see PROBE_UPDATE_ADOPT: only the hand-off sets it, and it
execs only an env it just installed or found complete.
"""

from __future__ import annotations

import contextlib
import json
import os
import shutil
import sys
import time
from dataclasses import dataclass
from pathlib import Path

from probe._shared import handoff

#: The update ends here, nothing switched: try again later (`wizard_lock.BUSY_EXIT_CODE`).
DEFERRED_EXIT = 75
FAILED_EXIT = 1
#: `active.json`: when the first switch started waiting for a quiet machine.
FIRST_SWITCH_WAIT_KEY = "first_switch_waiting_since"
#: `probe.cli.upgrading.SKIP_CLI_ENV` (and the service's): the CLI half of
#: this update is done or not to be done. Named here too so the service's
#: child reads it before importing the CLI.
SKIP_CLI_ENV = "PROBE_UPDATE_SKIP_CLI"


@dataclass(frozen=True)
class Ending:
    """The update ends at its first step: the exit status, and why (one line)."""

    status: int
    message: str


#: Set once `begin` ran in this process (an entry nested in another -- the
#: service's child runs the wizard's Update -- does not run it twice).
_begun = False
#: stage 1's answer in this process, when it ran and did not exec.
_answer: dict | None = None
#: The version the hand-off came from, once this process adopted.
_adopted_from: str | None = None
#: The trigger the hand-off ran under (PROBE_HANDOFF_TRIGGER, taken out of the
#: environment by the adopt): the report's attempt trigger.
_handed_trigger: str | None = None
#: What the adopted CLI step's line adds: receipt entries it could not carry.
_note: str = ""


def reset() -> None:
    """Forget this process's first step (tests)."""
    global _begun, _answer, _adopted_from, _handed_trigger, _note
    _begun, _answer, _adopted_from, _handed_trigger, _note = False, None, None, None, ""


def handed_trigger() -> str | None:
    """The trigger the release before this one ran the update under, when this
    process took it over (PROBE_HANDOFF_TRIGGER), else None."""
    return _handed_trigger


def _say(message: str) -> None:
    with contextlib.suppress(Exception):
        print(f"probe update: {message}", file=sys.stderr, flush=True)


def stage1_answer() -> dict | None:
    """What stage 1 answered in this process (None: it did not run)."""
    return _answer


def adopted_from() -> str | None:
    return _adopted_from


def runs_managed_cli() -> bool:
    """Is this process the machine's managed CLI: a uv tool install of
    probe-research from its index (not a path or URL), run from the tool
    path or a version env? Only that one is updated side by side -- and not
    when a person asked for in place (`updater.IN_PLACE_ENV`)."""
    if os.name == "nt":
        return False
    try:
        from probe._shared import installs
        from probe.cli import updater

        if os.environ.get(updater.IN_PLACE_ENV) == "1":
            return False
        prefix = str(Path(sys.prefix)).replace(os.sep, "/")
        if f"/uv/tools/{installs.DIST}" not in prefix and not installs.running_from_versions(prefix):
            return False
        if updater.detect_install().method != updater.Method.UV_TOOL:
            return False
        return updater.kept_from_uv_receipt() is not None
    except Exception:  # noqa: BLE001 -- unknown: the update goes on as before
        return False


def install_inputs() -> dict:
    """What stage 1 installs beside the running version: the extras, `--with`
    packages and Python this install's uv receipt records (the same restating
    `updater.upgrade_side_by_side` does), and uv."""
    from probe.cli import updater

    kept = updater.kept_from_uv_receipt() or updater.KeptInstall()
    if kept.dropped:
        _say("the new version is installed without what this install's uv receipt records that cannot be "
             f"restated: {', '.join(kept.dropped)}")
    spec = updater._dist(kept.extras)  # noqa: SLF001 -- the one rule for the extras
    extras = spec[spec.index("[") + 1: spec.index("]")].split(",") if "[" in spec else ["all"]
    return {
        "extras": [extra for extra in extras if extra],
        "with": list(kept.with_packages),
        "python_request": kept.python,
        "uv": shutil.which("uv"),
    }


def begin(trigger: str, *, argv: list[str] | None = None, before_exec=None) -> Ending | None:
    """The first step of an update (see the module docstring). None: go on.
    An `Ending`: the update stops here (an adopt that must wait, or a release
    that cannot run its own update). Runs once per process; never raises."""
    global _begun, _answer
    if _begun:
        return None
    _begun = True
    if os.environ.get(handoff.ADOPT_ENV):
        return adopt()
    if not runs_managed_cli():
        return None
    try:
        from probe import __version__, version_policy
        from probe._shared import installs

        _answer = handoff.stage1(
            trigger,
            argv=argv,
            before_exec=before_exec,
            tools=str(installs.tool_dir()),
            base_url=version_policy.base_url(),
            install_inputs=install_inputs(),
            current=__version__,
        )
    except Exception as exc:  # noqa: BLE001 -- the update goes on here, as before
        _answer = {"result": "error", "detail": f"{type(exc).__name__}: {exc}"}
    result = _answer.get("result")
    if result not in (handoff.Result.CURRENT, handoff.Result.NOT_MANAGED):
        _say(f"the newest release could not take this update over ({result}"
             + (f": {_answer['detail']}" if _answer.get("detail") else "") + "); it goes on here")
    return None


def selftest() -> str | None:
    """Does this release's own update path load, and can it read the manifest?
    None when it does (a manifest that cannot be fetched is the network's, not
    a fault of this release); else what failed."""
    import importlib

    try:
        for name in ("probe.core.run", "probe.cli.updater", "probe.cli.upgrading", "probe.cli.update_report",
                     "probe.cli.main"):
            importlib.import_module(name)
    except Exception as exc:  # noqa: BLE001 -- an import that fails is a release that cannot update
        # (Not BaseException: a Ctrl-C meanwhile must never reject a good release.)
        return f"{type(exc).__name__}: {exc}"[:300]
    from probe import version_policy
    from probe.cli import updater

    try:
        manifest = updater.fetch_latest(version_policy.base_url())
    except Exception:  # noqa: BLE001 -- offline, or the server's: not this release's fault
        return None
    try:
        updater.cli_latest(manifest)
        updater.plugin_latest(manifest)
        updater.tap_latest(manifest)
    except Exception as exc:  # noqa: BLE001
        return f"reading the manifest: {type(exc).__name__}: {exc}"[:300]
    return None


def _runs_from(target: Path) -> bool:
    try:
        return Path(sys.prefix).resolve() == target.resolve()
    except OSError:
        return False


def _skip(reason: str) -> None:
    """The deferral in `autoupdate.json` (`probe doctor`), as the service records its own."""
    with contextlib.suppress(Exception):
        from probe._shared import autoupdate
        from probe.cli import update_report
        from probe.service import updater as service_updater

        name = service_updater._SKIPS.get(reason)  # noqa: SLF001 -- the service's own map
        if name:
            trigger = update_report.trigger_from_env(update_report.Trigger.CLI)
            autoupdate.record_skip(getattr(autoupdate, name), trigger=trigger)


def first_switch_waits(tools: Path, *, at: float | None = None) -> str | None:
    """The first switch moves the folder every running `probe` reads its files
    through (`installs.needs_migration`), so it is made only on a quiet
    machine (the service's quiet check, `probe.service.updater.look`: a
    waiting wizard menu's marker counts, as this switch moves its files), or
    once every reason it waited for has lasted the service's DEFER_LIMIT_S (24
    h), as the service updates past them -- a setup by its own record's age.
    None: go on. A child of the service (its barrier's token) was let through
    by the service's own check."""
    from probe._shared import installs
    from probe.service import barrier
    from probe.service import updater as service_updater
    from probe.service.protocol import DeferReason

    if os.environ.get(barrier.TOKEN_ENV):
        return None
    at = time.time() if at is None else at
    # Never this process's own: a wizard menu's Update execs into this release
    # with the same pid, and its menu marker (or lock) is no setup to wait for.
    busy = service_updater.look(action_running=False, exclude_pid=os.getpid())
    reasons = busy.reasons()
    record = installs.record(tools)
    if not reasons:
        if FIRST_SWITCH_WAIT_KEY in record:
            installs.set_fields(tools, **{FIRST_SWITCH_WAIT_KEY: None})
        return None
    since = record.get(FIRST_SWITCH_WAIT_KEY)
    if not isinstance(since, (int, float)) or since > at:
        since = at
        installs.set_fields(tools, **{FIRST_SWITCH_WAIT_KEY: since})
    limit = service_updater._env_seconds(service_updater.DEFER_LIMIT_ENV, service_updater.DEFER_LIMIT_S)  # noqa: SLF001
    # A setup's time is its own (how long the lock has been held, or a menu has
    # waited: `Busy.setup_time`, plan C1), as the service counts it; else, a
    # holder from before the record, how long this switch has waited.
    held = busy.setup_time()

    def waited(reason: str) -> float:
        return at - (held if reason == DeferReason.SETUP_RUNNING and held is not None else since)

    if set(reasons) <= service_updater.LIMITED and all(waited(reason) >= limit for reason in reasons):
        _say(f"switching although {', '.join(reasons)} (waited {(at - since) / 3600:.1f} h)")
        return None
    _skip(reasons[0])
    return (f"the first switch to side-by-side installs waits for a quiet machine ({', '.join(reasons)}); "
            "the new version stays installed beside this one, and the next update switches")


def tools_for(target: Path) -> Path | None:
    """The uv tool folder whose versions folder holds `target`
    (`<tools>/../probe-versions/<v>/probe-research`): `uv tool dir`'s answer,
    else the one the last switch recorded (`active.json` `tools`), else the
    lifeboat's env.json -- a lifeboat's exec may carry a PATH without uv, and
    uv's default folder is not every machine's. None when none of them is."""
    from probe._shared import installs

    root = target.parent.parent
    candidates: list = []
    with contextlib.suppress(Exception):
        candidates.append(installs.tool_dir())
    with contextlib.suppress(OSError, ValueError, AttributeError):
        candidates.append(json.loads((root / installs.ACTIVE_NAME).read_text(encoding="utf-8")).get("tools"))
    candidates.append(handoff.read_env().get("tools"))
    for candidate in candidates:
        if not candidate:
            continue
        with contextlib.suppress(OSError):
            if installs.versions_root(Path(candidate)).resolve() == root.resolve():
                return Path(candidate)
    return None


def _wait_for_parent() -> None:
    """A detached update waits for the `probe` that spawned it before anything
    moves under it (`upgrading._update_turn`'s reason)."""
    from probe._shared import autoupdate

    parent = os.environ.get(autoupdate.WAIT_FOR_PID_ENV)
    if parent and parent.isdigit():
        autoupdate.wait_for_pid_exit(int(parent))


def adopt() -> Ending | None:
    """This process is the release a hand-off installed (PROBE_UPDATE_ADOPT):
    switch the CLI to it, then let the update go on with the CLI half done.
    The hand-off's variables are taken out of the environment (nothing this
    update starts adopts again), and its lock is let go once the switch is."""
    global _handed_trigger
    # Taken out of the environment at once: nothing this update starts (a
    # plugin step's `probe`, the pi update) may adopt or report as handed again.
    target = Path(os.environ.pop(handoff.ADOPT_ENV))
    dropped_raw = os.environ.pop(handoff.DROPPED_WITH_ENV, "")
    came_from = os.environ.pop(handoff.FROM_ENV, "") or None
    _handed_trigger = os.environ.pop(handoff.TRIGGER_ENV, "") or None
    try:
        return _adopt(target, dropped_raw, came_from)
    except Exception as exc:  # noqa: BLE001 -- said, never a traceback over the event stream
        return Ending(FAILED_EXIT, f"could not switch the CLI to {target}: {type(exc).__name__}: {exc}")
    finally:
        handoff.release_inherited(target.parent.parent)


def _adopt(target: Path, dropped_raw: str, came_from: str | None) -> Ending | None:
    global _adopted_from, _note
    from probe import __version__
    from probe._shared import installs
    from probe.cli import updater

    root = target.parent.parent
    if not _runs_from(target):
        return Ending(FAILED_EXIT, f"refusing to switch to {target}: this interpreter runs from {sys.prefix}")
    tools = tools_for(target)
    if tools is None:
        return Ending(FAILED_EXIT, f"refusing to switch to {target}: no uv tool folder here has it in its "
                                   "versions folder; nothing was switched")
    problem = selftest()
    if not problem:
        # The checks every switch makes before it (`upgrade_side_by_side`): the
        # service's start path and the CLI's import, by the env's own interpreter.
        problem = installs.selftest(target)
    if problem:
        installs.reject(__version__, f"it does not start: {problem}", tools)
        return Ending(FAILED_EXIT, f"CLI {__version__} does not start ({problem}); nothing was switched, "
                                   f"and {__version__} is skipped for {installs.REJECT_TTL_S // 3600} h")
    if installs.needs_migration(tools):
        waits = first_switch_waits(tools)
        if waits:
            return Ending(DEFERRED_EXIT, waits)
    _wait_for_parent()
    # What the install it replaces records: its receipt's unrestatable
    # entries (said on the CLI step's line) and what it has that this env
    # must have too (`updater.record_left_out`, after the switch).
    old = None
    with contextlib.suppress(Exception):
        old = updater.kept_from_uv_receipt(installs.tool_env(tools))
        _note = updater.dropped_note(old)
    installs.activate(target, tools=tools)  # under the lock the hand-off passed over
    # Let it go now: the plugin and pi steps after this never hold the install
    # lock (a long plugin phase would read as a stale holder to stop).
    handoff.release_inherited(root)
    with contextlib.suppress(Exception):
        installs.set_fields(tools, **{FIRST_SWITCH_WAIT_KEY: None})
    with contextlib.suppress(Exception):
        from probe.service import client

        client.write_runtime(str(installs.env_python(target)), __version__)
    with contextlib.suppress(Exception):
        updater.record_left_out(old, target, tools, _handed_drops(dropped_raw))
    with contextlib.suppress(Exception):
        installs.prune(tools)
    _adopted_from = came_from
    os.environ[SKIP_CLI_ENV] = "1"
    _say(f"switched the CLI {came_from or '?'} -> {__version__}; the rest of this update runs in {__version__}")
    return None


def _handed_drops(dropped_raw: str) -> list:
    """PROBE_HANDOFF_DROPPED_WITH: the `--with` packages the hand-off's install
    left out (what the receipts say decides, `updater.record_left_out`)."""
    try:
        new = json.loads(dropped_raw) if dropped_raw else []
    except ValueError:
        return []
    return [item for item in new if isinstance(item, str)] if isinstance(new, list) else []


def cli_result(current: str):
    """The CLI step of an update this process adopted: the switch it made
    (`before` is the version the hand-off came from). None when it did not adopt."""
    if _adopted_from is None:
        return None
    from probe.cli import updater

    before = _adopted_from
    if updater.is_newer(current, before):
        message = f"CLI upgraded {before} → {current} (beside {before}, which stays for a switch back)"
    elif before == current:
        message = f"CLI already at {current}"
    else:
        message = f"CLI switched back {before} → {current}"
    return updater.CliResult(ran=True, ok=True, changed=before != current, before=before, after=current,
                             message=message + _note)
