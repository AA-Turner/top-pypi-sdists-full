from .audio_preprocessing import preprocess_audio_in_messages, should_preprocess_audio
from .stt import (
    STTClient,
    STTRequest,
    STTResult,
    STTUsage,
    duration_to_stt_input_units,
    execute_stt,
)
from .transcription_cache import CachedTranscription, TranscriptionCache, clear_cache, get_cache

_LEGACY_GROQ_EXPORTS = frozenset({"GroqSTT", "TranscriptionResult", "TranscriptionUsage"})


def __getattr__(name: str):
    """Load the deprecated Groq compatibility surface only when requested."""
    if name not in _LEGACY_GROQ_EXPORTS:
        raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
    from . import groq_transcription

    value = getattr(groq_transcription, name)
    globals()[name] = value
    return value


def __dir__() -> list[str]:
    return sorted(set(globals()) | _LEGACY_GROQ_EXPORTS)

__all__ = [
    "preprocess_audio_in_messages",
    "should_preprocess_audio",
    "GroqSTT",
    "STTClient",
    "STTRequest",
    "STTResult",
    "STTUsage",
    "execute_stt",
    "duration_to_stt_input_units",
    "TranscriptionResult",
    "TranscriptionUsage",
    "get_cache",
    "clear_cache",
    "CachedTranscription",
    "TranscriptionCache",
]
