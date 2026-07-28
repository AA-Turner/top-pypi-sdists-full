"""
KugelAudio Python SDK - Official client for KugelAudio TTS API.

Example usage:
    from kugelaudio import KugelAudio

    client = KugelAudio(api_key="your_api_key")

    # List available models
    models = client.models.list()

    # List available voices
    voices = client.voices.list().voices

    # Generate audio (non-streaming)
    audio = client.tts.generate(
        text="Hello, world!",
        model="kugel-1-turbo",
        voice_id=123,
    )
    audio.save("output.wav")

    # Generate audio (streaming via WebSocket)
    for chunk in client.tts.stream(
        text="Hello, world!",
        model="kugel-1-turbo",
        voice_id=123,
    ):
        # Process audio chunk
        pass
"""

from kugelaudio.client import KugelAudio
from kugelaudio.exceptions import (
    AuthenticationError,
    ConnectionError as KugelAudioConnectionError,
    InsufficientCreditsError,
    KugelAudioError,
    NotFoundError,
    RateLimitError,
    ValidationError,
)
from kugelaudio.models import (
    AudioChunk,
    AudioResponse,
    BulkReplaceResult,
    Dictionary,
    DictionaryEntry,
    DictionaryEntryList,
    GenerateRequest,
    Model,
    SessionUsage,
    StreamConfig,
    Voice,
    VoiceDetail,
    VoiceListResponse,
    VoiceReference,
    WordTimestamp,
)
from kugelaudio.streaming import (
    MultiContextSession,
    StreamingSession,
    StreamingSessionSync,
)

__version__ = "1.8.0"
__all__ = [
    "KugelAudio",
    "AudioChunk",
    "AudioResponse",
    "BulkReplaceResult",
    "Dictionary",
    "DictionaryEntry",
    "DictionaryEntryList",
    "GenerateRequest",
    "Model",
    "SessionUsage",
    "StreamConfig",
    "Voice",
    "VoiceDetail",
    "VoiceListResponse",
    "VoiceReference",
    "WordTimestamp",
    "StreamingSession",
    "StreamingSessionSync",
    "MultiContextSession",
    "KugelAudioError",
    "AuthenticationError",
    "RateLimitError",
    "InsufficientCreditsError",
    "ValidationError",
    "NotFoundError",
    "KugelAudioConnectionError",
]

