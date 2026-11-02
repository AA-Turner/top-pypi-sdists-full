"""A TUS upload over an existing path is a new VERSION of that file — never a 502.

Live evidence (2026-10-21, Lane E defect a): a TUS upload to a path that already
held a file, declaring ``expectedchecksum`` = that file's current sha256 (the
sync engine's exact overwrite), passed every check and then died at the final
PATCH with 502. Finalize always INSERTed a brand-new row at ``file_path``; the
live ``(created_by, file_path)`` key refused it and the INSERT failure was
mapped to ``s3_cld_files_insert_failed``. Every overwrite of a file large
enough to ride TUS failed; only buffered (small) overwrites worked.

The SUT is the real router + session manager over ``_tus_harness``'s doubles,
which model that unique key.
"""

from __future__ import annotations

import base64
import hashlib

import pytest
from fastapi import FastAPI, Request
from fastapi.testclient import TestClient

from matrx_files.api.router_tus import build_tus_router

from _tus_harness import BUCKET, TusWorld, build_world, chunks_of

BASE = "/files/upload/tus"
PATH = "Docs/report.txt"
V1 = b"first version of the report"
V2 = b"second version of the report, longer"


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
            request_id_provider=lambda: "req-overwrite-1",
        )
    )
    return TestClient(app)


def _upload(client: TestClient, content: bytes, **meta: str):
    create = client.post(
        BASE,
        headers={"Tus-Resumable": "1.0.0", "Upload-Length": str(len(content)), "Upload-Metadata": _meta(**meta)},
    )
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


def test_an_overwrite_with_the_current_checksum_is_a_new_version(world: TusWorld) -> None:
    client = _client(world)
    sha1 = hashlib.sha256(V1).hexdigest()
    sha2 = hashlib.sha256(V2).hexdigest()
    first = _upload(client, V1, filepath=PATH, sha256=sha1, expectedchecksum="absent")
    assert first.status_code == 204, first.text
    file_id = first.headers["X-Cld-File-Id"]
    v1_uri = world.files.rows[file_id]["storage_uri"]
    # The owner's write access, as the host access checker answers it.
    world.grants.add(("user-a", "file", file_id, "write"))

    second = _upload(client, V2, filepath=PATH, sha256=sha2, expectedchecksum=sha1)

    assert second.status_code == 204, second.text
    assert second.headers["X-Cld-File-Id"] == file_id, "an overwrite keeps the file's identity"
    live = world.live_files()
    assert len(live) == 1, f"an overwrite left {len(live)} live rows"
    row = live[0]
    assert row["checksum"] == sha2
    assert row["size_bytes"] == len(V2)
    assert row["current_version"] == 2
    key = row["storage_uri"].split(f"{BUCKET}/", 1)[1]
    assert world.object_at(key) == V2
    # Both versions stay restorable, each from its own bytes.
    by_number = {v["version_number"]: v for v in _versions(world)}
    assert set(by_number) == {1, 2}
    assert by_number[1]["checksum"] == sha1
    assert world.object_at(by_number[1]["storage_uri"].split(f"{BUCKET}/", 1)[1]) == V1
    assert by_number[1]["storage_uri"] == v1_uri or world.object_at(v1_uri.split(f"{BUCKET}/", 1)[1]) == V1
    assert world.object_at(by_number[2]["storage_uri"].split(f"{BUCKET}/", 1)[1]) == V2
    assert by_number[2]["storage_uri"] != row["storage_uri"], (
        "the version snapshot must not share the live object an in-place write overwrites"
    )


def test_a_stale_checksum_is_still_refused_with_412(world: TusWorld) -> None:
    client = _client(world)
    sha1 = hashlib.sha256(V1).hexdigest()
    assert _upload(client, V1, filepath=PATH, sha256=sha1, expectedchecksum="absent").status_code == 204
    stale = _upload(client, V2, filepath=PATH, sha256=hashlib.sha256(V2).hexdigest(), expectedchecksum="0" * 64)
    assert stale.status_code == 412, stale.text
    assert [r["checksum"] for r in world.live_files()] == [sha1]


def _versions(world: TusWorld) -> list[dict]:
    from matrx_files.cloud_sync import db as db_module

    mf, _ = db_module._models()
    return list(mf.FileVersions.rows.values())
