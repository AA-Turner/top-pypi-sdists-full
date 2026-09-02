from __future__ import annotations

import base64
import json
from types import SimpleNamespace

import pytest

from matrx_ai.config import DocumentContent, TextContent, ToolResultContent, UnifiedMessage
from matrx_ai.providers.unified_client import (
    UnifiedAIClient,
    _resolve_media_ref_item,
    _strip_document_content_for_unsupported_model,
)
from matrx_ai.tools.models import ToolResult


def _document_result() -> ToolResultContent:
    result = ToolResult(
        success=True,
        tool_name="document_content",
        call_id="call-1",
        output={
            "kind": "document_ref",
            "media_ref": {
                "file_id": "selected-file-id",
                "mime_type": "application/pdf",
            },
            "media_type": "application/pdf",
            "document_id": "processed-doc-id",
            "source_pages": [44, 2, 19],
            "output_page_map": [
                {"output_page": 1, "source_page": 44},
                {"output_page": 2, "source_page": 2},
                {"output_page": 3, "source_page": 19},
            ],
        },
    )
    payload = result.to_tool_result_content()
    return ToolResultContent(**payload)


def test_document_ref_becomes_document_and_mapping_blocks() -> None:
    content = _document_result()

    assert isinstance(content.content, list)
    assert isinstance(content.content[0], DocumentContent)
    assert content.content[0].file_id == "selected-file-id"
    assert content.content[0].mime_type == "application/pdf"
    assert isinstance(content.content[1], TextContent)
    details = json.loads(content.content[1].text)
    assert details["source_pages"] == [44, 2, 19]
    assert details["attached_file_id"] == "selected-file-id"


def test_document_tool_result_reaches_openai_anthropic_and_google() -> None:
    content = _document_result()
    pdf_bytes = b"%PDF-1.7\nselected pages"
    encoded = base64.b64encode(pdf_bytes).decode()
    document = content.content[0]
    assert isinstance(document, DocumentContent)
    document.base64_data = encoded
    document.is_resolved = True

    openai_items = UnifiedMessage(role="tool", content=[content]).to_openai_items_modified()
    assert openai_items[0]["type"] == "function_call_output"
    assert encoded not in openai_items[0]["output"]
    assert openai_items[1]["role"] == "user"
    assert openai_items[1]["content"][0]["type"] == "input_file"
    assert encoded in openai_items[1]["content"][0]["file_data"]

    anthropic = content.to_anthropic()
    assert anthropic["content"][0]["type"] == "document"
    assert anthropic["content"][0]["source"]["data"] == encoded

    google = UnifiedMessage(role="tool", content=[content]).to_google_content()
    assert google is not None
    assert google["parts"][0]["functionResponse"]["name"] == "document_content"
    assert google["parts"][1]["inlineData"]["data"] == encoded


@pytest.mark.asyncio
async def test_mid_loop_document_ref_is_resolved_from_cloud_file_id() -> None:
    content = _document_result()
    document = content.content[0]
    assert isinstance(document, DocumentContent)

    class FakeFileManager:
        async def resolve_media_async(self, ref, *, needs_bytes):
            assert needs_bytes is True
            assert ref.file_id == "selected-file-id"
            ref.base64_data = base64.b64encode(b"%PDF resolved").decode()
            ref.mime_type = "application/pdf"
            ref.is_resolved = True

    await _resolve_media_ref_item(FakeFileManager(), document)

    assert document.is_resolved is True
    assert document.base64_data == base64.b64encode(b"%PDF resolved").decode()


def test_unsupported_route_replaces_nested_document_with_text() -> None:
    content = _document_result()
    messages = SimpleMessageList([UnifiedMessage(role="tool", content=[content])])

    replaced = _strip_document_content_for_unsupported_model(
        messages,
        model_name="text-only",
        wire_format="generic_openai_chat",
    )

    assert replaced == 1
    assert isinstance(content.content[0], TextContent)
    assert "physical-page content was omitted" in content.content[0].text


@pytest.mark.asyncio
async def test_required_document_input_fails_instead_of_becoming_placeholder() -> None:
    document = _document_result().content[0]
    assert isinstance(document, DocumentContent)
    messages = SimpleMessageList([UnifiedMessage(role="user", content=[document])])

    with pytest.raises(ValueError, match="requires native PDF/document input"):
        await UnifiedAIClient()._annotate_and_resolve_image_refs(
            messages,
            model_name="text-only",
            wire_format="generic_openai_chat",
            supports_vision=False,
            require_native_document_input=True,
        )


@pytest.mark.asyncio
@pytest.mark.parametrize("interaction", ["turn", "extraction"])
async def test_execute_rejects_required_pdf_before_fallback_or_extraction(
    monkeypatch: pytest.MonkeyPatch,
    interaction: str,
) -> None:
    """The route gate runs before both known no-source bypasses."""
    import matrx_ai.catalog.resolve as catalog_resolve
    import matrx_ai.processing.media_fallback as media_fallback

    document = _document_result().content[0]
    assert isinstance(document, DocumentContent)
    messages = SimpleMessageList([UnifiedMessage(role="user", content=[document])])
    config = SimpleNamespace(
        model="test-model",
        routing_offering_id=None,
        metadata={"require_native_document_input": True},
        messages=messages,
    )
    request = SimpleNamespace(config=config, debug=False, add_usage=lambda _usage: None)
    profile = SimpleNamespace(
        model_name="text-only",
        provider_model_id="provider-model",
        offering_id="offering-1",
        capabilities=SimpleNamespace(
            interaction=interaction,
            supports_vision=False,
        ),
        wire_format="generic_openai_chat",
        client_attr="extraction" if interaction == "extraction" else "generic_openai_chat",
    )

    async def resolve_profile(*_args, **_kwargs):
        return profile

    fallback_called = False

    async def media_fallback_should_not_run(*_args, **_kwargs):
        nonlocal fallback_called
        fallback_called = True
        return messages, []

    monkeypatch.setattr(catalog_resolve, "resolve_tts_call_profile", resolve_profile)
    monkeypatch.setattr(
        media_fallback, "preprocess_unsupported_media", media_fallback_should_not_run
    )

    with pytest.raises(ValueError, match="requires native PDF/document input"):
        await UnifiedAIClient().execute(request)

    assert fallback_called is False


class SimpleMessageList:
    def __init__(self, messages: list[UnifiedMessage]) -> None:
        self._messages = messages

    def to_list(self) -> list[UnifiedMessage]:
        return self._messages
