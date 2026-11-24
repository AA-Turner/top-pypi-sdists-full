"""A PICTURE WHOSE UPLOAD FAILED KEEPS ITS BYTES IN THE REQUEST SNAPSHOT (CGU-10 AND-V IMG17, finding N1).

AND-IMG17 (9c5b2d93346) has the snapshot reference a picture by its file instead of saving the bytes again. But a
person's attachment whose upload failed (or still runs beside the call) carries a MINTED file id that names no
stored file: its inline bytes are the only copy (``_bytes_are_the_only_copy``). The media pass still records it
(``_remember_media_blob``), and ``known_media_blobs`` reads it off the unified copy too, so the snapshot points at a
file that does not exist and the only copy of what the model was sent is gone. Before 9c5b2d93346 those bytes went
to the snapshot blob store.

Enabled with the fix (AND-IMG18): both doors skip a failed or still-running upload.
"""

from __future__ import annotations

import base64
import io
from typing import Any

import pytest

from matrx_ai.config.media_config import ImageContent
from matrx_ai.config.message_config import UnifiedMessage
from matrx_ai.config.unified_content import TextContent
from matrx_ai.orchestrator.execution_state import ExecutionState, _execution_state, set_execution_state
from matrx_ai.persistence import sealed
from matrx_ai.providers.snapshot_redactors import known_media_blobs, redactors_with_stored_blobs
from matrx_ai.providers.unified_client import UnifiedAIClient

MINTED = "minted-photo-never-stored"


def _jpeg() -> str:
    from PIL import Image

    import os

    buf = io.BytesIO()
    # Noise, so the picture re-encoded for the model stays over the snapshot's 64 KB inline-blob threshold
    # (a flat colour shrinks under it and the test could never see the bytes either way).
    Image.frombytes("RGB", (2400, 1800), os.urandom(2400 * 1800 * 3)).save(buf, "JPEG", quality=90)
    return base64.b64encode(buf.getvalue()).decode()


class _Messages:
    def __init__(self, messages: list[UnifiedMessage]) -> None:
        self._messages = messages

    def to_list(self) -> list[UnifiedMessage]:
        return self._messages


@pytest.fixture
def failed_upload(monkeypatch):
    monkeypatch.setitem(sealed._FAILED_UPLOADS, MINTED, "S3UploadFailed")
    from matrx_ai import _ext

    monkeypatch.setitem(_ext._registry, "get_cloud_file_manager", lambda: object())
    yield


@pytest.mark.asyncio
async def test_the_media_pass_never_names_a_file_that_was_not_stored(failed_upload) -> None:
    state = ExecutionState()
    token = set_execution_state(state)
    try:
        picture = ImageContent(base64_data=_jpeg(), mime_type="image/jpeg", file_id=MINTED)
        await UnifiedAIClient()._annotate_and_resolve_image_refs(
            _Messages([UnifiedMessage(role="user", content=[TextContent(text="what is this?"), picture])]),
            model_name="claude-sonnet-4-6", wire_format="anthropic", supports_vision=True,
        )
    finally:
        _execution_state.reset(token)
    sent = picture.base64_data
    uploads: list[str] = []

    async def store(raw: bytes, mime: str, sha: str, **_: Any) -> str:
        uploads.append(sha)
        return "snapshot-blob"

    wire = {"messages": [{"role": "user", "content": [
        {"type": "image", "source": {"type": "base64", "media_type": "image/jpeg", "data": sent}}]}]}
    await redactors_with_stored_blobs(wire, user_id="u", organization_id="o", store=store,
                                      known=dict(state.snapshot_media_blobs))
    assert uploads, "the only copy of the bytes the model was sent was referenced to a file that was never stored"


def test_the_unified_copy_never_names_a_file_that_was_not_stored(failed_upload) -> None:
    tree = {"messages": [{"content": [{"type": "image", "base64_data": _jpeg(), "file_id": MINTED}]}]}
    assert known_media_blobs(tree) == {}
