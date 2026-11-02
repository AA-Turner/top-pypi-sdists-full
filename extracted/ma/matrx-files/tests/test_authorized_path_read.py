from __future__ import annotations

from types import SimpleNamespace

import pytest

from matrx_files.service import FileService


class _DB:
    def __init__(self, record: dict | None) -> None:
        self.record = record

    async def get_file_by_path_async(self, owner_id: str, file_path: str) -> dict | None:
        assert owner_id == "owner-1"
        assert file_path == "reports/q3.txt"
        return self.record


class _Engine:
    def __init__(self, record: dict | None) -> None:
        self.db = _DB(record)
        self.authorized: list[tuple[str, str, str]] = []

    async def get_authorized_record_async(
        self, file_id: str, *, user_id: str, level: str, include_deleted: bool = False
    ) -> dict:
        self.authorized.append((file_id, user_id, level))
        if user_id == "denied":
            raise PermissionError("denied")
        assert self.db.record is not None
        return self.db.record


def _service(record: dict | None) -> tuple[FileService, _Engine]:
    engine = _Engine(record)
    return FileService(SimpleNamespace(sync_engine=engine)), engine  # type: ignore[arg-type]


@pytest.mark.asyncio
async def test_path_lookup_passes_through_the_authorized_record_gate() -> None:
    service, engine = _service({"id": "file-1", "organization_id": "org-1"})

    row = await service.read_record_by_path(
        "owner-1", "reports/q3.txt", user_id="actor-1", level="write"
    )

    assert row == {"id": "file-1", "organization_id": "org-1"}
    assert engine.authorized == [("file-1", "actor-1", "write")]


@pytest.mark.asyncio
async def test_tenant_scope_is_applied_only_after_access_is_decided() -> None:
    service, engine = _service({"id": "file-1", "organization_id": "org-2"})

    row = await service.read_record_by_path(
        "owner-1",
        "reports/q3.txt",
        user_id="actor-1",
        organization_id="org-1",
    )

    assert row is None
    assert engine.authorized == [("file-1", "actor-1", "read")]


@pytest.mark.asyncio
async def test_tenant_scope_never_turns_a_denial_into_absence() -> None:
    service, _ = _service({"id": "file-1", "organization_id": "org-2"})

    with pytest.raises(PermissionError, match="denied"):
        await service.read_record_by_path(
            "owner-1",
            "reports/q3.txt",
            user_id="denied",
            organization_id="org-1",
        )
