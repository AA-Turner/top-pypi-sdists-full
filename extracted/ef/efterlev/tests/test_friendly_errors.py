"""Tests for the friendly-error layer at the CLI/LLM boundary.

Priority 3.2 (2026-04-28). The user-experience win here is small but
high-leverage: instead of dumping a 600-line traceback on a missing
API key, the CLI prints one short error line + one hint line + exits
non-zero. Tests verify the mapping from typed SDK exceptions to
friendly text and the context-manager behavior at the agent boundary.
"""

from __future__ import annotations

import pytest
import typer

from efterlev.cli.friendly_errors import format_llm_error, friendly_llm_error_handler

# --- format_llm_error mapping ----------------------------------------------


def _api_error_with_status(status_code: int, message: str = "test") -> Exception:
    """Construct a real anthropic.APIError-shaped exception for testing.
    The SDK exception classes inherit from `APIError`; we instantiate a
    matching subtype based on status_code."""
    import anthropic
    from anthropic._exceptions import APIStatusError

    # Construct via the SDK's status-code-to-class mapping.
    cls_for_status = {
        400: anthropic.BadRequestError,
        401: anthropic.AuthenticationError,
        403: anthropic.PermissionDeniedError,
        404: anthropic.NotFoundError,
        429: anthropic.RateLimitError,
        500: anthropic.InternalServerError,
    }
    cls = cls_for_status.get(status_code, APIStatusError)

    # Build the response object the SDK expects.
    import httpx

    response = httpx.Response(
        status_code, text=message, request=httpx.Request("POST", "https://api.anthropic.com/v1")
    )
    return cls(message=message, response=response, body=None)


def test_authentication_error_maps_to_api_key_message() -> None:
    exc = _api_error_with_status(401, "bad key")
    msg, hint = format_llm_error(exc)
    assert "ANTHROPIC_API_KEY is missing or invalid" in msg
    assert hint is not None
    assert "console.anthropic.com" in hint
    assert "efterlev doctor" in hint


def test_permission_denied_maps_to_permission_message() -> None:
    exc = _api_error_with_status(403, "forbidden")
    msg, hint = format_llm_error(exc)
    assert "permission denied" in msg
    assert hint is not None
    assert "key has access to the requested model" in hint


def test_rate_limit_maps_to_rate_limit_message() -> None:
    exc = _api_error_with_status(429, "rate limited")
    msg, hint = format_llm_error(exc)
    assert "Rate-limited" in msg
    assert hint is not None
    assert "Wait a minute" in hint


def test_not_found_maps_to_model_not_found() -> None:
    exc = _api_error_with_status(404, "no such model")
    msg, hint = format_llm_error(exc)
    assert "Model not found" in msg
    assert hint is not None
    assert "claude-opus-4-7" in hint


def test_bad_request_maps_to_request_malformed() -> None:
    exc = _api_error_with_status(400, "bad request")
    msg, _hint = format_llm_error(exc)
    assert "rejected the request as malformed" in msg


def test_internal_server_error_maps_to_5xx_message() -> None:
    exc = _api_error_with_status(500, "boom")
    msg, hint = format_llm_error(exc)
    assert "internal server error" in msg
    assert hint is not None
    assert "status.anthropic.com" in hint


def test_unknown_exception_falls_through_to_str() -> None:
    """Non-anthropic exceptions return their str() unchanged with no hint."""
    exc = ValueError("unexpected thing")
    msg, hint = format_llm_error(exc)
    assert msg == "unexpected thing"
    assert hint is None


# --- friendly_llm_error_handler context manager ---------------------------


def test_handler_passes_through_when_no_exception() -> None:
    """Happy path: the context manager yields normally with no rewrite."""
    sentinel = []
    with friendly_llm_error_handler():
        sentinel.append("ran")
    assert sentinel == ["ran"]


def test_handler_converts_authentication_error_to_typer_exit(
    capsys: pytest.CaptureFixture[str],
) -> None:
    """An anthropic.AuthenticationError raises typer.Exit(1) and prints a
    friendly two-line message (error + hint) on stderr."""
    exc = _api_error_with_status(401, "bad key")
    with pytest.raises(typer.Exit) as exit_info, friendly_llm_error_handler():
        raise exc
    assert exit_info.value.exit_code == 1

    out = capsys.readouterr()
    assert "error: ANTHROPIC_API_KEY" in out.err
    assert "hint:" in out.err
    assert "console.anthropic.com" in out.err
    # No raw SDK class name / traceback shape in stderr — the friendly
    # message uses "HTTP 401" naturally but never the SDK class name.
    assert "AuthenticationError" not in out.err
    # Original exception is chained — preserves debuggability for
    # callers that introspect __cause__.
    assert exit_info.value.__cause__ is exc or exit_info.value.__context__ is exc


def test_handler_passes_non_anthropic_errors_unchanged() -> None:
    """A non-LLM exception (real bug) propagates with full traceback so
    the user can debug it normally. The friendly layer is for *known*
    boundary failures only."""
    with pytest.raises(ValueError, match="real bug"), friendly_llm_error_handler():
        raise ValueError("real bug")


def test_v0_1_38_handler_unwraps_chained_sdk_error_via_cause(
    capsys: pytest.CaptureFixture[str],
) -> None:
    """v0.1.38 fix for S2 (quickstart raw 401): AnthropicClient.complete()
    wraps non-retryable SDK errors as AgentError(...) before re-raising,
    so by the time the exception reaches the handler the outer type is
    AgentError — NOT anthropic.APIError. Pre-v0.1.38 the handler's
    `isinstance(e, APIError)` check failed against the wrapping
    AgentError and the user saw the raw 401 traceback instead of the
    friendly message. v0.1.38 walks the __cause__ chain to find the
    underlying SDK error.
    """
    from efterlev.errors import AgentError

    sdk_exc = _api_error_with_status(401, "bad key")
    wrapped = AgentError("anthropic completion failed: ...")
    wrapped.__cause__ = sdk_exc

    with pytest.raises(typer.Exit) as exit_info, friendly_llm_error_handler():
        raise wrapped
    assert exit_info.value.exit_code == 1

    out = capsys.readouterr()
    assert "error: ANTHROPIC_API_KEY" in out.err
    assert "hint:" in out.err


def test_v0_1_38_handler_unwraps_deeply_chained_sdk_error() -> None:
    """A real raise-chain may have multiple levels (AgentError wrapping
    AgentError wrapping APIError). The handler must walk all the way
    down, not just one level. Lock against shallow-walk regression.
    """
    from efterlev.errors import AgentError

    sdk_exc = _api_error_with_status(401, "bad key")
    inner = AgentError("inner wrap")
    inner.__cause__ = sdk_exc
    outer = AgentError("outer wrap")
    outer.__cause__ = inner

    with pytest.raises(typer.Exit), friendly_llm_error_handler():
        raise outer


def test_v0_1_38_handler_does_not_loop_on_self_referential_cause() -> None:
    """Defensive lock: a malformed exception with a cycle in its
    __cause__ chain (shouldn't happen, but Python permits it) must not
    hang the handler. The walker tracks seen IDs and breaks the cycle.
    """

    class CycleError(Exception):
        pass

    e1 = CycleError("a")
    e2 = CycleError("b")
    e1.__cause__ = e2
    e2.__cause__ = e1

    with pytest.raises(CycleError), friendly_llm_error_handler():
        raise e1
