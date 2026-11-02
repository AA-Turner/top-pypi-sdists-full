from __future__ import annotations

from types import SimpleNamespace
from typing import Any, cast

from fastapi import FastAPI
from fastapi.testclient import TestClient

from matrx_files.api import build_share_router
from matrx_files.cloud_sync.download_stream import StreamingResult


class _Permissions:
    async def resolve_share_link_async(self, token: str) -> dict[str, str] | None:
        if token == "valid-token":
            return {"resource_type": "file", "resource_id": "file-1"}
        return None


class _Streamer:
    async def open_stream(
        self,
        record: dict[str, Any],
        *,
        range_header: str | None = None,
        allow_inline: bool = False,
    ) -> StreamingResult:
        disposition = "inline" if allow_inline else "attachment"
        return StreamingResult(
            iterator=iter([b"image-bytes"]),
            media_type="image/png",
            headers={
                "Content-Disposition": f'{disposition}; filename="image.png"',
                "Content-Length": "11",
                **({"Content-Range": "bytes 0-10/11"} if range_header else {}),
            },
            status_code=206 if range_header else 200,
            content_length=11,
        )


class _Service:
    def __init__(self) -> None:
        self.sync_engine = SimpleNamespace(
            permissions=_Permissions(),
            streamer=_Streamer(),
        )

    async def read_record_unchecked(self, file_id: str) -> dict[str, Any] | None:
        return {"id": file_id, "file_name": "image.png", "mime_type": "image/png"}


def _client() -> TestClient:
    app = FastAPI()
    app.include_router(build_share_router(cast(Any, _Service())))
    return TestClient(app)


def test_clean_share_url_streams_inline_media() -> None:
    response = _client().get("/share/valid-token")

    assert response.status_code == 200
    assert response.content == b"image-bytes"
    assert response.headers["content-type"] == "image/png"
    assert response.headers["content-disposition"].startswith("inline;")
    assert response.headers["x-content-type-options"] == "nosniff"


def test_legacy_download_url_remains_embeddable_and_can_force_attachment() -> None:
    client = _client()

    legacy = client.get("/share/valid-token/download")
    attachment = client.get("/share/valid-token/download?inline=false")

    assert legacy.status_code == 200
    assert legacy.headers["content-disposition"].startswith("inline;")
    assert attachment.status_code == 200
    assert attachment.headers["content-disposition"].startswith("attachment;")


def test_invalid_share_token_is_not_publicly_readable() -> None:
    response = _client().get("/share/invalid-token")

    assert response.status_code == 404
    assert response.json()["detail"]["error"] == "share_link_invalid"


# --- Access ladder T-19b: a shared chat's attachments ride the chat's token ---


class _ChildPermissions(_Permissions):
    async def resolve_share_child_file_async(
        self, token: str, file_id: str
    ) -> dict[str, str] | None:
        # Only chat-token + its own attachment is a child; everything else is not.
        if token == "chat-token" and file_id == "11111111-1111-1111-1111-111111111111":
            return {
                "file_id": file_id,
                "resource_type": "conversation",
                "resource_id": "c-1",
            }
        return None


class _ChildService(_Service):
    def __init__(self) -> None:
        self.sync_engine = SimpleNamespace(
            permissions=_ChildPermissions(),
            streamer=_Streamer(),
        )
        self.read_ids: list[str] = []

    async def read_record_unchecked(self, file_id: str) -> dict[str, Any] | None:
        self.read_ids.append(file_id)
        return await super().read_record_unchecked(file_id)


def test_a_shared_chat_token_streams_its_own_attachment_inline_or_as_download() -> None:
    service = _ChildService()
    app = FastAPI()
    app.include_router(build_share_router(cast(Any, service)))
    client = TestClient(app)

    inline = client.get("/share/chat-token/files/11111111-1111-1111-1111-111111111111")
    download = client.get(
        "/share/chat-token/files/11111111-1111-1111-1111-111111111111?inline=false"
    )

    assert inline.status_code == 200
    assert inline.content == b"image-bytes"
    assert inline.headers["content-disposition"].startswith("inline;")
    assert download.headers["content-disposition"].startswith("attachment;")
    assert inline.headers["cache-control"] == "private, no-store"


def test_a_shared_chat_token_reaches_no_other_file_and_never_reads_it() -> None:
    service = _ChildService()
    app = FastAPI()
    app.include_router(build_share_router(cast(Any, service)))
    client = TestClient(app)

    other_file = client.get("/share/chat-token/files/22222222-2222-2222-2222-222222222222")
    other_token = client.get("/share/other-token/files/11111111-1111-1111-1111-111111111111")

    assert other_file.status_code == 404
    assert other_token.status_code == 404
    # The authorization answered first: no record was ever loaded for a refusal.
    assert service.read_ids == []
