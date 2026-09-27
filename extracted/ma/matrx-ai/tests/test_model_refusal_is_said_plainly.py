"""A model refusal is told to the person plainly and is not filed as a platform failure.

2026-09-24: Opus 5.5 refused an ordinary turn ("commit the code and deprecate the
old models") with zero output; the identical turn went through when sent again.
The person was shown "Model stopped with finish reason: refusal" and a vague
"may be a model error" warning, and the refusal was filed in system_error as a
provider failure.
"""

from __future__ import annotations

import pytest

from matrx_ai.config.finish_reason import FinishReason

from test_truncated_response_capture import _run_one_turn


@pytest.mark.asyncio
async def test_a_refusal_is_said_plainly_and_kept_out_of_the_error_queue(monkeypatch) -> None:
    run = await _run_one_turn(monkeypatch, str(FinishReason.from_anthropic("refusal")))

    [warning] = run["warnings"]
    assert warning.code == "model_refusal"
    assert "declined" in warning.user_message
    assert "again" in warning.user_message

    assert not [c for c in run["captured"] if c.get("kind") == "provider_response_failed"]

    [final] = run["finalized"]
    saved = final["metadata"]
    assert saved["finish_reason"] == "refusal"
    assert "finish reason" not in saved["error"]
    assert "declined" in saved["error"]


@pytest.mark.asyncio
async def test_an_unexplained_stop_is_still_filed_for_operators(monkeypatch) -> None:
    run = await _run_one_turn(monkeypatch, str(FinishReason.MALFORMED_FUNCTION_CALL))

    assert [c for c in run["captured"] if c.get("kind") == "provider_response_failed"]
