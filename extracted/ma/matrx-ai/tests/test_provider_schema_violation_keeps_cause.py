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
    assert "missing properties: '__kind'" in classified.message
    assert classified.status_code == 400
    assert classified.is_retryable is True
    assert "An unexpected" not in classified.user_message


_TOOL_MSG = (
    "Tool call validation failed: tool call validation failed: parameters for tool context "
    "did not match schema: errors: [`/action`: value must be one of 'get', 'batch', 'create']"
)


def test_tool_call_schema_violation_is_retryable_and_names_the_path() -> None:
    """Live 2026-11-05 (system_error 902f876c): the model sent a `context` action outside the enum."""
    exc = groq.APIError(_TOOL_MSG, httpx.Request("POST", "https://api.groq.com/openai/v1/chat/completions"), body=None)
    classified = classify_provider_error("groq", exc)
    assert classified.error_type == "structured_output_invalid"
    assert "value must be one of 'get', 'batch', 'create'" in classified.message
    assert classified.is_retryable is True


def test_unparseable_tool_call_arguments_are_a_retryable_sampling_failure() -> None:
    """Live 2026-11-16 (issue_class groq.unknown_error): the model's tool-call arguments were not JSON."""
    msg = "Failed to parse tool call arguments as JSON"
    exc = groq.APIError(msg, httpx.Request("POST", "https://api.groq.com/openai/v1/chat/completions"), body=None)
    classified = classify_provider_error("groq", exc)
    assert classified.error_type == "structured_output_invalid"
    assert classified.is_retryable is True
    assert "An unexpected" not in classified.user_message


# Live 2026-11-14 09:12 (issue_class groq.invalid_request): the NON-streamed path. Groq answers
# a typed call whose generated JSON broke (a missing `","keywords":`) with an HTTP 400
# ``BadRequestError`` carrying code ``json_validate_failed``. The 400 branch read it as a
# non-retryable ``invalid_request`` — the run died on a sample the next attempt could fix, and
# the class sat beside ``structured_output_invalid`` as if it were our request's fault.
_STATUS_400_MSG = (
    "Error code: 400 - {'error': {'message': \"Failed to generate JSON. Please adjust your prompt. "
    "See 'failed_generation' for more details.\", 'type': 'invalid_request_error', "
    "'code': 'json_validate_failed', 'failed_generation': '{\"label\":\"x\",\"description\":\"y Keywords\":[\"a\"]}'}}"
)


def _bad_request_400() -> Exception:
    request = httpx.Request("POST", "https://api.groq.com/openai/v1/chat/completions")
    response = httpx.Response(400, request=request)
    return groq.BadRequestError(
        _STATUS_400_MSG,
        response=response,
        body={"error": {"message": "Failed to generate JSON.", "code": "json_validate_failed"}},
    )


def test_status_400_json_validate_failed_is_a_retryable_schema_violation() -> None:
    classified = classify_provider_error("groq", _bad_request_400())
    assert classified.error_type == "structured_output_invalid"
    assert classified.is_retryable is True
    assert classified.status_code == 400


def test_a_plain_400_stays_invalid_request() -> None:
    request = httpx.Request("POST", "https://api.groq.com/openai/v1/chat/completions")
    exc = groq.BadRequestError(
        "Error code: 400 - {'error': {'message': 'messages: must not be empty'}}",
        response=httpx.Response(400, request=request),
        body={"error": {"message": "messages: must not be empty"}},
    )
    classified = classify_provider_error("groq", exc)
    assert classified.error_type == "invalid_request"
    assert classified.is_retryable is False
