from __future__ import annotations

import asyncio
import base64
import time
import uuid
from typing import TYPE_CHECKING, Any

import rich
from google import genai
from google.genai.types import (
    Candidate,
    GenerateContentResponse,
    Part,
)
from matrx_connect.context.events import InfoPayload
from matrx_utils import vcprint

from matrx_ai.config import (
    UnifiedConfig,
    UnifiedResponse,
)
from matrx_ai.context.emitter_protocol import Emitter
from matrx_ai.providers.keys import keyed_provider_client
from matrx_ai.providers.outbound_capture import (
    emit_explicit_context_analysis,
    stamp_call_meta,
)
from matrx_ai.providers.snapshot import capture_request_payload

from .translator import GoogleProviderConfig, GoogleTranslator

if TYPE_CHECKING:  # circular-by-design: catalog.models imports providers.resolved_capabilities
    from matrx_ai.catalog.models import ResolvedCallProfile

LOCAL_DEBUG = False

# Gemini's TTS stream is a blocking sync generator that yields audio chunks AS
# Google produces them. We collect it in a worker thread and watch those chunks
# as a liveness heartbeat: a call that keeps emitting chunks is healthy and is
# NEVER aborted, no matter how long the whole render takes. We only give up when
# the stream genuinely STALLS — no new chunk for _TTS_STALL_TIMEOUT_SECONDS — or
# when a generous, length-scaled total ceiling is blown (a pathological slow
# drip). Both abort paths are NON-retryable: the call was billed in full the
# instant it started, so re-running it just multiplies cost for the same result.
#
# This replaces an earlier design that wrapped a single `list(...)` of the whole
# stream in a flat 300s wall-clock timeout. That killed perfectly healthy long
# renders mid-flight and — because the timeout classified as a retryable
# `unknown_error` — re-ran the (already-paid) generation up to 3×, never
# producing audio. See the 2026-06-08 incident.
#
# How long the stream may sit silent before we treat it as hung. A working
# stream resets this on every chunk (the consumer's queue.get() timeout), so this
# is "dead air", not "total time".
_TTS_STALL_TIMEOUT_SECONDS = 250
# Absolute total-time backstop, scaled by input length. Floor honours "at least
# 500s for any clip"; the per-1k-chars term grows it for long multi-speaker
# scripts. The stall detector above is the real guard — this only stops a stream
# that never fully stalls yet never finishes.
_TTS_MIN_TOTAL_BUDGET_SECONDS = 500
_TTS_BUDGET_SECONDS_PER_1K_CHARS = 180
# Backstop read timeout (ms) on the SDK's httpx client so a TTS call that the
# asyncio side has already abandoned cannot leave its worker thread blocked
# forever (which would slowly exhaust the default executor in a long-lived
# server). Covers chat/image too; well above any legitimate single response.
_GOOGLE_HTTP_TIMEOUT_MS = 1_800_000

# Long-transcript segmentation. A single Gemini-TTS stream over a full multi-turn
# script runs long enough that Google's stream eventually goes silent and trips
# the stall watchdog above (2026-07-10 incident). We split any transcript longer
# than this into several short TTS calls so no single stream has to survive that
# long; each is well under the stall window and finishes cleanly. A transcript at
# or under the threshold takes the original single-call path unchanged.
_TTS_MAX_CHARS_PER_SEGMENT = 2000
# Per-model override, keyed by a provider-model-id substring. Gemini 3.1 Flash
# TTS is excellent on SHORT clips but degrades hard past ~60 seconds of audio:
# the voice drifts and can collapse toward a single speaker, articulation goes
# by ~2 minutes, and it mumbles by ~3 (Google's own AI-dev forum thread "voice
# slowly changing, massive audio quality + volume dropping on TTS requests
# longer than ~1 minute"; independent long-form audits report ~90% of >1-minute
# generations degraded). At ~150 wpm / ~5.5 chars per word, 60s of speech is
# ~800 chars — so the generic 2000-char window is ~2.5 minutes, deep inside the
# collapse zone. Segmenting smaller keeps every 3.1-flash call inside the
# window where it is genuinely as good as (or better than) 2.5 pro.
# 2.5-pro-preview-tts is long-form stable and keeps the generic window.
_TTS_MAX_CHARS_BY_MODEL: dict[str, int] = {
    "3.1-flash-tts": 750,
}


def _tts_segment_chars(provider_model_id: str) -> int:
    """The per-segment character cap for this TTS model (see the map above)."""
    model = (provider_model_id or "").lower()
    for needle, cap in _TTS_MAX_CHARS_BY_MODEL.items():
        if needle in model:
            return cap
    return _TTS_MAX_CHARS_PER_SEGMENT
# A stall is transient provider behavior, not a fatal input error — retry the ONE
# short segment that stalled (re-billing 2k chars is cheap; re-billing a 6-minute
# render is not). Never retry the whole run.
_TTS_SEGMENT_STALL_RETRIES = 1
_TTS_SEGMENT_RETRY_BACKOFF_SECONDS = 3.0


# Sentinel pushed onto the TTS chunk queue when the producer thread finishes.
_TTS_STREAM_DONE = object()


class _TTSSegmentStall(Exception):
    """A single segmented-TTS provider call stalled or blew its ceiling. Caught by
    the segment loop, which decides retry-once vs. recover-partial vs. hard-abort —
    it is NEVER allowed to escape as a raw error."""


def _iter_tts_user_text(contents: list[Any]) -> str:
    """Concatenate the user-turn text from a built Google ``contents`` payload.

    ``contents`` items are dicts (``{"role", "parts": [{"text": ...}]}``) — the
    shape ``GoogleTranslator`` emits — but tolerate SDK objects too."""
    out: list[str] = []
    for content in contents:
        if isinstance(content, dict):
            role = content.get("role")
            parts = content.get("parts") or []
        else:
            role = getattr(content, "role", None)
            parts = getattr(content, "parts", None) or []
        if role not in (None, "user"):
            continue
        for part in parts:
            text = part.get("text") if isinstance(part, dict) else getattr(part, "text", None)
            if text:
                out.append(text)
    return "\n".join(out)


def _required_speaker_labels(config: Any) -> list[str]:
    """The speaker names declared on a built multi-speaker ``speech_config``.

    Every segment we send must contain all of these labels — a Gemini
    multi-speaker request whose text is missing a declared speaker mis-renders.
    Single-voice TTS returns ``[]`` (no per-segment label constraint)."""
    speech_config = getattr(config, "speech_config", None)
    multi = getattr(speech_config, "multi_speaker_voice_config", None) if speech_config else None
    svcs = getattr(multi, "speaker_voice_configs", None) if multi else None
    if not svcs:
        return []
    return [s.speaker for s in svcs if getattr(s, "speaker", None)]


def _split_tts_text(full_text: str, required_labels: list[str], *, max_chars: int) -> list[str]:
    """Split a transcript into ``<= max_chars`` windows on line boundaries.

    Every window is guaranteed to contain each label in ``required_labels`` so a
    multi-speaker request never gets a segment missing a declared speaker; a
    trailing remainder that lacks a label is merged back into the previous window.
    Returns ``[full_text]`` unchanged when it already fits — the original
    single-call path, byte-for-byte, for short scripts."""
    if len(full_text) <= max_chars:
        return [full_text]

    def _has_all(text: str) -> bool:
        return all(lbl in text for lbl in required_labels) if required_labels else True

    windows: list[str] = []
    cur: list[str] = []
    for line in full_text.splitlines():
        cur.append(line)
        cur_text = "\n".join(cur)
        if len(cur_text) >= max_chars and _has_all(cur_text):
            windows.append(cur_text)
            cur = []
    if cur:
        remainder = "\n".join(cur)
        if windows and not _has_all(remainder):
            windows[-1] = windows[-1] + "\n" + remainder
        else:
            windows.append(remainder)
    return windows or [full_text]


def _tts_total_budget_seconds(text_len: int) -> int:
    return max(
        _TTS_MIN_TOTAL_BUDGET_SECONDS,
        int((text_len / 1000.0) * _TTS_BUDGET_SECONDS_PER_1K_CHARS),
    )


def _sanitize_for_debug(obj: object) -> object:
    if isinstance(obj, dict):
        return {
            k: ("<truncated: first 100 chars> " + repr(v)[:100])
            if k == "data" and isinstance(v, str) and len(v) > 100
            else _sanitize_for_debug(v)
            for k, v in obj.items()
        }
    if isinstance(obj, list):
        return [_sanitize_for_debug(item) for item in obj]
    return obj


class GoogleChat:
    """Google Gemini-specific endpoint implementation."""

    client: genai.Client
    endpoint_name: str
    translator: GoogleTranslator
    debug: bool

    # Dual-name resolution preserves the historical GEMINI_API_KEY /
    # GOOGLE_API_KEY behavior; memoized on the resolved key for rotation.
    client = keyed_provider_client(
        "GEMINI_API_KEY",
        "GOOGLE_API_KEY",
        "GOOGLE_AI_STUDIO",
        factory=lambda api_key: genai.Client(
            api_key=api_key,
            http_options=genai.types.HttpOptions(timeout=_GOOGLE_HTTP_TIMEOUT_MS),
        ),
    )

    def __init__(self, debug: bool = False):
        self.endpoint_name = "[GOOGLE CHAT]"
        self.translator = GoogleTranslator(debug=debug)
        self.debug = debug
        # Tracks whether we've emitted the content-less "reasoning started"
        # lifecycle signal for the current turn but not yet "stopped". Gemini has
        # no explicit reasoning-block-start event — reasoning is inferred from
        # part shape (part.thought, or a bare part.thought_signature when
        # include_thoughts=False), which is why the signal is tracked per-stream.
        self._reasoning_signaled = False

        if LOCAL_DEBUG:
            self.debug = True

    async def execute(
        self,
        unified_config: UnifiedConfig,
        profile: ResolvedCallProfile,
        debug: bool = False,
    ) -> UnifiedResponse:
        from matrx_ai.context.app_context import get_app_context

        emitter = get_app_context().emitter

        self.debug = debug
        if LOCAL_DEBUG:
            self.debug = True
        self.translator.debug = debug

        # TTS is a capability fact (audio out, no text out) — never a name or
        # api_class probe. Mirrors translate_request's speech predicate.
        caps = profile.capabilities
        is_tts = caps.produces_audio and not caps.produces_text

        if is_tts:
            from matrx_ai.catalog.resolve import resolve_tts_voice, validate_tts_voices
            tts = unified_config.tts_voice_config
            if tts is None:
                unified_config.tts_voice = resolve_tts_voice(profile, None)
            elif tts.is_multi_speaker:
                validate_tts_voices(profile, [speaker.voice for speaker in tts.speakers])
            elif not tts.is_multi_speaker:
                unified_config.tts_voice = resolve_tts_voice(profile, tts._primary_voice())

        # Custom Dictionary pronunciation floor for Gemini-TTS — it has no native
        # pronunciation channel (no SSML/phoneme/customPronunciations), so
        # substitute respellings into the spoken text before translation builds
        # `contents`. The pronunciation directive folded into the first user turn
        # by the translator still rides along as a soft nudge.
        # See docs/dictionary/providers/google.md.
        if is_tts and unified_config.dictionary is not None:
            from matrx_ai.config.dictionary_config import apply_tts_dictionary

            for _msg in unified_config.messages:
                for _c in getattr(_msg, "content", None) or []:
                    _t = getattr(_c, "text", None)
                    if _t:
                        _new = apply_tts_dictionary(
                            unified_config.dictionary,
                            _t,
                            provider="google",
                            model=unified_config.model,
                        )
                        if _new != _t:
                            try:
                                _c.text = _new
                            except Exception:  # noqa: BLE001 — best-effort, never break a render
                                pass

        config_data: GoogleProviderConfig = self.translator.build_request(unified_config, profile)
        capture_request_payload(
            config_data,
            provider="google",
            wire_format=profile.wire_format,
            debug=debug,
        )
        matrx_model_name = unified_config.model
        stamp_call_meta(
            provider="google",
            model=matrx_model_name,
            is_streaming=bool(unified_config.stream),
        )

        # Google's SDK uses a sync httpx client for its non-aio entry points,
        # so the request hook installed via make_capture_http_client doesn't
        # cleanly fire here. Emit an explicit CONTEXT_ANALYSIS using the
        # final dataclass config — the SDK serializes this same shape into
        # the on-wire JSON body. No duplicates: we don't install the hook
        # on the Google client.
        try:
            import dataclasses as _dc

            if _dc.is_dataclass(config_data) and not isinstance(config_data, type):
                _body = _dc.asdict(config_data)
            elif hasattr(config_data, "model_dump"):
                _body = config_data.model_dump()
            elif isinstance(config_data, dict):
                _body = dict(config_data)
            else:
                _body = {"_repr": repr(config_data)}
            _model_for_url = _body.get("model") or matrx_model_name or "unknown"
            _stream_suffix = (
                ":streamGenerateContent" if unified_config.stream else ":generateContent"
            )
            await emit_explicit_context_analysis(
                provider="google",
                method="POST",
                url=(
                    "https://generativelanguage.googleapis.com/v1beta/models/"
                    f"{_model_for_url}{_stream_suffix}"
                ),
                headers={"Content-Type": "application/json"},
                body=_body,
                is_streaming=bool(unified_config.stream),
                model=matrx_model_name,
            )
        except Exception:
            pass

        vcprint(f"[Google Chat] executing, with debug: {self.debug}", color="blue")
        # rich.print(config_data)

        if self.debug:
            rich.print(_sanitize_for_debug(config_data))

        try:
            if unified_config.stream:
                accumulated_chunks: list[GenerateContentResponse] = []
                audio_chunk_count = 0
                stream_id = ""
                seq = 0

                if is_tts:
                    # Gemini streams TTS as a sequence of RAW PCM segments. A
                    # single provider call over a LONG script routinely runs long
                    # enough to trip the stall watchdog and discard ~minutes of
                    # billed audio (2026-07-10 incident: 4449 chunks / 367s then a
                    # 250s stall on a full education-deck script → 0 episodes).
                    # The fix is to split a long transcript into several short TTS
                    # calls so no single stream must survive that long, accumulate
                    # ALL of their raw-PCM chunks into one list (the translator then
                    # persists ONE concatenated file), retry a stalled short segment
                    # once, and — if a segment still stalls after we've already
                    # rendered earlier ones — finalize the substantially-complete
                    # episode from the billed audio in hand rather than discarding
                    # it. Short scripts take exactly the original single-call path.
                    stream_id, seq, audio_chunk_count = await self._run_segmented_tts(
                        config_data=config_data,
                        accumulated_chunks=accumulated_chunks,
                        emitter=emitter,
                        matrx_model_name=matrx_model_name,
                    )
                else:
                    chunk: GenerateContentResponse
                    # Reset per-stream reasoning-lifecycle state so a signal left
                    # open by a prior request on a reused instance can't leak in.
                    self._reasoning_signaled = False
                    # Use the SDK's async client so the blocking ssl.read() in the
                    # sync httpx transport never runs on the event loop. The sync
                    # path froze the entire process for 2s+ between chunks (loop
                    # watchdog incident 2026-06-10).
                    async for chunk in await self.client.aio.models.generate_content_stream(
                        **config_data
                    ):
                        accumulated_chunks.append(chunk)
                        if chunk.candidates:
                            cand: Candidate
                            for cand in chunk.candidates:
                                if cand.content and cand.content.parts:
                                    part: Part
                                    for part in cand.content.parts:
                                        await self._handle_part(
                                            part, emitter, unified_config.audio_format
                                        )
                        await asyncio.sleep(0)
                    # Safety net: if the stream ended while still "thinking"
                    # (reasoning parts with no following content), close the
                    # lifecycle signal so the UI never stays stuck in a thinking
                    # state. No-op when a content part already closed it.
                    await self._signal_reasoning_stopped(emitter)

                converted_response = await self.translator.from_google_async(
                    accumulated_chunks, matrx_model_name, unified_config.audio_format
                )
                # Emit audio URLs from the converted response (avoids double-saving
                # since from_google is the authoritative save path for inline_data)
                await self._emit_media_from_response(converted_response, emitter)
                # Grounding metadata only exists at stream settle — emit the
                # normalized citations now so the FE gets them without waiting
                # for persistence.
                await self._emit_citations_from_response(converted_response, emitter)
                if is_tts:
                    # Tell the client the live stream is done and which persisted
                    # file is now authoritative (swap the buffered PCM for it).
                    await self._emit_audio_stream_end(converted_response, emitter, stream_id, seq)
            else:
                # Non-streaming mode - returns single GenerateContentResponse.
                # Async client keeps the blocking provider call off the loop.
                response: GenerateContentResponse = await self.client.aio.models.generate_content(
                    **config_data
                )

                # Wrap the single response in a list to maintain consistency with to_unified_config
                accumulated_chunks: list[GenerateContentResponse] = [response]

                converted_response = await self.translator.from_google_async(
                    accumulated_chunks, matrx_model_name, unified_config.audio_format
                )
                # Emit audio/media URLs through the emitter
                await self._emit_media_from_response(converted_response, emitter)
                await self._emit_citations_from_response(converted_response, emitter)

                # Also emit text parts through emitter for non-streaming mode
                if response.candidates:
                    cand: Candidate
                    for cand in response.candidates:
                        if cand.content and cand.content.parts:
                            part: Part
                            for part in cand.content.parts:
                                await self._handle_part(part, emitter, unified_config.audio_format)

            return converted_response

        except Exception as e:
            # Import here to avoid circular dependency
            from matrx_ai.providers.errors import classify_google_error, mark_billing_checked

            # Honor a classification the raising site already attached (e.g. the
            # non-retryable TTS stall/ceiling abort) — never let the generic
            # classifier overwrite it back into a retryable unknown_error.
            error_info = getattr(e, "error_info", None) or classify_google_error(e)

            # A provider bills us the instant the call starts. Gemini emits
            # usage_metadata on its stream chunks (typically the last) — if the
            # stream failed mid-flight after some chunks arrived, recover that
            # billed usage from the accumulated chunks and stamp it onto the error
            # so the failed cx_request row carries real cost, not $0.
            # A pre-response 5xx still crossed the provider wire. Mark that the
            # adapter inspected the failure even when Gemini returned no chunk
            # carrying usage.
            mark_billing_checked(e)
            _chunks = locals().get("accumulated_chunks")
            if _chunks:
                self._attach_billed_usage_from_chunks(e, _chunks, matrx_model_name)

            e.error_info = error_info
            raise

    def _attach_billed_usage_from_chunks(
        self,
        exc: BaseException,
        chunks: list[Any],
        matrx_model_name: str,
    ) -> None:
        """Best-effort: recover billed usage from the last Gemini stream chunk
        that carried ``usage_metadata`` and stamp it onto a failing/cancelling
        exception. Never raises, never overwrites an already-attached usage."""
        # LAYER 2: the mark means "an adapter LOOKED", which is true even when
        # there is nothing to attach — it must precede every early return.
        from matrx_ai.providers.errors import mark_billing_checked

        mark_billing_checked(exc)
        try:
            usage_metadata = None
            for chunk in reversed(chunks):
                um = getattr(chunk, "usage_metadata", None)
                if um is not None:
                    usage_metadata = um
                    break
            if usage_metadata is None:
                return
            from matrx_ai.config import TokenUsage
            from matrx_ai.providers.errors import attach_billed_usage

            token_usage = TokenUsage.from_gemini(
                usage_metadata,
                matrx_model_name=matrx_model_name,
                provider_model_name=matrx_model_name,
            )
            attach_billed_usage(exc, token_usage)
        except Exception as err:
            from matrx_ai.providers.errors import report_billed_usage_capture_failure

            report_billed_usage_capture_failure("google", err)

    @staticmethod
    def _tts_stream_id() -> str:
        from matrx_ai.context.app_context import get_app_context

        try:
            rid = getattr(get_app_context(), "request_id", None)
        except Exception:
            rid = None
        return str(rid) if rid else uuid.uuid4().hex

    async def _run_segmented_tts(
        self,
        *,
        config_data: dict[str, Any],
        accumulated_chunks: list[GenerateContentResponse],
        emitter: Emitter,
        matrx_model_name: str,
    ) -> tuple[str, int, int]:
        """Render TTS as one or more short streaming calls, all accumulating into
        ``accumulated_chunks`` (→ ONE concatenated file at persist time).

        Layered extinction of the long-render stall (each layer sufficient alone,
        each LOUD when it fires):
          1. Split a long transcript into short segments so no single stream runs
             long enough to stall — the primary fix.
          2. Retry a stalled short segment ONCE (a stall is transient).
          3. If a segment still stalls after earlier ones rendered, finalize the
             substantially-complete episode from billed audio in hand — never
             discard it. Only a first-segment total failure hard-aborts.
        Returns ``(stream_id, seq, audio_chunk_count)``."""
        stream_id = self._tts_stream_id()
        await emitter.send_info(
            InfoPayload(
                code="tts_generating",
                system_message="Generating audio...",
                user_message="Generating audio...",
            )
        )

        full_text = _iter_tts_user_text(config_data["contents"])
        required = _required_speaker_labels(config_data["config"])
        model = config_data["model"]
        cfg = config_data["config"]
        max_chars = _tts_segment_chars(str(model))
        segments = _split_tts_text(full_text, required, max_chars=max_chars)
        if len(segments) > 1:
            vcprint(
                f"[Google TTS] Long transcript ({len(full_text)} chars) → "
                f"{len(segments)} segmented TTS calls (<= {max_chars} "
                f"chars each) so no single provider stream can run long enough to "
                f"stall (2026-07-10 incident) or to enter this model's long-form "
                f"quality-degradation window (see _TTS_MAX_CHARS_BY_MODEL).",
                color="cyan",
            )

        seq = 0
        audio_chunk_count = 0
        completed_segments = 0
        for idx, seg_text in enumerate(segments):
            seg_config_data = {
                "model": model,
                "contents": [{"role": "user", "parts": [{"text": seg_text}]}],
                "config": cfg,
            }
            attempt = 0
            while True:
                try:
                    seq, added = await self._stream_one_tts_call(
                        seg_config_data,
                        emitter,
                        stream_id,
                        seq,
                        accumulated_chunks,
                        segment_index=idx,
                        segment_total=len(segments),
                    )
                    audio_chunk_count += added
                    completed_segments += 1
                    break
                except _TTSSegmentStall as stall:
                    if attempt < _TTS_SEGMENT_STALL_RETRIES:
                        attempt += 1
                        vcprint(
                            f"[Google TTS] Segment {idx + 1}/{len(segments)} stalled "
                            f"({stall}) — retrying once (attempt {attempt}) after "
                            f"{_TTS_SEGMENT_RETRY_BACKOFF_SECONDS}s. A stall is "
                            f"transient; re-billing one short segment, never the run.",
                            color="yellow",
                        )
                        await emitter.send_info(
                            InfoPayload(
                                code="tts_segment_retry",
                                system_message=(
                                    f"Audio segment {idx + 1}/{len(segments)} stalled; "
                                    "retrying that segment."
                                ),
                                user_message="Audio is taking longer than expected; retrying...",
                            )
                        )
                        await asyncio.sleep(_TTS_SEGMENT_RETRY_BACKOFF_SECONDS)
                        continue
                    # Segment stalled twice. If earlier segments rendered, keep the
                    # billed audio and finalize the substantially-complete episode
                    # — LOUD, but recovered, not discarded.
                    if completed_segments >= 1 and accumulated_chunks:
                        msg = (
                            f"Google TTS segment {idx + 1}/{len(segments)} stalled after "
                            f"a retry (model={matrx_model_name}). {completed_segments} of "
                            f"{len(segments)} segments rendered — FINALIZING the partial "
                            f"episode from billed audio already received (NOT discarding "
                            f"it)."
                        )
                        vcprint(f"[Google TTS] PARTIAL RECOVERY — {msg}", color="red")
                        await emitter.send_info(
                            InfoPayload(
                                code="tts_partial_recovered",
                                system_message=msg,
                                user_message=(
                                    "Some audio didn't finish generating; saved the part "
                                    "that completed."
                                ),
                            )
                        )
                        return stream_id, seq, audio_chunk_count
                    # First segment produced nothing usable → genuine, non-retryable
                    # abort (unchanged behavior for the no-audio case).
                    await self._raise_tts_abort(
                        emitter,
                        reason=str(stall),
                        model=matrx_model_name,
                        chunks=seq,
                        elapsed=0.0,
                    )

        await emitter.send_info(
            InfoPayload(
                code="tts_saving",
                system_message=f"Audio received ({audio_chunk_count} segments). Saving...",
                user_message="Audio received. Saving...",
            )
        )
        return stream_id, seq, audio_chunk_count

    async def _stream_one_tts_call(
        self,
        config_data: dict[str, Any],
        emitter: Emitter,
        stream_id: str,
        seq: int,
        accumulated_chunks: list[GenerateContentResponse],
        *,
        segment_index: int,
        segment_total: int,
    ) -> tuple[int, int]:
        """Run ONE Gemini-TTS streaming call. Appends every response chunk to
        ``accumulated_chunks`` (so the caller persists one concatenated file),
        forwards each raw-PCM audio segment live as ``AudioStreamChunkData``
        (``seq`` continues across segments), and RAISES ``_TTSSegmentStall`` on a
        dead-air stall or a blown per-segment ceiling. Returns
        ``(next_seq, audio_chunks_emitted)``.

        The provider stream is a blocking sync generator, so it runs in a worker
        thread (producer) while we consume on the loop (consumer); the arriving
        chunks double as the liveness heartbeat. On a stall we deliberately do NOT
        await the abandoned producer — the SDK http read-timeout backstop caps the
        orphaned thread — exactly as the original single-call path did."""
        loop = asyncio.get_event_loop()
        chunk_queue: asyncio.Queue = asyncio.Queue()
        producer_state: dict[str, BaseException | None] = {"error": None}

        def _produce_tts_chunks() -> None:
            try:
                for chunk in self.client.models.generate_content_stream(**config_data):
                    loop.call_soon_threadsafe(chunk_queue.put_nowait, chunk)
            except BaseException as exc:  # surface provider errors to consumer
                producer_state["error"] = exc
            finally:
                loop.call_soon_threadsafe(chunk_queue.put_nowait, _TTS_STREAM_DONE)

        text_len = len(_iter_tts_user_text(config_data["contents"]))
        total_budget = _tts_total_budget_seconds(text_len)
        label = f"segment {segment_index + 1}/{segment_total} " if segment_total > 1 else ""
        vcprint(
            f"[Google TTS] Streaming audio {label}(stall>{_TTS_STALL_TIMEOUT_SECONDS}s; "
            f"ceiling {total_budget}s for {text_len} chars)...",
            color="cyan",
        )

        started_at = time.monotonic()
        producer = loop.run_in_executor(None, _produce_tts_chunks)
        audio_chunk_count = 0
        audio_bytes_total = 0
        received_any = False
        while True:
            # Dead-air detection only makes sense BETWEEN chunks. Before the FIRST
            # chunk, generation latency dominates, so the length-scaled total
            # budget is the only honest guard until something arrives.
            timeout = (
                _TTS_STALL_TIMEOUT_SECONDS
                if received_any
                else max(1.0, total_budget - (time.monotonic() - started_at))
            )
            try:
                item = await asyncio.wait_for(chunk_queue.get(), timeout=timeout)
            except TimeoutError:
                raise _TTSSegmentStall(
                    f"no audio chunk for {_TTS_STALL_TIMEOUT_SECONDS}s (stall)"
                    if received_any
                    else f"no first chunk within the {total_budget:.0f}s budget"
                ) from None
            received_any = True

            if item is _TTS_STREAM_DONE:
                if producer_state["error"] is not None:
                    raise producer_state["error"]
                break

            chunk = item
            accumulated_chunks.append(chunk)

            elapsed = time.monotonic() - started_at
            if elapsed >= total_budget:
                raise _TTSSegmentStall(f"exceeded {total_budget}s total budget")

            if chunk.candidates:
                for cand in chunk.candidates:
                    if cand.content and cand.content.parts:
                        for part in cand.content.parts:
                            idata = getattr(part, "inline_data", None)
                            if not idata:
                                continue
                            raw_mime = idata.mime_type or ""
                            if not raw_mime.lower().startswith("audio/"):
                                continue
                            seq = await self._emit_audio_stream_chunk(
                                emitter, stream_id, seq, idata.data, raw_mime
                            )
                            audio_chunk_count += 1
                            audio_bytes_total += len(idata.data)
            await asyncio.sleep(0)

        await producer  # sentinel already sent; thread has finished
        vcprint(
            f"[Google TTS] {label or 'Stream '}complete: {audio_chunk_count} audio "
            f"segments ({audio_bytes_total} bytes) in {time.monotonic() - started_at:.0f}s",
            color="cyan",
        )
        return seq, audio_chunk_count

    async def _emit_audio_stream_chunk(
        self,
        emitter: Emitter,
        stream_id: str,
        seq: int,
        data: bytes,
        raw_mime: str,
    ) -> int:
        """Forward one raw-PCM segment to the client; return the next seq."""
        from matrx_connect.context.data_types import AudioStreamChunkData

        from matrx_ai.media.media_persistence import AIMediaHandler

        bits, rate = AIMediaHandler._parse_pcm_mime_params(raw_mime)
        await emitter.send_data(
            AudioStreamChunkData(
                stream_id=stream_id,
                seq=seq,
                audio_base64=base64.b64encode(data).decode("ascii"),
                mime_type=raw_mime or "audio/L16",
                sample_rate=rate,
                bits_per_sample=bits,
                channels=1,
            )
        )
        await asyncio.sleep(0)
        return seq + 1

    async def _raise_tts_abort(
        self,
        emitter: Emitter,
        *,
        reason: str,
        model: str,
        chunks: int,
        elapsed: float,
    ) -> None:
        """Emit a captured, NON-retryable TTS abort and raise. Never returns."""
        from matrx_ai.providers.errors import RetryableError

        msg = (
            f"Google TTS stream aborted — {reason} "
            f"(model={model}, {chunks} audio chunks received in {elapsed:.0f}s). "
            "The in-flight provider call was already billed; capturing and "
            "stopping WITHOUT retry."
        )
        vcprint(f"[Google TTS] ABORT — {msg}", color="red")
        await emitter.send_info(
            InfoPayload(
                code="tts_stalled",
                system_message=msg,
                user_message="Audio generation stalled and was stopped.",
            )
        )
        exc = TimeoutError(msg)
        # Non-retryable: re-running a long, already-paid render just multiplies
        # cost for the same likely outcome.
        exc.error_info = RetryableError(
            error_type="tts_stall_timeout",
            message=msg,
            is_retryable=False,
            user_message="Audio generation stalled and was stopped. Please try again.",
        )
        raise exc

    async def _emit_audio_stream_end(
        self,
        response: UnifiedResponse,
        emitter: Emitter,
        stream_id: str,
        total_chunks: int,
    ) -> None:
        """Signal end of a live audio stream + hand over the canonical file."""
        from matrx_connect.context.data_types import AudioStreamEndData

        from matrx_ai.config.media_config import AudioContent

        audio: AudioContent | None = None
        if response and response.messages:
            for msg in response.messages:
                for item in msg.content:
                    if isinstance(item, AudioContent) and item.url:
                        audio = item
                        break
                if audio:
                    break

        await emitter.send_data(
            AudioStreamEndData(
                stream_id=stream_id,
                total_chunks=total_chunks,
                url=audio.url if audio else "",
                mime_type=(audio.mime_type if audio and audio.mime_type else "audio/wav"),
                file_id=audio.file_id if audio else None,
                duration_ms=audio.duration_ms if audio else None,
            )
        )

    async def _emit_citations_from_response(
        self, response: UnifiedResponse, emitter: Emitter
    ) -> None:
        """Emit typed `citation` events for grounding citations on the response.

        Gemini delivers grounding metadata only at stream settle (on the final
        chunks), so this is the earliest possible emission point — the
        translator has already normalized supports×chunks into the canonical
        shape on each text block's metadata["citations"]. Delegates to the ONE
        shared settle-time emitter (providers/citation_emit.py)."""
        from matrx_ai.providers.citation_emit import emit_citations_from_response

        await emit_citations_from_response(response, emitter, "GOOGLE")

    async def _emit_media_from_response(self, response: UnifiedResponse, emitter: Emitter) -> None:
        """Emit audio_output / image_output events for any media in the response."""
        from matrx_ai.config.media_config import AudioContent, ImageContent

        if not emitter or not response or not response.messages:
            return

        from matrx_connect.context.data_types import MediaBlockData
        from matrx_connect.context.media_block import (
            cloud_file_to_media_block,
            external_url_to_media_block,
        )

        for msg in response.messages:
            for content_item in msg.content:
                if isinstance(content_item, AudioContent) and content_item.url:
                    if content_item.file_id:
                        block = cloud_file_to_media_block(
                            {
                                "id": content_item.file_id,
                                "storage_uri": content_item.file_uri,
                                "mime_type": content_item.mime_type,
                                "size_bytes": content_item.file_size,
                            },
                            kind_override="audio",
                        )
                    else:
                        block = external_url_to_media_block(
                            content_item.url,
                            kind="audio",
                            mime_type=content_item.mime_type,
                        )
                    await emitter.send_data(MediaBlockData(block=block))
                    await asyncio.sleep(0)
                elif isinstance(content_item, ImageContent) and content_item.url:
                    if content_item.file_id:
                        block = cloud_file_to_media_block(
                            {
                                "id": content_item.file_id,
                                "storage_uri": content_item.file_uri,
                                "mime_type": content_item.mime_type,
                                "size_bytes": content_item.file_size,
                            },
                            kind_override="image",
                        )
                    else:
                        block = external_url_to_media_block(
                            content_item.url,
                            kind="image",
                            mime_type=content_item.mime_type,
                        )
                    await emitter.send_data(MediaBlockData(block=block))
                    await asyncio.sleep(0)

    async def _signal_reasoning_started(self, emitter: Emitter) -> None:
        """Emit the content-less 'reasoning started' signal once per reasoning
        run. Idempotent — safe to call on every thought part."""
        if emitter and not self._reasoning_signaled:
            self._reasoning_signaled = True
            await emitter.send_reasoning_state("started")

    async def _signal_reasoning_stopped(self, emitter: Emitter) -> None:
        """Emit 'reasoning stopped' iff a 'started' is outstanding. Idempotent —
        safe to call on the first content part and again at stream end."""
        if emitter and self._reasoning_signaled:
            self._reasoning_signaled = False
            await emitter.send_reasoning_state("stopped")

    async def _handle_part(self, part: Part, emitter: Emitter, audio_format: str | None = None):
        await asyncio.sleep(0)

        # vcprint(part, "PART", color="green")

        if part.thought:
            # A thought part — the model is reasoning. Signal it (content-less)
            # even when part.text is empty, then stream the thought text if any.
            await self._signal_reasoning_started(emitter)
            if emitter:
                await emitter.send_chunk(f"\n<reasoning>\n {part.text} \n</reasoning>\n")
                # print(part.text)
                await asyncio.sleep(0)
            else:
                print(f"\n<reasoning>\n {part.text} \n</reasoning>\n")

        elif part.text:
            # Real answer content — reasoning (if any) is over.
            await self._signal_reasoning_stopped(emitter)
            if emitter:
                await emitter.send_chunk(part.text)
                await asyncio.sleep(0)
            else:
                print(part.text)

        elif part.inline_data:
            # Inline media (audio/image) is saved and emitted by _emit_media_from_response
            # after from_google() processes all chunks — skip here to avoid double-saving.
            await self._signal_reasoning_stopped(emitter)

        elif part.function_call:
            await self._signal_reasoning_stopped(emitter)

        elif part.thought_signature:
            # A bare thought_signature part (no thought flag, no text) is the ONLY
            # on-wire evidence the model reasoned when include_thoughts=False —
            # this is the Gemini case where the UI otherwise sees nothing but
            # heartbeats. Emit the content-less "reasoning started" signal; the
            # first content part (or stream end) closes it.
            await self._signal_reasoning_started(emitter)

        else:
            pass

        if LOCAL_DEBUG:
            await self._debug_part(part)

    async def _debug_part(self, part: Part):
        if part.thought:
            vcprint("=================== THOUGHT ===================", color="blue")
            print(part.text)
            vcprint("================================================", color="blue")
        elif part.text:
            print(part.text)
        elif part.function_call:
            vcprint(part.function_call, "Function Call", color="blue")
        elif part.thought_signature:
            vcprint("Empty Thought Signature", color="blue")
        else:
            vcprint(part, "Empty Part", color="blue")
