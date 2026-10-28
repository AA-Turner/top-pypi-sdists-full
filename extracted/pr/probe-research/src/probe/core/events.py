"""`probe wizard --json` and `python -m probe.core.run`: the events a program reads.

The desktop app runs its own onboarding screens and makes every change through
`probe wizard` (and `probe install`) with `--json`, reading stdout one line at
a time; the Probe service runs the same actions as `probe.core.run` children
and reads the same lines. So while a run writes events, stdout carries ONLY
these: one JSON object per line, flushed as it is written, each with
``"v": 1`` and an ``"event"`` naming its kind.

This module was `probe.cli.json_events`, which is now this same module object
(`probe/cli/json_events.py`), so both names share one run and one set of
globals. It imports nothing heavy at module level: `import probe.core` must not
pull in typer or the CLI (`tests/test_core_run.py` pins it).

    step                 {name, status, message, agent}
    device_prompt        {verification_uri, verification_uri_complete, user_code, expires_in}
    onboarding_required  {url}
    result               {action, agents: [{agent, requested, actual, ok, message}], complete, reason?}
    error                {code, message}
    done                 {ok, complete, exit_code, steps}

`done` is the last line however the run ends -- arguments that do not parse,
SIGINT, SIGTERM and SIGHUP included; only SIGKILL (or a power cut) ends a run
without one. `--help` is not a run: it prints the help text, and no events.
`complete` is False when the persistent CLI install failed, a step failed or
was skipped (a plugin that could not be verified included), a result row is
not ok, or the account still has to finish onboarding on the website -- a run
can exit 0 and still be incomplete. A failed marketplace refresh is written as
`done` ("used the copy already on this machine (refresh failed: ...)"): the run
installs from the copy on disk, and a plugin that cannot install from it fails
its own step. `step.agent` and `result.agents[].agent`
are null for what belongs to the device rather than one coding agent (the
sign-in). `result.reason` is there only when the action set one
(`set_reason`): `probe uninstall`'s machine-readable why of an exit 2 or 1,
`{code, resumed, ...}` (`probe.cli.uninstall.Reason`). Change this only by
adding fields; anything else bumps `SCHEMA_VERSION`.

Signals (`session`, main thread only). SIGINT stops a run only while it waits
for a browser approval (`interruptible`), when nothing is being written: the
run ends there with `error{code: interrupted}` and exit 130. Everywhere else
SIGINT is ignored, and child processes inherit that, so it can never land in
the middle of a config write or a `claude plugin install`. SIGTERM and SIGHUP
stop the run wherever it is, through its `finally` blocks, so it still writes
`done` (exit 143 and 129, `error{code: interrupted}`); a child process running
at that moment is killed too (`subprocess.run` kills its child on any
exception). To cancel a run safely, send SIGINT.

Everything else a run prints -- the wizard's own text, `typer.echo`, and child
processes, which write to file descriptor 1 directly -- goes to stderr:
`session` keeps a private copy of the real stdout for the events and points fd 1
and `sys.stdout` at stderr. That is ONE mechanism for every action, so no print
anywhere in the wizard can corrupt the stream, and nothing needs an `if json:`.
The text on stderr is the same text the terminal shows, kept for an error screen.

Without `--json` every function here returns at once: the terminal output is
byte-identical to a run without this module.

An in-process caller can take the events itself (`session(True, sink=...)`):
each one is handed over as the dict a reader would parse from its line, and
everything else about the run (fd 1 on stderr, the signals, `done` last) is
the same as on the wire.
"""

from __future__ import annotations

import json
import os
import signal
import sys
import threading
from collections.abc import Callable, Iterator, Sequence
from contextlib import contextmanager
from dataclasses import dataclass, field
from typing import Any, TextIO

from probe._compat import StrEnum

#: Takes each event, as the dict its NDJSON line parses to.
EventSink = Callable[[dict], None]

#: Bumped only for a change a reader written against the old shape would misread.
SCHEMA_VERSION = 1

#: The exit status of a run stopped by SIGINT, as a shell reports one (128 + 2).
INTERRUPTED_EXIT_CODE = 128 + int(signal.SIGINT)

#: The signals that stop a json run wherever it is (`_stop`). SIGHUP is POSIX only.
_STOP_SIGNALS: tuple[int, ...] = tuple(
    getattr(signal, name) for name in ("SIGTERM", "SIGHUP") if hasattr(signal, name)
)
#: SIGINT and, on Windows, SIGBREAK (what `action.cancel`'s CTRL_BREAK arrives
#: as): ignored for a json run except inside `interruptible`. Its default
#: action there ends the process, which would cut short a credentials write.
_INTERRUPT_SIGNALS: tuple[int, ...] = tuple(
    getattr(signal, name) for name in ("SIGINT", "SIGBREAK") if hasattr(signal, name)
)


class Event(StrEnum):
    STEP = "step"
    DEVICE_PROMPT = "device_prompt"
    ONBOARDING_REQUIRED = "onboarding_required"
    RESULT = "result"
    ERROR = "error"
    DONE = "done"


class Status(StrEnum):
    STARTED = "started"
    DONE = "done"
    FAILED = "failed"
    SKIPPED = "skipped"


class ErrorCode(StrEnum):
    #: Another `probe wizard` holds the run lock (`wizard_lock`): nothing changed.
    BUSY = "busy"
    #: The arguments were refused: nothing changed.
    USAGE = "usage"
    FAILED = "failed"
    #: Stopped by a signal: SIGINT during a browser approval (exit 130), or
    #: SIGTERM / SIGHUP anywhere (143, 129).
    INTERRUPTED = "interrupted"


class Step(StrEnum):
    """A step's stable name. Its `message` is the human wording, which changes."""

    PERSISTENT_INSTALL = "persistent_install"
    SIGN_IN = "sign_in"
    REFRESH_MARKETPLACE = "refresh_marketplace"
    TRACKING_PLUGIN = "tracking_plugin"
    REINSTALL_INTEGRATION = "reinstall_integration"
    REMOVE_SKILLS = "remove_skills"
    CODEX_MCP_LOGIN = "codex_mcp_login"
    MCP_TOKEN_SYNC = "mcp_token_sync"
    CAPTURE = "capture"
    CODEX_HOOKS_TRUST = "codex_hooks_trust"
    AUTO_UPDATE = "auto_update"
    AGENT_RULES = "agent_rules"
    STATUSLINE = "statusline"
    #: The verdict: the plugins asked for are installed. Skipped when the agent's
    #: own CLI could not be asked, which is not a finding either way.
    VERIFY_PLUGINS = "verify_plugins"
    UPDATE_MANIFEST = "update_manifest"
    UPDATE_CLI = "update_cli"
    UPDATE_INTEGRATIONS = "update_integrations"
    VERIFY_UPDATE = "verify_update"
    #: `probe repair` (plan clean-uninstall-reinstall R-T6): the CLI's env and
    #: command, the OS keeper and lifeboat, the service, the credentials held
    #: to the sign-in, and each agent's integrations.
    REPAIR_CLI = "repair_cli"
    KEEPER = "keeper"
    SERVICE = "service"
    IDENTITY = "identity"
    REPAIR_INTEGRATIONS = "repair_integrations"
    #: `probe uninstall`'s phases (`probe.cli.uninstall`), in order. The last,
    #: `uninstall_finish`, is written by the finisher the CLI becomes
    #: (`probe/_shared/finisher.py`), which also writes `result` and `done`.
    UNINSTALL_SCOPE = "uninstall_scope"
    UNINSTALL_PLAN = "uninstall_plan"
    UNINSTALL_STOP = "uninstall_stop"
    UNINSTALL_DRAIN = "uninstall_drain"
    UNINSTALL_SERVER = "uninstall_server"
    UNINSTALL_INTEGRATIONS = "uninstall_integrations"
    UNINSTALL_STATE = "uninstall_state"
    UNINSTALL_FINISH = "uninstall_finish"


def _usage_error(typer: Any) -> type[BaseException]:
    """Click's UsageError. Typer vendors its own click, so `import click` would
    catch nothing it raises: resolved from BadParameter's MRO, exactly as
    `probe.cli.main` does. Asked for only inside `session`, which imports typer
    then, so importing this module never does."""
    return next(
        (base for base in typer.BadParameter.__mro__ if base.__name__ == "UsageError"),
        type("_NoUsageError", (Exception,), {}),
    )


@dataclass
class _Run:
    out: TextIO
    #: An in-process reader (`session(sink=...)`): it gets each event instead of `out`.
    sink: EventSink | None = None
    #: The last status of each (step, agent), in the order the steps first ran.
    steps: dict[tuple[str, str | None], dict] = field(default_factory=dict)
    action: str | None = None
    #: The agents the action set out to change, so one it never reached (an
    #: earlier agent's failure ends a multi-agent configure) still gets a row.
    planned: list[str | None] = field(default_factory=list)
    rows: dict[str | None, dict] = field(default_factory=dict)
    #: Why the action ended as it did, for a program (`set_reason`); None: not said.
    reason: dict | None = None
    incomplete: bool = False
    errored: bool = False
    broken: bool = False
    #: This session set the process's signal handlers (`_owned_signals`): only
    #: the main thread can, so a run on another thread keeps the defaults.
    owns_signals: bool = False
    #: The signal that is ending the run, once one has (`_interrupt`, `_stop`).
    stopped_by: int | None = None


_run: _Run | None = None


def enabled() -> bool:
    """Whether this process is writing events (`--json`)."""
    return _run is not None


def emit(event: dict) -> None:
    """Write one event as one flushed line. A reader that went away (a closed
    pipe) loses the events, never the run: a half-applied install is worse."""
    run = _run
    if run is None or run.broken:
        return
    try:
        line = json.dumps({"v": SCHEMA_VERSION, **event})
    except ValueError:
        run.broken = True
        return
    if run.sink is not None:
        # The dict a reader parses from the line, never the live one: what the
        # sink sees is exactly what the wire would carry.
        try:
            run.sink(json.loads(line))
        except Exception:  # noqa: BLE001 - the caller's reader, never the run
            run.broken = True
        return
    try:
        run.out.write(line + "\n")
        run.out.flush()
    except (OSError, ValueError):
        run.broken = True


def step(name: Step, status: Status, message: str = "", *, agent: str | None = None) -> None:
    run = _run
    if run is None:
        return
    record = {"name": str(name), "status": str(status), "message": message, "agent": agent}
    run.steps[(record["name"], agent)] = record
    emit({"event": Event.STEP.value, **record})


def persistent_install(result: Any) -> None:
    """The bootstrap's outcome (`bootstrap.BootstrapResult`) as its step: an
    install that leaves no persistent `probe` behind is not a finished one."""
    if _run is None:
        return
    ok = bool(result.installed or result.already_persistent)
    step(Step.PERSISTENT_INSTALL, Status.DONE if ok else Status.FAILED, result.message or "")


def device_prompt(prompt: Any) -> None:
    """A browser approval about to be polled for (`probe.sdk.device.DevicePrompt`)."""
    emit(
        {
            "event": Event.DEVICE_PROMPT.value,
            "verification_uri": prompt.verification_uri,
            "verification_uri_complete": prompt.verification_uri_complete,
            "user_code": prompt.user_code,
            "expires_in": getattr(prompt, "expires_in", None),
        }
    )


def onboarding_required(url: str | None) -> None:
    """The account must finish onboarding on the website first. The run exits 0
    as it always has, so only `done.complete` tells a program it did not finish."""
    if _run is None:
        return
    _run.incomplete = True
    emit({"event": Event.ONBOARDING_REQUIRED.value, "url": url})


def begin_result(action: str, agents: Sequence[str | None]) -> None:
    """The action this run performs and the agents it means to change. A `result`
    event is written before `done` once a result has begun."""
    if _run is None:
        return
    _run.action = str(action)
    _run.planned = list(dict.fromkeys(agents))


def agent_result(
    agent: str | None,
    *,
    requested: dict | None,
    actual: dict | None,
    ok: bool,
    message: str = "",
) -> None:
    """One agent's outcome (None: the device's own, like its sign-in). `ok` is
    what the run verified, never what a step claimed."""
    if _run is None:
        return
    _run.rows[agent] = {
        "agent": agent,
        "requested": requested,
        "actual": actual,
        "ok": bool(ok),
        "message": message,
    }


def set_reason(reason: dict) -> None:
    """The `result` event's `reason`: why the action stopped, as data."""
    if _run is None:
        return
    _run.reason = dict(reason)


def error(code: ErrorCode, message: str) -> None:
    if _run is None:
        return
    _run.errored = True
    emit({"event": Event.ERROR.value, "code": str(code), "message": message})


def handover() -> tuple[dict, int | None]:
    """What a process that is about to BECOME another one (`probe uninstall`'s
    finisher, `os.execv`) hands it to end this run's stream: `{action, rows,
    steps, incomplete}` (the `result` rows as `_finish` would write them) and
    the events stream's file descriptor (None: no stream of its own, or no
    run). The new process writes the last events, `done` among them."""
    run = _run
    if run is None:
        return {}, None
    rows = [
        run.rows.get(agent)
        or {"agent": agent, "requested": None, "actual": None, "ok": False, "message": "not attempted"}
        for agent in run.planned
    ]
    rows += [row for agent, row in run.rows.items() if agent not in run.planned]
    tail = {"action": run.action, "rows": rows, "steps": list(run.steps.values()), "incomplete": run.incomplete}
    _flush(run.out)
    try:
        fd = run.out.fileno() if run.sink is None else None
    except (AttributeError, OSError, ValueError):
        fd = None
    return tail, fd


def done_events(*, code: ErrorCode, message: str, exit_code: int) -> None:
    """`error` + `done` for a run that never reached its session: the arguments
    did not parse. Written straight to stdout, where nothing else is printed."""
    with _writing(sys.stdout):
        error(code, message)
        _finish(exit_code)


class _HumanText:
    """`sys.stdout` while events own the real one: stderr, saying it is no
    terminal, so no screen is drawn and no prompt waits on a keystroke that a
    program reading the events cannot send."""

    def __init__(self, stream: TextIO) -> None:
        self._stream = stream

    def isatty(self) -> bool:
        return False

    def __getattr__(self, name: str) -> Any:
        return getattr(self._stream, name)


def _flush(stream: Any) -> None:
    try:
        stream.flush()
    except (AttributeError, OSError, ValueError):  # None, closed, or gone
        pass


def _events_stream(original: Any) -> tuple[TextIO, bool]:
    """A private copy of the real stdout for the events, and whether it is ours
    to close. A stdout with no descriptor (an in-process test runner) is used as
    it is; no stdout at all (`sys.stdout is None`) loses the events, never the run."""
    try:
        return os.fdopen(os.dup(original.fileno()), "w", encoding="utf-8", newline="\n"), True
    except (AttributeError, OSError, ValueError):
        pass
    if original is not None:
        return original, False
    return open(os.devnull, "w", encoding="utf-8"), True  # noqa: SIM115 - closed on the way out


@contextmanager
def redirect_stdout() -> Iterator[TextIO]:
    """Yield the stream events go to; fd 1 and `sys.stdout` point at stderr.

    A caller's `sys.stdout` with no descriptor of its own (an in-process test
    runner) is used for the events as it is; the process's fd 1 still moves, so
    a child process cannot write into either.
    """
    original = sys.stdout
    for stream in (original, sys.__stdout__, sys.stderr):
        _flush(stream)
    events, owned = _events_stream(original)
    saved_fd1: int | None = None
    try:
        saved_fd1 = os.dup(1)
        os.dup2(2, 1)
    except OSError:
        if saved_fd1 is not None:  # the dup worked and the redirect did not
            os.close(saved_fd1)
        saved_fd1 = None
    sys.stdout = _HumanText(sys.stderr)  # type: ignore[assignment]
    try:
        yield events
    finally:
        # While fd 1 still points at stderr: text left in the buffer of the real
        # stdout (`sys.__stdout__`, or a reference taken before the run) lands
        # on stderr now, not on stdout after `done` when the process exits.
        for stream in (sys.stdout, original, sys.__stdout__, sys.stderr):
            _flush(stream)
        sys.stdout = original
        if saved_fd1 is not None:
            try:
                os.dup2(saved_fd1, 1)
            except OSError:
                pass
            finally:
                os.close(saved_fd1)
        try:
            _flush(events)
        finally:
            if owned:
                try:
                    events.close()
                except (OSError, ValueError):
                    pass


def _interrupt(_signum: int, _frame: Any) -> None:
    """SIGINT inside `interruptible`. Once: the next SIGINT is ignored again at
    once, so it cannot cut short the cleanup this one starts."""
    for number in _INTERRUPT_SIGNALS:
        signal.signal(number, signal.SIG_IGN)
    if _run is not None:
        _run.stopped_by = signal.SIGINT
    raise KeyboardInterrupt


def _stop(signum: int, _frame: Any) -> None:
    """SIGTERM or SIGHUP: end the run through its `finally` blocks, so `done`
    is written. Once: every signal is ignored from here until the session ends."""
    _ignore_signals()
    if _run is not None:
        _run.stopped_by = signum
    raise SystemExit(128 + signum)


def _ignore_signals() -> None:
    for number in (*_INTERRUPT_SIGNALS, *_STOP_SIGNALS):
        signal.signal(number, signal.SIG_IGN)


@contextmanager
def _owned_signals() -> Iterator[bool]:
    """The process's signals for a json session: SIGINT ignored (children
    inherit it), SIGTERM and SIGHUP raising `SystemExit` (`_stop`). The previous
    handlers come back on the way out. Only the main thread can set handlers:
    anywhere else this yields False and changes nothing."""
    if threading.current_thread() is not threading.main_thread():
        yield False
        return
    previous: dict[int, Any] = {}
    try:
        for number in _INTERRUPT_SIGNALS:
            previous[number] = signal.signal(number, signal.SIG_IGN)
        for number in _STOP_SIGNALS:
            previous[number] = signal.signal(number, _stop)
    except (OSError, ValueError):
        pass
    try:
        yield bool(previous)
    finally:
        for number, handler in previous.items():
            # None: a handler not set from Python, which can only be put back as the default.
            signal.signal(number, signal.SIG_DFL if handler is None else handler)


@contextmanager
def interruptible() -> Iterator[None]:
    """The one stretch of a json run that SIGINT can end: the wait for a browser
    approval (`probe.sdk.device` wraps its token poll in this). Nothing is
    written while it waits, so stopping there leaves nothing half-done. Outside
    a session, or off the main thread, a no-op."""
    run = _run
    if run is None or not run.owns_signals or threading.current_thread() is not threading.main_thread():
        yield
        return
    previous = signal.signal(signal.SIGINT, _interrupt)
    # Windows: `action.cancel` sends CTRL_BREAK to the child's process group
    # (it cannot send SIGINT there), which arrives as SIGBREAK.
    brk = getattr(signal, "SIGBREAK", None)
    previous_break = signal.signal(brk, _interrupt) if brk is not None else None
    try:
        yield
    finally:
        signal.signal(signal.SIGINT, signal.SIG_IGN if previous is None else previous)
        if brk is not None:
            signal.signal(brk, signal.SIG_IGN if previous_break is None else previous_break)


@contextmanager
def session(enabled: bool, *, sink: EventSink | None = None) -> Iterator[None]:  # noqa: C901 - one exit per way a run ends
    """Own stdout and the signals for one wizard run, and end it with `done`
    however it ends.

    Every exception is re-raised after the events that describe it, with one
    change: an interrupted approval (KeyboardInterrupt) ends as `typer.Exit(130)`,
    because Click would turn it into "Aborted" and exit 1. Nested sessions
    (`install` calls `wizard`, `probe.core` calls `wizard`) share the outer one,
    and its sink.

    `sink`: the events go to it rather than to the real stdout (see the module
    docstring); fd 1 still points at stderr for the run.
    """
    global _run
    if not enabled or _run is not None:
        yield
        return
    # Here, not at the top: every run is the CLI's code, which imports typer
    # anyway, and the module itself stays light.
    import typer

    from probe.sdk import device

    usage_error = _usage_error(typer)
    with redirect_stdout() as out, _owned_signals() as owns_signals:
        _run = _Run(out=out, sink=sink, owns_signals=owns_signals)
        previous_observer = device.set_prompt_observer(device_prompt)
        previous_wait = device.set_approval_wait(interruptible)
        exit_code = 0
        try:
            yield
        except typer.Exit as exc:
            exit_code = int(exc.exit_code or 0)
            raise
        except usage_error as exc:
            exit_code = int(getattr(exc, "exit_code", 2) or 2)
            error(ErrorCode.USAGE, exc.format_message())  # type: ignore[attr-defined]
            raise
        except KeyboardInterrupt:
            exit_code = INTERRUPTED_EXIT_CODE
            error(
                ErrorCode.INTERRUPTED,
                "interrupted while waiting for the browser approval"
                if _run.stopped_by == signal.SIGINT else "interrupted",
            )
            raise typer.Exit(exit_code) from None
        except typer.Abort:
            # Click's own "Aborted" (a prompt that was abandoned): exit status 1.
            exit_code = 1
            error(ErrorCode.FAILED, "aborted")
            raise
        except SystemExit as exc:
            exit_code = exc.code if isinstance(exc.code, int) else (0 if exc.code is None else 1)
            if _run.stopped_by is not None:
                error(ErrorCode.INTERRUPTED, f"stopped by {signal.Signals(_run.stopped_by).name}")
            raise
        except Exception as exc:
            exit_code = 1
            error(ErrorCode.FAILED, f"{type(exc).__name__}: {exc}")
            raise
        finally:
            if owns_signals:
                _ignore_signals()  # nothing cuts `done` short; `_owned_signals` restores them
            device.set_prompt_observer(previous_observer)
            device.set_approval_wait(previous_wait)
            try:
                _finish(exit_code)
            finally:
                _run = None


@contextmanager
def _writing(out: TextIO) -> Iterator[None]:
    global _run
    _run = _Run(out=out)
    try:
        yield
    finally:
        _run = None


def _finish(exit_code: int) -> None:
    run = _run
    if run is None:
        return
    if exit_code != 0 and not run.errored:
        failed = next((row for row in run.rows.values() if not row["ok"]), None)
        error(
            ErrorCode.USAGE if exit_code == 2 else ErrorCode.FAILED,
            (failed["message"] if failed and failed["message"] else f"exited with status {exit_code}"),
        )
    steps = list(run.steps.values())
    # A step that ended failed or skipped (the persistent CLI install included)
    # is work this run did not do, whatever the exit status says.
    unfinished = any(record["status"] in (Status.FAILED, Status.SKIPPED) for record in steps)
    rows_ok = True
    if run.action is not None and (run.planned or run.rows):
        rows = [
            run.rows.get(agent)
            or {"agent": agent, "requested": None, "actual": None, "ok": False, "message": "not attempted"}
            for agent in run.planned
        ]
        rows += [row for agent, row in run.rows.items() if agent not in run.planned]
        rows_ok = all(row["ok"] for row in rows)
        emit(
            {
                "event": Event.RESULT.value,
                "action": run.action,
                "agents": rows,
                "complete": rows_ok and not (run.incomplete or unfinished),
                **({"reason": run.reason} if run.reason is not None else {}),
            }
        )
    emit(
        {
            "event": Event.DONE.value,
            "ok": exit_code == 0,
            "complete": exit_code == 0 and rows_ok and not (run.incomplete or unfinished),
            "exit_code": exit_code,
            "steps": steps,
        }
    )
