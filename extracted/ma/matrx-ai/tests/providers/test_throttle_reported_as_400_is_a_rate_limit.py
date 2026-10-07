"""A throttle a provider reports as HTTP 400 is classified rate_limit, not invalid_request.

Feedback eb34e17d: Anthropic answered 400 invalid_request_error "Grammar compilation rate
limit exceeded ... 20 compilations per minute"; it was recorded as invalid_request
(non-retryable) instead of a retryable rate limit with backoff.
"""

from __future__ import annotations

import anthropic
import httpx

from matrx_ai.providers.errors import classify_anthropic_error

_GRAMMAR_THROTTLE = (
    "Grammar compilation rate limit exceeded. Organization 57d272fd-2b2a-46f6-b402-7db41eff435d "
    "exceeded limit: 20 compilations per minute. You can try again later."
)


def _bad_request(message: str) -> anthropic.BadRequestError:
    body = {"type": "error", "error": {"type": "invalid_request_error", "message": message}}
    request = httpx.Request("POST", "https://api.anthropic.com/v1/messages")
    response = httpx.Response(400, request=request, json=body)
    return anthropic.BadRequestError(f"Error code: 400 - {body}", response=response, body=body)


def test_grammar_compilation_throttle_is_a_retryable_rate_limit() -> None:
    classified = classify_anthropic_error(_bad_request(_GRAMMAR_THROTTLE))
    assert classified.error_type == "rate_limit"
    assert classified.is_retryable is True
    assert (classified.retry_after or 0) >= 20


def test_a_real_bad_request_stays_invalid_request() -> None:
    classified = classify_anthropic_error(_bad_request("messages: at least one message is required"))
    assert classified.error_type == "invalid_request"
    assert classified.is_retryable is False
