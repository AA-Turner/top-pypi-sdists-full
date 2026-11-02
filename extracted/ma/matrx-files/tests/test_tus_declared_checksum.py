"""A completed sync upload never lands with checksum NULL (SPEC-SERVER §5).

The TUS path takes its checksum from S3's ``ChecksumSHA256`` on
complete_multipart_upload and deliberately lands ``checksum = NULL`` when S3
cannot supply a FULL_OBJECT value -- so the very uploads a sync client uses for
large files are the ones most likely to arrive unverifiable, and NULL-checksum
rows are excluded from the dedup index entirely.

The contract: the client declares ``sha256`` in Upload-Metadata; the server
verifies it against S3's FULL_OBJECT checksum when there is one and against a
STREAMED re-hash of the assembled object when there is not; a mismatch is 422
with the object purged and no row created; and a declared checksum that cannot
be verified FAILS the upload rather than landing unverifiable. Uploads that
declare nothing keep today's behavior exactly.

A composite (``<b64>-<n>``) checksum is never accepted as a full-object one: it
is a hash of part hashes and does not identify the bytes.
"""

from __future__ import annotations

import base64
import hashlib

import pytest
from _tus_harness import FakeS3Client, TusWorld, build_world, chunks_of
from fastapi import FastAPI, Request
from fastapi.testclient import TestClient

from matrx_files.api.router_tus import build_tus_router

BASE = "/files/upload/tus"
OCTET = "application/offset+octet-stream"
CONTENT = b"AAAABBBBCC"
SHA = hashlib.sha256(CONTENT).hexdigest()


def _meta(**kv: str) -> str:
    return ",".join(f"{k} {base64.b64encode(v.encode()).decode()}" for k, v in kv.items())


def _client(world: TusWorld) -> TestClient:
    def user_id_dep(request: Request) -> str:
        return request.headers.get("x-test-user", "user-a")

    app = FastAPI()
    app.include_router(
        build_tus_router(
            file_manager_dep=lambda: world.file_manager,
            user_id_dep=user_id_dep,
            request_id_provider=lambda: "req-checksum-1",
        )
    )
    return TestClient(app)


def _upload(client: TestClient, world: TusWorld, *, metadata: str, content: bytes = CONTENT):
    create = client.post(
        BASE,
        headers={
            "Tus-Resumable": "1.0.0",
            "Upload-Length": str(len(content)),
            "Upload-Metadata": metadata,
        },
    )
    assert create.status_code == 201, create.text
    location = create.headers["Location"]
    offset = 0
    last = create
    for chunk in chunks_of(content):
        last = client.patch(
            location,
            content=chunk,
            headers={
                "Tus-Resumable": "1.0.0",
                "Upload-Offset": str(offset),
                "Content-Type": OCTET,
            },
        )
        if last.status_code >= 400:
            return last
        offset += len(chunk)
    return last


@pytest.fixture
def world(monkeypatch: pytest.MonkeyPatch) -> TusWorld:
    return build_world(monkeypatch)


def test_a_declared_checksum_matching_s3_is_stored(world: TusWorld) -> None:
    client = _client(world)
    resp = _upload(client, world, metadata=_meta(filepath="Docs/a.txt", sha256=SHA))
    assert resp.status_code == 204, resp.text
    row = next(reversed(list(world.files.rows.values())))
    assert row["checksum"] == SHA


def test_a_mismatch_is_422_with_no_row_and_no_object(world: TusWorld) -> None:
    """A corrupt transfer must never become a file."""
    wrong = SHA[:-1] + ("0" if SHA[-1] != "0" else "1")
    client = _client(world)
    before = len(world.files.rows)
    resp = _upload(client, world, metadata=_meta(filepath="Docs/b.txt", sha256=wrong))
    assert resp.status_code == 422, resp.text
    assert resp.json()["detail"]["error"] == "checksum_mismatch"
    assert len(world.files.rows) == before, "a corrupt upload created a file row"
    assert world.s3.objects == {}, "the corrupt object was left in the bucket"


def test_no_full_object_checksum_falls_back_to_a_streamed_rehash(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """S3 refusing FULL_OBJECT must not mean an unverified file.

    This is the live behavior on buckets that reject the FULL_OBJECT multipart
    option -- exactly the path large sync uploads take.
    """
    world = build_world(monkeypatch, s3=FakeS3Client(reject_full_object_sha256=True))
    client = _client(world)
    resp = _upload(client, world, metadata=_meta(filepath="Docs/c.txt", sha256=SHA))
    assert resp.status_code == 204, resp.text
    row = next(reversed(list(world.files.rows.values())))
    assert row["checksum"] == SHA, (
        "with no FULL_OBJECT checksum from S3 the server must re-hash the "
        "assembled object rather than land the row unverifiable"
    )


def test_a_declared_checksum_that_cannot_be_verified_fails_the_upload(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """S12: declaring a checksum IS asking for verification.

    Landing the row with checksum NULL would silently give the client the
    opposite of what it asked for -- and exclude the row from dedup.
    """
    s3 = FakeS3Client(reject_full_object_sha256=True)

    def _unreadable(**kwargs):
        raise RuntimeError("object store read failed")

    s3.get_object = _unreadable  # type: ignore[method-assign]
    world = build_world(monkeypatch, s3=s3)
    client = _client(world)
    before = len(world.files.rows)
    resp = _upload(client, world, metadata=_meta(filepath="Docs/d.txt", sha256=SHA))
    assert resp.status_code == 422, resp.text
    assert resp.json()["detail"]["error"] == "checksum_unverifiable"
    assert len(world.files.rows) == before


def test_declaring_nothing_keeps_todays_behaviour(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """No declaration, no new refusal: existing callers are untouched."""
    world = build_world(monkeypatch, s3=FakeS3Client(reject_full_object_sha256=True))
    client = _client(world)
    resp = _upload(client, world, metadata=_meta(filepath="Docs/e.txt"))
    assert resp.status_code == 204, resp.text
    assert next(reversed(list(world.files.rows.values())))["checksum"] is None


def test_absent_is_not_a_checksum(world: TusWorld) -> None:
    """'absent' is a PRECONDITION value; accepting it as a hash would be nonsense."""
    client = _client(world)
    resp = client.post(
        BASE,
        headers={
            "Tus-Resumable": "1.0.0",
            "Upload-Length": str(len(CONTENT)),
            "Upload-Metadata": _meta(filepath="Docs/f.txt", sha256="absent"),
        },
    )
    assert resp.status_code == 400
    assert resp.json()["detail"]["error"] == "invalid_declared_checksum"


def test_transport_keys_do_not_leak_into_file_metadata(world: TusWorld) -> None:
    client = _client(world)
    resp = _upload(client, world, metadata=_meta(filepath="Docs/g.txt", sha256=SHA))
    assert resp.status_code == 204, resp.text
    metadata = next(reversed(list(world.files.rows.values()))).get("metadata") or {}
    for key in ("sha256", "expectedchecksum", "deviceid", "clientmodifiedat"):
        assert key not in metadata
    for key in metadata:
        assert not key.startswith("_sync_"), f"session transport state leaked as {key}"
