"""The Direct AI media steps send what they claim and return what the provider made.

``ai.image.edit``, ``ai.vision.read`` and ``ai.generate_music`` are thin nodes over the
``execute_ai_request`` funnel. The boundary (that funnel) is replaced by a recorder; each
node's own body runs for real, and the tests read the exact UnifiedConfig it built and
the output it shaped from a real ``UnifiedResponse`` with real content blocks.
"""

from __future__ import annotations

import dataclasses
from typing import Any

import pytest
from matrx_graph.types.result import Failure, Success

from matrx_ai.config import AudioContent, ImageContent, UnifiedMessage, UnifiedResponse
from matrx_ai.config.finish_reason import FinishReason
from matrx_ai.graph_nodes.image_edit_action import EditImageInput, ai_image_edit, image_part
from matrx_ai.graph_nodes.music_action import GenerateMusicInput, ai_generate_music
from matrx_ai.graph_nodes.tests.test_node_handlers_execute import _ctx
from matrx_ai.graph_nodes.vision_action import (
    MODE_INSTRUCTIONS,
    VisionReadInput,
    vision_config_payload,
)

FILE_ID = "11111111-2222-3333-4444-555555555555"
DURABLE = "https://cdn.example.com/out.png"


@dataclasses.dataclass
class _Completed:
    final_response: Any
    total_usage: Any = None
    metadata: dict[str, Any] = dataclasses.field(default_factory=dict)


def _record(monkeypatch: pytest.MonkeyPatch, response: Any) -> list[Any]:
    from matrx_ai.orchestrator import executor

    seen: list[Any] = []

    async def _fake(config: Any, **_k: Any) -> Any:
        seen.append(config)
        return _Completed(final_response=response)

    monkeypatch.setattr(executor, "execute_ai_request", _fake)
    monkeypatch.setattr("matrx_files.is_durable_media_url", lambda u: bool(u) and u == DURABLE)
    return seen


def _response(*blocks: Any, finish: FinishReason = FinishReason.STOP) -> UnifiedResponse:
    return UnifiedResponse(
        messages=[UnifiedMessage(role="assistant", content=list(blocks))], finish_reason=finish
    )


def test_image_part_keeps_a_file_id_as_an_id_and_a_url_as_a_url():
    assert image_part(FILE_ID) == {"type": "image", "file_id": FILE_ID}
    assert image_part("https://x.test/a.png", role="mask") == {
        "type": "image",
        "url": "https://x.test/a.png",
        "role": "mask",
    }
    # A data: URI left in ``url`` reached Gemini as no image at all (live, 2026-10-29).
    assert image_part("data:image/png;base64,QUJD") == {
        "type": "image",
        "mime_type": "image/png",
        "base64_data": "QUJD",
    }
    with pytest.raises(ValueError):
        image_part("  ")


async def test_edit_sends_every_image_and_the_mask_in_one_turn_and_returns_the_file(monkeypatch):
    seen = _record(
        monkeypatch,
        _response(ImageContent(file_id="out-file", url=DURABLE, mime_type="image/png")),
    )
    result = await ai_image_edit(
        _ctx(),
        EditImageInput(
            model="gpt-image-2.5-flare",
            prompt="make the sky purple",
            images=[FILE_ID, "https://x.test/ref.png"],
            mask="https://x.test/mask.png",
            count=2,
        ),
    )
    assert isinstance(result, Success), result
    out = result.result
    assert [i.file_id for i in out.images] == ["out-file"]
    assert out.images[0].url == DURABLE

    config = seen[0]
    blocks = config.messages[0].content
    images = [b for b in blocks if isinstance(b, ImageContent)]
    assert [(b.file_id, b.url, b.role) for b in images] == [
        (FILE_ID, None, None),
        (None, "https://x.test/ref.png", None),
        (None, "https://x.test/mask.png", "mask"),
    ]
    assert blocks[-1].text == "make the sky purple"
    assert config.count == 2


async def test_edit_with_no_image_back_fails_by_name(monkeypatch):
    _record(monkeypatch, _response())
    result = await ai_image_edit(
        _ctx(), EditImageInput(model="m", prompt="p", images=["https://x.test/a.png"])
    )
    assert isinstance(result, Failure)
    assert result.error.code == "edit_failed"


def test_vision_uses_the_mode_default_only_when_the_instruction_is_empty():
    read = vision_config_payload(
        VisionReadInput(model="m", images=[FILE_ID], mode="read_text")
    )
    content = read["messages"][0]["content"]
    assert content[0] == {"type": "image", "file_id": FILE_ID}
    assert content[-1]["text"] == MODE_INSTRUCTIONS["read_text"]
    assert read["temperature"] == 0.0

    own = vision_config_payload(
        VisionReadInput(model="m", images=[FILE_ID], mode="describe", instruction="Count the cats.")
    )
    assert own["messages"][0]["content"][-1]["text"] == "Count the cats."
    assert "temperature" not in own

    with pytest.raises(ValueError, match="needs an instruction"):
        vision_config_payload(VisionReadInput(model="m", images=[FILE_ID], mode="ask"))


async def test_music_asks_for_the_length_and_returns_the_audio_file(monkeypatch):
    seen = _record(
        monkeypatch,
        _response(AudioContent(file_id="song", url=DURABLE, mime_type="audio/mpeg", duration_ms=8000)),
    )
    result = await ai_generate_music(
        _ctx(), GenerateMusicInput(model="eleven_music_v2_5", prompt="lofi beat", duration_seconds=8)
    )
    assert isinstance(result, Success), result
    assert result.result.file_id == "song"
    assert result.result.duration_seconds == 8.0
    assert seen[0].duration_seconds == 8


async def test_music_declined_by_the_provider_says_so(monkeypatch):
    _record(monkeypatch, _response(finish=FinishReason.CONTENT_FILTER))
    result = await ai_generate_music(
        _ctx(), GenerateMusicInput(model="eleven_music_v2_5", prompt="x")
    )
    assert isinstance(result, Failure)
    assert result.error.code == "music_declined"


async def test_tts_sends_the_chosen_voice_where_the_provider_reads_it(monkeypatch):
    from matrx_ai.graph_nodes.tts_action import TextToSpeechInput, ai_text_to_speech

    seen = _record(monkeypatch, _response(AudioContent(file_id="a", url=DURABLE, mime_type="audio/mpeg")))
    result = await ai_text_to_speech(
        _ctx(), TextToSpeechInput(model="eleven_flash_v2_5", text="hi", voice="voice-123")
    )
    assert isinstance(result, Success), result
    # The step's voice was sent as ``voice``, which UnifiedConfig drops: ElevenLabs then
    # refused every call with "No tts_voice configured" (live, 2026-10-29).
    assert seen[0].tts_voice == "voice-123"


@pytest.mark.parametrize("node", ["tts", "image", "edit", "music"])
async def test_a_failed_turn_fails_the_step_with_the_providers_own_reason(monkeypatch, node):
    from matrx_ai.orchestrator import executor

    async def _failed(*_a: Any, **_k: Any) -> Any:
        return _Completed(
            final_response=UnifiedResponse(messages=[]),
            metadata={"status": "failed", "error": "No tts_voice configured", "error_type": "unknown_error"},
        )

    monkeypatch.setattr(executor, "execute_ai_request", _failed)
    from matrx_ai.graph_nodes.image_action import GenerateImageInput, ai_generate_image
    from matrx_ai.graph_nodes.tts_action import TextToSpeechInput, ai_text_to_speech

    run = {
        "tts": lambda: ai_text_to_speech(_ctx(), TextToSpeechInput(model="m", text="hi")),
        "image": lambda: ai_generate_image(_ctx(), GenerateImageInput(model="m", prompt="p")),
        "edit": lambda: ai_image_edit(_ctx(), EditImageInput(model="m", prompt="p", images=["https://x.test/a.png"])),
        "music": lambda: ai_generate_music(_ctx(), GenerateMusicInput(model="m", prompt="p")),
    }[node]
    result = await run()
    assert isinstance(result, Failure)
    assert "No tts_voice configured" in result.error.message
