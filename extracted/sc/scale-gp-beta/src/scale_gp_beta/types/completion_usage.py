# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import TYPE_CHECKING, Dict, Optional

from pydantic import Field as FieldInfo

from .._models import BaseModel

__all__ = ["CompletionUsage", "CompletionTokensDetails", "PromptTokensDetails"]


class CompletionTokensDetails(BaseModel):
    """Breakdown of tokens used in a completion."""

    accepted_prediction_tokens: Optional[int] = None

    audio_tokens: Optional[int] = None

    reasoning_tokens: Optional[int] = None

    rejected_prediction_tokens: Optional[int] = None

    if TYPE_CHECKING:
        # Some versions of Pydantic <2.8.0 have a bug and don’t allow assigning a
        # value to this field, so for compatibility we avoid doing it at runtime.
        __pydantic_extra__: Dict[str, object] = FieldInfo(init=False)  # pyright: ignore[reportIncompatibleVariableOverride]

        # Stub to indicate that arbitrary properties are accepted.
        # To access properties that are not valid identifiers you can use `getattr`, e.g.
        # `getattr(obj, '$type')`
        def __getattr__(self, attr: str) -> object: ...
    else:
        __pydantic_extra__: Dict[str, object]


class PromptTokensDetails(BaseModel):
    """Breakdown of tokens used in the prompt."""

    audio_tokens: Optional[int] = None

    cached_tokens: Optional[int] = None

    if TYPE_CHECKING:
        # Some versions of Pydantic <2.8.0 have a bug and don’t allow assigning a
        # value to this field, so for compatibility we avoid doing it at runtime.
        __pydantic_extra__: Dict[str, object] = FieldInfo(init=False)  # pyright: ignore[reportIncompatibleVariableOverride]

        # Stub to indicate that arbitrary properties are accepted.
        # To access properties that are not valid identifiers you can use `getattr`, e.g.
        # `getattr(obj, '$type')`
        def __getattr__(self, attr: str) -> object: ...
    else:
        __pydantic_extra__: Dict[str, object]


class CompletionUsage(BaseModel):
    """Usage statistics for the completion request."""

    completion_tokens: int

    prompt_tokens: int

    total_tokens: int

    completion_tokens_details: Optional[CompletionTokensDetails] = None
    """Breakdown of tokens used in a completion."""

    prompt_tokens_details: Optional[PromptTokensDetails] = None
    """Breakdown of tokens used in the prompt."""

    if TYPE_CHECKING:
        # Some versions of Pydantic <2.8.0 have a bug and don’t allow assigning a
        # value to this field, so for compatibility we avoid doing it at runtime.
        __pydantic_extra__: Dict[str, object] = FieldInfo(init=False)  # pyright: ignore[reportIncompatibleVariableOverride]

        # Stub to indicate that arbitrary properties are accepted.
        # To access properties that are not valid identifiers you can use `getattr`, e.g.
        # `getattr(obj, '$type')`
        def __getattr__(self, attr: str) -> object: ...
    else:
        __pydantic_extra__: Dict[str, object]
