"""Gemini Live session configuration for a host's realtime plugin.

The provider-facing ``google.genai`` types live in the provider layer; a host (the LiveKit voice
worker) passes plain values and gets back the plugin keyword arguments. Nothing here opens a
connection or holds a key.
"""

from __future__ import annotations

from typing import Any


def live_session_kwargs() -> dict[str, Any]:
    """Session resumption + sliding-window context compression (keeps a camera call past Gemini's
    2-minute audio+video session limit) and transcription of both sides (the chat saves the words;
    Gemini returns them only when asked)."""
    from google.genai import types

    return {
        "context_window_compression": types.ContextWindowCompressionConfig(
            sliding_window=types.SlidingWindow()
        ),
        "session_resumption": types.SessionResumptionConfig(),
        "input_audio_transcription": types.AudioTranscriptionConfig(),
        "output_audio_transcription": types.AudioTranscriptionConfig(),
    }
