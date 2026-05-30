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

"""KugelAudio TTS service for Pipecat.

Internally delegates to the core KugelAudio Python SDK for WebSocket
connection management, pooling, keepalive, and streaming. This avoids
duplicating low-level transport logic and ensures the PipeCat integration
inherits all SDK-level performance optimisations (connection reuse,
pre-warming, language-skip, etc.).
"""

from __future__ import annotations

import asyncio
import inspect
import logging
import os
import time
import uuid
from dataclasses import dataclass
from functools import lru_cache
from typing import Any, AsyncGenerator, Optional

from pipecat.frames.frames import (
    ErrorFrame,
    Frame,
    TTSAudioRawFrame,
    TTSStartedFrame,
    TTSStoppedFrame,
)
from pipecat.services.tts_service import TTSService

from kugelaudio import KugelAudio
from kugelaudio.client import _parse_api_key, _resolve_region_url
from kugelaudio.exceptions import (
    ConnectionError as KugelAudioConnectionError,
    ValidationError,
)
from kugelaudio.streaming import MultiContextSession

from .models import (
    DEFAULT_CFG_SCALE,
    DEFAULT_MAX_NEW_TOKENS,
    DEFAULT_MODEL,
    DEFAULT_SAMPLE_RATE,
    SUPPORTED_SAMPLE_RATES,
    TTSModels,
)

logger = logging.getLogger("kugelaudio.pipecat")


# Pipecat 1.x introduced TTSSettings + AIService.start().validate_complete(),
# which logs ERROR for any TTSSettings field still set to the NOT_GIVEN
# sentinel. Subclasses are expected to pass an initialized TTSSettings via
# super().__init__(settings=...). On Pipecat 0.x this module/class doesn't
# exist; we fall back to the old kwarg-only path. See
# pipecat/services/settings.py:TTSSettings.validate_complete.
try:  # noqa: SIM105 — explicit branch is clearer than contextlib.suppress
    from pipecat.services.settings import TTSSettings as _PipecatTTSSettings
except ImportError:  # Pipecat < 1.0
    _PipecatTTSSettings = None  # type: ignore[assignment]


@lru_cache(maxsize=None)
def _frame_supports_context_id(frame_type: type[Frame]) -> bool:
    """Return whether the installed Pipecat frame accepts context_id."""
    try:
        return "context_id" in inspect.signature(frame_type).parameters
    except (TypeError, ValueError):
        return False


def _tts_started_frame(context_id: Optional[str]) -> TTSStartedFrame:
    if context_id and _frame_supports_context_id(TTSStartedFrame):
        return TTSStartedFrame(context_id=context_id)
    return TTSStartedFrame()


def _tts_stopped_frame(context_id: Optional[str]) -> TTSStoppedFrame:
    if context_id and _frame_supports_context_id(TTSStoppedFrame):
        return TTSStoppedFrame(context_id=context_id)
    return TTSStoppedFrame()


def _tts_audio_frame(
    *,
    audio: bytes,
    sample_rate: int,
    num_channels: int,
    context_id: Optional[str],
) -> TTSAudioRawFrame:
    kwargs: dict[str, Any] = {
        "audio": audio,
        "sample_rate": sample_rate,
        "num_channels": num_channels,
    }
    if context_id and _frame_supports_context_id(TTSAudioRawFrame):
        kwargs["context_id"] = context_id
    return TTSAudioRawFrame(**kwargs)


def _is_ws_connection_closed_error(exc: BaseException) -> bool:
    """Return whether an exception is a raw websockets connection close."""
    return "ConnectionClosed" in type(exc).__name__


@dataclass
class _TTSOptions:
    model: TTSModels | str
    voice_id: int
    sample_rate: int
    cfg_scale: float
    max_new_tokens: int
    api_key: str
    base_url: str
    language: str | None = None
    normalize: bool = True


class KugelAudioTTSService(TTSService):
    """KugelAudio Text-to-Speech service for Pipecat.

    Integrates KugelAudio's TTS API with Pipecat's pipeline framework,
    providing high-quality voice synthesis via WebSocket streaming.

    Internally uses the core KugelAudio Python SDK for all WebSocket
    transport, connection pooling, and streaming logic.

    Example:
        ```python
        from kugelaudio.pipecat import KugelAudioTTSService

        tts = KugelAudioTTSService(
            api_key="your-api-key",
            voice_id=280,
            model="kugel-1-turbo",
            sample_rate=24000,
        )

        # Use in a Pipecat pipeline
        pipeline = Pipeline([..., tts, ...])
        ```
    """

    def __init__(
        self,
        *,
        api_key: Optional[str] = None,
        model: TTSModels | str = DEFAULT_MODEL,
        voice_id: int,
        sample_rate: int = DEFAULT_SAMPLE_RATE,
        cfg_scale: float = DEFAULT_CFG_SCALE,
        max_new_tokens: int = DEFAULT_MAX_NEW_TOKENS,
        language: Optional[str] = None,
        normalize: bool = True,
        region: Optional[str] = None,
        base_url: Optional[str] = None,
        **kwargs: Any,
    ) -> None:
        """Create a new KugelAudio TTS service for Pipecat.

        Args:
            api_key: KugelAudio API key. If not provided, reads from
                KUGELAUDIO_API_KEY environment variable. Prefix with
                ``"eu-"`` to select the direct EU endpoint; the prefix is
                stripped before auth.
            model: TTS model to use. "kugel-1-turbo" (fast) or
                "kugel-1" (premium).
            voice_id: Voice ID to use for synthesis.
            sample_rate: Output sample rate in Hz. Supported rates: 24000 (native),
                22050, 16000, 8000. Lower rates use server-side resampling.
            cfg_scale: CFG scale for generation quality. Defaults to 2.0.
            max_new_tokens: Maximum tokens to generate. Defaults to 2048.
            language: ISO 639-1 language code (e.g., 'en', 'de'). Setting this
                skips server-side auto-detection and saves ~60-150ms per request.
            normalize: Apply text normalization. Defaults to True.
            region: API endpoint region. Use ``"eu"`` for the direct EU endpoint.
                Overrides any prefix detected from the API key. Ignored when
                *base_url* is set.
            base_url: API base URL. Overrides region selection entirely. Defaults
                to the default geo-routed API endpoint if no region is specified.
            **kwargs: Additional arguments passed to Pipecat TTSService.
        """
        # On Pipecat 1.x the parent expects an initialized TTSSettings; if we
        # leave model / voice / language as NOT_GIVEN, AIService.start() logs
        # an ERROR per field. Build it from our typed wrapper params here so
        # the user doesn't have to construct one themselves. On Pipecat 0.x
        # _PipecatTTSSettings is None and we fall back to the legacy path.
        super_kwargs: dict[str, Any] = dict(kwargs)
        if _PipecatTTSSettings is not None and "settings" not in super_kwargs:
            # Drop a stray ``voice=`` kwarg if the caller passed both ways —
            # we already cover voice via the dedicated ``voice_id`` param,
            # and Pipecat 1.x routes voice through TTSSettings, not kwargs.
            super_kwargs.pop("voice", None)
            super_kwargs["settings"] = _PipecatTTSSettings(
                model=str(model) if model else None,
                voice=str(voice_id) if voice_id is not None else None,
                language=language,
            )
        super().__init__(sample_rate=sample_rate, **super_kwargs)

        kugelaudio_api_key = api_key or os.environ.get("KUGELAUDIO_API_KEY")
        if not kugelaudio_api_key:
            raise ValueError(
                "KUGELAUDIO_API_KEY must be set or api_key must be provided"
            )

        if sample_rate not in SUPPORTED_SAMPLE_RATES:
            raise ValueError(
                f"Unsupported sample rate: {sample_rate}. "
                f"Supported rates: {SUPPORTED_SAMPLE_RATES}"
            )

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
            language=language,
            normalize=normalize,
            api_key=clean_key,
            base_url=resolved_url,
        )

        self._client = KugelAudio(
            api_key=clean_key,
            tts_url=resolved_url,
        )
        self._multi_session: Optional[MultiContextSession] = None
        self._multi_session_lock = asyncio.Lock()
        self._multi_session_needs_reset = False
        # Pipecat 0.x calls run_tts(text) with no context_id, so the wrapper
        # owns context identity. We reuse ONE stable context for the whole WS
        # session instead of minting a fresh one per turn: a per-turn context
        # is never closed by this wrapper and the server hard-caps a session
        # at 5 concurrent contexts (the 6th create raises and tears the WS
        # down ~30-40s into a call). Reusing one context also lets the server
        # keep its KV cache warm across turns, lowering follow-up TTFA.
        # ``_session_context_needs_reset`` rotates the context after a turn
        # that didn't finish cleanly (barge-in cancel / mid-stream error) so
        # its un-drained tail can't bleed into the next turn.
        self._session_context_id: Optional[str] = None
        self._session_context_needs_reset = False
        # Pipecat 1.x (AudioContext API) calls run_tts(text, context_id) with a
        # FRESH context_id per turn and owns its identity. Unlike the wrapper-
        # owned 0.x path above, we must close each of those server-side contexts
        # when its turn ends — otherwise every turn leaks a /ws/tts/multi context
        # against the per-session cap and the call drops mid-conversation
        # (KUG-1087). We track the caller-supplied ids here and close them from
        # the Pipecat turn/audio completion hooks below.
        self._caller_contexts: set[str] = set()
        # Server-side contexts already create_context'd before run_tts(). Pipecat
        # 1.x mints the turn id on LLMFullResponseStartFrame — we provision
        # during on_turn_context_created so the ~30-45ms WS round-trip overlaps
        # LLM time-to-first-token instead of sitting on the TTFA critical path.
        self._provisioned_contexts: set[str] = set()
        self._closed = False

    def _create_multi_session(self) -> MultiContextSession:
        return self._client.tts.multi_context_session(
            default_voice_id=self._opts.voice_id,
            model_id=self._opts.model,
            sample_rate=self._opts.sample_rate,
            cfg_scale=self._opts.cfg_scale,
            max_new_tokens=self._opts.max_new_tokens,
            normalize=self._opts.normalize,
            language=self._opts.language,
        )

    async def _get_multi_session(self) -> MultiContextSession:
        if self._multi_session_needs_reset:
            await self._close_multi_session()
            self._multi_session_needs_reset = False
        # An idle WS may have been silently dropped by an upstream proxy / NAT
        # between turns of a voice conversation. Detect that here so we don't
        # ride a corpse forever; without this check, every subsequent run_tts
        # raises ConnectionClosedError("no close frame received or sent").
        if self._multi_session is not None and not self._multi_session.is_alive:
            logger.info(
                "KugelAudio multi-context session WS is dead; reconnecting"
            )
            await self._close_multi_session()
        if self._multi_session is None:
            session = self._create_multi_session()
            await session.connect()
            self._multi_session = session
        return self._multi_session

    async def _close_multi_session(self) -> None:
        session = self._multi_session
        self._multi_session = None
        self._multi_session_needs_reset = False
        # The reused context lived on this WS; a fresh connection starts with
        # no server-side contexts, so forget our id and mint a new one lazily.
        self._session_context_id = None
        self._session_context_needs_reset = False
        # Closing the WS frees every server-side context with it, so just drop
        # our caller-context bookkeeping rather than closing them one by one.
        self._caller_contexts.clear()
        self._provisioned_contexts.clear()
        if session is not None:
            await session.close()

    async def _resolve_turn_context_id(
        self, session: MultiContextSession, caller_context_id: Optional[str]
    ) -> str:
        """Pick the context_id for this turn.

        When the caller supplies one (Pipecat 1.x AudioContext API), honour it
        verbatim — the caller owns context creation and teardown. Otherwise use
        the wrapper-owned stable session context, rotating it first if the
        previous turn left it dirty (see ``_session_context_needs_reset``).
        """
        if caller_context_id:
            return caller_context_id

        if self._session_context_needs_reset and self._session_context_id:
            old = self._session_context_id
            self._session_context_id = None
            try:
                async for _ in session.close_context(old):
                    pass
            except Exception:
                # KEEP-JUSTIFIED: best-effort release of an interrupted/failed
                # context. If the WS is already gone the upcoming send() will
                # surface that and trigger the normal reconnect path; there is
                # no correctness value in propagating a cleanup failure here.
                logger.debug(
                    "Failed to close rotated context %s", old, exc_info=True
                )
        self._session_context_needs_reset = False

        if self._session_context_id is None:
            self._session_context_id = f"kugelaudio-{uuid.uuid4()}"
        return self._session_context_id

    async def _close_caller_context(self, context_id: Optional[str]) -> None:
        """Close a single caller-supplied (Pipecat 1.x) server-side context.

        Idempotent and best-effort: the SDK's ``close_context`` is a no-op for
        an unknown/already-closed id, and a dead WS is handled by the existing
        reconnect path on the next ``run_tts``.
        """
        if not context_id:
            return
        async with self._multi_session_lock:
            self._caller_contexts.discard(context_id)
            self._provisioned_contexts.discard(context_id)
            session = self._multi_session
            if session is None:
                return
            try:
                # immediate=True: the turn is over, free the slot now and don't
                # drain-then-discard a tail (the audio already played).
                async for _ in session.close_context(context_id, immediate=True):
                    pass
            except Exception:
                # KEEP-JUSTIFIED: best-effort server-side context release on turn
                # end. If the WS is already gone the next run_tts surfaces it via
                # the reconnect path, and the server's inactivity reaper is the
                # backstop. No correctness value in propagating a cleanup failure.
                logger.debug(
                    "Failed to close caller context %s", context_id, exc_info=True
                )

    async def _provision_caller_context(self, context_id: str) -> None:
        """Eagerly create a Pipecat 1.x turn context on the multi WS session.

        Called from ``on_turn_context_created`` (fires on LLMFullResponseStartFrame,
        before the first ``run_tts`` chunk) so the create_context round-trip
        overlaps LLM latency instead of adding to measured TTFA.
        """
        if not context_id or context_id in self._provisioned_contexts:
            return
        try:
            async with self._multi_session_lock:
                session = await self._get_multi_session()
                await session.create_context(context_id)
            self._provisioned_contexts.add(context_id)
            logger.debug("Pre-provisioned KugelAudio context %s", context_id)
        except Exception:
            # KEEP-JUSTIFIED: best-effort prefetch — run_tts still creates the
            # context lazily on send() if this fails.
            logger.warning(
                "Failed to pre-provision context %s; will retry on send",
                context_id,
                exc_info=True,
            )

    async def on_turn_context_created(self, context_id: str) -> None:
        """Pipecat 1.x: a new turn opened a new context_id.

        A new turn means every *previous* turn's context is finished, so close
        any still-open caller contexts (covers Pipecat builds that don't emit
        ``on_audio_context_completed``), then track this turn's id.
        """
        parent = getattr(super(), "on_turn_context_created", None)
        if parent is not None:
            await parent(context_id)
        for stale in list(self._caller_contexts):
            if stale != context_id:
                await self._close_caller_context(stale)
        if context_id:
            self._caller_contexts.add(context_id)
        await self._provision_caller_context(context_id)

    async def on_audio_context_completed(self, context_id: str) -> None:
        """Pipecat 1.x: a turn's audio finished playing — close its server-side
        context so it stops counting against the per-session cap."""
        parent = getattr(super(), "on_audio_context_completed", None)
        if parent is not None:
            await parent(context_id)
        await self._close_caller_context(context_id)

    async def _close_multi_session_locked(self) -> None:
        async with self._multi_session_lock:
            await self._close_multi_session()

    async def _invoke_super_set_voice(self, voice: str) -> None:
        """Call Pipecat's set_voice, awaiting when the installed version is async."""
        result = super().set_voice(voice)
        if inspect.isawaitable(result):
            await result

    def can_generate_metrics(self) -> bool:
        """Check if this service can generate processing metrics.

        Returns:
            True, as KugelAudio service supports metrics generation.
        """
        return True

    def prewarm(self) -> None:
        """Pre-establish the WebSocket connection to reduce TTFB on first synthesis.

        Call this during pipeline setup to eagerly establish the connection,
        eliminating ~100-220ms of handshake latency from the first request.

        Example:
            ```python
            tts = KugelAudioTTSService(api_key="your-api-key", language="en")
            tts.prewarm()
            ```
        """
        try:
            loop = asyncio.get_running_loop()
        except RuntimeError:
            logger.warning("prewarm() called outside event loop, skipping")
            return

        async def _do_prewarm() -> None:
            try:
                async with self._multi_session_lock:
                    await self._get_multi_session()
                logger.info("KugelAudio PipeCat TTS connection pre-warmed")
            except Exception:
                logger.warning(
                    "Failed to prewarm KugelAudio connection, "
                    "will retry on first synthesis",
                    exc_info=True,
                )

        loop.create_task(_do_prewarm())

    async def set_model(self, model: str) -> None:
        """Set the TTS model.

        Closes any existing connection since the model is part of the
        WebSocket URL routing.

        Args:
            model: The model identifier to use.
        """
        if model != self._opts.model:
            async with self._multi_session_lock:
                await self._close_multi_session()
        self._opts.model = model
        await super().set_model(model)

    async def set_voice(self, voice: str) -> None:
        """Set the voice ID.

        Closes the cached persistent multi-context WebSocket session before
        returning so the next ``run_tts`` opens a connection with the new voice.

        Args:
            voice: The voice identifier (integer as string).
        """
        previous_voice_id = self._opts.voice_id
        self._opts.voice_id = int(voice) if voice else None
        if self._opts.voice_id != previous_voice_id:
            async with self._multi_session_lock:
                await self._close_multi_session()
        await self._invoke_super_set_voice(voice)

    async def cleanup(self) -> None:
        """Clean up resources when the service is stopped."""
        self._closed = True
        async with self._multi_session_lock:
            await self._close_multi_session()
        self._client.close()

    async def run_tts(
        self, text: str, context_id: Optional[str] = None
    ) -> AsyncGenerator[Frame, None]:
        """Synthesize text to speech via the core KugelAudio SDK.

        Delegates to ``client.tts.multi_context_session()`` so Pipecat context
        IDs map onto KugelAudio's ``/ws/tts/multi`` endpoint.

        Args:
            text: The text to synthesize into speech.
            context_id: Pipecat TTS context ID. Pipecat 0.x calls this method
                with only ``text``; Pipecat 1.x passes this second argument for
                context tracking.

        Yields:
            Frame: TTSStartedFrame, TTSAudioRawFrame chunks, and TTSStoppedFrame.
        """
        logger.debug(f"Generating TTS [{text}]")
        # Pipecat 1.x supplies a per-turn context_id; record it so the turn/audio
        # completion hooks can close the server-side context (KUG-1087). The 0.x
        # path (context_id is None) is handled by the wrapper-owned stable
        # context and must not be tracked here.
        if context_id is not None:
            self._caller_contexts.add(context_id)
        error_frame: Optional[ErrorFrame] = None
        completed_cleanly = False

        await self.start_ttfb_metrics()
        await self.start_tts_usage_metrics(text)
        yield _tts_started_frame(context_id)

        try:
            # Try once, then retry once on a connection drop. The retry path
            # exists because a NAT/proxy can quietly drop the WS during the
            # user's think-time between turns, and we'd rather give the
            # conversation one transparent reconnect than a hard error frame.
            for attempt in (1, 2):
                first_chunk = True
                yielded_audio = False
                try:
                    async with self._multi_session_lock:
                        session = await self._get_multi_session()
                        effective_context_id = await self._resolve_turn_context_id(
                            session, context_id
                        )
                        t0 = time.perf_counter()
                        async for item in session.send(
                            effective_context_id,
                            text,
                            flush=True,
                            chunk_complete_idle_timeout=0.0,
                        ):
                            if first_chunk:
                                ttfa_ms = (time.perf_counter() - t0) * 1000
                                logger.info(f"KugelAudio TTFA: {ttfa_ms:.0f}ms")
                                first_chunk = False
                            await self.stop_ttfb_metrics()
                            yielded_audio = True
                            yield _tts_audio_frame(
                                audio=item.audio,
                                sample_rate=self._opts.sample_rate,
                                num_channels=1,
                                context_id=context_id,
                            )
                    error_frame = None
                    completed_cleanly = True
                    break
                except Exception as e:
                    # WS is dead. If nothing was streamed yet on this attempt
                    # and we have a retry budget, drop the cached session and
                    # try once more with a fresh connection. After that, give
                    # up loudly.
                    if isinstance(
                        e, KugelAudioConnectionError
                    ) or _is_ws_connection_closed_error(e):
                        self._multi_session_needs_reset = True
                        if attempt == 1 and not yielded_audio:
                            logger.warning(
                                "KugelAudio WS dropped; reconnecting and retrying once"
                            )
                            continue
                        logger.error(f"TTS error: {e}")
                        error_frame = ErrorFrame(error=f"KugelAudio error: {e}")
                        break

                    logger.error(f"TTS error: {e}")
                    error_frame = ErrorFrame(error=f"KugelAudio error: {e}")
                    break
        finally:
            # A turn that didn't finish cleanly — barge-in cancellation
            # (CancelledError unwinds through here) or a mid-stream error —
            # may have left un-drained audio on our reused context. Mark it so
            # the next turn rotates to a fresh context and that tail can't
            # bleed into the next utterance. Only applies to the wrapper-owned
            # context; a caller-supplied context_id is the caller's to manage.
            if not completed_cleanly and context_id is None:
                self._session_context_needs_reset = True

        await self.stop_ttfb_metrics()
        logger.debug(f"Finished TTS [{text}]")
        if error_frame is not None:
            yield error_frame
        yield _tts_stopped_frame(context_id)
