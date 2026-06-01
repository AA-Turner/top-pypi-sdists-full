"""
Utility functions for Pipecat integration.

Provides voice-specific utilities for:
- Pipecat availability and version checking
- Sensitive data masking for transcriptions
- Frame serialization and extraction
- Audio metadata utilities
"""

import logging
import re
from typing import Any

logger = logging.getLogger(__name__)


# Sensitive patterns for voice transcription masking
# Format: (pattern, replacement, description)
VOICE_SENSITIVE_PATTERNS: list[tuple[str, str, str]] = [
    # Phone numbers (spoken format)
    (
        r"\b(?:my\s+(?:phone\s+)?number\s+is\s+)?(\d{3})[-.\s]?(\d{3})[-.\s]?(\d{4})\b",
        "[PHONE]",
        "Phone numbers",
    ),
    (
        r"\b(?:call\s+me\s+at\s+)?(\d{3})[-.\s]?(\d{3})[-.\s]?(\d{4})\b",
        "[PHONE]",
        "Phone numbers with context",
    ),
    # Credit card numbers (spoken)
    (
        r"\b(?:card\s+number\s+(?:is\s+)?)?(\d{4})[-\s]?(\d{4})[-\s]?(\d{4})[-\s]?(\d{4})\b",
        "[CREDIT_CARD]",
        "Credit card numbers",
    ),
    # Social Security Numbers
    (
        r"\b(?:social\s+(?:security\s+)?(?:number\s+)?(?:is\s+)?)?(\d{3})[-\s]?(\d{2})[-\s]?(\d{4})\b",
        "[SSN]",
        "Social Security Numbers",
    ),
    # Email addresses (spoken)
    (
        r"\b[A-Za-z0-9._%+-]+\s*(?:at|@)\s*[A-Za-z0-9.-]+\s*(?:dot|\.)\s*(?:com|org|net|edu|gov|io|co)\b",
        "[EMAIL]",
        "Email addresses",
    ),
    (r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b", "[EMAIL]", "Email addresses standard"),
    # Account numbers
    (r"\b(?:account\s+(?:number\s+)?(?:is\s+)?)?(\d{8,16})\b", "[ACCOUNT]", "Account numbers"),
    # Passwords/PINs (spoken)
    (r"\b(?:password|pin|passcode)\s+(?:is\s+)?[^\s,]{4,}\b", "[PASSWORD]", "Passwords and PINs"),
    # Date of birth
    (
        r"\b(?:born\s+(?:on\s+)?|date\s+of\s+birth\s+(?:is\s+)?|dob\s+(?:is\s+)?)(\d{1,2})[/\-](\d{1,2})[/\-](\d{2,4})\b",
        "[DOB]",
        "Date of birth",
    ),
    # Addresses (basic patterns)
    (
        r"\b(\d{1,5})\s+([A-Za-z]+(?:\s+[A-Za-z]+)?)\s+(?:street|st|avenue|ave|road|rd|boulevard|blvd|drive|dr|lane|ln)\b",
        "[ADDRESS]",
        "Street addresses",
    ),
    # Names with context
    (
        r"\b(?:my\s+name\s+is|i\s+am|this\s+is)\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)?)\b",
        "[NAME]",
        "Names with context",
    ),
    # API keys and tokens (if spoken)
    (r"\b(?:api\s+key|token|secret)\s+(?:is\s+)?[A-Za-z0-9_\-]{16,}\b", "[API_KEY]", "API keys"),
]


def is_pipecat_available() -> bool:
    """
    Check if Pipecat is installed and available.

    Returns:
        True if Pipecat is available, False otherwise.
    """
    try:
        import pipecat

        return True
    except ImportError:
        return False


def get_pipecat_version() -> str | None:
    """
    Get the installed Pipecat version.

    Returns:
        Version string if Pipecat is installed, None otherwise.
    """
    try:
        import pipecat

        return getattr(pipecat, "__version__", "unknown")
    except ImportError:
        return None


def mask_sensitive_transcription(
    text: str,
    patterns: list[tuple[str, str, str]] | None = None,
) -> str:
    """
    Mask sensitive information in voice transcriptions.

    This is specifically designed for spoken content which may contain
    PII in natural language format (e.g., "my phone number is...").

    Args:
        text: Transcription text to mask
        patterns: Optional custom patterns (regex, replacement, description)

    Returns:
        Text with sensitive information masked
    """
    if not text:
        return text

    patterns_to_use = patterns if patterns is not None else VOICE_SENSITIVE_PATTERNS
    result = text

    for pattern, replacement, _ in patterns_to_use:
        try:
            result = re.sub(pattern, replacement, result, flags=re.IGNORECASE)
        except re.error:
            # Skip invalid patterns
            continue

    return result


def mask_sensitive_data(
    data: Any,
    patterns: list[tuple[str, str, str]] | None = None,
    max_depth: int = 10,
) -> Any:
    """
    Recursively mask sensitive data in various data structures.

    Args:
        data: Data to mask (string, dict, list, or nested combination)
        patterns: Optional custom patterns (regex, replacement, description)
        max_depth: Maximum recursion depth to prevent infinite loops

    Returns:
        Data with sensitive information masked
    """
    if max_depth <= 0:
        return data

    patterns_to_use = patterns if patterns is not None else VOICE_SENSITIVE_PATTERNS

    if isinstance(data, str):
        return mask_sensitive_transcription(data, patterns_to_use)
    if isinstance(data, dict):
        return {k: mask_sensitive_data(v, patterns_to_use, max_depth - 1) for k, v in data.items()}
    if isinstance(data, list):
        return [mask_sensitive_data(item, patterns_to_use, max_depth - 1) for item in data]
    if isinstance(data, tuple):
        return tuple(mask_sensitive_data(item, patterns_to_use, max_depth - 1) for item in data)
    return data


def mask_dict_keys(
    data: dict[str, Any],
    sensitive_keys: list[str] | None = None,
    mask_value: str = "[REDACTED]",
) -> dict[str, Any]:
    """
    Mask values for keys that might contain sensitive data.

    Args:
        data: Dictionary to mask
        sensitive_keys: List of key names to mask (case-insensitive partial match)
        mask_value: Value to use as replacement

    Returns:
        Dictionary with sensitive keys masked
    """
    default_sensitive_keys = [
        "password",
        "secret",
        "token",
        "api_key",
        "apikey",
        "auth",
        "credential",
        "private",
        "access_key",
        "secret_key",
        "bearer",
        "ssn",
        "social_security",
        "credit_card",
        "card_number",
    ]
    keys_to_check = sensitive_keys if sensitive_keys is not None else default_sensitive_keys

    result = {}
    for key, value in data.items():
        key_lower = key.lower()
        if any(sensitive in key_lower for sensitive in keys_to_check):
            result[key] = mask_value
        elif isinstance(value, dict):
            result[key] = mask_dict_keys(value, keys_to_check, mask_value)
        elif isinstance(value, list):
            result[key] = [
                mask_dict_keys(item, keys_to_check, mask_value) if isinstance(item, dict) else item
                for item in value
            ]
        else:
            result[key] = value

    return result


def safe_str(value: Any, max_length: int = 1000) -> str:
    """
    Safely convert a value to string with length limit.

    Args:
        value: Value to convert
        max_length: Maximum length of output string

    Returns:
        String representation, truncated if necessary
    """
    try:
        if value is None:
            return ""
        s = str(value)
        if len(s) > max_length:
            return s[:max_length] + "..."
        return s
    except Exception as e:
        return f"<error: {e}>"


def truncate_text(text: str, max_length: int = 2000, suffix: str = "...") -> str:
    """
    Truncate text to a maximum length.

    Args:
        text: Text to truncate
        max_length: Maximum length
        suffix: Suffix to add if truncated

    Returns:
        Truncated text
    """
    if not text:
        return text
    if len(text) <= max_length:
        return text
    return text[: max_length - len(suffix)] + suffix


def extract_frame_type(frame: Any) -> str:
    """
    Extract the type name from a Pipecat frame.

    Args:
        frame: Pipecat frame object

    Returns:
        Frame type name as string
    """
    if frame is None:
        return "unknown"

    if hasattr(frame, "__class__"):
        return frame.__class__.__name__

    return type(frame).__name__


def extract_text_from_frame(frame: Any) -> str | None:
    """
    Extract text content from various Pipecat frame types.

    Args:
        frame: Pipecat frame object

    Returns:
        Extracted text or None if no text content
    """
    if frame is None:
        return None

    # TranscriptionFrame, InterimTranscriptionFrame
    if hasattr(frame, "text"):
        return frame.text

    # TextFrame, LLMTextFrame
    if hasattr(frame, "text"):
        return frame.text

    # Handle dict-like frames
    if isinstance(frame, dict):
        return frame.get("text") or frame.get("content") or frame.get("message")

    return None


def extract_audio_metadata(frame: Any) -> dict[str, Any]:
    """
    Extract audio metadata from audio frames.

    Args:
        frame: Pipecat audio frame object

    Returns:
        Dictionary with audio metadata
    """
    metadata = {}

    # Sample rate
    if hasattr(frame, "sample_rate"):
        metadata["sample_rate"] = frame.sample_rate

    # Number of channels
    if hasattr(frame, "num_channels"):
        metadata["num_channels"] = frame.num_channels

    # Audio format
    if hasattr(frame, "audio_format"):
        metadata["audio_format"] = str(frame.audio_format)

    # Audio data length
    if hasattr(frame, "audio"):
        audio_data = frame.audio
        if hasattr(audio_data, "__len__"):
            metadata["audio_bytes"] = len(audio_data)

    # Duration if available
    if hasattr(frame, "duration"):
        metadata["duration_ms"] = frame.duration

    # Calculate duration from audio bytes if not directly available
    if "audio_bytes" in metadata and "sample_rate" in metadata:
        # Assuming 16-bit audio (2 bytes per sample)
        bytes_per_sample = 2
        num_channels = metadata.get("num_channels", 1)
        samples = metadata["audio_bytes"] / (bytes_per_sample * num_channels)
        metadata["calculated_duration_ms"] = (samples / metadata["sample_rate"]) * 1000

    return metadata


def serialize_frame(
    frame: Any,
    include_audio: bool = False,
    max_text_length: int = 2000,
) -> dict[str, Any]:
    """
    Serialize a Pipecat frame to a dictionary for tracing.

    Args:
        frame: Pipecat frame object
        include_audio: Whether to include audio data (can be large)
        max_text_length: Maximum length for text fields

    Returns:
        Serialized frame as dictionary
    """
    result = {
        "type": extract_frame_type(frame),
    }

    # Extract text content
    text = extract_text_from_frame(frame)
    if text:
        result["text"] = truncate_text(text, max_text_length)

    # Extract audio metadata
    audio_meta = extract_audio_metadata(frame)
    if audio_meta:
        result["audio_metadata"] = audio_meta

    # Common frame attributes
    if hasattr(frame, "id"):
        result["id"] = str(frame.id)

    if hasattr(frame, "timestamp"):
        result["timestamp"] = frame.timestamp

    if hasattr(frame, "name"):
        result["name"] = frame.name

    # Error frame specifics
    if hasattr(frame, "error"):
        result["error"] = safe_str(frame.error, 500)

    # Metrics frame specifics
    if hasattr(frame, "metrics"):
        result["metrics"] = frame.metrics if isinstance(frame.metrics, dict) else {}

    # Transcription specifics
    if hasattr(frame, "language"):
        result["language"] = frame.language

    if hasattr(frame, "confidence"):
        result["confidence"] = frame.confidence

    # User ID if available
    if hasattr(frame, "user_id"):
        result["user_id"] = frame.user_id

    return result


def extract_model_from_service(service: Any) -> str | None:
    """
    Extract the model name from a Pipecat service.

    Args:
        service: Pipecat service (STT, TTS, or LLM service)

    Returns:
        Model name or None
    """
    # Try common attribute names
    for attr in ["model", "model_name", "model_id", "_model", "_model_name"]:
        if hasattr(service, attr):
            value = getattr(service, attr)
            if value:
                return str(value)

    # Try to extract from class name
    class_name = service.__class__.__name__ if service else ""

    # Map common service class names to models
    service_model_map = {
        "DeepgramSTTService": "deepgram",
        "WhisperSTTService": "whisper",
        "AzureSTTService": "azure",
        "GoogleSTTService": "google",
        "ElevenLabsTTSService": "elevenlabs",
        "OpenAITTSService": "openai-tts",
        "AzureTTSService": "azure-tts",
        "CartesiaTTSService": "cartesia",
        "PlayHTTTSService": "playht",
        "OpenAILLMService": "gpt-4",
        "AnthropicLLMService": "claude",
        "GroqLLMService": "groq",
    }

    return service_model_map.get(class_name)


def format_duration_ms(duration_ms: float | None) -> str:
    """
    Format a duration in milliseconds to a human-readable string.

    Args:
        duration_ms: Duration in milliseconds

    Returns:
        Formatted duration string
    """
    if duration_ms is None:
        return "N/A"

    if duration_ms < 1000:
        return f"{duration_ms:.0f}ms"
    if duration_ms < 60000:
        return f"{duration_ms / 1000:.1f}s"
    minutes = int(duration_ms // 60000)
    seconds = (duration_ms % 60000) / 1000
    return f"{minutes}m {seconds:.1f}s"


def calculate_audio_duration_ms(
    audio_bytes: int,
    sample_rate: int = 16000,
    num_channels: int = 1,
    bits_per_sample: int = 16,
) -> float:
    """
    Calculate audio duration from byte length.

    Args:
        audio_bytes: Length of audio data in bytes
        sample_rate: Sample rate in Hz
        num_channels: Number of audio channels
        bits_per_sample: Bits per sample (typically 16)

    Returns:
        Duration in milliseconds
    """
    bytes_per_sample = bits_per_sample // 8
    total_samples = audio_bytes / (bytes_per_sample * num_channels)
    duration_seconds = total_samples / sample_rate
    return duration_seconds * 1000


def normalize_model_name(model: str) -> str:
    """
    Normalize model names for consistent pricing lookup.

    Args:
        model: Raw model name

    Returns:
        Normalized model name
    """
    if not model:
        return "unknown"

    model = model.lower().strip()

    # Common normalizations
    normalizations = {
        # OpenAI
        "gpt-4o": "gpt-4o",
        "gpt-4-turbo": "gpt-4-turbo",
        "gpt-4": "gpt-4",
        "gpt-3.5-turbo": "gpt-3.5-turbo",
        "gpt-3.5": "gpt-3.5-turbo",
        # Anthropic
        "claude-3-opus": "claude-3-opus",
        "claude-3-sonnet": "claude-3-sonnet",
        "claude-3-haiku": "claude-3-haiku",
        "claude-3.5-sonnet": "claude-3.5-sonnet",
        # Deepgram
        "nova-2": "deepgram-nova-2",
        "nova": "deepgram-nova",
        # ElevenLabs
        "eleven_multilingual_v2": "elevenlabs-multilingual-v2",
        "eleven_turbo_v2": "elevenlabs-turbo-v2",
    }

    for key, value in normalizations.items():
        if key in model:
            return value

    return model


def get_frame_category(frame_type: str) -> str:
    """
    Get the category of a frame based on its type name.

    Args:
        frame_type: Frame type name

    Returns:
        Category string (stt, tts, llm, audio, control, metrics, error, unknown)
    """
    frame_type_lower = frame_type.lower()

    if any(x in frame_type_lower for x in ["transcription", "stt", "speech"]):
        return "stt"
    if any(x in frame_type_lower for x in ["tts", "synthesis", "speak"]):
        return "tts"
    if any(x in frame_type_lower for x in ["llm", "text", "response", "chat"]):
        return "llm"
    if any(x in frame_type_lower for x in ["audio", "raw"]):
        return "audio"
    if any(x in frame_type_lower for x in ["start", "stop", "end", "cancel", "interrupt"]):
        return "control"
    if any(x in frame_type_lower for x in ["metric", "ttfb", "processing"]):
        return "metrics"
    if "error" in frame_type_lower:
        return "error"
    return "unknown"
