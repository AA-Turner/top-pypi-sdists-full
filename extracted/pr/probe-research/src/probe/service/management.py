"""`desktop.request`: the desktop app's management requests, answered by the
service (plan Q6) instead of a `probe desktop request --json` the app spawns.

    request   `params.request`: the closed JSON object that command reads on
              stdin (`{"op": ..., ...}`, `probe.cli.desktop.FIELDS`), checked
              by that code in the child, never here: one checker
    answer    its v1 envelope, unchanged: `{"v": 1, "ok": true, "data": ...}`
              or `{"v": 1, "ok": false, "error": str}`; an envelope that says
              ok from a child that then failed reads as the app reads it
              (`NOT_COMPLETED`)
    child     `<the CLI's python> -I -m probe.core.run desktop`, stdin the
              request (`probe.cli.desktop.respond`, which the command runs too;
              it waits out an update's barrier first, as `probe` does); its
              environment: the service's own, the login shell's PATH for the
              ops that run the agents' CLIs (NEEDS_AGENTS; read at most every
              LOGIN_TTL_S), the request's context, PROBE_DESKTOP_HUMAN
    deadline  per op (DEADLINES; READ_S, CHANGE_S otherwise), the wait for a
              turn included. A read (`protocol.DESKTOP_READS`) still running
              then is killed: it leaves nothing half-written. Every other op is
              a change, one added later included, and is never killed: the
              service stops waiting and says `timed_out` (`killed: false`),
              and the child finishes or fails on its own, as the app's CLI
              path lets it
    at once   MAX_RUNNING children, MAX_WAITING more waiting for a turn; a
              change's child counts as an action for the updater's quiet check
              until it exits (`running`), so no update replaces its files

The caller checks (sandbox, D9) are the server's.

Stdlib only (the start path; plan S1).
"""

from __future__ import annotations

import asyncio
import contextlib
import json
import os
import time
from collections.abc import Callable

from . import children, loginenv, paths, procid
from .actions import DESKTOP_HUMAN_ENV
from .protocol import (
    DESKTOP_READS,
    MAX_LINE_BYTES,
    BusyHolder,
    DesktopOp,
    ErrorCode,
    RefusedReason,
    RpcError,
    encode,
    result,
)

#: The `probe.core.run` read that answers a management request.
CORE_ACTION = "desktop"
#: The ops that look for, or start, the agents' own CLIs (a folder backfill
#: runs the Claude Code or Codex CLI): their child gets the login shell's PATH (D14),
#: which finds an agent installed with nvm or volta. The others need none.
NEEDS_AGENTS = frozenset({DesktopOp.PREVIEW_BACKFILL, DesktopOp.START_BACKFILL, DesktopOp.RESUME_JOB})
#: Seconds per op, the app's own limits: the analytics read and onboarding's
#: acknowledgement are bounded at 12 s by the app (onboarding by the CLI too).
DEADLINES = {DesktopOp.ANALYTICS_POLICY: 12.0, DesktopOp.ONBOARDING_COMPLETE: 15.0}
READ_S = 60.0
CHANGE_S = 120.0
#: A request whose turn came with less than this left is refused unrun.
MIN_RUN_S = 1.0
MAX_RUNNING = 4
MAX_WAITING = 8
#: The request as the child reads it, at most (`probe.cli.desktop.MAX_INPUT`).
MAX_REQUEST_BYTES = 1024 * 1024
#: The answer must fit one wire line (API v1); the app's CLI path takes more,
#: so a bigger one is `no_answer` with `too_large`, and the app asks the CLI.
MAX_ANSWER_BYTES = MAX_LINE_BYTES - 4096
LOGIN_TTL_S = 300.0
#: What the app says for an envelope that is ok from a child that failed.
NOT_COMPLETED = "The Probe CLI did not complete the desktop request."
#: The caller's process (pid, and start time where the kernel names it), set
#: by the service for the child, never by a request (`protocol.CONTEXT_ENV`
#: has neither): the child resolves the session the caller runs in from it,
#: as that caller's own `probe` would (`probe.core.run._desktop_refusal`).
CALLER_PID_ENV = "PROBE_DESKTOP_CALLER_PID"
CALLER_START_ENV = "PROBE_DESKTOP_CALLER_START"
#: The change children still running, by process identity, for the next
#: service when this one stops under them (`Management.load`).
CHANGES_NAME = "desktop-changes.json"
CHANGES_VERSION = 1


def is_change(op: str) -> bool:
    """Every op that is not a known read: fail closed."""
    return op not in DESKTOP_READS


def deadline(op: str) -> float:
    return DEADLINES.get(op, CHANGE_S if is_change(op) else READ_S)


def _refused(reason: str, message: str, **data: object) -> RpcError:
    return RpcError(ErrorCode.REFUSED, f"refused: {message}", {"reason": reason, **data})


class Management:
    def __init__(self, *, log=lambda message: None, changed: Callable[[], None] = lambda: None) -> None:
        self.log = log
        #: Called when a change's child exits (what holds the service changed).
        self.changed = changed
        self._slots = asyncio.Semaphore(MAX_RUNNING)
        #: Requests taken in: running, or waiting for a turn.
        self.admitted = 0
        #: Change children running now, answered or not, this service's and
        #: those an earlier one left (`load`): `{key: {"pid", "start"}}`. A read
        #: is not counted: it is killable, and it waits out an update's barrier
        #: before it imports anything.
        self._changes: dict = {}
        #: Children run so far (the tests read it).
        self.children = 0
        self._login: tuple[float, dict] | None = None
        self._login_flight: asyncio.Future | None = None
        self._tasks: set = set()

    @property
    def running(self) -> int:
        """Change children running now: they hold the service alive, the one
        mutating slot and the updater off, until each exits (also past its
        request's deadline, also across a service restart)."""
        return len(self._changes)

    def in_flight(self) -> bool:
        """Is a request being answered (it holds the service alive meanwhile)?"""
        return self.admitted > 0

    # -- change children: tracked until they exit, across restarts ------------------

    def _path(self):
        return paths.service_dir() / CHANGES_NAME

    def _save(self) -> None:
        """The identities of the change children running (those whose start
        time is read: a pid alone names no process), 0600, atomically."""
        rows = [{"pid": c["pid"], "start": c["start"]} for c in self._changes.values() if c.get("start")]
        target = self._path()
        tmp = target.with_name(f"{target.name}.{os.getpid()}.tmp")
        try:
            paths.private_dir(target.parent)
            with open(os.open(tmp, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o600), "w", encoding="utf-8") as handle:
                json.dump({"v": CHANGES_VERSION, "changes": rows}, handle)
            os.replace(tmp, target)
        except OSError:
            pass
        finally:
            with contextlib.suppress(OSError):
                os.unlink(tmp)

    def _started(self, key: object, child) -> None:
        """A change's child started: counted at once, its start time read off
        the loop (`ps` on macOS), then saved for a next service."""
        self._changes[key] = {"pid": child.pid, "start": None}
        task = asyncio.ensure_future(self._identify(key, child.pid))
        self._tasks.add(task)
        task.add_done_callback(self._tasks.discard)

    async def _identify(self, key: object, pid: int) -> None:
        try:
            start = await asyncio.to_thread(procid.start_time, pid)
        except Exception:  # noqa: BLE001 -- then it is counted here, never saved
            return
        entry = self._changes.get(key)
        if entry is not None and entry["pid"] == pid and start:
            entry["start"] = start
            self._save()

    def _gone(self, key: object) -> None:
        if self._changes.pop(key, None) is not None:
            self._save()
            self.changed()

    def load(self, watch: Callable[[object, int, str, Callable[[], None]], None]) -> None:
        """At start: the change children an earlier service saved that still
        run count here too, each watched to its exit (`watch(key, pid, start,
        callback)`, the service's pid watcher), so an Update is not admitted
        under one because the service that started it went."""
        try:
            data = json.loads(self._path().read_text(encoding="utf-8"))
        except (OSError, ValueError):
            return
        rows = data.get("changes") if isinstance(data, dict) and data.get("v") == CHANGES_VERSION else None
        for row in rows if isinstance(rows, list) else []:
            pid, start = (row.get("pid"), row.get("start")) if isinstance(row, dict) else (None, None)
            if not isinstance(pid, int) or isinstance(pid, bool) or pid <= 1 or not isinstance(start, str) or not start:
                continue
            key = ("desktop", pid, start)
            if key in self._changes or procid.alive(pid, start) is False:
                continue
            self._changes[key] = {"pid": pid, "start": start}
            watch(key, pid, start, lambda key=key: self._gone(key))
        self._save()

    def busy_holder(self) -> dict | None:
        """The mutating slot's holder while a change's child runs, else None."""
        return {"kind": BusyHolder.DESKTOP, "changes": self.running} if self.running > 0 else None

    async def _login_path(self) -> dict:
        """The login shell's PATH (`loginenv`), one read at a time, reused for
        LOGIN_TTL_S. PATH only: never a variable that could carry a password."""
        now = time.monotonic()
        if self._login is not None and now - self._login[0] < LOGIN_TTL_S:
            return dict(self._login[1])
        if self._login_flight is None or self._login_flight.done():
            self._login_flight = asyncio.ensure_future(loginenv.child_env(vars=False))
        env = await asyncio.shield(self._login_flight)
        self._login = (time.monotonic(), env)
        return dict(env)

    async def request(self, request: dict, env: dict, *, human: bool, may_start=lambda: None) -> dict:
        """Answer one management request (already shape-checked by the server).
        `may_start()` raises when no child may start now (an update applying):
        asked again right before the child starts, after any wait for a turn."""
        op = request["op"]
        change = is_change(op)
        try:
            # Strict JSON, as the child reads it (a `NaN` the wire let through is not).
            payload = json.dumps(request, ensure_ascii=False, allow_nan=False).encode("utf-8")
        except ValueError:
            raise RpcError(ErrorCode.INVALID_PARAMS, "invalid params: request is not plain JSON") from None
        if len(payload) > MAX_REQUEST_BYTES:
            raise RpcError(ErrorCode.INVALID_PARAMS, "invalid params: request exceeds 1 MiB")
        if self.admitted >= MAX_RUNNING + MAX_WAITING:
            raise _refused(RefusedReason.TOO_MANY, "too many desktop requests in flight; ask again shortly")
        limit = deadline(op)
        started = time.monotonic()
        self.admitted += 1
        try:
            try:
                await asyncio.wait_for(self._slots.acquire(), limit)
            except asyncio.TimeoutError:
                raise _refused(RefusedReason.TOO_MANY, "no turn came within the request's deadline") from None
            try:
                login = await self._login_path() if op in NEEDS_AGENTS else {}
                extra = {**login, **env, DESKTOP_HUMAN_ENV: "1" if human else "0"}
                left = limit - (time.monotonic() - started)
                if left < MIN_RUN_S:
                    raise _refused(RefusedReason.TOO_MANY, "its turn came too late to answer within the deadline")
                may_start()
                self.children += 1
                key = object()
                try:
                    # A change counts until its child EXITS, which one past its
                    # deadline does after this request has answered.
                    code, out, more = await children.run_once(
                        CORE_ACTION, payload, env_extra=extra, timeout=left, kill=not change,
                        max_output=MAX_ANSWER_BYTES,
                        on_start=(lambda child: self._started(key, child)) if change else None,
                        on_exit=(lambda: self._gone(key)) if change else None,
                    )
                except OSError as exc:
                    raise _refused(RefusedReason.CLI_UNAVAILABLE, f"the Probe CLI could not start ({exc})") from None
            finally:
                self._slots.release()
        finally:
            self.admitted -= 1
        if code is None:
            self.log(f"desktop.request {op!r}: no answer within {limit:g} s "
                     f"({'left running' if change else 'stopped'})")
            raise _refused(
                RefusedReason.TIMED_OUT, f"no answer within {limit:g} s", killed=not change, deadline_s=limit
            )
        if more:
            raise _refused(RefusedReason.NO_ANSWER, "the answer is over one line; ask the CLI", too_large=True,
                           exit_code=code)
        envelope = _envelope(out)
        if envelope is None:
            self.log(f"desktop.request {op!r}: the child gave no envelope (exit {code})")
            raise _refused(RefusedReason.NO_ANSWER, f"the Probe CLI gave no answer (exit {code})", exit_code=code)
        if code != 0 and envelope.get("ok") is True:
            return {"v": 1, "ok": False, "error": NOT_COMPLETED}
        return envelope


def _envelope(out: bytes) -> dict | None:
    """The child's one JSON line, if it is a v1 envelope the wire can carry
    (a lone surrogate, from a file name that is not UTF-8, cannot be)."""
    try:
        value = json.loads(out.decode("utf-8"))
    except (UnicodeDecodeError, ValueError):
        return None
    if not isinstance(value, dict) or value.get("v") != 1 or not isinstance(value.get("ok"), bool):
        return None
    if value["ok"] and "data" not in value:
        return None
    if not value["ok"] and not isinstance(value.get("error"), str):
        return None
    try:
        encode(result(0, value))
    except (UnicodeEncodeError, ValueError):
        return None
    return value
