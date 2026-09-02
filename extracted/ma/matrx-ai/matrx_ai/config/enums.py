# ============================================================================
# ENUMS AND CONSTANTS

# Tasks:
# - Content Type is unused - use it or remove it.
# - Provider is unused - use it or remove it.

# ============================================================================


from enum import StrEnum


class Role(StrEnum):
    SYSTEM = "system"
    DEVELOPER = "developer"
    USER = "user"
    ASSISTANT = "assistant"
    TOOL = "tool"  # For OpenAI tool results
    OUTPUT = "output"


class ContentType(StrEnum):
    TEXT = "text"
    IMAGE = "image"
    AUDIO = "audio"
    VIDEO = "video"
    DOCUMENT = "document"
    YOUTUBE_VIDEO = "youtube_video"
    MEDIA = "media"  # Unified storage format with kind discriminator
    TOOL_CALL = "tool_call"
    TOOL_RESULT = "tool_result"
    THINKING = "thinking"
    CODE_EXECUTION = "code_execution"
    CODE_EXECUTION_RESULT = "code_execution_result"
    EXECUTABLE_CODE = "executable_code"


class Provider(StrEnum):
    OPENAI = "openai"
    ANTHROPIC = "anthropic"
    GEMINI = "gemini"
    XAI = "xai"
    TOGETHER = "together"
    GROQ = "groq"
    CEREBRAS = "cerebras"
    OLLAMA = "ollama"
