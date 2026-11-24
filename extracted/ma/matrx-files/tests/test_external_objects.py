from __future__ import annotations

import asyncio
import hashlib
from contextlib import asynccontextmanager
from pathlib import Path

import pytest
from pydantic import ValidationError

import matrx_files.external_objects as external_objects
from matrx_files.cloud_sync.sync_engine import SyncEngine
from matrx_files.derivations import (
    ClientPolicyMetadataError,
    assert_no_client_policy_metadata,
)
from matrx_files.external_objects import (
    ExternalObjectAdoptionRequest,
    ExternalObjectDriftError,
    adopt_external_object,
    read_external_object_with_receipt,
    run_external_object_custody_canary,
)
from matrx_files.retention import VOICE_RECORDING_RETENTION_POLICY


OWNER_ID = "11111111-1111-4111-8111-111111111111"
OTHER_ID = "22222222-2222-4222-8222-222222222222"
ORG_ID = "33333333-3333-4333-8333-333333333333"
STORAGE_URI = "s3://recordings/twilio/us1/owner-beta/RE123.wav"
CONTENT = b"RIFF-owner-beta-recording"


class _S3:
    def __init__(self) -> None:
        self.objects = {"recordings/twilio/us1/owner-beta/RE123.wav": CONTENT}
        self.drift_on_download = False

    async def get_metadata_async(self, path: str) -> dict[str, object]:
        content = self.objects[path]
        return {
            "content_type": "audio/wav",
            "size": len(content),
            "last_modified": "2026-08-15T12:00:00Z",
            "etag": hashlib.md5(content, usedforsecurity=False).hexdigest(),
        }


class _Router:
    def __init__(self) -> None:
        self.s3 = _S3()

    async def download_to_path_async(self, uri: str, local_path: str) -> int:
        path = uri.removeprefix("s3://")
        content = self.s3.objects[path]
        await asyncio.to_thread(Path(local_path).write_bytes, content)
        if self.s3.drift_on_download:
            self.s3.objects[path] = content + b"-changed"
        return len(content)

    async def read_async(self, uri: str) -> bytes:
        return self.s3.objects[uri.removeprefix("s3://")]

    async def delete_async(self, uri: str) -> bool:
        self.s3.objects.pop(uri.removeprefix("s3://"), None)
        return True


@pytest.fixture(autouse=True)
def _external_database_transaction(monkeypatch: pytest.MonkeyPatch) -> None:
    # These existing unit tests replace the database; transaction integration is separate.
    @asynccontextmanager
    async def transaction(*, database: str):
        yield

    monkeypatch.setattr(external_objects, "transaction", transaction)


class _PathCollision(Exception):
    sqlstate = "23505"
    constraint_name = "cld_files_owner_id_file_path_key"


class _Db:
    @staticmethod
    def _db_name() -> str:
        return "unit-test"

    def __init__(self) -> None:
        self.rows: dict[str, dict[str, object]] = {}
        self.events: list[dict[str, object]] = []

    async def get_file_by_path_async(
        self, owner_id: str, file_path: str
    ) -> dict[str, object] | None:
        return next(
            (
                row
                for row in self.rows.values()
                if row["owner_id"] == owner_id and row["file_path"] == file_path
            ),
            None,
        )

    async def upsert_file_async(
        self, payload: dict[str, object]
    ) -> dict[str, object]:
        row = dict(payload)
        self.rows[str(row["id"])] = row
        return row

    async def append_event_async(
        self,
        event_type: str,
        *,
        actor_id: str,
        organization_id: str | None = None,
        actor_type: str = "user",
        resource_type: str | None = None,
        resource_id: str | None = None,
        payload: dict[str, object] | None = None,
        request_id: str | None = None,
        ip_address: str | None = None,
    ) -> None:
        self.events.append(
            {
                "event_type": event_type,
                "actor_id": actor_id,
                "organization_id": organization_id,
                "actor_type": actor_type,
                "resource_type": resource_type,
                "resource_id": resource_id,
                "payload": payload,
                "request_id": request_id,
                "ip_address": ip_address,
            }
        )


class _Engine:
    _is_folder_path_unique_violation = staticmethod(SyncEngine._is_folder_path_unique_violation)
    _is_path_unique_violation = staticmethod(SyncEngine._is_path_unique_violation)
    _is_dedup_unique_violation = staticmethod(SyncEngine._is_dedup_unique_violation)

    def __init__(self) -> None:
        self.router = _Router()
        self.db = _Db()
        self.allow_shared = False

    async def _resolve_write_organization_id_async(
        self, owner_id: str, organization_id: str | None = None
    ) -> str:
        assert owner_id == OWNER_ID
        return organization_id or ORG_ID

    async def _ensure_folder_async(
        self, file_path: str, owner_id: str, organization_id: str
    ) -> str:
        assert file_path.startswith(".matrx-tmp/voice-recordings/")
        assert owner_id == OWNER_ID
        assert organization_id == ORG_ID
        return "44444444-4444-4444-8444-444444444444"

    async def get_authorized_record_async(
        self,
        file_id: str,
        *,
        user_id: str,
        level: str = "read",
    ) -> dict[str, object]:
        row = self.db.rows[file_id]
        if row["owner_id"] != user_id and not self.allow_shared:
            raise PermissionError("denied")
        assert level in {"read", "admin"}
        return row

    async def hard_delete_and_purge_async(
        self, file_id: str, storage_uri: object
    ) -> dict[str, object]:
        assert isinstance(storage_uri, str)
        await self.router.delete_async(storage_uri)
        self.db.rows.pop(file_id)
        return {"main": storage_uri, "versions": []}


def _request() -> ExternalObjectAdoptionRequest:
    return ExternalObjectAdoptionRequest(
        owner_id=OWNER_ID,
        organization_id=ORG_ID,
        storage_uri=STORAGE_URI,
        file_path=".matrx-tmp/voice-recordings/recording_RE123.wav",
        file_name="recording_RE123.wav",
        mime_type="audio/wav",
        source_kind="twilio_voice_recording",
        source_event_key="twilio:voice-recording:AC123:RE123:completed",
        expected_size_bytes=len(CONTENT),
        expected_sha256=hashlib.sha256(CONTENT).hexdigest(),
    )


def test_request_refuses_provider_urls_and_non_retained_paths() -> None:
    values = _request().model_dump()
    values["storage_uri"] = "https://api.twilio.com/recording.wav?token=secret"
    with pytest.raises(ValidationError, match="native s3"):
        ExternalObjectAdoptionRequest.model_validate(values)


def test_client_metadata_cannot_mutate_custody_evidence() -> None:
    with pytest.raises(ClientPolicyMetadataError, match="durable evidence"):
        assert_no_client_policy_metadata(
            {"external_object_custody": {"sha256": "forged"}},
            existing={"external_object_custody": {"sha256": "real"}},
        )

    values = _request().model_dump()
    values["file_path"] = "system-files/recording.wav"
    values["file_name"] = "recording.wav"
    with pytest.raises(ValidationError, match="below .matrx-tmp"):
        ExternalObjectAdoptionRequest.model_validate(values)


@pytest.mark.asyncio
async def test_adoption_indexes_personal_file_without_returning_storage_location() -> None:
    engine = _Engine()

    result = await adopt_external_object(
        engine,
        _request(),
        retention_policy=VOICE_RECORDING_RETENTION_POLICY,
    )

    row = engine.db.rows[result.file_id]
    assert row["published_to_web"] is False
    # No hand-written label: NULL follows the file type's "Shown to" knob.
    assert row["shown_to"] is None
    assert row["checksum"] == hashlib.sha256(CONTENT).hexdigest()
    assert row["storage_uri"] == STORAGE_URI
    assert result.evidence.retention_policy == "voice_recordings_30d"
    assert result.evidence.retention_expires_at > result.evidence.adopted_at
    assert "storage_uri" not in result.model_dump_json()
    assert engine.db.events[-1]["event_type"] == "file.external_object_adopted"
    assert engine.db.events[-1]["organization_id"] == ORG_ID


@pytest.mark.asyncio
async def test_identical_replay_returns_same_file_and_different_operation_receipt() -> None:
    engine = _Engine()
    first = await adopt_external_object(
        engine,
        _request(),
        retention_policy=VOICE_RECORDING_RETENTION_POLICY,
    )
    second = await adopt_external_object(
        engine,
        _request(),
        retention_policy=VOICE_RECORDING_RETENTION_POLICY,
    )

    assert second.file_id == first.file_id
    assert second.replayed is True
    assert second.evidence.custody_receipt_id == first.evidence.custody_receipt_id
    assert second.operation_receipt_id != first.operation_receipt_id
    assert len(engine.db.rows) == 1
    assert engine.db.events[-1]["event_type"] == "file.external_object_adoption_replayed"


@pytest.mark.asyncio
async def test_adoption_refuses_object_that_changes_during_stream() -> None:
    engine = _Engine()
    engine.router.s3.drift_on_download = True

    with pytest.raises(ExternalObjectDriftError, match="metadata changed"):
        await adopt_external_object(
            engine,
            _request(),
            retention_policy=VOICE_RECORDING_RETENTION_POLICY,
        )

    assert engine.db.rows == {}
    assert engine.db.events == []


@pytest.mark.asyncio
async def test_read_refuses_other_owner_before_bytes_or_audit() -> None:
    engine = _Engine()
    adopted = await adopt_external_object(
        engine,
        _request(),
        retention_policy=VOICE_RECORDING_RETENTION_POLICY,
    )
    event_count = len(engine.db.events)

    with pytest.raises(PermissionError):
        await read_external_object_with_receipt(
            engine,
            file_id=adopted.file_id,
            user_id=OTHER_ID,
        )

    assert len(engine.db.events) == event_count


@pytest.mark.asyncio
async def test_external_object_stays_owner_only_even_if_generic_judge_allows_share() -> None:
    engine = _Engine()
    adopted = await adopt_external_object(
        engine,
        _request(),
        retention_policy=VOICE_RECORDING_RETENTION_POLICY,
    )
    engine.allow_shared = True
    event_count = len(engine.db.events)

    with pytest.raises(PermissionError, match="restricted to their owner"):
        await read_external_object_with_receipt(
            engine,
            file_id=adopted.file_id,
            user_id=OTHER_ID,
        )

    assert len(engine.db.events) == event_count


@pytest.mark.asyncio
async def test_canary_proves_owner_read_and_governed_delete_with_receipts() -> None:
    engine = _Engine()

    result = await run_external_object_custody_canary(
        engine,
        _request(),
        retention_policy=VOICE_RECORDING_RETENTION_POLICY,
    )

    assert result.sha256 == hashlib.sha256(CONTENT).hexdigest()
    assert result.size_bytes == len(CONTENT)
    assert result.deleted is True
    assert engine.db.rows == {}
    assert engine.router.s3.objects == {}
    assert [event["event_type"] for event in engine.db.events] == [
        "file.external_object_adopted",
        "file.external_object_read",
        "file.external_object_delete_authorized",
        "file.external_object_deleted",
    ]

@pytest.mark.asyncio
@pytest.mark.parametrize("branch", ["existing", "concurrent"])
@pytest.mark.parametrize("constraint", ["cld_files_owner_id_file_path_key", "cld_files_dedup_canonical", "uq_cld_files_storage_uri"])
@pytest.mark.parametrize("drift", [
    "owner", "path", "organization", "published", "shown", "uri", "checksum", "size", "mime",
    "source_kind", "event", "identity", "evidence_sha", "evidence_size",
])
async def test_concurrent_winner_must_match_the_same_custody_as_existing_replay(
    drift: str, branch: str, constraint: str,
) -> None:
    """A losing insert may never adopt a winner the ordinary replay would refuse."""
    engine = _Engine()
    first = await adopt_external_object(engine, _request(), retention_policy=VOICE_RECORDING_RETENTION_POLICY)
    row = engine.db.rows[first.file_id]
    metadata = row["metadata"]
    assert isinstance(metadata, dict)
    custody = metadata["external_object_custody"]
    assert isinstance(custody, dict)
    mutations = {
        "owner": (row, "owner_id", OTHER_ID),
        "path": (row, "file_path", "different/path"),
        "organization": (row, "organization_id", OTHER_ID),
        "published": (row, "published_to_web", True),
        "shown": (row, "shown_to", "everyone"),
        "uri": (row, "storage_uri", "s3://recordings/twilio/us1/owner-beta/other.wav"),
        "checksum": (row, "checksum", "0" * 64),
        "size": (row, "size_bytes", len(CONTENT) + 1),
        "mime": (row, "mime_type", "audio/mpeg"),
        "source_kind": (custody, "source_kind", "other"),
        "event": (custody, "source_event_key_hash", "0" * 64),
        "identity": (custody, "object_identity_hash", "0" * 64),
        "evidence_sha": (custody, "sha256", "0" * 64),
        "evidence_size": (custody, "size_bytes", len(CONTENT) + 1),
    }
    target, field, value = mutations[drift]
    target[field] = value
    reads = 0
    async def get_row(owner_id: str, file_path: str) -> dict[str, object] | None:
        nonlocal reads
        reads += 1
        return None if branch == "concurrent" and reads == 1 else row
    async def conflict(payload: dict[str, object]) -> dict[str, object]:
        error = _PathCollision("synthetic concurrent insert")
        error.constraint_name = constraint
        raise error
    engine.db.get_file_by_path_async = get_row
    engine.db.upsert_file_async = conflict
    previous_receipts = len(engine.db.events)
    with pytest.raises(ExternalObjectDriftError, match="custody evidence"):
        await adopt_external_object(engine, _request(), retention_policy=VOICE_RECORDING_RETENTION_POLICY)
    assert reads == (2 if branch == "concurrent" else 1)
    assert len(engine.db.events) == previous_receipts


@pytest.mark.asyncio
@pytest.mark.parametrize("constraint", ["cld_files_owner_id_file_path_key", "cld_files_dedup_canonical", "uq_cld_files_storage_uri"])
@pytest.mark.parametrize("organization_id", [ORG_ID, None])
@pytest.mark.parametrize("shown_to", [None, "only_me"])
async def test_identical_concurrent_winner_remains_a_replay(
    organization_id: str | None, shown_to: str | None, constraint: str,
) -> None:
    engine = _Engine()
    request = _request().model_copy(update={"organization_id": organization_id})
    first = await adopt_external_object(engine, request, retention_policy=VOICE_RECORDING_RETENTION_POLICY)
    row = engine.db.rows[first.file_id]
    row["shown_to"] = shown_to
    reads = 0
    async def get_row(owner_id: str, file_path: str) -> dict[str, object] | None:
        nonlocal reads
        reads += 1
        return None if reads == 1 else row
    async def conflict(payload: dict[str, object]) -> dict[str, object]:
        error = _PathCollision("synthetic concurrent insert")
        error.constraint_name = constraint
        raise error
    engine.db.get_file_by_path_async = get_row
    engine.db.upsert_file_async = conflict
    replay = await adopt_external_object(engine, request, retention_policy=VOICE_RECORDING_RETENTION_POLICY)
    assert replay.file_id == first.file_id and replay.replayed
    assert replay.organization_id == ORG_ID
    assert replay.evidence.custody_receipt_id == first.evidence.custody_receipt_id
    assert replay.operation_receipt_id != first.operation_receipt_id
    assert engine.db.events[-1]["event_type"] == "file.external_object_adoption_replayed"

@pytest.mark.asyncio
async def test_unrelated_insert_failure_is_not_misreported_as_replay() -> None:
    engine = _Engine()
    first = await adopt_external_object(engine, _request(), retention_policy=VOICE_RECORDING_RETENTION_POLICY)
    winner = engine.db.rows[first.file_id]
    reads = 0

    async def get_row(owner_id: str, file_path: str) -> dict[str, object] | None:
        nonlocal reads
        reads += 1
        return None if reads == 1 else winner

    async def fail_insert(payload: dict[str, object]) -> dict[str, object]:
        raise RuntimeError("database unavailable")

    engine.db.get_file_by_path_async = get_row
    engine.db.upsert_file_async = fail_insert
    with pytest.raises(RuntimeError, match="database unavailable"):
        await adopt_external_object(engine, _request(), retention_policy=VOICE_RECORDING_RETENTION_POLICY)
    assert len(engine.db.events) == 1


@pytest.mark.asyncio
@pytest.mark.parametrize("constraint,sqlstate,winner_exists", [
    ("cld_files_dedup_canonical", "23505", False),
    ("uq_cld_files_storage_uri", "23505", False),
    ("cld_files_pkey", "23505", True),
    ("cld_files_id_organization_id_key", "23505", True),
    ("unknown_unique", "23505", True),
    ("cld_files_dedup_canonical", "23503", True),
])
async def test_collision_without_matching_winner_or_known_constraint_propagates(
    constraint: str, sqlstate: str, winner_exists: bool,
) -> None:
    engine = _Engine()
    first = await adopt_external_object(engine, _request(), retention_policy=VOICE_RECORDING_RETENTION_POLICY)
    winner = engine.db.rows[first.file_id]
    reads = 0

    async def get_row(owner_id: str, file_path: str) -> dict[str, object] | None:
        nonlocal reads
        reads += 1
        return winner if reads > 1 and winner_exists else None

    error = _PathCollision("insert failed")
    error.constraint_name = constraint
    error.sqlstate = sqlstate

    async def conflict(payload: dict[str, object]) -> dict[str, object]:
        raise error

    engine.db.get_file_by_path_async = get_row
    engine.db.upsert_file_async = conflict
    with pytest.raises(_PathCollision) as caught:
        await adopt_external_object(engine, _request(), retention_policy=VOICE_RECORDING_RETENTION_POLICY)
    assert caught.value is error
    assert len(engine.db.events) == 1
    assert reads == (3 if not winner_exists and sqlstate == "23505" else 1)
