"""A model that calls a tool the request never offered fails with its real cause, never "An unexpected X error".

Break this guards (live 2026-11-10, system_error 7d1676bb, conversation 91ce306c): a test seat's
``chat.default_new_chat`` runs the tool-less "Test Reply" agent on groq openai/gpt-oss-20b. Asked to search the web,
the model emitted a tool call anyway; Groq's stream ended with a bare ``groq.APIError`` ("Tool choice is none, but model
called a tool") with no status, it fell to ``unknown_error``, and the person read "An unexpected Groq error occurred."
on every turn that reached for a tool. Two rules:

1. that provider wording is its own class (the model called a tool it was not given), naming what happened;
2. any error that still reaches the last-resort ``unknown_error`` carries the provider's own words in the sentence the
   person reads — nothing fails silently.
"""

from __future__ import annotations

import groq
import httpx
import pytest

from matrx_ai.providers.errors import classify_provider_error

_GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"


def _bare(msg: str) -> Exception:
    return groq.APIError(msg, httpx.Request("POST", _GROQ_URL), body=None)


def test_a_tool_call_with_no_tools_offered_names_the_cause() -> None:
    classified = classify_provider_error("groq", _bare("Tool choice is none, but model called a tool"))
    assert classified.error_type == "model_called_unoffered_tool"
    assert "An unexpected" not in classified.user_message
    assert "no tools" in classified.user_message
    # Sampling is nondeterministic: the next attempt can answer without a tool.
    assert classified.is_retryable is True


@pytest.mark.parametrize("provider", ["groq", "openai", "anthropic"])
def test_the_last_resort_sentence_carries_the_provider_words(provider: str) -> None:
    classified = classify_provider_error(provider, RuntimeError("zorblax frobnicated the widget"))
    assert classified.error_type == "unknown_error"
    assert "zorblax frobnicated the widget" in classified.details["provider_words"]


def test_the_last_resort_sentence_is_bounded() -> None:
    classified = classify_provider_error("groq", RuntimeError("x" * 5000))
    assert len(classified.user_message) < 800
