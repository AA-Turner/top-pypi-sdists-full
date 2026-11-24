"""A tool image the producer already saved (file_id, no base64) reaches the model as an image_ref."""

import pytest

from matrx_ai.tools.image_outputs import (
    is_persisted_image_output,
    normalize_tool_output_async,
)
from matrx_ai.tools.models import ToolResult

FID = "d312cb3c-1111-2222-3333-444455556666"


def _ext_screenshot(**over):
    out = {
        "ok": True,
        "mode": "visible",
        "media_type": "image/jpeg",
        "format": "jpeg",
        "width": 2576,
        "height": 1730,
        "source_width": 3458,
        "source_height": 2322,
        "byte_length": 178418,
        "file_id": FID,
        "file_url": "https://signed.example/x?sig=1",
    }
    out.update(over)
    return out


@pytest.mark.asyncio
async def test_persisted_shape_becomes_image_ref_without_urls():
    out = await normalize_tool_output_async(_ext_screenshot(), tool_name="computer")
    assert out["kind"] == "image_ref"
    assert out["media_ref"] == {"file_id": FID, "vision_class": None}
    assert out["file_id"] == FID
    assert out["media_type"] == "image/jpeg"
    assert "file_url" not in out
    assert out["source_width"] == 3458  # not overwritten by width


@pytest.mark.asyncio
async def test_mime_type_key_and_width_mapping():
    raw = {"mime_type": "image/png", "width": 10, "height": 20, "file_id": FID, "image_url": "u"}
    out = await normalize_tool_output_async(raw)
    assert out["media_ref"]["file_id"] == FID
    assert (out["source_width"], out["source_height"]) == (10, 20)
    assert "image_url" not in out


@pytest.mark.asyncio
async def test_non_image_with_file_id_untouched():
    raw = {"media_type": "application/pdf", "file_id": FID}
    assert not is_persisted_image_output(raw)
    assert await normalize_tool_output_async(raw) is raw


@pytest.mark.asyncio
async def test_idempotent_on_image_ref():
    once = await normalize_tool_output_async(_ext_screenshot())
    assert await normalize_tool_output_async(once) is once


@pytest.mark.asyncio
async def test_nested_image_envelope():
    raw = {"text": "shot", "image": {"media_type": "image/png", "file_id": FID}}
    out = await normalize_tool_output_async(raw)
    assert out["kind"] == "image_ref" and out["media_ref"]["file_id"] == FID
    assert out["text"] == "shot"


@pytest.mark.asyncio
async def test_base64_still_uploads(monkeypatch):
    from matrx_ai.tools import image_outputs

    called = {}

    async def fake_upload(output, **kw):
        called["yes"] = True
        return {"kind": "image_ref", "media_ref": {"file_id": "x"}}

    monkeypatch.setattr(image_outputs, "upload_image_master", fake_upload)
    out = await normalize_tool_output_async(
        {"media_type": "image/png", "image_base64": "AAAA", "file_id": FID}
    )
    assert called and out["media_ref"]["file_id"] == "x"


@pytest.mark.asyncio
async def test_rewritten_output_yields_an_image_block():
    out = await normalize_tool_output_async(_ext_screenshot(), tool_name="computer")
    content = ToolResult(
        success=True, output=out, tool_name="computer", call_id="c1"
    ).to_tool_result_content()
    blocks = content["content"] if isinstance(content, dict) else content.content
    assert isinstance(blocks, list)
    imgs = [b for b in blocks if type(b).__name__ == "ImageContent"]
    assert len(imgs) == 1 and str(imgs[0].file_id) == FID
