"""Audio transcription using Gemini Flash.

Transcribes voice messages received from WhatsApp so the agent
can process them as text commands.
"""

from __future__ import annotations

import logging
import os

logger = logging.getLogger(__name__)


async def transcribe_audio(file_path: str) -> str | None:
    """Transcribe an audio file using Gemini Flash.

    Args:
        file_path: Path to the audio file (ogg/mp3/wav).

    Returns:
        Transcribed text, or None if transcription failed.
    """
    if not os.path.isfile(file_path):
        logger.error("Audio file not found: %s", file_path)
        return None

    try:
        from google import genai
        from google.genai import types

        client = genai.Client()

        with open(file_path, "rb") as f:
            audio_bytes = f.read()

        # Determine MIME type from extension
        ext = os.path.splitext(file_path)[1].lower()
        mime_map = {
            ".ogg": "audio/ogg",
            ".mp3": "audio/mpeg",
            ".wav": "audio/wav",
            ".m4a": "audio/mp4",
            ".opus": "audio/opus",
            ".webm": "audio/webm",
        }
        mime_type = mime_map.get(ext, "audio/ogg")

        response = await client.aio.models.generate_content(
            model="gemini-3-flash-preview",
            contents=[
                types.Content(
                    role="user",
                    parts=[
                        types.Part.from_bytes(data=audio_bytes, mime_type=mime_type),
                        types.Part(
                            text="Transcribe this audio message exactly. "
                            "Return only the transcription, nothing else."
                        ),
                    ],
                )
            ],
        )

        if response.text:
            logger.info("Transcribed audio (%d bytes): %s", len(audio_bytes), response.text[:100])
            return response.text.strip()

        logger.warning("Gemini returned empty transcription")
        return None

    except Exception as e:
        logger.error("Audio transcription failed: %s", e)
        return None
