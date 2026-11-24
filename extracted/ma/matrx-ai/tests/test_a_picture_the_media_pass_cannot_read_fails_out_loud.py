"""A PICTURE THE MEDIA PASS CANNOT READ FAILS OUT LOUD, NEVER AS THE ORIGINAL'S URL (CGU-10 AND-V IMG17, finding N4).

Since AND-IMG17 #1 the request boundary resolves a stored picture WITHOUT bytes: it leaves a presigned URL of the
ORIGINAL on the item (``resolved_url``) and the media pass is the one byte reader. When that read fails (the
resolver returns ``resolver_error`` — S3 throttled under the new concurrency of 8, a variant render that failed),
the media pass records nothing (no ``capture_error``, a debug-only print) and the item still carries the original's
URL, so the translator sends ``{"source": {"type": "url"}}``: the provider fetches the full-size original itself
(over Claude's 5 MB cap for a large photo, so the whole turn 400s) and nobody is told why. Before AND-IMG17 the
fallback was the original's bytes; now it is an unannounced URL.

Enabled with the fix (AND-IMG18): a failed read is captured, retried once, and sent as an announced stand-in.
"""

from __future__ import annotations

from typing import Any

import pytest

from matrx_ai import _ext
from matrx_ai.config.media_config import ImageContent
from matrx_ai.config.message_config import UnifiedMessage
from matrx_ai.config.unified_content import TextContent
from matrx_ai.providers.unified_client import UnifiedAIClient

MASTER_URL = "https://bucket.s3.amazonaws.com/photos/master.jpg?X-Amz-Signature=boundary"


class _FailingFileManager:
    async def resolve_media_async(self, ref: Any, *, needs_bytes: bool = False) -> Any:
        ref.resolver_error = "storage_read_failed: SlowDown"
        ref.is_resolved = False
        return ref


class _Messages:
    def __init__(self, messages: list[UnifiedMessage]) -> None:
        self._messages = messages

    def to_list(self) -> list[UnifiedMessage]:
        return self._messages


async def _run(monkeypatch) -> tuple[ImageContent, list[str]]:
    monkeypatch.setitem(_ext._registry, "get_cloud_file_manager", lambda: _FailingFileManager())
    captured: list[str] = []

    async def capture(exc: BaseException, *, kind: str, **_: Any) -> None:
        captured.append(kind)

    import matrx_connect.streaming.error_capture as ec

    monkeypatch.setattr(ec, "capture_error", capture)
    # The item exactly as the boundary leaves it now: resolved, no bytes, the original's presigned URL.
    picture = ImageContent(file_id="stored-photo", mime_type="image/jpeg", resolved_url=MASTER_URL, is_resolved=True)
    await UnifiedAIClient()._annotate_and_resolve_image_refs(
        _Messages([UnifiedMessage(role="user", content=[TextContent(text="and this one?"), picture])]),
        model_name="claude-sonnet-4-6", wire_format="anthropic_chat", supports_vision=True,
    )
    return picture, captured


@pytest.mark.asyncio
async def test_a_failed_read_is_captured(monkeypatch) -> None:
    _, captured = await _run(monkeypatch)
    assert captured, "the picture could not be read for this model and nothing recorded it"


@pytest.mark.asyncio
async def test_a_failed_read_never_sends_the_originals_url(monkeypatch) -> None:
    picture, _ = await _run(monkeypatch)
    wire = picture.to_anthropic()
    assert not (wire and wire["source"].get("url") == MASTER_URL), wire


@pytest.mark.asyncio
async def test_the_model_is_told_in_words_and_never_gets_the_picture(monkeypatch) -> None:
    from matrx_ai.providers.unified_client import UNREADABLE_PICTURE_TEXT

    monkeypatch.setitem(_ext._registry, "get_cloud_file_manager", lambda: _FailingFileManager())
    picture = ImageContent(file_id="stored-photo", mime_type="image/jpeg", resolved_url=MASTER_URL, is_resolved=True)
    message = UnifiedMessage(role="user", content=[TextContent(text="and this one?"), picture])
    sent = await UnifiedAIClient()._annotate_and_resolve_image_refs(
        _Messages([message]), model_name="claude-sonnet-4-6", wire_format="anthropic_chat", supports_vision=True,
    )
    # The SEND copy carries the stand-in; her stored message keeps the picture (AND-V IMG18 F1).
    assert picture in message.content
    assert picture not in sent[0].content
    stand_in = sent[0].content[1]
    assert isinstance(stand_in, TextContent) and stand_in.text.startswith(UNREADABLE_PICTURE_TEXT[:-1]), stand_in


@pytest.mark.asyncio
async def test_a_throttled_read_is_retried_once(monkeypatch) -> None:
    calls: list[int] = []

    class _OnceThrottled:
        async def resolve_media_async(self, ref: Any, *, needs_bytes: bool = False) -> Any:
            calls.append(1)
            if len(calls) == 1:
                ref.resolver_error = "storage_read_failed: SlowDown"
                return ref
            ref.base64_data, ref.is_resolved = "QUJD", True
            return ref

    monkeypatch.setitem(_ext._registry, "get_cloud_file_manager", lambda: _OnceThrottled())
    picture = ImageContent(file_id="stored-photo", mime_type="image/jpeg", resolved_url=MASTER_URL, is_resolved=True)
    message = UnifiedMessage(role="user", content=[picture])
    await UnifiedAIClient()._annotate_and_resolve_image_refs(
        _Messages([message]), model_name="claude-sonnet-4-6", wire_format="anthropic_chat", supports_vision=True,
    )
    assert len(calls) == 2 and message.content[0] is picture and picture.base64_data == "QUJD"
    assert picture.to_anthropic()["source"]["type"] == "base64"


@pytest.mark.asyncio
@pytest.mark.parametrize(
    ("resolver_error", "words"),
    [
        ("file_not_found", "was deleted"),
        ("access_denied", "no longer have access"),
    ],
)
async def test_a_permanent_failure_is_read_once_and_worded_for_its_reason(monkeypatch, resolver_error, words) -> None:
    """CGU-10 AND-V IMG19 N4: a gone or forbidden file is never retried and never promised for next time."""
    calls: list[int] = []
    sent: list[Any] = []

    class _Permanent:
        async def resolve_media_async(self, ref: Any, *, needs_bytes: bool = False) -> Any:
            calls.append(1)
            ref.resolver_error = resolver_error
            return ref

    class _Emitter:
        async def send_warning(self, payload: Any) -> None:
            sent.append(payload)

    import matrx_connect.context.app_context as ac
    import matrx_connect.streaming.error_capture as ec

    async def capture(*_: Any, **__: Any) -> None:
        return None

    monkeypatch.setattr(ec, "capture_error", capture)
    monkeypatch.setattr(ac, "try_get_app_context", lambda: type("C", (), {"emitter": _Emitter()})())
    monkeypatch.setitem(_ext._registry, "get_cloud_file_manager", lambda: _Permanent())
    picture = ImageContent(file_id="stored-photo", mime_type="image/jpeg", resolved_url=MASTER_URL, is_resolved=True)
    await UnifiedAIClient()._annotate_and_resolve_image_refs(
        _Messages([UnifiedMessage(role="user", content=[picture])]),
        model_name="claude-sonnet-4-6", wire_format="anthropic_chat", supports_vision=True,
    )
    assert len(calls) == 1, f"a permanent failure was retried ({len(calls)} reads)"
    assert sent and words in sent[0].user_message and "next time" not in sent[0].user_message, sent
    assert sent[0].metadata["reasons"] == [getattr(picture, "read_failure", None)]


@pytest.mark.asyncio
async def test_a_throttled_failure_is_still_promised_for_next_time(monkeypatch) -> None:
    sent: list[Any] = []

    class _Emitter:
        async def send_warning(self, payload: Any) -> None:
            sent.append(payload)

    import matrx_connect.context.app_context as ac

    monkeypatch.setattr(ac, "try_get_app_context", lambda: type("C", (), {"emitter": _Emitter()})())
    await _run(monkeypatch)
    assert sent and "will be sent next time" in sent[0].user_message, sent


@pytest.mark.asyncio
async def test_a_deleted_picture_is_a_warning_not_a_system_error(monkeypatch) -> None:
    """system_error 2026-11-12: three ``media_pass_read_failed`` rows were pictures deleted ~2 s before the turn
    read them. A deletion is an expected outcome: the model still gets the stand-in and the person the "was
    deleted" words, but no server error is filed. A file id no row answers to (``file_not_found``) still files."""
    captured: list[str] = []
    sent: list[Any] = []

    class _Deleted:
        async def resolve_media_async(self, ref: Any, *, needs_bytes: bool = False) -> Any:
            ref.resolver_error = "file_deleted"
            return ref

    class _Emitter:
        async def send_warning(self, payload: Any) -> None:
            sent.append(payload)

    import matrx_connect.context.app_context as ac
    import matrx_connect.streaming.error_capture as ec

    async def capture(exc: BaseException, *, kind: str, **_: Any) -> None:
        captured.append(kind)

    monkeypatch.setattr(ec, "capture_error", capture)
    monkeypatch.setattr(ac, "try_get_app_context", lambda: type("C", (), {"emitter": _Emitter()})())
    monkeypatch.setitem(_ext._registry, "get_cloud_file_manager", lambda: _Deleted())
    picture = ImageContent(file_id="stored-photo", mime_type="image/jpeg", resolved_url=MASTER_URL, is_resolved=True)
    message = UnifiedMessage(role="user", content=[picture])
    out = await UnifiedAIClient()._annotate_and_resolve_image_refs(
        _Messages([message]), model_name="claude-sonnet-4-6", wire_format="anthropic_chat", supports_vision=True,
    )
    assert captured == [], f"a deleted picture was filed as a server error: {captured}"
    assert picture not in out[0].content, "the deleted picture was sent instead of its stand-in"
    assert sent and "was deleted" in sent[0].user_message, sent
