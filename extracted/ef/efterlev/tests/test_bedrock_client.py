"""Tests for `AnthropicBedrockClient` (SPEC-10).

Mocks the boto3 bedrock-runtime client so the retry/fallback/error-
classification logic is exercised without real AWS. Real Bedrock
integration is the responsibility of SPEC-13 (e2e harness Bedrock path),
gated on env vars and skipped by default.
"""

from __future__ import annotations

from typing import Any
from unittest.mock import MagicMock

import pytest

from efterlev.errors import AgentError
from efterlev.llm.base import LLMMessage
from efterlev.llm.bedrock_client import (
    _MAX_READ_TIMEOUT_RETRIES,
    _MAX_TOTAL_WALL_SECONDS,
    AnthropicBedrockClient,
    _backoff_delay,
    _is_read_timeout,
    _is_retryable_bedrock,
)

# --- helpers ---------------------------------------------------------


def _converse_response(text: str = "ok", stop_reason: str = "end_turn") -> dict[str, Any]:
    """Build a minimal Bedrock Converse API response shape."""
    return {
        "stopReason": stop_reason,
        "output": {"message": {"role": "assistant", "content": [{"text": text}]}},
        "ResponseMetadata": {
            "HTTPHeaders": {"x-amzn-bedrock-model-id": "us.anthropic.claude-opus-4-7-v1:0"},
        },
    }


def _client_error(code: str) -> Exception:
    """Build a botocore ClientError with the given Bedrock error code."""
    from botocore.exceptions import ClientError

    return ClientError(
        error_response={"Error": {"Code": code, "Message": f"simulated {code}"}},
        operation_name="Converse",
    )


def _bedrock_with_mock(
    *,
    region: str = "us-east-1",
    fallback_model: str | None = None,
    canned: list[Any] | None = None,
) -> tuple[AnthropicBedrockClient, MagicMock]:
    """Construct a client with a pre-injected mock boto3 bedrock-runtime."""
    client = AnthropicBedrockClient(
        region=region,
        fallback_model=fallback_model,
        sleeper=lambda _: None,
    )
    fake = MagicMock()
    if canned:
        # Each entry is either a response dict (returned) or an exception (raised).
        side_effects: list[Any] = list(canned)
        fake.converse.side_effect = side_effects
    client._client_obj = fake  # type: ignore[assignment]
    return client, fake


# --- happy paths -----------------------------------------------------


def test_complete_returns_response_text() -> None:
    client, fake = _bedrock_with_mock(canned=[_converse_response("hello world")])
    resp = client.complete(
        system="sys",
        messages=[LLMMessage(content="hi")],
        model="us.anthropic.claude-opus-4-7-v1:0",
    )
    assert resp.text == "hello world"
    assert resp.model == "us.anthropic.claude-opus-4-7-v1:0"
    assert resp.prompt_hash  # populated
    assert fake.converse.call_count == 1


def test_complete_concatenates_multi_block_response() -> None:
    """Multi-block responses (rare but possible per Bedrock docs)."""
    multi = _converse_response("first ")
    multi["output"]["message"]["content"] = [{"text": "first "}, {"text": "second"}]
    client, _ = _bedrock_with_mock(canned=[multi])
    resp = client.complete(
        system="sys",
        messages=[LLMMessage(content="hi")],
        model="m",
    )
    assert resp.text == "first second"


def test_complete_passes_system_and_messages_to_converse() -> None:
    client, fake = _bedrock_with_mock(canned=[_converse_response("ok")])
    client.complete(
        system="be helpful",
        messages=[LLMMessage(content="hello"), LLMMessage(content="follow up")],
        model="m",
    )
    call_kwargs = fake.converse.call_args.kwargs
    assert call_kwargs["modelId"] == "m"
    assert call_kwargs["system"] == [{"text": "be helpful"}]
    assert call_kwargs["messages"] == [
        {"role": "user", "content": [{"text": "hello"}]},
        {"role": "user", "content": [{"text": "follow up"}]},
    ]
    assert call_kwargs["inferenceConfig"] == {"maxTokens": 4096}


# --- response-validation failures ------------------------------------


def test_max_tokens_truncation_raises() -> None:
    truncated = _converse_response("partial", stop_reason="max_tokens")
    client, _ = _bedrock_with_mock(canned=[truncated])
    with pytest.raises(AgentError, match="truncated at max_tokens"):
        client.complete(system="s", messages=[LLMMessage("x")], model="m")


def test_no_text_blocks_raises() -> None:
    empty = _converse_response("")
    empty["output"]["message"]["content"] = []
    client, _ = _bedrock_with_mock(canned=[empty])
    with pytest.raises(AgentError, match="no text content"):
        client.complete(system="s", messages=[LLMMessage("x")], model="m")


# --- retry behavior --------------------------------------------------


def test_retry_on_throttling_then_success() -> None:
    """Transient ThrottlingException retries and the second attempt succeeds."""
    client, fake = _bedrock_with_mock(
        canned=[_client_error("ThrottlingException"), _converse_response("ok")],
    )
    resp = client.complete(system="s", messages=[LLMMessage("x")], model="m")
    assert resp.text == "ok"
    assert fake.converse.call_count == 2


def test_retry_exhausted_without_fallback_raises() -> None:
    """3 throttling errors + no fallback configured → AgentError."""
    client, fake = _bedrock_with_mock(
        canned=[_client_error("ThrottlingException")] * 3,
    )
    with pytest.raises(AgentError, match="bedrock completion failed"):
        client.complete(system="s", messages=[LLMMessage("x")], model="m")
    assert fake.converse.call_count == 3


def test_fallback_after_primary_exhausted() -> None:
    """3 primary throttles → fallback model attempted once → success on fallback."""
    client, fake = _bedrock_with_mock(
        fallback_model="us.anthropic.claude-sonnet-4-6-v1:0",
        canned=[
            _client_error("ThrottlingException"),
            _client_error("ThrottlingException"),
            _client_error("ThrottlingException"),
            _converse_response("from fallback"),
        ],
    )
    resp = client.complete(system="s", messages=[LLMMessage("x")], model="m-primary")
    assert resp.text == "from fallback"
    assert fake.converse.call_count == 4
    fallback_call = fake.converse.call_args_list[3].kwargs
    assert fallback_call["modelId"] == "us.anthropic.claude-sonnet-4-6-v1:0"


def test_fallback_also_failing_raises_original_error() -> None:
    """Primary exhausts retries, fallback also fails — the original error surfaces."""
    client, fake = _bedrock_with_mock(
        fallback_model="us.anthropic.claude-sonnet-4-6-v1:0",
        canned=[_client_error("ThrottlingException")] * 4,
    )
    with pytest.raises(AgentError, match="bedrock completion failed"):
        client.complete(system="s", messages=[LLMMessage("x")], model="m")
    assert fake.converse.call_count == 4


# --- non-retryable errors --------------------------------------------


def test_no_retry_on_access_denied() -> None:
    """AccessDeniedException is permanent — fail immediately, no retry."""
    client, fake = _bedrock_with_mock(canned=[_client_error("AccessDeniedException")])
    with pytest.raises(AgentError, match="bedrock completion failed"):
        client.complete(system="s", messages=[LLMMessage("x")], model="m")
    assert fake.converse.call_count == 1


def test_no_retry_on_validation_error() -> None:
    client, fake = _bedrock_with_mock(canned=[_client_error("ValidationException")])
    with pytest.raises(AgentError):
        client.complete(system="s", messages=[LLMMessage("x")], model="m")
    assert fake.converse.call_count == 1


def test_no_retry_on_resource_not_found() -> None:
    """ResourceNotFoundException is the GovCloud cross-boundary signal."""
    client, fake = _bedrock_with_mock(canned=[_client_error("ResourceNotFoundException")])
    with pytest.raises(AgentError):
        client.complete(system="s", messages=[LLMMessage("x")], model="m")
    assert fake.converse.call_count == 1


# --- classifier directly ---------------------------------------------


def test_is_retryable_bedrock_classifies_correctly() -> None:
    assert _is_retryable_bedrock(_client_error("ThrottlingException")) is True
    assert _is_retryable_bedrock(_client_error("ServiceQuotaExceededException")) is True
    assert _is_retryable_bedrock(_client_error("ModelTimeoutException")) is True
    assert _is_retryable_bedrock(_client_error("InternalServerException")) is True
    assert _is_retryable_bedrock(_client_error("AccessDeniedException")) is False
    assert _is_retryable_bedrock(_client_error("ValidationException")) is False
    assert _is_retryable_bedrock(_client_error("ResourceNotFoundException")) is False
    assert _is_retryable_bedrock(AgentError("self-raised, never retry")) is False


def test_is_retryable_bedrock_handles_network_errors() -> None:
    """ReadTimeoutError and friends are retryable per the docstring contract."""
    from botocore.exceptions import ConnectTimeoutError, EndpointConnectionError, ReadTimeoutError

    assert _is_retryable_bedrock(ReadTimeoutError(endpoint_url="x")) is True
    assert _is_retryable_bedrock(ConnectTimeoutError(endpoint_url="x")) is True
    assert _is_retryable_bedrock(EndpointConnectionError(endpoint_url="x")) is True


def test_is_retryable_bedrock_unknown_exception_not_retryable() -> None:
    """An unknown error type is conservatively classified non-retryable."""
    assert _is_retryable_bedrock(RuntimeError("???")) is False


# --- backoff ---------------------------------------------------------


def test_backoff_delay_within_cap() -> None:
    for attempt in range(10):
        d = _backoff_delay(attempt)
        assert 0 <= d <= 60.0


# --- v0.1.37: silent-wedge fix ---------------------------------------


def _read_timeout_error() -> Exception:
    """Build a botocore ReadTimeoutError matching what real Bedrock raises
    after the configured `read_timeout=600s` is exceeded."""
    from botocore.exceptions import ReadTimeoutError

    return ReadTimeoutError(endpoint_url="https://bedrock-runtime.us-east-1.amazonaws.com")


def test_v0_1_37_read_timeout_capped_at_one_retry(capsys: pytest.CaptureFixture[str]) -> None:
    """The v0.1.35 deep-test silent-wedge failure mode: ReadTimeoutError
    should NOT consume the full _MAX_RETRIES budget. Each ReadTimeout
    burns ~600s of wall time on real Bedrock; pre-v0.1.37 the loop
    allowed 3 of them (~30 min). v0.1.37 caps at
    `_MAX_READ_TIMEOUT_RETRIES + 1` total attempts (1 retry = 2 attempts).

    Verifies: ReadTimeout raised twice → second one trips the cap →
    AgentError raised → progress message written to stderr.
    """
    client, fake = _bedrock_with_mock(
        # 4 ReadTimeouts queued; the cap should make us stop after 2 attempts.
        canned=[_read_timeout_error()] * 4,
    )
    with pytest.raises(AgentError):
        client.complete(system="s", messages=[LLMMessage("x")], model="m")
    assert fake.converse.call_count == _MAX_READ_TIMEOUT_RETRIES + 1, (
        f"expected ReadTimeout to cap converse calls at "
        f"{_MAX_READ_TIMEOUT_RETRIES + 1}; got {fake.converse.call_count}"
    )
    err = capsys.readouterr().err
    assert "[bedrock]" in err
    assert "ReadTimeoutError" in err


def test_v0_1_37_progress_messages_visible_on_retry(capsys: pytest.CaptureFixture[str]) -> None:
    """Pre-v0.1.37 retry warnings only went via `log.warning` which is
    invisible without explicit logging config. v0.1.37 writes progress
    to stderr directly so the user sees what's happening even with
    logging unconfigured.

    Verifies: a transient throttle → retry attempt → success path emits
    a `[bedrock]` progress line to stderr. Note: `type(e).__name__` is
    `ClientError` (the botocore class), not the error code string —
    error code lives in e.response['Error']['Code'].
    """
    client, _ = _bedrock_with_mock(
        canned=[_client_error("ThrottlingException"), _converse_response("ok")],
    )
    resp = client.complete(system="s", messages=[LLMMessage("x")], model="m")
    assert resp.text == "ok"
    err = capsys.readouterr().err
    assert "[bedrock]" in err
    assert "ClientError" in err  # type name, per `type(e).__name__`
    assert "retrying in" in err


def test_v0_1_37_wall_clock_budget_caps_total_time(monkeypatch: pytest.MonkeyPatch) -> None:
    """Even if errors are retryable AND the per-error budget allows more
    attempts, the total wall-clock budget caps the whole sequence.

    We can't easily simulate 1200s of wall time in a test; instead, we
    monkeypatch `time.monotonic` (using pytest's monkeypatch fixture for
    automatic cleanup so the patch can't leak into adjacent tests) and
    verify the loop aborts after the deadline regardless of remaining
    retry budget.
    """
    import efterlev.llm.bedrock_client as bedrock_module

    # Build a clock that jumps past the deadline on the second tick.
    # First call computes deadline (T=0, deadline=1200); second call
    # is the loop pre-flight check (T=1201 > 1200 → break).
    fake_now = [0.0]

    def fake_monotonic() -> float:
        v = fake_now[0]
        fake_now[0] += _MAX_TOTAL_WALL_SECONDS + 1.0
        return v

    monkeypatch.setattr(bedrock_module.time, "monotonic", fake_monotonic)

    client, fake = _bedrock_with_mock(
        # Throttling is normally retried 3x, but the wall-clock cap
        # should stop us at attempt 0 (no converse calls — pre-flight
        # check fires before the first attempt).
        canned=[_client_error("ThrottlingException")] * 3,
    )
    with pytest.raises(AgentError):
        client.complete(system="s", messages=[LLMMessage("x")], model="m")
    # Deadline check fires on first iteration → break before any
    # converse call. (Real-world: deadline check on iter 2 after iter 1
    # already completed, so 1 call would be expected; this test's
    # extreme clock jump models the worst-case "deadline already past
    # before we even started" path.)
    assert fake.converse.call_count == 0


def test_v0_1_37_is_read_timeout_classifier() -> None:
    """`_is_read_timeout` distinguishes ReadTimeoutError from other
    retryable errors so callers can apply distinct retry budgets."""
    from botocore.exceptions import ConnectTimeoutError, EndpointConnectionError

    assert _is_read_timeout(_read_timeout_error()) is True
    # Other retryable errors are NOT classified as read-timeout.
    assert _is_read_timeout(ConnectTimeoutError(endpoint_url="x")) is False
    assert _is_read_timeout(EndpointConnectionError(endpoint_url="x")) is False
    assert _is_read_timeout(_client_error("ThrottlingException")) is False
    assert _is_read_timeout(RuntimeError("???")) is False


def test_v0_1_37_non_read_timeout_uses_full_retry_budget() -> None:
    """Non-ReadTimeout retryable errors (Throttling, 5xx) still get the
    full _MAX_RETRIES budget. The ReadTimeout cap is targeted, not
    a global retry-budget reduction."""
    client, fake = _bedrock_with_mock(
        canned=[
            _client_error("ThrottlingException"),
            _client_error("ThrottlingException"),
            _converse_response("ok"),
        ],
    )
    resp = client.complete(system="s", messages=[LLMMessage("x")], model="m")
    assert resp.text == "ok"
    assert fake.converse.call_count == 3
