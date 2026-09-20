"""TypeSafe System One provider contract.

Jev is a typed decision API, not a chat-completion provider.  This package is
therefore deliberately independent of ``UnifiedConfig`` and chat translators.
"""

from .client import (
    DEFAULT_BASE_URL,
    ChoiceAnswer,
    ChoiceQuestion,
    NoulAnswer,
    NoulQuestion,
    ScoreAnswer,
    ScoreQuestion,
    SystemOneRequest,
    SystemOneResult,
    TypeSafeProviderError,
    call_system_one,
)

__all__ = [
    "DEFAULT_BASE_URL",
    "ChoiceAnswer",
    "ChoiceQuestion",
    "NoulAnswer",
    "NoulQuestion",
    "ScoreAnswer",
    "ScoreQuestion",
    "SystemOneRequest",
    "SystemOneResult",
    "TypeSafeProviderError",
    "call_system_one",
]
