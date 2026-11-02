"""TUS resumable upload state machine.

Pure storage-layer logic — no FastAPI, no HTTP. The host wraps this with
a thin protocol-marshaling layer that parses TUS headers, maps typed
errors to HTTP status codes, and runs auth + quota pre-flight.

Operations (5):

- :meth:`TUSSessionManager.create_async`   — allocate S3 multipart + insert inflight row
- :meth:`TUSSessionManager.get_async`      — load inflight row (for HEAD's Upload-Offset)
- :meth:`TUSSessionManager.append_async`   — append one chunk (one S3 part)
- :meth:`TUSSessionManager.finalize_async` — complete multipart + insert files.files row
- :meth:`TUSSessionManager.abort_async`    — abort multipart + mark inflight row aborted

All operations are idempotent on retry — replaying ``create_async`` with
the same ``(owner_id, idempotency_key)`` returns the in-progress row's
state rather than creating a duplicate; replaying ``abort_async`` after
abort succeeds is a no-op. The state lives in ``files.uploads_inflight``
(packaged migration ``005_tus_uploads_realtime.sql``), accessed through
the package's own matrx-orm models.
"""

from __future__ import annotations

import asyncio
import base64
import logging
import uuid
from dataclasses import dataclass, field
from datetime import UTC, datetime, timedelta
from typing import BinaryIO, TYPE_CHECKING, Any

from matrx_utils import supervised_task
from matrx_utils.row_access import RowAccess

from ...artifact_identity import artifact_identity_columns
from ...user_visible import stamp_machine_artifact
from ...derivations import resolve_file_lineage
from ..db import _models, _row, _vals
from ..preconditions import PreconditionFailed, check_expected_checksum

#: Server-stamped keys the inflight session carries between create and finalize.
#: The `_` namespace is already refused to clients by ``merge_metadata_json``, so
#: these can never be forged, and they are STRIPPED before the files.files row is
#: written -- they are transport state, not file metadata.
SYNC_SESSION_KEYS = (
    "_sync_declared_sha256",
    "_sync_expected_checksum",
    "_sync_device_id",
    "_sync_client_modified_at",
    # The file's row-access words, carried on the session until the file row is written
    # (files.uploads_inflight is Private and carries neither word as a column).
    "_row_access_published_to_web",
    "_row_access_shown_to",
)

#: Chunk size for the streamed re-hash fallback (§5.2 S11). Streams from S3;
#: never buffers the whole object.
_REHASH_CHUNK_BYTES = 8 * 1024 * 1024

if TYPE_CHECKING:
    from ..sync_engine import SyncEngine

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Tunables. Hosts override at construction time.
# ---------------------------------------------------------------------------

#: The transport ceiling when a host sets none. It is NOT a product limit and
#: must never be read as one: a person's Google Takeout, Slack export or video
#: library is routinely larger than this, and the real gate on what someone may
#: store is their organization's quota, checked per-request by the host's
#: ``quota_checker``. A host that accepts large uploads sets
#: ``CloudSyncConfig.tus_max_size_bytes`` to its own ceiling and the manager
#: enforces that instead. (Raised from 5 GB, which silently refused every
#: multi-GB data export with a message that named a number and no remedy.)
DEFAULT_MAX_SIZE = 64 * 1024 * 1024 * 1024  # 64 GB
DEFAULT_MIN_PART_BYTES = 5 * 1024 * 1024  # S3 multipart minimum (5 MiB)
DEFAULT_MAX_PATCH_BYTES = 256 * 1024 * 1024  # 256 MiB — memory ceiling per PATCH

#: S3 refuses a multipart upload with more than this many parts, so the smallest
#: chunk a client may use is ``upload_length / S3_MAX_PARTS``. A client sending
#: 5 MiB chunks therefore tops out at 50 GB however high the ceiling above is
#: set; ``advise_part_bytes`` turns that into a sentence a client can act on.
S3_MAX_PARTS = 10_000
TUS_OPERATION_LEASE = timedelta(hours=1)
TUS_SESSION_TTL = timedelta(days=7)
TUS_READY_LEASE = timedelta(minutes=5)


# ---------------------------------------------------------------------------
# Result + row dataclasses. Typed so callers don't pass dicts around.
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class TUSCreateResult:
    upload_id: str
    file_id: str
    upload_offset: int  # always 0 for fresh; non-zero for idempotency replay
    upload_length: int
    is_replay: bool = False  # True when an idempotency-key matched an existing row


@dataclass(frozen=True)
class TUSSessionRow:
    upload_id: str
    file_id: str
    owner_id: str
    file_path: str
    bucket: str
    key: str
    multipart_upload_id: str
    upload_length: int
    upload_offset: int
    published_to_web: bool
    shown_to: str | None
    mime_type: str | None
    file_name: str
    metadata: dict[str, Any] = field(default_factory=dict)
    parts: list[dict[str, Any]] = field(default_factory=list)
    status: str = "in_progress"


@dataclass(frozen=True)
class TUSAppendResult:
    new_offset: int
    is_final: bool


@dataclass(frozen=True)
class TUSFinalizeResult:
    file_id: str
    file_path: str
    size_bytes: int
    checksum: str | None
    storage_uri: str
    is_new: bool = True


# ---------------------------------------------------------------------------
# Typed errors. The router maps these to HTTP status codes.
# ---------------------------------------------------------------------------


class TUSError(Exception):
    """Base class for the TUS state-machine errors."""


class DeclaredChecksumMismatch(TUSError):
    """The bytes that arrived are not the bytes the client said it was sending.

    HTTP 422. The session is failed, the S3 object purged, and NO files.files row
    is created: a corrupt transfer must never become a file.
    """


class DeclaredChecksumUnverifiable(TUSError):
    """A checksum was declared and the server could not verify it. HTTP 422.

    S12: declaring a checksum IS the client asking for verification, so landing
    the row with ``checksum`` NULL would silently give it the opposite of what it
    asked for -- and NULL rows are excluded from the dedup index entirely.
    Uploads that declare nothing keep today's behavior exactly.
    """


class UploadNotFound(TUSError):
    """``upload_id`` doesn't match an in-progress inflight row."""


class UploadCompleted(TUSError):
    """Operation attempted on an upload that is already completed/aborted."""


class OffsetMismatch(TUSError):
    """Client's Upload-Offset disagrees with the server's tracked offset."""

    def __init__(self, server_offset: int, client_offset: int) -> None:
        self.server_offset = server_offset
        self.client_offset = client_offset
        super().__init__(f"Server has {server_offset}; client sent {client_offset}")


class PartTooSmall(TUSError):
    """A non-final PATCH was below the S3 multipart minimum part size."""


class ExceedsLength(TUSError):
    """Append would push the offset past the declared Upload-Length."""


class PatchTooLarge(TUSError):
    """Single PATCH exceeded the configured per-chunk memory ceiling."""


class S3NotConfigured(TUSError):
    """The S3 backend is not wired — TUS requires multipart upload."""


class S3Failure(TUSError):
    """An S3 multipart operation failed; ``cause`` carries the boto exception."""

    def __init__(self, op: str, cause: Exception) -> None:
        self.op = op
        self.cause = cause
        super().__init__(f"S3 {op} failed: {cause!r}")


class CleanupPending(TUSError):
    """Storage cleanup is durable but not yet complete; retry is required."""


class IdempotencyKeyReuse(TUSError):
    """The key names a live upload session for a DIFFERENT path or length."""


class UploadBusy(TUSError):
    """Another append/finalize/abort operation owns the upload lease."""


class UploadIncomplete(TUSError):
    """Finalize was requested before every declared byte was committed."""


# ---------------------------------------------------------------------------
# Manager.
# ---------------------------------------------------------------------------


def _row_to_session(row: dict[str, Any]) -> TUSSessionRow:
    return TUSSessionRow(
        upload_id=row["id"],
        file_id=row["file_id"],
        owner_id=row["owner_id"],
        file_path=row["file_path"],
        bucket=row["bucket"],
        key=row["key"],
        multipart_upload_id=row["multipart_upload_id"],
        upload_length=int(row["upload_length"]),
        upload_offset=int(row["upload_offset"]),
        published_to_web=bool((row.get("metadata") or {}).get("_row_access_published_to_web")),
        shown_to=(row.get("metadata") or {}).get("_row_access_shown_to", "only_me"),
        mime_type=row.get("mime_type"),
        file_name=row.get("file_name") or "",
        metadata=dict(row.get("metadata") or {}),
        parts=list(row.get("parts") or []),
        status=row.get("status") or "in_progress",
    )


def upload_id_hint(upload_length: int) -> str:
    """A short, non-identifying label for a log line about a pending upload."""
    return f"upload of {upload_length / 1e9:.1f} GB"


class TUSSessionManager:
    """Portable TUS state machine.

    Construct via :attr:`SyncEngine.tus` or directly when wiring a custom
    upload pipeline. The manager owns all S3 multipart ops + every
    ``files.uploads_inflight`` write; callers handle the TUS protocol
    (headers, status codes), auth, and quota policy.
    """

    def __init__(
        self,
        engine: SyncEngine,
        *,
        max_size: int = DEFAULT_MAX_SIZE,
        min_part_bytes: int = DEFAULT_MIN_PART_BYTES,
        max_patch_bytes: int = DEFAULT_MAX_PATCH_BYTES,
    ) -> None:
        self._engine = engine
        self.max_size = max_size
        self.min_part_bytes = min_part_bytes
        self.max_patch_bytes = max_patch_bytes

    def advise_part_bytes(self, upload_length: int) -> int:
        """The smallest chunk size that keeps this file under S3's part limit.

        A fixed 5 MiB chunk caps a multipart upload at 50 GB, and the failure
        arrives ten thousand chunks into a multi-hour upload — the worst moment
        possible. This turns it into a number the client can be told up front.
        """
        if upload_length <= 0:
            return self.min_part_bytes
        needed = -(-upload_length // S3_MAX_PARTS)  # ceil
        if needed <= self.min_part_bytes:
            return self.min_part_bytes
        # Round up to the next whole MiB so a client can use a round number.
        mib = 1024 * 1024
        return -(-needed // mib) * mib

    # ------------------------------------------------------------------
    # Create
    # ------------------------------------------------------------------

    async def _get_idempotency_candidate_async(
        self,
        *,
        owner_id: str,
        idempotency_key: str,
    ) -> dict[str, Any] | None:
        mf, _ = _models()
        candidates = _vals(
            await mf.UploadsInflight.filter(
                owner_id=owner_id,
                idempotency_key=idempotency_key,
                status__in=[
                    "in_progress",
                    "uploading",
                    "ready",
                    "finalizing",
                    "aborting",
                ],
            )
            .limit(1)
            .values(
                "id",
                "file_id",
                "file_path",
                "upload_offset",
                "upload_length",
                "status",
            )
        )
        return candidates[0] if candidates else None

    async def create_async(
        self,
        *,
        owner_id: str,
        file_path: str,
        upload_length: int,
        mime_type: str | None = None,
        published_to_web: bool = False,
        shown_to: str | None = "only_me",
        metadata: dict[str, Any] | None = None,
        idempotency_key: str | None = None,
        declared_sha256: str | None = None,
        expected_checksum: str | None = None,
        origin_device_id: str | None = None,
        client_modified_at: datetime | None = None,
    ) -> TUSCreateResult:
        if upload_length <= 0:
            raise ExceedsLength(
                "An upload must declare how many bytes it will send, and the number must "
                "be greater than zero. Send Upload-Length with the file's real size."
            )
        if upload_length > self.max_size:
            raise ExceedsLength(
                f"This file is {upload_length / 1e9:.1f} GB and this server accepts "
                f"single uploads up to {self.max_size / 1e9:.1f} GB. Split the export into "
                "smaller archives, or ask an administrator to raise this server's upload "
                "ceiling — your storage quota is checked separately and is not what "
                "refused this."
            )
        advised = self.advise_part_bytes(upload_length)
        if advised > self.min_part_bytes:
            logger.info(
                "tus.create: %s needs >=%sB chunks to stay under S3's %s-part limit",
                upload_id_hint(upload_length),
                advised,
                S3_MAX_PARTS,
            )

        mf, _ = _models()

        # Idempotency replay: an in-progress row with the same key wins.
        if idempotency_key:
            try:
                existing = await self._get_idempotency_candidate_async(
                    owner_id=owner_id,
                    idempotency_key=idempotency_key,
                )
            except Exception:
                existing = None
            if existing and (
                existing.get("file_path") not in (None, file_path)
                or int(existing.get("upload_length") or 0) != int(upload_length)
            ):
                # Answering with the other session would hand this caller the
                # OTHER file's id for a path it never wrote (walker, 2026-10-21).
                raise IdempotencyKeyReuse(
                    f"X-Idempotency-Key {idempotency_key!r} already names an upload of "
                    f"{existing.get('file_path')!r} ({existing.get('upload_length')} bytes); "
                    f"this request is {file_path!r} ({upload_length} bytes). Use a key "
                    "that is unique per (device, path, content)."
                )
            if existing:
                if existing.get("status") == "aborting":
                    raise UploadBusy("The prior idempotent upload is still being cleaned up")
                return TUSCreateResult(
                    upload_id=existing["id"],
                    file_id=existing["file_id"],
                    upload_offset=int(existing["upload_offset"]),
                    upload_length=int(existing["upload_length"]),
                    is_replay=True,
                )

        # Resolve bucket. Public assets land in the CDN-fronted public bucket.
        if not self._engine.router.is_configured("s3"):
            raise S3NotConfigured("S3 backend is not configured")
        backend = self._engine.router.s3

        file_id = str(uuid.uuid4())
        bucket = self._engine.config.resolve_s3_bucket()
        if published_to_web:
            # 🚨 public_bucket_or_raise, NEVER `or bucket` — see
            # cdn.public_bucket_or_raise. A resumable upload can run for
            # hours; discovering at the END that the bytes went somewhere
            # unreadable is the worst possible time to find out.
            from ..cdn import public_bucket_or_raise

            bucket = public_bucket_or_raise("tus.create")

        # Canonical key — owner-scoped + file-id. No rekey backfill needed.
        key = f"{owner_id}/{file_id}"

        s3_client = backend._get_client()
        # Phase 1.5 — open the multipart with FULL_OBJECT SHA-256 so
        # complete_multipart_upload returns the real SHA-256 of the
        # original bytes (not the composite per-part hash). That's the
        # value we need to drive dedup; the composite hash is chunk-shape
        # dependent and would dedup nothing.
        mpu_kw: dict[str, Any] = {
            "Bucket": bucket,
            "Key": key,
            "ChecksumAlgorithm": "SHA256",
            "ChecksumType": "FULL_OBJECT",
        }
        if mime_type:
            mpu_kw["ContentType"] = mime_type
        try:
            mpu = await asyncio.to_thread(s3_client.create_multipart_upload, **mpu_kw)
        except Exception as e:
            # Two compatibility failures need the same safe fallback:
            # older boto3 rejects ChecksumType locally with TypeError, while
            # S3 currently accepts the wire shape but rejects FULL_OBJECT +
            # SHA256 with InvalidRequest. In either case, create the upload
            # without provider checksum support. Finalize then leaves the
            # checksum NULL and skips dedup rather than storing a composite
            # checksum as if it identified the full object.
            error = getattr(e, "response", {}).get("Error", {})
            unsupported_full_object_sha256 = (
                error.get("Code") == "InvalidRequest"
                and "FULL_OBJECT checksum type cannot be used"
                in str(error.get("Message") or e)
            )
            if not isinstance(e, TypeError) and not unsupported_full_object_sha256:
                raise S3Failure("create_multipart_upload", e)
            mpu_kw.pop("ChecksumType", None)
            mpu_kw.pop("ChecksumAlgorithm", None)
            try:
                mpu = await asyncio.to_thread(s3_client.create_multipart_upload, **mpu_kw)
            except Exception as e:
                raise S3Failure("create_multipart_upload", e)

        upload_id = str(uuid.uuid4())
        # Best-effort derive a filename from the path tail.
        file_name = (file_path.rsplit("/", 1)[-1]) or file_id
        # Strip the two header-supplied keys we promote to first-class columns.
        clean_metadata = {
            k: v for k, v in (metadata or {}).items() if k not in ("filename", "filepath")
        }
        # Server-stamped transport state, carried to finalize and stripped there.
        if declared_sha256:
            clean_metadata["_sync_declared_sha256"] = declared_sha256
        if expected_checksum:
            clean_metadata["_sync_expected_checksum"] = expected_checksum
        if origin_device_id:
            clean_metadata["_sync_device_id"] = origin_device_id
        if client_modified_at is not None:
            clean_metadata["_sync_client_modified_at"] = client_modified_at.isoformat()
        row: dict[str, Any] = {
            "id": upload_id,
            "owner_id": owner_id,
            "file_id": file_id,
            "file_path": file_path,
            "bucket": bucket,
            "key": key,
            "multipart_upload_id": mpu["UploadId"],
            "upload_length": upload_length,
            "upload_offset": 0,
            "mime_type": mime_type,
            "file_name": file_name,
            "metadata": {
                **clean_metadata,
                "_row_access_published_to_web": bool(published_to_web),
                "_row_access_shown_to": shown_to,
            },
            "parts": [],
            "status": "in_progress",
        }
        if idempotency_key:
            row["idempotency_key"] = idempotency_key

        create_cancelled = False
        create_exc: Exception | None = None
        create_task = asyncio.create_task(mf.UploadsInflight.create(**row))
        try:
            await asyncio.shield(create_task)
        except asyncio.CancelledError:
            # A canceled ORM await does not prove the INSERT rolled back.
            # Observe the real task result before aborting its MPU.
            create_cancelled = True
            try:
                await create_task
            except Exception as exc:
                create_exc = exc
        except Exception as exc:
            create_exc = exc

        if create_exc is not None:
            # A DB response can fail after COMMIT. Reconcile this exact
            # generated row before touching its MPU.
            try:
                committed = _row(
                    await mf.UploadsInflight.filter(
                        id=upload_id,
                        owner_id=owner_id,
                    ).first()
                )
            except Exception as reconcile_exc:
                raise S3Failure(
                    "inflight_insert_reconcile",
                    reconcile_exc,
                ) from create_exc
            if committed is not None:
                if create_cancelled:
                    raise asyncio.CancelledError
                return TUSCreateResult(
                    upload_id=upload_id,
                    file_id=file_id,
                    upload_offset=int(committed.get("upload_offset") or 0),
                    upload_length=int(committed.get("upload_length") or upload_length),
                    is_replay=False,
                )

            # Exact row absence is confirmed, so this MPU is exclusively a
            # loser/orphan and is safe to abort.
            try:
                await asyncio.to_thread(
                    s3_client.abort_multipart_upload,
                    Bucket=bucket,
                    Key=key,
                    UploadId=mpu["UploadId"],
                )
            except Exception as cleanup_exc:
                raise S3Failure(
                    "inflight_insert_abort",
                    cleanup_exc,
                ) from create_exc
            if idempotency_key:
                try:
                    winner = await self._get_idempotency_candidate_async(
                        owner_id=owner_id,
                        idempotency_key=idempotency_key,
                    )
                except Exception:
                    winner = None
                if winner is not None:
                    if winner.get("status") == "aborting":
                        raise UploadBusy(
                            "The prior idempotent upload is still being cleaned up"
                        ) from create_exc
                    if create_cancelled:
                        raise asyncio.CancelledError
                    return TUSCreateResult(
                        upload_id=winner["id"],
                        file_id=winner["file_id"],
                        upload_offset=int(winner["upload_offset"]),
                        upload_length=int(winner["upload_length"]),
                        is_replay=True,
                    )
            if create_cancelled:
                raise asyncio.CancelledError
            raise S3Failure("inflight_insert", create_exc)

        if create_cancelled:
            raise asyncio.CancelledError
        return TUSCreateResult(
            upload_id=upload_id,
            file_id=file_id,
            upload_offset=0,
            upload_length=upload_length,
            is_replay=False,
        )

    # ------------------------------------------------------------------
    # Get
    # ------------------------------------------------------------------

    async def get_async(
        self,
        *,
        upload_id: str,
        owner_id: str,
    ) -> TUSSessionRow | None:
        mf, _ = _models()
        try:
            row = _row(await mf.UploadsInflight.filter(id=upload_id, owner_id=owner_id).first())
        except Exception:
            return None
        if not row:
            return None
        return _row_to_session(row)

    # ------------------------------------------------------------------
    # Append
    # ------------------------------------------------------------------

    async def append_async(
        self,
        *,
        upload_id: str,
        owner_id: str,
        body: bytes | BinaryIO,
        client_offset: int,
        body_length: int | None = None,
    ) -> TUSAppendResult:
        """Append one chunk. One PATCH, one S3 part.

        ``body`` may be raw bytes OR an open, seekable binary handle positioned
        at 0. The handle form exists so an HTTP caller never has to hold a whole
        chunk in memory: the router spools the request body to a temp file in
        small blocks and hands the file over, so peak RSS is the block size
        rather than ``max_patch_bytes``. boto3 streams a file-like ``Body``
        straight to S3.

        ``body_length`` is REQUIRED with a handle and must be the real byte
        count. A chunk whose declared length disagrees with what was actually
        read is refused before it gets here — a truncated part stored as if it
        were whole is the worst outcome this transport has.
        """
        if isinstance(body, bytes | bytearray):
            chunk_bytes = len(body)
        else:
            if body_length is None:
                raise ValueError(
                    "append_async was given a stream with no body_length. The byte "
                    "count must be known before the part is sent, or a truncated "
                    "chunk would be stored as if it were whole."
                )
            chunk_bytes = body_length

        session = await self.get_async(upload_id=upload_id, owner_id=owner_id)
        if not session:
            raise UploadNotFound(f"Upload {upload_id!r} not found for owner")
        if session.status != "in_progress":
            raise UploadCompleted(f"Upload {upload_id!r} status={session.status!r}")

        if chunk_bytes > self.max_patch_bytes:
            raise PatchTooLarge(
                f"This chunk is {chunk_bytes / 1e6:.0f} MB and the server accepts chunks up "
                f"to {self.max_patch_bytes / 1e6:.0f} MB, because it holds one chunk in "
                "memory while it stores it. Send the file in smaller chunks — the upload "
                "resumes from where it is, nothing is lost."
            )

        if client_offset != session.upload_offset:
            raise OffsetMismatch(session.upload_offset, client_offset)

        new_offset = session.upload_offset + chunk_bytes
        if new_offset > session.upload_length:
            raise ExceedsLength(
                f"Adding {chunk_bytes}B would exceed declared length {session.upload_length}"
            )

        is_final = new_offset == session.upload_length
        required = max(self.min_part_bytes, self.advise_part_bytes(session.upload_length))
        if not is_final and chunk_bytes < required:
            raise PartTooSmall(
                f"Every chunk except the last must be at least "
                f"{required / 1e6:.0f} MB for a file this size, and this one is "
                f"{chunk_bytes / 1e6:.1f} MB. Storage accepts at most "
                f"{S3_MAX_PARTS:,} chunks per file, so a large file needs larger chunks. "
                "Resend this chunk at the larger size — the upload resumes from where it is."
            )

        if not self._engine.router.is_configured("s3"):
            raise S3NotConfigured("S3 backend is not configured")
        s3_client = self._engine.router.s3._get_client()

        claim_task = asyncio.create_task(
            self._transition_session_status_async(
                upload_id,
                expected_status="in_progress",
                new_status="uploading",
                expires_at=datetime.now(UTC) + TUS_OPERATION_LEASE,
            )
        )
        try:
            claimed = await asyncio.shield(claim_task)
        except asyncio.CancelledError:
            claimed = await claim_task
            if claimed:
                await asyncio.shield(
                    self._transition_session_status_async(
                        upload_id,
                        expected_status="uploading",
                        new_status="in_progress",
                        expires_at=datetime.now(UTC) + TUS_SESSION_TTL,
                    )
                )
            raise
        if not claimed:
            raise UploadBusy(f"Upload {upload_id!r} is already being modified")

        # One PATCH = one S3 part.
        part_number = len(session.parts) + 1
        upload_task = asyncio.create_task(
            asyncio.to_thread(
                s3_client.upload_part,
                Bucket=session.bucket,
                Key=session.key,
                UploadId=session.multipart_upload_id,
                PartNumber=part_number,
                Body=body,
            )
        )
        try:
            part_resp = await asyncio.shield(upload_task)
        except asyncio.CancelledError:
            try:
                part_resp = await upload_task
            except BaseException:
                await asyncio.shield(
                    self._transition_session_status_async(
                        upload_id,
                        expected_status="uploading",
                        new_status="in_progress",
                        expires_at=datetime.now(UTC) + TUS_SESSION_TTL,
                    )
                )
                raise
            new_parts = list(session.parts) + [
                {"PartNumber": part_number, "ETag": part_resp["ETag"]}
            ]
            await asyncio.shield(
                self._transition_session_status_async(
                    upload_id,
                    expected_status="uploading",
                    new_status="ready" if is_final else "in_progress",
                    upload_offset=new_offset,
                    parts=new_parts,
                    expires_at=datetime.now(UTC)
                    + (TUS_READY_LEASE if is_final else TUS_SESSION_TTL),
                )
            )
            raise
        except Exception as e:
            await asyncio.shield(
                self._transition_session_status_async(
                    upload_id,
                    expected_status="uploading",
                    new_status="in_progress",
                    expires_at=datetime.now(UTC) + TUS_SESSION_TTL,
                )
            )
            raise S3Failure("upload_part", e)

        new_parts = list(session.parts) + [{"PartNumber": part_number, "ETag": part_resp["ETag"]}]
        committed = await self._transition_session_status_observed_async(
            upload_id,
            expected_status="uploading",
            new_status="ready" if is_final else "in_progress",
            upload_offset=new_offset,
            parts=new_parts,
            expires_at=datetime.now(UTC) + (TUS_READY_LEASE if is_final else TUS_SESSION_TTL),
        )
        if not committed:
            raise RuntimeError(f"Upload {upload_id!r} lost its uploading claim")
        return TUSAppendResult(new_offset=new_offset, is_final=is_final)

    # ------------------------------------------------------------------
    # Finalize
    # ------------------------------------------------------------------

    async def finalize_async(
        self,
        *,
        upload_id: str,
        owner_id: str,
        extra_metadata: dict[str, Any] | None = None,
    ) -> TUSFinalizeResult:
        """Complete the S3 multipart, insert the files.files row, mark inflight done.

        ``extra_metadata`` is merged on top of the inflight row's metadata
        (e.g. request_id, fingerprint hash). Host callers stamp request-
        scoped context this way without the manager needing to know what
        AppContext looks like.
        """
        session = await self.get_async(upload_id=upload_id, owner_id=owner_id)
        if not session:
            raise UploadNotFound(f"Upload {upload_id!r} not found for owner")
        if session.status not in ("in_progress", "ready"):
            raise UploadCompleted(f"Upload {upload_id!r} status={session.status!r}")
        if session.upload_offset != session.upload_length:
            raise UploadIncomplete(
                f"Upload {upload_id!r} has {session.upload_offset} of {session.upload_length} bytes"
            )

        if not self._engine.router.is_configured("s3"):
            raise S3NotConfigured("S3 backend is not configured")
        s3_client = self._engine.router.s3._get_client()

        claim_task = asyncio.create_task(
            self._transition_session_status_async(
                upload_id,
                expected_status=session.status,
                new_status="finalizing",
                expires_at=datetime.now(UTC) + TUS_OPERATION_LEASE,
            )
        )
        try:
            claimed = await asyncio.shield(claim_task)
        except asyncio.CancelledError:
            claimed = await claim_task
            if claimed:
                await asyncio.shield(
                    self._abort_session_async(
                        session,
                        expected_status="finalizing",
                    )
                )
            raise
        if not claimed:
            raise UploadCompleted(f"Upload {upload_id!r} is already claimed")

        merged_metadata = dict(session.metadata)
        if extra_metadata:
            for k, v in extra_metadata.items():
                merged_metadata.setdefault(k, v)

        # Validate placement before completing the multipart upload. A
        # caller-supplied organization is context, never authority, and a
        # rejected placement must not assemble an orphan object first.
        try:
            requested_org_id = self._engine._metadata_organization_id(merged_metadata)
            org_id_for_dedup = await self._engine._resolve_write_organization_id_async(
                owner_id,
                requested_org_id,
            )
            merged_metadata["organization_id"] = org_id_for_dedup
            lineage = resolve_file_lineage(
                parent_file_id=None,
                derivation_kind=None,
                metadata=merged_metadata,
            )
            parent_file_id = lineage.parent_file_id
            derivation_kind = (
                lineage.derivation_kind.value if lineage.derivation_kind is not None else None
            )
            duplicate_of_file_id = merged_metadata.get("duplicate_of_file_id")
            if duplicate_of_file_id is not None:
                duplicate_of_file_id = str(duplicate_of_file_id)
            for referenced_file_id in {
                file_id for file_id in (parent_file_id, duplicate_of_file_id) if file_id is not None
            }:
                await self._engine.permissions.require_async(
                    "file",
                    referenced_file_id,
                    "read",
                    owner_id,
                )
        except BaseException:
            # Organization and lineage metadata are immutable for this TUS
            # session. A rejection can never succeed on retry, so terminate
            # the multipart and state row instead of leaking both indefinitely.
            await asyncio.shield(self._abort_session_async(session, expected_status="finalizing"))
            raise

        completion_task = asyncio.create_task(
            asyncio.to_thread(
                s3_client.complete_multipart_upload,
                Bucket=session.bucket,
                Key=session.key,
                UploadId=session.multipart_upload_id,
                MultipartUpload={"Parts": session.parts},
            )
        )
        try:
            # Shield the worker because canceling asyncio.to_thread does not
            # stop the underlying boto call. We must observe its real outcome
            # before deciding whether a completed object needs compensation.
            complete_resp = await asyncio.shield(completion_task)
        except asyncio.CancelledError:
            completion_confirmed = False
            try:
                await completion_task
                completion_confirmed = True
            except BaseException:
                pass
            if completion_confirmed:
                await asyncio.shield(self._fail_completed_session_async(session))
            else:
                await asyncio.shield(
                    self._reconcile_ambiguous_completion_async(
                        session,
                        expected_status="finalizing",
                    )
                )
            raise
        except Exception as e:
            await asyncio.shield(
                self._reconcile_ambiguous_completion_async(
                    session,
                    expected_status="finalizing",
                )
            )
            raise S3Failure("complete_multipart_upload", e)

        # Phase 1.5 — full-object SHA-256 from S3, captured server-side.
        # create_async opened the multipart with
        # ``ChecksumAlgorithm='SHA256', ChecksumType='FULL_OBJECT'`` so the
        # complete response carries the real SHA-256 of the original bytes
        # (base64-encoded). Decode to the 64-char hex form the rest of the
        # dedup system uses. If S3 didn't return one (older bucket config
        # that refused FULL_OBJECT — see the TypeError fallback in
        # create_async), checksum stays NULL and this row is excluded from
        # the dedup canonical index, same as Phase 1.
        checksum: str | None = None
        checksum_b64 = (
            complete_resp.get("ChecksumSHA256") if isinstance(complete_resp, dict) else None
        )
        if checksum_b64:
            try:
                checksum = base64.b64decode(checksum_b64).hex()
            except Exception:
                logger.warning(
                    "tus.finalize: invalid ChecksumSHA256 from S3 (%r); "
                    "row will land with checksum NULL",
                    checksum_b64,
                )
                checksum = None

        # Defensive HEAD — authoritative size after S3 confirms.
        head_task = asyncio.create_task(
            asyncio.to_thread(
                s3_client.head_object,
                Bucket=session.bucket,
                Key=session.key,
            )
        )
        try:
            head = await asyncio.shield(head_task)
            actual_size = int(head.get("ContentLength") or session.upload_offset)
        except asyncio.CancelledError:
            # Completion already succeeded. Finish observing HEAD, then remove
            # the unreferenced object before propagating cancellation.
            try:
                await head_task
            except BaseException:
                pass
            await asyncio.shield(self._fail_completed_session_async(session))
            raise
        except Exception:
            actual_size = session.upload_offset
        if actual_size != session.upload_length:
            await asyncio.shield(self._fail_completed_session_async(session))
            raise S3Failure(
                "completed_size_mismatch",
                ValueError(
                    f"S3 object size {actual_size} does not match declared "
                    f"upload length {session.upload_length}"
                ),
            )

        # ---- §5: the client-declared SHA-256 -------------------------------
        # The very uploads a sync client uses for large files are the ones most
        # likely to arrive unverifiable, because S3 only returns a FULL_OBJECT
        # checksum on buckets that accept the FULL_OBJECT multipart option. A
        # composite (`...-N`) value is a hash of part hashes and does NOT
        # identify the bytes, so it is never accepted as one -- the fallback is a
        # streamed re-hash of the assembled object.
        declared = session.metadata.get("_sync_declared_sha256")
        if declared:
            declared = str(declared).lower()
            if checksum is None:
                checksum = await self._streamed_sha256_async(session)
            if checksum is None:
                await asyncio.shield(self._fail_completed_session_async(session))
                raise DeclaredChecksumUnverifiable(
                    f"Upload {session.upload_id!r} declared sha256 {declared} but neither "
                    "S3's FULL_OBJECT checksum nor a streamed re-hash could produce a value "
                    "to verify it against. The upload is refused rather than landed "
                    "unverifiable: a declared checksum IS a request for verification, and a "
                    "NULL checksum is also excluded from the dedup index."
                )
            if checksum != declared:
                await asyncio.shield(self._fail_completed_session_async(session))
                raise DeclaredChecksumMismatch(
                    f"Upload {session.upload_id!r} declared sha256 {declared} but the "
                    f"assembled object hashes to {checksum}. The transfer was corrupted; "
                    "the object has been purged and no file row was created."
                )

        # ---- §3: the precondition, RE-EVALUATED at finalize ------------------
        # A resumable upload can run for minutes; the state the client checked at
        # creation is not the state it is about to overwrite.
        expected = session.metadata.get("_sync_expected_checksum")
        if expected:
            current_row = await self._engine.db.get_file_by_path_async(
                owner_id, session.file_path
            )
            try:
                check_expected_checksum(current_row, str(expected))
            except PreconditionFailed:
                await asyncio.shield(self._fail_completed_session_async(session))
                raise

        backend_name = self._engine.config.storage_backend
        storage_uri = f"{backend_name}://{session.bucket}/{session.key}"
        # Canonical key == native key for TUS uploads — no rekey backfill.

        file_path = session.file_path

        # ---- an upload over a LIVE file is a new version of THAT file -------
        # Finalize used to INSERT a brand-new row at ``file_path`` every time.
        # Over an existing file the live ``(created_by, file_path)`` key refused
        # it and the client got ``502 s3_cld_files_insert_failed`` -- every TUS
        # overwrite failed, including the sync engine's own guarded overwrite
        # (expectedchecksum = the current sha256). It runs before the dedup
        # gate: an overwrite's bytes matching some OTHER file must not turn
        # the overwrite into "here is that other file".
        if parent_file_id is None and duplicate_of_file_id is None:
            try:
                current_live = await self._engine.db.get_file_by_path_async(owner_id, file_path)
            except BaseException:
                await asyncio.shield(self._fail_completed_session_async(session))
                raise
            if current_live is not None:
                return await self._finalize_as_new_version_async(
                    session=session,
                    upload_id=upload_id,
                    owner_id=owner_id,
                    current=current_live,
                    checksum=checksum,
                    actual_size=actual_size,
                    storage_uri=f"{self._engine.config.storage_backend}://{session.bucket}/{session.key}",
                    merged_metadata=merged_metadata,
                )

        if duplicate_of_file_id is not None:
            try:
                await self._engine._validate_duplicate_target_async(
                    user_id=owner_id,
                    organization_id=org_id_for_dedup,
                    duplicate_of_file_id=duplicate_of_file_id,
                    checksum=checksum,
                )
            except BaseException:
                await asyncio.shield(self._fail_completed_session_async(session))
                raise

        # Phase 1.5 — content-hash dedup gate. Mirrors the gate inside
        # ``SyncEngine.managed_write_async``: brand-new ROOT inserts consult
        # the canonical row first; a scope-matching hit short-circuits
        # (delete the just-assembled S3 object, point the inflight row at
        # the canonical file_id, no files.files INSERT). Derivative writes
        # (an authorized parent or canonical duplicate) bypass the lookup
        # so variants of distinct parents don't alias.
        is_derivative_write = parent_file_id is not None or duplicate_of_file_id is not None
        if checksum and not is_derivative_write:
            from matrx_files.dedup import lookup_existing_async

            try:
                dedup_lookup = await lookup_existing_async(
                    self._engine.db,
                    checksum=checksum,
                    owner_id=owner_id,
                    organization_id=org_id_for_dedup,
                )
            except BaseException:
                await asyncio.shield(self._fail_completed_session_async(session))
                raise
            if dedup_lookup.has_duplicate and dedup_lookup.existing is not None:
                if dedup_lookup.existing.get("file_path") == file_path:
                    return await self._finalize_dedup_hit_async(
                        session=session,
                        upload_id=upload_id,
                        existing_row=dedup_lookup.existing,
                        checksum=checksum,
                        actual_size=actual_size,
                    )
                # Same bytes, ANOTHER path: a TUS upload always declares its
                # placement, so it gets a row of its own at that path, linked
                # to the canonical content (test_placement_survives_dedup.py's
                # doctrine). Short-circuiting to the canonical row answered
                # the caller with another file's id and recorded the path
                # nowhere (walker, 2026-10-21).
                duplicate_of_file_id = str(dedup_lookup.existing["id"])
                is_derivative_write = True

        # Resolve parent folder chain (use the existing RPC). Only matters
        # for the INSERT path — dedup hits skip this above.
        mf, _ = _models()
        try:
            parent_id = await self._engine._ensure_folder_async(
                file_path,
                owner_id,
                org_id_for_dedup,
            )
        except BaseException:
            await asyncio.shield(self._fail_completed_session_async(session))
            raise

        new_row = {
            "id": session.file_id,
            # files.files owner column is the canonical `created_by` (the
            # 2026 DB canonicalization renamed owner_id). This is a DIRECT
            # files insert that bypasses DatabaseClient.upsert_file's
            # owner_id->created_by shim, so write the canonical column here.
            "created_by": owner_id,
            "file_path": file_path,
            "storage_uri": storage_uri,
            # canonical_storage_uri not written — consolidated into storage_uri
            # by migration 007 (storage_uri is already the canonical file_id URI).
            "file_name": session.file_name,
            "mime_type": session.mime_type,
            "size_bytes": actual_size,
            "checksum": checksum,
            **RowAccess(published_to_web=session.published_to_web, shown_to=session.shown_to).columns(owner_id),
            "parent_folder_id": parent_id,
            "organization_id": org_id_for_dedup,
            "metadata": {
                k: v for k, v in merged_metadata.items() if k not in SYNC_SESSION_KEYS
            },
            # Device provenance (§2.2), validated at create time before it was
            # ever stored on the session.
            "origin_device_id": merged_metadata.get("_sync_device_id"),
            "client_modified_at": (
                datetime.fromisoformat(str(merged_metadata["_sync_client_modified_at"]))
                if merged_metadata.get("_sync_client_modified_at")
                else None
            ),
        }
        # The filterable copy of this row's produced-artifact identity. This is a
        # DIRECT files insert that does not pass through SyncEngine's payload, so
        # the same derivation is applied here — a resumable upload of a coding
        # artifact must be as findable as a simple one.
        # See matrx_files/artifact_identity.py.
        # The machine-artifact marker, from the path — the same stamp SyncEngine's door applies
        # (matrx_files/user_visible.py § MACHINE-ARTIFACT).
        new_row["metadata"] = stamp_machine_artifact(file_path, new_row["metadata"])
        new_row.update(artifact_identity_columns(new_row["metadata"]))
        if parent_file_id is not None:
            new_row["parent_file_id"] = parent_file_id
        if derivation_kind is not None:
            new_row["derivation_kind"] = derivation_kind
        if merged_metadata.get("derivation_metadata") is not None:
            new_row["derivation_metadata"] = merged_metadata["derivation_metadata"]
        if duplicate_of_file_id is not None:
            new_row["duplicate_of_file_id"] = duplicate_of_file_id
        insert_cancelled = False
        insert_exc: Exception | None = None
        insert_task = asyncio.create_task(mf.Files.create(**new_row))
        try:
            await asyncio.shield(insert_task)
        except asyncio.CancelledError:
            # Do not query-and-delete while the INSERT itself may still
            # commit. Wait for its true outcome first.
            insert_cancelled = True
            try:
                await insert_task
            except Exception as exc:
                insert_exc = exc
        except Exception as exc:
            insert_exc = exc

        if insert_exc is not None:
            try:
                committed = await self._file_row_owns_session_object_async(session)
            except Exception as reconcile_exc:
                # Never compensate while COMMIT is ambiguous.
                raise S3Failure("cld_files_insert_reconcile", reconcile_exc) from insert_exc
            if committed:
                insert_exc = None

            # Race: a concurrent TUS finalize (or managed_write_async) of
            # the same content won the canonical slot between our lookup
            # and this INSERT. Recover by re-querying for the winner,
            # deleting the orphan S3 object we just assembled, and
            # returning the winner's identity. Mirrors the recovery in
            # ``SyncEngine.managed_write_async``.
            if insert_exc is not None:
                from ..sync_engine import SyncEngine

                try:
                    if (
                        not is_derivative_write
                        and checksum
                        and SyncEngine._is_dedup_unique_violation(insert_exc)
                    ):
                        from matrx_files.dedup import lookup_existing_async

                        winner_lookup = await lookup_existing_async(
                            self._engine.db,
                            checksum=checksum,
                            owner_id=owner_id,
                            organization_id=org_id_for_dedup,
                        )
                        if winner_lookup.has_duplicate and winner_lookup.existing is not None:
                            result = await self._finalize_dedup_hit_async(
                                session=session,
                                upload_id=upload_id,
                                existing_row=winner_lookup.existing,
                                checksum=checksum,
                                actual_size=actual_size,
                            )
                            if insert_cancelled:
                                raise asyncio.CancelledError
                            return result
                except BaseException:
                    await asyncio.shield(self._fail_completed_session_async(session))
                    raise
                await asyncio.shield(self._fail_completed_session_async(session))
                raise S3Failure("cld_files_insert", insert_exc)

        # Shielded inflight transition. Without the shield, a client
        # disconnect between the files.files INSERT and this UPDATE leaves
        # the inflight row 'in_progress' while a perfectly good files.files
        # row exists — the TUS cleanup loop would later abort an
        # already-completed upload. Phase 2 doctrine: cancellation cannot
        # split a two-write commit. See PHASE_1_LESSONS_LEARNED.md §1.
        completed = await self._transition_session_status_observed_async(
            upload_id,
            expected_status="finalizing",
            new_status="completed",
            upload_offset=actual_size,
        )
        if not completed:
            raise RuntimeError(f"TUS finalize lost its finalizing claim for upload {upload_id!r}")
        if insert_cancelled:
            raise asyncio.CancelledError

        # Best-effort thumbnail. The processor handles "not a thumbnailable
        # mime" / "no s3" / etc. internally — we don't propagate its errors.
        try:
            from ..processing import generate_thumbnail_for_file

            supervised_task(
                generate_thumbnail_for_file(self._engine.fm, session.file_id),
                kind="file_thumbnail_generation_failed",
                name=f"thumbnail:{session.file_id}",
                context={"file_id": session.file_id, "upload_id": upload_id},
            )
        except Exception:
            pass

        return TUSFinalizeResult(
            file_id=session.file_id,
            file_path=file_path,
            size_bytes=actual_size,
            checksum=checksum,
            storage_uri=storage_uri,
        )

    async def _finalize_as_new_version_async(
        self,
        *,
        session: TUSSessionRow,
        upload_id: str,
        owner_id: str,
        current: dict[str, Any],
        checksum: str | None,
        actual_size: int,
        storage_uri: str,
        merged_metadata: dict[str, Any],
    ) -> TUSFinalizeResult:
        """Land a completed TUS object as version N+1 of the live row at its path.

        The same outcome ``SyncEngine.managed_write_async`` gives a buffered
        overwrite -- same row id, ``current_version`` + 1, a ``file_versions``
        snapshot per version -- without pulling the bytes into memory:

        1. write permission on the row, and never over a system-immutable file;
        2. server-side copy of the new object to its version snapshot key (the
           snapshot must not share the live object, because a later buffered
           write overwrites the live object IN PLACE);
        3. the previous version's snapshot row, when the row never had one (a
           row born from TUS has none) -- it points at the previous live
           object, which stops being live in step 4 and is never overwritten;
        4. compare-and-set the row onto the new object at ``current_version``;
           a lost race is a 412 and the new object is purged;
        5. the new version's snapshot row.

        Anything failing before step 4 purges the new object and leaves the
        row untouched. After step 4 the row references the object, so it is
        never purged.
        """
        file_id = str(current["id"])
        old_version = int(current.get("current_version") or 1)
        new_version = old_version + 1
        file_name = session.file_name or current.get("file_name") or file_id
        version_uri = self._engine.versions._version_uri(file_id, new_version, file_name)
        mf, _ = _models()
        try:
            if (current.get("metadata") or {}).get("system_immutable"):
                raise PermissionError(
                    f"system-managed immutable file cannot be overwritten: {file_id}"
                )
            await self._engine.permissions.require_async("file", file_id, "write", owner_id)
            if not current.get("checksum") or current.get("checksum") != checksum:
                snapshot_bucket, _, snapshot_key = version_uri.split("://", 1)[1].partition("/")
                s3_client = self._engine.router.s3._get_client()
                await asyncio.to_thread(
                    s3_client.copy_object,
                    CopySource={"Bucket": session.bucket, "Key": session.key},
                    Bucket=snapshot_bucket,
                    Key=snapshot_key,
                )
            if await self._engine.db.get_version_async(file_id, old_version) is None:
                await self._engine.db.create_version_async(
                    {
                        "file_id": file_id,
                        "version_number": old_version,
                        "storage_uri": current.get("storage_uri"),
                        "size_bytes": current.get("size_bytes"),
                        "checksum": current.get("checksum"),
                        "created_by": owner_id,
                        "organization_id": current.get("organization_id"),
                    }
                )
            row_metadata = {
                k: v for k, v in merged_metadata.items() if k not in SYNC_SESSION_KEYS
            }
            # The row keeps its own organization: a write never moves a file
            # between tenants (managed_write converges the same way).
            row_metadata["organization_id"] = current.get("organization_id")
            row_metadata = stamp_machine_artifact(session.file_path, row_metadata)
            result = await mf.Files.update_where(
                {"id": file_id, "current_version": old_version, "deleted_at__isnull": True},
                storage_uri=storage_uri,
                size_bytes=actual_size,
                checksum=checksum,
                mime_type=session.mime_type or current.get("mime_type"),
                current_version=new_version,
                metadata=row_metadata,
                origin_device_id=merged_metadata.get("_sync_device_id"),
                client_modified_at=(
                    datetime.fromisoformat(str(merged_metadata["_sync_client_modified_at"]))
                    if merged_metadata.get("_sync_client_modified_at")
                    else None
                ),
            )
            if not getattr(result, "rows_affected", 0):
                raise PreconditionFailed(
                    {
                        "error": "precondition_failed",
                        "message": "the file changed on the server while this upload was finishing",
                        "file_id": file_id,
                        "current_version": old_version,
                    }
                )
        except BaseException:
            await asyncio.shield(self._fail_completed_session_async(session))
            raise

        # The row now references the new object: from here on nothing purges it.
        if checksum and current.get("checksum") == checksum:
            snapshot_uri = None  # identical bytes: the previous snapshot already holds them
        else:
            snapshot_uri = version_uri
        if snapshot_uri is not None:
            await self._engine.db.create_version_async(
                {
                    "file_id": file_id,
                    "version_number": new_version,
                    "storage_uri": snapshot_uri,
                    "size_bytes": actual_size,
                    "checksum": checksum,
                    "created_by": owner_id,
                    "organization_id": current.get("organization_id"),
                }
            )
        completed = await self._transition_session_status_observed_async(
            upload_id,
            expected_status="finalizing",
            new_status="completed",
            upload_offset=actual_size,
            metadata={**session.metadata, "versioned_file_id": file_id, "version": new_version},
        )
        if not completed:
            raise RuntimeError(f"TUS finalize lost its finalizing claim for upload {upload_id!r}")
        return TUSFinalizeResult(
            file_id=file_id,
            file_path=session.file_path,
            size_bytes=actual_size,
            checksum=checksum,
            storage_uri=storage_uri,
            is_new=False,
        )

    # ------------------------------------------------------------------
    # Dedup hit — shared finish path used by both the pre-INSERT lookup
    # and the post-INSERT race recovery.
    # ------------------------------------------------------------------

    async def _finalize_dedup_hit_async(
        self,
        *,
        session: TUSSessionRow,
        upload_id: str,
        existing_row: dict[str, Any],
        checksum: str,
        actual_size: int,
    ) -> TUSFinalizeResult:
        """Wrap up a TUS upload that matched an already-existing canonical row.

        The just-assembled S3 object is orphaned (it's identical to the
        canonical row's storage_uri by definition), so we delete it.
        The inflight row gets marked completed with a metadata pointer at
        the canonical file_id so the audit trail records what happened.
        No files.files INSERT — caller uses the returned canonical file_id.
        """
        if not await self._delete_completed_object_async(session):
            raise S3Failure(
                "delete_dedup_orphan",
                RuntimeError("completed dedup object cleanup will be retried"),
            )

        canonical_id = str(existing_row["id"])
        canonical_storage_uri = (
            existing_row.get("canonical_storage_uri") or existing_row.get("storage_uri") or ""
        )

        completed = await self._transition_session_status_observed_async(
            upload_id,
            expected_status="finalizing",
            new_status="completed",
            upload_offset=actual_size,
            metadata={
                **session.metadata,
                "dedup_winner_file_id": canonical_id,
                "dedup_checksum": checksum,
            },
        )
        if not completed:
            raise RuntimeError(
                f"TUS dedup finalize lost its finalizing claim for upload {upload_id!r}"
            )

        return TUSFinalizeResult(
            file_id=canonical_id,
            file_path=existing_row.get("file_path") or session.file_path,
            size_bytes=int(existing_row.get("size_bytes") or actual_size),
            checksum=checksum,
            storage_uri=canonical_storage_uri,
            is_new=False,
        )

    async def _transition_session_status_observed_async(
        self,
        upload_id: str,
        *,
        expected_status: str,
        new_status: str,
        require_expired: bool = False,
        **fields: Any,
    ) -> bool:
        """Finish a CAS even when its caller is canceled while awaiting it."""
        transition_task = asyncio.create_task(
            self._transition_session_status_async(
                upload_id,
                expected_status=expected_status,
                new_status=new_status,
                require_expired=require_expired,
                **fields,
            )
        )
        try:
            return await asyncio.shield(transition_task)
        except asyncio.CancelledError:
            await transition_task
            raise

    @staticmethod
    def _s3_error_code(exc: BaseException) -> str | None:
        response = getattr(exc, "response", None)
        if not isinstance(response, dict):
            return None
        error = response.get("Error")
        if not isinstance(error, dict):
            return None
        code = error.get("Code")
        return str(code) if code is not None else None

    async def _probe_completed_object_async(
        self,
        session: TUSSessionRow,
    ) -> tuple[str, dict[str, Any] | None]:
        """Return ``exists``, ``missing``, or ``unknown`` for the exact key."""
        if not self._engine.router.is_configured("s3"):
            return "unknown", None
        s3_client = self._engine.router.s3._get_client()
        try:
            return (
                "exists",
                await asyncio.to_thread(
                    s3_client.head_object,
                    Bucket=session.bucket,
                    Key=session.key,
                ),
            )
        except Exception as exc:
            if self._s3_error_code(exc) in {"404", "NoSuchKey", "NotFound"}:
                return "missing", None
            return "unknown", None

    async def _delete_completed_object_async(self, session: TUSSessionRow) -> bool:
        """Delete a completed object before it has a row; report success."""
        if not self._engine.router.is_configured("s3"):
            return False
        s3_client = self._engine.router.s3._get_client()
        try:
            await asyncio.to_thread(
                s3_client.delete_object,
                Bucket=session.bucket,
                Key=session.key,
            )
            return True
        except Exception:
            logger.warning(
                "tus.finalize: orphan S3 cleanup failed for %s/%s",
                session.bucket,
                session.key,
                exc_info=True,
            )
            return False

    async def _transition_session_status_async(
        self,
        upload_id: str,
        *,
        expected_status: str,
        new_status: str,
        require_expired: bool = False,
        **fields: Any,
    ) -> bool:
        """Compare-and-set one session state; terminal writers never overwrite."""
        mf, _ = _models()
        filters: dict[str, Any] = {"id": upload_id, "status": expected_status}
        if require_expired:
            filters["expires_at__lt"] = datetime.now(UTC)
        result = await mf.UploadsInflight.update_where(
            filters,
            status=new_status,
            updated_at=datetime.now(UTC),
            **fields,
        )
        return int(result.rows_affected) == 1

    async def _mark_session_aborted_async(
        self,
        upload_id: str,
        *,
        expected_status: str,
    ) -> bool:
        """Best-effort terminal transition for a session that cannot retry."""
        try:
            return await self._transition_session_status_async(
                upload_id,
                expected_status=expected_status,
                new_status="aborted",
            )
        except Exception:
            logger.warning(
                "tus.abort: failed to mark upload %s aborted",
                upload_id,
                exc_info=True,
            )
            return False

    async def _streamed_sha256_async(self, session: TUSSessionRow) -> str | None:
        """SHA-256 of the assembled object, streamed from S3 (§5.2, S11).

        Used when S3 cannot supply a FULL_OBJECT checksum. Streams in chunks --
        the whole object is never buffered -- so a 5 GB upload costs one extra
        pass, not 5 GB of memory. Returns None only when the object cannot be
        read at all; the caller turns that into a loud refusal, never a NULL
        checksum.
        """
        import hashlib

        if not self._engine.router.is_configured("s3"):
            return None
        s3_client = self._engine.router.s3._get_client()

        def _hash() -> str:
            digest = hashlib.sha256()
            body = s3_client.get_object(Bucket=session.bucket, Key=session.key)["Body"]
            try:
                while True:
                    chunk = body.read(_REHASH_CHUNK_BYTES)
                    if not chunk:
                        break
                    digest.update(chunk)
            finally:
                body.close()
            return digest.hexdigest()

        try:
            return await asyncio.to_thread(_hash)
        except Exception as e:
            logger.warning(
                "tus.finalize: streamed re-hash of %s/%s failed (%r); the declared "
                "checksum cannot be verified and the upload will be refused",
                session.bucket,
                session.key,
                e,
            )
            return None

    async def _fail_completed_session_async(
        self,
        session: TUSSessionRow,
        *,
        expected_status: str = "finalizing",
    ) -> bool:
        """Delete an unreferenced completed object, terminalizing only on success."""
        if not await self._delete_completed_object_async(session):
            # Keep in_progress so the durable cleanup sweep retries.
            return False
        return await self._mark_session_aborted_async(
            session.upload_id,
            expected_status=expected_status,
        )

    async def _reconcile_ambiguous_completion_async(
        self,
        session: TUSSessionRow,
        *,
        expected_status: str,
    ) -> None:
        """Clean either side of an ambiguous CompleteMultipartUpload outcome."""
        object_state, _ = await self._probe_completed_object_async(session)
        if object_state == "exists":
            await self._fail_completed_session_async(
                session,
                expected_status=expected_status,
            )
            return
        await self._abort_session_async(
            session,
            expected_status=expected_status,
        )

    # ------------------------------------------------------------------
    # Abort
    # ------------------------------------------------------------------

    async def _file_row_owns_session_object_async(
        self,
        session: TUSSessionRow,
    ) -> bool:
        """Backstop a crash after file INSERT but before session completion."""
        mf, _ = _models()
        record = _row(
            await mf.Files.filter(
                id=session.file_id,
            ).first()
        )
        if not record:
            return False
        storage_uri = str(record.get("canonical_storage_uri") or record.get("storage_uri") or "")
        return storage_uri.partition("://")[2] == f"{session.bucket}/{session.key}"

    async def _abort_session_async(
        self,
        session: TUSSessionRow,
        *,
        expected_status: str,
    ) -> bool:
        """Clean an MPU or reconciled completed object, then mark it aborted."""
        if not self._engine.router.is_configured("s3"):
            return False

        if await self._file_row_owns_session_object_async(session):
            return await self._transition_session_status_async(
                session.upload_id,
                expected_status=expected_status,
                new_status="completed",
                upload_offset=session.upload_length,
            )

        s3_client = self._engine.router.s3._get_client()
        cleanup_succeeded = False
        try:
            await asyncio.to_thread(
                s3_client.abort_multipart_upload,
                Bucket=session.bucket,
                Key=session.key,
                UploadId=session.multipart_upload_id,
            )
            cleanup_succeeded = True
        except Exception as abort_exc:
            # CompleteMultipartUpload can succeed server-side while the client
            # observes a timeout. If abort then fails, reconcile the exact key.
            object_state, _ = await self._probe_completed_object_async(session)
            if object_state == "exists":
                cleanup_succeeded = await self._delete_completed_object_async(session)
            elif object_state == "missing" and self._s3_error_code(abort_exc) == "NoSuchUpload":
                # A prior cleanup removed the object but lost its DB status
                # update. The durable sweep can now finish that transition.
                cleanup_succeeded = True
            if not cleanup_succeeded:
                logger.warning(
                    "tus.abort: cleanup remains pending for upload %s",
                    session.upload_id,
                    exc_info=True,
                )

        if not cleanup_succeeded:
            # Keep in_progress so tus_cleanup retries this durable row.
            return False
        return await self._mark_session_aborted_async(
            session.upload_id,
            expected_status=expected_status,
        )

    async def abort_async(self, *, upload_id: str, owner_id: str) -> None:
        """Abort the multipart + mark the row aborted. Idempotent.

        Returns silently when the upload is already completed/aborted or
        doesn't exist — the protocol layer maps "no in-progress row" to
        a 404 itself.
        """
        session = await self.get_async(upload_id=upload_id, owner_id=owner_id)
        if not session or session.status not in ("in_progress", "ready"):
            raise UploadNotFound(f"Upload {upload_id!r} not in progress")

        if not await self._transition_session_status_async(
            upload_id,
            expected_status=session.status,
            new_status="aborting",
            expires_at=datetime.now(UTC) + TUS_OPERATION_LEASE,
        ):
            raise UploadCompleted(f"Upload {upload_id!r} is already claimed")
        if not await self._abort_session_async(
            session,
            expected_status="aborting",
        ):
            raise CleanupPending(f"Upload {upload_id!r} cleanup is pending and will be retried")

    async def abort_stale_async(
        self,
        *,
        upload_id: str,
        owner_id: str,
        expected_status: str,
    ) -> None:
        """Claim and clean one row already proven expired by the sweep."""
        session = await self.get_async(upload_id=upload_id, owner_id=owner_id)
        if not session or session.status != expected_status:
            raise UploadNotFound(f"Upload {upload_id!r} changed before cleanup")
        if not await self._transition_session_status_async(
            upload_id,
            expected_status=expected_status,
            new_status="aborting",
            require_expired=True,
            expires_at=datetime.now(UTC) + TUS_OPERATION_LEASE,
        ):
            raise UploadNotFound(f"Upload {upload_id!r} changed or renewed before cleanup")
        if not await self._abort_session_async(
            session,
            expected_status="aborting",
        ):
            raise CleanupPending(f"Upload {upload_id!r} cleanup is pending and will be retried")


__all__ = [
    "TUSSessionManager",
    "TUSSessionRow",
    "TUSCreateResult",
    "TUSAppendResult",
    "TUSFinalizeResult",
    "TUSError",
    "UploadCompleted",
    "UploadNotFound",
    "OffsetMismatch",
    "PartTooSmall",
    "S3_MAX_PARTS",
    "ExceedsLength",
    "PatchTooLarge",
    "S3Failure",
    "CleanupPending",
    "UploadBusy",
    "UploadIncomplete",
    "S3NotConfigured",
    "DEFAULT_MAX_SIZE",
    "DEFAULT_MIN_PART_BYTES",
    "DEFAULT_MAX_PATCH_BYTES",
]
