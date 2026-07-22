"""Pipecat user-turn stop strategy backed by KugelAudio turn detection."""

from __future__ import annotations

from pipecat.audio.resamplers.soxr_stream_resampler import SOXRStreamAudioResampler
from pipecat.frames.frames import (
    Frame,
    InputAudioRawFrame,
    InterimTranscriptionFrame,
    TranscriptionFrame,
    VADUserStartedSpeakingFrame,
    VADUserStoppedSpeakingFrame,
)
from pipecat.turns.user_stop.base_user_turn_stop_strategy import (
    BaseUserTurnStopStrategy,
)

from kugelaudio.turn import TurnDecision, TurnDetector, TurnLanguage
from kugelaudio.turn._stream import AsyncTurnEndpoint
from kugelaudio.turn.errors import TurnAudioError, TurnStateError


class KugelTurnStopStrategy(BaseUserTurnStopStrategy):
    """Consume Pipecat audio, transcription, and VAD frames to stop user turns."""

    def __init__(
        self,
        detector: TurnDetector,
        *,
        language: TurnLanguage,
        vad_silence_ms: int = 200,
        action_delay_ms: int | None = None,
        timeout_ms: int = 10_000,
        poll_interval_ms: int = 50,
        pre_roll_ms: int = 500,
        enable_user_speaking_frames: bool = True,
    ) -> None:
        super().__init__(enable_user_speaking_frames=enable_user_speaking_frames)
        if vad_silence_ms < 0:
            raise TurnStateError(
                f"vad_silence_ms must be non-negative, got {vad_silence_ms}"
            )
        self._vad_silence_ms = vad_silence_ms
        self._resampler = SOXRStreamAudioResampler(quality="HQ")
        self._endpoint = AsyncTurnEndpoint(
            detector.create_session(
                language,
                action_delay_ms=action_delay_ms,
                timeout_ms=timeout_ms,
            ),
            on_end_turn=self._trigger_stop,
            poll_interval_ms=poll_interval_ms,
            pre_roll_ms=pre_roll_ms,
        )

    async def process_frame(self, frame: Frame) -> None:
        """Update turn state and leave subsequent Pipecat strategies runnable."""
        await super().process_frame(frame)
        if isinstance(frame, InputAudioRawFrame):
            await self._handle_audio(frame)
        elif isinstance(frame, VADUserStartedSpeakingFrame):
            self._endpoint.speech_started()
        elif isinstance(frame, VADUserStoppedSpeakingFrame):
            # RISK: Pipecat <=0.0.101 does not expose stop_secs on the VAD
            # frame. Keep this explicit constructor value aligned with VADParams.
            stop_secs = getattr(frame, "stop_secs", self._vad_silence_ms / 1000)
            self._endpoint.speech_stopped(
                initial_silence_ms=max(0, round(stop_secs * 1000))
            )
        elif isinstance(frame, InterimTranscriptionFrame):
            self._endpoint.update_interim_transcript(frame.text)
        elif isinstance(frame, TranscriptionFrame):
            self._endpoint.update_final_transcript(frame.text)

    async def reset(self) -> None:
        """Reset both Pipecat strategy and Kugel turn state."""
        await super().reset()
        await self._endpoint.reset()

    async def cleanup(self) -> None:
        """Cancel endpoint work when the Pipecat pipeline closes."""
        await self._endpoint.aclose()
        await super().cleanup()

    async def _handle_audio(self, frame: InputAudioRawFrame) -> None:
        if frame.num_channels != 1:
            raise TurnAudioError(
                f"Pipecat turn detection requires mono audio, got {frame.num_channels} channels"
            )
        try:
            pcm = await self._resampler.resample(frame.audio, frame.sample_rate, 16_000)
        except ValueError as exc:
            raise TurnAudioError(f"cannot resample Pipecat turn audio: {exc}") from exc
        if pcm:
            self._endpoint.push_pcm16(pcm, sample_rate=16_000)

    async def _trigger_stop(self, decision: TurnDecision) -> None:
        await self.trigger_user_turn_stopped()
