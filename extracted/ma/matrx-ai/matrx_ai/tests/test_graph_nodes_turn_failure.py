"""Tests: a failed AI turn must FAIL the graph node, never pass as success.

Found live 2026-07-04: a provider 400 inside ``ai.agent.start`` produced a
CompletedRequest with ``metadata.status="failed"`` (the HTTP-stream contract),
``normalize_completed`` converted it into an empty-but-valid result, and the
workflow completed green with an empty answer downstream. The fix raises
``AiTurnFailedError`` from the one funnel every graph-action wrapper uses.

Run with:  python -m pytest packages/matrx-ai/matrx_ai/tests/test_graph_nodes_turn_failure.py -v
"""

from __future__ import annotations

from types import SimpleNamespace

import pytest

from matrx_ai.graph_nodes.shared import AiTurnFailedError, normalize_completed


def _completed(metadata: dict | None) -> SimpleNamespace:
    """Minimal CompletedRequest stand-in — normalize_completed is getattr-based."""
    return SimpleNamespace(
        request=None,
        final_response=None,
        total_usage=None,
        timing_stats={},
        tool_call_stats={},
        iterations=1,
        metadata=metadata or {},
    )


def test_failed_status_raises():
    completed = _completed(
        {
            "status": "failed",
            "error": "Error code: 400 - `temperature` is deprecated for this model.",
            "error_type": "invalid_request_error",
        }
    )
    with pytest.raises(AiTurnFailedError) as exc:
        normalize_completed(completed)
    msg = str(exc.value)
    assert "failed" in msg
    assert "temperature" in msg
    assert "invalid_request_error" in msg


@pytest.mark.parametrize("status", ["paused_loop_guard", "max_iterations_exceeded"])
def test_loop_guard_statuses_raise(status):
    with pytest.raises(AiTurnFailedError):
        normalize_completed(_completed({"status": status}))


def test_failed_status_without_detail_still_raises():
    with pytest.raises(AiTurnFailedError):
        normalize_completed(_completed({"status": "failed"}))


def test_success_and_truncated_do_not_raise():
    assert normalize_completed(_completed({})).iterations == 1
    assert normalize_completed(_completed(None)).iterations == 1
    # A truncated turn carries real content — it flows through like the chat path.
    assert normalize_completed(_completed({"status": "truncated"})).iterations == 1
