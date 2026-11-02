"""`probe uninstall`: Probe off this computer, leaving a clean slate (plan clean-uninstall-reinstall, PR U).

ONE implementation: `probe uninstall`, `probe wizard --action uninstall` (its
menu's Uninstall too) and the desktop app's Uninstall (`probe uninstall --yes
--json`, never a service action) all run `run()`. It goes through phases, each
recorded in the uninstall barrier (`S/uninstall/barrier.json`, S =
`~/.local/state/probe`) BEFORE it starts, so a run that is killed anywhere is
finished by running it again (C8):

    (scope)       who still uses this install, and are we inside a recorded
                  agent session: refuse (exit 2) unless --force (D2 = A)
    (plan)        the exact paths and server ids this uninstall owns
                  (`uninstall_plan`); a server it cannot reach refuses (exit 2)
                  before anything is touched, unless --offline
    planned       install lock taken (held to the very end, through the
                  finisher), plan and barrier written: from here nothing of
                  Probe's starts (`probe.shared.updates.uninstall_barrier`)
    stopping      the keeper's units and the lifeboat FIRST (a deployed v2
                  lifeboat must not fire), then every Probe process
                  (`uninstall_procs`), verified gone
    draining      every outbox sent and every unsent note edit pushed
                  (`uninstall_notes`), bounded (DRAIN_BUDGET_S); what is still
                  unsent (queued writes, unsynced offline runs, transcript
                  queues, note edits) follows D1 = A: asked (delete / save a
                  backup file / cancel), never deleted silently; `--yes` stops
                  (exit 2) unless --discard-unsent
    server        this device's installation rows retired (a DELETE-scope
                  token: the daemon key, else the API token; 404 = done), THEN
                  every attributable credential revoked: each context's API and
                  MCP tokens, the daemon key, every capture key. A key the
                  server only DETACHED (another computer holds it) is reported.
                  The point of no return: from here the barrier stays LIVE
                  until the job is finished
    integrations  every coding agent with a trace of Probe (`uninstall_agents`)
    state         Probe's files for this user on this machine (C1, C4)
    finishing     this process BECOMES the stdlib finisher (`os.execv`, same
                  pid and terminal, run by the base interpreter, the install
                  lock's fd inherited), which deletes the CLI's env
                  generations and shims, then the barrier

Exit codes: 0 done, 2 refused (live users / inside a session / offline /
unsent research; nothing destroyed), 1 partial (the resume command printed).
A cancel or refusal before "server" puts everything back as it was: the
barrier goes, so the service and the keeper come back with the next session.
Only what THIS run wrote is called off (`Run.wrote_barrier`, and the barrier's
pid and start are this process's): a second run that is refused, or stopped
while it waits for the lock, leaves the first one's barrier and plan alone.
A run that RESUMED an earlier one never calls off: how far that one got is
unknown, so its barrier stays LIVE (phase "resuming" until "server") and the
run says the uninstall is half-done and how to finish it.
"""

from __future__ import annotations

import contextlib
import sys

EXIT_DONE = 0
EXIT_PARTIAL = 1
EXIT_REFUSED = 2
#: The barrier's phase while a run that RESUMED an earlier one is before
#: "server": not a reversible phase, so LIVE to every reader whoever wrote it
#: (the earlier run may have got past the point of no return), and not one of
#: PHASES, so a rerun starts again from "stopping".
RESUMING = "resuming"


class Terminated(BaseException):
    """SIGTERM (or SIGHUP) arrived: end the run through its handlers."""

    def __init__(self, signum: int) -> None:
        super().__init__(signum)
        self.signum = signum


def _resume_point(run: Run) -> Phase | None:
    """Where an earlier run stopped, when it must be finished; None to start
    afresh (none, or a stale one before the point of no return, cleared)."""
    from probe.shared.updates import uninstall_barrier as reader
    from probe.cli.install.uninstall import plan as uninstall_plan

    record = reader.read()
    state = reader.state(record)
    if state == reader.State.ABSENT:
        return None
    if state == reader.State.STALE:
        return None  # cleared under the install lock (`_clear_stale_locked`): the reader's contract
    pid = record.get("pid") if isinstance(record, dict) else None
    if _owner_runs(record or {}) and not _is_self(record or {}):
        raise Stop(EXIT_REFUSED, f"probe uninstall: another uninstall is running (pid {pid}); let it finish.",
                   Reason.BUSY, {"pid": pid})
    phase = (record or {}).get("phase")
    if phase not in PHASES:
        # Unreadable, or a phase this release does not know: from the first
        # phase again (every phase can be run twice; what is gone stays gone).
        phase = Phase.STOPPING
    # From here this run finishes an earlier one: it never calls off.
    run.resumed = True
    run.at = Phase(phase)
    plan = uninstall_plan.read()
    if plan is None:
        # Its plan is gone: plan what is here now (the server's rows too,
        # while the server phase is still to run).
        due = PHASES.index(Phase(phase)) <= PHASES.index(Phase.SERVER)
        server = _server_ids(run) if due else {"device_ids": [], "installation_ids": [], "contexts": {}}
        plan = uninstall_plan.compute(server=server)
        uninstall_plan.write(plan)
    run.plan = plan
    return Phase(phase)


@contextlib.contextmanager
def _signals():
    """SIGTERM and SIGHUP end the run through its handlers (`Terminated`), as
    Ctrl-C does: before "server" everything is put back. A `--json` run's
    event session already turns them into SystemExit; it keeps its own."""
    from probe.core import events
    import signal
    import threading

    if events.enabled() or threading.current_thread() is not threading.main_thread():
        yield
        return

    def stop(signum, _frame):
        raise Terminated(signum)

    previous = {}
    for name in ("SIGTERM", "SIGHUP"):
        number = getattr(signal, name, None)
        if number is not None:
            with contextlib.suppress(OSError, ValueError):
                previous[number] = signal.signal(number, stop)
    try:
        yield
    finally:
        for number, handler in previous.items():
            with contextlib.suppress(OSError, ValueError):
                signal.signal(number, signal.SIG_DFL if handler is None else handler)


def _reversible(phase: object) -> bool:
    return phase in PHASES and PHASES.index(Phase(phase)) < PHASES.index(Phase.SERVER)


def _half_done(run: Run, stop: Stop) -> str:
    """A resumed run was refused: the barrier stays (LIVE), nothing is put
    back, and this says so. The way to finish: what the refusal said (the lock
    is held, the server is unreachable), else --discard-unsent only when
    something is unsent, else a rerun."""
    said = "This uninstall is half-done (an earlier run of it stopped partway), so Probe stays stopped until it is finished"
    if stop.reason in (Reason.BUSY, Reason.OFFLINE):
        return f"{said}."
    unsent = run.unsent
    if unsent is not None and unsent.total:
        online = ", or run `probe uninstall` again once online" if unsent.sendable else ""
        return (f"{said}: run `probe uninstall --backup-unsent` (or --discard-unsent) to finish it now"
                f"{online}.")
    return f"{said}: run `probe uninstall` again to finish it."


def _call_off(run: Run) -> str:
    """Before the point of no return, called off (a refusal, a cancel, a
    signal): the barrier goes, the service starts again the way `ensure`
    starts it (and with it the keeper and lifeboat), and what was stopped is
    said. Nothing else this run did lasts (the stop phase changes nothing on
    disk; what was sent stays sent). Returns the line to print."""
    _drop_barrier()
    said = "Nothing was removed."
    if run.stopped:
        said += f" Stopped meanwhile: {', '.join(run.stopped)}."
    if not run.options.embedded:
        with contextlib.suppress(Exception):
            from probe.foundation import service_api as client

            started = client.ensure()
            if started in (client.Ensured.SPAWNED, client.Ensured.STARTING, client.Ensured.RUNNING):
                said += " The Probe service is starting again."
    return said


def run(options: Options) -> int:
    """`probe uninstall`. Returns its exit code, or does not return (the
    finisher took over the process)."""
    from probe.core import events

    if not options.embedded:
        events.begin_result("uninstall", [None])
    state = Run(options=options)
    try:
        with _signals():
            try:
                return _run(state)
            except Stop as stop:
                return _stopped(state, stop)
            except (KeyboardInterrupt, Terminated, SystemExit) as exc:
                return _interrupted(state, exc)
    finally:
        if state.lock_fd is not None:
            from probe.shared.updates import handoff

            handoff.release_lock(state.lock_fd)


def _stopped(state: Run, stop: Stop) -> int:
    from probe.shared.updates import uninstall_barrier as reader
    from probe.core import events

    message = stop.message
    record = reader.read()
    if state.resumed:
        # Never called off: the earlier run's progress is unknown. The barrier
        # stays LIVE (RESUMING until "server").
        if stop.code == EXIT_REFUSED:
            message = f"{message} {_half_done(state, stop)}"
    elif record is None:
        if state.wrote_plan or state.wrote_barrier:
            _drop_barrier()  # stopped before it began: this run's plan goes too
    elif _owns_barrier(state, record) and _reversible(record.get("phase")):
        message = f"{message} {_call_off(state)}"
    print(message, file=sys.stderr if stop.code else sys.stdout)
    if not state.options.embedded:
        events.agent_result(None, requested={"signed_in": False}, actual=None, ok=False, message=message)
        events.set_reason(reason_record(state, stop.reason, stop.detail, stop.code))
    return stop.code


def reason_record(run: Run, reason: Reason | None, detail: dict | None, code: int) -> dict:
    """The `--json` result's `reason`: `{"code", "resumed", ...detail}`. A
    partial run says what finishes it (`resume`, `phase`). `resumed`: this run
    was finishing an earlier one, so a refusal leaves the uninstall half-done
    (nothing is put back)."""
    out = {"code": str(reason or (Reason.PARTIAL if code == EXIT_PARTIAL else Reason.CANCELLED)),
           "resumed": bool(run.resumed), **(detail or {})}
    if out["code"] == Reason.PARTIAL:
        out.setdefault("resume", "probe uninstall")
        out.setdefault("phase", str(run.at) if run.at else None)
    return out


def _interrupted(state: Run, exc: BaseException) -> int:
    """Ctrl-C, SIGTERM or SIGHUP: before "server" called off, as if it never
    began; after it, the barrier stays for `probe uninstall` to finish. Only
    this run's own barrier is called off; a resumed run's never is."""
    from probe.shared.updates import uninstall_barrier as reader

    record = reader.read()
    if state.resumed:
        phase = state.at or "first"
        print(f"probe uninstall: interrupted at its '{phase}' step; run `probe uninstall` again to finish.",
              file=sys.stderr)
        code = EXIT_PARTIAL
    elif record is None or not _owns_barrier(state, record):
        if record is None and (state.wrote_plan or state.wrote_barrier):
            _drop_barrier()  # this run's plan, written before its barrier
        print("probe uninstall: interrupted; nothing was changed.", file=sys.stderr)
        code = EXIT_REFUSED
    elif _reversible(record.get("phase")):
        print(f"probe uninstall: interrupted. {_call_off(state)}", file=sys.stderr)
        code = EXIT_REFUSED
    else:
        print(f"probe uninstall: interrupted at its '{record.get('phase')}' step; run `probe uninstall` again "
              "to finish.", file=sys.stderr)
        code = EXIT_PARTIAL
    if not state.options.embedded:
        from probe.core import events

        events.set_reason(reason_record(state, Reason.PARTIAL if code == EXIT_PARTIAL else Reason.INTERRUPTED,
                                        None, code))
    if isinstance(exc, SystemExit):
        raise exc  # a `--json` run's event session ends it (`done`, interrupted)
    return code


def _clear_stale_locked(run: Run) -> None:
    """Under the install lock (which an uninstall takes before it writes its
    barrier): a STALE barrier left by an earlier run is cleared, and one that
    turned LIVE while this run was asking (another uninstall began, or one
    died past the point of no return) stops this one."""
    from probe.shared.updates import uninstall_barrier as reader

    said = reader.clear_stale()
    if said:
        _say(f"probe uninstall: {said}; starting again.")
    record = reader.read()
    if reader.state(record) == reader.State.LIVE:
        pid = record.get("pid") if isinstance(record, dict) else None
        raise Stop(EXIT_REFUSED, "probe uninstall: another uninstall of Probe began meanwhile; nothing was changed. "
                                 "Run `probe uninstall` again when it ends.", Reason.BUSY, {"pid": pid})


def _run(run: Run) -> int:
    start = _resume_point(run)
    if start is None and run.options.embedded:
        return EXIT_DONE  # the barrier went meanwhile (another run finished it): never a fresh uninstall here
    if start is None:
        if not run.options.yes and not run.options.interactive:
            raise Stop(EXIT_REFUSED, "probe uninstall: nothing was changed: there is no terminal to confirm in. "
                                     "Pass --yes to confirm.", Reason.CONFIRM)
        _scope(run)
        run.agents = list(_all_traces())
        _telemetry_start(run)
        server = _server_ids(run)
        if run.options.interactive:
            _confirm(run)
        _telemetry_pin(run)
        _take_lock(run)
        _clear_stale_locked(run)
        _plan(run, server)
        run.at = Phase.PLANNED
        _write_barrier(run, Phase.PLANNED)
        start = Phase.STOPPING
        _say("Uninstalling Probe from this computer...")
    else:
        _take_lock(run)
        _say(f"Finishing the uninstall of Probe that stopped at its '{start}' step...")
    for phase in PHASES[PHASES.index(start):]:
        run.at = phase
        if phase is Phase.SERVER:
            # Reachable, right before the point of no return (a rerun too):
            # offline, a fresh run is called off and a resumed one waits.
            preflight_server(run)
        try:
            # A resumed run records RESUMING before "server": a barrier saying
            # "stopping" or "draining" would read STALE once it exits, and the
            # earlier run may have got further than that.
            _write_barrier(run, RESUMING if run.resumed and _reversible(phase) else phase)
        except OSError as exc:
            raise Stop(EXIT_PARTIAL, f"probe uninstall: could not record its progress ({exc}).") from None
        if phase is Phase.FINISHING:
            return _phase_finishing(run)
        step = _PHASE_STEPS.get(phase)
        if step is None:
            continue
        try:
            step(run)
        finally:
            run.warnings += sum(1 for line in run.out if str(line).lstrip().startswith("!"))
            _lines(run.out)
            run.out.clear()
    return EXIT_DONE
from probe.cli.install.uninstall.barrier import _drop_barrier, _is_self, _owner_runs, _owns_barrier, _write_barrier  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.cli.install.uninstall.phase import _PHASE_STEPS  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.cli.install.uninstall.phases.finishing import _phase_finishing  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.cli.install.uninstall.phases.server import preflight_server  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.cli.install.uninstall.preparation import _confirm, _plan, _scope, _server_ids, _take_lock  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.cli.install.uninstall.state import Options, PHASES, Phase, Reason, Run, Stop, _lines, _say  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.cli.install.uninstall.telemetry import _all_traces, _telemetry_pin, _telemetry_start  # noqa: E402 -- pieces need each other; the front door loads this one first
