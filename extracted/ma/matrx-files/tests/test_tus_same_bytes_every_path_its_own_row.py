"""Every path a TUS upload names gets its own files.files row — even for bytes
that already exist elsewhere.

Live evidence (2026-10-21, walker): upload ``a.txt``, then ``b.txt`` with the
same content — both PATCHes answered ``X-Cld-File-Id: a1a0078b...`` (the FIRST
file) and no row ever appeared at ``b.txt``. The TUS dedup gate short-circuited
to the canonical row exactly like an implicit alias, so the placement the sync
client asked for was recorded nowhere and the desktop kept replanning it.

The doctrine already holds for the buffered door
(``test_placement_survives_dedup.py``): a declared placement gets a ROW OF ITS
OWN, linked to the canonical content by ``duplicate_of_file_id``. A TUS upload
always declares its placement (``filepath`` is mandatory).

Also: an idempotency key replayed for a DIFFERENT path or length must be
refused, never answered with the other upload's session (and file id).
"""

from __future__ import annotations

import base64
import hashlib

import pytest
from fastapi import FastAPI, Request
from fastapi.testclient import TestClient

from _tus_harness import TusWorld, build_world, chunks_of
from matrx_files.api.router_tus import build_tus_router

BASE = "/files/upload/tus"
SAME = b"identical bytes in two places"


def _meta(**kv: str) -> str:
    return ",".join(f"{k} {base64.b64encode(v.encode()).decode()}" for k, v in kv.items())


@pytest.fixture
def world(monkeypatch: pytest.MonkeyPatch) -> TusWorld:
    return build_world(monkeypatch)


def _client(world: TusWorld) -> TestClient:
    def user_id_dep(request: Request) -> str:
        return "user-a"

    app = FastAPI()
    app.include_router(
        build_tus_router(
            file_manager_dep=lambda: world.file_manager,
            user_id_dep=user_id_dep,
            request_id_provider=lambda: "req-placement-1",
        )
    )
    return TestClient(app)


def _create(client: TestClient, content: bytes, key: str | None = None, **meta: str):
    headers = {"Tus-Resumable": "1.0.0", "Upload-Length": str(len(content)), "Upload-Metadata": _meta(**meta)}
    if key:
        headers["X-Idempotency-Key"] = key
    return client.post(BASE, headers=headers)


def _upload(client: TestClient, content: bytes, key: str | None = None, **meta: str):
    create = _create(client, content, key, **meta)
    if create.status_code != 201:
        return create
    offset, last = 0, create
    for chunk in chunks_of(content):
        last = client.patch(
            create.headers["Location"],
            content=chunk,
            headers={"Tus-Resumable": "1.0.0", "Upload-Offset": str(offset), "Content-Type": "application/offset+octet-stream"},
        )
        if last.status_code >= 400:
            return last
        offset += len(chunk)
    return last


def test_same_bytes_at_a_second_path_get_their_own_row(world: TusWorld) -> None:
    client = _client(world)
    sha = hashlib.sha256(SAME).hexdigest()
    a = _upload(client, SAME, filepath="Docs/a.txt", sha256=sha, expectedchecksum="absent")
    b = _upload(client, SAME, filepath="Docs/b.txt", sha256=sha, expectedchecksum="absent")
    assert a.status_code == 204 and b.status_code == 204, (a.text, b.text)

    a_id, b_id = a.headers["X-Cld-File-Id"], b.headers["X-Cld-File-Id"]
    assert a_id != b_id, "the second path was answered with the first file's id"
    by_path = {r["file_path"]: r for r in world.live_files()}
    assert set(by_path) == {"Docs/a.txt", "Docs/b.txt"}
    assert str(by_path["Docs/b.txt"]["id"]) == b_id
    assert str(by_path["Docs/b.txt"]["duplicate_of_file_id"]) == a_id
    assert by_path["Docs/b.txt"]["checksum"] == sha


def test_an_idempotency_key_reused_for_another_path_is_refused(world: TusWorld) -> None:
    client = _client(world)
    first = _create(client, SAME, "k-1", filepath="Docs/a.txt")
    assert first.status_code == 201, first.text
    reused = _create(client, SAME, "k-1", filepath="Docs/b.txt")
    assert reused.status_code == 409, reused.text
    assert "idempotency_key_reuse" in reused.text
    # The honest replay (same key, same path, same length) still resumes.
    replay = _create(client, SAME, "k-1", filepath="Docs/a.txt")
    assert replay.status_code == 201 and replay.headers["Location"] == first.headers["Location"]
