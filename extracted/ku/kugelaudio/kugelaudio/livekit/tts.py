# Copyright 2024 KugelAudio
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""KugelAudio TTS plugin for LiveKit Agents.

Uses a single persistent WebSocket to /ws/tts/multi with context IDs.
Each synthesize() or stream() call gets a unique context_id; the shared
connection multiplexes all contexts.  On barge-in (cancellation), the
context is deregistered locally and late server messages are silently
discarded.  A context's waiter resolves only on ``context_closed`` — the
server sends that frame after draining every audio frame, so the tail
is never clipped.
"""

from __future__ import annotations

import asyncio
import base64
import collections
import json
import logging
import os
import time
from dataclasses import dataclass, field, replace
from dataclasses import fields as dataclass_fields
from typing import Any

import aiohttp
from kugelaudio._sdk_metadata import sdk_query_string
from kugelaudio.client import _parse_api_key, _resolve_region_url
from kugelaudio.models import clamp_cfg_scale
from kugelaudio.exceptions import ValidationError, classify_ws_frame
from livekit.agents import (
    APIConnectionError,
    APIConnectOptions,
    APIStatusError,
    APITimeoutError,
    tts,
    utils,
)
from livekit.agents.types import DEFAULT_API_CONNECT_OPTIONS, NOT_GIVEN, NotGivenOr
from livekit.agents.utils import is_given
from livekit.agents.voice.io import TimedString

from .models import (
    DEFAULT_MODEL,
    DEFAULT_SAMPLE_RATE,
    SUPPORTED_SAMPLE_RATES,
    TTSModels,
)

logger = logging.getLogger("kugelaudio.livekit")


def _append_sdk_query(url: str) -> str:
    separator = "&" if "?" in url else "?"
    return f"{url}{separator}{sdk_query_string()}"


def _word_timestamps_to_timed(
    timestamps: list[dict[str, Any]],
) -> list[TimedString]:
    """Convert server word_timestamps payload to LiveKit TimedString list.

    The server sends timestamps with ``start_ms`` / ``end_ms`` (integers),
    while LiveKit expects ``start_time`` / ``end_time`` in seconds (floats).
    """
    return [
        TimedString(
            ts["word"],
            start_time=ts["start_ms"] / 1000.0,
            end_time=ts["end_ms"] / 1000.0,
        )
        for ts in timestamps
    ]


SUPPORTED_LANGUAGES: set[str] = {
    # Germanic
    "de",
    "en",
    "nl",
    "sv",
    "da",
    "no",
    # Romance
    "fr",
    "es",
    "it",
    "pt",
    "ro",
    # Slavic
    "pl",
    "cs",
    "uk",
    "bg",
    "sk",
    "sl",
    "hr",
    "sr",
    # Uralic
    "fi",
    "hu",
    # Other European
    "el",
    "tr",
    "ru",
    # CJK + SEA
    "zh",
    "ja",
    "ko",
    "vi",
    "yue",
    "th",
    "id",
    "ms",
    # Semitic + Indic + Other
    "ar",
    "hi",
    "he",
    "fa",
    "ur",
    "bn",
    "ta",
}


def _validate_language(language: str | None) -> str | None:
    """Validate that language is an ISO 639-1 code supported by the API.

    Raises:
        ValueError: If *language* is not a supported ISO 639-1 code.
            Common mistake: passing BCP 47 locale tags such as ``"de-DE"``
            instead of ``"de"``.
    """
    if language is None:
        return None
    if language not in SUPPORTED_LANGUAGES:
        raise ValueError(
            f"language must be a supported ISO 639-1 code "
            f"({', '.join(sorted(SUPPORTED_LANGUAGES))}), got {language!r}. "
            f"Note: BCP 47 tags like 'de-DE' are not accepted — use 'de' instead."
        )
    return language


@dataclass
class _TTSOptions:
    model: TTSModels | str
    voice_id: int | None
    sample_rate: int
    cfg_scale: float
    max_new_tokens: int
    api_key: str
    base_url: str
    word_timestamps: bool = False
    normalize: bool = True
    language: str | None = None

    def __post_init__(self) -> None:
        self.language = _validate_language(self.language)


@dataclass
class _SynthesizeContent:
    """Text message to send to a specific context."""

    context_id: str
    text: str
    flush: bool = False


@dataclass
class _CloseContext:
    """Signal to close a specific context on the server.

    ``immediate=True`` is sent on barge-in (caller cancelled _run).  The
    server cancels in-flight generation instead of draining — stops
    wasted GPU on audio the client will discard anyway.  End-of-stream
    closes from ``_input_task`` use the default (graceful drain).
    """

    context_id: str
    immediate: bool = False


@dataclass
class _ContextData:
    """Per-context state tracked inside _Connection.

    ``last_activity_at`` is refreshed every time the recv loop routes a
    server message to this context.  The per-run idle timeout uses it to
    distinguish "server is silent" from "server is still working".
    """

    emitter: tts.AudioEmitter
    waiter: asyncio.Future[None]
    stream: "SynthesizeStream | None" = None
    last_activity_at: float = field(default_factory=time.monotonic)


async def _wait_for_context_idle(
    ctx: _ContextData,
    waiter: asyncio.Future[None],
    idle_threshold: float,
) -> None:
    """Block until *waiter* resolves, failing only if the server has been
    silent for this context for longer than *idle_threshold* seconds.

    Unlike ``asyncio.wait_for(waiter, idle_threshold)``, this helper polls
    ``ctx.last_activity_at`` on every tick so long-running generations do
    not time out as long as frames keep arriving.
    """
    # Poll cadence is small so the effective idle-deadline resolution is
    # sub-second; callers only care that we do not fail early when frames
    # keep arriving.
    tick = min(1.0, max(0.1, idle_threshold / 4))
    while True:
        try:
            await asyncio.wait_for(asyncio.shield(waiter), timeout=tick)
            return
        except asyncio.TimeoutError:
            if time.monotonic() - ctx.last_activity_at >= idle_threshold:
                raise


def _api_status_error_from_ingress_payload(
    data: dict[str, Any], *, request_id: str = ""
) -> APIStatusError:
    """Convert an ingress WS error frame into LiveKit's status exception."""
    err = classify_ws_frame(data)
    status_code = err.status_code
    if status_code is None:
        code = data.get("code")
        status_code = code if isinstance(code, int) else 500
    return APIStatusError(
        message=err.message,
        status_code=status_code,
        request_id=request_id,
        body=data,
    )


def _api_status_error_from_handshake(
    exc: aiohttp.WSServerHandshakeError,
) -> APIStatusError:
    """Convert a rejected WS upgrade into LiveKit's status exception."""
    status_code = exc.status if isinstance(exc.status, int) else 500
    message = exc.message or str(exc)
    return APIStatusError(
        message=message,
        status_code=status_code,
        request_id="",
        body={"error": message, "code": status_code},
    )


class _Connection:
    """Single persistent WebSocket to /ws/tts/multi with background loops.

    Each synthesis (chunked or streaming) registers a unique context_id.
    The recv loop routes server messages by context_id; unknown IDs are
    silently dropped — this is what makes barge-in safe.
    """

    def __init__(self, opts: _TTSOptions, session: aiohttp.ClientSession) -> None:
        self._opts = replace(opts)
        self._session = session
        self._ws: aiohttp.ClientWebSocketResponse | None = None
        self._is_current = True
        self._closed = False
        self._active_contexts: set[str] = set()
        self._input_queue: asyncio.Queue[_SynthesizeContent | _CloseContext | None] = (
            asyncio.Queue()
        )
        self._context_data: dict[str, _ContextData] = {}
        # ctx_ids we have already logged a "dropped late frame" for —
        # bounded so a long-lived connection doesn't grow unboundedly.
        self._logged_late_drops: collections.deque[str] = collections.deque(maxlen=64)
        self._send_task: asyncio.Task | None = None
        self._recv_task: asyncio.Task | None = None

    @property
    def is_current(self) -> bool:
        return self._is_current

    def mark_non_current(self) -> None:
        self._is_current = False

    async def connect(self, timeout: float = 10.0) -> None:
        ws_url = self._opts.base_url.replace("https://", "wss://").replace(
            "http://", "ws://"
        )
        ws_url = _append_sdk_query(f"{ws_url}/ws/tts/multi?api_key={self._opts.api_key}")
        try:
            self._ws = await self._session.ws_connect(
                ws_url,
                timeout=aiohttp.ClientTimeout(total=None, sock_connect=timeout),
            )
        except asyncio.TimeoutError:
            raise APITimeoutError() from None
        except aiohttp.WSServerHandshakeError as e:
            raise _api_status_error_from_handshake(e) from e
        except aiohttp.ClientError as e:
            raise APIConnectionError(f"Failed to connect to /ws/tts/multi: {e}") from e
        self._send_task = asyncio.create_task(self._send_loop())
        self._recv_task = asyncio.create_task(self._recv_loop())
        logger.debug("Connection established to /ws/tts/multi")

    def register_context(
        self,
        context_id: str,
        emitter: tts.AudioEmitter,
        waiter: asyncio.Future[None],
        stream: "SynthesizeStream | None" = None,
    ) -> _ContextData | None:
        # If the connection closed between _ensure_connection returning and
        # this call (e.g., update_options raced with an in-flight _run),
        # reject immediately instead of inserting a waiter nobody will resolve.
        if self._closed:
            if not waiter.done():
                waiter.set_exception(
                    APIConnectionError("Connection closed before request started")
                )
            return None
        ctx = _ContextData(
            emitter=emitter,
            waiter=waiter,
            stream=stream,
        )
        self._context_data[context_id] = ctx
        return ctx

    def send_content(self, content: _SynthesizeContent) -> None:
        self._input_queue.put_nowait(content)

    def request_close_context(
        self, context_id: str, immediate: bool = False,
    ) -> None:
        self._input_queue.put_nowait(_CloseContext(context_id, immediate=immediate))

    def _cleanup_context(self, context_id: str) -> None:
        self._context_data.pop(context_id, None)
        self._active_contexts.discard(context_id)

    async def _send_loop(self) -> None:
        assert self._ws is not None
        try:
            while not self._closed:
                item = await self._input_queue.get()
                if item is None:
                    break

                if isinstance(item, _CloseContext):
                    payload: dict[str, Any] = {
                        "close_context": True,
                        "context_id": item.context_id,
                    }
                    if item.immediate:
                        payload["immediate"] = True
                    await self._ws.send_str(json.dumps(payload))
                    continue

                # _SynthesizeContent
                msg: dict[str, Any] = {
                    "text": item.text,
                    "context_id": item.context_id,
                }
                if item.flush:
                    msg["flush"] = True

                # First message for a new context: attach session + voice config
                if item.context_id not in self._active_contexts:
                    self._active_contexts.add(item.context_id)
                    msg["model_id"] = self._opts.model
                    msg["sample_rate"] = self._opts.sample_rate
                    msg["word_timestamps"] = self._opts.word_timestamps
                    msg["normalize"] = self._opts.normalize
                    if self._opts.language is not None:
                        msg["language"] = self._opts.language
                    voice_settings: dict[str, Any] = {}
                    if self._opts.voice_id is not None:
                        voice_settings["voice_id"] = self._opts.voice_id
                    if self._opts.cfg_scale != 2.0:
                        voice_settings["cfg_scale"] = self._opts.cfg_scale
                    if self._opts.max_new_tokens != 2048:
                        voice_settings["max_new_tokens"] = self._opts.max_new_tokens
                    if voice_settings:
                        msg["voice_settings"] = voice_settings

                await self._ws.send_str(json.dumps(msg))
        except Exception:
            # Mark dead so _ensure_connection reconnects next call, and
            # close the WS so _recv_loop exits and rejects pending waiters.
            self._is_current = False
            if self._ws and not self._ws.closed:
                await self._ws.close()
            raise

    async def _recv_loop(self) -> None:
        assert self._ws is not None
        try:
            await self._recv_loop_inner()
        finally:
            # Connection dropped or closed — mark dead so _ensure_connection
            # reconnects on the next call instead of handing out this zombie.
            self._is_current = False
            for ctx in list(self._context_data.values()):
                if not ctx.waiter.done():
                    ctx.waiter.set_exception(
                        APIConnectionError("WebSocket connection closed unexpectedly")
                    )

    async def _recv_loop_inner(self) -> None:
        assert self._ws is not None
        while not self._closed and not self._ws.closed:
            msg = await self._ws.receive()
            if msg.type != aiohttp.WSMsgType.TEXT:
                break
            data = json.loads(msg.data)

            if data.get("session_closed"):
                break

            context_id = data.get("context_id")

            # Error handling
            if data.get("error"):
                ctx = self._context_data.get(context_id) if context_id else None
                if ctx and not ctx.waiter.done():
                    ctx.waiter.set_exception(
                        _api_status_error_from_ingress_payload(
                            data,
                            request_id=context_id or "",
                        )
                    )
                if context_id:
                    self._cleanup_context(context_id)
                continue

            ctx = self._context_data.get(context_id) if context_id else None

            # Messages for unknown/cleaned-up contexts are silently discarded.
            # This is the core barge-in fix.  After a barge-in there's
            # always a small tail of in-flight frames (audio + the
            # context_closed confirmation) — log only the first per
            # ctx_id so the second/third frames don't spam the log.
            if ctx is None:
                if context_id and context_id not in self._logged_late_drops:
                    self._logged_late_drops.append(context_id)
                    logger.debug(
                        "[recv] dropped late frame(s) for closed ctx=%s "
                        "(further drops for this ctx will be silenced)",
                        context_id,
                    )
                continue

            # Any routed message counts as activity for the idle-timeout
            # watchdog in _run.  Update before per-field processing so
            # audio/chunk_complete/context_closed all refresh the deadline.
            ctx.last_activity_at = time.monotonic()

            if data.get("audio"):
                audio_bytes = base64.b64decode(data["audio"])
                if ctx.stream is not None:
                    ctx.stream._mark_started()
                ctx.emitter.push(audio_bytes)

            if data.get("word_timestamps"):
                ctx.emitter.push_timed_transcript(
                    _word_timestamps_to_timed(data["word_timestamps"])
                )

            if data.get("chunk_complete"):
                ctx.emitter.flush()
                # For non-streaming (chunked) contexts, close after the
                # server confirms generation is done — avoids the race
                # where close_context arrives before audio is generated.
                if ctx.stream is None:
                    self._input_queue.put_nowait(_CloseContext(context_id))

            if data.get("context_closed"):
                # Sole terminal signal. The server sends this only after it
                # has drained every audio frame for the context, so the
                # waiter resolves at the correct point for both streaming
                # and chunked contexts.
                if not ctx.waiter.done():
                    ctx.waiter.set_result(None)
                self._cleanup_context(context_id)

    async def aclose(self) -> None:
        if self._closed:
            return
        self._closed = True
        self._input_queue.put_nowait(None)
        for ctx in self._context_data.values():
            if not ctx.waiter.done():
                ctx.waiter.set_exception(APIConnectionError("Connection closed"))
        self._context_data.clear()
        if self._ws and not self._ws.closed:
            try:
                await self._ws.send_str(json.dumps({"close_socket": True}))
            except Exception:
                pass
            await self._ws.close()
        if self._send_task:
            await utils.aio.gracefully_cancel(self._send_task)
        if self._recv_task:
            await utils.aio.gracefully_cancel(self._recv_task)


class TTS(tts.TTS):
    """KugelAudio Text-to-Speech plugin for LiveKit Agents.

    This plugin integrates KugelAudio's TTS API with LiveKit's agent framework,
    providing high-quality voice synthesis with streaming support.

    Example:
        ```python
        from kugelaudio.livekit import TTS

        tts = TTS(api_key="your-api-key")

        # Use with VoicePipelineAgent
        agent = VoicePipelineAgent(
            tts=tts,
            ...
        )
        ```

    Or via the livekit.plugins namespace (after registering):
        ```python
        from kugelaudio.livekit import register_plugin
        register_plugin()

        from livekit.plugins import kugelaudio
        tts = kugelaudio.TTS()
        ```
    """

    def __init__(
        self,
        *,
        api_key: str | None = None,
        model: TTSModels | str = DEFAULT_MODEL,
        voice_id: int | None = None,
        sample_rate: int = DEFAULT_SAMPLE_RATE,
        cfg_scale: float = 2.0,
        max_new_tokens: int = 2048,
        normalize: bool = True,
        word_timestamps: bool = False,
        language: str | None = None,
        region: str | None = None,
        base_url: str | None = None,
        http_session: aiohttp.ClientSession | None = None,
    ) -> None:
        """Create a new KugelAudio TTS instance.

        Args:
            api_key: KugelAudio API key. If not provided, reads from
                KUGELAUDIO_API_KEY environment variable. Prefix with
                ``"eu-"`` to select the direct EU endpoint; the prefix is
                stripped before auth.
            model: TTS model to use. "kugel-1-turbo" (fast) or
                "kugel-1" (premium).
            voice_id: Voice ID to use. If None, uses server default.
            sample_rate: Output sample rate in Hz. Supported rates: 24000 (native),
                22050, 16000, 8000. Lower rates use server-side resampling with
                minimal latency impact (~0.1ms per 100ms of audio).
            cfg_scale: Classifier-free guidance scale. Clamped to [1.2, 2.5]. Defaults to 2.0.
            max_new_tokens: Maximum tokens to generate. Defaults to 2048.
            normalize: Apply loudness normalization to the output audio. Defaults
                to True.
            word_timestamps: Request per-chunk word-level timestamps for aligned
                transcript / barge-in. Defaults to False (matches the HTTP SDK).
                Enable only when your model supports server-side alignment;
                ``kugel-2.5`` and ``kugel-2-turbo`` may return a post-processing
                error when this is True.
            language: ISO 639-1 language code for text normalization (e.g. "de",
                "en", "fr"). When set, skips server-side auto-detection saving
                ~60-150ms per request. Supported: de, en, fr, es, it, pt, nl, pl,
                sv, da, no, fi, cs, hu, ro, el, uk, bg, tr, vi, ar, hi, zh, ja, ko,
                sk, sl, hr, sr, ru, he, fa, ur, bn, ta, yue, th, id, ms.
            region: API endpoint region. Use ``"eu"`` for the direct EU endpoint.
                Overrides any prefix detected from the API key. Ignored when
                *base_url* is set.
            base_url: API base URL. Overrides region selection entirely. Defaults
                to the default geo-routed API endpoint if no region is specified.
            http_session: Optional aiohttp session to reuse.
        """
        # ``aligned_transcript`` only exists on newer livekit-agents
        # TTSCapabilities; older 1.0.x raises TypeError on unknown kwargs.
        capability_kwargs: dict[str, Any] = {"streaming": True}
        if "aligned_transcript" in {
            f.name for f in dataclass_fields(tts.TTSCapabilities)
        }:
            capability_kwargs["aligned_transcript"] = word_timestamps
        super().__init__(
            capabilities=tts.TTSCapabilities(**capability_kwargs),
            sample_rate=sample_rate,
            num_channels=1,
        )

        kugelaudio_api_key = api_key or os.environ.get("KUGELAUDIO_API_KEY")
        if not kugelaudio_api_key:
            raise ValueError(
                "KUGELAUDIO_API_KEY must be set or api_key must be provided"
            )

        cfg_scale = clamp_cfg_scale(cfg_scale)

        clean_key, detected_region = _parse_api_key(kugelaudio_api_key)

        if base_url:
            resolved_url = base_url.rstrip("/")
        else:
            effective_region = region or detected_region
            try:
                resolved_url = _resolve_region_url(effective_region)
            except ValidationError as exc:
                raise ValueError(str(exc)) from exc

        self._opts = _TTSOptions(
            model=model,
            voice_id=voice_id,
            sample_rate=sample_rate,
            cfg_scale=cfg_scale,
            max_new_tokens=max_new_tokens,
            normalize=normalize,
            word_timestamps=word_timestamps,
            language=language,
            api_key=clean_key,
            base_url=resolved_url,
        )

        self._session = http_session
        self._current_connection: _Connection | None = None
        self._connection_lock = asyncio.Lock()

    @property
    def model(self) -> str:
        return self._opts.model

    @property
    def provider(self) -> str:
        return "KugelAudio"

    def _ensure_session(self) -> aiohttp.ClientSession:
        if not self._session:
            self._session = utils.http_context.http_session()
        return self._session

    async def _ensure_connection(self, timeout: float = 10.0) -> _Connection:
        """Get or create the persistent /ws/tts/multi connection."""
        async with self._connection_lock:
            if (
                self._current_connection
                and self._current_connection.is_current
                and not self._current_connection._closed
            ):
                return self._current_connection
            session = self._ensure_session()
            conn = _Connection(self._opts, session)
            await conn.connect(timeout)
            self._current_connection = conn
            return conn

    def prewarm(self) -> None:
        """Pre-warm the WebSocket connection to reduce TTFA on first synthesis.

        Call this from LiveKit's ``before_tts_cb`` or during agent setup
        to eagerly establish the WebSocket connection and authenticate,
        eliminating ~35-290ms of handshake latency from the first request.

        This is a synchronous method (as required by the LiveKit TTS interface)
        that schedules the async connection establishment in the background.

        Example:
            ```python
            tts = TTS(api_key="your-api-key")
            tts.prewarm()  # establishes WS connection in background
            ```
        """
        try:
            loop = asyncio.get_running_loop()
        except RuntimeError:
            logger.warning("prewarm() called outside event loop, skipping")
            return

        async def _do_prewarm() -> None:
            try:
                await self._ensure_connection(timeout=10.0)
                logger.info("KugelAudio TTS connection pre-warmed")
            except Exception:
                logger.warning(
                    "Failed to prewarm KugelAudio connection, "
                    "will retry on first synthesis",
                    exc_info=True,
                )

        loop.create_task(_do_prewarm())

    def update_options(
        self,
        *,
        model: NotGivenOr[TTSModels | str] = NOT_GIVEN,
        voice_id: NotGivenOr[int | None] = NOT_GIVEN,
        cfg_scale: NotGivenOr[float] = NOT_GIVEN,
        max_new_tokens: NotGivenOr[int] = NOT_GIVEN,
        normalize: NotGivenOr[bool] = NOT_GIVEN,
        word_timestamps: NotGivenOr[bool] = NOT_GIVEN,
        language: NotGivenOr[str | None] = NOT_GIVEN,
    ) -> None:
        """Update TTS options dynamically.

        Args:
            model: TTS model to use.
            voice_id: Voice ID to use.
            cfg_scale: Classifier-free guidance scale. Clamped to [1.2, 2.5].
            max_new_tokens: Maximum tokens to generate.
            normalize: Apply loudness normalization to the output audio.
            word_timestamps: Enable or disable word-level timestamps.
            language: ISO 639-1 language code for text normalization (e.g. "de").
        """
        changed = False
        if is_given(model) and model != self._opts.model:
            self._opts.model = model
            changed = True
        if is_given(voice_id) and voice_id != self._opts.voice_id:
            self._opts.voice_id = voice_id
            changed = True
        if is_given(cfg_scale) and cfg_scale != self._opts.cfg_scale:
            cfg_scale = clamp_cfg_scale(cfg_scale)
            self._opts.cfg_scale = cfg_scale
            changed = True
        if is_given(max_new_tokens) and max_new_tokens != self._opts.max_new_tokens:
            self._opts.max_new_tokens = max_new_tokens
            changed = True
        if is_given(normalize) and normalize != self._opts.normalize:
            self._opts.normalize = normalize
            changed = True
        if is_given(word_timestamps) and word_timestamps != self._opts.word_timestamps:
            self._opts.word_timestamps = word_timestamps
            changed = True
        if is_given(language):
            validated = _validate_language(language)
            if validated != self._opts.language:
                self._opts.language = validated
                changed = True
        if changed and self._current_connection:
            old_conn = self._current_connection
            old_conn.mark_non_current()
            self._current_connection = None
            try:
                loop = asyncio.get_running_loop()
                loop.create_task(old_conn.aclose())
            except RuntimeError:
                pass

    def synthesize(
        self,
        text: str,
        *,
        conn_options: APIConnectOptions = DEFAULT_API_CONNECT_OPTIONS,
    ) -> ChunkedStream:
        """Synthesize text to speech (non-streaming).

        Args:
            text: Text to synthesize.
            conn_options: Connection options.

        Returns:
            ChunkedStream that yields audio frames.
        """
        return ChunkedStream(tts=self, input_text=text, conn_options=conn_options)

    def stream(
        self,
        *,
        conn_options: APIConnectOptions = DEFAULT_API_CONNECT_OPTIONS,
    ) -> "SynthesizeStream":
        """Create a streaming TTS session.

        Args:
            conn_options: Connection options.

        Returns:
            SynthesizeStream for streaming text input.
        """
        return SynthesizeStream(tts=self, conn_options=conn_options)

    async def aclose(self) -> None:
        """Close the TTS instance and release resources."""
        if self._current_connection:
            await self._current_connection.aclose()
            self._current_connection = None


class ChunkedStream(tts.ChunkedStream):
    """Non-streaming TTS synthesis using WebSocket."""

    def __init__(
        self,
        *,
        tts: TTS,
        input_text: str,
        conn_options: APIConnectOptions,
    ) -> None:
        super().__init__(tts=tts, input_text=input_text, conn_options=conn_options)
        self._tts = tts
        self._opts = replace(tts._opts)

    async def _run(self, output_emitter: tts.AudioEmitter) -> None:
        context_id = utils.shortuuid()

        output_emitter.initialize(
            request_id=context_id,
            sample_rate=self._opts.sample_rate,
            num_channels=1,
            mime_type="audio/pcm",
            frame_size_ms=20,
        )

        connection = await self._tts._ensure_connection(
            timeout=self._conn_options.timeout
        )
        waiter: asyncio.Future[None] = asyncio.get_event_loop().create_future()
        ctx = connection.register_context(context_id, output_emitter, waiter)
        if ctx is None:
            # register_context rejected (connection closed) — waiter already
            # has the exception; await it so the caller sees it.
            try:
                await waiter
            finally:
                output_emitter.flush()
            return

        try:
            connection.send_content(
                _SynthesizeContent(context_id, self._input_text, flush=True)
            )
            await _wait_for_context_idle(
                ctx, waiter, idle_threshold=self._conn_options.timeout
            )
        except asyncio.CancelledError:
            connection.request_close_context(context_id, immediate=True)
            connection._cleanup_context(context_id)
            raise
        except asyncio.TimeoutError:
            connection.request_close_context(context_id, immediate=True)
            connection._cleanup_context(context_id)
            raise APITimeoutError() from None
        finally:
            output_emitter.flush()


class SynthesizeStream(tts.SynthesizeStream):
    """Streaming TTS synthesis over the shared /ws/tts/multi connection.

    Each stream gets its own context_id.  Text tokens are forwarded to
    the shared connection; audio arrives via the recv loop and is routed
    back by context_id.
    """

    def __init__(
        self,
        *,
        tts: TTS,
        conn_options: APIConnectOptions,
    ) -> None:
        super().__init__(tts=tts, conn_options=conn_options)
        self._tts = tts
        self._opts = replace(tts._opts)

    async def _run(self, output_emitter: tts.AudioEmitter) -> None:
        context_id = utils.shortuuid()
        output_emitter.initialize(
            request_id=context_id,
            sample_rate=self._opts.sample_rate,
            num_channels=1,
            mime_type="audio/pcm",
            stream=True,
        )
        output_emitter.start_segment(segment_id=context_id)

        connection = await self._tts._ensure_connection(
            timeout=self._conn_options.timeout
        )
        waiter: asyncio.Future[None] = asyncio.get_event_loop().create_future()
        ctx = connection.register_context(
            context_id, output_emitter, waiter, stream=self
        )
        if ctx is None:
            # Connection closed before register — waiter is already failed.
            try:
                await waiter
            finally:
                output_emitter.end_segment()
            return

        async def _input_task() -> None:
            async for data in self._input_ch:
                if isinstance(data, self._FlushSentinel):
                    connection.send_content(
                        _SynthesizeContent(context_id, "", flush=True)
                    )
                    continue
                if not data:
                    continue
                connection.send_content(_SynthesizeContent(context_id, data))
            # Input channel closed — flush + close context
            connection.send_content(_SynthesizeContent(context_id, "", flush=True))
            connection.request_close_context(context_id)

        input_t = asyncio.create_task(_input_task())

        def _on_input_done(t: asyncio.Task) -> None:
            # Without this, an exception in _input_task would be stored on
            # the task but never observed — _run would hang on `await waiter`
            # because no flush/close was sent to the server.
            if waiter.done():
                return
            exc = t.exception() if not t.cancelled() else None
            if exc is not None:
                waiter.set_exception(exc)

        input_t.add_done_callback(_on_input_done)

        try:
            await _wait_for_context_idle(
                ctx, waiter, idle_threshold=self._conn_options.timeout
            )
        except asyncio.CancelledError:
            # Barge-in / caller cancelled: tell the server to cancel
            # in-flight generation (immediate=True) instead of letting
            # it drain.  Without this the server keeps generating audio
            # for several seconds after the user has moved on.
            connection.request_close_context(context_id, immediate=True)
            connection._cleanup_context(context_id)
            raise
        except asyncio.TimeoutError:
            connection.request_close_context(context_id, immediate=True)
            connection._cleanup_context(context_id)
            raise APITimeoutError() from None
        finally:
            output_emitter.end_segment()
            await utils.aio.gracefully_cancel(input_t)
