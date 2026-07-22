"""Native LiveKit Agents bridge for KugelAudio semantic turn detection."""

from __future__ import annotations

import asyncio
from collections.abc import AsyncIterable, AsyncIterator, Callable
import inspect
import logging
from typing import Protocol, cast, runtime_checkable

from livekit import rtc
from livekit.agents import (
    Agent,
    ModelSettings,
    UserInputTranscribedEvent,
    UserStateChangedEvent,
    stt,
)

from kugelaudio.turn import TurnDecision, TurnDetector, TurnLanguage
from kugelaudio.turn._stream import AsyncTurnEndpoint
from kugelaudio.turn.errors import TurnAudioError, TurnStateError

logger = logging.getLogger("kugelaudio.livekit")


@runtime_checkable
class _LiveKitSession(Protocol):
    def on(self, event: str, callback: Callable[[object], None]) -> object: ...

    def off(self, event: str, callback: Callable[[object], None]) -> object: ...

    def commit_user_turn(self) -> object: ...


class KugelTurnBridge:
    """Bind one LiveKit Agent session to a shared Kugel turn detector."""

    def __init__(
        self,
        detector: TurnDetector,
        *,
        language: TurnLanguage,
        on_decision: Callable[[TurnDecision], None] | None = None,
        vad_silence_ms: int = 200,
        action_delay_ms: int | None = None,
        timeout_ms: int = 10_000,
        poll_interval_ms: int = 50,
        pre_roll_ms: int = 500,
    ) -> None:
        if vad_silence_ms < 0:
            raise TurnStateError(
                f"vad_silence_ms must be non-negative, got {vad_silence_ms}"
            )
        self._session: _LiveKitSession | None = None
        self._vad_silence_ms = vad_silence_ms
        self._resampler: rtc.AudioResampler | None = None
        self._input_rate: int | None = None
        self._closed = False
        self._commit_futures: set[asyncio.Future[object]] = set()
        self._commit_failure: BaseException | None = None
        self._endpoint = AsyncTurnEndpoint(
            detector.create_session(
                language,
                action_delay_ms=action_delay_ms,
                timeout_ms=timeout_ms,
            ),
            on_end_turn=self._commit_user_turn,
            on_decision=on_decision,
            poll_interval_ms=poll_interval_ms,
            pre_roll_ms=pre_roll_ms,
        )

    def attach(self, session: object) -> None:
        """Register transcript and VAD listeners on exactly one AgentSession."""
        if self._closed:
            raise TurnStateError("KugelTurnBridge is closed and cannot be reattached")
        if not isinstance(session, _LiveKitSession):
            raise TurnStateError(
                "session does not implement the LiveKit AgentSession API"
            )
        typed_session = cast(_LiveKitSession, session)
        if self._session is typed_session:
            return
        if self._session is not None:
            raise TurnStateError(
                "KugelTurnBridge is already attached to another session"
            )
        self._session = typed_session
        typed_session.on(
            "user_input_transcribed",
            cast(Callable[[object], None], self._on_transcript),
        )
        typed_session.on(
            "user_state_changed", cast(Callable[[object], None], self._on_user_state)
        )

    async def stt_node(
        self,
        agent: Agent,
        audio: AsyncIterable[rtc.AudioFrame],
        model_settings: ModelSettings,
    ) -> AsyncIterator[stt.SpeechEvent]:
        """Tee raw user audio into KugelTurn while preserving LiveKit's STT node."""
        self.attach(agent.session)

        async def tee_audio() -> AsyncIterator[rtc.AudioFrame]:
            async for frame in audio:
                self._push_audio_frame(frame)
                yield frame

        async for event in Agent.default.stt_node(agent, tee_audio(), model_settings):
            yield event

    async def aclose(self) -> None:
        """Detach event listeners and cancel pending endpoint work."""
        session = self._session
        if session is not None:
            session.off(
                "user_input_transcribed",
                cast(Callable[[object], None], self._on_transcript),
            )
            session.off(
                "user_state_changed",
                cast(Callable[[object], None], self._on_user_state),
            )
        self._session = None
        await self._endpoint.aclose()
        try:
            if self._commit_futures:
                await asyncio.gather(*self._commit_futures)
        except Exception as exc:
            raise TurnStateError("LiveKit user-turn commit failed") from exc
        finally:
            self._closed = True
        self._raise_commit_failure()

    def _push_audio_frame(self, frame: rtc.AudioFrame) -> None:
        self._raise_commit_failure()
        if frame.num_channels != 1:
            raise TurnAudioError(
                f"LiveKit turn detection requires mono audio, got {frame.num_channels} channels"
            )
        if frame.sample_rate == 16_000:
            self._endpoint.push_pcm16(
                frame.data.cast("B").tobytes(), sample_rate=16_000
            )
            return
        if self._resampler is None:
            self._input_rate = frame.sample_rate
            self._resampler = rtc.AudioResampler(
                input_rate=frame.sample_rate,
                output_rate=16_000,
                num_channels=1,
                quality=rtc.AudioResamplerQuality.HIGH,
            )
        elif frame.sample_rate != self._input_rate:
            raise TurnAudioError(
                "LiveKit input sample rate changed during a session: "
                f"{self._input_rate} -> {frame.sample_rate}"
            )
        for output in self._resampler.push(frame):
            self._endpoint.push_pcm16(
                output.data.cast("B").tobytes(), sample_rate=16_000
            )

    def _on_transcript(self, event: UserInputTranscribedEvent) -> None:
        self._raise_commit_failure()
        if event.is_final:
            self._endpoint.update_final_transcript(event.transcript)
        else:
            self._endpoint.update_interim_transcript(event.transcript)

    def _on_user_state(self, event: UserStateChangedEvent) -> None:
        self._raise_commit_failure()
        if event.new_state == "speaking":
            self._endpoint.speech_started()
        elif event.new_state == "listening" and self._endpoint.active:
            self._endpoint.speech_stopped(initial_silence_ms=self._vad_silence_ms)

    async def _commit_user_turn(self, decision: TurnDecision) -> None:
        session = self._session
        if session is None:
            raise TurnStateError("LiveKit session detached before turn commit")
        result = session.commit_user_turn()
        # LiveKit 1.3 returns None; newer releases return an awaitable transcript.
        # RISK: this compatibility branch is version-sensitive and must remain
        # covered against both supported LiveKit API generations.
        if inspect.isawaitable(result):
            future = asyncio.ensure_future(result)
            self._commit_futures.add(future)
            future.add_done_callback(self._commit_done)

    def _commit_done(self, future: asyncio.Future[object]) -> None:
        self._commit_futures.discard(future)
        if future.cancelled():
            return
        failure = future.exception()
        if failure is not None:
            self._commit_failure = failure
            logger.error(
                "LiveKit user-turn commit failed",
                exc_info=(type(failure), failure, failure.__traceback__),
            )

    def _raise_commit_failure(self) -> None:
        if self._commit_failure is not None:
            raise TurnStateError(
                "LiveKit user-turn commit failed"
            ) from self._commit_failure
