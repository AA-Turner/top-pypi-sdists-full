"""Actions over the service socket: run, recover, cancel (plan X5, A5, R9).

    action.run     check the request, take the one mutating slot (or answer
                   `busy` naming its holder), journal it, answer `{action_id}`
                   BEFORE any work, then run `python -m probe.core.run <action>`,
                   stopped (and failed) past ACTION_TIMEOUT_S (60 min, C1),
                   one an earlier service left running too. While an update
                   holds the slot (a cycle's CLI step, a person's Update) the
                   action is journaled and answered `{action_id, queued: true}`
                   instead, and runs once the update lets go, in the order
                   accepted (`drain`): a setting changed right after the app
                   opens, which starts a cycle, is not refused for it
    action.status  from the journal: queued | running | done (+ the `done` event)
    action.events  the journaled events after `since`, and whether it is done
    action.cancel  SIGINT to the child, only while it waits for a browser
                   approval (its last event is `device_prompt`); else refused.
                   The action counts as cancelled only if the child then exits
                   130: a SIGINT that lands just outside the approval wait is
                   ignored by the child, which finishes as it would have

The journal is `<service dir>/actions/<action_id>.jsonl`, one JSON object per
line, appended as things happen, so a client that lost its connection -- or a
service that restarted -- reads the outcome instead of running it again:

    {"type": "accepted", "v": 1, "action_id", "action", "params", "client_request_id", "accepted_at", "service_pid"}
    {"type": "queued", "at", "holder"}                              (it waited for an update)
    {"type": "child", "pid", "start_time", "at"}
    {"type": "event", "seq": 1.., "event": <NDJSON event v1>}      (`done` last)
    {"type": "cancel", "at"}                                        (a cancel was sent)
    {"type": "ended", "at", "exit_code"}

Every journal ends with a `done` event, whoever wrote it. A child that ended
without one (killed, crashed) gets an `error` and a `done{ok: false}` with its
exit status. A child the service lost -- the service stopped under it -- is
found at the next start: still running, it holds the slot and is watched until
it exits; gone, it reads as `error{interrupted, "service stopped"}` +
`done{ok: false, complete: false, exit_code: null}`. Never as success, and
never run again: `client_request_id` returns the existing `action_id` for 24 h.
A queued action the service stopped before (a signal, a crash: the restart
for a new CLI waits for the queue) reads the same way.

The request's context (plan X2) reaches the child's environment only; it is
never journaled (a proxy URL can carry a password).

Stdlib only at import (the start path; plan S1). Checking `params` uses
`probe.core.requests` (light: no CLI), imported on the first `action.run`.
"""

from __future__ import annotations

import asyncio
import contextlib
import json
import os
import re
import secrets
import signal
import time
from collections.abc import Callable
from dataclasses import dataclass, field
from pathlib import Path

from . import children, loginenv, paths, procid
from .protocol import (
    ACTIONS,
    ORIGIN_DESKTOP,
    REPORT_TRIGGERS,
    Action,
    ActionState,
    BusyHolder,
    ErrorCode,
    RefusedReason,
    ReportTrigger,
    RpcError,
    invalid_params,
)

JOURNAL_VERSION = 1
#: `client_request_id` returns the same action this long (API v1).
DEDUPE_S = 24 * 3600
#: Journals (and their logs) older than this are deleted at start ...
KEEP_S = 7 * 24 * 3600
#: ... and past this many, the oldest are.
MAX_JOURNALS = 200
SERVICE_STOPPED = "service stopped"
#: What asked for an `update` action, for the server's update report (the
#: wizard reads it: `probe.cli.update_report.TRIGGER_ENV`).
TRIGGER_ENV = "PROBE_AUTOUPDATE_TRIGGER"
DESKTOP_HUMAN_ENV = "PROBE_DESKTOP_HUMAN"  # probe._shared.telemetry, kept stdlib-only here
#: `probe.core.events.INTERRUPTED_EXIT_CODE`: a run stopped during its approval wait.
INTERRUPTED_EXIT = 130
#: An action child's wall time, at most (plan C1). Past it the child is stopped
#: (SIGTERM to its process group, SIGKILL past ACTION_STOP_GRACE_S) and the
#: action fails saying so: a child that never returned held the one mutating
#: slot -- and with it every update -- for good. An hour is twice the update
#: child's own limit (`updater.UPDATE_TIMEOUT_S`) and well past a browser
#: approval's wait: a child still running then is hung, not slow.
ACTION_TIMEOUT_S = 60 * 60
#: SIGTERM to SIGKILL: the child's handler (`probe.core.events`) ends the run
#: through its `finally` blocks, its locks let go and `done` written.
ACTION_STOP_GRACE_S = 30.0
#: Actions waiting for an update at once, at most (`run` answers `busy` past it).
MAX_QUEUED_ACTIONS = 16
#: Test-only overrides of the two, read where the manager runs (a service that
#: `client.ensure` starts never gets them: `client.ENV_ALLOWLIST`). Nothing in
#: production sets them.
ACTION_TIMEOUT_ENV = "PROBE_SERVICE_ACTION_TIMEOUT_S"
ACTION_STOP_GRACE_ENV = "PROBE_SERVICE_ACTION_STOP_GRACE_S"
_ACTION_ID = re.compile(r"^act_[0-9a-f]{16}$")

#: NDJSON event kinds (`probe.core.events.Event`).
EVENT_DONE = "done"
EVENT_ERROR = "error"
EVENT_DEVICE_PROMPT = "device_prompt"


def _now() -> float:
    return time.time()


def _env_seconds(name: str, default: float) -> float:
    """A test override of a time limit (ACTION_TIMEOUT_ENV), else `default`."""
    try:
        value = float(os.environ.get(name) or default)
    except ValueError:
        return default
    return value if value >= 0 else default


def _span(seconds: float) -> str:
    """`60 min`, `2 s`: a time limit as a person reads it (`updater.span`)."""
    return f"{seconds / 60:.0f} min" if seconds >= 120 else f"{seconds:g} s"


def done_event(exit_code: int | None) -> dict:
    """A `done` for a run that wrote none itself (events schema v1)."""
    return {"v": 1, "event": EVENT_DONE, "ok": False, "complete": False, "exit_code": exit_code, "steps": []}


def error_event(code: str, message: str) -> dict:
    return {"v": 1, "event": EVENT_ERROR, "code": code, "message": message}


def _is_update(holder: dict | None) -> bool:
    """Is the slot's holder an update: a cycle's CLI step, or a person's Update action?"""
    if holder is None:
        return False
    return holder.get("kind") == BusyHolder.UPDATE or (
        holder.get("kind") == BusyHolder.ACTION and holder.get("action") == Action.UPDATE
    )


def shell_status(returncode: int | None) -> int | None:
    """asyncio's -N (killed by signal N) as a shell reports it, 128 + N."""
    if returncode is None:
        return None
    return 128 - returncode if returncode < 0 else returncode


@dataclass
class Record:
    action_id: str
    action: str
    client_request_id: str
    accepted_at: float
    params: dict = field(default_factory=dict)
    state: str = ActionState.QUEUED
    events: list = field(default_factory=list)  # [(seq, event)]
    ended_at: float | None = None
    exit_code: int | None = None
    child_pid: int | None = None
    child_start: str | None = None
    #: When the child started (its `child` line): a recovered child's time
    #: limit counts from it, not from a wait behind an update.
    child_at: float | None = None
    process: object = None  # our asyncio child, while it runs
    #: A child a previous service started that still ran when this one did.
    orphan: bool = False
    #: `action.cancel` sent it SIGINT.
    cancel_sent: bool = False
    #: Why the service ended it (it ran past ACTION_TIMEOUT_S), kept even when
    #: the child wrote its own `done` as it stopped: the action's error.
    failure: str | None = None

    @property
    def done(self) -> dict | None:
        for _seq, event in reversed(self.events):
            if event.get("event") == EVENT_DONE:
                return event
        return None

    @property
    def last_kind(self) -> str | None:
        return self.events[-1][1].get("event") if self.events else None

    def last_error(self) -> dict | None:
        for _seq, event in reversed(self.events):
            if event.get("event") == EVENT_ERROR:
                return event
        return None

    def public(self) -> dict:
        out: dict = {
            "action_id": self.action_id,
            "action": self.action,
            "state": self.state,
            "started_at": self.accepted_at,
        }
        if self.state == ActionState.DONE:
            done = self.done
            out["done"] = done
            out["ended_at"] = self.ended_at
            # Only the child's own word: it exits 130 when the SIGINT stopped
            # it in its approval wait, and ignores one anywhere else.
            out["cancelled"] = self.cancel_sent and isinstance(done, dict) and done.get("exit_code") == INTERRUPTED_EXIT
            error = error_event("failed", self.failure) if self.failure else self.last_error()
            if error is not None:
                out["error"] = error
        return out


class ActionManager:
    def __init__(
        self,
        *,
        emit: Callable[[str, dict], None],
        changed: Callable[[], None],
        holder: Callable[[], dict | None],
        finished: Callable[[str], None] | None = None,
    ) -> None:
        #: (topic, payload) to subscribers.
        self.emit = emit
        #: Called when an action is queued, starts or ends (the service re-reads what holds it).
        self.changed = changed
        #: What holds the mutating slot service-wide (an action, or an update).
        self.holder = holder
        #: Called with an action's name once it is done (before `changed`).
        self.finished = finished
        self.records: dict[str, Record] = {}
        self.by_request: dict[str, tuple[str, float]] = {}
        self.running: Record | None = None
        #: Accepted while an update held the slot, oldest first: (record, request, env).
        self.queue: list[tuple[Record, dict, dict]] = []
        #: The service is stopping (`close`): nothing queued starts any more.
        self.closed = False
        self._fds: dict[str, int] = {}
        self._tasks: set = set()
        #: The time limits of children an earlier service left running (`_limit_orphan`).
        self._timers: list = []
        self._watch: Callable | None = None

    # -- disk ------------------------------------------------------------------

    def _journal(self, action_id: str) -> Path:
        return paths.actions_dir() / f"{action_id}.jsonl"

    def _log(self, action_id: str) -> Path:
        return paths.actions_dir() / f"{action_id}.log"

    def _write(self, record: Record, line: dict) -> None:
        """Append one line to the action's journal (opened on first use, closed by `_close`)."""
        try:
            fd = self._fds.get(record.action_id)
            if fd is None:
                fd = os.open(
                    self._journal(record.action_id),
                    os.O_WRONLY | os.O_CREAT | os.O_APPEND | getattr(os, "O_NOFOLLOW", 0),
                    0o600,
                )
                self._fds[record.action_id] = fd
            os.write(fd, (json.dumps(line, separators=(",", ":"), ensure_ascii=False) + "\n").encode("utf-8"))
        except OSError:
            pass  # the in-memory record still answers; the client still gets its events

    def _close(self, record: Record) -> None:
        fd = self._fds.pop(record.action_id, None)
        if fd is not None:
            with contextlib.suppress(OSError):
                os.close(fd)

    def load(self, watch: Callable[[object, int, str, Callable[[], None]], None]) -> None:
        """Read what earlier services journaled: the 24 h dedupe index, and
        the actions they never finished. `watch(key, pid, start, callback)`
        is the service's pid watcher."""
        self._watch = watch
        directory = paths.actions_dir()
        try:
            paths.private_dir(directory)
            journals = sorted(directory.glob("*.jsonl"), key=lambda p: p.stat().st_mtime)
        except OSError:
            return
        now = _now()
        loaded: list[Record] = []
        for path in journals:
            record = self._read(path)
            if record is None:
                continue
            loaded.append(record)
        unfinished = [r for r in loaded if r.done is None]
        # Old and surplus journals go, never one that is still unfinished.
        finished = [r for r in loaded if r.done is not None]
        keep = finished[-MAX_JOURNALS:] if len(finished) > MAX_JOURNALS else finished
        for record in finished:
            if record not in keep or now - (record.ended_at or record.accepted_at) > KEEP_S:
                for target in (self._journal(record.action_id), self._log(record.action_id)):
                    with contextlib.suppress(OSError):
                        target.unlink()
            else:
                self._remember(record, now)
        for record in unfinished:
            self._remember(record, now)
            self._recover(record)

    def _remember(self, record: Record, now: float) -> None:
        self.records[record.action_id] = record
        if record.client_request_id and now - record.accepted_at < DEDUPE_S:
            self.by_request[record.client_request_id] = (record.action_id, record.accepted_at)

    def _read(self, path: Path) -> Record | None:
        try:
            lines = path.read_text(encoding="utf-8").splitlines()
        except OSError:
            return None
        record: Record | None = None
        for raw in lines:
            try:
                line = json.loads(raw)
            except ValueError:
                continue  # a torn last line from a crash: what is whole still counts
            if not isinstance(line, dict):
                continue
            kind = line.get("type")
            if kind == "accepted" and record is None:
                action_id = str(line.get("action_id") or "")
                if not _ACTION_ID.match(action_id) or path.stem != action_id:
                    return None
                try:
                    accepted_at = float(line.get("accepted_at") or 0)
                except (TypeError, ValueError):
                    accepted_at = 0.0
                record = Record(
                    action_id=action_id,
                    action=str(line.get("action") or ""),
                    client_request_id=str(line.get("client_request_id") or ""),
                    accepted_at=accepted_at,
                    params=line.get("params") if isinstance(line.get("params"), dict) else {},
                )
            elif record is None:
                return None
            elif kind == "child":
                if isinstance(line.get("pid"), int):
                    record.child_pid = line["pid"]
                    record.child_start = str(line.get("start_time") or "") or None
                    with contextlib.suppress(TypeError, ValueError):
                        record.child_at = float(line.get("at"))
                    record.state = ActionState.RUNNING
            elif kind == "cancel":
                record.cancel_sent = True
            elif kind == "event" and isinstance(line.get("event"), dict):
                record.events.append((len(record.events) + 1, line["event"]))
            elif kind == "ended":
                record.state = ActionState.DONE
                with contextlib.suppress(TypeError, ValueError):
                    record.ended_at = float(line.get("at"))
                code = line.get("exit_code")
                record.exit_code = code if isinstance(code, int) else None
                failure = line.get("failure")
                record.failure = failure if isinstance(failure, str) and failure else None
        if record is not None and record.done is not None:
            record.state = ActionState.DONE
            if record.ended_at is None:
                record.ended_at = record.accepted_at
        return record

    def _recover(self, record: Record) -> None:
        """An action an earlier service never finished: watch its child to
        the end if it still runs, else close it as stopped with the service."""
        pid, start = record.child_pid, record.child_start
        alive = procid.alive(pid, start or "") if pid else False
        if alive is not False and pid and start and self._watch is not None:
            record.orphan = True
            record.state = ActionState.RUNNING
            if self.running is None or record.accepted_at > self.running.accepted_at:
                self.running = record
            self._watch(("action", record.action_id), pid, start, lambda: self._orphan_exited(record))
            self._limit_orphan(record)
            return
        self._finish(record, None, interrupted=SERVICE_STOPPED)

    def _orphan_exited(self, record: Record) -> None:
        if record.failure:
            self._finish(record, None, failed=record.failure)  # this service stopped it
        else:
            self._finish(record, None, interrupted=SERVICE_STOPPED)

    def _limit_orphan(self, record: Record) -> None:
        """A child an earlier service left running gets the same time limit as
        this one's own (ACTION_TIMEOUT_S, C1), counted from the child's start
        (its acceptance, in a journal without one): stopped then, its group with
        it, and the action failed saying why. Never raises; with no running loop
        (a test loading journals) there is none."""
        limit = _env_seconds(ACTION_TIMEOUT_ENV, ACTION_TIMEOUT_S)
        try:
            loop = asyncio.get_running_loop()
        except RuntimeError:
            return
        delay = max(0.0, (record.child_at or record.accepted_at) + limit - _now())

        def due() -> None:
            task = asyncio.ensure_future(self._stop_orphan(record, limit))
            self._tasks.add(task)
            task.add_done_callback(self._tasks.discard)

        self._timers.append(loop.call_later(delay, due))

    async def _stop_orphan(self, record: Record, limit: float) -> None:
        if record.state == ActionState.DONE or not record.orphan or not record.child_pid or not record.child_start:
            return
        from .updater import stop_process  # the service's own, loaded with it

        record.failure = f"the action ran past {_span(limit)} and was stopped"
        await stop_process(
            record.child_pid, record.child_start, _env_seconds(ACTION_STOP_GRACE_ENV, ACTION_STOP_GRACE_S)
        )
        if record.state != ActionState.DONE:
            self._finish(record, None, failed=record.failure)

    # -- requests --------------------------------------------------------------

    def run(self, params: dict, env_extra: dict) -> dict:
        """`action.run`: `{action_id}` once it is journaled, before any work."""
        action = params.get("action")
        if action not in ACTIONS:
            raise invalid_params(f"action must be one of {sorted(ACTIONS)}")
        request = params.get("params", {})
        if request is None:
            request = {}
        if not isinstance(request, dict):
            raise invalid_params("params must be an object")
        trigger = params.get("trigger")
        if trigger is not None and (action != Action.UPDATE or trigger not in REPORT_TRIGGERS):
            raise invalid_params(f"trigger is for the update action only, one of {sorted(REPORT_TRIGGERS)}")
        origin = params.get("origin")
        if origin is not None and origin != ORIGIN_DESKTOP:
            raise invalid_params("origin must be desktop when supplied")
        crid = params.get("client_request_id")
        if not isinstance(crid, str) or not crid or len(crid) > 128:
            raise invalid_params("client_request_id must be a non-empty string of at most 128 characters")
        now = _now()
        known = self.by_request.get(crid)
        if known is not None and now - known[1] < DEDUPE_S and known[0] in self.records:
            return self._existing_answer(known[0])
        from probe.core import requests as core_requests

        try:
            core_requests.parse(action, request)
        except core_requests.RequestError as exc:
            raise invalid_params(str(exc)) from None
        holder = self.holder()
        # Behind an update, or behind actions already waiting for one (they go
        # first); never an Update while an update holds the slot: that is the same work.
        # A stopping service queues nothing: it would never start it.
        updating = _is_update(holder)
        queued = (bool(self.queue) or updating) and not (updating and action == Action.UPDATE) and not self.closed
        if holder is not None and not queued:
            raise RpcError(ErrorCode.BUSY, f"busy: {holder.get('kind')} running", {"holder": holder})
        if queued and len(self.queue) >= MAX_QUEUED_ACTIONS:
            raise RpcError(ErrorCode.BUSY, f"busy: {len(self.queue)} actions waiting", {"holder": holder})
        action_id = "act_" + secrets.token_hex(8)
        record = Record(action_id, action, crid, now, params=request)
        try:
            paths.private_dir(paths.actions_dir())
            fd = os.open(
                self._journal(action_id), os.O_WRONLY | os.O_CREAT | os.O_EXCL | getattr(os, "O_NOFOLLOW", 0), 0o600
            )
        except OSError as exc:
            raise RpcError(ErrorCode.REFUSED, f"cannot journal the action: {exc}", {"reason": RefusedReason.INTERNAL}) from None
        accepted = {
            "type": "accepted",
            "v": JOURNAL_VERSION,
            "action_id": action_id,
            "action": action,
            "params": request,
            "client_request_id": crid,
            "accepted_at": now,
            "service_pid": os.getpid(),
        }
        try:
            # Not `_write`, which lets a lost line go: an action whose acceptance
            # is not on disk could be neither recovered nor deduped after a
            # restart, so it is refused before it runs (X5).
            os.write(fd, (json.dumps(accepted, separators=(",", ":"), ensure_ascii=False) + "\n").encode("utf-8"))
        except OSError as exc:
            with contextlib.suppress(OSError):
                os.close(fd)
            with contextlib.suppress(OSError):
                self._journal(action_id).unlink()
            raise RpcError(ErrorCode.REFUSED, f"cannot journal the action: {exc}", {"reason": RefusedReason.INTERNAL}) from None
        self._fds[action_id] = fd
        self.records[action_id] = record
        self.by_request[crid] = (action_id, now)
        env = dict(env_extra)
        # Never infer a human from client=app: startup/scheduled update checks
        # use that client too. Only an explicit action carries this provenance.
        env[DESKTOP_HUMAN_ENV] = "1" if origin == ORIGIN_DESKTOP else "0"
        if action == Action.UPDATE:
            # By default a person's Update (the app's button).
            env[TRIGGER_ENV] = trigger or ReportTrigger.MANUAL
        if queued:
            self._write(record, {"type": "queued", "at": now, "holder": holder})
            self._close(record)  # opened again when it starts: a waiting action holds no descriptor
            self.queue.append((record, request, env))
            self.drain()  # nothing holds the slot by now: the line moves at once
            self.changed()
            return {"action_id": action_id, "queued": True}
        self._start(record, request, env)
        return {"action_id": action_id}

    def _start(self, record: Record, request: dict, env: dict) -> None:
        self.running = record
        task = asyncio.ensure_future(self._run(record, request, env))
        self._tasks.add(task)
        task.add_done_callback(self._tasks.discard)
        self.changed()

    def pending(self) -> bool:
        """An action runs, or waits for an update: the service stays up for it."""
        return self.running is not None or bool(self.queue)

    def queued_ids(self) -> list[str]:
        """The actions waiting for an update, oldest first."""
        return [record.action_id for record, _request, _env in self.queue]

    def stop_starting(self) -> None:
        """The service is stopping: nothing queued starts any more."""
        self.closed = True

    def drain(self) -> None:
        """Start the oldest queued action once nothing holds the slot (the
        update let go, the action before it ended). One at a time: the next
        starts when this one is done (`_finish`)."""
        if self.queue and not self.closed and self.running is None and self.holder() is None:
            record, request, env = self.queue.pop(0)
            self._start(record, request, env)

    def existing(self, params: dict) -> dict | None:
        """`action.run`'s answer for a `client_request_id` already accepted in
        the last DEDUPE_S (`{action_id, existing: true}`), else None. Starts
        nothing, so the service answers it before any check of the caller: a
        retry of a request accepted once must never read as refused (its
        sender would then run it itself as well)."""
        crid = params.get("client_request_id")
        if not isinstance(crid, str) or not crid:
            return None
        known = self.by_request.get(crid)
        if known is not None and _now() - known[1] < DEDUPE_S and known[0] in self.records:
            return self._existing_answer(known[0])
        return None

    def _existing_answer(self, action_id: str) -> dict:
        answer = {"action_id": action_id, "existing": True}
        if action_id in self.queued_ids():
            answer["queued"] = True  # still waiting for an update
        return answer

    def _record(self, params: dict) -> Record:
        action_id = params.get("action_id")
        if not isinstance(action_id, str) or not _ACTION_ID.match(action_id):
            raise invalid_params("action_id must be an action id (act_ + 16 hex)")
        record = self.records.get(action_id)
        if record is None:
            raise RpcError(ErrorCode.NOT_FOUND, f"not_found: no action {action_id}")
        return record

    def status(self, params: dict) -> dict:
        return self._record(params).public()

    def events(self, params: dict) -> dict:
        record = self._record(params)
        since = params.get("since", 0)
        if not isinstance(since, int) or isinstance(since, bool) or since < 0:
            raise invalid_params("since must be an integer >= 0")
        return {
            "events": [{"seq": seq, "event": event} for seq, event in record.events if seq > since],
            "done": record.state == ActionState.DONE,
        }

    def cancel(self, params: dict) -> dict:
        record = self._record(params)
        if record.state == ActionState.DONE:
            raise RpcError(ErrorCode.REFUSED, "refused: the action already finished", {"reason": RefusedReason.FINISHED})
        if record.last_kind != EVENT_DEVICE_PROMPT:
            raise RpcError(
                ErrorCode.REFUSED,
                "refused: the action is not waiting for a browser approval, and may be writing",
                {"reason": RefusedReason.WRITING},
            )
        process = record.process
        sent = False
        if os.name == "nt":
            # Windows: CTRL_BREAK to the child's own process group (it shares
            # the service's hidden console), which arrives as SIGBREAK: the
            # child stops only inside its approval wait, as SIGINT does on
            # POSIX, never in a write. Nothing is sent when it cannot be
            # delivered (no console): the approval then runs out by itself.
            if process is not None and getattr(process, "returncode", None) is None:
                with contextlib.suppress(OSError, ValueError):
                    process.send_signal(signal.CTRL_BREAK_EVENT)
                    sent = True
        elif process is not None and getattr(process, "returncode", None) is None:
            with contextlib.suppress(ProcessLookupError):
                process.send_signal(signal.SIGINT)
                sent = True
        elif record.child_pid and record.child_start and procid.alive(record.child_pid, record.child_start):
            with contextlib.suppress(OSError):
                os.kill(record.child_pid, signal.SIGINT)
                sent = True
        if sent and not record.cancel_sent:
            record.cancel_sent = True
            self._write(record, {"type": "cancel", "at": _now()})
        return {}

    def busy_holder(self) -> dict | None:
        record = self.running
        if record is None:
            return None
        return {"kind": BusyHolder.ACTION, "action_id": record.action_id, "action": record.action}

    # -- running ---------------------------------------------------------------

    async def _run(self, record: Record, request: dict, env: dict) -> None:
        def started(process) -> None:
            record.process = process
            record.child_pid = process.pid
            record.child_start = procid.start_time(process.pid)
            record.child_at = _now()
            record.state = ActionState.RUNNING
            self._write(
                record, {"type": "child", "pid": process.pid, "start_time": record.child_start, "at": record.child_at}
            )

        code: int | None
        failure: str | None = None
        limit = _env_seconds(ACTION_TIMEOUT_ENV, ACTION_TIMEOUT_S)
        try:
            # The login shell's PATH (D14): an agent installed with nvm or volta
            # is found. The request's context, not the shell, says the rest.
            login = await loginenv.child_env(vars=False)
            code = await children.run_events(
                record.action,
                request,
                env_extra={**login, **env},
                on_event=lambda event: self._event(record, event),
                on_start=started,
                log_path=self._log(record.action_id),
                # Past it the child's group is stopped and the action fails, so
                # the slot (and the update it holds off) is free again (C1).
                timeout=limit,
                grace=_env_seconds(ACTION_STOP_GRACE_ENV, ACTION_STOP_GRACE_S),
            )
        except children.Overran as exc:
            code = exc.code
            failure = f"the action ran past {_span(limit)} and was stopped ({exc.how})"
        except OSError as exc:
            code, failure = None, f"the action could not start: {exc}"
        except asyncio.CancelledError:
            # The service is stopping under it (a signal): its child goes on,
            # and the next service finds it in the journal.
            raise
        except Exception as exc:  # noqa: BLE001 -- a bug here must still end the action
            code, failure = None, f"the service lost the action: {exc!r}"
        record.process = None
        self._finish(record, shell_status(code), failed=failure)

    def _event(self, record: Record, event: dict) -> None:
        if record.done is not None:
            return  # `done` is the last event, whatever a child prints after it
        seq = len(record.events) + 1
        record.events.append((seq, event))
        self._write(record, {"type": "event", "seq": seq, "event": event})
        self.emit("action.event", {"action_id": record.action_id, "seq": seq, "event": event})

    def _finish(
        self,
        record: Record,
        exit_code: int | None,
        *,
        interrupted: str | None = None,
        failed: str | None = None,
    ) -> None:
        if record.state == ActionState.DONE and record.done is not None:
            return  # finished already (an orphan's exit after its journal was closed)
        if record.done is None:
            if interrupted is not None:
                self._event(record, error_event("interrupted", interrupted))
            elif failed is not None:
                self._event(record, error_event("failed", failed))
            else:
                self._event(
                    record,
                    error_event("failed", f"the action ended without finishing (exit {exit_code})"),
                )
            self._event(record, done_event(exit_code))
        elif failed is not None:
            # The child wrote its own `done` as it was stopped (its SIGTERM
            # handler ends the run through its `finally` blocks): the reason
            # the service stopped it is still the action's error.
            record.failure = failed
        record.exit_code = exit_code
        record.ended_at = _now()
        record.state = ActionState.DONE
        record.orphan = False
        ended = {"type": "ended", "at": record.ended_at, "exit_code": exit_code}
        if record.failure:
            ended["failure"] = record.failure
        self._write(record, ended)
        self._close(record)
        if self.running is record:
            self.running = None
        self.emit("action.done", {"action_id": record.action_id, "done": record.done})
        if self.finished is not None:
            self.finished(record.action)
        self.drain()
        self.changed()

    def close(self) -> None:
        # What is still queued stays unfinished in its journal: the next service
        # reads it as stopped with this one (`_recover`), never as run.
        self.stop_starting()
        for timer in self._timers:
            timer.cancel()
        self._timers.clear()
        for task in list(self._tasks):
            task.cancel()
        for action_id in list(self._fds):
            fd = self._fds.pop(action_id)
            with contextlib.suppress(OSError):
                os.close(fd)

