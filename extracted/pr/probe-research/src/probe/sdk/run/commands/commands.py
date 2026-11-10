"""RunCommandsMixin: a running script takes commands (agentic W&B C.1). `run.on(kind, fn)` registers a handler and,
for a new kind, says so on one beat at once; every writer beat declares what is registered (`capabilities`) and, when
the run's command counter moves, lists, claims and queues the asks for this writer; the next `run.log()` (a safe point
on the training thread) runs each handler and answers it. `stop --force` is answered and done on the beat thread.
Why: DESIGN.md."""

from __future__ import annotations

import collections
import enum
import logging
import os
import re
import signal
import threading
import weakref
from collections.abc import Callable
from typing import TYPE_CHECKING, Any

from ....foundation.safe_warn import safe_warn as _diagnostics
from ....generated.records import CommandKind
from ..closing.heartbeat import _beat_once
from .ranks import get_world, send_to_every_rank
from .stream import ProducerStream

if TYPE_CHECKING:
    from ...client.client import Client

logger = logging.getLogger(__name__)

#: The built-in kinds a script registers by `CommandKind`; any other kind is the script's own `StrEnum` member.
RUN_KINDS = (CommandKind.CHECKPOINT, CommandKind.CONFIG, CommandKind.STOP)
#: A custom kind's value (`probe_contracts.records.command.CUSTOM_NAME_PATTERN`).
_CUSTOM_NAME = re.compile(r"^[a-z][a-z0-9_]{0,63}$")
#: Why a command waits in vain in a job of several processes with no sync point.
NO_SYNC_POINT = ("this run has {world} processes: call probe.commands.sync() on every rank (the HF Trainer and "
                 "Lightning integrations do it for you)")  # fmt: skip
#: `0` keeps a script on its beat alone (no live stream for commands).
COMMANDS_STREAM_ENV = "PROBE_COMMANDS_STREAM"
#: The live kinds the stream follows: a run kind's notice, and `resync` (always delivered) to read again.
_RUN_COMMAND_KIND = "run.command"
_RESYNC_KIND = "resync"
#: After a forced stop's SIGTERM, the SIGKILL that follows if the process is still there.
FORCE_KILL_AFTER_SECONDS = 60.0
_MAX_REASON_CHARS = 1024


class CommandBox:
    """One run handle's command state: the handlers, the last command number seen, the claimed asks waiting for the
    next safe point. Shared by the beat thread (fills it) and the training thread (empties it)."""

    def __init__(self) -> None:
        self.lock = threading.Lock()
        self.handlers: dict[str, Callable[..., Any]] = {}
        self.seen = 0
        self.due: collections.deque[dict] = collections.deque()
        #: A handler that logs reaches the safe point again: it must not run the next command inside itself.
        self.is_running = False
        #: A sync point hands the commands to every rank (`probe.commands.sync()`, the HF Trainer and Lightning
        #: integrations): `run.log()` then leaves them to it.
        self.is_shared = False
        #: One reader at a time (the beat and the live stream both read): a command is claimed and queued once.
        self.read_lock = threading.Lock()
        #: This handle's one producer stream (`ProducerStream`), shared with the sample command listener; made on
        #: first use.
        self.producer: ProducerStream | None = None
        #: Whether this handle follows `run.command` on it (once a handler is registered).
        self.is_following = False
        #: Whether a beat saying what is registered is on its way (`_report_capabilities`).
        self.is_report_due = False
        #: One lease beat of this handle at a time, each reading the handlers as it sends (`_lease_beat`). The server
        #: keeps the last beat's capabilities, so a beat that read fewer must never land after one that read more
        #: (prod smoke 5: three beats in flight at once, and the one saying only `checkpoint` landed last; config and
        #: stop were refused until the next loop beat). Re-entrant: the capabilities beat holds it while it clears
        #: `is_report_due`, then beats.
        self.beat_lock = threading.RLock()
        #: This process's rank in torch.distributed, kept from the last time it ran: after the process group ends a
        #: rank above 0 still never claims.
        self.torch_rank: int | None = None


def get_handler_key(kind: str, args: dict[str, Any]) -> str:
    """`checkpoint`, or a custom kind's own name: one key per thing a script can be asked."""
    return str(args.get("name", "")) if kind == CommandKind.CUSTOM.value else kind


def check_kind(kind: enum.Enum) -> str:
    if not isinstance(kind, enum.Enum) or not isinstance(kind.value, str):
        raise TypeError(f"run.on takes an enum member (CommandKind.CHECKPOINT, or a member of your own StrEnum: "
                        f"class TrainerCommand(StrEnum): EVAL_NOW = 'eval_now'), not {kind!r}")  # fmt: skip
    if isinstance(kind, CommandKind):
        if kind not in RUN_KINDS:
            raise ValueError(f"{kind.value} is not asked of a run's script: register checkpoint, config, stop or your "
                             "own StrEnum's kinds")  # fmt: skip
        return kind.value
    if not _CUSTOM_NAME.fullmatch(kind.value) or kind.value in {member.value for member in CommandKind}:
        raise ValueError(f"{kind.value!r}: a command kind's value is lowercase letters, digits and _ (up to 64), "
                         "and not a built-in kind")  # fmt: skip
    return kind.value


class RunCommandsMixin:
    """Part of Run: its methods run with `self` the Run; compose() folds them into Run."""

    _commands: CommandBox
    _client: Client

    def on(self, kind: enum.Enum, handler: Callable[..., Any]) -> None:
        """Run ``handler`` when this run is asked for ``kind``, at the next ``run.log()`` (a safe point).

        ``kind`` is an enum member, never a string: ``CommandKind.CHECKPOINT`` (``handler()``; return the saved
        artifact's id, or a dict), ``CommandKind.CONFIG`` (``handler(values)``; the values are then recorded on
        ``run.config``), ``CommandKind.STOP`` (``handler()``, a graceful stop; ``--force`` signals the process
        itself), or a member of your own ``StrEnum`` (``handler(payload)``). Asked with ``probe run send``."""
        key = check_kind(kind)
        if not callable(handler):
            raise TypeError("run.on takes a callable handler")
        self._add_handlers({key: handler})

    def _add_handlers(self, handlers: dict[str, Callable[..., Any]], *, should_replace: bool = True) -> None:
        """Register handlers by key and, when one is new, say so on one beat. Several at once (an integration's
        built-ins) reach that beat together, never a beat with only some of them. ``should_replace=False`` keeps a
        handler already registered (the script's own)."""
        with self._commands.lock:
            is_new = any(key not in self._commands.handlers for key in handlers)
            for key, handler in handlers.items():
                if should_replace or key not in self._commands.handlers:
                    self._commands.handlers[key] = handler
        self._start_command_stream()
        if is_new:
            self._report_capabilities()

    def _report_capabilities(self) -> None:
        """Say what this script can be asked now, on one lease beat off the training thread, not at the next beat (up
        to a minute away): an ask sent around `run.on` then reaches the script at once instead of waiting for it.
        Rank 0, while this handle beats its lease; one such beat waiting at a time (it reads the handlers once it
        holds `beat_lock`, so kinds registered while it waited ride on it)."""
        box, lease, stop = self._commands, getattr(self, "_lease", None), getattr(self, "_hb_stop", None)
        if (not lease or not self._is_claiming_rank() or stop is None or stop.is_set()
                or getattr(self, "_hb_role", "owner") == "observer"):  # fmt: skip
            return
        with box.lock:
            if box.is_report_due:
                return
            box.is_report_due = True
        threading.Thread(target=_send_capabilities, args=(weakref.ref(self), self._client, lease),
                         name=f"probe-run-capabilities-{self.id[:8]}", daemon=True).start()  # fmt: skip

    def _start_command_stream(self) -> None:
        """Hear an ask within a second (agentic W&B W20): follow the run's `run.command` events as this writer's
        producer stream, and read the commands when one is asked (or the stream says to re-read). The beat stays the
        backstop, so a stream that cannot start or stops costs only speed. Rank 0 only; once per handle."""
        box, lease = self._commands, getattr(self, "_lease", None)
        if (box.is_following or not lease or not self._is_claiming_rank()
                or os.environ.get(COMMANDS_STREAM_ENV, "").strip() == "0"):  # fmt: skip
            return
        handle, client, session_id = weakref.ref(self), self._client, str(lease["session_id"])

        def handle_event(event: Any) -> None:
            run = handle()
            if run is None:
                return
            data = event.data if isinstance(event.data, dict) else {}
            if event.kind == _RESYNC_KIND:
                run._read_new_commands(client, session_id, run._commands.seen + 1)
            elif event.kind == _RUN_COMMAND_KIND and data.get("state") == "open":
                run._read_new_commands(client, session_id, int(data.get("seq") or 0))

        box.is_following = True
        self._get_producer_stream().follow(_RUN_COMMAND_KIND, handle_event)

    def _is_claiming_rank(self) -> bool:
        """Whether this process claims the run's commands: rank 0 by its launcher (the lease's rank, from RANK and
        kin) AND by torch.distributed once it runs. A launcher that sets no RANK (`mp.spawn`, Lightning's
        `ddp_spawn`) gives every rank a lease without one, so the lease alone made every rank claim, and a command
        a rank above 0 claimed never reached the hand-off."""
        if (getattr(self, "_lease", None) or {}).get("rank") not in (None, 0):
            return False
        box = self._commands
        try:
            rank, world = get_world()
        except Exception:  # noqa: BLE001 -- the process group ending under the beat thread: the rank it last had
            rank, world = 0, 1
        if world > 1:
            box.torch_rank = rank
        return not box.torch_rank

    def _get_producer_stream(self) -> ProducerStream:
        """This handle's one producer stream: the server keeps one per writer session, so the sample command
        listener follows its kind on the same one."""
        box = self._commands
        with box.lock:
            if box.producer is None:
                box.producer = ProducerStream(self)
            return box.producer

    def _stop_command_stream(self) -> None:
        producer, self._commands.producer = self._commands.producer, None
        self._commands.is_following = False
        if producer is not None:
            producer.close()

    def _get_command_capabilities(self) -> dict[str, list[str]]:
        """The beat's `capabilities`: the built-in kinds and custom names registered here (both may be empty: an
        SDK that takes commands, with nothing registered yet)."""
        with self._commands.lock:
            keys = set(self._commands.handlers)
        built_in = {kind.value for kind in RUN_KINDS}
        return {"kinds": sorted(keys & built_in), "custom": sorted(keys - built_in)}

    def _read_new_commands(self, client: Client, session_id: str, seq: Any) -> None:
        """On the beat thread: the run's counter moved past what this writer saw, so list the new asks and claim the
        ones it has a handler for. Rank 0 claims (the beat and the live stream both read here); the sync point hands
        them to the other ranks. Never raises."""
        box = self._commands
        if not isinstance(seq, int) or seq <= box.seen:
            return
        if not self._is_claiming_rank():
            box.seen = seq
            return
        with box.read_lock:
            if seq <= box.seen:
                return  # the other reader got here first
            try:
                self._claim_new_commands(client, session_id)
            except Exception as exc:  # noqa: BLE001 -- the beat must never fail on a command
                logger.debug("probe: run %s: reading its commands failed: %s", self.id, exc)

    def _claim_new_commands(self, client: Client, session_id: str) -> None:
        box = self._commands
        after: int | None = box.seen
        while after is not None:
            page = client.list_run_commands(self.id, after=after)
            for row in page.get("commands", []):
                self._take_command(client, session_id, row)
                # Past a row only once it is handled: a claim that failed is read again on the next beat.
                box.seen = max(box.seen, int(row["seq"]))
            after = page.get("next_after")

    def _take_command(self, client: Client, session_id: str, row: dict) -> None:
        """Claim an open run command this writer has a handler for, and queue it (a forced stop: do it now)."""
        box = self._commands
        key = get_handler_key(row["kind"], row.get("args") or {})
        if row["state"] != "open" or row.get("attempt_id") or key not in box.handlers:
            return
        claimed = client.claim_run_command(self.id, row["id"], session_id)
        if claimed is None:
            return
        if row["kind"] == CommandKind.STOP.value and (row.get("args") or {}).get("force"):
            self._stop_now(client, session_id, claimed)
            return
        with box.lock:
            box.due.append({**claimed, "session_id": session_id})

    def _stop_now(self, client: Client, session_id: str, command: dict) -> None:
        """`stop --force`: answered, then SIGTERM to this process (the SDK's preempt handler flushes), and SIGKILL
        if it is still there a minute later."""
        client.answer_run_command(self.id, command["id"], session_id, state="done", result={"signal": "SIGTERM"})
        _diagnostics.warn(f"probe: run {self.id}: stopping now (`probe run send stop --force`)")
        pid = os.getpid()
        killer = threading.Timer(FORCE_KILL_AFTER_SECONDS, os.kill, args=(pid, getattr(signal, "SIGKILL", signal.SIGTERM)))
        killer.daemon = True
        killer.start()
        os.kill(pid, signal.SIGTERM)

    def _run_due_commands(self) -> None:
        """At a safe point on the training thread (`run.log()`): run each claimed ask's handler and answer it. A
        handler that raises answers `refused` with its error; the run goes on."""
        box = self._commands
        if box.is_running or box.is_shared:
            return
        _rank, world = get_world()
        if world > 1:
            self._refuse_commands(self._take_due_commands(), NO_SYNC_POINT.format(world=world))
            return
        box.is_running = True
        try:
            while box.due:
                with box.lock:
                    if not box.due:
                        return
                    command = box.due.popleft()
                self._answer_command(command)
        finally:
            box.is_running = False

    def _take_due_commands(self) -> list[dict]:
        """Every claimed command waiting, taken off the queue (a sync point hands them to every rank)."""
        with self._commands.lock:
            taken = list(self._commands.due)
            self._commands.due.clear()
        return taken

    def _refuse_commands(self, commands: list[dict], reason: str) -> None:
        for command in commands:
            self._send_answer(command, "refused", reason, {})

    def _answer_command(self, command: dict, *, should_answer: bool = True) -> None:
        """Run the command's handler here; answer it when asked to (rank 0 answers for the job, as the claiming
        session the command carries)."""
        kind, args = command["kind"], command.get("args") or {}
        handler = self._commands.handlers.get(get_handler_key(kind, args))
        state, reason, result = "done", None, {}
        try:
            result = _to_result(kind, self._call_handler(handler, kind, args))
        except Exception as exc:  # noqa: BLE001 -- a handler's failure is the command's answer, not the run's
            state, reason = "refused", f"{type(exc).__name__}: {exc}"[:_MAX_REASON_CHARS]
        if should_answer:
            self._send_answer(command, state, reason, result)

    def _send_answer(self, command: dict, state: str, reason: str | None, result: dict) -> None:
        try:
            self._client.answer_run_command(self.id, command["id"], command["session_id"], state=state,
                                            reason=reason, result=result)  # fmt: skip
        except Exception as exc:  # noqa: BLE001 -- an unanswered command reads `lost` once this writer ends
            logger.debug("probe: run %s: answering command %s failed: %s", self.id, command["id"], exc)

    def sync_commands(self) -> int:
        """Hand the claimed commands to every rank and run each one's handler on every rank, at the same point
        (`probe.commands.sync()`). Rank 0 claims, but a rank that claimed before torch.distributed numbered it hands
        its own on too, so nothing claimed waits in one process. Every rank must call it, or the job hangs; rank 0
        answers. Returns how many commands ran here."""
        self._commands.is_shared = True
        rank, _world = get_world()
        commands = send_to_every_rank(self._take_due_commands())
        for command in commands:
            self._answer_command(command, should_answer=rank == 0)
        return len(commands)

    def _call_handler(self, handler: Callable[..., Any] | None, kind: str, args: dict[str, Any]) -> Any:
        if handler is None:
            raise LookupError("no handler is registered for it any more")
        if kind == CommandKind.CONFIG.value:
            values = dict(args.get("values") or {})
            returned = handler(values)
            # Asked for by a person: a change, never a surprise to warn about.
            self.update_config(values, allow_val_change=True)
            return returned if returned is not None else {"applied": sorted(values)}
        if kind == CommandKind.CUSTOM.value:
            return handler(dict(args.get("payload") or {}))
        return handler()


def _send_capabilities(handle: weakref.ref, client: Client, lease: dict) -> None:
    """One lease beat, after any beat of this handle already on its way (`CommandBox.beat_lock`); its body carries
    the handlers registered when it sends. Never raises: the loop's next beat says the same."""
    run = handle()
    if run is None:
        return
    box = run._commands
    run_id, write_epoch, attached = run.id, run.write_epoch, bool(getattr(run, "attached", False))
    del run  # held weakly from here on, as the loop holds it
    with box.beat_lock:
        with box.lock:
            box.is_report_due = False  # this beat reads the handlers now: a kind registered from here on needs its own
        try:
            _beat_once(client, run_id, role="owner", attached=attached, write_epoch=write_epoch, lease=lease,
                       handle_ref=handle)  # fmt: skip
        except Exception as exc:  # noqa: BLE001 -- a liveness beat never fails the script
            logger.debug("probe: run %s: saying what it can be asked failed: %s", run_id, exc)


def _to_result(kind: str, returned: Any) -> dict[str, Any]:
    """A handler's return as the answer's `result`: a dict as it is, a checkpoint's id as `artifact_id`."""
    if isinstance(returned, dict):
        return returned
    if returned is not None and kind == CommandKind.CHECKPOINT.value:
        return {"artifact_id": str(returned)}
    return {}


__all__ = ["COMMANDS_STREAM_ENV", "FORCE_KILL_AFTER_SECONDS", "NO_SYNC_POINT", "CommandBox", "RunCommandsMixin", "check_kind", "get_handler_key"]
