"""STT/TTS span handlers for the Pipecat observer.

Module-level functions taking the observer first, matching ``_llm.py``'s
convention — ``native_callback.py`` stays close to the file-length cap.

STT and TTS are emitted as ``span_type="tool"``, never ``"llm"``: neither
bills in tokens (STT bills audio-seconds, TTS bills characters), so typing
them ``llm`` would permanently fail the span contract's token/model gate.
``metadata.modality`` ("stt" / "tts") is what ``error_conversion.py`` reads
to route them to error source "model" rather than "tool" — do not rename it.
"""

from __future__ import annotations

from typing import Any

from aigie.context_manager import merge_metadata
from aigie.integrations.pipecat import _frames

_BASE_META = _frames._BASE_META

_STT_KEY = "stt"
_TTS_KEY = "tts"


def on_stt_transcription(obs: Any, frame: Any) -> None:
    """Open-then-immediately-close: Pipecat gives no STT-start signal for
    streaming transcription, so a ``TranscriptionFrame`` is the only unit we
    can span.

    Whether that frame is "final" is decided by its *class*, not by any field
    on it: ``InterimTranscriptionFrame`` is NOT a subclass of
    ``TranscriptionFrame``, it is rejected in ``_frames.REJECTED`` and never
    reaches ``_dispatch``, and dispatch only routes here on the exact class
    name ``"TranscriptionFrame"`` (see ``PipecatObserver._dispatch_media``).
    Reaching this function at all already means "final".

    ``frame.finalized`` is an OPTIONAL extra commit/finalize signal that most
    STT services never set — Pipecat's own docstring says so, and real
    Deepgram finals arrive with ``finalized=False``. Gating span creation on
    that flag silently drops every Deepgram transcript (proven against a real
    closed-loop run) and, worse, drops the root input via the sibling gate in
    ``native_callback.py::_on_transcription`` — a clause-C violation (blank
    user input in the trace). Do not reintroduce a truthiness check on
    ``finalized`` here or in ``_on_transcription``; it is recorded below only
    as informational metadata for services that do set it.
    """
    boundary = obs._boundary
    if boundary is None or not obs._flag("trace_stt"):
        return
    is_final_flag = bool(getattr(frame, "finalized", False))
    run_id = f"stt:{boundary.trace_id}:{id(frame)}"
    metadata = merge_metadata(
        _BASE_META,
        {"modality": "stt", "is_final": True, "finalized": is_final_flag},
        _pop_stt_usage(boundary),
    )
    language = getattr(frame, "language", None)
    if language:
        metadata["language"] = language
    boundary.open_spans[_STT_KEY] = run_id
    obs.spans.open_span(
        run_id=run_id,
        parent_run_id=obs.turn_run_id or obs.CONVERSATION_RUN_ID,
        name="stt",
        span_type="tool",
        input=None,
        metadata=metadata,
    )
    text = getattr(frame, "text", None)
    output = (
        _frames.truncate(text, obs._limit()) if text and obs._flag("capture_transcripts") else None
    )
    obs.spans.close_span(run_id=run_id, output=output)
    boundary.open_spans.pop(_STT_KEY, None)


def _pop_stt_usage(boundary: Any) -> dict[str, Any]:
    usage_data = boundary.pending_stt_usage
    boundary.pending_stt_usage = None
    # Arm the discard latch: see `_Boundary.discard_next_stt_usage`. The very
    # next STTUsageMetricsData is the trailing-silence frame for the
    # utterance whose span we're about to close, not usage for the next one.
    boundary.discard_next_stt_usage = True
    return _frames.stt_metadata(usage_data) if usage_data is not None else {}


def on_tts_started(obs: Any, frame: Any) -> None:
    boundary = obs._boundary
    if boundary is None or not obs._flag("trace_tts"):
        return
    if _TTS_KEY in boundary.open_spans:
        return  # never orphan a span if Pipecat re-fires start without a stop
    run_id = f"tts:{boundary.trace_id}:{id(frame)}"
    boundary.open_spans[_TTS_KEY] = run_id
    obs.spans.open_span(
        run_id=run_id,
        parent_run_id=obs.turn_run_id or obs.CONVERSATION_RUN_ID,
        name="tts",
        span_type="tool",
        input=None,
        metadata=merge_metadata(_BASE_META, {"modality": "tts"}),
    )
    state = obs.spans.get_state(run_id)
    if state is not None:
        state["_text_parts"] = []
        state["_usage_data"] = None
        voice_id = getattr(frame, "voice_id", None)
        if voice_id:
            state["_voice_id"] = voice_id


def on_tts_text(obs: Any, frame: Any) -> None:
    boundary = obs._boundary
    if boundary is None:
        return
    run_id = boundary.open_spans.get(_TTS_KEY)
    state = obs.spans.get_state(run_id) if run_id else None
    if state is None:
        return
    text = getattr(frame, "text", None)
    if not text:
        return
    # TTS providers disagree on whether a chunk already carries its own
    # spacing: Deepgram's sentence-level chunks do, ElevenLabs' word-level
    # chunks don't. TTSTextFrame.includes_inter_frame_spaces is the frame's
    # own answer to that, decided per-chunk so a mixed stream (or a third
    # provider either way) reconstructs correctly without a global join
    # policy. Missing entirely (older/newer frame shape) keeps today's
    # behaviour of gluing chunks together.
    parts = state.setdefault("_text_parts", [])
    if parts and not getattr(frame, "includes_inter_frame_spaces", True):
        parts.append(" ")
    parts.append(text)


def on_metrics(obs: Any, frame: Any) -> None:
    """Filters the shared ``MetricsFrame`` channel for STT/TTS usage data.

    Called unconditionally alongside ``_llm.on_metrics`` — both look for
    different item types on the same frame, so neither excludes the other.
    """
    boundary = obs._boundary
    if boundary is None:
        return
    for item in getattr(frame, "data", None) or []:
        cls_name = type(item).__name__
        if cls_name == "STTUsageMetricsData":
            _accumulate_stt_seconds(boundary, item)
            _stash_stt_usage(boundary, item)
        elif cls_name == "TTSUsageMetricsData":
            _accumulate_tts_characters(boundary, item)
            _stash_tts_usage(obs, boundary, item)


def _accumulate_stt_seconds(boundary: Any, item: Any) -> None:
    """Sum every STT usage delta over the whole conversation, regardless of
    whether this particular delta could be attached to a span.

    Providers report usage as deltas that do not partition by transcript —
    Deepgram's own deltas straddle transcript boundaries, so no single span's
    ``audio_seconds`` is reliably "the" total for that utterance — but the
    provider bills per connection, not per transcript, so the running sum
    over the conversation is the one figure that is provably correct.
    """
    value = getattr(item, "value", None)
    audio_seconds = getattr(value, "audio_seconds", None)
    if isinstance(audio_seconds, (int, float)):
        boundary.stt_audio_seconds_total += audio_seconds


def _accumulate_tts_characters(boundary: Any, item: Any) -> None:
    # Same accounting shape as STT: falls out cleanly here since every
    # TTSUsageMetricsData item already attaches to the one open tts span
    # unambiguously, but the conversation total is recorded anyway for parity.
    value = getattr(item, "value", None)
    if isinstance(value, (int, float)):
        boundary.tts_character_count_total += value


def _stash_stt_usage(boundary: Any, item: Any) -> None:
    """Stash usage for the next stt span to consume — unless it's the
    trailing-silence frame armed by `_pop_stt_usage`; see that function and
    `_Boundary.discard_next_stt_usage` for why this frame has nowhere to go.
    """
    if boundary.discard_next_stt_usage:
        boundary.discard_next_stt_usage = False
        return
    boundary.pending_stt_usage = item


def _stash_tts_usage(obs: Any, boundary: Any, item: Any) -> None:
    run_id = boundary.open_spans.get(_TTS_KEY)
    state = obs.spans.get_state(run_id) if run_id else None
    if state is not None:
        state["_usage_data"] = item


def on_tts_stopped(obs: Any, frame: Any) -> None:
    del frame  # stop frame carries nothing we need; the span state does
    boundary = obs._boundary
    if boundary is None:
        return
    run_id = boundary.open_spans.pop(_TTS_KEY, None)
    if run_id is None:
        return
    state = obs.spans.get_state(run_id)
    text = "".join(state.get("_text_parts", [])).strip() if state else ""
    usage_data = state.get("_usage_data") if state else None
    metadata_updates = dict(_frames.tts_metadata(usage_data)) if usage_data is not None else {}
    voice_id = state.get("_voice_id") if state else None
    if voice_id:
        metadata_updates["voice_id"] = voice_id
    if state is not None and text and obs._flag("capture_inputs"):
        state["input"] = _frames.truncate(text, obs._limit())
    # Pipecat still pushes this stop frame after a barge-in — without checking
    # the flag, audio the user talked over closes exactly like audio that
    # finished playing on its own.
    status = "interrupted" if boundary.interrupted else "success"
    obs.spans.close_span(
        run_id=run_id, output=None, metadata_updates=metadata_updates or None, status=status
    )
    _frames.clear_interrupted_if_settled(boundary)
