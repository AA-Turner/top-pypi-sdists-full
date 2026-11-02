from __future__ import annotations

import asyncio
import dataclasses
import datetime
import enum
import json
import sys
import time
import uuid
from collections.abc import AsyncIterator
from typing import TYPE_CHECKING, Any

import orjson
from matrx_utils import vcprint

from matrx_connect.context.data_types import DataPayload
from matrx_connect.context.events import (
    END_REASON_CANCELLED,
    END_REASON_ERROR,
    CitationPayload,
    ContextAnalysisPayload,
    ContextStatePayload,
    ContextTrimmedPayload,
    ControlTokenPayload,
    EndPayload,
    ErrorPayload,
    EventType,
    HeartbeatPayload,
    InfoPayload,
    InjectionConsumedPayload,
    ProviderRetryPayload,
    ReasoningPayload,
    ReasoningState,
    RecordReservedPayload,
    RecordUpdatePayload,
    ResourceAction,
    ResourceChangedPayload,
    StreamEvent,
    StructuredOutputPayload,
    ToolEventPayload,
    WarningPayload,
    build_event,
)
from matrx_connect.context.operations import CompletionPayload, InitPayload
from matrx_connect.context.phases import Phase, PhasePayload
from matrx_connect.emitters.control_tokens import ControlTokenFilter, ControlTokenHit
from matrx_connect.emitters.error_guard import ErrorEmissionGuard
from matrx_connect.emitters.log_truncation import is_scrape_data_log, truncate_strings_for_log
from matrx_connect.request_latency import (
    LATENCY_MARK_FIELD,
    RequestLatencyClock,
    claim_first_emit,
    note_first_emit,
)

if TYPE_CHECKING:
    from matrx_connect.streaming.journal import StreamJournalSink


#: THE SNAPSHOT DEFENSE (2026-09-09).
#:
#: Every provider streams visible text through ``send_chunk``, but they do not
#: all agree on what a "chunk" IS. Anthropic and OpenAI key off explicit
#: ``.delta`` fields, so each chunk is the NEW text. Others hand back the
#: running text so far — a growing SNAPSHOT — and forwarding those verbatim
#: replays the whole turn on every chunk: a ~6 KB answer arrives as hundreds of
#: kilobytes of stuttering duplicate ("Here is the", "Here is the raw sp", …),
#: which is exactly the shape observed in the 2026-09-08 Plan Room incident.
#:
#: This is the ONE seam every provider passes through on its way to a user's
#: wire, and the only one that already holds the accumulated turn text a
#: snapshot must be diffed against — so the defense lives here rather than
#: being re-implemented (and re-forgotten) in each provider adapter.
#:
#: A chunk is treated as a snapshot only when the accumulated turn text is at
#: least this long AND the chunk is a growing prefix-extension of it.
#:
#: The floor is deliberately LOW, and that is the whole design. Detection has to
#: land on the SECOND chunk of a turn or never: once a raw snapshot has been
#: forwarded, the accumulator is the concatenation of snapshots and no later
#: snapshot is a prefix of it any more. So the real comparison this makes is
#: "is chunk 2 a growing extension of chunk 1" — which is the exact signature of
#: a cumulative stream, and which a delta stream produces only if the model
#: literally repeated its own opening.
#:
#: The floor's remaining job is to refuse the degenerate openings where that
#: coincidence IS plausible: a first chunk of "\n" followed by "\n\n", or " "
#: followed by "  ". Three characters clears those without giving up detection.
#: A false positive costs one screamed-about duplicate prefix; a miss costs the
#: 2026-09-08 incident.
SNAPSHOT_MIN_ACCUMULATED = 3

#: The error-capture kind prefix. The resolved model is appended when the
#: ambient context knows it, so a burst of these names its own culprit.
SNAPSHOT_CAPTURE_KIND = "provider_stream_snapshot_not_delta"


class ProviderSentSnapshotNotDelta(Exception):
    """A provider streamed cumulative snapshots where the wire expects deltas.

    Raised only to carry a stack into ``capture_error`` — the stream is
    repaired in flight (only the new suffix is forwarded), never dropped. It
    screams once per emitter so a long run does not flood the queue, and it
    NEVER degrades silently: silent repair is how a provider adapter stays
    broken for months.
    """


class StreamEmitter:
    def __init__(self, debug: bool = False, heartbeat_interval: float = 5.0):
        self.queue: asyncio.Queue[str | bytes | None] = asyncio.Queue()
        self._latency_emit_clock: RequestLatencyClock | None = None
        # Every live wire item is retained until this emitter settles. A second
        # HTTP connection can replay the exact NDJSON already emitted and then
        # follow new items without a replay/follow gap. This is intentionally
        # process-local: the durable runtime spine remains the cross-process
        # recovery path, while this buffer restores token streaming instantly
        # when the detached task is still alive here.
        self._wire_replay: list[bytes] = []
        self._wire_subscribers: set[asyncio.Queue[bytes | None]] = set()
        self._wire_seq = 0
        # Token, tool, and heartbeat producers are independent coroutines.
        # Hold this through bounded sink admission so a later sequence cannot
        # overtake an earlier frame that yielded for backpressure.
        self._wire_publish_lock = asyncio.Lock()
        # PRE-WIRE STAGING — the reason an announcement made during request
        # PREP can no longer kill a response.
        #
        # Request preparation (tool merge, MCP attachment, sandbox arming,
        # surface resolution) runs BEFORE the NDJSON body opens and therefore
        # before ``attach_journal_sink``. Any frame published in that window
        # advanced ``_wire_seq``, and the journal attach that follows then
        # raised "journal must attach before first wire frame" from inside the
        # response generator — after headers were committed. The client saw an
        # HTTP 200 with an EMPTY body and nothing persisted (prod, 2026-09-13:
        # every chat with an attached MCP server).
        #
        # So the emitter, not each caller, owns the rule: while staging is
        # armed every frame is HELD (``_wire_seq`` stays 0, the journal can
        # still attach) and is flushed, in order, the moment the response body
        # opens the wire. ``None`` means the wire is open — the normal state
        # for emitters that never serve an HTTP body.
        self._wire_staging: list[str | bytes] | None = None
        self._ending = False
        self._stream_id: str | None = None
        self._journal_sink: StreamJournalSink | None = None
        # Set when a sink raised and was dropped. Delivery continued; only
        # cross-replica rejoin for this stream is gone.
        self._journal_detached_error: BaseException | None = None
        self._journal_detached_sink: StreamJournalSink | None = None
        self._primary_attached = True
        self.debug = debug
        self._ended = False
        # The reason word of the END frame this emitter published ("complete",
        # "error", "cancelled"), or None while the stream is open. Read by the
        # stream-run seam so a task that reported its own failure on the wire
        # settles its durable run as failed, never completed.
        self._end_reason: str | None = None
        self.cancelled = False
        # When True, a client disconnect MUST NOT cancel the work task. The task
        # keeps running to completion in the background (expensive / durable
        # pipelines: podcast, workflow runs, scraping, media generation). The
        # stream simply stops being read; the work — and all its DB writes —
        # finishes regardless. Set via create_streaming_response(detach_on_disconnect=True).
        self.detach_on_disconnect = False
        self._task: asyncio.Task[None] | None = None
        self._heartbeat_task: asyncio.Task[None] | None = None
        self._heartbeat_interval = heartbeat_interval
        # Liveness diagnostics — see _on_heartbeat_task_done / _heartbeat_loop.
        self._heartbeat_seq = 0
        self._heartbeat_restarts = 0
        self._heartbeat_stopped = False

        self._text_buffer: list[str] = []
        self._last_chunk_time: float = 0.0

        # Full assistant text streamed in the CURRENT turn (NOT cleared on flush,
        # unlike _text_buffer). The orchestrator resets it before each model call
        # and reads it on interrupt/cancel to persist the partial assistant turn
        # ("keep what the model said up to the cut"). Provider-agnostic: every
        # provider streams visible text through send_chunk.
        self._turn_text_acc: list[str] = []
        # Running length of _turn_text_acc — the O(1) gate that keeps the
        # snapshot check off the per-chunk hot path (a true delta is shorter
        # than the text before it, so the join below is never reached).
        self._turn_text_len: int = 0
        # The RAW provider text of the current turn — what the provider actually
        # sent, before control-token filtering. The snapshot defense compares
        # against THIS: a cumulative provider repeats its own output, which
        # includes any control line we stripped, so comparing against the
        # cleaned text would miss the repeat and replay the turn.
        self._raw_turn_text_acc: list[str] = []
        self._raw_turn_text_len: int = 0
        # WHAT REACHED A PERSON. Bumped by reset_turn_text so a cut recorded in
        # one turn is never applied to the next. ``_unread_from`` is set when
        # the LAST live reader (primary HTTP body or in-process replay) leaves:
        # (turn, chars of that turn already on the wire). A Stop arrives AFTER
        # the browser aborted its read (detach_on_disconnect keeps generating
        # until the cancel lands), so text past this point was never seen and
        # must not persist as the stopped answer (bench 2026-10-01, 360f1626…).
        self._turn_index: int = 0
        self._unread_from: tuple[int, int] | None = None
        # The page's own cursor (bench run 2, 2026-10-01, 6ca03037…): frames
        # already written to the socket when the browser aborted never reached
        # the page, so the reader-left mark alone still saved more than was
        # shown. The cancel carries the last ``stream_seq`` the client APPLIED;
        # ``_turn_chunk_marks`` maps each chunk frame of this turn to the
        # turn's text length on the wire after it.
        self.seen_seq: int | None = None
        self._turn_chunk_marks: list[tuple[int, int]] = []
        self._turn_wire_chars: int = 0
        # Snapshot defense state, both per RUN. Once a provider is caught
        # sending snapshots it keeps doing so, so `_snapshot_mode` drops the
        # length floor for every later turn (repair from the second chunk
        # instead of after 24 characters); `_snapshot_screamed` keeps the
        # capture to ONE per run instead of one per chunk.
        self._snapshot_mode: bool = False
        self._snapshot_screamed: bool = False
        # THE CONTROL-TOKEN FILTER — see matrx_connect/emitters/control_tokens.py.
        # Declared machine lines (``WRAP_RATING: 4``) are taken OUT of the
        # visible text here, at the one seam every provider passes through, and
        # re-emitted as structured ``control_token`` events. A renderer never
        # sees them, so no renderer ever needs a regex for them.
        self._control_filter = ControlTokenFilter()
        self._error_guard = ErrorEmissionGuard("StreamEmitter")

    # ------------------------------------------------------------------
    # Task / lifecycle management
    # ------------------------------------------------------------------

    def set_task(self, task: asyncio.Task[None]) -> None:
        self._task = task

    def set_detach_on_disconnect(self, value: bool) -> None:
        """Opt this stream's work task out of client-disconnect cancellation.

        Used for expensive / long-running / durable pipelines that must run to
        completion no matter what the browser does. When True, a client
        disconnect stops the OUTBOUND stream (the queue is no longer read) but
        leaves the work task running on the event loop until it finishes."""
        self.detach_on_disconnect = value

    def release_primary_reader(self) -> None:
        """No primary HTTP reader will ever drain ``queue`` (the client left
        before the body opened). Frames keep flowing to the replay buffer and
        rejoin subscribers; nothing piles up in a queue nobody reads."""
        self._primary_attached = False
        self._note_readers_changed()

    def _note_readers_changed(self) -> None:
        """Record where the wire stopped being read; clear it on a rejoin.

        A rejoin replays from the first frame, so a live reader means
        everything published so far is (or will be) seen. Cross-replica
        rejoins read the journal and are invisible here — for those the cut is
        conservative and the client keeps its longer screen (W-47 capture)."""
        if self._primary_attached or self._wire_subscribers:
            self._unread_from = None
        elif self._unread_from is None:
            on_wire = self._turn_text_len - sum(len(t) for t in self._text_buffer)
            self._unread_from = (self._turn_index, max(on_wire, 0))

    def note_seen_seq(self, seq: int) -> None:
        """The client's last APPLIED wire frame, sent with its Stop."""
        self.seen_seq = seq

    def get_seen_turn_text(self) -> str:
        """The current turn's text the person actually got.

        Cut at the earlier of: where the last live reader left, and the last
        frame the client says it applied (``seen_seq``). Equals
        ``get_turn_text()`` while anyone is reading and no cursor was sent.
        Used ONLY by a Stop: a detached run that finishes keeps everything."""
        text = self.get_turn_text()
        cut = len(text)
        if self._unread_from is not None:
            turn, chars = self._unread_from
            cut = min(cut, chars if turn == self._turn_index else 0)
        if self.seen_seq is not None:
            applied = 0
            for seq, chars in self._turn_chunk_marks:
                if seq > self.seen_seq:
                    break
                applied = chars
            cut = min(cut, applied)
        return text[:cut]

    @property
    def stream_id(self) -> str | None:
        """Immutable segment identity assigned by an optional durable sink."""
        return self._stream_id

    @property
    def has_ended(self) -> bool:
        """True once a terminal END frame has been published (or is being
        published). The crash handler in ``create_streaming_response`` reads
        this so a task that already terminalized its own stream never gets a
        SECOND terminal event bolted on behind it."""
        return self._ended or self._ending

    @property
    def end_reason(self) -> str | None:
        """The reason word on the END frame this emitter published, else None."""
        return self._end_reason

    def hold_wire_until_open(self) -> None:
        """Arm pre-wire staging: hold every frame until ``open_wire()``.

        Armed once per HTTP request, before any request-preparation code can
        run, so prep-phase announcements (MCP attachments, tool routing,
        sandbox arming) cannot advance the wire sequence ahead of the journal
        attach. Idempotent; a no-op once real frames are already on the wire.
        """
        if self._wire_seq or self._ended or self.cancelled:
            return
        if self._wire_staging is None:
            self._wire_staging = []

    def take_staged_wire(self) -> list[str | bytes]:
        """Open the wire and hand back everything staged, in the order produced.

        The streaming response calls this once the body has started and the
        journal sink (if any) is attached, then publishes the frames itself —
        AFTER the opening events, so ``connected`` stays the first frame on
        every wire while the prep-phase announcements still ride the journal
        and the replay buffer like any later frame.
        """
        staged = self._wire_staging or []
        self._wire_staging = None
        return staged

    def discard_staged_wire(self) -> int:
        """Drop staged frames for a request that will never stream a body.

        Returns how many were dropped. Never silent: an announcement that no
        client will ever see is reported so it cannot rot unnoticed.
        """
        staged = self._wire_staging or []
        self._wire_staging = None
        if staged:
            vcprint(
                f"[StreamEmitter] {len(staged)} staged pre-wire frame(s) dropped: "
                f"this request never opened a streaming body.",
                color="yellow",
            )
        return len(staged)

    def attach_journal_sink(self, sink: StreamJournalSink) -> None:
        """Attach before the first frame; a later attach would split one wire."""
        if self._wire_seq or self._journal_sink is not None:
            raise RuntimeError("StreamEmitter journal must attach before first wire frame")
        self._journal_sink = sink
        self._stream_id = sink.stream_id

    def start_heartbeat(self) -> None:
        if self._heartbeat_task is None or self._heartbeat_task.done():
            self._heartbeat_task = asyncio.create_task(self._heartbeat_loop())
            self._heartbeat_task.add_done_callback(self._on_heartbeat_task_done)

    def _stop_heartbeat(self) -> None:
        self._heartbeat_stopped = True
        if self._heartbeat_task and not self._heartbeat_task.done():
            self._heartbeat_task.cancel()

    def _on_heartbeat_task_done(self, task: asyncio.Task[None]) -> None:
        """The heartbeat is LIFE-CRITICAL for long streams: clients run a
        watchdog (~30s) and kill any stream with no bytes — a silently dead
        heartbeat task turns every long-running tool call into a spurious
        client-side "stream dead" error on a perfectly healthy run
        (observed in prod 2026-06-10). So a heartbeat task that ends while
        the stream is still alive is a defect: scream and auto-restart."""
        if self._ended or self.cancelled or self._heartbeat_stopped:
            return  # legitimate teardown
        if task.cancelled():
            reason = "canceled by an outside actor"
        else:
            exc = task.exception()
            reason = (
                f"crashed: {type(exc).__name__}: {exc}"
                if exc
                else "exited cleanly (loop condition flipped?)"
            )
        self._heartbeat_restarts += 1
        print(
            f"[StreamEmitter] HEARTBEAT TASK DIED MID-STREAM ({reason}) — "
            f"restart #{self._heartbeat_restarts}. A dead heartbeat makes client "
            f"watchdogs kill healthy streams; this must be root-caused.",
            file=sys.stderr,
            flush=True,
        )
        if self._heartbeat_restarts <= 20:  # backstop against a crash loop
            self.start_heartbeat()

    async def _heartbeat_loop(self) -> None:
        try:
            while not self._ended and not self.cancelled:
                before = time.monotonic()
                await asyncio.sleep(self._heartbeat_interval)
                # Late wake-up = the event loop was starved (sync work blocked
                # it). Surface the evidence on the beat itself AND on stderr —
                # starvation also delays every OTHER event on this worker.
                late_by = (time.monotonic() - before) - self._heartbeat_interval
                if not self._ended and not self.cancelled:
                    self._heartbeat_seq += 1
                    payload = HeartbeatPayload(
                        seq=self._heartbeat_seq,
                        late_by_seconds=(
                            round(late_by, 3) if late_by > self._heartbeat_interval else None
                        ),
                    )
                    if late_by > self._heartbeat_interval:
                        print(
                            f"[StreamEmitter] heartbeat #{self._heartbeat_seq} fired "
                            f"{late_by:.1f}s late — event loop starvation "
                            f"(synchronous work is blocking this worker).",
                            file=sys.stderr,
                            flush=True,
                        )
                    event = build_event(EventType.HEARTBEAT, payload)
                    await self._publish_wire(event.to_jsonl())
        except asyncio.CancelledError:
            pass

    async def generate(self):
        self.start_heartbeat()
        try:
            while True:
                try:
                    item = await asyncio.wait_for(self.queue.get(), timeout=1.0)
                except TimeoutError:
                    # Drain whatever is still queued before checking if done.
                    # Without this, a fast task that finishes while we're in
                    # wait_for would cause us to exit with items still in the
                    # queue (data + end events never yielded to the client).
                    while not self.queue.empty():
                        queued = self.queue.get_nowait()
                        if queued is None:
                            return
                        yield queued
                    if self._task and self._task.done():
                        break
                    continue

                if item is None:
                    break
                yield item
        except (GeneratorExit, asyncio.CancelledError):
            # In detach mode the work task OWNS its own lifecycle — a client
            # disconnect must never cancel it OR disable its emitter. The old
            # `cancelled=True` assignment silently discarded every later token,
            # making a live reattach impossible even though the paid work kept
            # running. Stop only this primary reader; replay subscribers can
            # attach immediately and the producer keeps publishing.
            self._primary_attached = False
            self._note_readers_changed()
            if not self.detach_on_disconnect:
                self.cancelled = True
            if self._task and not self._task.done() and not self.detach_on_disconnect:
                self._task.cancel()
        finally:
            if self._ended or self.cancelled or not self.detach_on_disconnect:
                self._stop_heartbeat()

    async def generate_replay(self) -> AsyncIterator[bytes]:
        """Replay this live stream, then follow it to terminal.

        Subscribe-before-snapshot is deliberate: publishing contains no await
        between appending to the replay list and fan-out, so one event can
        never fall into the replay/follow seam. Every item carries a monotonic
        ``stream_seq``; reconnecting clients drop frames they already applied.
        """
        queue: asyncio.Queue[bytes | None] = asyncio.Queue()
        self._wire_subscribers.add(queue)
        self._note_readers_changed()
        replay = list(self._wire_replay)
        ended = self._ended
        try:
            for item in replay:
                yield item
            if ended:
                return
            while True:
                item = await queue.get()
                if item is None:
                    return
                yield item
        finally:
            self._wire_subscribers.discard(queue)
            self._note_readers_changed()

    # ------------------------------------------------------------------
    # Internal emit
    # ------------------------------------------------------------------

    async def publish_wire(self, item: str | bytes) -> None:
        """Publish an already-canonical NDJSON frame (used for response opening)."""
        await self._publish_wire(item)

    async def _publish_wire(self, item: str | bytes) -> None:
        """Sequence, retain, and fan out one canonical NDJSON frame."""
        async with self._wire_publish_lock:
            if self._ending:
                return
            await self._publish_wire_locked(item)

    async def _publish_wire_locked(self, item: str | bytes) -> None:
        """Publish while ``_wire_publish_lock`` is held."""
        if self._wire_staging is not None:
            # The body has not opened yet: hold the frame instead of burning a
            # sequence number the journal attach would then refuse. See
            # ``_wire_staging`` in __init__.
            self._wire_staging.append(item)
            return
        self._wire_seq += 1
        payload = orjson.loads(item)
        if not isinstance(payload, dict):
            raise TypeError("StreamEmitter wire events must be JSON objects")
        payload["stream_seq"] = self._wire_seq
        if payload.get("e") == "c":
            self._turn_wire_chars += len(payload.get("t") or "")
            self._turn_chunk_marks.append((self._wire_seq, self._turn_wire_chars))
        if self._stream_id is not None:
            payload["stream_id"] = self._stream_id
        # LEG 3 of the request's latency (request_latency.RequestLatencyClock): the FIRST
        # frame written after the provider responded carries the request's latency id, and
        # its write time is stamped once the frame is actually handed to the reader.
        if payload.get("event") != "heartbeat":
            clock = claim_first_emit()
            if clock is not None:
                payload[LATENCY_MARK_FIELD] = clock.latency_id
                self._latency_emit_clock = clock
        # orjson writes U+2028/U+2029 raw inside strings; Unicode-aware line
        # splitters (str.splitlines, some JS readers) then tear one event into
        # two. Escaping is still valid JSON with an identical parsed value.
        encoded = (
            orjson.dumps(payload).replace(b"\xe2\x80\xa8", b"\\u2028").replace(b"\xe2\x80\xa9", b"\\u2029")
            + b"\n"
        )
        sink = self._journal_sink
        if sink is not None:
            # THE JOURNAL IS A SINK, NOT A GATE. It buys cross-replica rejoin;
            # it does not own whether this response happens. A sink that raises
            # would otherwise travel up through send_chunk/send_tool_event into
            # the agent executor and kill a paid, mid-flight run — and then kill
            # fatal_error's own emit, leaving the screen silent. Detach the sink
            # on its first raise and deliver directly from here on.
            try:
                await sink.enqueue(
                    sequence=self._wire_seq,
                    wire=encoded,
                    publish=self._publish_committed,
                )
                return
            except asyncio.CancelledError:
                raise
            except Exception as exc:  # noqa: BLE001
                self._detach_journal_sink(exc, "enqueue")
        await self._publish_committed(encoded)

    def _detach_journal_sink(self, exc: BaseException, stage: str) -> None:
        """Drop a sink that raised, once, loudly. Delivery continues without it."""
        if self._journal_sink is None:
            return
        # Keep the reference: a sink usually owns a background writer task, and
        # dropping it on the floor would leave that task parked on its queue for
        # the life of the process. send_end still gives it one guarded chance to
        # terminalize itself.
        self._journal_detached_sink = self._journal_sink
        self._journal_sink = None
        self._journal_detached_error = exc
        vcprint(
            f"[StreamEmitter] journal sink raised during {stage} "
            f"({type(exc).__name__}: {exc}) — DETACHED. This stream keeps "
            f"delivering; cross-replica rejoin for it is gone.",
            color="red",
        )

    async def _publish_committed(self, encoded: bytes) -> None:
        """The sole local fan-out point; journal sinks call only after commit."""
        self._wire_replay.append(encoded)
        if self._latency_emit_clock is not None:
            note_first_emit(self._latency_emit_clock)
            self._latency_emit_clock = None
        # Fan out in the same synchronous section as the replay append. A
        # rejoiner subscribes before taking its replay snapshot, so keeping
        # this seam await-free guarantees the frame appears in exactly one of
        # those two places.
        for subscriber in tuple(self._wire_subscribers):
            subscriber.put_nowait(encoded)
        if self._primary_attached:
            await self.queue.put(encoded)

    async def _finish_wire(self) -> None:
        if self._primary_attached:
            await self.queue.put(None)
        for subscriber in tuple(self._wire_subscribers):
            subscriber.put_nowait(None)

    def _serialize(self, data: Any) -> Any:
        if data is None or isinstance(data, bool | int | float | str):
            return data
        if isinstance(data, datetime.datetime | datetime.date):
            return data.isoformat()
        if isinstance(data, uuid.UUID):
            return str(data)
        if isinstance(data, enum.Enum):
            return data.value
        if dataclasses.is_dataclass(data) and not isinstance(data, type):
            return self._serialize(dataclasses.asdict(data))
        if isinstance(data, set | tuple):
            return [self._serialize(item) for item in data]
        if isinstance(data, dict):
            return {key: self._serialize(value) for key, value in data.items()}
        if isinstance(data, list):
            return [self._serialize(item) for item in data]
        if hasattr(data, "model_dump"):
            # Recurse: model_dump() output can still nest datetimes/UUIDs/enums
            # (e.g. extra="allow" event payloads carrying DB rows), and the
            # legacy path json.dumps()es the result with no default.
            return self._serialize(data.model_dump())
        return str(data)

    async def _flush_text(self) -> None:
        if self._text_buffer:
            combined = "".join(self._text_buffer)
            self._text_buffer.clear()
            await self._publish_wire(orjson.dumps({"e": "c", "t": combined}) + b"\n")

    async def _emit_event(self, event: StreamEvent) -> None:
        if self._text_buffer:
            await self._flush_text()
        if self._ended or self.cancelled:
            return
        await self._publish_wire(event.to_jsonl())

    async def _emit_raw(self, event_type: EventType, data: dict[str, Any]) -> None:
        if self._text_buffer:
            await self._flush_text()
        if self._ended or self.cancelled:
            return
        payload = {"event": event_type.value, "data": data}
        await self._publish_wire(json.dumps(payload) + "\n")

    # ------------------------------------------------------------------
    # Public API — one method per canonical event type
    # ------------------------------------------------------------------

    def reset_turn_text(self) -> None:
        """Clear the current-turn accumulator. The orchestrator calls this right
        before each model call so the accumulator holds only the in-flight turn."""
        self._turn_index += 1
        self._turn_chunk_marks = []
        self._turn_wire_chars = 0
        self._turn_text_acc = []
        self._turn_text_len = 0
        self._raw_turn_text_acc = []
        self._raw_turn_text_len = 0
        self._control_filter.start_line()

    def configure_control_tokens(
        self, *, mandate_key: str | None = None, enabled: bool | None = None
    ) -> None:
        """THE KNOB. Point this stream at a mandate (so that mandate's registry
        override applies) and/or turn filtering off for this stream entirely.

        ``enabled=False`` is for a consumer that parses the control lines out of
        the raw text itself — a machine-only transcript. It is never the answer
        to "a client needs the value": the value is on the structured
        ``control_token`` event, which is the whole point.
        """
        self._control_filter.configure(mandate_key=mandate_key, enabled=enabled)

    @property
    def control_tokens_enabled(self) -> bool:
        return self._control_filter.enabled

    async def send_control_token(
        self, name: str, value: str, declared_by: str | None = None
    ) -> None:
        """Emit one declared control token on the structured channel.

        The ONLY way a control value reaches a consumer. Callers that hold their
        own text path (the block-streaming wrapper) route through here rather
        than putting the line back into anyone's prose.
        """
        await self._emit_control_tokens(
            (ControlTokenHit(name=name, value=value, declared_by=declared_by or ""),)
        )

    async def _emit_control_tokens(self, hits: tuple[ControlTokenHit, ...]) -> None:
        for hit in hits:
            vcprint(
                {"name": hit.name, "value": hit.value, "declared_by": hit.declared_by},
                "[Stream Emitter] Control token (stripped from visible text)",
                color="yellow",
                verbose=self.debug,
            )
            event = build_event(
                EventType.CONTROL_TOKEN,
                ControlTokenPayload(
                    name=hit.name, value=hit.value, declared_by=hit.declared_by or None
                ),
            )
            await self._emit_event(event)

    async def flush_control_tokens(self) -> None:
        """Release the filter's held partial line — a control line or text.

        Called at END. A stream that stops mid-line never loses those bytes:
        they are emitted verbatim unless they completed a declared token.
        """
        if not self._control_filter.has_pending:
            return
        filtered = self._control_filter.flush()
        if filtered.hits:
            await self._emit_control_tokens(filtered.hits)
        if filtered.text and not (self._ended or self.cancelled):
            self._text_buffer.append(filtered.text)
            self._turn_text_acc.append(filtered.text)
            self._turn_text_len += len(filtered.text)
            await self._flush_text()

    @property
    def provider_sent_snapshots(self) -> bool:
        """True once this run caught a provider streaming cumulative snapshots."""
        return self._snapshot_mode

    def get_turn_text(self) -> str:
        """The assistant text streamed so far in the current turn — used to
        persist a partial assistant message when a run is interrupted."""
        return "".join(self._turn_text_acc)

    async def _reduce_snapshot_to_delta(self, text: str) -> str:
        """Return the NEW text in ``text``, screaming once if it was a snapshot.

        A provider that hands back the running text so far (rather than the new
        text) would otherwise replay the whole turn on every chunk. When the
        incoming chunk is a strict growing-prefix extension of what this turn
        has already emitted, only the suffix goes to the wire — and the first
        time it happens the run screams through the error-capture system, so
        the broken adapter is named instead of silently compensated for.

        A chunk that is NOT a prefix-extension is returned untouched: this
        never guesses, and it never drops text it does not recognize.
        """
        accumulated = "".join(self._raw_turn_text_acc)
        if not text.startswith(accumulated):
            return text
        suffix = text[len(accumulated) :]
        self._snapshot_mode = True
        if not self._snapshot_screamed:
            self._snapshot_screamed = True
            await self._scream_snapshot(accumulated_len=len(accumulated), chunk_len=len(text))
        return suffix

    async def _scream_snapshot(self, *, accumulated_len: int, chunk_len: int) -> None:
        """One capture per run naming the provider/model that sent snapshots."""
        model = "unattributed"
        source_app = source_feature = None
        try:
            from matrx_connect.context.app_context import try_get_app_context

            ctx = try_get_app_context()
            if ctx is not None:
                source_app = getattr(ctx, "source_app", None)
                source_feature = getattr(ctx, "source_feature", None)
                metadata = getattr(ctx, "metadata", None)
                if isinstance(metadata, dict):
                    model = str(metadata.get("initial_model") or model)
        except Exception:  # noqa: BLE001 — attribution must never break the stream
            pass

        exc = ProviderSentSnapshotNotDelta(
            f"A provider streamed a CUMULATIVE SNAPSHOT ({chunk_len} chars) where the "
            f"wire expects a delta ({accumulated_len} chars already sent). The stream "
            "has been repaired in flight — only the new suffix reached the client — "
            "but the provider adapter is emitting the wrong thing and must be fixed "
            "to key off its explicit delta field."
        )
        vcprint(
            f"[Stream Emitter] PROVIDER SENT A SNAPSHOT, NOT A DELTA "
            f"(model={model}, accumulated={accumulated_len}, chunk={chunk_len}). "
            "Forwarding only the new suffix; see capture kind "
            f"'{SNAPSHOT_CAPTURE_KIND}'.",
            color="red",
        )
        try:
            from matrx_connect.streaming.error_capture import capture_error

            # The capture sink takes a FIXED keyword surface (record_error);
            # anything else belongs in `context`. Passing model/accumulated_chars
            # as top-level kwargs raised TypeError inside the sink and this
            # scream was never filed at all.
            await capture_error(
                exc,
                kind=f"{SNAPSHOT_CAPTURE_KIND}:{model}",
                source_app=source_app,
                source_feature=source_feature,
                context={
                    "model": model,
                    "accumulated_chars": accumulated_len,
                    "chunk_chars": chunk_len,
                },
            )
        except Exception:  # noqa: BLE001 — the console scream above still stands
            pass

    async def send_chunk(self, text: str) -> None:
        if self._ended or self.cancelled:
            return
        # THE SNAPSHOT DEFENSE — see SNAPSHOT_MIN_ACCUMULATED above. The length
        # comparison is the whole hot path for a well-behaved provider: a real
        # delta is shorter than everything before it, so nothing else runs.
        # It runs on the RAW provider text, before control-token filtering:
        # a snapshot repeats what the provider sent, not what we forwarded.
        floor = 1 if self._snapshot_mode else SNAPSHOT_MIN_ACCUMULATED
        if text and self._raw_turn_text_len >= floor and len(text) >= self._raw_turn_text_len:
            text = await self._reduce_snapshot_to_delta(text)
            if not text:
                return
        self._raw_turn_text_acc.append(text)
        self._raw_turn_text_len += len(text)

        # THE CONTROL-TOKEN FILTER. Declared machine lines never reach the wire
        # or the turn accumulator (which is what persists a partial turn), and
        # their values ride the structured channel instead.
        filtered = self._control_filter.feed(text)
        if filtered.hits:
            await self._emit_control_tokens(filtered.hits)
            if self._ended or self.cancelled:
                return
        text = filtered.text
        if not text:
            return

        self._text_buffer.append(text)
        self._turn_text_acc.append(text)
        self._turn_text_len += len(text)

        now = asyncio.get_event_loop().time()
        # Flush if we cross 25 chars or 15ms elapsed
        if sum(len(t) for t in self._text_buffer) > 25 or (now - self._last_chunk_time) > 0.015:
            await self._flush_text()
            self._last_chunk_time = now

    async def send_reasoning_chunk(self, text: str) -> None:
        if self._text_buffer:
            await self._flush_text()
        if self._ended or self.cancelled:
            return
        await self._publish_wire(orjson.dumps({"e": "r", "t": text}) + b"\n")

    async def send_reasoning_state(self, state: ReasoningState) -> None:
        """Content-less reasoning lifecycle signal ('started' / 'stopped'). Low
        frequency (once or twice a turn) so it rides the normal event form, not
        the compact chunk shape. Providers emit 'started' at the reasoning
        block open — even when reasoning text is suppressed — so the UI can show
        a thinking state instead of a silent heartbeat gap."""
        vcprint({"state": state}, "[Stream Emitter] Reasoning", color="blue", verbose=self.debug)
        event = build_event(EventType.REASONING, ReasoningPayload(state=state))
        await self._emit_event(event)

    async def send_phase(self, phase: Phase) -> None:
        vcprint({"phase": phase}, "[Stream Emitter] Phase", color="blue", verbose=self.debug)
        event = build_event(EventType.PHASE, PhasePayload(phase=phase))
        await self._emit_event(event)

    async def send_warning(self, payload: WarningPayload) -> None:
        """Emit a WARNING event. USE THIS (not send_error) whenever:

        - Any response content has already been streamed to the client, OR
        - The condition describes a caveat about an otherwise-delivered
          response (``finish_reason`` was ``MAX_TOKENS`` / unexpected / etc.),
          OR
        - The condition describes a failure of a post-response side effect
          (snapshot write, labeling, caching) that the user does not need
          to see.

        A WARNING decorates a response — it never invalidates it. The UI
        should render it as an advisory notice, not a failure state.
        See ``send_error`` for the complementary rule.
        """
        vcprint(
            {"code": payload.code, "level": payload.level, "message": payload.system_message},
            "[Stream Emitter] Warning",
            color="yellow",
        )
        event = build_event(EventType.WARNING, payload)
        await self._emit_event(event)

    async def send_info(self, payload: InfoPayload) -> None:
        vcprint(
            {"code": payload.code, "message": payload.system_message},
            "[Stream Emitter] Info",
            color="blue",
            verbose=self.debug,
        )
        event = build_event(EventType.INFO, payload)
        await self._emit_event(event)

    async def send_data(self, payload: DataPayload | dict[str, Any] | Any) -> None:
        if isinstance(payload, DataPayload):
            log_payload = payload.model_dump()
            if is_scrape_data_log(log_payload):
                log_payload = truncate_strings_for_log(log_payload)
            vcprint(log_payload, "[Stream Emitter] Data", color="blue", verbose=self.debug)
            event = build_event(EventType.DATA, payload)
            await self._emit_event(event)
        else:
            # Large legacy payloads can contain thousands of nested rows.
            # Recursive coercion is CPU work and must not freeze the request loop.
            serialized = await asyncio.to_thread(self._serialize, payload)
            if not isinstance(serialized, dict):
                serialized = {"value": serialized}
            log_payload = serialized
            if is_scrape_data_log(log_payload):
                log_payload = truncate_strings_for_log(log_payload)
            vcprint(
                log_payload,
                "[Stream Emitter] Data (legacy)",
                color="yellow",
                verbose=self.debug,
            )
            await self._emit_raw(EventType.DATA, serialized)

    async def send_init(self, payload: InitPayload) -> None:
        vcprint(
            {"operation": payload.operation, "operation_id": payload.operation_id},
            "[Stream Emitter] Init",
            color="blue",
            verbose=self.debug,
        )
        event = build_event(EventType.INIT, payload)
        await self._emit_event(event)

    async def send_completion(self, payload: CompletionPayload) -> None:
        color = (
            "green"
            if payload.status == "success"
            else "red"
            if payload.status == "failed"
            else "blue"
        )
        vcprint(
            {
                "operation": payload.operation,
                "operation_id": payload.operation_id,
                "status": payload.status,
            },
            "[Stream Emitter] Completion",
            color=color,
            verbose=self.debug,
        )
        event = build_event(EventType.COMPLETION, payload)
        await self._emit_event(event)

    async def send_error(
        self,
        error_type: str,
        message: str,
        user_message: str | None = None,
        code: str | None = None,
        details: dict[str, Any] | None = None,
    ) -> None:
        """Emit an ERROR event. USE THIS ONLY when the response itself has
        failed to reach the client — API exceptions before any chunk is
        streamed, stream-level errors that corrupt the payload in flight,
        auth/rate-limit rejections, or hard cancellations.

        DO NOT use this for:

        - Truncation or unexpected ``finish_reason`` *after* chunks have
          already been streamed. The content is valid; the condition is a
          caveat. Use ``send_warning`` instead.
        - Post-response side-effect failures (snapshot writes, conversation
          labeling, cache refreshes). These must never reach the user
          stream; log them and move on.
        - "Nice to know" model metadata (refusals that produced content,
          safety flags, etc.). Use ``send_warning``.

        The rule: an ERROR invalidates the response the client believes it
        received. If the client already received usable content, this is
        the wrong event type — and the UI will display an incorrect
        failure state.
        """
        if not self._error_guard.claim(error_type):
            return
        vcprint(
            {"error_type": error_type, "message": message},
            "[Stream Emitter] Error",
            color="red",
        )
        event = build_event(
            EventType.ERROR,
            ErrorPayload(
                error_type=error_type,
                message=message,
                user_message=user_message or message,
                code=code,
                details=self._serialize(details) if details else None,
            ),
        )
        await self._emit_event(event)

    async def send_tool_event(self, event_data: ToolEventPayload | dict[str, Any]) -> None:
        if isinstance(event_data, dict):
            payload = ToolEventPayload.model_validate(event_data)
        else:
            payload = event_data
        color = (
            "red"
            if payload.event == "tool_error"
            else "green"
            if payload.event == "tool_completed"
            else "blue"
        )
        vcprint(payload, "[Stream Emitter] Tool Event", color=color, verbose=self.debug)
        event = build_event(EventType.TOOL_EVENT, payload)
        await self._emit_event(event)

    async def send_record_reserved(self, payload: RecordReservedPayload) -> None:
        vcprint(
            {"table": payload.table, "record_id": payload.record_id},
            "[Stream Emitter] Record Reserved",
            color="blue",
            verbose=self.debug,
        )
        event = build_event(EventType.RECORD_RESERVED, payload)
        await self._emit_event(event)

    async def send_record_update(self, payload: RecordUpdatePayload) -> None:
        color = (
            "green"
            if payload.status in ("active", "completed")
            else "red"
            if payload.status == "failed"
            else "blue"
        )
        vcprint(
            {"table": payload.table, "record_id": payload.record_id, "status": payload.status},
            "[Stream Emitter] Record Update",
            color=color,
            verbose=self.debug,
        )
        event = build_event(EventType.RECORD_UPDATE, payload)
        await self._emit_event(event)

    async def send_resource_changed(
        self,
        *,
        kind: str,
        action: ResourceAction,
        resource_id: str,
        sandbox_id: str | None = None,
        user_id: str | None = None,
        metadata: dict[str, Any] | None = None,
    ) -> None:
        """Emit a RESOURCE_CHANGED event — generic "something the client may
        care about changed; refetch if you're displaying it" notification.

        Distinct from ``send_record_update`` (matrx-orm rows specifically)
        and ``send_data`` (which carries actual content, not change hints).
        Use this for filesystem mutations inside sandboxes, cache
        invalidations, cross-process state changes — anything where the
        client should reconcile its view but the server isn't shipping the
        new value inline.

        ``kind`` is namespaced ("fs.file", "cld_files", "cache.<key>", …) and
        opaque to matrx-connect; consumers register their own conventions.
        On move/rename, ``resource_id`` is the NEW identifier — put the
        old one in ``metadata.previous_id``.
        """
        payload = ResourceChangedPayload(
            kind=kind,
            action=action,
            resource_id=resource_id,
            sandbox_id=sandbox_id,
            user_id=user_id,
            metadata=metadata or {},
        )
        vcprint(
            {"kind": kind, "action": action, "resource_id": resource_id},
            "[Stream Emitter] Resource Changed",
            color="cyan",
            verbose=self.debug,
        )
        event = build_event(EventType.RESOURCE_CHANGED, payload)
        await self._emit_event(event)

    async def send_structured_output(self, payload: StructuredOutputPayload) -> None:
        """Emit a STRUCTURED_OUTPUT event — agent's final assistant text parsed
        against its declared ``output_schema``.

        Fired automatically by ``matrx_ai.agents.Agent.execute`` when the
        agent has a schema and the execution loop has produced its final
        message. The payload carries the full schema AND the parsed value so
        the FE can drive generic renderers without re-running extraction or
        re-fetching the agent record. Fires whether extraction succeeded or
        failed — ``success=False`` is the signal that the agent declared a
        contract and the parser couldn't honor it.
        """
        vcprint(
            {
                "schema_name": payload.schema_name,
                "success": payload.success,
                "match_count": payload.match_count,
                "agent_name": payload.agent_name,
                "operation_id": payload.operation_id,
            },
            "[Stream Emitter] Structured Output",
            color="green" if payload.success else "yellow",
            verbose=self.debug,
        )
        event = build_event(EventType.STRUCTURED_OUTPUT, payload)
        await self._emit_event(event)

    async def send_injection_consumed(self, payload: InjectionConsumedPayload) -> None:
        """Emit an INJECTION_CONSUMED event — queued Turn-Boundary Inbox item(s)
        were drained into the running conversation at a turn boundary. Lets the
        FE reflect 'your queued message was delivered' without polling."""
        vcprint(
            {"conversation_id": payload.conversation_id, "count": payload.count},
            "[Stream Emitter] Injection Consumed",
            color="cyan",
            verbose=self.debug,
        )
        event = build_event(EventType.INJECTION_CONSUMED, payload)
        await self._emit_event(event)

    async def send_citation(self, payload: CitationPayload) -> None:
        """Emit a CITATION event — one normalized citation attached to the
        streaming answer (live via provider citation deltas/annotations, or at
        settle for terminal-only providers like Gemini grounding)."""
        vcprint(
            {
                "block_index": payload.block_index,
                "kind": payload.citation.get("kind"),
                "title": payload.citation.get("title"),
            },
            "[Stream Emitter] Citation",
            color="cyan",
            verbose=self.debug,
        )
        event = build_event(EventType.CITATION, payload)
        await self._emit_event(event)

    async def send_provider_retry(self, payload: ProviderRetryPayload) -> None:
        vcprint(
            {
                "state": payload.state,
                "provider": payload.provider,
                "attempt": payload.failed_attempt,
                "next": payload.next_attempt,
                "delay": payload.retry_delay,
                "error_type": payload.error_type,
                "request_id": payload.request_id,
                "conversation_id": payload.conversation_id,
            },
            "[Stream Emitter] Provider Retry",
            color="yellow" if payload.state != "recovered" else "green",
            verbose=self.debug,
        )
        event = build_event(EventType.PROVIDER_RETRY, payload)
        await self._emit_event(event)

    async def send_context_analysis(self, payload: ContextAnalysisPayload) -> None:
        """Emit a CONTEXT_ANALYSIS event — wire-level snapshot of one
        outbound provider HTTP request.

        Only ever fired by ``matrx_ai.providers.outbound_capture`` when the
        active ``AppContext.snapshot`` flag is True. The payload carries
        the literal HTTP request shape (URL / method / headers / body) so
        operators can audit exactly what each provider received on each
        iteration. Auth headers must already be redacted by the caller.
        """
        vcprint(
            {
                "provider": payload.provider,
                "model": payload.model,
                "iteration": payload.iteration,
                "url": payload.url,
                "body_size_bytes": payload.body_size_bytes,
                "is_streaming": payload.is_streaming,
            },
            "[Stream Emitter] Context Analysis",
            color="magenta",
            verbose=self.debug,
        )
        event = build_event(EventType.CONTEXT_ANALYSIS, payload)
        await self._emit_event(event)

    async def send_context_state(self, payload: ContextStatePayload) -> None:
        """Emit a CONTEXT_STATE event — snapshot of what the model is seeing.

        Fired after each persisted turn by ``matrx_ai.db.persistence``. The
        FE Model Context tab consumes this into ``context-state`` Redux
        slice to drive the live gauge and per-message size badges.
        """
        vcprint(
            {
                "conv": payload.conversation_id[:8] + "…",
                "chars": payload.total_chars_visible_to_model,
                "msgs": payload.message_count_visible,
                "input": payload.last_request_input_tokens,
                "cached": payload.last_request_cached_tokens,
            },
            "[Stream Emitter] Context State",
            color="cyan",
            verbose=self.debug,
        )
        event = build_event(EventType.CONTEXT_STATE, payload)
        await self._emit_event(event)

    async def send_context_trimmed(self, payload: ContextTrimmedPayload) -> None:
        """Emit a CONTEXT_TRIMMED event — audit of a trim_messages_context pass.

        Fires when blocks were rewritten OR when the cache-aware gate
        skipped an eligible pass. Renders in the "What just happened"
        section of the FE Model Context tab.
        """
        ts = payload.trim_summary or {}
        vcprint(
            {
                "conv": payload.conversation_id[:8] + "…",
                "rewritten": ts.get("blocks_rewritten", 0),
                "freed": ts.get("freed_chars", 0),
                "skipped": ts.get("eligible_but_skipped_reason"),
            },
            "[Stream Emitter] Context Trimmed",
            color="yellow",
            verbose=self.debug,
        )
        event = build_event(EventType.CONTEXT_TRIMMED, payload)
        await self._emit_event(event)

    async def send_end(self, reason: str = "complete") -> None:
        if self._control_filter.has_pending:
            await self.flush_control_tokens()
        if self._text_buffer:
            await self._flush_text()
        if not self._ended:
            color = "green" if reason == "complete" else "blue"
            vcprint({"reason": reason}, "[Stream Emitter] End", color=color, verbose=self.debug)
            async with self._wire_publish_lock:
                if self._ending:
                    return
                self._ending = True
                self._end_reason = reason
                event = build_event(EventType.END, EndPayload(reason=reason))
                await self._publish_wire_locked(event.to_jsonl())
                self._ended = True
            self._stop_heartbeat()
            sink = self._journal_sink
            if sink is not None:
                try:
                    await sink.close(
                        # END is replayable whether the domain work completed,
                        # canceled, or returned an application error. ``failed``
                        # is reserved for a journal/storage failure or truncation.
                        status="closed",
                        last_seq=self._wire_seq,
                    )
                except asyncio.CancelledError:
                    raise
                except Exception as exc:  # noqa: BLE001
                    # _finish_wire below is what puts the terminator on the
                    # client's queue. A raising sink close used to skip it, so
                    # the browser sat on an open stream that would never end —
                    # the screen froze mid-turn with no error at all.
                    self._detach_journal_sink(exc, "close")
            elif self._journal_detached_sink is not None:
                # A sink detached mid-stream still owns a writer task. Give it
                # one guarded chance to flush and stop rather than leaking it.
                detached, self._journal_detached_sink = self._journal_detached_sink, None
                try:
                    await detached.close(status="failed", last_seq=self._wire_seq)
                except asyncio.CancelledError:
                    raise
                except Exception as exc:  # noqa: BLE001
                    vcprint(
                        f"[StreamEmitter] detached journal sink could not close "
                        f"({type(exc).__name__}: {exc}); its writer may linger "
                        f"until the process ends.",
                        color="yellow",
                    )
            await self._finish_wire()

    async def abandon(self) -> int:
        """Stop publishing WITHOUT a terminal END, because the work continues elsewhere.

        For a stream whose producer hands the operation to another runner (a
        crash-recovery attempt interrupted by shutdown, or one that will be retried):
        an END would tell every reader the turn is over. Stops the heartbeat,
        refuses further frames, releases local readers, and returns the last
        wire sequence so the owner can hand its journal segment over. The journal
        sink is left to the owner.
        """
        async with self._wire_publish_lock:
            self._ending = True
        self._stop_heartbeat()
        await self._finish_wire()
        return self._wire_seq

    async def send_cancelled(self) -> None:
        await self.send_error(
            error_type="task_cancelled",
            message="Task was canceled.",
            user_message="Your request was canceled.",
        )
        await self.send_end(reason=END_REASON_CANCELLED)

    async def fatal_error(
        self,
        error_type: str,
        message: str,
        user_message: str | None = None,
        code: str | None = None,
        details: dict[str, Any] | None = None,
    ) -> None:
        from matrx_connect.reservations import try_get_tracker

        tracker = try_get_tracker()
        if tracker:
            try:
                await tracker.fail_all_pending(self)
            except Exception as tracker_exc:
                vcprint(
                    f"[StreamEmitter] fail_all_pending raised during fatal_error: {tracker_exc}",
                    color="yellow",
                )
        await self.send_error(error_type, message, user_message, code, details)
        # A FATAL error must not terminate the wire with a success word. The
        # default reason is "complete", so this used to hand the client an
        # error frame followed by `{"reason":"complete"}` — and any consumer
        # that trusts the terminal event (or whose error frame was suppressed
        # because the stream had already ended) read a clean, empty success.
        await self.send_end(reason=END_REASON_ERROR)


# Active delivery registry -------------------------------------------------
#
# A detached work task is still alive inside this process, so the request id
# is the stable receipt a replacement HTTP connection uses to find its emitter.
# The runtime spine remains authoritative for ownership and lifecycle; this
# registry carries only the live NDJSON delivery object and is removed as soon
# as the work task settles.
_ACTIVE_STREAMS: dict[str, StreamEmitter] = {}


def register_active_stream(request_id: str, emitter: StreamEmitter) -> None:
    _ACTIVE_STREAMS[request_id] = emitter


def unregister_active_stream(request_id: str, emitter: StreamEmitter) -> None:
    if _ACTIVE_STREAMS.get(request_id) is emitter:
        _ACTIVE_STREAMS.pop(request_id, None)


def get_active_stream(request_id: str) -> StreamEmitter | None:
    return _ACTIVE_STREAMS.get(request_id)
