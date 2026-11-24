"""A delegated tool result may carry SEVERAL already-saved pictures (``pictures``), each reaching
the model as a real image with its label, in order, beside the tool's own output; a model that
cannot read images is told each picture was skipped instead of being sent it."""

import json

import pytest

from matrx_ai.config import ImageContent, TextContent
from matrx_ai.tools.image_outputs import (
    has_picture_list,
    normalize_tool_output_async,
)
from matrx_ai.tools.models import media_ref_output_blocks

A = "aaaaaaaa-1111-2222-3333-444455556666"
B = "bbbbbbbb-1111-2222-3333-444455556666"


def _pic(fid, label):
    return {
        "kind": "image_ref",
        "media_type": "image/jpeg",
        "file_id": fid,
        "media_ref": {"file_id": fid, "vision_class": None},
        "file_url": "https://signed.example/x?sig=1",
        "source_width": 1280,
        "source_height": 800,
        "size_bytes": 120000,
        "label": label,
        "auto": True,
    }


def _batch_output():
    return {
        "count": 2,
        "results": [{"step": 0, "ok": True}, {"step": 1, "ok": True}],
        "pictures": [_pic(A, "after step 0 (navigate)"), _pic(B, "after step 1 (computer)")],
    }


def test_detects_picture_list():
    assert has_picture_list(_batch_output())
    assert not has_picture_list({"pictures": []})
    assert not has_picture_list({"pictures": [{"file_id": A}]})  # not an image


@pytest.mark.asyncio
async def test_pictures_become_ordered_image_ref_list_with_output_kept():
    out = await normalize_tool_output_async(_batch_output(), tool_name="chrome_batch")
    assert out["kind"] == "image_ref_list"
    assert [i["file_id"] for i in out["items"]] == [A, B]
    assert all("file_url" not in i and "url" not in i for i in out["items"])
    assert out["details"]["results"][1]["step"] == 1
    assert "pictures" not in out["details"]
    blocks = media_ref_output_blocks(json.dumps(out))  # a DB rebuild sees the same thing
    images = [b for b in blocks if isinstance(b, ImageContent)]
    texts = [b.text for b in blocks if isinstance(b, TextContent)]
    assert [b.file_id for b in images] == [A, B]
    assert images[0].metadata.get("auto_picture") is True
    assert texts[0].startswith("after step 0 (navigate)")
    assert '"results"' in texts[-1]


@pytest.mark.asyncio
async def test_non_vision_model_is_told_each_picture_was_skipped():
    from matrx_ai.config import MessageList, UnifiedMessage
    from matrx_ai.config.tools_config import ToolResultContent
    from matrx_ai.processing.media_fallback.handler import preprocess_unsupported_media

    out = await normalize_tool_output_async(_batch_output(), tool_name="chrome_batch")
    blocks = media_ref_output_blocks(out)
    msg = UnifiedMessage(
        role="tool",
        content=[ToolResultContent(tool_use_id="t1", name="chrome_batch", content=blocks)],
    )
    converted, usage = await preprocess_unsupported_media(
        MessageList(_messages=[msg]),
        "anthropic",
        model_name="text-only-model",
        model_supports_vision=False,
    )
    trc = converted.to_list()[0].content[0]
    assert not any(isinstance(b, ImageContent) for b in trc.content)
    skipped = [b.text for b in trc.content if isinstance(b, TextContent) and "skipped" in b.text]
    assert len(skipped) == 2 and "text-only-model cannot read images" in skipped[0]
    assert usage == []
    # the original message (and so the saved history) still holds the pictures
    assert any(isinstance(b, ImageContent) for b in msg.content[0].content)
