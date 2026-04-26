"""Browser-level PDF attachment fallback regression tests."""

from __future__ import annotations

from typing import Any, AsyncGenerator
from unittest.mock import patch

import pytest

from anteroom.services.document_extractor import ExtractionResult

pytestmark = [pytest.mark.e2e]

try:
    from playwright.sync_api import Page, expect

    HAS_PLAYWRIGHT = True
except ImportError:  # pragma: no cover - exercised only without playwright installed
    HAS_PLAYWRIGHT = False

requires_playwright = pytest.mark.skipif(not HAS_PLAYWRIGHT, reason="playwright not installed")


def _stream_capturing(captured: dict[str, Any]):
    async def _stream(
        self,
        messages: list[dict[str, Any]],
        tools: list[dict[str, Any]] | None = None,
        cancel_event: Any = None,
        extra_system_prompt: str | None = None,
        **kwargs: Any,
    ) -> AsyncGenerator[dict[str, Any], None]:
        captured["messages"] = messages
        captured["tools"] = tools
        captured["extra_system_prompt"] = extra_system_prompt
        yield {"event": "token", "data": {"content": "Captured."}}
        yield {"event": "done", "data": {}}

    return _stream


def _flatten_message_text(messages: list[dict[str, Any]]) -> str:
    parts: list[str] = []
    for message in messages:
        content = message.get("content")
        if isinstance(content, str):
            parts.append(content)
        elif isinstance(content, list):
            for item in content:
                if isinstance(item, dict) and item.get("type") == "text":
                    parts.append(str(item.get("text") or ""))
    return "\n".join(parts)


@requires_playwright
def test_pdf_upload_success_includes_extracted_text(
    authenticated_page: "Page",
    tmp_path,
) -> None:
    pdf = tmp_path / "report.pdf"
    pdf.write_bytes(b"%PDF-1.4 fake pdf")
    captured: dict[str, Any] = {}

    with (
        patch(
            "anteroom.services.document_extractor.extract_text",
            return_value=ExtractionResult(text="PDF content from extraction"),
        ),
        patch("anteroom.services.ai_service.AIService.stream_chat", new=_stream_capturing(captured)),
    ):
        authenticated_page.locator("#file-input").set_input_files(str(pdf))
        expect(authenticated_page.locator("#attachment-previews")).to_contain_text("report.pdf")
        authenticated_page.locator("#message-input").fill("summarize this pdf")
        authenticated_page.locator("#btn-send").click()
        expect(authenticated_page.locator(".message.assistant .message-content")).to_contain_text(
            "Captured.", timeout=10000
        )

    text = _flatten_message_text(captured["messages"])
    assert "PDF content from extraction" in text
    assert "PDF text could not be extracted automatically" not in text
    assert "Use the appropriate tool" not in text
    assert "use tools to read this file" not in text


@requires_playwright
def test_pdf_upload_failure_does_not_emit_positive_tool_routing(
    authenticated_page: "Page",
    tmp_path,
) -> None:
    pdf = tmp_path / "scan.pdf"
    pdf.write_bytes(b"%PDF-1.4 fake pdf")
    captured: dict[str, Any] = {}

    with (
        patch(
            "anteroom.services.document_extractor.extract_text",
            return_value=ExtractionResult(
                text=None,
                warnings=["pypdf not installed - PDF text extraction unavailable"],
            ),
        ),
        patch("anteroom.services.ai_service.AIService.stream_chat", new=_stream_capturing(captured)),
    ):
        authenticated_page.locator("#file-input").set_input_files(str(pdf))
        expect(authenticated_page.locator("#attachment-previews")).to_contain_text("scan.pdf")
        authenticated_page.locator("#message-input").fill("summarize this pdf")
        authenticated_page.locator("#btn-send").click()
        expect(authenticated_page.locator(".message.assistant .message-content")).to_contain_text(
            "Captured.", timeout=10000
        )

    text = _flatten_message_text(captured["messages"])
    prompt = captured["extra_system_prompt"]
    assert "PDF text could not be extracted automatically" in text
    assert "Uploaded attachments are not workspace file paths" in text
    assert "Use the appropriate tool" not in text
    assert "use tools to read this file" not in text
    assert "Use the appropriate tool" not in prompt
    assert "use tools to read this file" not in prompt
