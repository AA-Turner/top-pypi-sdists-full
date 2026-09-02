"""ToolError.from_exception — the primitive that keeps a tool's stack alive.

Pairs with test_no_traceback_destroying_tool_errors.py (which forbids the
antipattern) — this pins that the sanctioned replacement actually works.
"""
from __future__ import annotations

import pytest

from matrx_ai.tools.models import ToolError


def _raise_deep() -> None:
    def inner() -> None:
        raise ValueError("invalid input for query argument $5: 0 (expected str, got int)")

    inner()


def test_from_exception_captures_the_real_stack():
    try:
        _raise_deep()
    except ValueError as exc:
        err = ToolError.from_exception(exc, error_type="search_failed", message=f"RAG search failed: {exc}")

    assert err.error_type == "search_failed"
    assert "expected str, got int" in err.message
    # The whole point: the stack survives, and it names the frames.
    assert err.traceback is not None
    assert "_raise_deep" in err.traceback
    assert "inner" in err.traceback
    assert "ValueError" in err.traceback


def test_from_exception_defaults_message_to_type_and_str():
    try:
        raise KeyError("missing")
    except KeyError as exc:
        err = ToolError.from_exception(exc, error_type="boom")
    assert err.message.startswith("KeyError")
    assert err.traceback is not None


def test_from_exception_preserves_the_other_kwargs():
    try:
        raise RuntimeError("nope")
    except RuntimeError as exc:
        err = ToolError.from_exception(
            exc,
            error_type="execution",
            message="Web search failed",
            is_retryable=True,
            suggested_action="Try again.",
        )
    assert err.is_retryable is True
    assert err.suggested_action == "Try again."
    assert err.traceback is not None


def test_to_agent_message_surfaces_the_traceback():
    """The model gets the technical details too — same contract the executor's
    own exception handler has always had."""
    try:
        _raise_deep()
    except ValueError as exc:
        err = ToolError.from_exception(exc, error_type="search_failed", message="RAG search failed")
    msg = err.to_agent_message()
    assert "TOOL ERROR [search_failed]" in msg
    assert "Technical details:" in msg
    assert "_raise_deep" in msg


@pytest.mark.parametrize("exc_type", [ValueError, RuntimeError, TypeError])
def test_from_exception_works_for_any_exception_type(exc_type):
    try:
        raise exc_type("x")
    except Exception as exc:
        err = ToolError.from_exception(exc, error_type="t")
    assert exc_type.__name__ in err.traceback
