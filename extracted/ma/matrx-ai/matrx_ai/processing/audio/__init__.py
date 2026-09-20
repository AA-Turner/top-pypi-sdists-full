from .audio_preprocessing import preprocess_audio_in_messages, should_preprocess_audio
from .stt import (
    DEFAULT_PROVIDER_AUDIO_LIMIT_MB,
    PROVIDER_ACCEPTED_AUDIO_SUFFIXES,
    STTClient,
    STTRequest,
    STTResult,
    STTUsage,
    duration_to_stt_input_units,
    execute_stt,
    provider_accepts_audio_container,
    provider_audio_limit_mb,
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
    "provider_accepts_audio_container",
    "provider_audio_limit_mb",
    "PROVIDER_ACCEPTED_AUDIO_SUFFIXES",
    "DEFAULT_PROVIDER_AUDIO_LIMIT_MB",
    "TranscriptionResult",
    "TranscriptionUsage",
    "get_cache",
    "clear_cache",
    "CachedTranscription",
    "TranscriptionCache",
]
