"""Voice controller — wake word detection + Gemini Live streaming.

State machine:
  IDLE → LISTENING → ACTIVE → IDLE

LISTENING: Microphone captures audio → feed to OpenWakeWord detector
ACTIVE: Wake word detected → open Gemini Live session → stream audio
IDLE: 30s silence or "that's all" → close session, back to listening

Integrates with:
  - VoiceSession (voice_agent.py): Gemini Live bidirectional audio
  - EchoGate (echo_gate.py): half-duplex mic muting during playback
  - SpeakerPlayer (audio_io.py): audio output through speakers

Requires: sounddevice, openwakeword
"""

from __future__ import annotations

import asyncio
import enum
import logging
from collections.abc import Callable
from typing import Any

logger = logging.getLogger(__name__)

# Audio settings
SAMPLE_RATE = 16000
CHANNELS = 1
CHUNK_SIZE = 1280  # 80ms at 16kHz
SILENCE_TIMEOUT = 30.0  # seconds of silence before returning to IDLE
WAKE_WORD = "hey_jarvis"


class VoiceState(enum.Enum):
    """Voice controller states."""

    IDLE = "idle"
    LISTENING = "listening"
    ACTIVE = "active"
    STOPPING = "stopping"


class VoiceController:
    """Manages wake word detection, voice session lifecycle, and audio routing.

    When a wake word is detected:
    1. Creates a VoiceSession (Gemini Live)
    2. Sets up echo gating (mute mic during agent speech)
    3. Streams mic audio to Gemini via the session
    4. Plays audio responses through speakers
    5. Returns to listening after silence timeout
    """

    def __init__(
        self,
        on_wake: Callable[[], Any] | None = None,
        on_audio_chunk: Callable[[bytes], Any] | None = None,
        on_silence_timeout: Callable[[], Any] | None = None,
        wake_word: str = WAKE_WORD,
    ) -> None:
        self._state = VoiceState.IDLE
        self._on_wake = on_wake
        self._on_audio_chunk = on_audio_chunk
        self._on_silence_timeout = on_silence_timeout
        self._wake_word = wake_word
        self._running = False
        self._wake_model: Any = None
        self._last_voice_time = 0.0

        # Voice session components (created on wake)
        self._voice_session: Any = None
        self._echo_gate: Any = None
        self._speaker: Any = None

    @property
    def state(self) -> VoiceState:
        return self._state

    async def start(self) -> None:
        """Start the voice controller (wake word detection loop)."""
        if self._running:
            return

        self._running = True
        self._state = VoiceState.LISTENING

        try:
            await self._run_detection_loop()
        except asyncio.CancelledError:
            pass
        finally:
            await self._close_voice_session()
            self._running = False
            self._state = VoiceState.IDLE

    async def stop(self) -> None:
        """Stop the voice controller."""
        self._running = False
        self._state = VoiceState.STOPPING
        await self._close_voice_session()

    def activate(self) -> None:
        """Manually activate voice mode (skip wake word detection)."""
        self._state = VoiceState.ACTIVE

    def deactivate(self) -> None:
        """Return to listening mode."""
        self._state = VoiceState.LISTENING

    async def _open_voice_session(self) -> None:
        """Create and start a VoiceSession with echo gating."""
        try:
            from ghost_pc.agent.voice_agent import VoiceSession, create_voice_agent
            from ghost_pc.voice.audio_io import SpeakerPlayer
            from ghost_pc.voice.echo_gate import EchoGate

            self._echo_gate = EchoGate()
            self._speaker = SpeakerPlayer()

            agent = create_voice_agent()
            self._voice_session = VoiceSession(
                agent=agent,
                on_audio_response=self._handle_audio_response,
                on_text_response=self._handle_text_response,
                on_speaking_start=lambda: self._echo_gate.set_speaking(True),
                on_speaking_end=lambda: self._echo_gate.set_speaking(False),
            )
            await self._voice_session.start()
            logger.info("Voice session opened")
        except Exception as e:
            logger.error("Failed to open voice session: %s", e)
            self._voice_session = None

    async def _close_voice_session(self) -> None:
        """Stop and clean up the voice session."""
        if self._voice_session:
            try:
                await self._voice_session.stop()
            except Exception:
                pass
            self._voice_session = None

        if self._speaker:
            self._speaker.stop()
            self._speaker = None

        self._echo_gate = None

    async def _handle_audio_response(self, audio_data: bytes) -> None:
        """Handle audio output from Gemini — play through speakers."""
        if self._speaker:
            await self._speaker.play(audio_data)

    async def _handle_text_response(self, text: str) -> None:
        """Handle text transcription from Gemini."""
        logger.debug("Voice transcription: %s", text[:100])

    async def _run_detection_loop(self) -> None:
        """Main loop: capture audio and detect wake word."""
        try:
            import sounddevice as sd
        except ImportError:
            logger.warning("sounddevice not installed — voice control unavailable")
            return

        try:
            from openwakeword.model import Model

            self._wake_model = Model(
                wakeword_models=[self._wake_word],
                inference_framework="onnx",
            )
        except ImportError:
            logger.warning("openwakeword not installed — wake word detection unavailable")
            return
        except Exception as e:
            logger.warning("Failed to load wake word model: %s", e)
            return

        logger.info("Voice controller started — listening for wake word '%s'", self._wake_word)

        # Audio callback runs in a separate thread
        audio_queue: asyncio.Queue[bytes] = asyncio.Queue()
        loop = asyncio.get_running_loop()

        def _audio_callback(
            indata: Any,
            frames: int,
            time_info: Any,
            status: Any,
        ) -> None:
            if status:
                logger.debug("Audio status: %s", status)
            loop.call_soon_threadsafe(audio_queue.put_nowait, bytes(indata))

        stream = sd.RawInputStream(
            samplerate=SAMPLE_RATE,
            channels=CHANNELS,
            dtype="int16",
            blocksize=CHUNK_SIZE,
            callback=_audio_callback,
        )

        with stream:
            import time

            while self._running:
                try:
                    chunk = await asyncio.wait_for(audio_queue.get(), timeout=1.0)
                except TimeoutError:
                    continue

                if self._state == VoiceState.LISTENING:
                    # Feed to wake word detector
                    await self._check_wake_word(chunk)

                elif self._state == VoiceState.ACTIVE:
                    self._last_voice_time = time.monotonic()

                    # Echo gate: only forward mic audio when agent isn't speaking
                    if self._echo_gate and self._echo_gate.should_forward():
                        # Stream to voice session
                        if self._voice_session:
                            await self._voice_session.send_audio(chunk)

                        # Also forward to legacy callback if set
                        if self._on_audio_chunk:
                            try:
                                result = self._on_audio_chunk(chunk)
                                if asyncio.iscoroutine(result):
                                    await result
                            except Exception as e:
                                logger.error("Audio chunk callback error: %s", e)
                    elif not self._echo_gate:
                        # No echo gate — forward everything (legacy behavior)
                        if self._on_audio_chunk:
                            try:
                                result = self._on_audio_chunk(chunk)
                                if asyncio.iscoroutine(result):
                                    await result
                            except Exception as e:
                                logger.error("Audio chunk callback error: %s", e)

                    # Check silence timeout
                    if time.monotonic() - self._last_voice_time > SILENCE_TIMEOUT:
                        logger.info("Silence timeout — returning to listening")
                        self._state = VoiceState.LISTENING
                        await self._close_voice_session()
                        if self._on_silence_timeout:
                            try:
                                result = self._on_silence_timeout()
                                if asyncio.iscoroutine(result):
                                    await result
                            except Exception as e:
                                logger.error("Silence timeout callback error: %s", e)

    async def _check_wake_word(self, audio_chunk: bytes) -> None:
        """Feed audio to wake word model and check for detection."""
        if self._wake_model is None:
            return

        import numpy as np

        # Convert bytes to numpy int16 array
        audio_array = np.frombuffer(audio_chunk, dtype=np.int16)

        # Feed to model
        prediction = self._wake_model.predict(audio_array)

        # Check all wake words
        for key, score in prediction.items():
            if score > 0.5:
                logger.info("Wake word detected: %s (score=%.2f)", key, score)
                self._state = VoiceState.ACTIVE

                # Open Gemini Live session
                await self._open_voice_session()

                if self._on_wake:
                    try:
                        result = self._on_wake()
                        if asyncio.iscoroutine(result):
                            await result
                    except Exception as e:
                        logger.error("Wake callback error: %s", e)
                break
