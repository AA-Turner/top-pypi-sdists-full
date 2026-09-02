"""ToolResult.to_tool_result_content() must turn image_ref / image_ref_list
outputs into REAL vision blocks (ImageContent), never JSON text — and an
image_ref_list's optional `details` dict must ride along as one structured
TextContent block (feedback 6104ed3d: cms_verify returned file_id metadata
only, leaving the calling model visually blind)."""

import json

from matrx_ai.config import ImageContent, TextContent
from matrx_ai.tools.models import ToolResult


def _image_ref(file_id: str, viewport: str) -> dict:
    return {
        "kind": "image_ref",
        "media_ref": {"file_id": file_id, "vision_class": None},
        "media_type": "image/png",
        "source_width": 1440,
        "source_height": 900,
        "viewport": viewport,
        "url": "https://mymatrx.com/c/dev-website/general/x",
    }


def _result(output) -> ToolResult:
    return ToolResult(success=True, output=output, tool_name="cms_verify", call_id="c1")


def test_image_ref_list_becomes_vision_blocks():
    out = {
        "kind": "image_ref_list",
        "items": [_image_ref("f-1", "viewport_desktop"), _image_ref("f-2", "viewport_mobile")],
        "count": 2,
    }
    content = _result(out).to_tool_result_content()["content"]
    images = [b for b in content if isinstance(b, ImageContent)]
    assert [b.file_id for b in images] == ["f-1", "f-2"]
    # per-image summary text mentions the viewport
    texts = [b.text for b in content if isinstance(b, TextContent)]
    assert any("viewport_desktop" in t for t in texts)


def test_image_ref_list_details_ride_along_as_text_block():
    details = {
        "url_captured": "https://mymatrx.com/c/dev-website/general/x",
        "http_status": 200,
        "console_errors": ["Uncaught Error: boom"],
    }
    out = {"kind": "image_ref_list", "items": [_image_ref("f-1", "full_page")], "count": 1, "details": details}
    content = _result(out).to_tool_result_content()["content"]
    assert isinstance(content, list)
    last = content[-1]
    assert isinstance(last, TextContent)
    parsed = json.loads(last.text)
    assert parsed["http_status"] == 200
    assert parsed["console_errors"] == ["Uncaught Error: boom"]
    # and the image block still leads
    assert isinstance(content[0], ImageContent) and content[0].file_id == "f-1"


def test_plain_dict_output_stays_json_text():
    content = _result({"pages_total": 3}).to_tool_result_content()["content"]
    assert isinstance(content, str)
    assert json.loads(content) == {"pages_total": 3}
