"""TUSSessionManager finalize — assembly integrity, dedup gate, lineage, compensation.

SUT: ``matrx_files.cloud_sync.transports.tus.TUSSessionManager`` together with
what it relies on inside this package and does not stub: the dedup scope query
(``DatabaseClient.get_file_by_checksum_async``), organization resolution and
duplicate-target validation on ``SyncEngine``, ``PermissionsManager``, and
``tus_cleanup.sweep_once``.

Doubles (``tests/_tus_harness.py``): S3 client with real multipart assembly and
FULL_OBJECT SHA-256, the matrx-orm model layer, iam RPCs, host access checker,
folder RPC. Expected checksums are ``hashlib`` over the uploaded bytes; expected
identities are ids the test itself observed.
"""

from __future__ import annotations

import asyncio
import hashlib
import threading
from datetime import UTC, datetime, timedelta

import pytest
from _tus_harness import (
    BUCKET,
    FakeS3Client,
    S3ClientError,
    TusWorld,
    build_world,
    chunks_of,
    CARRIED_ORG,
    upload_file,
    upload_to_ready,
)
from matrx_orm import UUIDField

from matrx_files.cloud_sync.transports.tus import (
    S3Failure,
    UploadCompleted,
    UploadIncomplete,
)
from matrx_files.cloud_sync.transports.tus_cleanup import sweep_once
from matrx_files.db.models_files import UploadsInflight

CONTENT = b"AAAABBBBCC"  # 4 + 4 + 2: every chunk distinguishable
SHA256_HEX = hashlib.sha256(CONTENT).hexdigest()


@pytest.fixture
def world(monkeypatch: pytest.MonkeyPatch) -> TusWorld:
    return build_world(monkeypatch)


def _stored(world: TusWorld, row: dict) -> bytes | None:
    bucket, _, key = row["storage_uri"].partition("://")[2].partition("/")
    return world.s3.objects.get((bucket, key))


def _session_key(world: TusWorld, upload_id: str) -> str:
    return world.session_row(upload_id)["key"]


def test_inflight_file_id_is_an_eventual_id_not_a_foreign_key():
    """TUS reserves the files.files id before that row exists at finalize."""
    assert type(UploadsInflight._fields["file_id"]) is UUIDField


# ---------------------------------------------------------------------------
# Assembly integrity + full-object checksum
# ---------------------------------------------------------------------------


async def test_finalized_row_records_the_sha256_hex_of_the_assembled_bytes(world: TusWorld):
    upload_id, result = await upload_file(world, owner="user-a", path="docs/q1.pdf", content=CONTENT)

    [row] = world.live_files()
    assert _stored(world, row) == CONTENT
    assert row["checksum"] == SHA256_HEX
    assert result.checksum == SHA256_HEX
    assert row["size_bytes"] == len(CONTENT)
    assert row["organization_id"] == CARRIED_ORG
    assert result.is_new is True
    assert result.file_id == row["id"]
    assert world.session_row(upload_id)["status"] == "completed"


async def test_finalize_before_every_byte_is_committed_is_refused_and_stays_resumable(
    world: TusWorld,
):
    created = await world.manager.create_async(
        owner_id="user-a", file_path="docs/partial.pdf", upload_length=len(CONTENT)
    )
    await world.manager.append_async(
        upload_id=created.upload_id, owner_id="user-a", body=b"AAAA", client_offset=0
    )

    with pytest.raises(UploadIncomplete, match="has 4 of 10 bytes"):
        await world.manager.finalize_async(upload_id=created.upload_id, owner_id="user-a")

    assert world.s3.complete_calls == 0
    assert world.s3.objects == {}
    assert world.live_files() == []
    assert world.session_row(created.upload_id)["status"] == "in_progress"

    await world.manager.append_async(
        upload_id=created.upload_id, owner_id="user-a", body=b"BBBB", client_offset=4
    )
    await world.manager.append_async(
        upload_id=created.upload_id, owner_id="user-a", body=b"CC", client_offset=8
    )
    result = await world.manager.finalize_async(upload_id=created.upload_id, owner_id="user-a")
    assert _stored(world, world.files.rows[result.file_id]) == CONTENT


async def test_parts_record_missing_a_chunk_is_refused_instead_of_stored_short(world: TusWorld):
    upload_id = await upload_to_ready(world, owner="user-a", path="docs/q1.pdf", content=CONTENT)
    # A lost part record: the offset says 10 bytes, the parts list covers 8.
    world.session_row(upload_id)["parts"] = world.session_row(upload_id)["parts"][:2]

    with pytest.raises(S3Failure, match="completed_size_mismatch"):
        await world.manager.finalize_async(upload_id=upload_id, owner_id="user-a")

    assert world.live_files() == []
    assert world.s3.objects == {}
    assert world.session_row(upload_id)["status"] == "aborted"


# ---------------------------------------------------------------------------
# Dedup gate — scope
# ---------------------------------------------------------------------------


async def test_identical_bytes_from_the_same_owner_at_another_path_alias_the_canonical_file(
    world: TusWorld,
):
    # Every declared path keeps a row of its own; the content link is
    # duplicate_of_file_id (test_tus_same_bytes_every_path_its_own_row.py).
    _, first = await upload_file(world, owner="user-a", path="docs/first.pdf", content=CONTENT)
    second_upload, second = await upload_file(
        world, owner="user-a", path="docs/second.pdf", content=CONTENT
    )

    assert second.file_id != first.file_id
    assert second.checksum == SHA256_HEX
    rows = {str(r["id"]): r for r in world.live_files()}
    assert set(rows) == {first.file_id, second.file_id}
    assert rows[second.file_id]["file_path"] == "docs/second.pdf"
    assert str(rows[second.file_id]["duplicate_of_file_id"]) == first.file_id
    assert world.session_row(second_upload)["status"] == "completed"


async def test_identical_bytes_from_another_member_of_the_same_org_are_never_aliased(
    world: TusWorld,
):
    world.org_members["org-shared"] = {"user-a", "user-b"}
    shared = {"organization_id": "org-shared"}
    _, a = await upload_file(world, owner="user-a", path="docs/a.pdf", content=CONTENT, metadata=shared)
    _, b = await upload_file(world, owner="user-b", path="docs/b.pdf", content=CONTENT, metadata=shared)

    assert b.is_new is True
    assert b.file_id != a.file_id
    rows = {r["created_by"]: r for r in world.live_files()}
    assert set(rows) == {"user-a", "user-b"}
    assert rows["user-b"]["organization_id"] == "org-shared"
    assert _stored(world, rows["user-a"]) == CONTENT
    assert _stored(world, rows["user-b"]) == CONTENT


async def test_derivative_with_identical_bytes_is_stored_as_its_own_row(world: TusWorld):
    _, root = await upload_file(world, owner="user-a", path="docs/root.png", content=CONTENT)
    world.grants.add(("user-a", "file", root.file_id, "read"))

    _, page = await upload_file(
        world,
        owner="user-a",
        path="docs/page-1.png",
        content=CONTENT,
        metadata={
            "parent_file_id": root.file_id,
            "derivation_kind": "rendered_page_image",
            "page_number": 1,
        },
    )

    assert page.is_new is True
    assert page.file_id != root.file_id
    derived = world.files.rows[page.file_id]
    assert derived["parent_file_id"] == root.file_id
    assert derived["derivation_kind"] == "rendered_page_image"
    assert derived["checksum"] == SHA256_HEX
    assert _stored(world, derived) == CONTENT


async def test_derivation_kind_without_a_parent_still_dedups_against_the_root(world: TusWorld):
    _, root = await upload_file(world, owner="user-a", path="docs/root.pdf", content=CONTENT)
    _, again = await upload_file(
        world,
        owner="user-a",
        path="docs/again.pdf",
        content=CONTENT,
        metadata={"derivation_kind": "manual_upload"},
    )
    # Still matched against the root (not treated as a derivative): the new
    # placement is linked to it as a dedup alias.
    assert again.file_id != root.file_id
    assert str(world.files.rows[again.file_id]["duplicate_of_file_id"]) == root.file_id


async def test_duplicate_of_an_identical_canonical_file_is_persisted_as_an_alias(world: TusWorld):
    _, canonical = await upload_file(world, owner="user-a", path="docs/root.pdf", content=CONTENT)
    world.grants.add(("user-a", "file", canonical.file_id, "read"))

    _, alias = await upload_file(
        world,
        owner="user-a",
        path="docs/copy.pdf",
        content=CONTENT,
        metadata={"duplicate_of_file_id": canonical.file_id},
    )

    assert alias.is_new is True
    assert alias.file_id != canonical.file_id
    row = world.files.rows[alias.file_id]
    assert row["duplicate_of_file_id"] == canonical.file_id
    assert row["checksum"] == SHA256_HEX


async def test_duplicate_of_a_file_with_different_bytes_is_refused_and_cleaned(world: TusWorld):
    _, other = await upload_file(world, owner="user-a", path="docs/other.pdf", content=b"ZZZZYYYYXX")
    world.grants.add(("user-a", "file", other.file_id, "read"))
    upload_id = await upload_to_ready(
        world,
        owner="user-a",
        path="docs/copy.pdf",
        content=CONTENT,
        metadata={"duplicate_of_file_id": other.file_id},
    )

    with pytest.raises(ValueError, match="identical content"):
        await world.manager.finalize_async(upload_id=upload_id, owner_id="user-a")

    assert world.object_at(_session_key(world, upload_id)) is None
    assert [r["id"] for r in world.live_files()] == [other.file_id]
    assert world.session_row(upload_id)["status"] == "aborted"


# ---------------------------------------------------------------------------
# Checksum unavailable
# ---------------------------------------------------------------------------


async def test_bucket_rejecting_full_object_sha256_uploads_with_null_checksum_and_no_dedup(
    monkeypatch: pytest.MonkeyPatch,
):
    world = build_world(monkeypatch, s3=FakeS3Client(reject_full_object_sha256=True))
    _, first = await upload_file(world, owner="user-a", path="docs/a.pdf", content=CONTENT)
    _, second = await upload_file(world, owner="user-a", path="docs/b.pdf", content=CONTENT)

    assert first.checksum is None
    assert second.is_new is True
    assert second.file_id != first.file_id
    rows = world.live_files()
    assert len(rows) == 2
    assert all(r["checksum"] is None for r in rows)
    assert all(_stored(world, r) == CONTENT for r in rows)


async def test_unrelated_invalid_request_fails_create_without_retry_or_state(world: TusWorld):
    world.s3.fail["create_multipart_upload"] = S3ClientError(
        "InvalidRequest", "The bucket policy rejected this operation."
    )
    with pytest.raises(S3Failure, match="create_multipart_upload"):
        await world.manager.create_async(owner_id="user-a", file_path="docs/new.pdf", upload_length=10)
    assert len(world.s3.create_calls) == 1
    assert world.inflight.rows == {}


async def test_garbled_s3_checksum_lands_null_and_never_dedups(monkeypatch: pytest.MonkeyPatch):
    world = build_world(monkeypatch, s3=FakeS3Client(checksum_override="not-valid-base64!!!"))
    _, first = await upload_file(world, owner="user-a", path="docs/a.pdf", content=CONTENT)
    _, second = await upload_file(world, owner="user-a", path="docs/b.pdf", content=CONTENT)

    assert first.checksum is None
    assert second.is_new is True
    assert len(world.live_files()) == 2


# ---------------------------------------------------------------------------
# Placement authorization — refused before the multipart is assembled
# ---------------------------------------------------------------------------


async def test_member_organization_places_the_row_and_its_folder(world: TusWorld):
    world.org_members["org-shared"] = {"user-a"}
    _, result = await upload_file(
        world,
        owner="user-a",
        path="docs/q1.pdf",
        content=CONTENT,
        metadata={"organization_id": "org-shared"},
    )
    assert world.files.rows[result.file_id]["organization_id"] == "org-shared"
    assert world.folder_calls == [("docs/q1.pdf", "user-a", "org-shared")]


async def test_non_member_organization_refuses_before_assembly_and_releases_the_multipart(
    world: TusWorld,
):
    upload_id = await upload_to_ready(
        world,
        owner="user-a",
        path="docs/q1.pdf",
        content=CONTENT,
        metadata={"organization_id": "org-not-mine"},
    )
    with pytest.raises(PermissionError, match="not a member of organization org-not-mine"):
        await world.manager.finalize_async(upload_id=upload_id, owner_id="user-a")

    assert world.s3.complete_calls == 0
    assert world.s3.uploads == {}
    assert world.s3.objects == {}
    assert world.live_files() == []
    assert world.session_row(upload_id)["status"] == "aborted"


async def test_unreadable_parent_refuses_before_assembly_and_releases_the_multipart(
    world: TusWorld,
):
    upload_id = await upload_to_ready(
        world,
        owner="user-a",
        path="docs/variant.png",
        content=CONTENT,
        metadata={"parent_file_id": "hidden-parent", "derivation_kind": "variant"},
    )
    with pytest.raises(PermissionError, match="'read' access on file 'hidden-parent'"):
        await world.manager.finalize_async(upload_id=upload_id, owner_id="user-a")

    assert world.s3.complete_calls == 0
    assert world.s3.uploads == {}
    assert world.s3.objects == {}
    assert world.live_files() == []
    assert world.session_row(upload_id)["status"] == "aborted"


# ---------------------------------------------------------------------------
# Compensation — no orphan object, no half-committed session
# ---------------------------------------------------------------------------


async def test_folder_failure_deletes_the_assembled_object_and_aborts(world: TusWorld):
    world.folder_failure = RuntimeError("folder failure")
    upload_id = await upload_to_ready(world, owner="user-a", path="docs/q1.pdf", content=CONTENT)

    with pytest.raises(RuntimeError, match="folder failure"):
        await world.manager.finalize_async(upload_id=upload_id, owner_id="user-a")

    assert world.s3.complete_calls == 1
    assert world.object_at(_session_key(world, upload_id)) is None
    assert world.live_files() == []
    assert world.session_row(upload_id)["status"] == "aborted"


async def test_failed_object_cleanup_leaves_the_session_retryable(world: TusWorld):
    world.folder_failure = RuntimeError("folder failure")
    world.s3.fail["delete_object"] = S3ClientError("ServiceUnavailable")
    upload_id = await upload_to_ready(world, owner="user-a", path="docs/q1.pdf", content=CONTENT)

    with pytest.raises(RuntimeError, match="folder failure"):
        await world.manager.finalize_async(upload_id=upload_id, owner_id="user-a")

    assert world.session_row(upload_id)["status"] == "finalizing"
    assert world.object_at(_session_key(world, upload_id)) == CONTENT


async def test_lost_completion_response_deletes_the_completed_object_and_aborts(world: TusWorld):
    world.s3.fail_after["complete_multipart_upload"] = TimeoutError("response lost after completion")
    upload_id = await upload_to_ready(world, owner="user-a", path="docs/q1.pdf", content=CONTENT)

    with pytest.raises(S3Failure, match="complete_multipart_upload"):
        await world.manager.finalize_async(upload_id=upload_id, owner_id="user-a")

    assert world.s3.objects == {}
    assert world.live_files() == []
    assert world.session_row(upload_id)["status"] == "aborted"


async def test_completion_failure_before_assembly_releases_the_multipart(world: TusWorld):
    world.s3.fail["complete_multipart_upload"] = TimeoutError("connect timeout")
    upload_id = await upload_to_ready(world, owner="user-a", path="docs/q1.pdf", content=CONTENT)

    with pytest.raises(S3Failure, match="complete_multipart_upload"):
        await world.manager.finalize_async(upload_id=upload_id, owner_id="user-a")

    assert world.s3.uploads == {}
    assert world.s3.objects == {}
    assert world.session_row(upload_id)["status"] == "aborted"


async def test_cancellation_during_completion_waits_for_it_then_compensates(world: TusWorld):
    started, release = threading.Event(), threading.Event()

    def hold_completion() -> None:
        started.set()
        release.wait(timeout=5)

    world.s3.before["complete_multipart_upload"] = hold_completion
    upload_id = await upload_to_ready(world, owner="user-a", path="docs/q1.pdf", content=CONTENT)

    task = asyncio.create_task(world.manager.finalize_async(upload_id=upload_id, owner_id="user-a"))
    assert await asyncio.to_thread(started.wait, 5), "completion never started"
    task.cancel()
    release.set()
    with pytest.raises(asyncio.CancelledError):
        await task

    assert world.s3.objects == {}
    assert world.live_files() == []
    assert world.session_row(upload_id)["status"] == "aborted"


async def test_path_collision_deletes_the_assembled_object(world: TusWorld):
    # An upload over a file that is ALREADY live is a new version of it
    # (test_tus_overwrite_existing_path.py). The collision left is the race: a
    # row lands at the path after finalize looked and before its INSERT.
    async def concurrent_writer_lands_at_the_path(file_path: str, user_id: str, org_id: str) -> None:
        world.files.seed(
            id="existing-file",
            created_by="user-a",
            file_path="docs/q1.pdf",
            checksum=None,
            organization_id=CARRIED_ORG,
            storage_uri=f"s3://{BUCKET}/user-a/existing-file",
        )

    world.folder_hook = concurrent_writer_lands_at_the_path
    upload_id = await upload_to_ready(world, owner="user-a", path="docs/q1.pdf", content=CONTENT)

    with pytest.raises(S3Failure, match="cld_files_insert"):
        await world.manager.finalize_async(upload_id=upload_id, owner_id="user-a")

    assert world.object_at(_session_key(world, upload_id)) is None
    assert [r["id"] for r in world.live_files()] == ["existing-file"]
    assert world.session_row(upload_id)["status"] == "aborted"


async def test_insert_race_on_the_dedup_index_resolves_to_the_winner(world: TusWorld):
    upload_id = await upload_to_ready(world, owner="user-a", path="docs/raced.pdf", content=CONTENT)

    async def concurrent_writer_wins(file_path: str, user_id: str, org_id: str) -> None:
        # Runs after the dedup lookup missed and before our INSERT.
        world.files.seed(
            id="winner-file",
            created_by=user_id,
            organization_id=org_id,
            file_path="docs/winner.pdf",
            checksum=SHA256_HEX,
            size_bytes=len(CONTENT),
            storage_uri=f"s3://{BUCKET}/{user_id}/winner-file",
        )

    world.folder_hook = concurrent_writer_wins
    result = await world.manager.finalize_async(upload_id=upload_id, owner_id="user-a")

    assert result.file_id == "winner-file"
    assert result.is_new is False
    assert result.storage_uri == f"s3://{BUCKET}/user-a/winner-file"
    assert [r["id"] for r in world.live_files()] == ["winner-file"]
    assert world.object_at(_session_key(world, upload_id)) is None
    assert world.session_row(upload_id)["metadata"]["dedup_winner_file_id"] == "winner-file"


async def test_cancelled_insert_is_observed_before_compensation(world: TusWorld):
    started, release = asyncio.Event(), asyncio.Event()

    async def slow_insert(_values: dict) -> None:
        started.set()
        await release.wait()

    world.files.before_create = slow_insert
    upload_id = await upload_to_ready(world, owner="user-a", path="docs/q1.pdf", content=CONTENT)

    task = asyncio.create_task(world.manager.finalize_async(upload_id=upload_id, owner_id="user-a"))
    await asyncio.wait_for(started.wait(), 5)
    task.cancel()
    release.set()
    with pytest.raises(asyncio.CancelledError):
        await task

    [row] = world.live_files()
    assert _stored(world, row) == CONTENT
    assert world.session_row(upload_id)["status"] == "completed"


async def test_lost_insert_response_reconciles_the_committed_row(world: TusWorld):
    world.files.fail_after_commit = TimeoutError("response lost")
    upload_id = await upload_to_ready(world, owner="user-a", path="docs/q1.pdf", content=CONTENT)

    result = await world.manager.finalize_async(upload_id=upload_id, owner_id="user-a")

    [row] = world.live_files()
    assert result.file_id == row["id"]
    assert _stored(world, row) == CONTENT
    assert world.session_row(upload_id)["status"] == "completed"


async def test_lost_inflight_insert_response_reconciles_without_aborting_the_multipart(
    world: TusWorld,
):
    world.inflight.fail_after_commit = TimeoutError("response lost after commit")
    created = await world.manager.create_async(
        owner_id="user-a", file_path="docs/new.pdf", upload_length=len(CONTENT)
    )
    world.inflight.fail_after_commit = None

    assert created.upload_offset == 0
    assert set(world.inflight.rows) == {created.upload_id}
    assert len(world.s3.uploads) == 1

    offset = 0
    for chunk in chunks_of(CONTENT):
        offset = (
            await world.manager.append_async(
                upload_id=created.upload_id, owner_id="user-a", body=chunk, client_offset=offset
            )
        ).new_offset
    result = await world.manager.finalize_async(upload_id=created.upload_id, owner_id="user-a")
    assert _stored(world, world.files.rows[result.file_id]) == CONTENT


async def test_concurrent_finalizers_of_a_ready_upload_have_exactly_one_winner(world: TusWorld):
    upload_id = await upload_to_ready(world, owner="user-a", path="docs/q1.pdf", content=CONTENT)

    outcomes = await asyncio.gather(
        world.manager.finalize_async(upload_id=upload_id, owner_id="user-a"),
        world.manager.finalize_async(upload_id=upload_id, owner_id="user-a"),
        return_exceptions=True,
    )

    assert sum(not isinstance(o, BaseException) for o in outcomes) == 1
    assert sum(isinstance(o, UploadCompleted) for o in outcomes) == 1
    assert world.s3.complete_calls == 1
    [row] = world.live_files()
    assert _stored(world, row) == CONTENT


# ---------------------------------------------------------------------------
# Cleanup sweep
# ---------------------------------------------------------------------------


async def test_sweep_finalizes_expired_ready_uploads_via_host_and_aborts_stale_ones(world: TusWorld):
    ready_id = await upload_to_ready(world, owner="user-a", path="docs/ready.pdf", content=CONTENT)
    stale = await world.manager.create_async(owner_id="user-b", file_path="docs/stale.pdf", upload_length=10)
    fresh = await world.manager.create_async(owner_id="user-c", file_path="docs/fresh.pdf", upload_length=10)
    past = datetime.now(UTC) - timedelta(hours=1)
    world.session_row(ready_id)["expires_at"] = past
    world.session_row(stale.upload_id)["expires_at"] = past
    world.session_row(fresh.upload_id)["expires_at"] = datetime.now(UTC) + timedelta(days=1)

    host_calls: list[tuple[str, str]] = []

    async def finalize_ready(fm, manager, upload_id: str, owner_id: str):
        host_calls.append((upload_id, owner_id))
        return await manager.finalize_async(
            upload_id=upload_id, owner_id=owner_id, extra_metadata={"request_id": "sweep"}
        )

    report = await sweep_once(world.file_manager, finalize_ready=finalize_ready)

    assert (report.scanned, report.finalized, report.aborted, report.failed) == (2, 1, 1, 0)
    assert host_calls == [(ready_id, "user-a")]
    [row] = world.live_files()
    assert row["metadata"]["request_id"] == "sweep"
    assert _stored(world, row) == CONTENT
    assert world.session_row(stale.upload_id)["status"] == "aborted"
    assert world.session_row(fresh.upload_id)["status"] == "in_progress"
    assert [u["Key"] for u in world.s3.uploads.values()] == [world.session_row(fresh.upload_id)["key"]]


async def test_sweep_finishes_status_when_a_prior_cleanup_already_released_storage(world: TusWorld):
    created = await world.manager.create_async(owner_id="user-a", file_path="docs/q1.pdf", upload_length=10)
    row = world.session_row(created.upload_id)
    row["status"] = "aborting"
    row["expires_at"] = datetime.now(UTC) - timedelta(hours=1)
    world.s3.uploads.clear()  # the MPU was aborted by a prior pass whose status write was lost

    report = await sweep_once(world.file_manager)

    assert (report.aborted, report.failed) == (1, 0)
    assert world.session_row(created.upload_id)["status"] == "aborted"
