"""AN ATTACHMENT WHOSE UPLOAD RUNS BESIDE THE CALL IS SENT FROM ITS OWN BYTES (CGU-10 AND-IMG14 #3, 2026-11-11).

A person's inline picture gets its file id BEFORE its bytes reach storage, and the upload runs beside the
provider call. The media pass must not fetch that id from storage — the file is not there yet (a wait in front
of the first token at best, a failed lookup at worst). It re-encodes the picture's OWN bytes for the model's
vision class with the same pure encoder the stored variant uses. Red when the media pass resolves an
uploading (or failed) attachment by id, or sends it un-encoded.
"""

from __future__ import annotations

import asyncio
import base64
from io import BytesIO
from typing import Any

import pytest
from PIL import Image

from matrx_ai import _ext
from matrx_ai.config.media_config import ImageContent
from matrx_ai.config.message_config import UnifiedMessage
from matrx_ai.persistence import sealed
from matrx_ai.providers.unified_client import UnifiedAIClient

_MINTED = "6b1f0c2e-0000-4000-8000-00000000a14e"


class _Messages:
    def __init__(self, messages: list[UnifiedMessage]) -> None:
        self._messages = messages

    def to_list(self) -> list[UnifiedMessage]:
        return self._messages

    def __iter__(self):
        return iter(self._messages)


class _StorageThatHasNoSuchFile:
    def __init__(self) -> None:
        self.lookups: list[str] = []

    async def resolve_media_async(self, ref: Any, *, needs_bytes: bool = False) -> Any:
        self.lookups.append(str(ref.file_id))
        raise FileNotFoundError(f"no stored file {ref.file_id}")


def _big_png() -> str:
    buf = BytesIO()
    Image.new("RGB", (3000, 2000), (40, 120, 200)).save(buf, format="PNG")
    return base64.b64encode(buf.getvalue()).decode("ascii")


@pytest.mark.asyncio
@pytest.mark.parametrize("state", ["uploading", "failed"])
async def test_an_uploading_attachment_is_encoded_from_its_bytes_never_fetched(monkeypatch, state) -> None:
    storage = _StorageThatHasNoSuchFile()
    monkeypatch.setitem(_ext._registry, "get_cloud_file_manager", lambda: storage)
    never = asyncio.get_running_loop().create_future()
    if state == "uploading":
        monkeypatch.setitem(sealed._IN_FLIGHT, _MINTED, never)
    else:
        monkeypatch.setitem(sealed._FAILED_UPLOADS, _MINTED, "ConnectionError")
    master = _big_png()
    picture = ImageContent(file_id=_MINTED, base64_data=master, mime_type="image/png")
    messages = _Messages([UnifiedMessage(role="user", content=[picture])])

    await asyncio.wait_for(
        UnifiedAIClient()._annotate_and_resolve_image_refs(
            messages, model_name="mock-model", wire_format="anthropic", supports_vision=True
        ),
        timeout=10,
    )
    never.cancel()

    assert storage.lookups == [], f"the media pass fetched an attachment by an id with no stored file: {storage.lookups}"
    assert picture.file_id == _MINTED
    assert picture.base64_data and picture.base64_data != master, "the picture was sent un-encoded"
    sent = Image.open(BytesIO(base64.b64decode(picture.base64_data)))
    assert max(sent.size) < 3000, f"not re-encoded for the vision class: {sent.size}"
