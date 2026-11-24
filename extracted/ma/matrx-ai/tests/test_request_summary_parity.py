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


def _cr(status: str | None = None, error=None, error_type: str | None = None, **extra) -> CompletedRequest:
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
    cr.metadata.update(extra)
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
    # A run WAITING on a client-run tool or a person is 'paused' — never a silent 'completed'.
    for raw in CompletedRequest.RESUMABLE_SUSPEND_STATUSES:
        assert _cr(status=raw).build_request_summary()["status"] == "paused", raw


def test_a_reply_cut_at_its_length_limit_finishes_the_run_marked():
    """Q-15 X3 (2026-11-18, execution 975f9e08): a reply cut at its output-token limit was
    saved 'paused' and the spine parked at WAITING_INPUT, yet nothing resumes it (/resume
    refuses it; "continue" is a new turn) — the conversation stayed paused and the send
    button spun. It FINISHES: 'completed', the structured error kept, the stop named."""
    assert "truncated" not in CompletedRequest.RESUMABLE_SUSPEND_STATUSES
    assert "truncated" in CompletedRequest.FINISHED_WITH_STOP_STATUSES
    for sub_agent in (False, True):
        extra = {CompletedRequest.CALLER_RESUMES_KEY: True} if sub_agent else {}
        s = _cr(
            status="truncated",
            error="Response truncated: model hit the output token limit (model=m, max_output_tokens=100)",
            error_type="truncated_response",
            **extra,
        ).build_request_summary()
        assert s["status"] == "completed"
        assert s["error"] == {
            "error_type": "truncated_response",
            "message": "Response truncated: model hit the output token limit (model=m, max_output_tokens=100)",
        }
        assert s["metadata"]["stop_status"] == "truncated", "a reload must still say it was cut off"


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


def test_a_paused_or_stopped_turn_saves_which_stop_it_was():
    """A reload must say WHY a turn stopped. The loop guard and the step limit both save
    ``error_type = tool_loop_stalled`` and both read ``paused``; without the stop's own name on the
    saved row a reloaded chat can only say "Stopped before finishing" for either (2026-11-18)."""
    for stop in CompletedRequest.RESUMABLE_SUSPEND_STATUSES:
        summary = _cr(stop).build_request_summary()
        assert summary["status"] == "paused"
        assert summary["metadata"]["stop_status"] == stop, f"{stop}: the saved row does not name its stop"
    for stop in CompletedRequest.FINISHED_WITH_STOP_STATUSES:
        summary = _cr(stop).build_request_summary()
        assert summary["status"] == "completed", f"{stop}: nothing resumes it, so the run ends"
        assert summary["metadata"]["stop_status"] == stop, f"{stop}: the saved row does not name its stop"


def test_a_finished_or_failed_turn_saves_no_stop_name():
    for status in (None, "failed", "cancelled", "completed_with_warning"):
        assert "stop_status" not in _cr(status).build_request_summary()["metadata"]
