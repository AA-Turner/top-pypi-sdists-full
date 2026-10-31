"""A failed AI turn fails the step with the friendly sentence AND the real exception behind it.

The provider error translators turn anything they do not recognise — a plain ``ValueError``
raised by an adapter — into "An unexpected <provider> error occurred.". That sentence is right
for a person, but it was all a step failure carried: the 2026-10-29 voice changer ("the audio part
has no bytes") and moderation ("extraction agent ... has no labels") failures read as unexplained.
The turn's real classifier runs here on a really raised exception; the funnel returns what the
executor returns on that path (``metadata.error`` = the person sentence, ``terminal_exception``).
"""

from __future__ import annotations

import dataclasses
from typing import Any

import pytest
from matrx_graph.types.result import Failure

from matrx_ai.config import UnifiedResponse
from matrx_ai.graph_nodes.tests.test_node_handlers_execute import _ctx
from matrx_ai.providers.errors import classify_elevenlabs_error, classify_openai_error


@dataclasses.dataclass
class _FailedTurn:
    final_response: Any
    metadata: dict[str, Any]
    terminal_exception: BaseException | None = None
    total_usage: Any = None


def _raise_from_adapter() -> ValueError:
    try:
        raise ValueError("[ElevenLabs Voice Changer] the audio part has no bytes and no resolvable location")
    except ValueError as exc:
        return exc


@pytest.mark.parametrize("classify", [classify_elevenlabs_error, classify_openai_error])
async def test_the_step_failure_carries_the_real_exception_and_its_traceback(monkeypatch, classify):
    from matrx_ai.graph_nodes.voice_to_voice_action import VoiceToVoiceInput, ai_voice_to_voice
    from matrx_ai.orchestrator import executor

    exc = _raise_from_adapter()
    info = classify(exc)
    assert info.user_message.startswith("An unexpected")  # the person sentence stays generic

    async def _failed(*_a: Any, **_k: Any) -> Any:
        return _FailedTurn(
            final_response=UnifiedResponse(messages=[]),
            metadata={"status": "failed", "error": info.user_message, "error_type": info.error_type},
            terminal_exception=exc,
        )

    monkeypatch.setattr(executor, "execute_ai_request", _failed)
    result = await ai_voice_to_voice(_ctx(), VoiceToVoiceInput(audio_source="https://x.test/a.mp3"))
    assert isinstance(result, Failure)
    assert info.user_message in result.error.message
    assert result.error.details["cause"] == (
        "ValueError: [ElevenLabs Voice Changer] the audio part has no bytes and no resolvable location"
    )
    assert "_raise_from_adapter" in (result.error.technical or "")  # the raise site, from the traceback


async def test_a_turn_with_no_exception_keeps_the_old_shape(monkeypatch):
    from matrx_ai.graph_nodes.moderation_action import ModerateInput, ai_moderate
    from matrx_ai.orchestrator import executor

    async def _failed(*_a: Any, **_k: Any) -> Any:
        return _FailedTurn(final_response=UnifiedResponse(messages=[]), metadata={"status": "failed", "error": "quota"})

    monkeypatch.setattr(executor, "execute_ai_request", _failed)
    result = await ai_moderate(_ctx(), ModerateInput(text="t"))
    assert isinstance(result, Failure) and result.error.details["cause"] is None and result.error.technical is None
