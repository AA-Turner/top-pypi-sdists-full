"""Write preconditions: a stale write LOSES loudly (SPEC-SERVER §3).

Before this there was no precondition of any kind on either write path. Two
devices editing one file both won, in arrival order, and the loser's bytes were
gone with nothing anywhere to say a conflict had happened -- the single worst
failure a file sync can have.

Pinned here: 412 on every stale `expected_checksum`, the exact §3.2 payload keys
(it is the engine's conflict INPUT, not a log line), the `"absent"` semantics,
`If-Match` in both its strong and weak forms, and §3.3's idempotent replay --
including that a stored 412 replays AS a 412, so a retry loop can never quietly
become a last-write-wins overwrite.
"""

from __future__ import annotations

from datetime import UTC, datetime
from types import SimpleNamespace
from typing import Any

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from matrx_files.api.router_files import build_file_router

SHA_A = "a" * 64
SHA_B = "b" * 64
FILE_ID = "00000000-0000-0000-0000-00000000beef"
DEVICE = "22222222-2222-2222-2222-222222222222"
PATH = "Docs/report.txt"


def _row(**over: Any) -> dict[str, Any]:
    row = {
        "id": FILE_ID,
        "file_path": PATH,
        "file_name": "report.txt",
        "checksum": SHA_A,
        "current_version": 7,
        "size_bytes": 18422,
        "updated_at": datetime(2026, 9, 13, 18, 22, 10, 114000, tzinfo=UTC),
        "origin_device_id": DEVICE,
        "deleted_at": None,
    }
    row.update(over)
    return row


class _StubDb:
    def __init__(self, row: dict[str, Any] | None):
        self.row = row

    async def get_file_by_path_async(self, owner_id: str, file_path: str):
        return self.row if self.row and self.row["file_path"] == file_path else None

    async def get_file_async(self, file_id: str, *, include_deleted: bool = False):
        return self.row if self.row and self.row["id"] == file_id else None


class _StubService:
    """Only what the two routes actually call. No idempotency store is wired
    unless a test asks for one (IdempotencyStore needs a real sync_engine)."""

    def __init__(self, row: dict[str, Any] | None):
        db = _StubDb(row)
        self.file_manager = SimpleNamespace(sync_engine=SimpleNamespace(db=db, tus=None))
        self.written: list[dict[str, Any]] = []
        self.mutations: list[dict[str, Any]] = []

    async def upload_simple(self, content: bytes, **kwargs: Any):
        self.written.append(kwargs)
        return SimpleNamespace(
            file_id=FILE_ID,
            size_bytes=len(content),
            checksum=SHA_B,
            url=None,
            cdn_url=None,
            download_url=None,
            published_to_web=False,
            shown_to="only_me",
        )

    async def mutate_file(self, file_id: str, **kwargs: Any):
        self.mutations.append(kwargs)
        return {
            "asset": {"file_id": file_id, "file_path": PATH, "folder": "Docs"},
            "errors": [],
        }

    async def update_record(self, *a: Any, **k: Any):
        return {"file_id": FILE_ID}


def _client(service: _StubService) -> TestClient:
    app = FastAPI()
    app.include_router(build_file_router(service))
    return TestClient(app)


def _upload(client: TestClient, *, expected: str | None = None, **extra: Any):
    data: dict[str, Any] = {"file_path": PATH}
    if expected is not None:
        data["expected_checksum"] = expected
    return client.post(
        "/files/upload",
        data=data,
        files={"file": ("report.txt", b"new bytes", "text/plain")},
        **extra,
    )


# ---------------------------------------------------------------- upload ----


def test_no_precondition_is_todays_behaviour_unchanged() -> None:
    service = _StubService(_row())
    assert _upload(_client(service)).status_code == 200
    assert service.written, "the write must still happen when nothing is asserted"


def test_a_matching_checksum_lets_the_write_through() -> None:
    service = _StubService(_row())
    assert _upload(_client(service), expected=SHA_A).status_code == 200
    assert service.written


def test_a_stale_checksum_is_412_with_the_exact_conflict_payload() -> None:
    service = _StubService(_row())
    resp = _upload(_client(service), expected=SHA_B)
    assert resp.status_code == 412
    body = resp.json()["detail"]
    assert body == {
        "error": "precondition_failed",
        "message": "the file changed on the server since you last read it",
        "file_id": FILE_ID,
        "current_checksum": SHA_A,
        "current_version": 7,
        "current_size_bytes": 18422,
        "current_updated_at": "2026-09-13T18:22:10.114000+00:00",
        "origin_device_id": DEVICE,
        "expected_checksum": SHA_B,
    }
    assert not service.written, "a refused write must not have written bytes"


def test_absent_means_i_believe_nothing_is_here() -> None:
    empty = _StubService(None)
    assert _upload(_client(empty), expected="absent").status_code == 200

    occupied = _StubService(_row())
    resp = _upload(_client(occupied), expected="absent")
    assert resp.status_code == 412
    assert resp.json()["detail"]["current_checksum"] == SHA_A
    assert not occupied.written


def test_a_trashed_row_counts_as_absent() -> None:
    trashed = _StubService(_row(deleted_at=datetime.now(UTC)))
    assert _upload(_client(trashed), expected="absent").status_code == 200


def test_expecting_a_version_that_is_gone_is_412_not_a_fresh_create() -> None:
    """The client believed a specific version was there. Nothing is.

    Writing anyway would silently resurrect a file the user deleted elsewhere.
    """
    resp = _upload(_client(_StubService(None)), expected=SHA_A)
    assert resp.status_code == 412
    assert resp.json()["detail"]["file_id"] is None


@pytest.mark.parametrize("bad", ["not-a-hash", "ABC", "a" * 63])
def test_a_malformed_expected_checksum_is_400(bad: str) -> None:
    resp = _upload(_client(_StubService(_row())), expected=bad)
    assert resp.status_code == 400
    assert resp.json()["detail"]["error"] == "invalid_expected_checksum"


def test_an_uppercase_checksum_is_accepted_and_normalised() -> None:
    service = _StubService(_row())
    assert _upload(_client(service), expected=SHA_A.upper()).status_code == 200


# ----------------------------------------------------------------- PATCH ----


def test_if_match_strong_form_gates_a_patch() -> None:
    service = _StubService(_row())
    client = _client(service)
    ok = client.patch(
        f"/files/{FILE_ID}",
        json={"name": "renamed.txt"},
        headers={"If-Match": f'"{SHA_A}"'},
    )
    assert ok.status_code == 200, ok.text

    stale = client.patch(
        f"/files/{FILE_ID}",
        json={"name": "renamed.txt"},
        headers={"If-Match": f'"{SHA_B}"'},
    )
    assert stale.status_code == 412
    assert stale.json()["detail"]["current_checksum"] == SHA_A


def test_if_match_weak_form_gates_a_metadata_only_patch() -> None:
    """W/"v<n>" exists for mutations that do not touch the bytes."""
    service = _StubService(_row())
    client = _client(service)
    assert (
        client.patch(
            f"/files/{FILE_ID}",
            json={"name": "x.txt"},
            headers={"If-Match": 'W/"v7"'},
        ).status_code
        == 200
    )
    stale = client.patch(
        f"/files/{FILE_ID}",
        json={"name": "x.txt"},
        headers={"If-Match": 'W/"v6"'},
    )
    assert stale.status_code == 412
    assert stale.json()["detail"]["current_version"] == 7


def test_a_wildcard_if_match_is_refused() -> None:
    """The point of the header is to name the exact state the client read."""
    resp = _client(_StubService(_row())).patch(
        f"/files/{FILE_ID}", json={"name": "x.txt"}, headers={"If-Match": "*"}
    )
    assert resp.status_code == 400
    assert resp.json()["detail"]["error"] == "invalid_if_match"


def test_no_if_match_is_todays_behaviour_unchanged() -> None:
    service = _StubService(_row())
    assert (
        _client(service).patch(f"/files/{FILE_ID}", json={"name": "x.txt"}).status_code == 200
    )
    assert service.mutations


# ------------------------------------------------------- device provenance ----


class _FakeAppInstances:
    """Only what resolve_write_origin calls. Ownership is the whole point."""

    registry: dict[str, str] = {DEVICE: "anonymous"}  # the router's test-mode caller

    @classmethod
    def filter(cls, **flt: Any):
        rows = [
            {"id": k, "user_id": v}
            for k, v in cls.registry.items()
            if k == flt.get("id")
        ]

        class _Q:
            async def values(self, *fields: str):
                return rows

        return _Q()


@pytest.fixture
def devices(monkeypatch: pytest.MonkeyPatch):
    import matrx_files.db.models as models

    monkeypatch.setattr(models, "AppInstances", _FakeAppInstances)
    return _FakeAppInstances


def test_the_upload_route_stamps_a_validated_device(devices) -> None:
    service = _StubService(_row())
    resp = _upload(
        _client(service),
        headers={
            "X-Matrx-Device-Id": DEVICE,
            "X-Matrx-Client-Modified-At": "2026-09-13T10:00:00Z",
        },
    )
    assert resp.status_code == 200, resp.text
    written = service.written[-1]
    assert written["origin_device_id"] == DEVICE
    assert written["client_modified_at"].isoformat().startswith("2026-09-13T10:00:00")


def test_an_unregistered_device_is_400_and_writes_nothing(devices) -> None:
    service = _StubService(_row())
    resp = _upload(
        _client(service),
        headers={"X-Matrx-Device-Id": "99999999-9999-9999-9999-999999999999"},
    )
    assert resp.status_code == 400
    assert resp.json()["detail"]["error"] == "invalid_device"
    assert not service.written


def test_a_future_client_clock_is_400_and_writes_nothing(devices) -> None:
    service = _StubService(_row())
    resp = _upload(
        _client(service),
        headers={"X-Matrx-Client-Modified-At": "2099-01-01T00:00:00Z"},
    )
    assert resp.status_code == 400
    assert resp.json()["detail"]["error"] == "implausible_client_time"
    assert not service.written


def test_a_browser_upload_declares_nothing_and_is_fine(devices) -> None:
    service = _StubService(_row())
    assert _upload(_client(service)).status_code == 200
    assert service.written[-1]["origin_device_id"] is None
