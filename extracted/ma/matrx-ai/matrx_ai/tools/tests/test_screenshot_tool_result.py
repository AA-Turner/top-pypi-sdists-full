"""End-to-end forcing-function test for the screenshot tool-result path.

This is the test that pins the ENTIRE class of failure that started this
work — the 6.1M-token bug. We feed a screenshot-shaped tool output
through:

  1. ``normalize_tool_output_async`` — uploads master, rewrites to image_ref.
  2. ``ToolResult(output=...).to_tool_result_content()`` — emits typed blocks.
  3. ``ToolResultContent(...).to_anthropic()`` / ``.to_openai()`` /
     ``.to_google()`` — provider serialisation.

The forcing function is **the absence of base64 in the final provider
payload**. If anything in the chain regresses to JSON-stringifying the
image into a text content block, the assertions catch it: the encoded
JSON would carry the base64 string, exceeding hundreds of bytes per
content block.

A ``return original_output`` regression in ``upload_image_master`` would
fail these assertions too, because the test asserts the *rewritten*
output's structural properties (no base64 keys present, ``kind`` set to
``image_ref``, ``media_ref.file_id`` populated).
"""

from __future__ import annotations

import base64
import json

import pytest

from matrx_ai._ext import _registry as _ext_registry
from matrx_ai.config.tools_config import ToolResultContent
from matrx_ai.tools.image_outputs import (
    is_image_ref_output,
    is_image_shaped_output,
    normalize_tool_output_async,
)
from matrx_ai.tools.models import ToolResult

# ---------------------------------------------------------------------------
# In-memory fake FileManager — same shape as the real one's call sites
# ---------------------------------------------------------------------------


class _FakeSyncResult:
    def __init__(self, file_id: str, storage_uri: str, url: str | None = None) -> None:
        self.file_id = file_id
        self.storage_uri = storage_uri
        self.url = url
        self.is_new = True


class _FakeSyncEngine:
    def __init__(self) -> None:
        self.writes: list[dict] = []

    async def managed_write_async(
        self,
        file_path: str,
        content: bytes,
        *,
        mime_type: str | None = None,
        visibility: str = "personal",
        change_summary: str | None = None,
        metadata: dict | None = None,
    ) -> _FakeSyncResult:
        self.writes.append(
            {
                "file_path": file_path,
                "size": len(content),
                "mime_type": mime_type,
                "visibility": visibility,
                "metadata": metadata or {},
            }
        )
        return _FakeSyncResult(
            file_id=f"file-{len(self.writes)}",
            storage_uri=f"s3://bucket/{file_path}",
            url=f"https://fake.cdn/{file_path}",
        )


class _FakeFileManager:
    def __init__(self) -> None:
        self.sync_engine = _FakeSyncEngine()


@pytest.fixture
def fake_fm() -> _FakeFileManager:
    fm = _FakeFileManager()

    snap = dict(_ext_registry)
    _ext_registry["get_cloud_file_manager"] = lambda: fm
    yield fm
    _ext_registry.clear()
    _ext_registry.update(snap)


# A small valid PNG (1x1 red) so the shape detector + base64 decoder both
# work on real data.
_PNG_BYTES = (
    b"\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01"
    b"\x08\x02\x00\x00\x00\x90wS\xde\x00\x00\x00\x0cIDATx\x9cc\xf8\xcf"
    b"\xc0\x00\x00\x00\x03\x00\x01\x00\x18\xdd\x8d\xb4\x00\x00\x00\x00IEND\xaeB`\x82"
)
_PNG_B64 = base64.b64encode(_PNG_BYTES).decode("ascii")


def _make_screenshot_output() -> dict:
    """Mimic the wire shape the browser extension's take_screenshot returns."""
    return {
        "media_type": "image/png",
        "screenshot_base64": _PNG_B64,
        "width": 1,
        "height": 1,
        "url": "https://example.com/page",
        "title": "Example Page",
    }


def test_is_image_shaped_output_detects_screenshot_payloads() -> None:
    assert is_image_shaped_output(_make_screenshot_output())
    assert not is_image_shaped_output({"media_type": "image/png"})  # no base64
    assert not is_image_shaped_output({"screenshot_base64": _PNG_B64})  # no media_type
    assert not is_image_shaped_output({"media_type": "text/plain", "screenshot_base64": _PNG_B64})
    assert not is_image_shaped_output("not a dict")
    assert is_image_shaped_output(
        {
            "text": "local capture",
            "image": {"media_type": "image/png", "base64_data": _PNG_B64},
        }
    )


def test_provider_content_is_model_visible_but_never_serialized() -> None:
    from matrx_ai.config import ImageContent

    block = ImageContent(base64_data=_PNG_B64, mime_type="image/png")
    result = ToolResult(
        success=True,
        output={"kind": "image_ref", "artifact_id": "local-1"},
        provider_content=[block],
        call_id="call-local",
        tool_name="local_screen",
    )

    assert result.to_tool_result_content()["content"] == [block]
    dumped = result.model_dump()
    assert "provider_content" not in dumped
    assert _PNG_B64 not in json.dumps(dumped)


@pytest.mark.asyncio
async def test_normalize_flattens_legacy_local_screenshot_envelope(fake_fm) -> None:
    rewritten = await normalize_tool_output_async(
        {
            "text": "local capture",
            "image": {"media_type": "image/png", "base64_data": _PNG_B64},
            "metadata": {"width": 1, "height": 1},
        },
        tool_name="local_screen",
    )

    assert rewritten["kind"] == "image_ref"
    assert rewritten["media_ref"]["file_id"] == "file-1"
    assert rewritten["text"] == "local capture"
    assert rewritten["metadata"] == {"width": 1, "height": 1}
    assert "image" not in rewritten
    assert "base64_data" not in json.dumps(rewritten)


@pytest.mark.asyncio
async def test_normalize_uploads_master_and_strips_base64(fake_fm) -> None:
    """The funnel must: upload master, strip every *_base64 key, set
    ``kind=image_ref``, populate ``media_ref.file_id``. Forcing function:
    a regression that left base64 in the output would fail
    ``no_base64_keys`` below."""
    out = _make_screenshot_output()

    rewritten = await normalize_tool_output_async(out, tool_name="take_screenshot")

    # Master upload happened exactly once with the decoded bytes.
    writes = fake_fm.sync_engine.writes
    assert len(writes) == 1
    assert writes[0]["size"] == len(_PNG_BYTES)
    assert writes[0]["mime_type"] == "image/png"
    assert "tool-images" in writes[0]["file_path"]

    # Output rewritten to image_ref shape, base64 stripped.
    assert rewritten["kind"] == "image_ref"
    assert rewritten["media_ref"] == {"file_id": "file-1", "vision_class": None}
    assert rewritten["media_type"] == "image/png"
    assert rewritten["source_width"] == 1
    assert rewritten["source_height"] == 1
    no_base64_keys = [
        k for k in rewritten if k.endswith("_base64") or k == "image_base64"
    ]
    assert no_base64_keys == [], f"base64 leaked into rewritten output: {no_base64_keys}"

    # Idempotent.
    rewritten2 = await normalize_tool_output_async(rewritten, tool_name="take_screenshot")
    assert rewritten2 is rewritten
    assert len(fake_fm.sync_engine.writes) == 1, "second normalize call re-uploaded"


@pytest.mark.asyncio
async def test_normalize_no_op_when_not_image_shaped(fake_fm) -> None:
    plain = {"text": "hello", "ok": True}
    out = await normalize_tool_output_async(plain, tool_name="some_tool")
    assert out is plain
    assert fake_fm.sync_engine.writes == []


@pytest.mark.asyncio
async def test_tool_result_emits_typed_blocks_for_image_ref(fake_fm) -> None:
    """``ToolResult.to_tool_result_content`` must turn an image_ref output
    into a list containing an ImageContent block — NOT a JSON-stringified
    text blob. Forcing function: the content is a list and the first
    element walks like an ImageContent."""
    rewritten = await normalize_tool_output_async(
        _make_screenshot_output(), tool_name="take_screenshot"
    )
    assert is_image_ref_output(rewritten)

    result = ToolResult(
        success=True,
        output=rewritten,
        call_id="call-xyz",
        tool_name="take_screenshot",
    )
    payload = result.to_tool_result_content()

    assert isinstance(payload["content"], list), (
        f"expected typed-block list, got {type(payload['content']).__name__}"
    )
    assert len(payload["content"]) >= 1
    image_block = payload["content"][0]
    # Walks like an ImageContent.
    assert hasattr(image_block, "to_anthropic")
    assert hasattr(image_block, "to_openai")
    assert hasattr(image_block, "to_google")
    assert getattr(image_block, "file_id", None) == "file-1"
    assert getattr(image_block, "mime_type", None) == "image/png"


@pytest.mark.asyncio
async def test_anthropic_serialisation_carries_no_base64(fake_fm) -> None:
    """The smoking-gun assertion. After end-to-end serialisation, the
    Anthropic payload must NOT contain the original base64 string anywhere.
    A regression that leaks base64 (the original 6.1M-token bug) fails."""
    rewritten = await normalize_tool_output_async(
        _make_screenshot_output(), tool_name="take_screenshot"
    )
    # Simulate the resolution step that fills in `url` after master/variant
    # render. We bypass the matrx-utils resolver here — just confirm the
    # serialiser doesn't put base64 on the wire when the URL is set.
    result = ToolResult(
        success=True, output=rewritten, call_id="cid", tool_name="take_screenshot"
    )
    payload = result.to_tool_result_content()
    blocks = payload["content"]
    # Stamp a URL on the image block (what the resolver would do).
    blocks[0].url = "https://fake.cdn/screens/master.png"

    trc = ToolResultContent(
        name="take_screenshot",
        call_id="cid",
        content=blocks,
    )

    anthropic_payload = trc.to_anthropic()
    serialised = json.dumps(anthropic_payload)
    assert _PNG_B64 not in serialised, (
        "base64 leaked into Anthropic payload — the 6.1M-token bug is back"
    )
    # And the image URL is present.
    assert "https://fake.cdn/screens/master.png" in serialised
    # And Anthropic shape is right: tool_result with a list of content blocks.
    assert anthropic_payload["type"] == "tool_result"
    content = anthropic_payload["content"]
    assert isinstance(content, list)
    image_blocks = [b for b in content if b.get("type") == "image"]
    assert len(image_blocks) == 1
    assert image_blocks[0]["source"]["type"] == "url"


@pytest.mark.asyncio
async def test_openai_serialisation_uses_typed_blocks_summary(fake_fm) -> None:
    rewritten = await normalize_tool_output_async(
        _make_screenshot_output(), tool_name="take_screenshot"
    )
    result = ToolResult(
        success=True, output=rewritten, call_id="cid", tool_name="take_screenshot"
    )
    blocks = result.to_tool_result_content()["content"]
    blocks[0].url = "https://fake.cdn/screens/master.png"

    trc = ToolResultContent(
        name="take_screenshot",
        call_id="cid",
        content=blocks,
    )
    openai_payload = trc.to_openai()
    serialised_full = json.dumps(openai_payload)
    assert _PNG_B64 not in serialised_full

    # OpenAI's function_call_output requires string content — verify the
    # blocks are JSON-serialised as a stringified `{"blocks": [...]}` payload.
    output = openai_payload.get("output")
    assert isinstance(output, str)
    parsed = json.loads(output)
    assert "blocks" in parsed
    assert isinstance(parsed["blocks"], list)
    assert len(parsed["blocks"]) >= 1


@pytest.mark.asyncio
async def test_google_serialisation_uses_typed_blocks_text(fake_fm) -> None:
    rewritten = await normalize_tool_output_async(
        _make_screenshot_output(), tool_name="take_screenshot"
    )
    result = ToolResult(
        success=True, output=rewritten, call_id="cid", tool_name="take_screenshot"
    )
    blocks = result.to_tool_result_content()["content"]
    blocks[0].url = "https://fake.cdn/screens/master.png"

    trc = ToolResultContent(
        name="take_screenshot",
        call_id="cid",
        content=blocks,
    )
    google_payload = trc.to_google()
    serialised = json.dumps(google_payload)
    assert _PNG_B64 not in serialised


@pytest.mark.asyncio
async def test_normalize_records_upload_failure_without_leaking_base64(monkeypatch) -> None:
    """When upload fails, the base64 must STILL be stripped — the LLM
    context never sees a multi-megabyte blob, even on failure. The
    failure is surfaced as a structured ``media_ref_error`` instead."""

    class _BrokenSyncEngine:
        async def managed_write_async(self, *a, **kw):
            raise RuntimeError("simulated S3 outage")

    class _BrokenFM:
        sync_engine = _BrokenSyncEngine()

    snap = dict(_ext_registry)
    _ext_registry["get_cloud_file_manager"] = lambda: _BrokenFM()
    try:
        out = await normalize_tool_output_async(
            _make_screenshot_output(), tool_name="take_screenshot"
        )
    finally:
        _ext_registry.clear()
        _ext_registry.update(snap)

    assert out["kind"] == "image_ref"
    assert out["media_ref"] is None
    assert "media_ref_error" in out
    assert "simulated S3 outage" in out["media_ref_error"]
    assert "screenshot_base64" not in out
    serialised = json.dumps(out)
    assert _PNG_B64 not in serialised, "base64 leaked even after upload failure"
