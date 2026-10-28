"""A provider that stayed overloaded fails the AI step — it is never an answer.

Live 2026-10-27, run 477536f8 (audio.narrate, step ``voice``): Google TTS returned 503 through every retry.
The orchestrator suspended the turn (``suspended_provider_overload`` — resumable in a chat, where a person can
press Retry), ``normalize_completed`` did not count that status as a failure, fell back to the LAST message (the
user's own prompt) as ``final_text``, and the step "succeeded". Run once per key then stored that echo and a
second identical run reused it in 1 s. Inside an unattended workflow step there is nobody to resume it: the
step fails, so its retry ladder applies and nothing is stored for reuse.
"""

from __future__ import annotations

from types import SimpleNamespace

import pytest

from matrx_ai.graph_nodes.shared import (
    AiTurnFailedError,
    normalize_completed,
    normalize_completed_result,
)


def _overloaded() -> SimpleNamespace:
    return SimpleNamespace(
        metadata={
            "status": "suspended_provider_overload",
            "error": "Google is temporarily overloaded (503)",
            "error_type": "provider_overloaded",
            "status_code": 503,
            "retries_exhausted": True,
        },
        total_usage=None,
        request=SimpleNamespace(conversation_id="c", request_id="r"),
        final_response=None,
    )


def test_an_overloaded_provider_fails_the_step_with_its_reason() -> None:
    result = normalize_completed_result(_overloaded())
    assert result.error is not None, "a provider overload must never be a successful step"
    assert result.error.code == "ai_turn_failed"
    assert "overloaded (503)" in result.error.message
    assert result.error.details["status"] == "suspended_provider_overload"


def test_the_raised_door_fails_too() -> None:
    with pytest.raises(AiTurnFailedError, match="suspended_provider_overload"):
        normalize_completed(_overloaded())
