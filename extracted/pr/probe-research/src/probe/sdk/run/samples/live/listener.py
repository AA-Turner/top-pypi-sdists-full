"""CommandListener: hears a run's sample commands on a producer stream (through the Probe service) or, as a backstop,
from the writer beat's counter; claims those this process holds, runs each handler, answers. Never raises."""

from __future__ import annotations

import logging
import queue
import threading
from collections.abc import Callable
from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Any

from .....generated.records import Command, CommandKind, CommandState

if TYPE_CHECKING:
    from ...run import Run

log = logging.getLogger("probe.samples")

#: The live notice a producer follows (`LiveEventKind.SAMPLES_COMMAND`).
COMMAND_EVENT_KIND = "samples.command"
#: The kinds asked of a sample; a run kind (checkpoint, config, stop, custom) is the run script's (`run.on`).
SAMPLE_KINDS = frozenset({CommandKind.CANCEL.value, CommandKind.RETRY.value, CommandKind.WATCH.value})
#: Commands remembered as handled, so a notice and a backstop list never run one twice.
HANDLED_REMEMBERED = 10_000
#: An answer that cannot be sent is tried this many times; then the command reads `lost` once the lease ends.
ANSWER_TRIES = 3
#: The live route's refusal of a producer stream whose writer lease is not live (`app/live/router.py`).
WRITER_NOT_LIVE = "writer_not_live"
#: Past every seq: a list after it is empty and names the run's counter (`CommandList.seq`).
_PAST_EVERY_SEQ = 2**62
_STOP = object()


@dataclass(frozen=True)
class Answer:
    """What a handler's run says: `done` with a `result`, or `refused` with why."""

    state: CommandState
    reason: str | None = None
    result: dict[str, Any] = field(default_factory=dict)


class CommandListener:
    """``holds(attempt_key, kind)``: does this process hold that sample (and can do the kind)? ``run_command``:
    the handler's run, as an `Answer`. Both are called on the listener's own thread."""

    def __init__(self, run: Run, *, holds: Callable[[str, str], bool], run_command: Callable[[Command], Answer]) -> None:
        self._run = run
        self._holds = holds
        self._run_command = run_command
        self._session_id = str(run.session_id)
        self._jobs: queue.Queue = queue.Queue()
        self._handled: dict[str, None] = {}
        #: The highest command seq a notice or a list showed this process; the beat's counter past it is a miss.
        self._delivered: int | None = None
        #: A command whose claim failed on the way (not a 409): the next beat lists again from before it.
        self._retry_from: int | None = None
        self._subscription = None
        self._producer: Any = None
        self._is_closed = False
        self._thread = threading.Thread(target=self._run_jobs, name="probe-sample-commands", daemon=True)

    @property
    def subscription(self):
        """The producer stream (`probe.events.Subscription`), once open."""
        return self._subscription

    def start(self) -> None:
        """Read the run's counter (commands from before this process held a sample are not its own), then follow
        the producer stream. Its claims, handlers and answers run on this listener's thread."""
        self._thread.start()
        self._jobs.put(("baseline", None))
        self._open_stream(since=None)

    def check_commands_seq(self, seq: Any) -> None:
        """The writer beat's answer: the run's command counter. Past what this process saw, list what it missed.
        A stream the server refused while this writer's lease was not live opens again from where it stopped."""
        old = self._subscription
        if old is not None and not old.is_running and not self._is_closed and _is_lease_refusal(old.error):
            self._open_stream(since=old.cursor)
        if not isinstance(seq, int) or isinstance(seq, bool):
            return
        delivered = self._delivered
        if self._retry_from is not None or delivered is None or seq > delivered:
            self._jobs.put(("backstop", None))

    def close(self, timeout: float = 2.0) -> None:
        self._is_closed = True
        if self._subscription is not None:
            # Shared with the run command listener: stop following, never close it under the other one.
            self._get_producer().stop_following(COMMAND_EVENT_KIND, self._take_event)
        self._jobs.put((_STOP, None))
        if self._thread.is_alive() and self._thread is not threading.current_thread():
            self._thread.join(timeout)

    def _open_stream(self, since: int | None) -> None:
        try:
            # The handle's one producer stream, shared with the run command listener (`run.command`): the server
            # keeps one per writer session, so two would replace each other.
            self._subscription = self._get_producer().follow(COMMAND_EVENT_KIND, self._take_event, since=since)
        except Exception as exc:  # noqa: BLE001 -- the beat backstop still delivers
            log.debug("probe: run %s: the command stream did not open: %s", self._run.id, exc)

    def _get_producer(self) -> Any:
        """The run handle's one producer stream (shared with its run command listener), else one of this
        listener's own for a handle that has none."""
        if self._producer is None:
            from ...commands.stream import ProducerStream

            shared = getattr(self._run, "_get_producer_stream", None)
            self._producer = shared() if callable(shared) else ProducerStream(self._run)
        return self._producer

    # -- on the stream's thread: hand off, never block it ------------------------------------------
    def _take_event(self, event: Any) -> None:
        if event.kind == COMMAND_EVENT_KIND and isinstance(event.data, dict):
            self._jobs.put(("notice", dict(event.data)))
        elif event.kind == "resync":
            self._jobs.put(("backstop", None))

    # -- on the listener's thread ------------------------------------------------------------------
    def _run_jobs(self) -> None:
        while True:
            job, payload = self._jobs.get()
            if job is _STOP:
                return
            try:
                if job == "baseline":
                    self._read_baseline()
                elif job == "backstop":
                    self._list_missed()
                else:
                    self._take_notice(payload)
            except Exception as exc:  # noqa: BLE001 -- fail open: the next beat lists again
                log.debug("probe: run %s: a command step failed (%s: %s)", self._run.id, type(exc).__name__, exc)

    def _read_baseline(self) -> None:
        if self._delivered is not None:
            return
        page = self._run._client.list_run_commands(str(self._run.id), after=_PAST_EVERY_SEQ, limit=1)
        self._mark_delivered(int(page.get("seq") or 0))

    def _take_notice(self, data: dict) -> None:
        seq = data.get("seq")
        if isinstance(seq, int):
            self._mark_delivered(seq)
        if data.get("state") == CommandState.OPEN.value:
            self._take(str(data.get("command_id")), data, seq if isinstance(seq, int) else None)

    def _list_missed(self) -> None:
        """A beat said the counter moved past what this process saw (or a claim failed on the way): list from
        there, by seq, and take what is open and held."""
        starts = [value for value in (self._delivered, self._retry_from) if value is not None]
        after: int | None = min(starts) if starts else 0
        self._retry_from = None
        client = self._run._client
        while after is not None:
            page = client.list_run_commands(str(self._run.id), after=after)
            for row in page.get("commands") or ():
                if row.get("state") == CommandState.OPEN.value:
                    self._take(str(row.get("id")), row, int(row["seq"]))
                self._mark_delivered(int(row["seq"]))
            self._mark_delivered(int(page.get("seq") or 0))
            after = page.get("next_after")

    def _take(self, command_id: str, data: dict, seq: int | None) -> None:
        """Claim an open sample command for an attempt this process holds, in its write epoch; run it; answer."""
        if command_id in self._handled or data.get("kind") not in SAMPLE_KINDS:
            return
        key = data.get("attempt_key")
        epoch = self._run.write_epoch or 1
        if not key or data.get("write_epoch") != epoch or not self._holds(str(key), str(data["kind"])):
            return
        client = self._run._client
        try:
            claimed = client.claim_run_command(str(self._run.id), command_id, self._session_id)
        except Exception:  # noqa: BLE001 -- not a 409: the next beat lists from before it and tries again
            if seq is not None:
                self._retry_from = min(seq - 1, self._retry_from if self._retry_from is not None else seq - 1)
            raise
        self._remember(command_id)
        if claimed is None:
            return  # another producer took it, or it ended
        answer = self._run_command(Command.model_validate(claimed))
        self._send_answer(command_id, answer)

    def _send_answer(self, command_id: str, answer: Answer) -> None:
        for attempt in range(ANSWER_TRIES):
            try:
                self._run._client.answer_run_command(
                    str(self._run.id), command_id, self._session_id, state=answer.state.value,
                    reason=answer.reason, result=answer.result,
                )  # fmt: skip
                return
            except Exception as exc:  # noqa: BLE001 -- unanswered, it reads `lost` once this lease ends
                if attempt == ANSWER_TRIES - 1:
                    log.debug("probe: run %s: answering command %s failed: %s", self._run.id, command_id, exc)

    def _mark_delivered(self, seq: int) -> None:
        self._delivered = seq if self._delivered is None else max(self._delivered, seq)

    def _remember(self, command_id: str) -> None:
        self._handled[command_id] = None
        while len(self._handled) > HANDLED_REMEMBERED:
            self._handled.pop(next(iter(self._handled)))


def _is_lease_refusal(error: BaseException | None) -> bool:
    """The stream stopped because the server did not see this writer's lease as live (a lapse; a beat renews it)."""
    detail = getattr(error, "detail", None)
    return isinstance(detail, dict) and detail.get("code") == WRITER_NOT_LIVE
