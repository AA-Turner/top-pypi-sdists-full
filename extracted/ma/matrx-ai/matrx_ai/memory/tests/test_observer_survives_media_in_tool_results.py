"""A tool result carrying an image (ImageContent) must not crash the memory Observer.

2026-11-15: every Observer pass on a conversation whose tool returned an image failed
with "Object of type ImageContent is not JSON serializable", so memory stopped there.
Two layers: the adapter stores JSON-safe results, and the renderers never raise.
"""

from matrx_ai.config.media_config import ImageContent
from matrx_ai.config.tools_config import ToolResultContent
from matrx_ai.memory.adapter import convert_to_om_messages
from matrx_ai.memory.observer_agent import format_messages_for_observer
from matrx_ai.memory.types import ToolCallPart, ToolResultPart


def _messages() -> list[dict]:
    image = ImageContent(url="https://example.com/shot.png", mime_type="image/png")
    result = ToolResultContent(
        tool_use_id="toolu_1",
        name="browser_screenshot",
        content=[{"type": "text", "text": "captured"}, image],
    )
    return [{"role": "tool", "content": [result]}, {"role": "user", "content": [image, "look"]}]


def test_tool_result_with_image_formats_for_observer() -> None:
    om = convert_to_om_messages(_messages(), thread_id="t", resource_id="r")
    text = format_messages_for_observer(om)
    assert "captured" in text
    assert "[image content]" in text


def test_renderers_survive_raw_media_objects_when_adapter_is_bypassed() -> None:
    om = convert_to_om_messages(_messages(), thread_id="t", resource_id="r")
    raw = [ImageContent(url="https://example.com/x.png")]
    for msg in om:
        for part in msg.content:
            if isinstance(part, ToolResultPart):
                part.result = raw
    om[0].content.append(ToolCallPart(tool_call_id="c", tool_name="t", args={"img": raw[0]}))
    assert "[image content]" in format_messages_for_observer(om)
    assert "[image content]" in om[0].get_text()
