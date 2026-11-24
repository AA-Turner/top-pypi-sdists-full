"""Every paid media node that gets no artifact names the REAL cause (shared.no_media_reason).

Image nodes already did (e68a653c1). A chat model the free-tier swap substituted answers in
prose; the video / speech / music / sound-effect / voice-to-voice / moderation steps used to
say only "returned no audio/videos/verdict" and name a model that never ran.
"""

from __future__ import annotations

import dataclasses
from typing import Any

import pytest
from matrx_graph.types.result import Failure

from matrx_ai.config import UnifiedMessage, UnifiedResponse
from matrx_ai.config.finish_reason import FinishReason
from matrx_ai.config.unified_content import TextContent
from matrx_ai.graph_nodes.tests.test_node_handlers_execute import _ctx

ANSWER = "Sorry, I can only reply in text and cannot produce that."


@dataclasses.dataclass
class _Ran:
    config: Any


@dataclasses.dataclass
class _Completed:
    final_response: Any
    total_usage: Any = None
    metadata: dict[str, Any] = dataclasses.field(default_factory=dict)
    request: Any = None


def _text_only_swapped_completed() -> _Completed:
    response = UnifiedResponse(
        messages=[UnifiedMessage(role="assistant", content=[TextContent(text=ANSWER)])],
        finish_reason=FinishReason.STOP,
    )
    config = type("Cfg", (), {})()
    config.model = "chat-model-that-ran"
    config.metadata = {"model_swap_reason": "free_tier"}
    return _Completed(final_response=response, request=_Ran(config=config))


def _runs() -> dict[str, Any]:
    from matrx_ai.graph_nodes.moderation_action import ModerateInput, ai_moderate
    from matrx_ai.graph_nodes.music_action import GenerateMusicInput, ai_generate_music
    from matrx_ai.graph_nodes.sound_effect_action import (
        GenerateSoundEffectInput,
        ai_generate_sound_effect,
    )
    from matrx_ai.graph_nodes.tts_action import TextToSpeechInput, ai_text_to_speech
    from matrx_ai.graph_nodes.video_action import GenerateVideoInput, ai_generate_video
    from matrx_ai.graph_nodes.voice_to_voice_action import VoiceToVoiceInput, ai_voice_to_voice

    return {
        "video": lambda: ai_generate_video(_ctx(), GenerateVideoInput(model="req-model", prompt="p")),
        "tts": lambda: ai_text_to_speech(_ctx(), TextToSpeechInput(model="req-model", text="hi")),
        "music": lambda: ai_generate_music(_ctx(), GenerateMusicInput(model="req-model", prompt="p")),
        "sound_effect": lambda: ai_generate_sound_effect(
            _ctx(), GenerateSoundEffectInput(model="req-model", prompt="p")
        ),
        "voice_to_voice": lambda: ai_voice_to_voice(
            _ctx(), VoiceToVoiceInput(model="req-model", audio_source="https://x.test/a.mp3")
        ),
        "moderation": lambda: ai_moderate(_ctx(), ModerateInput(model="req-model", text="hello")),
    }


@pytest.mark.parametrize(
    "node", ["video", "tts", "music", "sound_effect", "voice_to_voice", "moderation"]
)
async def test_no_artifact_names_the_model_that_ran_and_what_it_said(monkeypatch, node):
    from matrx_ai.orchestrator import executor

    async def _fake(*_a: Any, **_k: Any) -> Any:
        return _text_only_swapped_completed()

    monkeypatch.setattr(executor, "execute_ai_request", _fake)
    result = await _runs()[node]()
    assert isinstance(result, Failure), result
    message = result.error.message
    assert "chat-model-that-ran" in message and "free_tier" in message, message
    assert "cannot produce that" in message, message
    assert result.error.details["ran_model"] == "chat-model-that-ran"
