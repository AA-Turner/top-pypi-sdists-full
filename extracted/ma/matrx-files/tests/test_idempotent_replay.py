"""Idempotent replay of a buffered upload (SPEC-SERVER §3.3).

A sync daemon retries. Without memoization, a retry after a `kill -9` mid-upload
uploads the file twice; with memoization but no precondition in the key's
fingerprint, a retry of a LOSING write could silently become a winning one.

Three rules, each pinned here:
  1. same key + same precondition -> the STORED response, never a re-upload;
  2. same key + a DIFFERENT precondition -> 409 idempotency_key_reuse;
  3. a 412 is stored under the key, so a losing write loses IDENTICALLY.
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
PATH = "Docs/report.txt"
KEY = "idem-key-1"


class _FakeIdempotencyTable:
    """The two operations IdempotencyStore actually uses, with real UPSERT
    semantics on (owner_id, idempotency_key)."""

    def __init__(self) -> None:
        self.rows: dict[tuple[str, str], dict[str, Any]] = {}

    def filter(self, **flt: Any):
        rows = [
            r
            for r in self.rows.values()
            if all(r.get(k) == v for k, v in flt.items())
        ]

        class _Q:
            def limit(self, _n: int):
                return self

            async def values(self, *fields: str):
                return [{f: r.get(f) for f in fields} for r in rows]

        return _Q()

    async def upsert(self, values: dict[str, Any], *, on_conflict: list[str]) -> None:
        self.rows[(values["owner_id"], values["idempotency_key"])] = dict(values)


class _StubDb:
    def __init__(self, row: dict[str, Any] | None):
        self.row = row

    async def get_file_by_path_async(self, owner_id: str, file_path: str):
        return self.row

    async def get_file_async(self, file_id: str, **_: Any):
        return self.row


class _StubService:
    def __init__(self, row: dict[str, Any] | None):
        self.file_manager = SimpleNamespace(
            sync_engine=SimpleNamespace(db=_StubDb(row), tus=None)
        )
        self.uploads = 0
        self.upload_kwargs: dict[str, Any] | None = None
        self.permissions = SimpleNamespace(create_share_link_async=self._create_share_link)
        self.share_link_creations = 0

    async def _create_share_link(self, *_: Any, **__: Any) -> dict[str, str]:
        self.share_link_creations += 1
        return {"token": "anyone-token"}

    async def upload_simple(self, content: bytes, **kwargs: Any):
        self.uploads += 1
        self.upload_kwargs = kwargs
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


def _row() -> dict[str, Any]:
    return {
        "id": FILE_ID,
        "file_path": PATH,
        "checksum": SHA_A,
        "current_version": 7,
        "size_bytes": 10,
        "updated_at": datetime(2026, 9, 13, tzinfo=UTC),
        "origin_device_id": None,
        "deleted_at": None,
    }


@pytest.fixture
def table(monkeypatch: pytest.MonkeyPatch) -> _FakeIdempotencyTable:
    t = _FakeIdempotencyTable()
    monkeypatch.setattr(
        "matrx_files.cloud_sync.idempotency._models",
        lambda: (SimpleNamespace(Idempotency=t), SimpleNamespace()),
    )
    return t


def _client(service: _StubService) -> TestClient:
    app = FastAPI()
    app.include_router(build_file_router(service))
    return TestClient(app)


def _upload(
    client: TestClient,
    *,
    expected: str,
    key: str = KEY,
    visibility: str | None = None,
    published_to_web: str | None = None,
):
    data = {"file_path": PATH, "expected_checksum": expected}
    if visibility is not None:
        data["visibility"] = visibility
    if published_to_web is not None:
        data["published_to_web"] = published_to_web
    return client.post(
        "/files/upload",
        data=data,
        files={"file": ("report.txt", b"new bytes", "text/plain")},
        headers={"X-Idempotency-Key": key},
    )


def test_a_replay_returns_the_stored_response_and_does_not_re_upload(
    table: _FakeIdempotencyTable,
) -> None:
    service = _StubService(_row())
    client = _client(service)

    first = _upload(client, expected=SHA_A)
    assert first.status_code == 200, first.text
    assert service.uploads == 1

    second = _upload(client, expected=SHA_A)
    assert second.status_code == 200
    assert second.json() == first.json()
    assert service.uploads == 1, "the replay re-uploaded the bytes"


def test_a_stored_412_replays_as_a_412(table: _FakeIdempotencyTable) -> None:
    service = _StubService(_row())
    client = _client(service)

    first = _upload(client, expected=SHA_B)
    assert first.status_code == 412
    assert service.uploads == 0

    second = _upload(client, expected=SHA_B)
    assert second.status_code == 412, (
        "a losing write must lose identically on retry -- replaying a stored 412 "
        "as a success would turn a retry loop into a last-write-wins overwrite"
    )
    assert second.json()["detail"] == first.json()["detail"]
    assert service.uploads == 0


def test_reusing_one_key_for_a_different_request_is_409(
    table: _FakeIdempotencyTable,
) -> None:
    service = _StubService(_row())
    client = _client(service)

    assert _upload(client, expected=SHA_A).status_code == 200
    clash = _upload(client, expected="absent")
    assert clash.status_code == 409
    assert clash.json()["detail"]["error"] == "idempotency_key_reuse"
    assert clash.json()["detail"]["idempotency_key"] == KEY
    assert service.uploads == 1, "the clashing request must not have been performed"


@pytest.mark.parametrize(("first_visibility", "replay_visibility"), ((None, "link"), ("link", None)))
def test_reusing_one_key_for_a_different_access_intent_is_409(
    table: _FakeIdempotencyTable, first_visibility: str | None, replay_visibility: str | None
) -> None:
    service = _StubService(_row())
    client = _client(service)

    assert _upload(client, expected=SHA_A, visibility=first_visibility).status_code == 200
    clash = _upload(client, expected=SHA_A, visibility=replay_visibility)
    assert clash.status_code == 409
    assert clash.json()["detail"]["error"] == "idempotency_key_reuse"
    assert service.uploads == 1


def test_explicit_private_access_wins_over_legacy_link(
    table: _FakeIdempotencyTable,
) -> None:
    service = _StubService(_row())
    client = _client(service)

    response = _upload(
        client, expected=SHA_A, visibility="link", published_to_web="false"
    )
    assert response.status_code == 200, response.text
    assert response.json()["share_token"] is None
    assert service.share_link_creations == 0


@pytest.mark.parametrize(
    ("spelling", "expected"), (("t", True), ("f", False), ("y", True), ("n", False))
)
def test_legacy_fastapi_boolean_spellings_stay_accepted(
    table: _FakeIdempotencyTable, spelling: str, expected: bool
) -> None:
    service = _StubService(_row())
    response = _upload(
        _client(service),
        expected=SHA_A,
        visibility="link",
        published_to_web=spelling,
    )

    assert response.status_code == 200, response.text
    assert service.upload_kwargs is not None
    assert service.upload_kwargs["published_to_web"] is expected
    assert service.share_link_creations == 0


def test_upload_openapi_keeps_published_to_web_nullable_boolean(
    table: _FakeIdempotencyTable,
) -> None:
    schema = _client(_StubService(_row())).get("/openapi.json").json()
    body = schema["paths"]["/files/upload"]["post"]["requestBody"]["content"]["multipart/form-data"]["schema"]
    component = schema["components"]["schemas"][body["$ref"].rsplit("/", 1)[-1]]
    assert {"type": "boolean"} in component["properties"]["published_to_web"]["anyOf"]


def test_a_fresh_key_is_a_fresh_request(table: _FakeIdempotencyTable) -> None:
    service = _StubService(_row())
    client = _client(service)
    assert _upload(client, expected=SHA_A, key="k1").status_code == 200
    assert _upload(client, expected=SHA_A, key="k2").status_code == 200
    assert service.uploads == 2


def test_legacy_link_upload_returns_and_replays_the_created_share_token(
    table: _FakeIdempotencyTable,
) -> None:
    service = _StubService(_row())
    client = _client(service)

    first = _upload(client, expected=SHA_A, visibility="link")
    assert first.status_code == 200, first.text
    assert first.json()["share_token"] == "anyone-token"
    assert first.json()["share_url"] == "/share/anyone-token"
    assert service.share_link_creations == 1

    replay = _upload(client, expected=SHA_A, visibility="link")
    assert replay.status_code == 200
    assert replay.json() == first.json()
    assert service.share_link_creations == 1, "a replay must not create another Anyone link"
