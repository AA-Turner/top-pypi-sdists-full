"""TUS 1.0.0 wire contract — the real router over the real state machine.

SUT: ``matrx_files.api.router_tus.build_tus_router`` mounted on FastAPI, over
the real ``TUSSessionManager``. Only S3, the matrx-orm model layer, and host
RPCs are doubled (``tests/_tus_harness.py``). Expected statuses and headers come
from the TUS 1.0.0 spec (https://tus.io/protocols/resumable-upload); expected
stored bytes / checksums come from the bytes each test sent, via ``hashlib``.

The host suite (aidream ``tests/test_files_tus_wire.py``) mirrors this against
the aidream mount.
"""

from __future__ import annotations

import base64
import hashlib
import json
from types import SimpleNamespace

import pytest
from _tus_harness import TusWorld, build_world
from fastapi import FastAPI, Request
from fastapi.testclient import TestClient

from matrx_files.api.router_tus import (
    MAX_METADATA_JSON_BYTES,
    build_tus_router,
    merge_metadata_json,
)

BASE = "/files/upload/tus"
OCTET = "application/offset+octet-stream"
# 10 bytes, uploaded as 4 + 4 + 2 (harness min part = 4): every chunk is
# distinguishable, so a dropped, reordered or corrupted chunk changes the object.
CONTENT = b"AAAABBBBCC"


def _meta(**kv: str) -> str:
    return ",".join(f"{k} {base64.b64encode(v.encode()).decode()}" for k, v in kv.items())


@pytest.fixture
def world(monkeypatch: pytest.MonkeyPatch) -> TusWorld:
    return build_world(monkeypatch)


def _client(world: TusWorld, **factory_kwargs: object) -> TestClient:
    def user_id_dep(request: Request) -> str:
        return request.headers.get("x-test-user", "user-a")

    app = FastAPI()
    app.include_router(
        build_tus_router(
            file_manager_dep=lambda: world.file_manager,
            user_id_dep=user_id_dep,
            request_id_provider=lambda: "req-wire-1",
            **factory_kwargs,
        )
    )
    return TestClient(app)


@pytest.fixture
def client(world: TusWorld) -> TestClient:
    return _client(world)


def _create(
    client: TestClient,
    *,
    length: int = len(CONTENT),
    metadata: str | None = None,
    body: bytes | None = None,
    user: str = "user-a",
    headers: dict[str, str] | None = None,
):
    h = {
        "Tus-Resumable": "1.0.0",
        "Upload-Length": str(length),
        "Upload-Metadata": metadata or _meta(filename="rec.webm"),
        "x-test-user": user,
    }
    if body is not None:
        h["Content-Type"] = OCTET
    h.update(headers or {})
    return client.post(BASE, headers=h, content=body)


def _patch(client: TestClient, location: str, offset: int, body: bytes, *, user: str = "user-a"):
    return client.patch(
        location,
        headers={
            "Tus-Resumable": "1.0.0",
            "Content-Type": OCTET,
            "Upload-Offset": str(offset),
            "x-test-user": user,
        },
        content=body,
    )


def _head(client: TestClient, location: str, *, user: str = "user-a"):
    return client.head(location, headers={"Tus-Resumable": "1.0.0", "x-test-user": user})


def _stored(world: TusWorld, row: dict) -> bytes | None:
    bucket, _, key = row["storage_uri"].partition("://")[2].partition("/")
    return world.s3.objects.get((bucket, key))


# ---------------------------------------------------------------------------
# OPTIONS / version negotiation
# ---------------------------------------------------------------------------


def test_options_advertises_tus_1_0_0_capabilities(client: TestClient) -> None:
    resp = client.options(BASE)
    assert resp.status_code == 204
    assert resp.headers["Tus-Resumable"] == "1.0.0"
    assert resp.headers["Tus-Version"] == "1.0.0"
    assert set(resp.headers["Tus-Extension"].split(",")) == {
        "creation",
        "termination",
        "creation-with-upload",
    }
    assert int(resp.headers["Tus-Max-Size"]) > 0


def test_unsupported_client_version_is_412_with_tus_version_and_allocates_nothing(
    client: TestClient, world: TusWorld
) -> None:
    resp = client.post(
        BASE,
        headers={"Tus-Resumable": "0.2.2", "Upload-Length": "10", "Upload-Metadata": _meta(filename="a")},
    )
    assert resp.status_code == 412
    assert resp.headers["Tus-Version"] == "1.0.0"
    assert resp.headers["Tus-Resumable"] == "1.0.0"
    assert world.s3.create_calls == []
    assert world.inflight.rows == {}


# ---------------------------------------------------------------------------
# Creation + PATCH — the stored object is exactly the uploaded bytes
# ---------------------------------------------------------------------------


def test_chunked_upload_stores_exact_bytes_in_order_and_reports_completion(
    client: TestClient, world: TusWorld
) -> None:
    created = _create(client)
    assert created.status_code == 201
    assert created.headers["Tus-Resumable"] == "1.0.0"
    assert created.headers["Upload-Offset"] == "0"
    location = created.headers["Location"]
    assert location.startswith(f"{BASE}/")

    first = _patch(client, location, 0, b"AAAA")
    assert (first.status_code, first.headers["Upload-Offset"]) == (204, "4")
    assert "Upload-Complete" not in first.headers
    second = _patch(client, location, 4, b"BBBB")
    assert (second.status_code, second.headers["Upload-Offset"]) == (204, "8")
    final = _patch(client, location, 8, b"CC")
    assert final.status_code == 204
    assert final.headers["Upload-Offset"] == "10"
    assert final.headers["Upload-Complete"] == "true"

    [row] = world.live_files()
    assert final.headers["X-Cld-File-Id"] == row["id"]
    assert _stored(world, row) == CONTENT
    assert row["checksum"] == hashlib.sha256(CONTENT).hexdigest()
    assert row["size_bytes"] == 10
    assert row["created_by"] == "user-a"
    assert row["metadata"]["request_id"] == "req-wire-1"


def test_patch_at_a_stale_or_future_offset_is_409_and_appends_nothing(
    client: TestClient, world: TusWorld
) -> None:
    location = _create(client).headers["Location"]
    assert _patch(client, location, 0, b"AAAA").status_code == 204

    replayed = _patch(client, location, 0, b"XXXX")
    assert replayed.status_code == 409
    assert replayed.json()["detail"]["error"] == "offset_mismatch"
    assert replayed.headers["Tus-Resumable"] == "1.0.0"
    assert _patch(client, location, 8, b"XXXX").status_code == 409
    assert _head(client, location).headers["Upload-Offset"] == "4"

    assert _patch(client, location, 4, b"BBBB").status_code == 204
    assert _patch(client, location, 8, b"CC").headers["Upload-Complete"] == "true"
    [row] = world.live_files()
    assert _stored(world, row) == CONTENT


def test_head_reports_the_committed_offset_and_resuming_there_completes(
    client: TestClient, world: TusWorld
) -> None:
    location = _create(client).headers["Location"]
    _patch(client, location, 0, b"AAAA")
    _patch(client, location, 4, b"BBBB")

    head = _head(client, location)
    assert head.status_code == 200
    assert head.headers["Upload-Offset"] == "8"
    assert head.headers["Upload-Length"] == "10"
    assert head.headers["Cache-Control"] == "no-store"
    assert "Upload-Complete" not in head.headers
    # Nothing is stored before the last byte arrives.
    assert world.live_files() == []
    assert world.s3.objects == {}

    resumed = _patch(client, location, int(head.headers["Upload-Offset"]), CONTENT[8:])
    assert resumed.headers["Upload-Complete"] == "true"
    [row] = world.live_files()
    assert _stored(world, row) == CONTENT


def test_patch_past_upload_length_is_413_and_the_upload_stays_resumable(
    client: TestClient, world: TusWorld
) -> None:
    location = _create(client).headers["Location"]
    _patch(client, location, 0, b"AAAA")

    over = _patch(client, location, 4, b"BBBBCCC")  # 4 + 7 = 11 > 10
    assert over.status_code == 413
    assert over.json()["detail"]["error"] == "exceeds_upload_length"
    assert _head(client, location).headers["Upload-Offset"] == "4"

    _patch(client, location, 4, b"BBBB")
    _patch(client, location, 8, b"CC")
    [row] = world.live_files()
    assert _stored(world, row) == CONTENT


def test_non_final_patch_below_the_minimum_part_is_400_and_appends_nothing(
    client: TestClient,
) -> None:
    location = _create(client).headers["Location"]
    resp = _patch(client, location, 0, b"AA")
    assert resp.status_code == 400
    assert resp.json()["detail"]["error"] == "patch_too_small"
    assert _head(client, location).headers["Upload-Offset"] == "0"


@pytest.mark.parametrize("active_status", ["uploading", "ready", "finalizing"])
def test_head_during_a_leased_operation_stays_visible_with_retry_after(
    client: TestClient, world: TusWorld, active_status: str
) -> None:
    location = _create(client).headers["Location"]
    _patch(client, location, 0, b"AAAA")
    world.session_row(location.rsplit("/", 1)[-1])["status"] = active_status  # a concurrent op holds the lease

    head = _head(client, location)
    assert head.status_code == 200
    assert head.headers["Upload-Offset"] == "4"
    assert head.headers["Retry-After"] == "1"


# ---------------------------------------------------------------------------
# creation-with-upload + idempotent create
# ---------------------------------------------------------------------------


def test_creation_with_upload_body_completes_in_one_request(
    client: TestClient, world: TusWorld
) -> None:
    resp = _create(client, body=CONTENT)
    assert resp.status_code == 201
    assert resp.headers["Upload-Offset"] == "10"
    assert resp.headers["Upload-Complete"] == "true"
    [row] = world.live_files()
    assert resp.headers["X-Cld-File-Id"] == row["id"]
    assert _stored(world, row) == CONTENT


def test_creation_with_a_partial_body_advances_the_offset_for_resume(
    client: TestClient, world: TusWorld
) -> None:
    resp = _create(client, body=b"AAAA")
    assert resp.status_code == 201
    assert resp.headers["Upload-Offset"] == "4"
    assert "Upload-Complete" not in resp.headers
    location = resp.headers["Location"]
    assert _head(client, location).headers["Upload-Offset"] == "4"

    assert _patch(client, location, 4, b"BBBBCC").headers["Upload-Complete"] == "true"
    [row] = world.live_files()
    assert _stored(world, row) == CONTENT


def test_idempotent_create_replay_resumes_the_session_without_reappending_its_body(
    client: TestClient, world: TusWorld
) -> None:
    first = _create(client, body=b"AAAA", headers={"X-Idempotency-Key": "rec-1"})
    replay = _create(client, body=b"AAAA", headers={"X-Idempotency-Key": "rec-1"})

    assert replay.status_code == 201
    assert replay.headers["Location"] == first.headers["Location"]
    assert replay.headers["Upload-Offset"] == "4"
    assert len(world.inflight.rows) == 1
    assert len(world.s3.create_calls) == 1

    done = _patch(client, first.headers["Location"], 4, b"BBBBCC")
    assert done.headers["Upload-Complete"] == "true"
    [row] = world.live_files()
    assert _stored(world, row) == CONTENT


# ---------------------------------------------------------------------------
# HEAD after completion (lost final response) + dedup winner
# ---------------------------------------------------------------------------


def test_head_after_completion_returns_final_state_for_lost_response_recovery(
    client: TestClient, world: TusWorld
) -> None:
    location = _create(client, body=CONTENT).headers["Location"]
    head = _head(client, location)
    assert head.status_code == 200
    assert head.headers["Upload-Offset"] == "10"
    assert head.headers["Upload-Length"] == "10"
    assert head.headers["Upload-Complete"] == "true"
    [row] = world.live_files()
    assert head.headers["X-Cld-File-Id"] == row["id"]


def test_reupload_of_identical_bytes_at_another_path_gets_its_own_row(
    client: TestClient, world: TusWorld
) -> None:
    # Same bytes, another path: a placement of its own (its own id), linked to
    # the first by duplicate_of_file_id -- never the first file's id
    # (test_tus_same_bytes_every_path_its_own_row.py).
    first_id = _create(client, body=CONTENT, metadata=_meta(filename="first.webm")).headers[
        "X-Cld-File-Id"
    ]
    second = _create(client, metadata=_meta(filename="second.webm")).headers["Location"]
    _patch(client, second, 0, b"AAAA")
    _patch(client, second, 4, b"BBBB")
    final = _patch(client, second, 8, b"CC")

    assert final.headers["Upload-Complete"] == "true"
    second_id = final.headers["X-Cld-File-Id"]
    assert second_id != first_id
    assert _head(client, second).headers["X-Cld-File-Id"] == second_id
    rows = {str(r["id"]): r for r in world.live_files()}
    assert set(rows) == {first_id, second_id}
    assert str(rows[second_id]["duplicate_of_file_id"]) == first_id


# ---------------------------------------------------------------------------
# Owner isolation + termination
# ---------------------------------------------------------------------------


def test_another_user_can_neither_resume_nor_append_to_nor_terminate_the_upload(
    client: TestClient, world: TusWorld
) -> None:
    location = _create(client).headers["Location"]
    _patch(client, location, 0, b"AAAA")

    assert _head(client, location, user="user-b").status_code == 404
    stolen = _patch(client, location, 4, b"XXXX", user="user-b")
    assert stolen.status_code == 404
    assert stolen.json()["detail"]["error"] == "not_found"
    terminate = client.delete(location, headers={"Tus-Resumable": "1.0.0", "x-test-user": "user-b"})
    assert terminate.status_code == 404

    assert _head(client, location).headers["Upload-Offset"] == "4"
    _patch(client, location, 4, b"BBBB")
    _patch(client, location, 8, b"CC")
    [row] = world.live_files()
    assert _stored(world, row) == CONTENT


def test_delete_terminates_the_upload_and_releases_its_multipart(
    client: TestClient, world: TusWorld
) -> None:
    location = _create(client, body=b"AAAA").headers["Location"]
    assert len(world.s3.uploads) == 1

    resp = client.delete(location, headers={"Tus-Resumable": "1.0.0", "x-test-user": "user-a"})
    assert resp.status_code == 204
    assert resp.headers["Tus-Resumable"] == "1.0.0"
    assert world.s3.uploads == {}
    assert world.s3.objects == {}
    assert _head(client, location).status_code == 404


@pytest.mark.parametrize("gone_status", ["aborting", "aborted"])
def test_head_of_a_terminated_session_is_404(
    client: TestClient, world: TusWorld, gone_status: str
) -> None:
    location = _create(client).headers["Location"]
    world.session_row(location.rsplit("/", 1)[-1])["status"] = gone_status
    assert _head(client, location).status_code == 404


def test_error_responses_carry_tus_resumable(client: TestClient) -> None:
    """Spec: Tus-Resumable MUST be on every response except OPTIONS — errors too."""
    location = _create(client).headers["Location"]
    unsupported = client.patch(
        location,
        headers={"Tus-Resumable": "1.0.0", "Content-Type": "text/plain", "Upload-Offset": "0"},
        content=b"AAAA",
    )
    assert unsupported.status_code == 415
    assert unsupported.headers["Tus-Resumable"] == "1.0.0"
    missing = _head(client, f"{BASE}/no-such-upload")
    assert missing.status_code == 404
    assert missing.headers["Tus-Resumable"] == "1.0.0"


# ---------------------------------------------------------------------------
# Request validation — refusals allocate nothing
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    ("headers", "status", "error"),
    [
        ({"Content-Type": "text/plain", "Upload-Offset": "0"}, 415, "unsupported_media_type"),
        ({"Content-Type": OCTET}, 400, "missing_upload_offset"),
        ({"Content-Type": OCTET, "Upload-Offset": "zero"}, 400, "invalid_upload_offset"),
    ],
)
def test_patch_header_violations_are_refused_without_appending(
    client: TestClient, headers: dict[str, str], status: int, error: str
) -> None:
    location = _create(client).headers["Location"]
    resp = client.patch(location, headers={"Tus-Resumable": "1.0.0", **headers}, content=b"AAAA")
    assert resp.status_code == status
    assert resp.json()["detail"]["error"] == error
    assert _head(client, location).headers["Upload-Offset"] == "0"


_B64_NAME = base64.b64encode(b"a.webm").decode()


@pytest.mark.parametrize(
    ("headers", "error"),
    [
        ({"Upload-Metadata": _meta(filename="a.webm")}, "missing_upload_length"),
        ({"Upload-Length": "ten", "Upload-Metadata": _meta(filename="a.webm")}, "invalid_upload_length"),
        ({"Upload-Length": "10", "Upload-Metadata": _meta(visibility="personal")}, "missing_filepath"),
        ({"Upload-Length": "10", "Upload-Metadata": _meta(filepath="../../etc/passwd")}, "invalid_path"),
        ({"Upload-Length": "10", "Upload-Metadata": _meta(filename="a.webm", metadata_json="not json")}, "invalid_metadata"),
        ({"Upload-Length": "10", "Upload-Metadata": _meta(filename="a.webm", metadata_json="[1, 2]")}, "invalid_metadata"),
        ({"Upload-Length": "10", "Upload-Metadata": _meta(filename="a.webm", metadata_json='"scalar"')}, "invalid_metadata"),
        (
            {
                "Upload-Length": "10",
                "Upload-Metadata": _meta(
                    filename="a.webm",
                    metadata_json=json.dumps({"blob": "x" * (MAX_METADATA_JSON_BYTES + 1)}),
                ),
            },
            "invalid_metadata",
        ),
        (
            {"Upload-Length": "10", "Upload-Metadata": _meta(filename="a.webm", metadata_json=json.dumps({"_idempotency_key": "sneak"}))},
            "invalid_metadata",
        ),
        ({"Upload-Length": "10", "Upload-Metadata": f"filename {_B64_NAME},metadata_json !!!not-base64!!!"}, "invalid_metadata"),
    ],
)
def test_invalid_creation_is_400_and_allocates_nothing(
    client: TestClient, world: TusWorld, headers: dict[str, str], error: str
) -> None:
    resp = client.post(BASE, headers={"Tus-Resumable": "1.0.0", **headers})
    assert resp.status_code == 400
    assert resp.json()["detail"]["error"] == error
    assert world.s3.create_calls == []
    assert world.inflight.rows == {}


def test_client_supplied_policy_metadata_is_403_and_allocates_nothing(
    client: TestClient, world: TusWorld
) -> None:
    resp = _create(
        client,
        metadata=_meta(filename="a.webm", metadata_json=json.dumps({"system_artifact": True})),
    )
    assert resp.status_code == 403
    assert resp.json()["detail"]["error"] == "reserved_metadata_key"
    assert world.s3.create_calls == []
    assert world.inflight.rows == {}


def test_quota_refusal_is_413_with_reason_and_allocates_nothing(world: TusWorld) -> None:
    seen: list[tuple[str, int]] = []
    decision = SimpleNamespace(allowed=False, reason="storage_quota_exceeded", raw={"limit_bytes": 5})

    def quota_dep():
        async def check(user_id: str, upload_length: int):
            seen.append((user_id, upload_length))
            return decision

        return check

    resp = _create(_client(world, quota_checker_dep=quota_dep))
    assert resp.status_code == 413
    detail = resp.json()["detail"]
    assert detail["error"] == "storage_quota_exceeded"
    assert detail["details"] == {"limit_bytes": 5}
    assert seen == [("user-a", 10)]
    assert world.s3.create_calls == []
    assert world.inflight.rows == {}


# ---------------------------------------------------------------------------
# Placement + metadata reach the finished file row
# ---------------------------------------------------------------------------


def test_transcript_origin_upload_is_filed_under_the_system_folder(
    client: TestClient, world: TusWorld
) -> None:
    resp = _create(
        client,
        body=CONTENT,
        metadata=_meta(
            filepath="Transcripts/Recordings/rec.webm",
            metadata_json=json.dumps({"origin": "transcripts"}),
        ),
    )
    assert resp.headers["Upload-Complete"] == "true"
    [row] = world.live_files()
    assert row["file_path"] == "system-files/transcripts/Recordings/rec.webm"
    assert row["metadata"]["origin"] == "transcripts"


def test_host_relocation_callable_decides_the_stored_path(world: TusWorld) -> None:
    def relocate(clean_path: str, origin: str | None) -> str:
        return f"hosted/{origin}/{clean_path}" if origin else clean_path

    client = _client(world, relocate_path=relocate)
    _create(
        client,
        body=CONTENT,
        metadata=_meta(filename="rec.webm", metadata_json=json.dumps({"origin": "transcripts"})),
    )
    [row] = world.live_files()
    assert row["file_path"] == "hosted/transcripts/rec.webm"


def test_nested_metadata_json_lands_on_the_file_row(client: TestClient, world: TusWorld) -> None:
    capture = {"capture": {"kind": "screen", "duration_ms": 1234}}
    _create(client, body=CONTENT, metadata=_meta(filename="a.webm", metadata_json=json.dumps(capture)))
    [row] = world.live_files()
    assert row["metadata"]["capture"] == {"kind": "screen", "duration_ms": 1234}
    assert "metadata_json" not in row["metadata"]


def test_nested_metadata_json_wins_over_a_flat_key_on_collision() -> None:
    merged = merge_metadata_json(
        {"origin": "flat", "custom": "v", "metadata_json": json.dumps({"origin": "nested"})}
    )
    assert merged == {"origin": "nested", "custom": "v"}


# ---------------------------------------------------------------------------
# Factory contract + standalone auth coverage (TUS routes never fail open)
# ---------------------------------------------------------------------------


def test_factory_requires_exactly_one_manager_source() -> None:
    placeholder_service = SimpleNamespace(file_manager=None)
    with pytest.raises(ValueError, match="exactly one of file_service / file_manager_dep"):
        build_tus_router()
    with pytest.raises(ValueError, match="exactly one of file_service / file_manager_dep"):
        build_tus_router(placeholder_service, file_manager_dep=lambda: None)


def test_standalone_auth_coverage_accepts_tus_router() -> None:
    from matrx_files.standalone.security import assert_route_auth_coverage

    def auth_dep() -> str:
        return "user-a"

    app = FastAPI()
    app.include_router(build_tus_router(SimpleNamespace(file_manager=None), user_id_dep=auth_dep))
    # OPTIONS shares the create path but is legitimately anonymous.
    assert_route_auth_coverage(
        app,
        auth_dependency=auth_dep,
        public_paths=frozenset(),
        public_prefixes=(),
        public_operations=frozenset({"OPTIONS /files/upload/tus"}),
    )


def test_standalone_auth_coverage_rejects_unauthenticated_tus_router() -> None:
    from matrx_files._config import IndependenceConfigError
    from matrx_files.standalone.security import assert_route_auth_coverage

    def auth_dep() -> str:
        return "user-a"

    app = FastAPI()
    app.include_router(build_tus_router(SimpleNamespace(file_manager=None)))  # anonymous default dep
    with pytest.raises(IndependenceConfigError):
        assert_route_auth_coverage(
            app,
            auth_dependency=auth_dep,
            public_paths=frozenset(),
            public_prefixes=(),
            public_operations=frozenset({"OPTIONS /files/upload/tus"}),
        )
