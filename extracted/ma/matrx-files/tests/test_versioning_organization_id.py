"""files.file_versions.organization_id is NOT NULL — a version row is a CHILD
of its file and must inherit the file's organization_id, never write None.

Regression for the 2026-09-20 org-write-omission sweep: VersionManager built
the version_row dict for record_version/record_version_async/restore_version/
restore_version_async with no ``organization_id`` key at all, so every
archived-version write could 500 the caller with
``null value in column "organization_id" violates not-null constraint``.
"""

from __future__ import annotations

import asyncio

import pytest

from matrx_files.cloud_sync.config import CloudSyncConfig
from matrx_files.cloud_sync.versioning import VersionManager

ORG_ID = "11111111-1111-1111-1111-111111111111"


class _FakeRouter:
    def write(self, uri: str, content: bytes) -> None:
        pass

    async def write_async(self, uri: str, content: bytes) -> None:
        pass

    def read(self, uri: str) -> bytes:
        return b"old-bytes"

    async def read_async(self, uri: str) -> bytes:
        return b"old-bytes"


class _FakeDb:
    """Records every payload passed to create_version(_async) so the test can
    assert organization_id landed in it — the same shape a real write would
    reject with a not-null violation if it were missing."""

    def __init__(self) -> None:
        self.create_version_calls: list[dict] = []

    def create_version(self, data: dict) -> dict:
        self.create_version_calls.append(data)
        if "organization_id" not in data or data["organization_id"] is None:
            raise AssertionError(
                'null value in column "organization_id" violates not-null constraint'
            )
        return {**data, "id": "version-row-id"}

    async def create_version_async(self, data: dict) -> dict:
        return self.create_version(data)

    # -- used only by restore_version(_async) --
    def get_file(self, file_id: str) -> dict:
        return _FILE_RECORD

    async def get_file_async(self, file_id: str) -> dict:
        return _FILE_RECORD

    def get_version(self, file_id: str, version_number: int) -> dict:
        return {"storage_uri": "s3://bucket/old", "checksum": "abc"}

    async def get_version_async(self, file_id: str, version_number: int) -> dict:
        return self.get_version(file_id, version_number)

    def update_file(self, file_id: str, updates: dict, **kwargs) -> dict:
        return {**_FILE_RECORD, **updates}

    async def update_file_async(self, file_id: str, updates: dict, **kwargs) -> dict:
        return self.update_file(file_id, updates, **kwargs)

    async def _rpc(self, schema: str, fn: str, *args):
        if fn == "bump_version":
            return _FILE_RECORD["current_version"] + 1
        raise NotImplementedError(fn)


_FILE_RECORD = {
    "id": "file-id-1",
    "file_path": "reports/q1.json",
    "owner_id": "owner-id-1",
    "organization_id": ORG_ID,
    "current_version": 1,
    "storage_uri": "s3://bucket/current",
}


def _vm(db: _FakeDb) -> VersionManager:
    return VersionManager(db, _FakeRouter(), CloudSyncConfig(user_id="owner-id-1", s3_bucket="bucket"))


def test_record_version_carries_organization_id() -> None:
    db = _FakeDb()
    vm = _vm(db)
    vm.record_version(_FILE_RECORD, b"content", checksum="c1")
    assert db.create_version_calls[-1]["organization_id"] == ORG_ID


def test_record_version_async_carries_organization_id() -> None:
    db = _FakeDb()
    vm = _vm(db)
    asyncio.run(vm.record_version_async(_FILE_RECORD, b"content", checksum="c1"))
    assert db.create_version_calls[-1]["organization_id"] == ORG_ID


def test_restore_version_carries_organization_id(monkeypatch: pytest.MonkeyPatch) -> None:
    db = _FakeDb()
    vm = _vm(db)

    async def _fake_update_file_converging(*args, **kwargs):
        return {"current_version": 2, "size_bytes": 9, "checksum": "abc"}

    import matrx_files.cloud_sync.versioning as versioning_mod

    monkeypatch.setattr(
        versioning_mod, "update_file_converging", lambda *a, **k: {"current_version": 2}
    )
    vm.restore_version("file-id-1", 1, user_id="owner-id-1")
    assert db.create_version_calls[-1]["organization_id"] == ORG_ID


def test_restore_version_async_carries_organization_id(monkeypatch: pytest.MonkeyPatch) -> None:
    db = _FakeDb()
    vm = _vm(db)

    import matrx_files.cloud_sync.versioning as versioning_mod

    async def _fake_update_file_converging_async(*args, **kwargs):
        return {"current_version": 2, "size_bytes": 9, "checksum": "abc"}

    monkeypatch.setattr(
        versioning_mod, "update_file_converging_async", _fake_update_file_converging_async
    )
    asyncio.run(vm.restore_version_async("file-id-1", 1, user_id="owner-id-1"))
    assert db.create_version_calls[-1]["organization_id"] == ORG_ID
