"""A media item refused before dispatch is never classified as a provider connection failure.

Live 2026-11-12: a ``MediaFallbackResolutionError`` whose resolver detail contained "Refused" fell to the
string fallback and became an Anthropic ``connection_error`` ("Could not connect to Anthropic"), retried
until exhausted, though no request was ever sent. The typed branch keys on the exception, not its text.
"""

from __future__ import annotations

import pytest

from matrx_ai.processing.media_fallback.handler import MediaFallbackResolutionError
from matrx_ai.providers.errors import classify_anthropic_error, classify_provider_error
from matrx_ai.providers.provider_io_capabilities import MediaContainer


@pytest.mark.parametrize(
    "detail",
    [
        "resolver for video raised: BaaRefusedError('turned off here') — dropped.",
        "resolver for video raised: ConnectionError('network unreachable') — dropped.",
        "resolver for document raised: TimeoutError('timed out') — dropped.",
    ],
)
@pytest.mark.parametrize("provider", ["anthropic", "openai", "google", "unknown"])
def test_media_conversion_failure_is_typed_and_not_retried(detail: str, provider: str) -> None:
    error = MediaFallbackResolutionError(
        MediaContainer.VIDEO, model_name="claude-sonnet-5-5", endpoint="anthropic_chat", detail=detail
    )

    classified = classify_provider_error(provider, error)

    assert classified.error_type == "media_conversion_failed"
    assert classified.is_retryable is False
    assert classified.details["container"] == "video"
    assert "Could not connect" not in classified.user_message
    # the resolver's own words are developer detail: kept in ``message``, never in the person's sentence
    assert detail in classified.message
    assert detail not in classified.user_message


def test_anthropic_entry_point_agrees() -> None:
    error = MediaFallbackResolutionError(
        MediaContainer.YOUTUBE, model_name="m", endpoint=None, detail="connection refused"
    )
    assert classify_anthropic_error(error).error_type == "media_conversion_failed"
