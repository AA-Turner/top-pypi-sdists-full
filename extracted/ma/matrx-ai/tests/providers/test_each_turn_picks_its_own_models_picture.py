"""CGU-10 AND-IMG16 #2 — a stored picture's vision class is a record, never a request.

Live run 7abfdf61: a chat started on a GPT model stored its picture part with
``vision_class: openai_original``; turn 2 on Claude read that part back
(``reconstruct_media_content`` keeps the stored class) and the media pass kept any class already on
the item, so Claude was sent the OpenAI 2048 variant instead of its own. Every turn must pick the
class for the model it is about to call.

The path here is the real one: the stored part dict → ``reconstruct_media_content`` → the media
pass in ``UnifiedAIClient``. The fake file manager renders the variant with the production encoder.
"""

from __future__ import annotations

import base64
from io import BytesIO
from typing import Any

import pytest
from PIL import Image

from matrx_ai import _ext
from matrx_ai.config.media_config import ImageContent, reconstruct_media_content
from matrx_ai.config.message_config import UnifiedMessage
from matrx_ai.config.unified_content import TextContent
from matrx_ai.processing.vision import VISION_API_CLASSES, reencode_for_vision_class, resolve_vision_class
from matrx_ai.providers.unified_client import UnifiedAIClient

MASTER_SIZE = (3000, 2250)


def _master() -> bytes:
    buf = BytesIO()
    Image.new("RGB", MASTER_SIZE, (40, 120, 200)).save(buf, format="PNG")
    return buf.getvalue()


MASTER = _master()


class _FakeFileManager:
    def __init__(self) -> None:
        self.classes_rendered: list[str | None] = []

    async def resolve_media_async(self, ref: Any, *, needs_bytes: bool = False) -> Any:
        self.classes_rendered.append(ref.vision_class)
        if ref.vision_class:
            data = reencode_for_vision_class(MASTER, VISION_API_CLASSES[ref.vision_class])
            ref.mime_type = "image/jpeg"
        else:
            data = MASTER
            ref.mime_type = "image/png"
        ref.base64_data = base64.b64encode(data).decode("ascii")
        ref.is_resolved = True
        return ref


class _Messages:
    def __init__(self, messages: list[UnifiedMessage]) -> None:
        self._messages = messages

    def to_list(self) -> list[UnifiedMessage]:
        return self._messages


async def _turn(fm: _FakeFileManager, item: ImageContent, model: str, wire: str) -> None:
    messages = _Messages([UnifiedMessage(role="user", content=[TextContent(text="what is this?"), item])])
    await UnifiedAIClient()._annotate_and_resolve_image_refs(
        messages, model_name=model, wire_format=wire, supports_vision=True
    )


def _long_edge(item: ImageContent) -> int:
    return max(Image.open(BytesIO(base64.b64decode(item.base64_data))).size)


@pytest.mark.asyncio
@pytest.mark.parametrize(
    ("first", "second"),
    [
        (("gpt-5.4-nano", "openai_responses"), ("claude-sonnet-4-6", "anthropic")),
        (("gpt-5.4-nano", "openai_responses"), ("claude-opus-4-7", "anthropic")),
        (("claude-sonnet-4-6", "anthropic"), ("gpt-5.4-nano", "openai_responses")),
    ],
)
async def test_a_stored_class_from_one_model_never_reaches_the_next(monkeypatch, first, second):
    fm = _FakeFileManager()
    monkeypatch.setitem(_ext._registry, "get_cloud_file_manager", lambda: fm)

    # Turn 1: the person's picture, as the boundary resolves it (master bytes, no class).
    sent = ImageContent(
        file_id="pic-1",
        base64_data=base64.b64encode(MASTER).decode("ascii"),
        mime_type="image/png",
        is_resolved=True,
    )
    await _turn(fm, sent, *first)
    first_class = resolve_vision_class(*first).name
    assert sent.vision_class == first_class

    # The part is stored and read back on turn 2 (what the database row holds — no bytes).
    stored = sent.to_storage_dict()
    stored.pop("base64_data", None)
    assert stored["metadata"]["vision_class"] == first_class, "the stored part records what was sent"
    replayed = reconstruct_media_content(stored)
    assert isinstance(replayed, ImageContent)
    # Read back, the class is a record (metadata), never a request: the request boundary resolves every item
    # with the class it carries, so carrying the stored one rendered the EARLIER model's variant first (live).
    assert replayed.vision_class is None
    assert replayed.metadata.get("vision_class") == first_class
    assert replayed.to_storage_dict()["metadata"]["vision_class"] == first_class, "the record survives a re-save"

    await _turn(fm, replayed, *second)

    want = resolve_vision_class(*second)
    assert want.name != first_class
    assert replayed.vision_class == want.name, (
        f"turn 2 on {second[0]} kept the earlier model's class {replayed.vision_class!r}"
    )
    assert fm.classes_rendered[-1] == want.name, "the variant rendered for turn 2 is the earlier model's"
    assert _long_edge(replayed) <= want.long_edge


@pytest.mark.asyncio
async def test_a_cached_item_resolved_for_another_model_is_re_rendered(monkeypatch):
    """The same in-memory item (a cached conversation) already holds GPT's bytes: Claude re-renders."""
    fm = _FakeFileManager()
    monkeypatch.setitem(_ext._registry, "get_cloud_file_manager", lambda: fm)
    item = ImageContent(
        file_id="pic-2",
        base64_data=base64.b64encode(MASTER).decode("ascii"),
        mime_type="image/png",
        is_resolved=True,
    )
    await _turn(fm, item, "gpt-5.4-nano", "openai_responses")
    gpt_edge = _long_edge(item)
    await _turn(fm, item, "claude-sonnet-4-6", "anthropic")
    sonnet = resolve_vision_class("claude-sonnet-4-6", "anthropic")
    assert item.vision_class == sonnet.name
    assert _long_edge(item) <= sonnet.long_edge < gpt_edge
    # And the same model again re-uses what it has (no second render).
    renders = len(fm.classes_rendered)
    await _turn(fm, item, "claude-sonnet-4-6", "anthropic")
    assert len(fm.classes_rendered) == renders


@pytest.mark.asyncio
@pytest.mark.parametrize("class_from_client", [None, "anthropic_sonnet_default"])
async def test_a_picture_the_boundary_resolved_without_bytes_is_fetched_here_once(monkeypatch, class_from_client):
    """AND-IMG17 #1: the boundary resolves a stored picture with NO bytes (a url, the access gate run). The media
    pass is the one byte fetcher: it reads the model's variant once — even when the class the client sent is
    already this model's (the boundary used to fetch those bytes itself)."""
    fm = _FakeFileManager()
    monkeypatch.setitem(_ext._registry, "get_cloud_file_manager", lambda: fm)
    item = ImageContent(
        file_id="pic-3",
        mime_type="image/png",
        resolved_url="https://cdn.example/pic-3.png",
        is_resolved=True,
        vision_class=class_from_client,
    )
    await _turn(fm, item, "claude-sonnet-4-6", "anthropic")
    assert fm.classes_rendered == ["anthropic_sonnet_default"], fm.classes_rendered
    assert item.base64_data, "the model was sent a url where its variant's bytes belong"
    assert _long_edge(item) <= VISION_API_CLASSES["anthropic_sonnet_default"].long_edge


@pytest.mark.asyncio
async def test_a_turns_pictures_are_read_side_by_side(monkeypatch):
    """AND-IMG17: the media pass is the one byte fetcher; a cold turn over 20 history photos took 17 s reading
    them one after another. Each read here takes 0.2 s: 10 pictures read in turn would take 2 s."""
    import asyncio
    import time

    class _SlowFileManager(_FakeFileManager):
        async def resolve_media_async(self, ref: Any, *, needs_bytes: bool = False) -> Any:
            await asyncio.sleep(0.2)  # the storage read: I/O, never CPU
            self.classes_rendered.append(ref.vision_class)
            ref.base64_data, ref.mime_type, ref.is_resolved = "VkFSSUFOVA==", "image/jpeg", True
            return ref

    fm = _SlowFileManager()
    monkeypatch.setitem(_ext._registry, "get_cloud_file_manager", lambda: fm)
    items = [
        ImageContent(file_id=f"pic-{i}", mime_type="image/png", resolved_url=f"https://cdn.example/{i}.png", is_resolved=True)
        for i in range(10)
    ]
    messages = _Messages([UnifiedMessage(role="user", content=[TextContent(text="what are these?"), *items])])
    started = time.monotonic()
    await UnifiedAIClient()._annotate_and_resolve_image_refs(
        messages, model_name="claude-sonnet-4-6", wire_format="anthropic", supports_vision=True
    )
    elapsed = time.monotonic() - started
    assert all(item.base64_data for item in items)
    assert elapsed < 1.0, f"10 pictures took {elapsed:.2f}s: read one after another"
