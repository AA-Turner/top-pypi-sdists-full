"""Performing an update, as a function the wizard can call.

This was the body of a top-level `probe update` command. It moved here because
the wizard's Update action used to print "Run: probe update" and exit — which
is absurd. The wizard's whole job is to DO the thing; bouncing the user back to
a shell to type a command themselves is the failure it exists to remove.

There is still a hidden `probe update` bound to this, because the plugin's
SessionStart hook spawns it and plugins update on the USER's schedule, not
ours. Deleting the command outright would silently break auto-update on every
machine whose plugin has not been refreshed yet.
"""

from __future__ import annotations

import dataclasses
import contextlib
import contextvars
import os
import signal
import threading
import time
from collections.abc import Callable, Sequence
from concurrent.futures import Future
from concurrent.futures import TimeoutError as FuturesTimeout
from contextlib import ExitStack, contextmanager
from dataclasses import dataclass, field

from probe import __version__
from probe._compat import StrEnum
# `update_report` is imported HERE, at the top, for the same reason updater.py
# imports its whole call graph eagerly (H8): it runs after `uv tool upgrade` has
# replaced the installed tree, when a first import would read the new files.
from probe.cli import (
    autoupdate,
    claude_cli,
    plugin_cli,
    root_skills,
    update_report,
    updater,
    versions,
    wizard_lock,
)
from probe.cli.capabilities import agent_source
from probe.harness import get_registry
from probe.core import events as json_events


class UpdatePart(StrEnum):
    """The parts of an Update a progress hook (`reporting_progress`) hears
    finish, besides each agent's own plugins (named by its source)."""

    CLI = "cli"
    PI_PACKAGE = "pi_package"


_progress: contextvars.ContextVar[Callable[[str], None] | None] = contextvars.ContextVar(
    "probe_update_progress", default=None
)


@contextmanager
def reporting_progress(hook: Callable[[str], None]):
    """In this block, `hook(part)` hears each part of an Update finish (an
    `UpdatePart`, or an agent's source once its plugins are through), from
    whichever thread ran it: the wizard's bar. Never fails the update."""
    token = _progress.set(hook)
    try:
        yield
    finally:
        _progress.reset(token)


def _finished(part: str) -> None:
    hook = _progress.get()
    if hook is None:
        return
    try:
        hook(part)
    except Exception:  # noqa: BLE001 - a progress bar must never fail an update
        pass


@dataclass
class UpdateOutcome:
    lines: list[str]
    ok: bool
    #: The plugin or the tap moved and open sessions cannot follow it by
    #: themselves (`updater.follows_without_restart`: a Kimi Code session that
    #: loaded an older manifest or started before its hooks handed over, a
    #: project-scope install, a tap before the hand-back, a session on
    #: protocol 1, one still on its own tap watch): they need a restart, as before.
    restart_needed: bool
    #: The plugin or the tap moved and open sessions follow it: an open
    #: session runs the installed plugin's hooks from its next event
    #: (`hooks/dispatch.py hand_over`), its skill copies are refreshed here,
    #: and the Probe service moves the rest (the status line, the managed
    #: block, its recorders' tap) after its update cycle.
    plugins_moved: bool = False
    #: For the wizard's final screen (`setup.RunSummary`): a few words on where
    #: this agent's plugins ended ("plugin 0.180.0, tap 0.10.23")...
    summary: str = ""
    #: ...what needs attention about them (a failure and the commands to run
    #: by hand), and what needs attention about the run itself (the CLI's
    #: upgrade, pi's package: failures and what open sessions must do), the
    #: same on every agent's answer.
    problems: list[str] = field(default_factory=list)
    run_notes: list[str] = field(default_factory=list)
    #: What the person still has to do with it, though it worked: open
    #: sessions to /reload or restart. Never counts as a failure.
    actions: list[str] = field(default_factory=list)
    #: The run's own such steps: pi's /reload, from an Update of any agents.
    run_actions: list[str] = field(default_factory=list)
    #: The CLI's version line: "Probe CLI 0.324.0", "(updated from 0.323.1)".
    cli: str = ""
    #: A live run held the update off: nothing was updated (`lines` says why).
    deferred: bool = False


#: What `probe update` and the wizard's Update say when the plugins moved and
#: open sessions follow.
PICKED_UP = "No restart needed: open sessions pick up the new plugin at their next prompt."


def after_update_line(outcome: "UpdateOutcome", agent: str, source: str | None = None) -> str | None:
    """The line `probe update` and the wizard's Update end with: no restart
    where open sessions follow, the restart line where they cannot, else none.
    An agent that reloads its plugins in place (`reloads_plugins`: Kimi Code's
    and pi's /reload) is told that first: cheaper than a restart."""
    if getattr(outcome, "plugins_moved", False):
        return PICKED_UP
    if getattr(outcome, "restart_needed", False):
        if source and reloads_plugins(source):
            return f"Run /reload in {agent} (or restart it) to apply the plugin update."
        return f"Restart {agent} to apply the plugin update."
    return None


def reloads_plugins(source: str) -> bool:
    """Does this agent re-read Probe's plugin or package in place with /reload
    (a manifest kept from its start: `loaded_records`; an extension: pi)?"""
    from probe.harness.registry import CAPABILITY_LOADED_RECORDS, FAMILY_EXTENSION

    harness = get_registry().find(source)
    return harness is not None and (harness.can(CAPABILITY_LOADED_RECORDS) or harness.family == FAMILY_EXTENSION)


#: Set by the Probe service (`probe.service.updater.SKIP_CLI_ENV`) when the CLI
#: is current and daemon workers run from its env: plugins only.
SKIP_CLI_ENV = "PROBE_UPDATE_SKIP_CLI"
#: Set by the Probe service (`probe.service.updater.FORCED_ENV`) when it updates
#: past what deferred it for DEFER_LIMIT_S: those reasons, comma separated
#: (`forced_past`). Past a live run the run-lock check is skipped (D33); past a
#: setup holding wizard.lock for a day, the update runs without that lock (C1).
FORCED_ENV = "PROBE_UPDATE_FORCED"


def forced_past(reason: str) -> bool:
    """Did the Probe service decide to update past `reason` (a
    `probe.service.protocol.DeferReason`), naming it in FORCED_ENV?"""
    return reason in os.environ.get(FORCED_ENV, "").split(",")


def menu_holds_update_off() -> bool:
    """Does a `probe wizard` menu in another process wait on a person
    (`setup_marks.menu_waiting`) -- for less than a day -- while this update
    may move the files that menu runs from? The menu lets go of wizard.lock
    while it waits (C1), so this marker is what stops an update from replacing
    files under it mid-write: as the lock, for a day at most, and never once
    the Probe service decided to go past a setup (FORCED_ENV).

    Only an update bound to go beside the running version passes it: the
    Probe service's, which says so (REQUIRE_SIDE_BY_SIDE_ENV) and then never
    falls back to in place. Any other may: a side-by-side machine still updates
    in place with IN_PLACE_ENV, a receipt it cannot restate, or no target
    version known (`updater.upgrade_side_by_side`), so it waits. Never raises:
    unknown reads as no."""
    try:
        from probe._shared import setup_marks
        from probe.sdk import session_marker
        from probe.service.protocol import DeferReason

        if (
            forced_past(DeferReason.SETUP_RUNNING)
            or os.environ.get(updater.REQUIRE_SIDE_BY_SIDE_ENV) == "1"
            # Plugins only (the service's, or what follows an adopt's switch):
            # the CLI's files stay where they are.
            or os.environ.get(SKIP_CLI_ENV) == "1"
        ):
            return False
        waiting, since = setup_marks.menu_waiting(session_marker.state_dir(), exclude_pid=os.getpid())
        if not waiting:
            return False
        from probe.service.updater import DEFER_LIMIT_S

        return since is None or time.time() - since < DEFER_LIMIT_S
    except Exception:  # noqa: BLE001
        return False


def cli_left_alone(version: str) -> "updater.CliResult":
    """The CLI step when the Probe service asked for plugins only (SKIP_CLI_ENV):
    nothing ran, and the CLI is where it should be (a success, never a failure
    in `probe doctor` or the update report)."""
    return updater.CliResult(
        ran=False, ok=True, changed=False, before=version, after=version,
        message=f"CLI {version} current; left as it is while daemon workers run",
    )


@contextlib.contextmanager
def _service_stopped_on_windows(install):
    """Windows (R3): the Probe service runs from the CLI's own uv tool env, and
    Windows cannot replace a file a running process holds. Stop it (its
    recorders pause, saved) for the upgrade, and start it again after (they
    resume). Yields False when it would not stop: the upgrade waits for the
    next try rather than half-replace an env in use. Elsewhere, and for any
    other install, nothing (True).

    Held through the upgrade: `start.lock`, so no hook, tap or keeper starts
    one meanwhile (`client.ensure` finds it taken and starts none), and
    `service.lock`, so one started just before exits as a duplicate."""
    if os.name != "nt" or install.method != updater.Method.UV_TOOL:
        yield True
        return
    from probe.service import client, paths
    from probe.service.protocol import Method

    held: list[int] = []
    asked = False
    stopped = True
    try:
        paths.ensure_dirs()
        with contextlib.suppress(Exception):  # none runs, or it cannot be asked
            client.call(Method.STOP, {}, client="cli", client_version=__version__, timeout=5.0)
            asked = True
        for path in (paths.start_lock_path(), paths.lock_path()):
            fd = os.open(path, os.O_RDWR | os.O_CREAT)
            deadline = time.monotonic() + (15.0 if asked else 2.0)
            while not paths.try_lock(fd):
                if time.monotonic() >= deadline:
                    os.close(fd)
                    stopped = False
                    break
                time.sleep(0.2)
            else:
                held.append(fd)
            if not stopped:
                break
    except OSError:
        pass  # no folder for it: none runs
    try:
        yield stopped
    finally:
        for fd in reversed(held):
            with contextlib.suppress(OSError):
                paths.unlock(fd)
            with contextlib.suppress(OSError):
                os.close(fd)
        if asked:
            with contextlib.suppress(Exception):
                client.ensure()


@contextmanager
def _update_turn(manifest: dict | None, trigger: update_report.Trigger):
    """The wait and the lock an update takes before it changes anything."""
    # WAIT FOR THE PROCESS THAT SPAWNED US, if it named itself.
    #
    # Only the detached auto-update path sets this; the wizard's interactive
    # Update action has no parent to outlive and skips the wait. Replacing the
    # installed tree while the triggering command is still lazily importing from
    # it is how you get a ModuleNotFoundError out of a command that has worked
    # for a year (see autoupdate.wait_for_pid_exit).
    parent = os.environ.get(autoupdate.WAIT_FOR_PID_ENV)
    if parent:
        try:
            autoupdate.wait_for_pid_exit(int(parent))
        except (TypeError, ValueError):
            pass

    # ONE SETUP AT A TIME (`wizard_lock`), and only after the wait: the process
    # that spawned us can be a `probe wizard`, which holds the lock until it
    # exits. The wizard's own Update action holds it already and goes through.
    # So does an update the Probe service runs past a setup that has held the
    # lock for a day (C1): without it, beside that setup, as the service decided.
    # A menu waiting on a person holds no lock: its marker holds an update off
    # that would move its files (`menu_holds_update_off`).
    from probe.service.protocol import DeferReason  # loaded already, by `updater`

    with ExitStack() as stack:
        try:
            stack.enter_context(wizard_lock.held())
            if menu_holds_update_off():
                raise wizard_lock.Busy(wizard_lock.BUSY_MESSAGE)
        except wizard_lock.Busy:
            if not forced_past(DeferReason.SETUP_RUNNING):
                autoupdate.record_skip(
                    autoupdate.SKIP_SETUP_RUNNING,
                    available=updater.cli_latest(manifest) if manifest else None,
                    trigger=trigger.value,
                )
                raise
        yield


def perform_update(
    *,
    base_url: str,
    include_plugin: bool = True,
    force: bool = False,
    manifest: dict | None = None,
    trigger: update_report.Trigger | None = None,
) -> UpdateOutcome:
    """Upgrade the CLI and (optionally) the plugins, and record the attempt.

    There is no confirmation hook. Both callers -- the wizard's Update action
    and the plugin's SessionStart hook -- have already been told to update by
    the time they get here, and the one that has a terminal must not stop to
    ask a second time.

    ``force`` skips the run-lock check. Reserved for a human who has explicitly
    asked to upgrade now and can see what is running; nothing automatic sets it.

    ``manifest`` is for a caller that ALREADY fetched one. The run-end path
    (version_refresh's apply-if-newer mode) has to compare before it decides to
    call us at all, and without this it would fetch twice -- once to decide, once
    here to pick a target. Two fetches are not just wasteful: a release landing
    between them means comparing against one version and upgrading toward
    another. Omit it and we fetch, exactly as before.

    ``trigger`` is what asked for this run, for the server's update report
    (`update_report`); omitted, the spawner's `PROBE_AUTOUPDATE_TRIGGER`, else
    a person. It changes nothing about the update itself.

    Raises `wizard_lock.Busy`, having changed nothing and recorded the skip,
    while another Probe setup holds the device.
    """
    trigger = trigger or update_report.trigger_from_env(update_report.Trigger.MANUAL)

    with _update_turn(manifest, trigger):
        return _perform_update(
            base_url=base_url, include_plugin=include_plugin, force=force, manifest=manifest, trigger=trigger
        )


#: Each component's own deadline (plan A3): a coding agent's plugin step, pi's
#: package. Past it the component is failed and left running on its thread;
#: the CLI's step and the other components finish and report.
COMPONENT_DEADLINE_S = 10 * 60
#: Overrides COMPONENT_DEADLINE_S, in seconds (tests).
COMPONENT_DEADLINE_ENV = "PROBE_UPDATE_COMPONENT_DEADLINE_S"


def component_deadline() -> float:
    try:
        value = float(os.environ.get(COMPONENT_DEADLINE_ENV, ""))
    except ValueError:
        return COMPONENT_DEADLINE_S
    return value if value > 0 else COMPONENT_DEADLINE_S


class ComponentOverdue(Exception):
    """A component that did not finish within its deadline (`component_deadline`)."""


def _deadline_words(seconds: float) -> str:
    return f"{seconds / 60:.0f} min" if seconds >= 120 else f"{seconds:g} s"


@dataclass
class _Component:
    """One part of an update on its thread (`_start`): its Future, and the
    processes it started (`claude_cli.Processes`), stopped at its deadline."""

    future: Future
    processes: claude_cli.Processes


def _start(name: str, body: Callable[[], object]) -> _Component:
    """`body` on a thread of its own, in a copy of this context, every agent
    CLI it starts tracked (`claude_cli.tracking`). A thread that cannot start
    runs it here instead."""
    future: Future = Future()
    processes = claude_cli.Processes()
    context = contextvars.copy_context()

    def tracked() -> object:
        with claude_cli.tracking(processes):
            return body()

    def run() -> None:
        try:
            future.set_result(context.run(tracked))
        except BaseException as exc:  # noqa: BLE001 - handed to the waiter, for its component
            future.set_exception(exc)

    try:
        threading.Thread(target=run, name=f"probe-update-{name}", daemon=True).start()
    except RuntimeError:
        run()
    return _Component(future, processes)


def _outcome_by(component: _Component, deadline: float, what: str) -> object:
    """The component's result, or what it raised (an exception value, never
    raised here), or `ComponentOverdue` at `deadline` (time.monotonic()): then
    every process it started is killed with its process group, and it starts
    no more (its thread winds down on its own). An interrupt of THIS thread
    while it waits still rises."""
    future = component.future
    try:
        failure = future.exception(timeout=max(0.0, deadline - time.monotonic()))
    except FuturesTimeout:
        stopped = component.processes.stop()
        return ComponentOverdue(
            f"{what} did not finish within {_deadline_words(component_deadline())}"
            + (f" and was stopped ({stopped} process{'' if stopped == 1 else 'es'})" if stopped else "")
            + "; the next update tries again"
        )
    return failure if failure is not None else future.result()


#: Signals that end an update wherever it is (the service's SIGTERM to the
#: update's process group, a closed terminal's SIGHUP).
_ENDING_SIGNALS = tuple(
    number for number in (getattr(signal, "SIGTERM", None), getattr(signal, "SIGHUP", None)) if number is not None
)


def _exit_on_signal(number: int, _frame) -> None:
    """End the update (SystemExit 128+N) -- the next ending signal ignored
    meanwhile, so a second SIGTERM cannot cut its way out short of stopping
    every step's processes (`_stopped_with_the_update`)."""
    for each in _ENDING_SIGNALS:
        with contextlib.suppress(OSError, ValueError):
            if signal.getsignal(each) is _exit_on_signal:  # only ours: the wait puts them back
                signal.signal(each, signal.SIG_IGN)
    raise SystemExit(128 + number)


@contextmanager
def _stopped_with_the_update(components: "list[_Component]"):
    """The wait for `components`: whatever ends it early -- Ctrl-C's
    KeyboardInterrupt, the service's SIGTERM (`events._stop`'s SystemExit),
    any exception -- first stops every process they started (each runs in a
    session of its own, out of reach of a signal to this process's group),
    then rises. SIGTERM and SIGHUP that nothing here handles (a terminal
    `probe update`: their default kills at once, leaving those processes
    behind) get a handler for the wait that raises SystemExit(128+N)."""
    installed: dict = {}
    if threading.current_thread() is threading.main_thread():
        for number in _ENDING_SIGNALS:
            with contextlib.suppress(OSError, ValueError):
                if signal.getsignal(number) in (signal.SIG_DFL, None):
                    installed[number] = signal.signal(number, _exit_on_signal)
    try:
        yield
    except BaseException:
        for component in components:
            component.processes.stop()
        raise
    finally:
        for number, handler in installed.items():
            with contextlib.suppress(OSError, ValueError):
                signal.signal(number, signal.SIG_DFL if handler is None else handler)


def _stopped_detail(what: str, exc: BaseException) -> str:
    """What a component that raised says, naming the component."""
    if isinstance(exc, ComponentOverdue):
        return str(exc)
    return f"{what} stopped: {type(exc).__name__}: {exc}"


def perform_updates(
    sources: "Sequence[str]",
    *,
    base_url: str,
    include_plugin: bool = True,
    force: bool = False,
    manifest: dict | None = None,
    trigger: update_report.Trigger | None = None,
) -> "dict[str, UpdateOutcome]":
    """`perform_update` for several coding agents at once, by source, in order.

    The CLI's upgrade, the manifest and pi's package run ONCE (`_Prelude`):
    one pass per agent used to repeat all three, `pi update` included. Each
    agent's own plugins (`_plugin_pass`: its marketplace fetch, `plugin update`,
    its skills) then move on threads of their own, at the same time, and each
    pass is recorded and reported in `sources` order, as one after another
    were. The CLI's and pi's lines go to the first agent's answer (pi's to
    pi's own, when it is one of them); a deferral (a live run) answers for all.

    One agent's pass that raises, or runs past `component_deadline()`, fails
    that agent's answer alone (plan A3, I7): recorded and reported as the
    failure it is, while the CLI's step and every other pass finish and report.
    """
    trigger = trigger or update_report.trigger_from_env(update_report.Trigger.MANUAL)
    with _update_turn(manifest, trigger):
        prelude = _update_prelude(
            base_url=base_url, include_plugin=include_plugin, force=force, manifest=manifest, trigger=trigger
        )
        if prelude.deferred is not None:
            return {source: prelude.deferred for source in sources}
        passes = _plugin_passes(sources, include_plugin=include_plugin, prelude=prelude)
        package_harness = _package_harness()
        pi_home = package_harness if package_harness in sources else sources[0] if sources else None
        # What failed the whole run, on every agent's answer: each pass's
        # `ok` carries it, and `--json` sends each agent's lines as its reason.
        res, pi_update = prelude.res, prelude.pi_update
        cli_failure = [f"  {res.message}"] if res is not None and not res.ok else []
        pi_failure = [f"  pi package: {pi_update.detail}"] if pi_update is not None and not pi_update.ok else []
        outcomes: dict[str, UpdateOutcome] = {}
        for index, source in enumerate(sources):
            agent = passes[source]
            lines = [*prelude.lines] if index == 0 else [*cli_failure]
            lines.extend(pi_update.lines if pi_update is not None and source == pi_home else pi_failure)
            if isinstance(agent, BaseException):
                outcomes[source] = _crashed_pass(
                    source, agent, lines, prelude=prelude, base_url=base_url, trigger=trigger
                )
                continue
            outcomes[source] = _finish_pass(
                agent, [*lines, *agent.lines],
                prelude=prelude, include_plugin=include_plugin, base_url=base_url, trigger=trigger,
            )
        _refresh_lifeboat(prelude)
        return outcomes


def _plugin_passes(
    sources, *, include_plugin: bool, prelude: "_Prelude"
) -> "dict[str, _AgentPass | BaseException]":
    """`_plugin_pass` for every source at once, one thread each (each in a copy
    of this context): each source's pass, or what it raised, or
    `ComponentOverdue` once it has run `component_deadline()` (plan A3). A
    thread that cannot start runs its pass here instead."""
    components: dict[str, _Component] = {}
    started: list[_Component] = []
    found: dict = {}
    # From before the first start: a signal while they start stops what did.
    with _stopped_with_the_update(started):
        for source in sources:

            def body(source=source):
                try:
                    return _plugin_pass(source, include_plugin=include_plugin, prelude=prelude)
                finally:
                    _finished(source)

            components[source] = _start(source, body)
            started.append(components[source])
        deadline = time.monotonic() + component_deadline()
        for source, component in components.items():
            found[source] = _outcome_by(component, deadline, _plugins_of(source))
            if isinstance(found[source], ComponentOverdue):
                _finished(source)  # the bar moves on
    return found


def _plugins_of(source: str) -> str:
    """"Codex's plugin update": a component's name, from the registry."""
    return f"{_agent_label(source) or source}'s plugin update"


def _crashed_pass(
    source: str,
    exc: BaseException,
    lines: list[str],
    *,
    prelude: "_Prelude",
    base_url: str,
    trigger: update_report.Trigger,
) -> UpdateOutcome:
    """One agent's pass that raised or ran out of time (`_plugin_passes`): recorded
    and reported as that agent's failure (`_record_crash`), answered like the rest."""
    detail = _stopped_detail(_plugins_of(source), exc)
    _record_crash(source, exc, prelude=prelude, base_url=base_url, trigger=trigger, detail=detail)
    res = prelude.res
    heading = f"{_agent_label(source) or source} plugins:"
    return UpdateOutcome(
        lines=[*lines, heading, f"  ! {detail}"],
        ok=False,
        restart_needed=False,
        problems=[detail],
        run_notes=[*([f"Probe CLI: {res.message}"] if res is not None and not res.ok else [])],
        cli=_cli_line(res),
    )


def _cli_from(res: "updater.CliResult | None") -> str:
    """The CLI version this update started from: the hand-off's (the version
    before this release took the update over, `adopt.cli_result`), else this one."""
    from probe.core import adopt

    return (res.before if res is not None and res.before and adopt.adopted_from() else None) or __version__


def _cli_line(res: "updater.CliResult | None") -> str:
    """"Probe CLI 0.324.0 (updated from 0.323.1)": the CLI's version line."""
    if res is None:
        return f"Probe CLI {__version__}"
    return f"Probe CLI {res.after or __version__}" + (
        f" (updated from {res.before})" if res.changed and res.before else ""
    )


def _perform_update(
    *,
    base_url: str,
    include_plugin: bool,
    force: bool,
    manifest: dict | None,
    trigger: update_report.Trigger,
) -> UpdateOutcome:
    """`perform_update` once its spawner has exited and the wizard lock is held."""
    prelude = _update_prelude(
        base_url=base_url, include_plugin=include_plugin, force=force, manifest=manifest, trigger=trigger
    )
    if prelude.deferred is not None:
        return prelude.deferred
    if prelude.pi_update is not None:
        prelude.lines.extend(prelude.pi_update.lines)
    source = agent_source()
    agent = _plugin_passes([source], include_plugin=include_plugin, prelude=prelude)[source]
    if isinstance(agent, BaseException):
        outcome = _crashed_pass(source, agent, [*prelude.lines], prelude=prelude, base_url=base_url, trigger=trigger)
    else:
        outcome = _finish_pass(
            agent, [*prelude.lines, *agent.lines],
            prelude=prelude, include_plugin=include_plugin, base_url=base_url, trigger=trigger,
        )
    _refresh_lifeboat(prelude)
    return outcome


def _refresh_lifeboat(prelude: _Prelude) -> None:
    """The CLI's step ended ok (current, or moved): the lifeboat and its
    env.json as this release has them (plan fool-proof-updates B4), on every
    path an update takes -- the service's child, a session start's own update
    where no service runs (a pod), `probe update`, a run's end -- with the
    keeper's guards (`keeper.refresh_lifeboat`). A plugin that failed changes
    nothing of it. Never raises."""
    if prelude.deferred is not None or (prelude.res is not None and not prelude.res.ok):
        return
    try:
        from probe.service import keeper

        keeper.refresh_lifeboat()
    except Exception:  # noqa: BLE001 -- the update itself is done
        pass


@dataclass
class _Prelude:
    """What an Update does ONCE, whatever the agents: the run-lock check, the
    manifest, the CLI's own upgrade and pi's package (`_update_pi_package`,
    moved whatever agent runs it). `deferred` is the whole answer when a live
    run holds the upgrade off."""

    lines: list[str]
    res: "updater.CliResult | None" = None
    refused: str = ""
    plugin_target: str | None = None
    tap_target: str | None = None
    cli_target: str | None = None
    pi_update: "_PiUpdate | None" = None
    deferred: "UpdateOutcome | None" = None


@dataclass
class _AgentPass:
    """One coding agent's own plugin update (`_plugin_pass`): what it ran and
    what it printed. Built from the agent's source alone, so several agents'
    passes can run at once (`perform_updates`)."""

    source: str
    lines: list[str]
    pres: "updater.PluginResult | None" = None
    plugins_moved: bool = False
    restart_needed: bool = False
    tap_behind: str = ""
    nothing_installed: bool = False
    #: `UpdateOutcome.summary`, `.problems` and `.actions`.
    summary: str = ""
    problems: list[str] = field(default_factory=list)
    actions: list[str] = field(default_factory=list)


def _update_prelude(
    *,
    base_url: str,
    include_plugin: bool,
    force: bool,
    manifest: dict | None,
    trigger: update_report.Trigger,
) -> _Prelude:
    """The once-per-run half of `_perform_update` (`_Prelude`)."""
    lines: list[str] = []
    # Loaded before the CLI's step can replace the files they come from (an
    # in-place upgrade): the lifeboat's refresh at the end runs this code.
    with contextlib.suppress(Exception):
        from probe.service import keeper, lifeboat  # noqa: F401

    # THE RUN-LOCK CHECK IS UNCONDITIONAL, and deliberately outside the wait in
    # `perform_update`. It used to sit inside it, which meant it only ran for
    # spawns that named a parent -- and the plugin's SessionStart hook does not: it runs
    # `probe wizard --action update --yes`, which lands here with no parent pid
    # and would have upgraded straight through a live training run. The hook is
    # the OLDEST caller of this function, so scoping the check to the new one
    # protected everything except the path that already existed.
    #
    # For the spawned path this is also a RE-check: the gate that allowed the
    # spawn ran before the wait, and a run started during it must not be
    # upgraded into by a decision made minutes earlier.
    # The Probe service decided to update past a live run (24 h of deferral,
    # plan D33) and says so: that decision stands here too.
    # Nor when it must update beside the running version (plan D6): a run keeps
    # its own files then, and the service let it go on for that reason.
    # Without a service the same day applies (C3, `autoupdate.defer_for_run`):
    # a run held this update off for 24 h without a break, so it goes on.
    from probe.service.protocol import DeferReason  # loaded already, by `updater`

    deferred = False
    if (
        not force
        and not forced_past(DeferReason.RUN_IN_FLIGHT)
        and os.environ.get(updater.REQUIRE_SIDE_BY_SIDE_ENV) != "1"
    ):
        try:
            from probe.cli import run_lock

            if run_lock.any_live() and autoupdate.defer_for_run(trigger=trigger.value):
                # Not a training loop: this is the updater, so the skip it just
                # recorded can go to the server now.
                update_report.flush(base_url)
                deferred = True
        except Exception:  # noqa: BLE001 -- an unreadable lock must not strand the upgrade
            pass
    if deferred:
        # Deferred, Probe's hooks in Codex are still approved (#3617): Codex
        # rewrites its copies of Probe's plugins by itself, and a day's deferral
        # left Codex unrecorded that long. Outside the check above, whose
        # handler would go on with the upgrade.
        return _Prelude(lines=[], deferred=UpdateOutcome(
            lines=[
                "a run is in flight on this machine; upgrade deferred "
                "(`probe doctor` shows what is holding it)" + updater.approve_codex_hooks_note()
            ],
            ok=True,
            restart_needed=False,
            deferred=True,
        ))

    # A failed manifest fetch must never block the upgrade -- being unable to
    # ask "what is latest" is not a reason to refuse to move.
    json_events.step(json_events.Step.UPDATE_MANIFEST, json_events.Status.STARTED)
    if manifest is None:
        try:
            manifest = updater.fetch_latest(base_url)
        except Exception:  # noqa: BLE001
            manifest = {}
    plugin_target = updater.plugin_latest(manifest)
    tap_target = updater.tap_latest(manifest)
    cli_target = updater.cli_latest(manifest)
    json_events.step(json_events.Step.UPDATE_MANIFEST, json_events.Status.DONE)

    if include_plugin:
        # The pi step runs AFTER the CLI upgrade below has replaced the files
        # it would lazily import, so import them now, from this version.
        # (`probe.harness` is imported at the top: `_agent_label` needs it.)
        from probe.cli import pi_config  # noqa: F401
        from probe.sdk import session_marker  # noqa: F401

    json_events.step(json_events.Step.UPDATE_CLI, json_events.Status.STARTED)
    install = updater.detect_install()
    lines.append(f"Probe Research CLI {__version__}  (installed via: {install.method})")
    from probe.cli import capy_retire

    lines.extend(f"  {line}" for line in capy_retire.retire())

    res: updater.CliResult | None = None
    refused = ""
    if install.method is updater.Method.EPHEMERAL:
        res = _update_persistent_copy(cli_target, lines)
    elif install.method in (
        updater.Method.EDITABLE,
        updater.Method.MANAGED,
        updater.Method.UNKNOWN,
    ):
        # Running a package-manager upgrade against a source checkout or a
        # lockfile-managed environment would trash someone's working tree.
        refused = updater.upgrade_cli(install, __version__, cli_target).message
        lines.append(f"  skipping auto-upgrade: {refused}")
    else:
        if os.environ.get(SKIP_CLI_ENV) == "1":
            # The CLI half is done already: this release took the update over
            # from a hand-off and switched to itself (`probe.core.adopt`), or
            # the Probe service updates the plugins only (the CLI is current
            # and daemon workers run from its env, left as it is: plan D7).
            from probe.core import adopt

            res = adopt.cli_result(__version__) or cli_left_alone(__version__)
        else:
            try:
                with _service_stopped_on_windows(install) as stopped:
                    if stopped:
                        res = updater.upgrade_cli(install, __version__, cli_target)
                    else:
                        res = updater.CliResult(
                            ran=False, ok=False, changed=False, before=__version__, after=__version__,
                            message="CLI upgrade waits: the Probe service did not stop, and Windows cannot "
                                    "replace the files it holds (the next update tries again)",
                        )
            except Exception as exc:  # noqa: BLE001 -- its own failure, never the components' (plan A3)
                res = updater.CliResult(
                    ran=True, ok=False, changed=False, before=__version__, after=__version__,
                    message=f"the CLI upgrade stopped: {type(exc).__name__}: {updater.clean_reason(str(exc))}",
                )
        lines.append(f"  {res.message}")
        if res.changed:
            versions.record_installed_cli(res.after)

    json_events.step(
        json_events.Step.UPDATE_CLI,
        json_events.Status.DONE if res is None or res.ok else json_events.Status.FAILED,
    )
    _finished(UpdatePart.CLI)
    json_events.step(json_events.Step.UPDATE_INTEGRATIONS, json_events.Status.STARTED)
    pi_update: _PiUpdate | None = None
    if include_plugin:
        # pi's Probe package is updated whatever agent runs this: an Update from
        # a plain terminal (claude_code by default) or Claude Code's auto-update
        # used to skip it, so pi stayed on whatever package it was installed
        # with (2026-10-02: a 0.2.x package under a 0.206 CLI, so pi never
        # switched to the daemon). Its own `pi update <source>`, never a
        # marketplace. Once per run, however many agents it updates. In a
        # boundary and a deadline of its own (plan A3): pi failing or hanging
        # fails pi's step alone.
        pi_update = _bounded_pi_update()
    _finished(UpdatePart.PI_PACKAGE)
    return _Prelude(
        lines=lines, res=res, refused=refused, plugin_target=plugin_target, tap_target=tap_target,
        cli_target=cli_target, pi_update=pi_update,
    )


def _plugin_pass(source: str, *, include_plugin: bool, prelude: _Prelude) -> _AgentPass:
    """One agent's marketplace plugins brought up to the manifest (`_AgentPass`).
    Reads nothing of the agent but `source`: no `agent_source()`, no
    process-wide state, so passes for different agents may run at once."""
    lines: list[str] = []
    plugin_target, tap_target = prelude.plugin_target, prelude.tap_target
    plugins_moved = False
    restart_needed = False
    pres: updater.PluginResult | None = None
    tap_behind = ""
    # None of Probe's plugins in this agent, before or after: nothing to update,
    # which is not a failure (`updater.nothing_installed`, the report's rule too).
    nothing_installed = False
    summary = ""
    problems: list[str] = []
    actions: list[str] = []
    if include_plugin:
        # pi has no marketplace plugin: for it `pres` stays None, same bucket as
        # `include_plugin=False`.
        if source != "pi":
            codex = source == "codex"
            kimi = source == plugin_cli.KIMI
            lines.append("Codex plugins:" if codex else "Kimi Code plugins:" if kimi else "Claude Code plugins:")
            pres = (
                updater.update_codex_plugins()
                if codex
                else updater.update_kimi_plugins()
                if kimi
                else updater.update_plugin(plugin_target)
            )
            lines.append(f"  {pres.message}")
            if pres.attempted:
                # Claude Code reads Probe's skills from its own skills folder
                # (copies of the installed plugin's) and re-reads it when it
                # changes: refreshing it now is what gives every open session
                # the new plugin's skill text on its next skill call, instead of
                # whenever a session next starts. A harness that reads the
                # plugin's own folder (Codex, Kimi) has none: a no-op there.
                skills = root_skills.refresh(source)
                lines.extend(f"  {line}" for line in skills)
                problems.extend(line for line in skills if _reports_failure(line))
            # The sessions still running a tap from before this update: the
            # machine reports the oldest live tap, so a current install beside
            # one of them still reads as the old version until it restarts.
            if pres.attempted and pres.tap_after:
                pres = dataclasses.replace(
                    pres, tap_running_stale=updater.stale_tap_daemons(source, pres.tap_after)
                )
            # "No restart needed" only where it is true (Claude Code or Codex,
            # a user-scope install, a tap with the hand-back, every old session
            # movable): everywhere else the restart line, as before.
            pres = dataclasses.replace(pres, follows=updater.follows_without_restart(source, pres))
            # THE TAP'S OWN LINE, so all three versions are on screen (the CLI's
            # is above). It is a separate plugin, and "updated the plugin" said
            # nothing about it while it sat a version behind.
            if pres.attempted:
                tap_line, behind = updater.tap_verdict(pres, tap_target)
                lines.append(f"  {tap_line}")
                tap_behind = tap_line if behind else ""
            if pres.confirmed and (pres.changed or updater.tap_changed(pres)):
                plugins_moved = pres.follows
                restart_needed = not pres.follows
            nothing_installed = updater.nothing_installed(pres, source)
            # A machine that cannot run git would fail these the same way; the
            # failure printed above already says what to run first. Nor when
            # there was nothing to update: those commands would fail the same.
            plugin_failed = not pres.confirmed and not nothing_installed
            if plugin_failed:
                problems.append(pres.message)
            elif tap_behind:
                problems.append(tap_behind.strip())
            elif pres.attempted and not pres.follows and (stale := updater.running_stale_note(pres)):
                # Installed and current, but sessions still run an older tap:
                # something to do, not a failure.
                actions.append(stale)
            if (plugin_failed or tap_behind) and not pres.git_blocked:
                agent = "Codex" if codex else "Kimi Code" if kimi else "Claude Code"
                manual = (
                    updater.manual_codex_plugin_commands()
                    if codex
                    else updater.manual_kimi_plugin_commands()
                    if kimi
                    else updater.manual_plugin_commands()
                )
                # Followed once updated by hand only with the tap it would get.
                follows = updater.follows_without_restart(
                    source, pres, tap_after=tap_target or pres.tap_after, predicting=True
                )
                heading = (
                    f"update them manually ({agent} needs no restart):" if follows
                    else f"update them manually, then restart {agent}:"
                )
                lines.append(f"  {heading}")
                lines.extend(f"    {line}" for line in manual.split("\n"))
                problems += [heading[0].upper() + heading[1:], *(f"  {line}" for line in manual.split("\n"))]
            if pres.confirmed and not nothing_installed:
                summary = _versions_summary(pres)
    return _AgentPass(
        source=source, lines=lines, pres=pres, plugins_moved=plugins_moved,
        restart_needed=restart_needed, tap_behind=tap_behind, nothing_installed=nothing_installed,
        summary=summary, problems=problems, actions=actions,
    )


def _reports_failure(line: str) -> bool:
    from probe.cli import setup as wizard

    return wizard.reports_failure(line.strip())


def _versions_summary(pres: "updater.PluginResult") -> str:
    """"plugin 0.180.0 (updated), tap 0.10.23": where a confirmed pass left
    the plugins. Claude Code's `after` is the plugin's version; Codex's and
    Kimi Code's name each plugin (`name=version, ...`)."""
    named = dict(part.split("=", 1) for part in (pres.after or "").split(", ") if "=" in part)
    plugin = next((v for n, v in named.items() if n != "probe-research-tap"), None) if named else pres.after
    parts = []
    if plugin:
        parts.append(f"plugin {plugin}{' (updated)' if pres.changed else ''}")
    if pres.tap_after:
        parts.append(f"tap {pres.tap_after}{' (updated)' if updater.tap_changed(pres) else ''}")
    return ", ".join(parts)


def _finish_pass(
    agent: _AgentPass,
    lines: list[str],
    *,
    prelude: _Prelude,
    include_plugin: bool,
    base_url: str,
    trigger: update_report.Trigger,
) -> UpdateOutcome:
    """One agent's pass recorded (`probe doctor`'s attempt, the server's report)
    and answered, from the run's `prelude` and the agent's own `agent` pass."""
    source, pres, tap_behind = agent.source, agent.pres, agent.tap_behind
    nothing_installed = agent.nothing_installed
    res, refused, pi_update = prelude.res, prelude.refused, prelude.pi_update
    cli_target, plugin_target, tap_target = prelude.cli_target, prelude.plugin_target, prelude.tap_target

    # `attempted` is what separates "the plugin update failed" from "there was no
    # Claude Code to update" -- a CLI-only user has no `claude` on PATH, and
    # recording that as a failure every session would train everyone to ignore
    # the one line that is supposed to mean something. `nothing_installed` is
    # the same for an agent that IS here with no Probe plugin in it: its update
    # command fails because there is nothing to update.
    #
    # A tap still behind the manifest after the run fails the plugin half too:
    # it is installed, `claude` was asked to move it, and it did not. So does a
    # tap the run removed (`tap_verdict`).
    #
    # EVERY way this half fails has a component in the server's report that
    # says so (`update_report`'s rules read the same facts); a pass that failed
    # with every component reading fine is what this used to send.
    plugin_ok = (
        True if pres is None else (pres.confirmed or not pres.attempted or nothing_installed)
    ) and not tap_behind
    if pres is not None and not pres.confirmed and not nothing_installed:
        plugin_detail = pres.message
    else:
        # Sessions on an older tap are not a failure, but `probe doctor` is
        # where a person looks, so the local record says it too.
        plugin_detail = tap_behind or (updater.running_stale_note(pres) if pres else "")
    # pi's package is the plugin half for pi: an attempted update that failed
    # fails it, or a detached run (pi's session start) would report success.
    if pi_update is not None and not pi_update.ok:
        plugin_ok = False
        plugin_detail = "; ".join(part for part in (plugin_detail, pi_update.detail) if part)
    plugin_version = pres.after if pres is not None else None
    json_events.step(
        json_events.Step.UPDATE_INTEGRATIONS,
        json_events.Status.DONE if plugin_ok else json_events.Status.FAILED,
    )
    json_events.step(json_events.Step.VERIFY_UPDATE, json_events.Status.STARTED)

    # The ONLY way a detached auto-update can report failure: it runs with no
    # terminal attached, so without this an updater that has been broken for a
    # month is indistinguishable from one that works. `probe doctor` prints it.
    # BOTH halves are recorded -- the plugin's outcome used to live only in
    # `lines`, which a detached run sends straight to /dev/null.
    attempted_at = int(time.time())
    autoupdate.record_attempt(
        autoupdate.Attempt(
            at=attempted_at,
            # No `res` means the install method was one we refuse to auto-upgrade.
            # That is a deliberate skip, not a failure.
            ok=res.ok if res is not None else True,
            detail="" if res is None or res.ok else res.message,
            # The version the machine ran before: a hand-off's (`adopt.cli_result`)
            # when this release took the update over, else this one.
            from_version=_cli_from(res),
            # A failure with no observed version records none: falling back to
            # the manifest's latest printed "FAILED ... still at CLI <latest>".
            to_version=(
                cli_target if res is None else res.after or (cli_target if res.ok else None)
            ),
            plugin_ok=plugin_ok,
            plugin_detail=plugin_detail,
            plugin_version=plugin_version,
        ),
        agent=_agent_label(source),
    )
    ok = (res.ok if res is not None else True) and plugin_ok

    # The same outcome, to the server, per component -- the local record above
    # is read by `probe doctor` on THIS machine only. Best-effort and bounded;
    # see update_report.
    _report_attempt(
        lambda: update_report.attempt_report(
            trigger=trigger,
            ok=ok,
            at=attempted_at,
            source=source,
            cli=update_report.cli_component(
                res, current=__version__, target=cli_target, refused=refused
            ),
            # No marketplace plugin ran (`pres`) although plugins were asked
            # for: pi, whose package IS its plugin half. On another agent's
            # pass pi's package moves too, and its failure fails the pass, so
            # it is named there as well (`plugin_half`).
            plugin=(
                update_report.pi_component(pi_update, target=plugin_target)
                if include_plugin and pres is None
                else update_report.plugin_half(
                    update_report.plugin_component(pres, target=plugin_target, source=source),
                    update_report.pi_component(
                        pi_update, target=plugin_target, harness=_package_harness()
                    )
                    if pi_update is not None and not pi_update.ok
                    else None,
                )
            ),
            tap=update_report.tap_component(pres, target=tap_target),
            legacy_ids=pres.legacy_ids if pres is not None else (),
        ),
        base_url=base_url,
    )

    json_events.step(json_events.Step.VERIFY_UPDATE, json_events.Status.DONE)
    summary, problems, actions = agent.summary, list(agent.problems), list(agent.actions)
    pi_failure = ""
    if pi_update is not None and not pi_update.ok:
        # Its own line under "pi package:", which carries the command to run.
        said = [line.strip().removeprefix("! ").strip() for line in pi_update.lines[1:] if line.strip()]
        pi_failure = f"pi's Probe package: {said[0] if said else pi_update.detail}"
    pi_action = pi_update.action if pi_update is not None else ""
    if source == _package_harness() and pi_update is not None:
        if pi_update.ok and pi_update.after:
            moved = pi_update.ran and pi_update.before not in (None, pi_update.after)
            summary = f"package {pi_update.after}{' (updated)' if moved else ''}"
        problems += [pi_failure] if pi_failure else []
        actions += [pi_action] if pi_action else []
    return UpdateOutcome(
        lines=lines,
        # Both halves, so `probe update`'s exit code means "the update worked",
        # not "the CLI half worked".
        ok=ok,
        restart_needed=agent.restart_needed,
        plugins_moved=agent.plugins_moved,
        summary=summary,
        problems=problems,
        actions=actions,
        # pi's package moves whatever agents run (`_update_pi_package`): its
        # failure (and what its sessions must do: `run_actions`) is the run's,
        # and pi's own where pi is one of them (the summary names each once).
        run_notes=[
            *([f"Probe CLI: {res.message}"] if res is not None and not res.ok else []),
            *([pi_failure] if pi_failure else []),
        ],
        run_actions=[pi_action] if pi_action else [],
        cli=(
            f"Probe CLI {res.after or __version__}"
            + (f" (updated from {res.before})" if res.changed and res.before else "")
            if res is not None
            else f"Probe CLI {__version__}"
        ),
    )


def _record_crash(
    source: str,
    exc: BaseException,
    *,
    prelude: _Prelude,
    base_url: str,
    trigger: update_report.Trigger,
    detail: str | None = None,
) -> None:
    """A pass that raised (or ran out of time), recorded as the failure it is
    (`probe doctor`'s attempt, the server's report). The run's one merged
    record reads only what its passes recorded, so without this an Update
    whose Codex pass crashed beside a Claude Code pass that worked said ok.
    Never raises."""
    res, cli_target = prelude.res, prelude.cli_target
    detail = detail or f"the update stopped: {type(exc).__name__}: {exc}"
    at = int(time.time())
    try:
        autoupdate.record_attempt(
            autoupdate.Attempt(
                at=at,
                ok=res.ok if res is not None else True,
                detail="" if res is None or res.ok else res.message,
                from_version=_cli_from(res),
                to_version=cli_target if res is None else res.after or (cli_target if res.ok else None),
                plugin_ok=False,
                plugin_detail=detail,
            ),
            agent=_agent_label(source),
        )
    except Exception:  # noqa: BLE001 - the error itself still rises
        pass
    _report_attempt(
        lambda: update_report.attempt_report(
            trigger=trigger,
            ok=False,
            at=at,
            source=source,
            cli=update_report.cli_component(res, current=__version__, target=cli_target, refused=prelude.refused),
            plugin=update_report.error_component(detail, target=prelude.plugin_target),
            tap=None,
        ),
        base_url=base_url,
    )


def _agent_label(source: str | None) -> str | None:
    """The coding agent a pass ran for, as `probe doctor` names it."""
    try:
        return get_registry().get(source).label if source else None
    except Exception:  # noqa: BLE001 - only a label
        return source


def _report_attempt(build: Callable[[], dict], *, base_url: str | None = None) -> None:
    """Build the server's update report and send it. NEVER RAISES.

    By the time this runs the update is over and recorded locally (`probe
    doctor` reads that record). A bug in building or sending the report may
    cost the report; it must never turn a finished update into a traceback."""
    try:
        update_report.submit_attempt(build(), base_url=base_url)
    except Exception:  # noqa: BLE001 - see docstring
        pass


@dataclass(frozen=True)
class _PiUpdate:
    """What the pi step did: its lines, and whether an ATTEMPTED update failed
    (skipped -- not installed, another update holding the lock -- is not a
    failure)."""

    lines: list[str]
    ok: bool = True
    detail: str = ""
    #: `pi update` actually ran (a skip did not).
    ran: bool = False
    #: For the server's update report only: which of the returns below this
    #: is, and the package versions either side of it.
    code: update_report.PiStep | None = None
    before: str | None = None
    after: str | None = None
    #: What open pi sessions need to run the new package, when they cannot
    #: switch by themselves ("" when they can, or nothing moved).
    action: str = ""


def package_harness() -> str | None:
    """The coding agent whose Probe plugin is a package (pi), not a
    marketplace plugin: its update is `_update_pi_package`'s."""
    return _package_harness()


def _package_harness() -> str | None:
    """The extension-family harness whose package `_update_pi_package` moves
    (pi's), from the registry rather than by name."""
    from probe.harness import FAMILY_EXTENSION, get_registry

    return next(
        (h.id for h in get_registry().installable() if h.family == FAMILY_EXTENSION), None
    )


@contextmanager
def _pi_update_lock():
    """One `pi update` at a time on this machine: two runs on one clone (two
    Claude Code windows' auto-updates and a pi start) race git and npm. Yields
    whether this run holds it; without `fcntl` (Windows) it always does."""
    try:
        import fcntl
    except ImportError:
        yield True
        return
    from probe.sdk import session_marker

    try:
        path = session_marker.state_dir() / "pi-update.lock"
        path.parent.mkdir(parents=True, exist_ok=True)
        handle = open(path, "a+")  # noqa: SIM115 - held across the yield
    except OSError:
        # A lock that cannot be opened is never worth failing the update over.
        yield True
        return
    with handle:
        try:
            fcntl.flock(handle, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except OSError:
            yield False
            return
        try:
            yield True
        finally:
            fcntl.flock(handle, fcntl.LOCK_UN)


def _update_pi_package() -> _PiUpdate:
    """`pi update` for Probe's pi package when pi has it installed; nothing
    otherwise. Says the versions it moved between, or how to do it by hand.

    It runs while pi does, as pi's own `pi update` does. It used to wait until
    no pi process was left, and a researcher running pi agents around the
    clock never got the package at all (strand-ai, 2026-10-15). A running pi
    keeps the extension and capture watcher it loaded: in real pi 1.0.0, with
    the package's `node_modules` deleted and then `pi update`d from 0.4.0 to
    0.5.0 under it, turns, `/probe-status`, `/probe-mcp-login` and the watcher
    process carried on, `/new` started a session, and `/reload` loaded 0.5.0
    (a running session's capture watcher keeps its old code until pi restarts).
    Killed mid-`npm install`, the orphaned npm still finished `node_modules`.
    Only a pi STARTED during the second or two in which `pi update` has removed
    `node_modules` fails to load the package, and exits 1."""
    from probe.cli import pi_config

    directory = pi_config.installed_package_dir()
    if directory is None or not directory.is_dir():
        autoupdate.mark_pi_update_pending(False)
        return _PiUpdate([], code=update_report.PiStep.NOT_INSTALLED)
    with _pi_update_lock() as held:
        if not held:
            return _PiUpdate(
                ["pi package:", "  another update is updating it now"],
                code=update_report.PiStep.LOCKED,
            )
        before = pi_config.installed_package_version()
        # Owed until it is known to have worked: an updater killed mid-update
        # (it removes and reinstalls `node_modules`) is retried, not forgotten.
        autoupdate.mark_pi_update_pending(True)
        result = pi_config.update_package()
        after = pi_config.installed_package_version()

    def shown(version) -> str:
        return ".".join(str(part) for part in version) if version else "unknown"

    versions_seen = {
        "before": shown(before) if before else None,
        "after": shown(after) if after else None,
    }
    if not result.ok and not getattr(result, "reachable", True):
        # pi itself is gone (uninstalled, its settings still naming us): nothing
        # to update with, which is not an update that failed.
        autoupdate.mark_pi_update_pending(False)
        return _PiUpdate(
            ["pi package:", f"  not updated: {result.detail}"],
            code=update_report.PiStep.UNREACHABLE,
            **versions_seen,
        )
    # A failure stays owed, so pi's next session start tries again.
    autoupdate.mark_pi_update_pending(not result.ok)
    if not result.ok:
        return _PiUpdate(
            ["pi package:", f"  ! not updated ({result.detail}); run `pi update {pi_config.MIRROR_GIT_SOURCE}`"],
            ok=False,
            detail=f"pi package not updated: {result.detail}",
            ran=True,
            code=update_report.PiStep.FAILED,
            **versions_seen,
        )
    # The copy open sessions' shims switch to (kimi/pi update parity P1): made
    # from the clone `pi update` just finished; a package from before the shim
    # makes none.
    from probe.cli import pi_pins

    pinned = None
    try:
        pinned = pi_pins.pin_installed()
    except Exception:  # noqa: BLE001 -- no pin: open sessions keep what they run
        pinned = None
    if before != after:
        # One line: the attempt record (`update_owed_pi_package`) and the update
        # report read the last line as what happened.
        harness = _package_harness()
        binary = get_registry().get(harness).binary if harness else None
        follows = bool(pinned is not None and binary and pi_pins.sessions_follow((binary,)))
        if follows:
            follow = "open pi sessions switch to it at their next turn, no restart needed"
        else:
            follow = "run /reload in open pi sessions (or restart them) to apply"
        return _PiUpdate(
            ["pi package:", f"  updated {shown(before)} → {shown(after)} ({follow})"],
            ran=True, code=update_report.PiStep.UPDATED, **versions_seen,
            action="" if follows else "Run /reload in open pi sessions (or restart them) to apply the update.",
        )
    return _PiUpdate(
        ["pi package:", f"  already {shown(after)}"],
        ran=True, code=update_report.PiStep.CURRENT, **versions_seen,
    )


def _bounded_pi_update() -> _PiUpdate:
    """`_update_pi_package` in an exception boundary and a deadline of its own
    (`component_deadline`, plan A3): one that raises or hangs is pi's failed
    step (owed, so pi's next start tries again), never the run's."""
    label = _agent_label(_package_harness())
    what = f"{label}'s package update" if label else "the package update"
    started: list[_Component] = []
    with _stopped_with_the_update(started):
        started.append(_start(UpdatePart.PI_PACKAGE, _update_pi_package))
        found = _outcome_by(started[0], time.monotonic() + component_deadline(), what)
    if isinstance(found, _PiUpdate):
        return found
    detail = _stopped_detail(what, found)
    with contextlib.suppress(Exception):
        autoupdate.mark_pi_update_pending(True)
    return _PiUpdate(
        ["pi package:", f"  ! not updated ({detail})"],
        ok=False,
        detail=f"pi package not updated: {detail}",
        ran=True,
        code=update_report.PiStep.FAILED,
    )


def update_owed_pi_package() -> None:
    """Run ONLY the pi step, for a pi package update that failed
    (`autoupdate.PI_UPDATE_PENDING_FILENAME`) while the CLI itself is current.
    The caller holds the update lock. Records the attempt only when `pi update`
    ran: a skip is not news, and overwriting `last_attempt` with it would hide
    the real one."""
    step = _bounded_pi_update()
    if not step.ran:
        return
    attempted_at = int(time.time())
    autoupdate.record_attempt(
        autoupdate.Attempt(
            at=attempted_at,
            ok=True,
            from_version=__version__,
            plugin_ok=step.ok,
            plugin_detail=step.detail or f"pi package {step.lines[-1].strip()}",
        )
    )
    # Only pi's step ran: no CLI or tap half to report. pi's session start or a
    # run's end asked for it; the spawner's TRIGGER_ENV says which.
    _report_attempt(
        lambda: update_report.attempt_report(
            trigger=update_report.trigger_from_env(update_report.Trigger.SESSION_START),
            ok=step.ok,
            at=attempted_at,
            source=_package_harness(),
            cli=None,
            plugin=update_report.pi_component(step, target=None),
            tap=None,
        )
    )


def _update_persistent_copy(cli_target: str | None, lines: list[str]) -> updater.CliResult | None:
    """Bring the persistent install up to date from a temporary (npx/uvx) run.

    This environment is discarded on exit, so there is nothing here to upgrade:
    the persistent install is what matters. Each outcome is said outright. This
    used to print "upgrading your installed copy instead" and then nothing,
    because bootstrap has no message for "already current", which read as the
    upgrade having silently failed.

    None means nothing needed doing; otherwise the outcome to record.
    """
    from probe.cli import bootstrap

    from probe.cli import install_pipeline

    # Finishes an uninstall that stopped halfway only for an update a person asked for.
    boot = bootstrap.ensure_persistent_install(target=cli_target,
                                               finish_uninstall=install_pipeline.update_may_finish())
    if boot.already_persistent:
        # Bootstrap proves only that the installed copy is at least THIS one, and
        # a uvx/pipx cache can serve a stale copy: compare with the latest too.
        installed = bootstrap.installed_version() or __version__
        if not updater.is_newer(cli_target, installed):
            lines.append(
                "  running from a temporary environment — your installed copy is "
                f"already {installed}, nothing to upgrade"
            )
            versions.record_installed_cli(installed)
            return None
        lines.append(
            "  running from a temporary environment — upgrading your installed copy "
            f"({installed} → {cli_target})"
        )
        # The version itself, never `@latest`: the one installer puts a known
        # version beside the running one (`install_pipeline`).
        boot = bootstrap.install_persistent(f"{bootstrap.INSTALL_SPEC}=={cli_target}")
    else:
        lines.append("  running from a temporary environment — installing a permanent copy")
    # Installer output, shown and (on failure) stored: scrubbed once for both.
    said = updater.clean_reason(boot.message) if boot.message else ""
    if said:
        lines.append(f"  {said}")
    if not boot.installed or getattr(boot, "waiting", False):
        # A failed install was recorded as a success: `probe doctor` said
        # "success -> CLI <latest>" and `probe update` exited 0. One that
        # waits for a quiet machine to switch over is not done either.
        return updater.CliResult(True, False, False, __version__, None, said)
    after = bootstrap.installed_version()
    versions.record_installed_cli(after)
    if not after:
        message = "installed, but no `probe` could be found to confirm its version"
    elif updater.is_newer(cli_target, after):
        message = f"the installed copy is still {after} after installing {cli_target}"
    else:
        return updater.CliResult(True, True, True, __version__, after, "")
    # On screen too: "Installed `probe`" alone read as the upgrade landing.
    lines.append(f"  {message}")
    return updater.CliResult(True, False, True, __version__, after, message)
