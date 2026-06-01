"""Voice processing — whisper.cpp STT and piper TTS via subprocess."""

from __future__ import annotations

import asyncio
import logging
import tempfile
from pathlib import Path

log = logging.getLogger("yantrik.voice")


class VoiceProcessor:
    """Handles speech-to-text (whisper.cpp) and text-to-speech (piper)."""

    def __init__(
        self,
        whisper_model: str = "/opt/models/whisper-tiny-en.bin",
        piper_model: str = "/opt/models/piper-lessac-medium.onnx",
        whisper_threads: int = 2,
    ):
        self.whisper_model = whisper_model
        self.piper_model = piper_model
        self.whisper_threads = whisper_threads

    async def transcribe(self, audio_path: str) -> str:
        """Transcribe audio file to text using whisper.cpp."""
        wav_path = audio_path

        # Convert to WAV if not already (browser sends webm/opus)
        if not audio_path.endswith(".wav"):
            wav_path = audio_path + ".wav"
            proc = await asyncio.create_subprocess_exec(
                "ffmpeg", "-i", audio_path, "-ar", "16000", "-ac", "1",
                "-sample_fmt", "s16", wav_path, "-y",
                stdout=asyncio.subprocess.DEVNULL,
                stderr=asyncio.subprocess.DEVNULL,
            )
            await proc.wait()
            if proc.returncode != 0:
                raise RuntimeError("ffmpeg conversion failed")

        proc = await asyncio.create_subprocess_exec(
            "whisper-cli",
            "-m", self.whisper_model,
            "-f", wav_path,
            "--no-timestamps",
            "-t", str(self.whisper_threads),
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.DEVNULL,
        )
        stdout, _ = await proc.communicate()
        if proc.returncode != 0:
            raise RuntimeError("whisper-cli failed")

        text = stdout.decode().strip()
        log.info("Transcribed: %s", text[:80])
        return text

    async def synthesize(self, text: str) -> str:
        """Synthesize text to speech using piper. Returns path to WAV file."""
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as f:
            out_path = f.name

        proc = await asyncio.create_subprocess_exec(
            "piper",
            "-m", self.piper_model,
            "-f", out_path,
            stdin=asyncio.subprocess.PIPE,
            stdout=asyncio.subprocess.DEVNULL,
            stderr=asyncio.subprocess.DEVNULL,
        )
        await proc.communicate(input=text.encode())
        if proc.returncode != 0:
            raise RuntimeError("piper TTS failed")

        log.info("Synthesized %d chars to %s", len(text), out_path)
        return out_path
