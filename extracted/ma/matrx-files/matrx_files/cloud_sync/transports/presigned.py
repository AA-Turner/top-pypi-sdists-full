"""Presigned-PUT upload state machine.

Two-phase browser-direct upload:

1. ``create`` — server mints a presigned PUT URL + records the pending upload.
2. (Browser PUTs the object straight to S3.)
3. ``finalize`` — server inserts the files.files row, HEAD-verifies the size,
   runs the same post-upload orchestration as the buffered path.

State: a durable row in ``files.uploads_inflight`` (the same table TUS uses),
marked by ``multipart_upload_id = 'presigned'``. It survives restarts and is
visible to every worker/task: the live server runs 4 tasks, and the old per-process
dict made ``finalize`` 404 whenever it landed on a task that had not minted the
upload. ``_claim_pending`` is an atomic ``in_progress -> completed`` transition, so
exactly one finalize wins. The TUS sweeper skips these rows (there is no multipart
upload to abort); expired ones are closed by :meth:`PresignedManager._gc`.
"""

from __future__ import annotations

import logging
import time
import uuid
from dataclasses import dataclass, field
from datetime import UTC, datetime, timedelta
from typing import TYPE_CHECKING, Any

from matrx_utils.row_access import RowAccess

from .. import db as _db

if TYPE_CHECKING:
    from ..sync_engine import SyncEngine

logger = logging.getLogger(__name__)


# Pending-entry TTL. Re-runs in finalize and on every create.
_PENDING_TTL_SECONDS = 1800  # 30 min — matches the presigned URL window

#: ``files.uploads_inflight.multipart_upload_id`` value that marks a presigned-PUT
#: pending row (it has no S3 multipart upload). The TUS sweeper skips it.
PRESIGNED_MARKER = "presigned"


# ---------------------------------------------------------------------------
# Errors. Same pattern as TUSSessionManager — host maps to HTTP codes.
# ---------------------------------------------------------------------------


class PresignedError(Exception):
    """Base class for presigned-upload errors."""


class PresignedUnavailable(PresignedError):
    """The configured S3 backend doesn't expose ``get_presigned_put_url``."""


class UploadNotFound(PresignedError):
    """``upload_id`` doesn't match a pending entry (expired or invalid)."""


class OwnerMismatch(PresignedError):
    """The finalize caller is not the user that requested the upload."""


# ---------------------------------------------------------------------------
# Result dataclasses.
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class PresignedCreateResult:
    upload_id: str
    url: str
    headers: dict[str, str]
    expires_in: int
    file_path: str
    storage_uri: str


@dataclass(frozen=True)
class PresignedFinalizeResult:
    file_id: str
    file_path: str
    storage_uri: str
    size_bytes: int
    checksum: str | None
    version_number: int
    url: str | None
    cdn_url: str | None
    is_new: bool
    #: ``/files/finalize-upload`` answers the same ``FileUploadResponse`` as the buffered
    #: upload, which carries these two; a presigned upload mints no share link.
    share_token: str | None = None
    share_url: str | None = None


@dataclass
class _PendingEntry:
    user_id: str
    file_path: str
    storage_uri: str
    content_type: str | None
    published_to_web: bool
    shown_to: str | None
    metadata: dict[str, Any] = field(default_factory=dict)
    expected_size: int | None = None
    created_at: float = 0.0


# ---------------------------------------------------------------------------
# Manager.
# ---------------------------------------------------------------------------


class PresignedManager:
    """Presigned PUT upload coordinator.

    Construct via :attr:`SyncEngine.presigned` or directly. The in-memory
    pending-store is the default; subclass + override the two underscore
    methods for a multi-worker shared store (Redis, DB, etc).
    """

    def __init__(self, engine: "SyncEngine") -> None:
        self._engine = engine

    # ------------------------------------------------------------------
    # Pending store — durable rows in files.uploads_inflight.
    # ------------------------------------------------------------------

    async def _put_pending(self, upload_id: str, entry: _PendingEntry) -> None:
        mf, _ = _db._models()
        bucket, _, key = entry.storage_uri.split("://", 1)[1].partition("/")
        await mf.UploadsInflight.create(
            id=upload_id,
            owner_id=entry.user_id,
            file_id=upload_id,  # placeholder: the real file id exists only after finalize
            file_path=entry.file_path,
            bucket=bucket,
            key=key,
            multipart_upload_id=PRESIGNED_MARKER,
            upload_length=int(entry.expected_size or 0),
            upload_offset=0,
            mime_type=entry.content_type,
            file_name=entry.file_path.split("/")[-1],
            metadata={
                "_presigned": {
                    "storage_uri": entry.storage_uri,
                    "published_to_web": entry.published_to_web,
                    "shown_to": entry.shown_to,
                    "metadata": entry.metadata,
                }
            },
            parts=[],
            status="in_progress",
            expires_at=datetime.now(UTC) + timedelta(seconds=_PENDING_TTL_SECONDS),
        )

    async def _peek_pending(self, upload_id: str) -> _PendingEntry | None:
        """Read a live pending upload without consuming it (None if absent/expired/done)."""
        mf, _ = _db._models()
        rows = _db._vals(
            await mf.UploadsInflight.filter(
                id=upload_id, multipart_upload_id=PRESIGNED_MARKER, status="in_progress"
            )
            .limit(1)
            .values(
                "owner_id", "file_path", "mime_type", "upload_length", "metadata", "expires_at"
            )
        )
        if not rows:
            return None
        row = rows[0]
        expires_at = row["expires_at"]
        if isinstance(expires_at, str):
            expires_at = datetime.fromisoformat(expires_at.replace("Z", "+00:00"))
        if expires_at is not None and expires_at.tzinfo is None:
            expires_at = expires_at.replace(tzinfo=UTC)
        if expires_at is not None and expires_at < datetime.now(UTC):
            return None
        meta = (row["metadata"] or {}).get("_presigned") or {}
        return _PendingEntry(
            user_id=str(row["owner_id"]),
            file_path=row["file_path"],
            storage_uri=meta.get("storage_uri", ""),
            content_type=row["mime_type"],
            published_to_web=bool(meta.get("published_to_web")),
            shown_to=meta.get("shown_to"),
            metadata=dict(meta.get("metadata") or {}),
            expected_size=int(row["upload_length"] or 0) or None,
        )

    async def _claim_pending(self, upload_id: str) -> bool:
        """Atomically consume the pending upload: exactly one caller gets True."""
        mf, _ = _db._models()
        result = await mf.UploadsInflight.update_where(
            {"id": upload_id, "multipart_upload_id": PRESIGNED_MARKER, "status": "in_progress"},
            status="completed",
        )
        return bool(result.rows_affected)

    async def _take_pending(self, upload_id: str) -> _PendingEntry | None:
        """Peek + claim (no owner check). The finalize path peeks, checks the owner, then claims."""
        entry = await self._peek_pending(upload_id)
        if entry is None or not await self._claim_pending(upload_id):
            return None
        return entry

    async def _gc(self) -> None:
        """Close expired presigned rows so the watchdog never sees them as stuck."""
        mf, _ = _db._models()
        try:
            await mf.UploadsInflight.update_where(
                {
                    "multipart_upload_id": PRESIGNED_MARKER,
                    "status": "in_progress",
                    "expires_at__lt": datetime.now(UTC),
                },
                status="aborted",
            )
        except Exception:  # housekeeping only; the next create retries
            logger.warning("presigned pending gc failed", exc_info=True)

    # ------------------------------------------------------------------
    # Create
    # ------------------------------------------------------------------

    async def create(
        self,
        *,
        owner_id: str,
        file_path: str,
        content_type: str | None = None,
        published_to_web: bool = False,
        shown_to: str | None = "only_me",
        metadata: dict[str, Any] | None = None,
        expected_size_bytes: int | None = None,
        expires_in: int = 900,
    ) -> PresignedCreateResult:
        """Mint a presigned PUT URL + register a pending entry.

        Returns ``(upload_id, url, headers, expires_in, file_path, storage_uri)``.
        The browser PUTs the object to ``url`` with ``headers``; then calls
        :meth:`finalize` with ``upload_id`` to commit the files.files row.
        """
        router = self._engine.router
        if not router.is_configured("s3"):
            raise PresignedUnavailable("S3 backend is not configured")
        backend = router.s3
        if not hasattr(backend, "get_presigned_put_url"):
            raise PresignedUnavailable("S3 backend does not expose get_presigned_put_url")

        # Bucket follows the web lane: files published to the web go to the
        # CDN-fronted public bucket; every other file stays on the default.
        # 🚨 public_bucket_or_raise, NEVER `or default_bucket` — a public
        # upload landing in the private bucket is a lie the system tells
        # itself (see cdn.public_bucket_or_raise). This is a BROWSER upload
        # path: the presigned PUT is handed to the user's browser, so a wrong
        # bucket here bakes the mistake into bytes we never see again.
        from ..cdn import public_bucket_or_raise

        default_bucket = self._engine.config.resolve_s3_bucket()
        bucket = (
            public_bucket_or_raise("presigned.create") if published_to_web else default_bucket
        )

        storage_uri = f"s3://{bucket}/{owner_id}/{file_path}"
        presigned = backend.get_presigned_put_url(
            f"{bucket}/{owner_id}/{file_path}",
            expires_in=expires_in,
            content_type=content_type,
            max_size_bytes=expected_size_bytes,
        )

        upload_id = str(uuid.uuid4())
        await self._put_pending(
            upload_id,
            _PendingEntry(
                user_id=owner_id,
                file_path=file_path,
                storage_uri=storage_uri,
                content_type=content_type,
                published_to_web=bool(published_to_web),
                shown_to=shown_to,
                metadata=dict(metadata or {}),
                expected_size=expected_size_bytes,
                created_at=time.monotonic(),
            ),
        )
        await self._gc()

        return PresignedCreateResult(
            upload_id=upload_id,
            url=presigned["url"],
            headers=presigned.get("headers") or {},
            expires_in=presigned.get("expires_in") or expires_in,
            file_path=file_path,
            storage_uri=storage_uri,
        )

    # ------------------------------------------------------------------
    # Finalize
    # ------------------------------------------------------------------

    async def finalize(
        self,
        *,
        upload_id: str,
        owner_id: str,
        actual_size_bytes: int | None = None,
        checksum: str | None = None,
        extra_metadata: dict[str, Any] | None = None,
        expected_checksum: str | None = None,
        organization_id: str,
    ) -> PresignedFinalizeResult:
        """Register the uploaded object in files.files. The bytes are already
        in S3 thanks to the browser PUT.

        The size is HEAD-verified against S3 to defend against client
        misreporting. Folder chain is created via ``ensure_folder_chain``
        so the files.files row lands with a real ``parent_folder_id``.

        ``organization_id`` is the initiating request's admitted organization. It
        is REQUIRED (AD240): every folder the chain creates and the file row itself
        carry it; a missing one is refused before the pending upload is consumed,
        so the client can retry with its organization.
        """
        if not organization_id:
            raise ValueError(
                f"presigned finalize {upload_id!r}: organization_id is required — the "
                "upload's folders and file row are never left to a database default"
            )
        pending = await self._peek_pending(upload_id)
        if not pending:
            raise UploadNotFound(f"No pending upload {upload_id!r} (expired or already finalized)")
        if pending.user_id != owner_id:
            raise OwnerMismatch(f"Upload {upload_id!r} was issued for {pending.user_id!r}")
        if not await self._claim_pending(upload_id):
            # A concurrent finalize won the atomic claim.
            raise UploadNotFound(f"No pending upload {upload_id!r} (expired or already finalized)")

        file_path = pending.file_path
        storage_uri = pending.storage_uri

        # SPEC-SERVER §3, RE-EVALUATED HERE. The presigned lane is a complete
        # content-write surface -- finalize upserts files.files, so it can
        # overwrite an alive row at an existing file_path -- and it took no
        # precondition of any kind. Evaluated at finalize rather than only at
        # creation because a browser PUT runs for as long as the upload takes,
        # and the state the client checked when it asked for the URL is not the
        # state it is about to overwrite. The path is only known here: create()
        # hands it to the session and _take_pending pops it.
        if expected_checksum:
            from ..preconditions import check_expected_checksum

            check_expected_checksum(
                await self._engine.db.get_file_by_path_async(owner_id, file_path),
                expected_checksum,
            )

        # Authoritative size via S3 HEAD; tolerate propagation lag by
        # falling back to the client-reported value.
        actual_size = actual_size_bytes
        router = self._engine.router
        if router.is_configured("s3"):
            try:
                backend = router.s3
                uri_path = storage_uri.split("://", 1)[1]
                obj_bucket, obj_key = backend._parse_path(uri_path)
                head = backend._get_client().head_object(
                    Bucket=obj_bucket,
                    Key=obj_key,
                )
                actual_size = int(head.get("ContentLength") or actual_size or 0)
            except Exception:
                pass

        # Folder chain.
        db = self._engine.db
        parent_path = "/".join(file_path.split("/")[:-1])
        parent_id: str | None = None
        if parent_path:
            # Never swallowed: a refused chain used to land the file with
            # parent_folder_id NULL under a nested file_path (silent path drift).
            r = await db._rpc(
                "files", "ensure_folder_chain", owner_id, parent_path, str(organization_id)
            )
            parent_id = str(r) if r else None

        merged_metadata = dict(pending.metadata)
        if extra_metadata:
            for k, v in extra_metadata.items():
                merged_metadata.setdefault(k, v)

        # Content-hash dedup, the same doctrine as the TUS finalize: the caller declared this
        # PATH, so the upload always gets a row of its own there. When the same bytes are
        # already a canonical row of this owner+organization at ANOTHER path, the new row is
        # linked to it (``duplicate_of_file_id``) instead of colliding on
        # ``cld_files_dedup_canonical`` (live 500, 2026-10-27). A race that still collides
        # converges inside ``insert_file_converging_async``.
        from ...dedup import insert_file_converging_async, lookup_existing_async

        duplicate_of: str | None = None
        existing_here = False
        if checksum:
            found = await lookup_existing_async(
                db, checksum=checksum, owner_id=owner_id, organization_id=str(organization_id)
            )
            if found.has_duplicate and found.existing is not None:
                if found.existing.get("file_path") == file_path:
                    existing_here = True
                else:
                    duplicate_of = str(found.existing["id"])

        payload = {
                "owner_id": owner_id,
                "file_path": file_path,
                "storage_uri": storage_uri,
                "file_name": file_path.split("/")[-1],
                "mime_type": pending.content_type,
                "size_bytes": actual_size,
                "checksum": checksum,
                **RowAccess(published_to_web=pending.published_to_web, shown_to=pending.shown_to).columns(owner_id),
                "parent_folder_id": parent_id,
                "organization_id": str(organization_id),
                "metadata": merged_metadata,
        }
        if duplicate_of:
            payload["duplicate_of_file_id"] = duplicate_of
        record = await insert_file_converging_async(
            db, payload, owner_id=owner_id, organization_id=str(organization_id)
        )

        # URLs from the central minter — same shape as managed_write_async.
        urls = await self._engine.build_urls_for_record_async(
            {
                "published_to_web": pending.published_to_web,
                "storage_uri": storage_uri,
                "checksum": checksum,
                "file_name": record.get("file_name") or file_path.rsplit("/", 1)[-1],
                "mime_type": record.get("mime_type"),
                "deleted_at": None,
            }
        )

        return PresignedFinalizeResult(
            file_id=record["id"],
            file_path=file_path,
            storage_uri=storage_uri,
            size_bytes=int(actual_size or 0),
            checksum=checksum,
            version_number=record.get("current_version", 1),
            url=urls.get("url"),
            cdn_url=urls.get("cdn_url"),
            is_new=not existing_here,
        )


__all__ = [
    "PresignedManager",
    "PresignedCreateResult",
    "PresignedFinalizeResult",
    "PresignedError",
    "PresignedUnavailable",
    "UploadNotFound",
    "OwnerMismatch",
]
