"""Every provider stop is named for what it is, and a delivered answer stands.

Live 2026-10-07 (user_request d47c434d… / a642b45f…, Gemini 3.8 Flash): a
student asked for her own textbook definitions, unchanged, as flashcards.
Gemini ended with RECITATION after the whole answer had streamed. The platform
said "stopped by the provider's content-safety filters ... try rephrasing" and
recorded the request ``failed`` over a complete answer.

These run the real executor stop path (tests/test_truncated_response_capture.py
harness) and the real request-summary mapping — no classifier is mocked.
"""

from __future__ import annotations

from types import SimpleNamespace

import pytest
from test_truncated_response_capture import _run_one_turn

from matrx_ai.config.finish_reason import FinishReason, provider_stop
from matrx_ai.config.message_config import TextContent
from matrx_ai.orchestrator.requests import CompletedRequest


@pytest.mark.asyncio
async def test_recitation_after_a_delivered_answer_is_named_and_the_answer_stands(
    monkeypatch,
) -> None:
    run = await _run_one_turn(monkeypatch, str(FinishReason.from_google("RECITATION")))

    [warning] = run["warnings"]
    assert warning.code == "provider_recitation_stop"
    assert "safety" not in warning.user_message
    assert "word for word" in warning.user_message
    assert warning.metadata["answer_kept"] is True

    # Expected provider control flow: never filed as a platform failure.
    assert not [c for c in run["captured"] if c.get("kind") == "provider_response_failed"]
    # A warning decorates a delivered answer; it never invalidates it.
    assert run["errors"] == []

    [final] = run["finalized"]
    saved = final["metadata"]
    assert saved["status"] == "completed_with_warning"
    assert saved["error_type"] == "provider_recitation_stop"
    assert saved["finish_reason"] == "recitation"


@pytest.mark.asyncio
async def test_recitation_with_nothing_delivered_still_fails_but_says_why(monkeypatch) -> None:
    run = await _run_one_turn(
        monkeypatch, str(FinishReason.RECITATION), content=[TextContent(text="  ")]
    )

    [final] = run["finalized"]
    saved = final["metadata"]
    assert saved["status"] == "failed"
    assert saved["error_type"] == "provider_recitation_stop"
    assert "word for word" in saved["error"]


@pytest.mark.asyncio
async def test_a_real_safety_block_is_still_a_failure_named_as_safety(monkeypatch) -> None:
    run = await _run_one_turn(monkeypatch, str(FinishReason.SAFETY))

    [warning] = run["warnings"]
    assert warning.code == "content_safety_stop"
    [final] = run["finalized"]
    assert final["metadata"]["status"] == "failed"
    assert final["metadata"]["error_type"] == "content_safety_stop"


@pytest.mark.parametrize(
    ("reason", "code", "must_not_say"),
    [
        (FinishReason.LANGUAGE, "unsupported_language_stop", "safety"),
        (FinishReason.SPII, "sensitive_information_stop", "safety"),
        (FinishReason.BLOCKLIST, "blocked_term_stop", "safety"),
        (
            FinishReason.MODEL_CONTEXT_WINDOW_EXCEEDED,
            "context_window_exceeded",
            "content restrictions",
        ),
        (FinishReason.OTHER, "model_stop", "content restrictions"),
    ],
)
def test_no_stop_borrows_another_stops_sentence(reason, code, must_not_say) -> None:
    stop = provider_stop(reason)
    assert stop.code == code
    assert must_not_say not in stop.user_message
    # Only recitation lets a delivered answer stand.
    assert stop.delivered_text_stands is False


def test_completed_with_warning_is_completed_and_keeps_its_warning() -> None:
    req = SimpleNamespace(
        request_id="r1", conversation_id="c1", user_id="u1", usage_history=[], metadata={}
    )
    completed = CompletedRequest(request=req, iterations=1, final_response=None)  # type: ignore[arg-type]
    completed.metadata.update(
        {
            "status": "completed_with_warning",
            "finish_reason": "recitation",
            "error": "The provider stopped this answer because ...",
            "error_type": "provider_recitation_stop",
        }
    )
    summary = completed.build_request_summary()
    assert summary["status"] == "completed"
    assert summary["error"] == {
        "error_type": "provider_recitation_stop",
        "message": "The provider stopped this answer because ...",
    }


def test_openai_content_filter_incomplete_is_not_called_a_token_limit() -> None:
    from matrx_ai.providers.openai.translator import OpenAITranslator

    response = SimpleNamespace(
        id="resp_1",
        model="gpt-test",
        status="incomplete",
        incomplete_details=SimpleNamespace(reason="content_filter"),
        output=[],
        usage=SimpleNamespace(
            input_tokens=10,
            output_tokens=5,
            total_tokens=15,
            input_tokens_details=None,
            output_tokens_details=None,
        ),
    )
    unified = OpenAITranslator().from_openai(response, "gpt-test")
    assert unified.finish_reason == FinishReason.CONTENT_FILTER

    response.incomplete_details = SimpleNamespace(reason="max_output_tokens")
    assert OpenAITranslator().from_openai(response, "gpt-test").finish_reason == (
        FinishReason.MAX_TOKENS
    )
