from enum import Enum
from typing import Optional


class LLMChatApiVersion(Enum):
    V6 = 6
    V8 = 8


class LLMCompletionApiVersion(Enum):
    V3 = 3
    V8 = 8


class StopReason(str, Enum):
    STOP = "stop"
    LENGTH = "length"
    FUNCTION_CALL = "function_call"
    TOOL_CALL = "tool_call"
    UNKNOWN = "unknown"


class UnknownMetadataResponse:
    """
    Simple container for any number of arbitrary fields without validation
    """

    content: Optional[str] = None

    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

    def __repr__(self):
        fields = ", ".join(f"{k}={v!r}" for k, v in self.__dict__.items())
        return f"{self.__class__.__name__}({fields})"


class DeprecatedError(Exception):
    pass
