"""A completed user request never claims "completed" with no finish reason when its
final provider call reported one (false-labels audit item 8).

`persist_completed_request` built the parent row's finish_reason from the request-level
metadata only; on paths that never set it (mandate candidates, sub-agent guards) the
row read status=completed, finish_reason=NULL while its own final chat.request said
`stop` / `tool_calls`. The settled value is the final call's, never invented.
"""

from __future__ import annotations

from matrx_ai.db.persistence import _settled_finish_reason


def test_request_level_value_wins():
    assert _settled_finish_reason({"finish_reason": "stop"}, [{"iteration": 1, "finish_reason": "tool_calls"}]) == "stop"


def test_falls_back_to_the_final_call():
    reqs = [
        {"iteration": 2, "finish_reason": "stop"},
        {"iteration": 1, "finish_reason": "tool_calls"},
    ]
    assert _settled_finish_reason({}, reqs) == "stop"


def test_a_final_call_with_no_reason_stays_unknown():
    # Image models report no finish reason: NULL is the truth, nothing is guessed
    # from an earlier call.
    reqs = [{"iteration": 1, "finish_reason": "tool_calls"}, {"iteration": 2, "finish_reason": None}]
    assert _settled_finish_reason({}, reqs) is None


def test_no_calls_is_none():
    assert _settled_finish_reason({}, []) is None
