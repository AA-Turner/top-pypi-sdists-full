"""Seltz Python SDK for interacting with the Seltz API."""

from ._types import OMIT, Omit
from .exceptions import (
    SeltzAPIError,
    SeltzAuthenticationError,
    SeltzConfigurationError,
    SeltzConnectionError,
    SeltzError,
    SeltzRateLimitError,
    SeltzTimeoutError,
)
from .seltz import AsyncSeltz, Seltz
from .services import (
    AnswerResponse,
    AnswerStreamResponse,
    Citation,
    Citations,
    Document,
    SearchResponse,
)

__all__ = [
    # Main client
    "Seltz",
    "AsyncSeltz",
    # Types (protobuf)
    "SearchResponse",
    "Document",
    "AnswerResponse",
    "AnswerStreamResponse",
    "Citation",
    "Citations",
    # Sentinel
    "OMIT",
    "Omit",
    # Exceptions
    "SeltzError",
    "SeltzConfigurationError",
    "SeltzAuthenticationError",
    "SeltzConnectionError",
    "SeltzAPIError",
    "SeltzTimeoutError",
    "SeltzRateLimitError",
]
