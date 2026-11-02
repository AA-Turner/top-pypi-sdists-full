from __future__ import annotations

import hashlib
from pathlib import Path

import pytest
from pydantic import ValidationError

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
        Path(local_path).write_bytes(content)
        if self.s3.drift_on_download:
            self.s3.objects[path] = content + b"-changed"
        return len(content)

    async def read_async(self, uri: str) -> bytes:
        return self.s3.objects[uri.removeprefix("s3://")]

    async def delete_async(self, uri: str) -> bool:
        self.s3.objects.pop(uri.removeprefix("s3://"), None)
        return True


class _Db:
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
    assert row["shown_to"] == "only_me"
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
