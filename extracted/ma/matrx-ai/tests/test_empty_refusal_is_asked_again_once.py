"""A provider refusal that wrote nothing is asked again ONCE, then fails loudly.

Live 2026-10-18: the Studio Debrief on Claude Opus 5.5 came back as a blank
assistant turn (stop_reason=refusal, 0 output tokens) in ~4 of 6 tries. The
engine ended the run quietly with only a warning, so the UI showed an empty
"done". A zero-token refusal is free to re-ask; the second one must be a
terminal error the person can read.
"""

from __future__ import annotations

from matrx_utils.source_guard import stable_source
from types import SimpleNamespace

from matrx_ai.config import TextContent, ThinkingContent, UnifiedMessage
from matrx_ai.config.finish_reason import FinishReason
from matrx_ai.orchestrator import executor
from matrx_ai.orchestrator.recovery_logic import handle_finish_reason, response_has_no_output


def _response(*content, reason=FinishReason.REFUSAL) -> SimpleNamespace:
    return SimpleNamespace(
        finish_reason=reason,
        messages=[UnifiedMessage(role="assistant", content=list(content))],
        raw_response=None,
    )


def _request() -> SimpleNamespace:
    return SimpleNamespace(config=SimpleNamespace(model="m", max_output_tokens=100, tools=None, messages=[]))


def test_empty_refusal_retries_once_then_stops() -> None:
    blank = _response()
    assert response_has_no_output(blank)
    assert handle_finish_reason(blank, _request(), 0, 2) == "retry"
    assert handle_finish_reason(blank, _request(), 1, 2) == "stop"


def test_thinking_only_refusal_counts_as_empty() -> None:
    assert handle_finish_reason(_response(ThinkingContent(text="hm")), _request(), 0, 2) == "retry"


def test_refusal_after_text_is_not_retried() -> None:
    r = _response(TextContent(text="Part of an answer"))
    assert not response_has_no_output(r)
    assert handle_finish_reason(r, _request(), 0, 2) == "stop"


def test_stop_branch_tells_the_person_when_nothing_was_written() -> None:
    src = stable_source(executor)
    assert 'code="refusal_retry"' in src
    assert src.index("if not has_visible_answer and not _response_has_tool_calls(api_response)") < src.index(
        "provider_response_failed"
    )
