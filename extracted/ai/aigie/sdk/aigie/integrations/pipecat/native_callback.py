"""Pipecat BaseObserver that emits Aigie spans (L3 binding, callback-driven)."""

from __future__ import annotations

import logging
from collections import OrderedDict
from collections.abc import Callable
from contextlib import suppress
from dataclasses import dataclass, field
from typing import Any

from aigie.auto_instrument.trace import get_or_create_trace
from aigie.context_manager import merge_metadata
from aigie.integrations.pipecat import _frames, _llm, _media
from aigie.tracing.span_event_handler import SpanEventHandler
from aigie.tracing.trace_state import (
    claim_provider_spans,
    close_ambient,
    current_trace_id,
    is_inside_traced_run,
    open_ambient,
    release_provider_spans,
)
from aigie.tracing.workflow_root import WorkflowRoot

logger = logging.getLogger(__name__)

_BASE_META = _frames._BASE_META


@dataclass
class _Boundary:
    trace_id: str
    root: WorkflowRoot
    ambient_token: Any = None
    turn_run_id: str | None = None
    open_spans: dict[str, str] = field(default_factory=dict)
    # Every STT/TTS usage delta ever received, summed regardless of whether it
    # could be attached to a span: Deepgram's deltas straddle transcript
    # boundaries, so no single span's value is reliably "the" total, but the
    # provider bills per connection, so the running sum is. See `_frames.usage_totals`.
    stt_audio_seconds_total: float = 0.0
    tts_character_count_total: float = 0.0
    # STT has no span open when its usage metrics arrive (they land on the
    # same MetricsFrame channel ahead of the finalized TranscriptionFrame
    # that opens-and-closes the span), so there is nowhere else to hold it.
    pending_stt_usage: Any = None
    # Confirmed against real Deepgram: STTUsageMetricsData arrives on BOTH
    # sides of a final transcript — a pre-final frame for the utterance's own
    # audio (correctly attached above), then a post-final frame billing the
    # trailing silence after endpointing. That post-final frame has no span
    # to land on; left in pending_stt_usage it would silently misattach to
    # the *next* utterance's span (wrong data presented as correct — worse
    # than the alternative here, which is that next span simply carrying no
    # usage). Set the instant a span consumes pending_stt_usage; the very
    # next STT usage frame received while this is True is that trailing one
    # and gets discarded instead of stashed. Tradeoff: an STT service that
    # never emits a trailing frame would have its next utterance's own
    # (legitimate) pre-final usage eaten by this flag instead — accepted
    # because it degrades to missing data, never to a misattributed value.
    discard_next_stt_usage: bool = False
    # Mirror image for LLM: a call's span has already closed its text-
    # accumulation phase (LLMFullResponseEndFrame arrived) but its usage
    # MetricsFrame hasn't landed yet — possibly not until after the next
    # call's start frame. FIFO list of run_ids, oldest first; see
    # `_llm._attach_llm_usage` / `_llm.flush_pending_llm`.
    pending_llm: list[str] = field(default_factory=list)
    # LLMContextFrame can arrive before LLMFullResponseStartFrame opens the
    # llm span (it is what triggers the LLM service to run in the first
    # place), so there is nowhere on the not-yet-open span to stash it.
    # Stash-then-consume, mirroring pending_llm/pending_stt_usage. Overwritten
    # (not appended) on each new frame: only the most recent context is ever
    # relevant to the next call, and per-hop redelivery of the SAME frame is
    # already filtered upstream by `_is_duplicate_frame`.
    pending_llm_context: list[dict[str, Any]] | None = None
    # Set only by an InterruptionFrame that `_frames.is_barge_in` accepts (not
    # every turn's routine one); read by `_llm.on_llm_end` / `_media.on_tts_stopped`
    # so a barge-in — Pipecat still pushes the normal end frames after one —
    # closes their span truthfully as "interrupted", not "success". Cleared via
    # `_frames.interruption_settled` once neither lane is open, not on first read.
    interrupted: bool = False


class PipecatObserver:
    """One observer per PipelineWorker — therefore one per conversation.

    Duck-typed against pipecat's BaseObserver rather than subclassing it, so this
    module imports without Pipecat present (it is unavailable on Python 3.10).
    """

    _is_aigie_handler = True

    # In-memory run_id the root span is opened under, so turn spans (and later
    # LLM/STT/TTS spans) can parent to it via SpanEventHandler's _open registry.
    CONVERSATION_RUN_ID = "__conversation__"

    # `WorkerObserver.on_push_frame` fires once per pipeline hop, not once per
    # conceptual frame: the same frame instance is renotified as it crosses each
    # processor (measured on real Bedrock: StartFrame x5, TranscriptionFrame x4,
    # LLMFullResponseStartFrame x3, TTSStartedFrame x2, EndFrame x3 for one
    # utterance in a 3-processor pipeline). A bounded LRU of already-dispatched
    # `frame.id`s is how every handler below — present and future — gets exactly
    # one notification per frame without re-deriving the guard per handler.
    # 256 is a generous multiple of Pipecat's own precedent (its
    # TurnTrackingObserver bounds a comparable per-frame set at max_frames=100);
    # a single utterance's hop-fanout tops out in the single digits per frame, so
    # this comfortably covers the frames in flight for one turn without growing
    # unbounded over a long call.
    _MAX_SEEN_FRAME_IDS = 256

    # Pipecat frame/data classes vary by release; Any at the observer boundary.
    def __init__(self, emitter: Any, *, config: Any = None) -> None:
        self._emitter = emitter
        self._config = config
        self.spans = SpanEventHandler(emitter, config=config)
        # Instance state, NOT a ContextVar: Pipecat runs each observer in its own
        # asyncio task and a ContextVar set in one task is invisible in another.
        self._boundary: _Boundary | None = None
        self._has_tracker = False
        # Insertion-ordered so the oldest id is evicted first (an LRU by arrival,
        # not by access — see `_is_duplicate_frame`).
        self._seen_frame_ids: OrderedDict[Any, None] = OrderedDict()

    async def on_pipeline_started(self) -> None:
        return None

    async def on_process_frame(self, data: Any) -> None:
        """Deliberately empty — on_push_frame already sees every frame.

        Implemented rather than omitted: Pipecat calls this, and an AttributeError
        raised inside its proxy task kills the observer for the rest of the call.
        """
        return

    async def cleanup(self) -> None:
        """Pipecat calls this on pipeline teardown; every real observer inherits it
        from BaseObject. Also the last chance to finalize a conversation whose
        pipeline died without a terminal frame, which would otherwise leak the
        provider-span claim for the life of the thread.
        """
        try:
            if self._boundary is not None:
                self._finalize_conversation(
                    lambda root: root.close(
                        status="interrupted",
                        metadata_updates={"ended_by": "cleanup", **self._usage_totals_metadata()},
                    )
                )
        except Exception as e:  # noqa: BLE001
            logger.debug("pipecat observer cleanup failed: %s", e)

    async def on_push_frame(self, data: Any) -> None:
        frame = getattr(data, "frame", None)
        name = type(frame).__name__
        try:
            # Rejection check stays first and outside the dedupe bookkeeping:
            # audio frames arrive tens of thousands of times per call and must
            # never even enter the seen-id set.
            if _frames.is_rejected(name):
                return
            if self._is_duplicate_frame(frame):
                return
            await self._dispatch(name, frame)
        except Exception as e:  # noqa: BLE001
            # Never re-touch `data`/`frame` here: if the original failure was the
            # attribute access itself, doing so would raise again and escape this
            # handler, killing the observer for the rest of the call.
            logger.debug("pipecat observer failed on frame %s: %s", name, e)

    def _is_duplicate_frame(self, frame: Any) -> bool:
        """True if this exact frame instance was already dispatched.

        Keyed on `frame.id` (a stable field Pipecat puts on every frame), never on
        `id(frame)` — a memory address that CPython recycles once the frame is
        garbage-collected, which would silently start matching an unrelated later
        frame. This codebase already carries one scar from that exact mistake
        (the llm span's run_id was switched from `id(frame)` to `uuid4()` for the
        same reason). A frame with no `id` (a test double, or a future Pipecat
        frame type that dropped the field) is dispatched rather than dropped:
        losing a span is worse than one duplicate.
        """
        frame_id = getattr(frame, "id", None)
        if frame_id is None:
            return False
        if frame_id in self._seen_frame_ids:
            return True
        self._seen_frame_ids[frame_id] = None
        if len(self._seen_frame_ids) > self._MAX_SEEN_FRAME_IDS:
            self._seen_frame_ids.popitem(last=False)
        return False

    async def _dispatch(self, name: str, frame: Any) -> None:
        if name in _frames.CONVERSATION_START:
            await self._open_conversation(frame)
            return
        if self._boundary is None:
            return
        self._reassert_ambient()
        if self._dispatch_lifecycle(name, frame):
            return
        if self._dispatch_llm(name, frame):
            return
        if self._dispatch_tools(name, frame):
            return
        if name in _frames.ERROR:
            _llm.on_error(self, frame)
            return
        self._dispatch_media(name, frame)

    def _dispatch_lifecycle(self, name: str, frame: Any) -> bool:
        del frame  # neither branch below carries data read past this point
        boundary = self._boundary
        if boundary is None:
            return False
        if name in _frames.INTERRUPTION:
            # `or` keeps the flag sticky once set; see _frames.is_barge_in.
            boundary.interrupted |= _frames.is_barge_in(boundary.open_spans)
            return True
        if name in _frames.CONVERSATION_END:
            self._close_conversation(name)
            return True
        return False

    def _dispatch_llm(self, name: str, frame: Any) -> bool:
        if name in _frames.LLM_CONTEXT:
            _llm.on_llm_context(self, frame)
        elif name in _frames.LLM_START:
            _llm.on_llm_start(self, frame)
        elif name in _frames.LLM_TEXT:
            _llm.on_llm_text(self, frame)
        elif name in _frames.LLM_END:
            _llm.on_llm_end(self, frame)
        else:
            return False
        return True

    def _dispatch_tools(self, name: str, frame: Any) -> bool:
        if name in _frames.FUNCTION_CALL_STARTED:
            _llm.on_function_call_started(self, frame)
        elif name in _frames.FUNCTION_CALL_RESULT:
            _llm.on_function_call_result(self, frame)
        elif name in _frames.FUNCTION_CALL_CANCEL:
            _llm.on_function_call_cancel(self, frame)
        else:
            return False
        return True

    def _dispatch_media(self, name: str, frame: Any) -> None:
        # MetricsFrame is one channel shared by llm/stt/tts usage data; both
        # handlers filter by item type internally, so calling both is safe.
        if name in _frames.METRICS:
            _llm.on_metrics(self, frame)
            _media.on_metrics(self, frame)
        elif name == "TranscriptionFrame":
            self._on_stt(frame)
        elif name in _frames.TTS_START:
            _media.on_tts_started(self, frame)
        elif name in _frames.TTS_TEXT:
            _media.on_tts_text(self, frame)
        elif name in _frames.TTS_END:
            _media.on_tts_stopped(self, frame)

    def _on_stt(self, frame: Any) -> None:
        """One frame, two responsibilities: stamp the root input (Task 5)
        and emit the STT span (Task 8) — kept in separate methods so neither
        grows past the statement cap and each stays independently gate-able.
        """
        self._on_transcription(frame)
        _media.on_stt_transcription(self, frame)

    def _reassert_ambient(self) -> None:
        """Re-open the ambient trace when this task never had it set.

        Copied from the Strands provider: an async framework dispatches handlers in
        their own tasks, and open_span requires an ambient trace id.
        """
        boundary = self._boundary
        if boundary is None or current_trace_id() == boundary.trace_id:
            return
        # Discard the token: it belongs to this task's ambient state, not to the
        # boundary's own opening token, and storing it would let a later
        # close_ambient() reset the wrong task's ContextVar (see Strands).
        open_ambient(trace_id=boundary.trace_id)

    async def _open_conversation(self, frame: Any) -> None:
        if self._boundary is not None:
            return  # StartFrame reaches every processor; one root only.
        if not self._flag("trace_conversations"):
            return
        if self._zero_retention() or is_inside_traced_run():
            return
        # StartFrame carries the effective flags. Without usage metrics the llm spans
        # carry no tokens, and a silently unpriceable trace is worse than a log line.
        # Warn only once we know we are actually going to trace this conversation —
        # otherwise an operator who disabled tracing gets log noise every call.
        if not getattr(frame, "enable_usage_metrics", False):
            logger.warning("pipecat: enable_usage_metrics is off; llm spans will carry no tokens")
        trace = await get_or_create_trace(name="voice conversation", metadata=dict(_BASE_META))
        if trace is None:
            return
        trace_id = str(trace.id)
        token = open_ambient(trace_id=trace_id)
        root = WorkflowRoot(
            self.spans,
            "voice conversation",
            trace_id=trace_id,
            framework="pipecat",
            run_id=self.CONVERSATION_RUN_ID,
        )
        self._boundary = _Boundary(trace_id=trace_id, root=root, ambient_token=token)
        # This conversation now owns the llm spans for every provider call the
        # pipeline makes: those run in sibling asyncio tasks that cannot see the
        # ambient trace opened just above, so the bare provider patch would
        # otherwise open a second trace for a call we already price from
        # MetricsFrame. Paired with the release in _close_conversation.
        claim_provider_spans()
        if not self._has_tracker:
            # enable_turn_tracking=False: one implicit turn spans the whole call
            # so downstream (LLM/STT/TTS) spans always have a turn to parent to.
            self._on_turn_started(1)

    def _close_conversation(self, frame_name: str) -> None:
        # SpanStatus has no "cancelled"; an abandoned run is "interrupted".
        status = "success" if frame_name == "EndFrame" else "interrupted"
        self._finalize_conversation(
            lambda root: root.close(
                status=status,
                metadata_updates={"ended_by": frame_name, **self._usage_totals_metadata()},
            )
        )

    def _fail_conversation(self, error: BaseException) -> None:
        """Finalize the conversation as errored (a fatal ``ErrorFrame``).

        Routed through the root's own error path — ``WorkflowRoot.close(error=...)``
        calls ``fail_span`` and yields ``status="error"`` — rather than threading an
        unsupported status string through the success/interrupted close below.
        """
        self._finalize_conversation(
            lambda root: root.close(error=error, metadata_updates=self._usage_totals_metadata())
        )

    def _usage_totals_metadata(self) -> dict[str, Any]:
        # See `_Boundary.stt_audio_seconds_total` for why the sum, not any one
        # span's value, is the figure that is provably correct here.
        boundary = self._boundary
        if boundary is None:
            return {}
        return _frames.usage_totals(
            boundary.stt_audio_seconds_total, boundary.tts_character_count_total
        )

    def _finalize_conversation(self, close_root: Callable[[WorkflowRoot], None]) -> None:
        boundary = self._boundary
        if boundary is None:
            return
        try:
            self._drain_open_spans(boundary)
            self._close_open_turn()
            close_root(boundary.root)
            if boundary.ambient_token is not None:
                with suppress(ValueError, LookupError):
                    close_ambient(boundary.ambient_token)
        finally:
            # Emitting the root runs completion hooks and payload shaping, none of
            # it isolated. A raise there would otherwise leave the claim standing
            # and this thread's provider spans suppressed for the rest of the
            # process — a permanent blast radius for a one-off failure.
            release_provider_spans()
            self._boundary = None

    def _drain_open_spans(self, boundary: _Boundary) -> None:
        """Close any span still in flight (e.g. an ``llm`` span whose
        ``LLMFullResponseEndFrame`` never arrived — barge-in / CancelFrame mid-response).

        Runs before the turn and root close, so children finalize ahead of their
        parents. Left open, these only ship via the global shutdown finalizer as
        "interrupted" after their parent has already closed, and they leak into
        whatever conversation opens next since the key space is per-boundary.
        """
        # An llm span merely awaiting its usage MetricsFrame is not "interrupted" —
        # the LLM did respond — so flush it (as success) before the blanket drain
        # below, which is for spans that genuinely never finished.
        _llm.flush_pending_llm(self)
        for run_id in boundary.open_spans.values():
            self.spans.close_span(run_id=run_id, output=None, status="interrupted")
        boundary.open_spans.clear()

    def _on_transcription(self, frame: Any) -> None:
        """Stamp the root input from a ``TranscriptionFrame``.

        Only called from ``_on_stt``, which only fires on the exact class
        name ``"TranscriptionFrame"`` — ``InterimTranscriptionFrame`` is
        rejected upstream in ``_frames.REJECTED`` and never reaches here, so
        reaching this method already means "final". Do NOT gate on
        ``frame.finalized``: it is an optional commit signal most STT
        services (Deepgram included) never set, defaulting to False even on
        a genuine final. Gating on it drops the root input entirely — a
        clause-C violation (blank user input rendered in the trace).
        """
        boundary = self._boundary
        if boundary is None:
            return
        text = getattr(frame, "text", None)
        if not text or not self._flag("capture_transcripts"):
            return
        boundary.root.note_input(_frames.truncate(text, self._limit()))

    def attach_turn_tracker(self, tracker: Any) -> None:
        """Register handlers on Pipecat's own TurnTrackingObserver.

        Its heuristic already handles the end-of-turn timeout and interruptions;
        re-deriving turns from speaking frames would be a worse copy.
        """
        self._has_tracker = True

        @tracker.event_handler("on_turn_started")
        async def _started(_tracker: Any, turn_number: int) -> None:
            try:
                self._on_turn_started(turn_number)
            except Exception as e:  # noqa: BLE001
                logger.debug("pipecat turn start failed: %s", e)

        @tracker.event_handler("on_turn_ended")
        async def _ended(
            _tracker: Any, turn_number: int, duration: float, was_interrupted: bool
        ) -> None:
            try:
                self._on_turn_ended(turn_number, duration, was_interrupted)
            except Exception as e:  # noqa: BLE001
                logger.debug("pipecat turn end failed: %s", e)

    @property
    def turn_run_id(self) -> str | None:
        boundary = self._boundary
        return boundary.turn_run_id if boundary is not None else None

    def _on_turn_started(self, turn_number: int) -> None:
        boundary = self._boundary
        if boundary is None or not self._flag("trace_turns"):
            return
        self._reassert_ambient()
        # A prior call's llm span may still be waiting on a usage MetricsFrame that
        # never arrived before the next turn started; it must not bleed into it.
        _llm.flush_pending_llm(self)
        self._close_open_turn()
        run_id = f"turn:{boundary.trace_id}:{turn_number}"
        boundary.turn_run_id = run_id
        self.spans.open_span(
            run_id=run_id,
            parent_run_id=self.CONVERSATION_RUN_ID,
            name=f"turn {turn_number}",
            span_type="chain",
            input=None,
            metadata=merge_metadata(_BASE_META, {"turn.number": turn_number}),
        )

    def _on_turn_ended(self, turn_number: int, duration: float, was_interrupted: bool) -> None:
        boundary = self._boundary
        if boundary is None or boundary.turn_run_id is None:
            return
        expected_run_id = f"turn:{boundary.trace_id}:{turn_number}"
        if boundary.turn_run_id != expected_run_id:
            logger.debug(
                "pipecat: on_turn_ended turn_number %s does not match open turn %s; ignoring",
                turn_number,
                boundary.turn_run_id,
            )
            return
        self._reassert_ambient()
        # `was_interrupted` is Pipecat's own TurnTrackingObserver signal, already
        # reliable — this is turn-level barge-in coverage, so `boundary.interrupted`
        # (which this class sets from InterruptionFrame for the llm/tts spans) is
        # deliberately not duplicated as a second source of truth here.
        self.spans.close_span(
            run_id=boundary.turn_run_id,
            output=None,
            metadata_updates={
                "turn.duration_seconds": duration,
                "turn.was_interrupted": was_interrupted,
            },
        )
        boundary.turn_run_id = None

    def _close_open_turn(self) -> None:
        boundary = self._boundary
        if boundary is None or boundary.turn_run_id is None:
            return
        self.spans.close_span(run_id=boundary.turn_run_id, output=None)
        boundary.turn_run_id = None

    def _flag(self, name: str) -> bool:
        return bool(getattr(self._config, name, True))

    def _limit(self) -> int:
        return getattr(self._config, "max_content_length", 10000)

    def _zero_retention(self) -> bool:
        return bool(getattr(self._config, "zero_retention", False))
