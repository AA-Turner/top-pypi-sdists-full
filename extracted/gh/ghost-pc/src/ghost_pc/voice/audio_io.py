"""Audio I/O for voice control — mic capture and speaker playback.

Uses sounddevice with RawInputStream/RawOutputStream for zero-copy PCM handling.
Thread-safe bridging to asyncio via loop.call_soon_threadsafe().

Audio formats:
  Mic input:   16kHz, 16-bit signed, mono PCM (matches Gemini Live + OpenWakeWord)
  Speaker out:  24kHz, 16-bit signed, mono PCM (from Gemini Live)

Requires: pip install ghost-pc[voice]  (sounddevice>=0.5.5)
"""

from __future__ import annotations

import asyncio
import logging
import queue
from collections.abc import AsyncIterator

logger = logging.getLogger(__name__)

# Audio format constants
MIC_SAMPLE_RATE = 16000
SPEAKER_SAMPLE_RATE = 24000
CHANNELS = 1
DTYPE = "int16"
MIC_CHUNK_SIZE = 1280  # 80ms at 16kHz


async def mic_stream(
    sample_rate: int = MIC_SAMPLE_RATE,
    chunk_size: int = MIC_CHUNK_SIZE,
) -> AsyncIterator[bytes]:
    """Async generator yielding PCM audio chunks from the microphone.

    Each chunk is 80ms of 16kHz, 16-bit, mono PCM audio (1280 samples = 2560 bytes).

    Yields:
        bytes: Raw PCM audio data.

    Raises:
        ImportError: If sounddevice is not installed.
        RuntimeError: If no audio input device is available.
    """
    import sounddevice as sd

    # Verify input device exists
    try:
        sd.query_devices(kind="input")
    except sd.PortAudioError:
        raise RuntimeError("No audio input device found")

    audio_queue: asyncio.Queue[bytes] = asyncio.Queue()
    loop = asyncio.get_running_loop()

    def _callback(indata: bytes, frames: int, time_info: object, status: object) -> None:
        if status:
            logger.debug("Mic status: %s", status)
        loop.call_soon_threadsafe(audio_queue.put_nowait, bytes(indata))

    stream = sd.RawInputStream(
        samplerate=sample_rate,
        channels=CHANNELS,
        dtype=DTYPE,
        blocksize=chunk_size,
        callback=_callback,
    )

    with stream:
        logger.info("Microphone stream started (%dHz, %d-sample chunks)", sample_rate, chunk_size)
        while True:
            chunk = await audio_queue.get()
            yield chunk


class SpeakerPlayer:
    """Plays PCM audio through speakers with queue-based buffering.

    Audio chunks are queued and played sequentially. Thread-safe for
    receiving audio from the Gemini Live event loop.
    """

    def __init__(self, sample_rate: int = SPEAKER_SAMPLE_RATE) -> None:
        self._sample_rate = sample_rate
        self._audio_queue: queue.Queue[bytes] = queue.Queue()
        self._playing = False

    async def play(self, audio_data: bytes) -> None:
        """Queue audio data for playback.

        Args:
            audio_data: Raw PCM bytes (24kHz, 16-bit, mono).
        """
        self._audio_queue.put(audio_data)
        if not self._playing:
            self._playing = True
            loop = asyncio.get_running_loop()
            await loop.run_in_executor(None, self._drain_queue)

    def _drain_queue(self) -> None:
        """Play all queued audio chunks (runs in thread)."""
        try:
            import sounddevice as sd

            while not self._audio_queue.empty():
                try:
                    chunk = self._audio_queue.get_nowait()
                    # Convert bytes to int16 numpy array for playback
                    import numpy as np

                    audio = np.frombuffer(chunk, dtype=np.int16)
                    sd.play(audio, samplerate=self._sample_rate, blocking=True)
                except queue.Empty:
                    break
                except Exception as e:
                    logger.debug("Speaker playback error: %s", e)
        except ImportError:
            logger.debug("sounddevice not available for playback")
        finally:
            self._playing = False

    def stop(self) -> None:
        """Stop playback and clear the queue."""
        try:
            import sounddevice as sd

            sd.stop()
        except ImportError:
            pass
        # Clear remaining items
        while not self._audio_queue.empty():
            try:
                self._audio_queue.get_nowait()
            except queue.Empty:
                break
        self._playing = False
