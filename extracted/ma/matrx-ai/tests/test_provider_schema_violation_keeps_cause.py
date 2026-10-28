"""A provider's "your output broke the schema" error keeps its real cause.

Break this guards (live 2026-10-27, Brand Curator on groq openai/gpt-oss-20b): Groq's
streamed ``json_validate_failed`` arrives as a bare ``groq.APIError`` with no status.
It fell to ``unknown_error`` and the saved turn read "An unexpected Groq error
occurred." — the schema path the model violated was lost. Any provider wording that
reaches the fallback without being named turns this red.
"""

from __future__ import annotations

import groq
import httpx
import pytest

from matrx_ai.providers.errors import classify_provider_error

_MSG = (
    "Generated JSON does not match the expected schema. Please adjust your prompt. "
    "See 'failed_generation' for more details. Error: jsonschema: '/entries/0' does not "
    "validate with /properties/entries/items/$ref/required: missing properties: '__kind'"
)


def _bare_api_error() -> Exception:
    return groq.APIError(_MSG, httpx.Request("POST", "https://api.groq.com/openai/v1/chat/completions"), body=None)


@pytest.mark.parametrize("provider", ["groq", "openai", "cerebras", "together"])
def test_schema_violation_names_the_schema_path(provider: str) -> None:
    exc = _bare_api_error() if provider == "groq" else RuntimeError(_MSG)
    classified = classify_provider_error(provider, exc)
    assert classified.error_type == "structured_output_invalid"
    assert "missing properties: '__kind'" in classified.user_message
    assert classified.status_code == 400
    assert classified.is_retryable is True
    assert "An unexpected" not in classified.user_message
