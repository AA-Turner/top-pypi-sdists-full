"""A document that reaches the media fallback as a bare ``file_id`` is read, never dropped.

Live 2026-11-19 (claude-haiku-5-5, anthropic_chat): a person attached a stored text file; the
part reached dispatch as ``{kind: document, file_id}`` with no bytes (and once with no mime). The
fallback runs BEFORE the media pass that fetches document bytes, so it dropped the file with
``unsupported document format (mime='', name='document')`` / ``DocumentContent had no
base64_data`` and the model never saw it. The fallback now reads the stored file through the
host's files manager first.
"""

from __future__ import annotations

import base64

import pytest

from matrx_ai import _ext
from matrx_ai.config import MessageList, TextContent, UnifiedMessage
from matrx_ai.config.media_config import DocumentContent
from matrx_ai.processing.media_fallback import (
    MediaFallbackResolutionError,
    preprocess_unsupported_media,
)

_FILE_ID = "59c63223-c4a5-492f-a5b6-4a572d9c92ec"
_WORD = "zorblequint"


class _FakeFileManager:
    def __init__(self, *, fail: bool = False) -> None:
        self.calls: list[tuple[str | None, bool]] = []
        self.fail = fail

    async def resolve_media_async(self, ref, needs_bytes: bool = False):
        self.calls.append((ref.file_id, needs_bytes))
        if self.fail:
            ref.resolver_error = "access denied"
            return ref
        if needs_bytes:
            ref.base64_data = base64.b64encode(f"The word is {_WORD}.".encode()).decode()
        ref.mime_type = "text/plain"
        ref.metadata = {**(ref.metadata or {}), "file_name": "secret-word.txt"}
        ref.is_resolved = True
        return ref


@pytest.fixture
def file_manager(monkeypatch):
    fm = _FakeFileManager()
    monkeypatch.setitem(_ext._registry, "get_cloud_file_manager", lambda: fm)
    return fm


def _msg(document: DocumentContent) -> MessageList:
    return MessageList(
        _messages=[
            UnifiedMessage(
                role="user",
                content=[TextContent(text="Reply with the made-up word in the file."), document],
            )
        ]
    )


def _texts(ml: MessageList) -> str:
    return "\n".join(getattr(c, "text", "") or "" for m in ml.to_list() for c in (m.content or []))


@pytest.mark.parametrize("mime", [None, "text/plain"], ids=["no-mime", "text-plain-no-bytes"])
async def test_bare_file_id_document_is_read_and_converted(file_manager, mime):
    document = DocumentContent(file_id=_FILE_ID, mime_type=mime)
    out, _usage = await preprocess_unsupported_media(
        _msg(document), "anthropic_chat", model_name="claude-haiku-5-5"
    )
    assert _WORD in _texts(out)
    assert "secret-word.txt" in _texts(out)
    assert (_FILE_ID, True) in file_manager.calls


async def test_unreadable_stored_document_still_fails_loud_and_names_why(monkeypatch):
    fm = _FakeFileManager(fail=True)
    monkeypatch.setitem(_ext._registry, "get_cloud_file_manager", lambda: fm)
    document = DocumentContent(file_id=_FILE_ID, mime_type="text/plain")
    with pytest.raises(MediaFallbackResolutionError, match="access denied"):
        await preprocess_unsupported_media(
            _msg(document), "anthropic_chat", model_name="claude-haiku-5-5"
        )
