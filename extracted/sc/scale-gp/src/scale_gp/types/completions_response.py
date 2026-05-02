# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Dict, Optional

from .._models import BaseModel

__all__ = ["CompletionsResponse", "Completion", "TokenUsage"]


class Completion(BaseModel):
    """The actual completion text and the finish reason."""

    text: str
    """Completion text. If streaming, this field will contain each packet of text."""

    finish_reason: Optional[str] = None
    """Reason the LLM finished generating text."""

    response_metadata: Optional[Dict[str, object]] = None
    """Additional metadata returned from the completion response"""


class TokenUsage(BaseModel):
    """Token usage numbers.

    If streaming, this field is null until the stream completes, at which point it will be populated (if supported).
    """

    total: int
    """Total number of tokens in both the prompt and the completion."""

    completion: Optional[int] = None
    """Number of tokens in the completion."""

    prompt: Optional[int] = None
    """Number of tokens in the prompt."""


class CompletionsResponse(BaseModel):
    completion: Completion
    """The actual completion text and the finish reason."""

    token_usage: Optional[TokenUsage] = None
    """Token usage numbers.

    If streaming, this field is null until the stream completes, at which point it
    will be populated (if supported).
    """
