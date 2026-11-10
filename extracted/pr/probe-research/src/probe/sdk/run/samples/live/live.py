"""LiveSamples: one run handle's live side of `run.samples`: the samples this process holds, the handlers adapters
register (`on_cancel`, `on_retry`, `on_watch`), the listener. A handler's raise is its command's refusal."""

from __future__ import annotations

import logging
import threading
from collections.abc import Callable
from dataclasses import dataclass
from typing import TYPE_CHECKING, Any

from .....generated.records import Command, CommandKind, CommandState
from .listener import Answer, CommandListener
from .turns import WatchedTurns

if TYPE_CHECKING:
    from ...run import Run

log = logging.getLogger("probe.samples")

#: A command's handler: ``handler(attempt_key, command)``. A retry's returns the new attempt's key (or a dict).
CommandHandler = Callable[[str, Command], Any]
#: Attempts remembered at once (held, ended ones kept for a retry); the oldest is forgotten past it.
ATTEMPTS_REMEMBERED = 100_000
#: A watch's length when its args name none (`WatchArgs.seconds`).
WATCH_SECONDS = 600
_MAX_REASON_CHARS = 1024


class CommandRefused(Exception):
    """Raised by a handler to refuse its command with this reason, e.g. "the group already finished"."""


@dataclass
class HeldAttempt:
    """A sample this process started: its producer, try, and the commands claimed for it."""

    producer: str
    try_number: int = 1
    is_running: bool = True
    cancel_id: str | None = None
    retry_id: str | None = None


class LiveSamples:
    """One per run handle. Nothing starts until a producer registers a handler (`run.samples.on_cancel`, ...)."""

    def __init__(self, run: Run, scrub: Callable[[str], str]) -> None:
        self._run = run
        self.turns = WatchedTurns(scrub)
        self._attempts: dict[str, HeldAttempt] = {}
        self._handlers: dict[tuple[str, CommandKind], CommandHandler | None] = {}
        self._lock = threading.Lock()
        self._listener: CommandListener | None = None

    # -- handlers ---------------------------------------------------------------------------------
    def register(self, producer: str, kind: CommandKind, handler: CommandHandler | None) -> list[CommandKind]:
        """``producer`` can do ``kind`` (a watch may have no handler: the SDK sends the turns). Returns every kind
        the producer can do now, for its plan row. Starts the listener on first use."""
        if handler is not None and not callable(handler):
            raise TypeError(f"on_{kind.value} takes a callable: handler(attempt_key, command)")
        if getattr(self._run, "_lease", None) is None:
            raise RuntimeError("this run handle holds no writer lease, so no command can be claimed for it")
        with self._lock:
            self._handlers[(producer, kind)] = handler
            kinds = [known for known in CommandKind if (producer, known) in self._handlers]
            is_new = self._listener is None
            if is_new:
                self._listener = CommandListener(self._run, holds=self.holds, run_command=self.run_command)
            listener = self._listener
        if is_new:
            listener.start()
        return kinds

    def get_handler(self, producer: str, kind: CommandKind) -> CommandHandler | None:
        """The handler ``producer`` registered for ``kind``, if any (the rollout proxy serves the rest through it)."""
        with self._lock:
            return self._handlers.get((producer, kind))

    # -- attempts ---------------------------------------------------------------------------------
    def record_start(self, key: str, producer: str, start: dict) -> dict:
        """A sample started: remember it; a retry's start gets its try and the retry command, when not given."""
        with self._lock:
            retried = self._attempts.get(str(start.get("retry_of") or ""))
            if retried is not None:
                start.setdefault("try_number", retried.try_number + 1)
                if retried.retry_id:
                    start.setdefault("command_id", retried.retry_id)
            self._attempts.pop(key, None)
            self._attempts[key] = HeldAttempt(producer, int(start.get("try_number") or 1))
            while len(self._attempts) > ATTEMPTS_REMEMBERED:
                self._attempts.pop(next(iter(self._attempts)))
        return start

    def record_end(self, key: str) -> str | None:
        """A sample ended: no command but a retry reaches it now. Returns the cancel claimed for it, if any."""
        self.turns.forget(key)
        with self._lock:
            held = self._attempts.get(key)
            if held is None:
                return None
            held.is_running = False
            return held.cancel_id

    def holds(self, key: str, kind: str) -> bool:
        """This process started the sample and can do ``kind`` for it (cancel and watch: while it runs)."""
        with self._lock:
            held = self._attempts.get(key)
        if held is None:
            return False
        return held.is_running or kind == CommandKind.RETRY.value

    def check_commands_seq(self, seq: Any) -> None:
        """The writer beat's command counter: the listener's backstop."""
        listener = self._listener
        if listener is not None:
            listener.check_commands_seq(seq)

    def close(self) -> None:
        listener = self._listener
        if listener is not None:
            listener.close()

    # -- a claimed command (on the listener's thread) ---------------------------------------------
    def run_command(self, command: Command) -> Answer:
        """Run the claimed command's handler. Whatever it raises is the refusal, never the script's."""
        key = str(command.attempt_key)
        with self._lock:
            held = self._attempts.get(key)
            producer = held.producer if held is not None else None
            has_kind = producer is not None and (producer, command.kind) in self._handlers
            handler = self._handlers.get((producer, command.kind)) if has_kind else None
        if producer is None or not has_kind:
            return Answer(CommandState.REFUSED, f"{command.kind.value} not supported by {producer or 'this process'}")
        if command.kind is not CommandKind.RETRY and not held.is_running:  # type: ignore[union-attr]
            return Answer(CommandState.REFUSED, "the sample already ended")
        try:
            result = self._run_kind(key, command, handler, held)  # type: ignore[arg-type]
        except CommandRefused as exc:
            return Answer(CommandState.REFUSED, (str(exc) or "refused")[:_MAX_REASON_CHARS])
        except Exception as exc:  # noqa: BLE001 -- a handler's failure is the command's answer, not the run's
            log.warning("probe: the %s handler for sample %s raised %s: %s; training goes on", command.kind.value,
                        key, type(exc).__name__, exc)  # fmt: skip
            return Answer(CommandState.REFUSED, f"{type(exc).__name__}: {exc}"[:_MAX_REASON_CHARS])
        return Answer(CommandState.DONE, result=result)

    def _run_kind(self, key: str, command: Command, handler: CommandHandler | None, held: HeldAttempt) -> dict:
        if command.kind is CommandKind.WATCH:
            seconds = (command.args or {}).get("seconds") or WATCH_SECONDS
            self.turns.start_watch(key, float(seconds))
            if handler is not None:
                handler(key, command)
            return {"seconds": int(seconds)}
        if command.kind is CommandKind.CANCEL:
            held.cancel_id = str(command.id)
            try:
                returned = handler(key, command) if handler is not None else None
            except BaseException:
                held.cancel_id = None
                raise
            return returned if isinstance(returned, dict) else {}
        held.retry_id = str(command.id)
        returned = handler(key, command) if handler is not None else None
        if isinstance(returned, str):
            return {"attempt_key": returned}
        return returned if isinstance(returned, dict) else {}
