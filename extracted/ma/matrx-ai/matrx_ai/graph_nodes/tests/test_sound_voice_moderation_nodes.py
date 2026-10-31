"""Create Sound Effect, Voice to Voice and Check Content Safety send what they claim and return what the provider made.

Thin nodes over the ``execute_ai_request`` funnel; the funnel is replaced by a recorder (the same one the other
Direct AI media steps use), each node's body runs for real, and the tests read the UnifiedConfig it built and
the output it shaped from a real ``UnifiedResponse``.
"""

from __future__ import annotations

import json
from typing import Any

import pytest
from matrx_graph.types.result import Failure, Success

from matrx_ai.config import AudioContent, TextContent, UnifiedMessage, UnifiedResponse
from matrx_ai.config.finish_reason import FinishReason
from matrx_ai.graph_nodes.moderation_action import ModerateInput, ai_moderate
from matrx_ai.graph_nodes.sound_effect_action import GenerateSoundEffectInput, ai_generate_sound_effect
from matrx_ai.graph_nodes.tests.test_direct_ai_media_nodes import DURABLE, FILE_ID, _Completed, _record, _response
from matrx_ai.graph_nodes.tests.test_node_handlers_execute import _ctx
from matrx_ai.graph_nodes.voice_to_voice_action import VoiceToVoiceInput, ai_voice_to_voice, audio_part


async def test_sound_effect_asks_for_the_length_and_returns_the_audio_file(monkeypatch):
    seen = _record(monkeypatch, _response(AudioContent(file_id="fx", url=DURABLE, mime_type="audio/mpeg", duration_ms=2000)))
    result = await ai_generate_sound_effect(_ctx(), GenerateSoundEffectInput(prompt="glass breaking", duration_seconds=2))
    assert isinstance(result, Success), result
    assert result.result.file_id == "fx" and result.result.audio_url == DURABLE
    assert seen[0].model == "eleven_text_to_sound_v2" and seen[0].duration_seconds == 2


async def test_sound_effect_declined_by_the_provider_says_so(monkeypatch):
    _record(monkeypatch, _response(finish=FinishReason.CONTENT_FILTER))
    result = await ai_generate_sound_effect(_ctx(), GenerateSoundEffectInput(prompt="x"))
    assert isinstance(result, Failure) and result.error.code == "sound_effect_declined"


def test_voice_to_voice_takes_a_file_id_as_an_id_and_inline_audio_as_base64():
    assert audio_part(VoiceToVoiceInput(file_id=FILE_ID)) == {"type": "audio", "file_id": FILE_ID}
    assert audio_part(VoiceToVoiceInput(audio_source="data:audio/wav;base64,UklGRg==")) == {
        "type": "audio", "mime_type": "audio/wav", "base64_data": "UklGRg=="}
    assert audio_part(VoiceToVoiceInput(audio_source="https://x.test/a.mp3")) == {"type": "audio", "url": "https://x.test/a.mp3"}
    with pytest.raises(ValueError, match="exactly one"):
        VoiceToVoiceInput(file_id=FILE_ID, audio_source="https://x.test/a.mp3")


async def test_voice_to_voice_sends_the_speech_and_voice_and_returns_the_new_audio(monkeypatch):
    seen = _record(monkeypatch, _response(AudioContent(file_id="out", url=DURABLE, mime_type="audio/mpeg", duration_ms=3000)))
    result = await ai_voice_to_voice(_ctx(), VoiceToVoiceInput(file_id=FILE_ID, voice="voice-9"))
    assert isinstance(result, Success), result
    assert result.result.file_id == "out" and result.result.duration_seconds == 3.0
    part = seen[0].messages[0].content[0]
    assert isinstance(part, AudioContent) and part.file_id == FILE_ID
    assert seen[0].tts_voice == "voice-9" and seen[0].model == "eleven_multilingual_sts_v2"


async def test_voice_to_voice_with_no_voice_leaves_it_to_the_catalog_default(monkeypatch):
    seen = _record(monkeypatch, _response(AudioContent(file_id="out", url=DURABLE, mime_type="audio/mpeg")))
    await ai_voice_to_voice(_ctx(), VoiceToVoiceInput(audio_source="https://x.test/a.mp3"))
    assert not seen[0].tts_voice


def _verdict_response(verdict: dict[str, Any], *, in_metadata: bool) -> UnifiedResponse:
    meta = {"moderation": verdict} if in_metadata else {}
    return UnifiedResponse(
        messages=[UnifiedMessage(role="assistant", content=[TextContent(text=json.dumps(verdict))], metadata=meta)],
        finish_reason=FinishReason.STOP,
    )


@pytest.mark.parametrize("in_metadata", [True, False])
async def test_moderation_returns_a_verdict_a_branch_can_route_on(monkeypatch, in_metadata):
    verdict = {"flagged": True, "model": "omni-moderation-latest", "categories": [
        {"name": "violence", "flagged": False, "score": 0.1},
        {"name": "harassment", "flagged": True, "score": 0.9}]}
    seen = _record(monkeypatch, _verdict_response(verdict, in_metadata=in_metadata))
    result = await ai_moderate(_ctx(), ModerateInput(text="you are awful"))
    assert isinstance(result, Success), result
    out = result.result
    assert out.flagged is True and out.flagged_categories == ["harassment"]
    assert out.top_category == "harassment" and out.top_score == pytest.approx(0.9)
    assert [c.name for c in out.categories] == ["harassment", "violence"]
    assert seen[0].model == "omni-moderation-latest"


async def test_moderation_without_a_verdict_fails_by_name(monkeypatch):
    _record(monkeypatch, _response(TextContent(text="hello")))
    result = await ai_moderate(_ctx(), ModerateInput(text="x"))
    assert isinstance(result, Failure) and result.error.code == "moderation_failed"


@pytest.mark.parametrize("node", ["sfx", "v2v", "moderate"])
async def test_a_failed_turn_fails_the_step_with_the_providers_own_reason(monkeypatch, node):
    from matrx_ai.orchestrator import executor

    async def _failed(*_a: Any, **_k: Any) -> Any:
        return _Completed(final_response=UnifiedResponse(messages=[]),
                          metadata={"status": "failed", "error": "quota exceeded", "error_type": "quota"})

    monkeypatch.setattr(executor, "execute_ai_request", _failed)
    run = {
        "sfx": lambda: ai_generate_sound_effect(_ctx(), GenerateSoundEffectInput(prompt="p")),
        "v2v": lambda: ai_voice_to_voice(_ctx(), VoiceToVoiceInput(file_id=FILE_ID)),
        "moderate": lambda: ai_moderate(_ctx(), ModerateInput(text="t")),
    }[node]
    result = await run()
    assert isinstance(result, Failure) and "quota exceeded" in result.error.message
