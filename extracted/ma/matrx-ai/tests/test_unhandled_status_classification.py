"""An HTTP status a provider classifier has no branch for is classified by what
the status MEANS, never as a retryable ``unknown_error``.

Break named (review 2026-10-01): 415 / 422 / 451 fell through every
``*_by_status`` classifier to the string fallback → retryable ``unknown_error``,
so a transcription the provider rejected as an unsupported container (415) was
sent three times, as was every 422. Only a status that can succeed on a second
attempt (408 timeout, 425 too-early) may retry.

SUT: the shared status classifiers in ``matrx_ai.providers.errors``, reached
through ``classify_provider_error`` with each SDK family's real status error.
"""

from __future__ import annotations

import anthropic
import groq
import httpx
import openai
import pytest

from matrx_ai.providers.errors import classify_provider_error

_REQ = httpx.Request("POST", "https://provider.invalid/v1/audio/transcriptions")

_SDKS = [
    ("groq", groq.APIStatusError),
    ("openai", openai.APIStatusError),
    ("anthropic", anthropic.APIStatusError),
    ("together", openai.APIStatusError),
]

_EXPECTED = [
    (415, False),  # unsupported media type — the file is the problem
    (422, False),  # unprocessable — the request is the problem
    (451, False),  # unavailable for legal reasons
    (408, True),  # request timeout — a second attempt can succeed
    (425, True),  # too early — retry is the documented remedy
]


@pytest.mark.parametrize(("provider", "sdk_error"), _SDKS, ids=[p for p, _ in _SDKS])
@pytest.mark.parametrize(("status", "retryable"), _EXPECTED, ids=[str(s) for s, _ in _EXPECTED])
def test_an_unbranched_status_is_classified_by_its_meaning(provider, sdk_error, status, retryable) -> None:
    exc = sdk_error(
        f"Error code: {status} - The audio file format is not accepted for this model.",
        response=httpx.Response(status, request=_REQ),
        body=None,
    )
    result = classify_provider_error(provider, exc)
    assert result.is_retryable is retryable, (provider, status, result.error_type)
    assert result.error_type != "unknown_error"
    assert result.status_code == status
