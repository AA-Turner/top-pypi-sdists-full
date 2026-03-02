"""Voice message transcription using OpenAI Whisper API."""

import io
import logging
import os

log = logging.getLogger(__name__)


async def transcribe_voice(audio_bytes: bytes, mime_type: str = "audio/ogg") -> str | None:
    """Transcribe voice audio bytes using OpenAI Whisper API.

    Args:
        audio_bytes: Raw audio file bytes (typically OGG from Telegram)
        mime_type: MIME type of the audio (default: audio/ogg)

    Returns:
        Transcribed text, or None if transcription fails
    """
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        log.warning("OPENAI_API_KEY not set — skipping voice transcription")
        return None

    try:
        from openai import AsyncOpenAI

        client = AsyncOpenAI(api_key=api_key)

        # Map MIME type to file extension for the API
        ext_map = {
            "audio/ogg": "ogg",
            "audio/mpeg": "mp3",
            "audio/mp4": "m4a",
            "audio/wav": "wav",
            "audio/webm": "webm",
        }
        ext = ext_map.get(mime_type, "ogg")

        # Wrap bytes in a file-like object with a name attribute
        audio_file = io.BytesIO(audio_bytes)
        audio_file.name = f"voice.{ext}"

        transcription = await client.audio.transcriptions.create(
            model="whisper-1",
            file=audio_file,
        )

        text = transcription.text.strip()
        if text:
            log.info("Voice transcribed: %s chars", len(text))
            return text

        return None

    except ImportError:
        log.warning("openai package not installed — skipping voice transcription")
        return None
    except Exception as e:
        log.warning("Voice transcription failed: %s", e)
        return None
