"""Adopt provider-written S3 objects into canonical AI Matrx file custody.

The provider location is server-only evidence. Callers receive a ``file_id``
and checksummed receipts; they never receive the bucket/key or a provider URL.
"""

from __future__ import annotations

import asyncio
import hashlib
import json
import os
import tempfile
import uuid
from datetime import UTC, datetime
from pathlib import PurePosixPath
from typing import TYPE_CHECKING, Literal
from urllib.parse import urlparse

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    JsonValue,
    field_validator,
    model_validator,
)

from .dedup import compute_checksum_stream
from .derivations import EXTERNAL_OBJECT_CUSTODY_METADATA_KEY
from .retention import TemporaryFileRetentionPolicy

if TYPE_CHECKING:
    from .cloud_sync.sync_engine import SyncEngine


_CUSTODY_VERSION = 1
_GENERIC_OBJECT_MIMES = frozenset({"", "application/octet-stream", "binary/octet-stream"})


class ExternalObjectError(RuntimeError):
    """Base error for a provider-external object custody operation."""


class ExternalObjectMismatchError(ExternalObjectError):
    """The stored object does not match the caller's expected evidence."""


class ExternalObjectDriftError(ExternalObjectError):
    """The object or canonical row changed across an adoption/read boundary."""


class ExternalObjectAdoptionRequest(BaseModel):
    """Trusted server request to adopt one already-written S3 object."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    owner_id: str = Field(min_length=36, max_length=36)
    organization_id: str | None = Field(default=None, min_length=36, max_length=36)
    storage_uri: str = Field(min_length=8, max_length=2_048)
    file_path: str = Field(min_length=1, max_length=1_024)
    file_name: str = Field(min_length=1, max_length=255)
    mime_type: str = Field(min_length=3, max_length=255)
    source_kind: str = Field(
        min_length=1,
        max_length=100,
        pattern=r"^[a-z][a-z0-9_-]*$",
    )
    source_event_key: str = Field(min_length=8, max_length=512)
    expected_size_bytes: int | None = Field(default=None, ge=0)
    expected_sha256: str | None = Field(
        default=None,
        pattern=r"^[0-9a-f]{64}$",
    )
    metadata: dict[str, JsonValue] = Field(default_factory=dict)

    @field_validator("owner_id", "organization_id")
    @classmethod
    def _validate_uuid(cls, value: str | None) -> str | None:
        if value is None:
            return None
        try:
            parsed = uuid.UUID(value)
        except ValueError as exc:
            raise ValueError("must be a UUID") from exc
        if str(parsed) != value.lower():
            raise ValueError("must be a canonical lowercase UUID")
        return value

    @field_validator("storage_uri")
    @classmethod
    def _validate_storage_uri(cls, value: str) -> str:
        parsed = urlparse(value)
        key = parsed.path.lstrip("/")
        if (
            parsed.scheme != "s3"
            or not parsed.netloc
            or not key
            or parsed.params
            or parsed.query
            or parsed.fragment
            or parsed.username
            or parsed.password
            or ".." in PurePosixPath(key).parts
            or any(ord(char) < 32 for char in value)
        ):
            raise ValueError(
                "storage_uri must be a native s3://bucket/key URI with no credentials, "
                "query, fragment, traversal, or control characters"
            )
        return f"s3://{parsed.netloc}/{key}"

    @field_validator("file_path")
    @classmethod
    def _validate_file_path(cls, value: str) -> str:
        path = PurePosixPath(value)
        if (
            value.startswith("/")
            or "\\" in value
            or ".." in path.parts
            or not value.startswith(".matrx-tmp/")
            or any(ord(char) < 32 for char in value)
        ):
            raise ValueError(
                "file_path must be a normalized relative path below .matrx-tmp/"
            )
        return value

    @field_validator("file_name")
    @classmethod
    def _validate_file_name(cls, value: str) -> str:
        if value in {".", ".."} or "/" in value or "\\" in value:
            raise ValueError("file_name must be one basename")
        if any(ord(char) < 32 for char in value):
            raise ValueError("file_name cannot contain control characters")
        return value

    @field_validator("mime_type")
    @classmethod
    def _validate_mime_type(cls, value: str) -> str:
        if "/" not in value or any(ord(char) < 32 for char in value):
            raise ValueError("mime_type must be a valid media type")
        return value.lower()

    @model_validator(mode="after")
    def _validate_path_name_and_metadata(self) -> ExternalObjectAdoptionRequest:
        if PurePosixPath(self.file_path).name != self.file_name:
            raise ValueError("file_name must equal the basename of file_path")
        if (
            EXTERNAL_OBJECT_CUSTODY_METADATA_KEY in self.metadata
            or "storage_uri" in self.metadata
        ):
            raise ValueError("metadata cannot override custody fields or expose storage_uri")
        return self


class ExternalObjectCustodyEvidence(BaseModel):
    """Stable, non-secret evidence stored with and returned for the file."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    version: Literal[1] = 1
    source_kind: str
    source_event_key_hash: str
    object_identity_hash: str
    sha256: str
    size_bytes: int
    mime_type: str
    retention_policy: str
    adopted_at: datetime
    retention_expires_at: datetime
    custody_receipt_id: str


class ExternalObjectAdoptionResult(BaseModel):
    """Canonical identity and evidence; deliberately excludes storage location."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    file_id: str
    owner_id: str
    organization_id: str
    file_path: str
    evidence: ExternalObjectCustodyEvidence
    operation_receipt_id: str
    replayed: bool


class ExternalObjectReadResult(BaseModel):
    """Owner-authorized canary read plus an audit receipt."""

    model_config = ConfigDict(extra="forbid", frozen=True, arbitrary_types_allowed=True)

    file_id: str
    content: bytes
    sha256: str
    size_bytes: int
    operation_receipt_id: str


class ExternalObjectDeleteResult(BaseModel):
    """Governed hard-delete result without exposing purged storage locations."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    file_id: str
    operation_receipt_id: str
    deleted: bool


class ExternalObjectCustodyCanaryResult(BaseModel):
    """End-to-end application custody proof for a provider-written canary."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    adoption: ExternalObjectAdoptionResult
    read_receipt_id: str
    delete_receipt_id: str
    sha256: str
    size_bytes: int
    deleted: bool


class _ObjectSnapshot(BaseModel):
    model_config = ConfigDict(extra="ignore", frozen=True)

    content_type: str = ""
    size: int = Field(ge=0)
    last_modified: str = ""
    etag: str = ""


def _sha256_text(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def _object_identity_hash(
    *, source_event_key_hash: str, snapshot: _ObjectSnapshot, sha256: str
) -> str:
    payload = {
        "source_event_key_hash": source_event_key_hash,
        "size": snapshot.size,
        "last_modified": snapshot.last_modified,
        "etag": snapshot.etag,
        "sha256": sha256,
    }
    return _sha256_text(json.dumps(payload, sort_keys=True, separators=(",", ":")))


async def _snapshot_s3(engine: SyncEngine, storage_uri: str) -> _ObjectSnapshot:
    _, raw_path = storage_uri.split("://", 1)
    metadata = await engine.router.s3.get_metadata_async(raw_path)
    return _ObjectSnapshot.model_validate(metadata)


async def _stream_and_hash(engine: SyncEngine, storage_uri: str) -> tuple[int, str]:
    descriptor, temp_name = tempfile.mkstemp(prefix="matrx-external-object-")
    os.close(descriptor)
    try:
        downloaded = await engine.router.download_to_path_async(storage_uri, temp_name)

        def _hash() -> str:
            with open(temp_name, "rb") as reader:
                return compute_checksum_stream(reader)

        checksum = await asyncio.to_thread(_hash)
        actual_size = os.path.getsize(temp_name)
        if downloaded != actual_size:
            raise ExternalObjectDriftError(
                "external object download byte count changed while establishing custody"
            )
        return actual_size, checksum
    finally:
        try:
            os.unlink(temp_name)
        except FileNotFoundError:
            pass


def _validate_object(
    request: ExternalObjectAdoptionRequest,
    *,
    before: _ObjectSnapshot,
    after: _ObjectSnapshot,
    actual_size: int,
    sha256: str,
) -> None:
    if before != after:
        raise ExternalObjectDriftError(
            "external object metadata changed while establishing custody"
        )
    if before.size != actual_size:
        raise ExternalObjectDriftError(
            "external object HEAD size did not match the streamed byte count"
        )
    if request.expected_size_bytes is not None and request.expected_size_bytes != actual_size:
        raise ExternalObjectMismatchError("external object size did not match expected evidence")
    if request.expected_sha256 is not None and request.expected_sha256 != sha256:
        raise ExternalObjectMismatchError("external object SHA-256 did not match expected evidence")
    object_mime = before.content_type.lower()
    if object_mime not in _GENERIC_OBJECT_MIMES and object_mime != request.mime_type:
        raise ExternalObjectMismatchError(
            "external object content type did not match expected evidence"
        )


def _custody_from_row(row: dict[str, object]) -> ExternalObjectCustodyEvidence:
    metadata = row.get("metadata")
    if not isinstance(metadata, dict):
        raise ExternalObjectDriftError("canonical file is missing custody metadata")
    custody = metadata.get(EXTERNAL_OBJECT_CUSTODY_METADATA_KEY)
    try:
        return ExternalObjectCustodyEvidence.model_validate(custody)
    except Exception as exc:
        raise ExternalObjectDriftError(
            "canonical file has invalid external-object custody evidence"
        ) from exc


async def _append_receipt(
    engine: SyncEngine,
    *,
    action: str,
    owner_id: str,
    organization_id: str,
    file_id: str,
    receipt_id: str,
    evidence: ExternalObjectCustodyEvidence,
) -> None:
    await engine.db.append_event_async(
        action,
        actor_id=owner_id,
        organization_id=organization_id,
        resource_type="file",
        resource_id=file_id,
        payload={
            "receipt_id": receipt_id,
            "source_kind": evidence.source_kind,
            "source_event_key_hash": evidence.source_event_key_hash,
            "object_identity_hash": evidence.object_identity_hash,
            "sha256": evidence.sha256,
            "size_bytes": evidence.size_bytes,
            "retention_policy": evidence.retention_policy,
            "retention_expires_at": evidence.retention_expires_at.isoformat(),
        },
    )


async def adopt_external_object(
    engine: SyncEngine,
    request: ExternalObjectAdoptionRequest,
    *,
    retention_policy: TemporaryFileRetentionPolicy,
) -> ExternalObjectAdoptionResult:
    """Index one immutable provider-written S3 object as a personal file.

    This function never copies or rewrites provider bytes. It proves the
    object did not change across a streaming SHA-256 read, inserts one
    canonical row, and durably audits the custody receipt before returning.
    """
    if not retention_policy.matches_path(request.file_path):
        raise ValueError(
            f"file_path is outside retention policy {retention_policy.name!r}"
        )

    before = await _snapshot_s3(engine, request.storage_uri)
    actual_size, sha256 = await _stream_and_hash(engine, request.storage_uri)
    after = await _snapshot_s3(engine, request.storage_uri)
    _validate_object(
        request,
        before=before,
        after=after,
        actual_size=actual_size,
        sha256=sha256,
    )

    source_event_key_hash = _sha256_text(request.source_event_key)
    identity_hash = _object_identity_hash(
        source_event_key_hash=source_event_key_hash,
        snapshot=after,
        sha256=sha256,
    )
    existing = await engine.db.get_file_by_path_async(request.owner_id, request.file_path)
    operation_receipt_id = str(uuid.uuid4())
    if existing is not None:
        evidence = _custody_from_row(existing)
        existing_uri = existing.get("storage_uri")
        if (
            str(existing.get("owner_id") or "") != request.owner_id
            or str(existing.get("organization_id") or "")
            != str(request.organization_id or existing.get("organization_id") or "")
            or bool(existing.get("published_to_web"))
            or existing.get("shown_to") != "only_me"
            or existing_uri != request.storage_uri
            or str(existing.get("checksum") or "") != sha256
            or int(existing.get("size_bytes") or -1) != actual_size
            or str(existing.get("mime_type") or "").lower() != request.mime_type
            or evidence.source_kind != request.source_kind
            or evidence.source_event_key_hash != source_event_key_hash
            or evidence.object_identity_hash != identity_hash
            or evidence.sha256 != sha256
            or evidence.size_bytes != actual_size
        ):
            raise ExternalObjectDriftError(
                "idempotent adoption found a canonical row with different custody evidence"
            )
        await _append_receipt(
            engine,
            action="file.external_object_adoption_replayed",
            owner_id=request.owner_id,
            organization_id=str(existing["organization_id"]),
            file_id=str(existing["id"]),
            receipt_id=operation_receipt_id,
            evidence=evidence,
        )
        return ExternalObjectAdoptionResult(
            file_id=str(existing["id"]),
            owner_id=request.owner_id,
            organization_id=str(existing["organization_id"]),
            file_path=request.file_path,
            evidence=evidence,
            operation_receipt_id=operation_receipt_id,
            replayed=True,
        )

    organization_id = await engine._resolve_write_organization_id_async(
        request.owner_id,
        request.organization_id,
    )
    folder_id = await engine._ensure_folder_async(
        request.file_path,
        request.owner_id,
        organization_id,
    )
    adopted_at = datetime.now(UTC)
    custody_receipt_id = str(uuid.uuid4())
    evidence = ExternalObjectCustodyEvidence(
        source_kind=request.source_kind,
        source_event_key_hash=source_event_key_hash,
        object_identity_hash=identity_hash,
        sha256=sha256,
        size_bytes=actual_size,
        mime_type=request.mime_type,
        retention_policy=retention_policy.name,
        adopted_at=adopted_at,
        retention_expires_at=adopted_at + retention_policy.ttl,
        custody_receipt_id=custody_receipt_id,
    )
    metadata = dict(request.metadata)
    metadata[EXTERNAL_OBJECT_CUSTODY_METADATA_KEY] = evidence.model_dump(mode="json")
    file_id = str(uuid.uuid4())
    insert_payload: dict[str, object] = {
        "id": file_id,
        "owner_id": request.owner_id,
        "organization_id": organization_id,
        "parent_folder_id": folder_id,
        "file_path": request.file_path,
        "file_name": request.file_name,
        "storage_uri": request.storage_uri,
        "mime_type": request.mime_type,
        "size_bytes": actual_size,
        "checksum": sha256,
        "published_to_web": False,
        "shown_to": "only_me",
        "metadata": metadata,
    }
    try:
        row = await engine.db.upsert_file_async(insert_payload)
        replayed = False
    except Exception as exc:
        winner = await engine.db.get_file_by_path_async(request.owner_id, request.file_path)
        if winner is None:
            raise
        winner_evidence = _custody_from_row(winner)
        if (
            winner.get("storage_uri") != request.storage_uri
            or winner_evidence.source_event_key_hash != source_event_key_hash
            or winner_evidence.object_identity_hash != identity_hash
        ):
            raise ExternalObjectDriftError(
                "concurrent adoption won the path with different custody evidence"
            ) from exc
        row = winner
        evidence = winner_evidence
        file_id = str(winner["id"])
        replayed = True

    action = (
        "file.external_object_adoption_replayed"
        if replayed
        else "file.external_object_adopted"
    )
    await _append_receipt(
        engine,
        action=action,
        owner_id=request.owner_id,
        organization_id=str(row["organization_id"]),
        file_id=file_id,
        receipt_id=operation_receipt_id,
        evidence=evidence,
    )
    return ExternalObjectAdoptionResult(
        file_id=file_id,
        owner_id=request.owner_id,
        organization_id=str(row["organization_id"]),
        file_path=request.file_path,
        evidence=evidence,
        operation_receipt_id=operation_receipt_id,
        replayed=replayed,
    )


async def read_external_object_with_receipt(
    engine: SyncEngine,
    *,
    file_id: str,
    user_id: str,
) -> ExternalObjectReadResult:
    """Read adopted bytes through the canonical access judge and audit it."""
    row = await engine.get_authorized_record_async(file_id, user_id=user_id, level="read")
    if str(row.get("owner_id") or "") != user_id:
        raise PermissionError("provider-external objects are restricted to their owner")
    evidence = _custody_from_row(row)
    content = await engine.router.read_async(str(row["storage_uri"]))
    sha256 = hashlib.sha256(content).hexdigest()
    if (
        sha256 != evidence.sha256
        or len(content) != evidence.size_bytes
        or str(row.get("checksum") or "") != evidence.sha256
    ):
        raise ExternalObjectDriftError(
            "canonical external object no longer matches its custody evidence"
        )
    receipt_id = str(uuid.uuid4())
    await _append_receipt(
        engine,
        action="file.external_object_read",
        owner_id=user_id,
        organization_id=str(row["organization_id"]),
        file_id=file_id,
        receipt_id=receipt_id,
        evidence=evidence,
    )
    return ExternalObjectReadResult(
        file_id=file_id,
        content=content,
        sha256=sha256,
        size_bytes=len(content),
        operation_receipt_id=receipt_id,
    )


async def delete_external_object_with_receipt(
    engine: SyncEngine,
    *,
    file_id: str,
    user_id: str,
) -> ExternalObjectDeleteResult:
    """Hard-delete one adopted object through the governed purge path."""
    row = await engine.get_authorized_record_async(file_id, user_id=user_id, level="admin")
    if str(row.get("owner_id") or "") != user_id:
        raise PermissionError("provider-external objects are restricted to their owner")
    evidence = _custody_from_row(row)
    receipt_id = str(uuid.uuid4())
    await _append_receipt(
        engine,
        action="file.external_object_delete_authorized",
        owner_id=user_id,
        organization_id=str(row["organization_id"]),
        file_id=file_id,
        receipt_id=receipt_id,
        evidence=evidence,
    )
    await engine.hard_delete_and_purge_async(file_id, row.get("storage_uri"))
    await _append_receipt(
        engine,
        action="file.external_object_deleted",
        owner_id=user_id,
        organization_id=str(row["organization_id"]),
        file_id=file_id,
        receipt_id=receipt_id,
        evidence=evidence,
    )
    return ExternalObjectDeleteResult(
        file_id=file_id,
        operation_receipt_id=receipt_id,
        deleted=True,
    )


async def run_external_object_custody_canary(
    engine: SyncEngine,
    request: ExternalObjectAdoptionRequest,
    *,
    retention_policy: TemporaryFileRetentionPolicy,
) -> ExternalObjectCustodyCanaryResult:
    """Prove adoption, owner-only read, checksum, governed delete, and audit."""
    adoption = await adopt_external_object(
        engine,
        request,
        retention_policy=retention_policy,
    )
    read = await read_external_object_with_receipt(
        engine,
        file_id=adoption.file_id,
        user_id=request.owner_id,
    )
    deleted = await delete_external_object_with_receipt(
        engine,
        file_id=adoption.file_id,
        user_id=request.owner_id,
    )
    return ExternalObjectCustodyCanaryResult(
        adoption=adoption,
        read_receipt_id=read.operation_receipt_id,
        delete_receipt_id=deleted.operation_receipt_id,
        sha256=read.sha256,
        size_bytes=read.size_bytes,
        deleted=deleted.deleted,
    )


__all__ = [
    "ExternalObjectAdoptionRequest",
    "ExternalObjectAdoptionResult",
    "ExternalObjectCustodyCanaryResult",
    "ExternalObjectCustodyEvidence",
    "ExternalObjectDeleteResult",
    "ExternalObjectDriftError",
    "ExternalObjectError",
    "ExternalObjectMismatchError",
    "ExternalObjectReadResult",
    "adopt_external_object",
    "delete_external_object_with_receipt",
    "read_external_object_with_receipt",
    "run_external_object_custody_canary",
]
