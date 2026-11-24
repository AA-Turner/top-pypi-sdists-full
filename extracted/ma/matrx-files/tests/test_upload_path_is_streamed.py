"""GUARD — a file already on disk is saved without its bytes ever being held whole (AD294).

``FileService.upload_simple`` takes ``bytes``, so a server-made multi-GB file (a person's whole
account export) had to be read into a task that cannot hold it. ``FileService.upload_path`` drives
the resumable door's state machine server-side: one part read at a time, then the same finalize.

Checked by running it, against the real ``TUSSessionManager`` (S3, the ORM layer and host RPCs are
the ``_tus_harness`` doubles):

1. the largest piece of the file ever read into memory is one part — never the file;
2. what lands in storage is byte-identical (``hashlib`` over what the test wrote), in the carried
   organization, stamped with the person pathway it named;
3. an automated pathway is refused before anything is written (the resumable door would drop it);
4. a failure mid-upload aborts the multipart — no half object, no live session.
"""

from __future__ import annotations

import hashlib
import os
from pathlib import Path
from types import SimpleNamespace

import pytest
from _tus_harness import BUCKET, TusWorld, build_world

from matrx_files.cloud_sync.transports.tus import TUSSessionManager
from matrx_files.service import FileService

OWNER = "11111111-1111-1111-1111-111111111111"
ORG = "22222222-2222-4222-8222-222222222222"
PART = 64 * 1024
SIZE = PART * 9 + 1234  # ten parts, the last one short


@pytest.fixture
def world(monkeypatch: pytest.MonkeyPatch) -> TusWorld:
    world = build_world(monkeypatch)
    # The durable download_url needs a public base; pin it so the test never depends on the
    # machine's PUBLIC_URL env or on another test's matrx_files.configure() leaking.
    from matrx_files.cloud_sync import render_urls

    monkeypatch.setattr(render_urls, "files_public_base_url", lambda: "https://files.test")
    manager = TUSSessionManager(world.engine, min_part_bytes=PART)
    world.engine._tus_manager = manager
    world.manager = manager
    world.org_members[ORG] = {OWNER}
    return world


def _service(world: TusWorld) -> FileService:
    return FileService(SimpleNamespace(sync_engine=world.engine))


def _big_file(tmp_path: Path) -> tuple[Path, str]:
    path = tmp_path / "export.zip"
    data = os.urandom(SIZE)
    path.write_bytes(data)
    return path, hashlib.sha256(data).hexdigest()


async def test_a_file_on_disk_is_saved_one_part_at_a_time(world, tmp_path, monkeypatch):
    path, digest = _big_file(tmp_path)
    reads: list[int] = []
    real_open = Path.open

    def counting_open(self, mode="r", *args, **kwargs):
        handle = real_open(self, mode, *args, **kwargs)
        if self == path and "b" in mode:
            real_read = handle.read

            class Counted:
                def __getattr__(self, name):
                    return getattr(handle, name)

                def __enter__(self):
                    return self

                def __exit__(self, *exc):
                    return handle.__exit__(*exc)

                def read(self, n=-1):
                    data = real_read(n)
                    reads.append(len(data))
                    return data

            return Counted()
        return handle

    monkeypatch.setattr(Path, "open", counting_open)
    saved = await _service(world).upload_path(
        path,
        file_path="Documents/Account exports/export.zip",
        user_id=OWNER,
        organization_id=ORG,
        mime_type="application/zip",
        metadata={"account_export": {"tables": 3}},
        pathway="files.user_upload",
    )

    assert reads, "the file was never read through the handle"
    assert max(reads) <= PART, f"read {max(reads):,} bytes at once for a {PART:,}-byte part"
    assert sum(reads) == SIZE and len(reads) == -(-SIZE // PART)
    stored = world.object_at(saved.storage_uri.split(f"s3://{BUCKET}/", 1)[-1])
    assert stored is not None and hashlib.sha256(stored).hexdigest() == digest
    assert saved.size_bytes == SIZE and saved.checksum == digest
    row = world.files.rows[saved.file_id]
    assert row["organization_id"] == ORG
    assert row.get("file_pathway") == "files.user_upload"
    assert (row.get("metadata") or {}).get("account_export") == {"tables": 3}
    assert saved.download_url and saved.file_id in saved.download_url


async def test_an_automated_pathway_is_refused_before_anything_is_written(world, tmp_path):
    path, _ = _big_file(tmp_path)
    with pytest.raises(ValueError, match="automated"):
        await _service(world).upload_path(
            path, file_path="x/export.zip", user_id=OWNER, organization_id=ORG,
            pathway="files.variant",
        )
    assert not world.inflight.rows and not world.live_files()


async def test_a_failure_mid_upload_aborts_the_multipart(world, tmp_path, monkeypatch):
    path, _ = _big_file(tmp_path)
    real_append = world.manager.append_async
    calls = 0

    async def failing_append(**kwargs):
        nonlocal calls
        calls += 1
        if calls == 3:
            raise ConnectionError("storage went away")
        return await real_append(**kwargs)

    monkeypatch.setattr(world.manager, "append_async", failing_append)
    with pytest.raises(ConnectionError):
        await _service(world).upload_path(
            path, file_path="x/export.zip", user_id=OWNER, organization_id=ORG
        )
    assert not world.live_files()
    assert all(r["status"] not in ("in_progress", "ready") for r in world.inflight.rows.values())
