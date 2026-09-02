"""`CompletedRequest.build_request_summary` — the ONE builder for the aggregated
per-request summary, shared by the legacy `cx_user_request` row (`to_storage_dict`)
and the runtime spine's `request_summary` NOTE. These lock the status mapping (the
correctness-critical bit: a resumable suspend must NOT read as a clean completion) and
the one-source-of-truth invariant that keeps the two consumers from drifting apart
while cx_user_request is retired onto the spine.
"""

from __future__ import annotations

import types

from matrx_ai.config.usage_config import TokenUsage
from matrx_ai.orchestrator.requests import CompletedRequest


def _cr(status: str | None = None, error=None, error_type: str | None = None) -> CompletedRequest:
    """A minimal CompletedRequest — build_request_summary only reads request identity,
    usage_history (empty ⇒ zero cost), and metadata, so a stub request suffices."""
    req = types.SimpleNamespace(
        request_id="r1", conversation_id="c1", user_id="u1", usage_history=[], metadata={}
    )
    cr = CompletedRequest(request=req, iterations=1, final_response=None)  # type: ignore[arg-type]
    if status is not None:
        cr.metadata["status"] = status
    if error is not None:
        cr.metadata["error"] = error
    if error_type is not None:
        cr.metadata["error_type"] = error_type
    return cr


def test_summary_carries_cached_tokens_field():
    s = _cr().build_request_summary()
    assert "total_cached_tokens" in s  # parity with cx_user_request.total_cached_tokens


def test_unknown_child_cost_propagates_to_parent_total():
    cr = _cr()
    cr.request.usage_history = [
        TokenUsage(
            input_tokens=0,
            output_tokens=0,
            matrx_model_name="gpt-image-2",
            api="openai",
            metadata={"cost_reconciliation": "unknown_missing_provider_usage"},
        )
    ]

    summary = cr.build_request_summary()

    assert summary["total_cost"] is None
    assert summary["metadata"]["cost_reconciliation"] == "incomplete_child_costs"
    assert summary["metadata"]["known_cost_subtotal"] == 0


def test_missing_iteration_usage_propagates_unknown_cost():
    summary = _cr().build_request_summary()

    assert summary["total_cost"] is None
    assert summary["metadata"]["cost_reconciliation"] == "incomplete_child_costs"


def test_default_status_is_completed():
    assert _cr().build_request_summary()["status"] == "completed"
    assert _cr(status="stop").build_request_summary()["status"] == "completed"


def test_failed_status_maps_to_failed_with_error():
    s = _cr(status="failed", error={"error_type": "provider_500", "message": "boom"}).build_request_summary()
    assert s["status"] == "failed"
    assert s["error"] == {"error_type": "provider_500", "message": "boom"}


def test_cancelled_status_maps_to_cancelled():
    assert _cr(status="cancelled").build_request_summary()["status"] == "cancelled"


def test_every_resumable_suspend_maps_to_paused():
    # A run WAITING on the client/user is 'paused' — never a silent 'completed'.
    for raw in CompletedRequest.RESUMABLE_SUSPEND_STATUSES:
        assert _cr(status=raw).build_request_summary()["status"] == "paused", raw


def test_truncated_is_resumable_and_maps_to_paused_with_error_preserved():
    # "truncated" = the model hit its output-token limit (executor.py sets
    # metadata error + error_type="truncated_response"). It is limit-hit +
    # RESUMABLE → 'paused', NEVER 'completed' (the old else-branch mapping
    # recorded a real limit-hit as a clean success). The structured error
    # detail must survive onto the summary.
    assert "truncated" in CompletedRequest.RESUMABLE_SUSPEND_STATUSES
    s = _cr(
        status="truncated",
        error="Response truncated: model hit the output token limit (model=m, max_output_tokens=100)",
        error_type="truncated_response",
    ).build_request_summary()
    assert s["status"] == "paused"
    assert s["error"] == {
        "error_type": "truncated_response",
        "message": "Response truncated: model hit the output token limit (model=m, max_output_tokens=100)",
    }


def test_paused_without_error_carries_no_error_field():
    # A clean suspend (delegated client tool etc.) has no error payload —
    # the summary must not invent one.
    s = _cr(status="suspended_awaiting_client").build_request_summary()
    assert "error" not in s


def test_failed_bare_string_error_with_type_is_lifted_to_structured():
    s = _cr(status="failed", error="boom", error_type="provider_500").build_request_summary()
    assert s["status"] == "failed"
    assert s["error"] == {"error_type": "provider_500", "message": "boom"}


def test_storage_dict_delegates_to_the_one_builder(monkeypatch):
    # to_storage_dict must consume build_request_summary verbatim — one source of truth,
    # so cx_user_request and the spine NOTE can never diverge. Guards a future re-inline:
    # whatever the builder returns is exactly what lands in the storage dict's user_request.
    cr = _cr()
    sentinel = {"__sentinel__": "one-source-of-truth"}
    monkeypatch.setattr(cr, "build_request_summary", lambda: sentinel)
    # Stub the rest of the storage surface the method touches before the user_request line.
    cr.request.config = types.SimpleNamespace(
        to_storage_dict=lambda: {
            "model": "m", "system_instruction": None, "config": {}, "messages": []
        }
    )
    cr.request.parent_conversation_id = None
    cr.request.timing_history = []
    cr.request.tool_call_history = []
    assert cr.to_storage_dict()["user_request"] is sentinel
