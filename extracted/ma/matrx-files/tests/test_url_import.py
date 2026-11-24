"""POST /files/import-url: a web address becomes the actor's file, fetched server-side.

The fetch is stubbed at the package's one safe external fetcher
(``_media_resolution._fetch_external_url_into_ref``) — the test proves the door
uses THAT fetcher (never its own httpx call), stores through ``upload_simple``
with the admitted organization and the carried actor, and turns every fetch
refusal into the server's own sentence with its own status.
"""

from __future__ import annotations

import base64
from types import SimpleNamespace
from typing import Any

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from matrx_files import url_import
from matrx_files.api import router_files
from matrx_files.api.router_files import build_file_router
from matrx_files.cloud_sync import _media_resolution
from matrx_utils.row_access import SHOWN_TO_TYPE_DEFAULT

FILE_ID = "00000000-0000-0000-0000-00000000cafe"
ORG = "11111111-1111-1111-1111-111111111111"
PNG = b"\x89PNG\r\n\x1a\n" + b"\x00" * 64


class _StubService:
    def __init__(self) -> None:
        self.written: list[tuple[bytes, dict[str, Any]]] = []

    async def upload_simple(self, content: bytes, **kwargs: Any):
        self.written.append((content, kwargs))
        return SimpleNamespace(
            file_id=FILE_ID,
            size_bytes=len(content),
            checksum="c" * 64,
            url=None,
            cdn_url=None,
            download_url=f"/files/{FILE_ID}/download",
            published_to_web=False,
            shown_to=None,
        )


def _client(service: _StubService, monkeypatch: pytest.MonkeyPatch) -> TestClient:
    monkeypatch.setattr(router_files, "admitted_organization_id", lambda: ORG)
    app = FastAPI()
    app.include_router(build_file_router(service, user_id_dep=lambda: "user-1"))
    return TestClient(app)


def _stub_fetch(monkeypatch: pytest.MonkeyPatch, *, content: bytes = PNG, mime: str = "image/png",
                error: str | None = None) -> list[str]:
    fetched: list[str] = []

    async def fake(ref, *, max_bytes=None, timeout_seconds=None):
        fetched.append(ref.url)
        ref.is_resolved = True
        if error:
            ref.resolver_error = error
            return
        ref.base64_data = base64.b64encode(content).decode("ascii")
        ref.mime_type = mime
        ref.file_size = len(content)

    monkeypatch.setattr(_media_resolution, "_fetch_external_url_into_ref", fake)
    return fetched


def test_import_url_stores_the_fetched_bytes_as_the_actors_file(monkeypatch):
    fetched = _stub_fetch(monkeypatch)
    service = _StubService()
    res = _client(service, monkeypatch).post(
        "/files/import-url", json={"url": "https://example.com/pics/cat.png?x=1"}
    )
    assert res.status_code == 200, res.text
    body = res.json()
    assert body["file_id"] == FILE_ID
    assert fetched == ["https://example.com/pics/cat.png?x=1"]
    content, kwargs = service.written[0]
    assert content == PNG
    assert kwargs["user_id"] == "user-1"
    assert kwargs["organization_id"] == ORG  # the admitted org, never chosen here
    assert kwargs["pathway"] == "files.import"
    assert kwargs["mime_type"] == "image/png"
    # No hand-written label: the file type's "Shown to" knob decides (stored NULL).
    assert kwargs["shown_to"] == SHOWN_TO_TYPE_DEFAULT
    assert kwargs["metadata"] == {"source_url": "https://example.com/pics/cat.png?x=1"}
    assert kwargs["file_path"].startswith("My Files/Imports/Web/cat-")
    assert kwargs["file_path"].endswith(".png")
    assert body["file_path"] == kwargs["file_path"]


@pytest.mark.parametrize(
    ("error", "status", "code", "words"),
    [
        ("external_fetch_refused: private address", 400, "url_not_public", "not a public web address"),
        ("external_fetch_http_403: Forbidden", 502, "url_fetch_http_error", "answered 403"),
        ("external_fetch_too_large: > 50 MB", 413, "url_too_large", "too large"),
        ("external_fetch_timeout: > 30s", 504, "url_fetch_timeout", "did not answer in time"),
    ],
)
def test_a_refused_fetch_is_the_servers_own_sentence(monkeypatch, error, status, code, words):
    _stub_fetch(monkeypatch, error=error)
    service = _StubService()
    res = _client(service, monkeypatch).post("/files/import-url", json={"url": "https://example.com/a.png"})
    assert res.status_code == status, res.text
    detail = res.json()["detail"]
    assert detail["error"] == code
    assert words in detail["user_message"]
    assert service.written == []


def test_a_non_web_address_is_refused_before_any_fetch(monkeypatch):
    fetched = _stub_fetch(monkeypatch)
    res = _client(_StubService(), monkeypatch).post("/files/import-url", json={"url": "file:///etc/passwd"})
    assert res.status_code == 400
    assert res.json()["detail"]["error"] == "url_not_web"
    assert fetched == []


def test_the_file_name_is_unique_per_address_and_keeps_an_extension():
    a = url_import._file_name("https://a.com/x/photo.JPG", "image/jpeg")
    b = url_import._file_name("https://b.com/x/photo.JPG", "image/jpeg")
    assert a != b and a.startswith("photo-") and a.endswith(".jpg")
    bare = url_import._file_name("https://a.com/", "image/png")
    assert bare.startswith("import-") and bare.endswith(".png")
