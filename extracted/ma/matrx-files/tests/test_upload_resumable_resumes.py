"""GUARD — a server-made file saved across several calls resumes at the stored offset, never from zero.

``FileService.upload_resumable`` keys the resumable door's session by an idempotency key. An account export's
assembler streams a ~15 GB zip through it and is stopped by every deploy (export 03411af5, 2026-11-13, lost three
whole attempts that way): the next call must ask its source only for the bytes after what storage already holds.

Checked against the real ``TUSSessionManager`` (S3, the ORM layer and host RPCs are the ``_tus_harness`` doubles):
a stop between parts keeps the session and raises ``UploadPaused``; the next call resumes at that offset; the saved
object is byte-identical; a caller that always says stop still finishes (one part per call).
"""

from __future__ import annotations

import hashlib
import os
from types import SimpleNamespace

import pytest
from _tus_harness import BUCKET, TusWorld, build_world

from matrx_files.cloud_sync.transports.tus import TUSSessionManager
from matrx_files.service import FileService, UploadPaused

OWNER = "11111111-1111-1111-1111-111111111111"
ORG = "22222222-2222-4222-8222-222222222222"
PART = 64 * 1024
SIZE = PART * 5 + 999
DATA = os.urandom(SIZE)


@pytest.fixture
def world(monkeypatch: pytest.MonkeyPatch) -> TusWorld:
    world = build_world(monkeypatch)
    manager = TUSSessionManager(world.engine, min_part_bytes=PART)
    world.engine._tus_manager = manager
    world.manager = manager
    world.org_members[ORG] = {OWNER}
    return world


def _source(asked: list[int]):
    async def source(offset: int):
        asked.append(offset)
        for at in range(offset, SIZE, 10_000):
            yield DATA[at:at + 10_000]

    return source


async def _save(world: TusWorld, asked: list[int], should_stop) -> object:
    return await FileService(SimpleNamespace(sync_engine=world.engine)).upload_resumable(
        _source(asked), size=SIZE, idempotency_key="export:abc", file_path="Documents/Account exports/x.zip",
        user_id=OWNER, organization_id=ORG, mime_type="application/zip", metadata={"k": 1},
        pathway="files.user_upload", should_stop=should_stop,
    )


async def test_a_paused_upload_resumes_at_the_stored_offset(world):
    asked: list[int] = []
    with pytest.raises(UploadPaused) as paused:  # a deploy drain says stop: one part is stored, then it pauses
        await _save(world, asked, lambda: True)
    assert paused.value.offset == PART, paused.value.offset
    saved = await _save(world, asked, lambda: False)
    assert asked == [0, PART], f"the second call did not resume at the stored offset: {asked}"
    stored = world.object_at(saved.storage_uri.split(f"s3://{BUCKET}/", 1)[-1])
    assert stored is not None and hashlib.sha256(stored).hexdigest() == hashlib.sha256(DATA).hexdigest()


async def test_a_caller_that_always_says_stop_still_finishes(world):
    asked: list[int] = []
    for _ in range(-(-SIZE // PART) + 1):
        try:
            saved = await _save(world, asked, lambda: True)
            break
        except UploadPaused:
            continue
    else:
        raise AssertionError("the upload never finished")
    assert asked == [i * PART for i in range(len(asked))], asked
    stored = world.object_at(saved.storage_uri.split(f"s3://{BUCKET}/", 1)[-1])
    assert stored == DATA
