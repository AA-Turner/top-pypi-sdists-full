"""TypeSafe System One provider contract.

Jev is a typed decision API, not a chat-completion provider. Jev 1.14 also
reads images (``assets``) and answers Box questions (where is X in the image).  This package is
therefore deliberately independent of ``UnifiedConfig`` and chat translators.
"""

from .client import (
    DEFAULT_BASE_URL,
    IMAGES_HEADER,
    BoxAnswer,
    BoxCoordinates,
    BoxQuestion,
    ChoiceAnswer,
    ChoiceQuestion,
    ImageAsset,
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
    "IMAGES_HEADER",
    "BoxAnswer",
    "BoxCoordinates",
    "BoxQuestion",
    "ChoiceAnswer",
    "ChoiceQuestion",
    "ImageAsset",
    "NoulAnswer",
    "NoulQuestion",
    "ScoreAnswer",
    "ScoreQuestion",
    "SystemOneRequest",
    "SystemOneResult",
    "TypeSafeProviderError",
    "call_system_one",
]
