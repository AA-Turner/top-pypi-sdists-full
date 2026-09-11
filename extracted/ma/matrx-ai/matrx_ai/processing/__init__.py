from matrx_ai.processing.audio import (
    CachedTranscription,
    STTClient,
    STTRequest,
    STTResult,
    STTUsage,
    TranscriptionCache,
    clear_cache,
    duration_to_stt_input_units,
    execute_stt,
    get_cache,
    preprocess_audio_in_messages,
    should_preprocess_audio,
)
from matrx_ai.processing.vision import (
    MODEL_TO_VISION_CLASS,
    VISION_API_CLASSES,
    WIRE_FORMAT_DEFAULT_VISION_CLASS,
    VisionApiClass,
    is_known_vision_class,
    reencode_for_vision_class,
    resolve_vision_class,
    should_skip_reencode,
)

_LEGACY_GROQ_EXPORTS = frozenset({"GroqSTT", "TranscriptionResult", "TranscriptionUsage"})


def __getattr__(name: str):
    """Keep deprecated audio exports lazy to avoid provider import cycles."""
    if name not in _LEGACY_GROQ_EXPORTS:
        raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
    from matrx_ai.processing import audio

    value = getattr(audio, name)
    globals()[name] = value
    return value


def __dir__() -> list[str]:
    return sorted(set(globals()) | _LEGACY_GROQ_EXPORTS)

__all__ = [
    "CachedTranscription",
    "GroqSTT",
    "STTClient",
    "STTRequest",
    "STTResult",
    "STTUsage",
    "TranscriptionCache",
    "TranscriptionResult",
    "TranscriptionUsage",
    "clear_cache",
    "duration_to_stt_input_units",
    "execute_stt",
    "get_cache",
    "preprocess_audio_in_messages",
    "should_preprocess_audio",
    "VisionApiClass",
    "VISION_API_CLASSES",
    "MODEL_TO_VISION_CLASS",
    "WIRE_FORMAT_DEFAULT_VISION_CLASS",
    "resolve_vision_class",
    "is_known_vision_class",
    "reencode_for_vision_class",
    "should_skip_reencode",
]
