"""Sync engine — orchestrates cloud upload, database tracking, and versioning.

This is the central component of the cloud sync layer.  It is created by
FileManager when a ``CloudSyncConfig`` is provided, and is called
automatically on every file write/delete operation.

Design goals:
    1. **Transparent** — local operations succeed even if sync fails: the
       FileManager hook runs ``track_write`` in a daemon thread. ``track_write``
       itself converges a dedup collision and logs AND re-raises every other
       failure — a background save is never silently lost.
    2. **Background** — auto-sync on existing FileManager methods runs in
       a daemon thread (sync context) or a background task (async context).
    3. **Full control** — the ``managed_*`` methods give callers a
       ``SyncResult`` with file_id, version, URL, etc.
    4. **Permission-aware** — managed reads/writes check permissions.

Usage::

    # Auto-created by FileManager:
    fm = FileManager("my_app", cloud_sync=CloudSyncConfig(...))

    # Background sync happens on every write:
    fm.write_json("base", "report.json", data)

    # Full control via managed methods:
    result = await fm.managed_write_async("reports/q1.json", data)
    result = await fm.managed_read_async("reports/q1.json")
"""

from __future__ import annotations

from matrx_orm import db_constraint, db_sqlstate

# The (owner_id, file_path) unique key: its current name and the legacy cld_-prefixed one.
_PATH_UNIQUE_CONSTRAINTS = frozenset({"files_owner_id_file_path_key", "cld_files_owner_id_file_path_key"})

import asyncio
import hashlib
import json
import logging
import mimetypes
import threading
import uuid
from datetime import datetime
from posixpath import basename, dirname
from typing import TYPE_CHECKING, Any

from matrx_utils.row_access import (
    SHOWN_TO_TYPE_DEFAULT,
    LegacyLevelInput,
    RowAccess,
    publish_columns,
    reconcile_row_access,
)

from ..artifact_identity import artifact_identity_columns
from ..user_visible import stamp_machine_artifact
from .config import CloudSyncConfig
from .db import DatabaseClient
from ..dedup import (
    insert_file_converging,
    insert_file_converging_async,
    update_file_converging,
    update_file_converging_async,
)
from ..derivations import resolve_file_lineage
from .models import SyncResult
from .permissions import PermissionsManager
from .versioning import VersionManager

if TYPE_CHECKING:
    from .download_stream import DownloadStreamer
    from .transports.presigned import PresignedManager
    from .transports.tus import TUSSessionManager
    from .variants_service import VariantsService

logger = logging.getLogger(__name__)


def row_access_insert_columns(
    published_to_web: bool | None, shown_to: str | None, actor_id: str | None
) -> dict[str, Any]:
    """Row-access columns for a NEW file (access ladder T-13).

    ``published_to_web`` is the only anonymous lane (and decides the public bucket);
    ``shown_to`` is a list filter only. A new file defaults to not published and shown
    only to its creator in lists — what an upload with no stated audience always meant.
    """
    # Unstated → "only me" (what an upload with no stated audience always meant);
    # SHOWN_TO_TYPE_DEFAULT → NULL (follow the type's knob).
    return RowAccess(
        published_to_web=bool(published_to_web),
        shown_to=shown_to if shown_to is not None else "only_me",
    ).columns(actor_id)


def row_access_update_columns(
    published_to_web: bool | None, shown_to: str | None, actor_id: str | None
) -> dict[str, Any]:
    """Row-access columns for a new VERSION of an existing file: only what the caller stated.

    A new version never moves the web lane or the list filter by omission (the stored bytes
    stay in the bucket the row already names).
    """
    out: dict[str, Any] = {}
    if published_to_web is not None:
        out.update(publish_columns(published_to_web, actor_id))
    if shown_to is not None:
        out["shown_to"] = None if shown_to == SHOWN_TO_TYPE_DEFAULT else shown_to
    return out


def _legacy_write_access(
    published_to_web: bool | None, shown_to: str | None, visibility: LegacyLevelInput | None
) -> tuple[bool | None, str | None, bool]:
    """Accept retiring writes without changing omission semantics.

    Explicit row-access words win. ``link`` is an action, not a stored row
    state, and is completed after the file row exists.
    """
    if visibility is None:
        return published_to_web, shown_to, False
    access = reconcile_row_access(
        published_to_web=published_to_web,
        shown_to=shown_to,
        legacy_level=visibility,
        boundary="cloud sync managed write",
    )
    if published_to_web is not None or shown_to is not None:
        return published_to_web, shown_to, False
    return access.published_to_web, access.shown_to, access.wants_anyone_link


class FolderOrganizationMismatch(ValueError):
    """A write that must land in ONE organization's folder met a folder of another organization.

    A person's folder tree is per organization; every folder lookup is keyed on
    (owner, organization, path), so this names a lookup defect — it is never resolved by reusing
    the other organization's folder (``_reconcile_folder_org``).
    """


class EmptyOverwriteRefused(ValueError):
    """A zero-byte body would replace a file that already holds bytes.

    Production defect (2026-10-22): image rows were overwritten with empty content — the version
    advanced, ``size_bytes`` went to 0 and every later read was an empty body no browser can
    decode. The empty-content guard exists so an empty upload never aliases an unrelated file; it
    must never let an empty body erase a file that has content. ``http_status``/``code``/
    ``user_message`` are read by ``api/errors.py:map_exception`` (its own-status branch).
    """

    http_status = 409
    code = "empty_overwrite_refused"
    user_message = "That save is empty and would erase the file's content. Nothing was changed."


def _refuse_empty_overwrite(existing: dict | None, content_bytes: bytes) -> None:
    """Refuse an empty body over an existing row that records stored bytes.

    An existing row with no recorded size (or 0) has nothing to lose, so an empty write is allowed
    there; every other overwrite with empty content is refused BEFORE any storage write or row update.
    """
    if existing is None or content_bytes or not existing.get("size_bytes"):
        return
    raise EmptyOverwriteRefused(
        f"refused an empty write over file {existing['id']}: {existing['size_bytes']} bytes are stored"
    )




class HardDeleteDatabaseError(RuntimeError):
    """Raised when neither database cascade can delete a file row."""


class HardDeleteStorageError(RuntimeError):
    """Raised after a DB cascade when one or more storage objects remain."""

    def __init__(self, file_id: str, failed_uris: list[str]) -> None:
        self.file_id = file_id
        self.failed_uris = tuple(failed_uris)
        super().__init__(
            f"hard-delete purged the database row for {file_id!r}, but storage "
            f"deletion failed for {len(failed_uris)} object(s)"
        )


class OrphanCleanupError(RuntimeError):
    """A failed insert left exclusive bytes that could not be removed."""

    def __init__(self, storage_uri: str, context: str) -> None:
        self.storage_uri = storage_uri
        self.context = context
        super().__init__(f"{context}: failed to remove unreferenced storage object {storage_uri!r}")


def _stamp_request_id(metadata: dict | None) -> dict:
    """Add ``metadata.request_id`` from the active matrx-utils context.

    Phase 1d.5 (FE REQUESTS item 9). Every cloud_sync write stamps the
    request_id of the inbound HTTP request into the row's ``metadata``
    JSONB. Supabase Realtime then echoes the metadata back to every
    subscriber, including the FE that just issued the write — which uses
    the round-tripped request_id to dedupe its own optimistic state
    from the server broadcast.

    Caller-supplied ``metadata.request_id`` always wins (back-compat +
    explicit override). When no active context is available (background
    jobs, scripts, tests) the field is simply not added.
    """
    out = dict(metadata or {})
    if "request_id" in out:
        return out
    try:
        from matrx_utils.ctx import get_active_context

        ctx = get_active_context()
        rid = getattr(ctx, "request_id", None) if ctx else None
        if rid:
            out["request_id"] = rid
    except Exception:
        # Never let request-id stamping break a real write.
        pass
    return out


class SyncEngine:
    """Orchestrates cloud storage, Postgres metadata, permissions, and versioning."""

    def __init__(self, config: CloudSyncConfig, router: object) -> None:
        self._config = config
        self._router = router  # BackendRouter
        self._db = DatabaseClient(config)
        self.permissions = PermissionsManager(self._db, config.user_id)
        self.versions = VersionManager(self._db, router, config)
        # Lazy: instantiated on first access so a circular import between
        # variants_service and sync_engine can't form.
        self._variants_service: object | None = None
        self._fm_ref: object | None = None  # set by FileManager when wiring

    # ------------------------------------------------------------------
    # Public sub-component accessors. These supersede direct ``_db``,
    # ``_router``, ``_config`` reads from outside this class — callers
    # should use the unprefixed names. The underscore variants are kept
    # for the lifetime of the v1.x line for back-compat.
    # ------------------------------------------------------------------

    @property
    def db(self) -> DatabaseClient:
        """The metadata store. Use ``engine.db.get_file_async(...)`` etc."""
        return self._db

    @property
    def router(self) -> object:
        """The storage gateway (``BackendRouter``). Use for raw bytes reads/writes."""
        return self._router

    @property
    def config(self) -> CloudSyncConfig:
        return self._config

    @property
    def fm(self) -> object:
        """The owning FileManager. Set by FileManager.__init__ via _fm_ref.

        Needed by VariantsService to reach fm.image_handler for the actual
        Pillow encoder. Returns None when the engine was constructed
        outside a FileManager (rare — only test fixtures do this).
        """
        return self._fm_ref

    @property
    def variants(self) -> VariantsService:
        """The idempotent variants engine. See VariantsService docstring."""
        if self._variants_service is None:
            from .variants_service import VariantsService

            self._variants_service = VariantsService(self)
        return self._variants_service  # type: ignore[return-value]

    @property
    def tus(self) -> TUSSessionManager:
        """The TUS resumable-upload state machine. See TUSSessionManager docstring."""
        if not hasattr(self, "_tus_manager") or self._tus_manager is None:
            from .transports.tus import DEFAULT_MAX_SIZE, TUSSessionManager

            self._tus_manager = TUSSessionManager(
                self,
                max_size=self._config.tus_max_size_bytes or DEFAULT_MAX_SIZE,
            )
        return self._tus_manager  # type: ignore[return-value]

    @property
    def presigned(self) -> PresignedManager:
        """The presigned-PUT upload coordinator. Two-phase create + finalize."""
        if not hasattr(self, "_presigned_manager") or self._presigned_manager is None:
            from .transports.presigned import PresignedManager

            self._presigned_manager = PresignedManager(self)
        return self._presigned_manager  # type: ignore[return-value]

    @property
    def streamer(self) -> DownloadStreamer:
        """Range-aware download streamer. Picks S3 chunked vs buffered."""
        if not hasattr(self, "_streamer") or self._streamer is None:
            from .download_stream import DownloadStreamer

            self._streamer = DownloadStreamer(self)
        return self._streamer  # type: ignore[return-value]

    # ------------------------------------------------------------------
    # Authorized record fetch — the public primitive every router /
    # service should use instead of ``engine._db.get_file_async(id)``
    # followed by an inlined ``_require_access`` block. Returns the
    # cld_files row only after the access check passes; raises
    # ``PermissionError`` on denial and ``FileNotFoundError`` on miss.
    # ------------------------------------------------------------------

    async def get_authorized_record_async(
        self,
        file_id: str,
        *,
        user_id: str,
        level: str = "read",
    ) -> dict:
        """Load a file row and enforce access in one call.

        ``level`` is ``"read" | "write" | "admin"``. Raises ``FileNotFoundError``
        if the row is missing, ``PermissionError`` if the caller lacks access.

        Every decision, including ownership, is delegated to
        ``PermissionsManager``. Contextual system artifacts deliberately ignore
        their historical ``created_by`` owner and follow their container's
        access and revocation instead. Do not add owner or publish-state shortcuts
        here.
        """
        record = await self._db.get_file_async(file_id)
        if not record:
            raise FileNotFoundError(f"File {file_id!r} not found")
        await self.permissions.require_async("file", record["id"], level, user_id)
        return record

    # ------------------------------------------------------------------
    # User context (for per-request user switching in web apps)
    # ------------------------------------------------------------------

    def set_user(self, user_id: str) -> None:
        """Switch the active user (call per-request in FastAPI)."""
        self._config = CloudSyncConfig(
            user_id=user_id,
            s3_bucket=self._config.s3_bucket,
            storage_backend=self._config.storage_backend,
            auto_sync=self._config.auto_sync,
            version_storage_prefix=self._config.version_storage_prefix,
            database_url=self._config.database_url,
        )
        self.permissions.user_id = user_id

    @property
    def user_id(self) -> str:
        return self._config.user_id

    @property
    def auto_sync(self) -> bool:
        return self._config.auto_sync

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _resolve_user_id(self, explicit: str | None) -> str:
        """Resolve user_id with three-level priority:

        1. Explicitly passed ``user_id`` argument (highest — per-call override).
        2. ``CloudSyncConfig.user_id`` baked in at construction time.
        3. Active request context via ``matrx_utils.ctx.get_active_user_id()``
           (set automatically by middleware in web apps that called
           ``configure_context()``).

        Returns ``""`` if none of the above is set.
        """
        if explicit:
            return explicit
        if self._config.user_id:
            return self._config.user_id
        from matrx_utils.ctx import get_active_user_id

        return get_active_user_id()

    def _storage_uri(
        self,
        file_path: str,
        user_id: str | None = None,
        *,
        published_to_web: bool = False,
        visibility: LegacyLevelInput | None = None,
    ) -> str:
        """Build the canonical cloud storage URI for a file path.

        Files published to the web (``published_to_web=True``) live in a dedicated
        public S3 bucket whose name equals the CDN host (configured
        via ``AWS_S3_PUBLIC_BUCKET`` + ``CDN_PUBLIC_BASE_URL``).
        Private/shared files always use the default bucket.

        🚨 A public write with no public bucket RAISES — it does not fall back
        to the default bucket. See ``public_bucket_or_raise``.
        """
        from .cdn import public_bucket_or_raise

        if visibility is not None:
            published_to_web, _, _ = _legacy_write_access(None, None, visibility)
        uid = self._resolve_user_id(user_id)
        backend = self._config.storage_backend
        if published_to_web:
            bucket = public_bucket_or_raise("_storage_uri")
        else:
            bucket = self._config.resolve_s3_bucket()
        return f"{backend}://{bucket}/{uid}/{file_path}"

    def _delete_orphan_or_raise(self, storage_uri: str, *, context: str) -> None:
        try:
            self._router.delete(storage_uri)
        except Exception as exc:
            logger.error(
                "%s: orphan cleanup failed for %s",
                context,
                storage_uri,
                exc_info=True,
            )
            raise OrphanCleanupError(storage_uri, context) from exc

    async def _delete_orphan_or_raise_async(
        self,
        storage_uri: str,
        *,
        context: str,
    ) -> None:
        try:
            await self._router.delete_async(storage_uri)
        except Exception as exc:
            logger.error(
                "%s: orphan cleanup failed for %s",
                context,
                storage_uri,
                exc_info=True,
            )
            raise OrphanCleanupError(storage_uri, context) from exc

    @staticmethod
    def _checksum(content: bytes) -> str:
        return hashlib.sha256(content).hexdigest()

    async def _checksum_async(self, content: bytes) -> str:
        """Hash upload bytes without monopolizing the application event loop."""
        return await asyncio.to_thread(self._checksum, content)

    # ==================================================================
    # URL BUILDING — centralized. ALL callers (routers, services, scripts)
    # use these helpers; nothing else may import cdn.public_url_for or
    # call _router.get_url_async directly on a record's storage_uri.
    #
    # 🚨 THE LAW (Arman 2026-08-21/26): these helpers NEVER mint a signed
    # URL. A file is addressed by id; the URLs here are durable — CDN for
    # public rows, the authenticated /files/{id}/download route otherwise.
    # Presigned URLs exist only in the three handoff lanes documented in
    # cloud_sync/render_urls.py. Never add a presign call back here.
    # ==================================================================

    # TTL for the provider-handoff mint lane ONLY (resolve_media_async).
    # Never used for client-facing URLs — those are durable and unexpiring.
    DEFAULT_SIGNED_TTL = 3600

    @staticmethod
    def _content_disposition(file_name: str | None, disposition: str) -> str:
        """Build an RFC 6266 Content-Disposition value with safe quoting.

        ``disposition`` is "inline" or "attachment". File names with
        non-ASCII characters use the ``filename*=UTF-8''<pct-encoded>``
        extended form.
        """
        from urllib.parse import quote as _quote

        name = file_name or "download"
        try:
            name.encode("ascii")
            return f'{disposition}; filename="{name}"'
        except UnicodeEncodeError:
            ascii_fallback = name.encode("ascii", "replace").decode("ascii")
            return (
                f'{disposition}; filename="{ascii_fallback}"; '
                f"filename*=UTF-8''{_quote(name, safe='')}"
            )

    def build_urls_for_record(self, record_or_synthetic: dict) -> dict:
        """Build the durable URL contract for a file. NEVER mints a signed URL.

        ``record_or_synthetic`` is either a real ``cld_files`` row (dict
        as returned by ``DatabaseClient.get_file_async``) OR a synthetic
        dict assembled from a ``SyncResult`` for just-written files
        (must carry at minimum ``id`` (or ``file_id``) and ``published_to_web``;
        optional ``checksum``, ``file_name``, ``mime_type``, ``deleted_at``).

        Returns ``{url, cdn_url, download_url}`` — all durable:

        - ``cdn_url``       permanent CDN URL (public + CDN configured only)
        - ``url``           always-renderable: the CDN URL when public,
                            otherwise the authenticated durable route
                            ``/files/{id}/download?inline=1``
        - ``download_url``  attachment-disposition durable route
                            ``/files/{id}/download``

        Soft-deleted records yield all-None values. Pure function — no
        S3 call, no I/O; the sync and async entry points are identical.
        """
        empty = {"url": None, "cdn_url": None, "download_url": None}
        if not record_or_synthetic:
            return empty
        if record_or_synthetic.get("deleted_at"):
            return empty
        from .cdn import public_url_for
        from .render_urls import durable_download_url, durable_inline_url

        cdn_url = public_url_for(record_or_synthetic)
        raw_id = record_or_synthetic.get("id") or record_or_synthetic.get("file_id")
        file_id = str(raw_id) if raw_id else None
        if not file_id:
            # A URL request for a row with no identity is a caller bug —
            # every real row and every SyncResult synthetic carries the id.
            logger.warning(
                "build_urls_for_record: record has no id/file_id — cannot build "
                "the durable download route (file_name=%s)",
                record_or_synthetic.get("file_name"),
            )
            return {**empty, "cdn_url": cdn_url, "url": cdn_url}
        inline = durable_inline_url(file_id)
        download = durable_download_url(file_id)
        return {
            "url": cdn_url or inline,
            "cdn_url": cdn_url,
            "download_url": download,
        }

    async def build_urls_for_record_async(self, record_or_synthetic: dict) -> dict:
        """Async entry point for ``build_urls_for_record``.

        Since the durable contract requires no minting, this is now a pure
        delegation — kept so every existing async call site keeps working
        and so a future I/O need has one seam to grow in.
        """
        return self.build_urls_for_record(record_or_synthetic)

    @staticmethod
    def _to_bytes(content: object) -> bytes:
        """Convert content to bytes for upload and checksum."""
        if isinstance(content, bytes):
            return content
        if isinstance(content, str):
            return content.encode("utf-8")
        if isinstance(content, dict | list):
            return json.dumps(content, indent=2, default=str).encode("utf-8")
        if isinstance(content, memoryview):
            return bytes(content)
        return str(content).encode("utf-8")

    @staticmethod
    def _guess_mime(file_path: str) -> str | None:
        mime, _ = mimetypes.guess_type(file_path)
        return mime

    @staticmethod
    def _metadata_organization_id(metadata: dict[str, Any] | None) -> str | None:
        if not metadata:
            return None
        direct = metadata.get("organization_id")
        if direct:
            return str(direct)
        scope = metadata.get("scope")
        if isinstance(scope, dict) and scope.get("organization_id"):
            return str(scope["organization_id"])
        return None

    @staticmethod
    def _warn_write_organization_converges_on_existing_row(
        file_path: str, existing_org_id: str | None, requested_org_id: str | None
    ) -> None:
        """A write's requested organization disagrees with the existing row's.

        ``cld_files`` is UNIQUE on ``(created_by, file_path)`` — one row per
        owner per path, forever — so a write naming a DIFFERENT organization
        than the row already carries can never relocate it; there is nowhere
        else for the bytes to land. The row's own organization wins (context,
        never authority: the caller's requested org is a hint, not a grant)
        and the write proceeds as an ordinary update, gated by the normal
        write-ACL check right after this. Until this fix the write refused
        outright with an internal-column error ("organization_id cannot
        change...") that a person re-dropping the same file — e.g. the same
        export re-uploaded under a different active organization — could
        never recover from (production defect, bring-your-export round 7,
        2026-09-18). Convergence is announced here, never silent.
        """
        logger.warning(
            "matrx-files: write to %s requested organization %s but the "
            "existing row belongs to organization %s; keeping the row's own "
            "organization (the path already identifies exactly one owner's "
            "row) instead of refusing the write",
            file_path,
            requested_org_id,
            existing_org_id,
        )

    # THE ORGANIZATION OF A WRITE IS CARRIED, NEVER DEFAULTED
    # (common-docs/policies/context-is-carried-never-rebuilt.md). The three
    # lawful sources, in order:
    #   1. the organization the caller passes (metadata / an existing row's own
    #      column / the host's explicit argument) — context, never authority, so
    #      it is verified against real membership before it is used;
    #   2. the organization the request context CARRIES (injected by the host
    #      through ``configure_context``; in aidream that is the AppContext the
    #      auth boundary admitted with a VERIFIED organization, so it is READ
    #      here and not re-verified);
    #   3. nothing — and then the write REFUSES, naming this site and the remedy.
    # Until 2026-09-17 branch 3 was a per-user saved-organization lookup: a
    # write whose organization the caller had dropped landed silently in an
    # organization picked for the owner instead of the tenant the person was
    # working in. No per-user lookup can answer "nobody passed one".
    _ORG_REFUSAL = (
        "matrx-files: this write carries no organization (owner=%s). "
        "Pass organization_id= explicitly (the file row's own column, the "
        "upload metadata, or the request's organization), or run it inside a "
        "request context that carries one (matrx_utils configure_context / "
        "X-Organization-Id at the host boundary). A file's organization is "
        "never defaulted to an organization picked for the owner."
    )

    def _carried_organization_id(self) -> str | None:
        """The organization THIS request was admitted with, or None.

        Reads ``matrx_files.request_organization.admitted_organization_id`` — the
        ONE resolver — instead of a single ambient seam. Until 2026-09-19 this
        read only ``matrx_utils.ctx``, which the matrx-files STANDALONE host
        (files.matrxserver.com) never wired, so every upload there refused with
        ``_ORG_REFUSAL`` while the browser's verified ``X-Organization-Id`` sat
        unread on the matrx-connect AppContext one layer away. See that module's
        docstring for the whole seam.
        """
        from matrx_files.request_organization import admitted_organization_id

        return admitted_organization_id()

    def _resolve_write_organization_id(
        self, user_id: str, organization_id: str | None = None
    ) -> str:
        if organization_id and organization_id == self._carried_organization_id():
            # Not a claim — this IS the organization the auth boundary admitted
            # for this request (AuthMiddleware already ran `iam.has_org_access_for`
            # before any route code). Threading it explicitly from the API edge
            # must cost exactly what reading it ambiently did: no second
            # membership round-trip per upload, and the same answer.
            return str(organization_id)
        if organization_id:
            allowed = self._db._rpc_sync(
                "iam",
                "has_org_access_for",
                user_id,
                organization_id,
            )
            if not allowed:
                raise PermissionError(
                    f"user {user_id} is not a member of organization {organization_id}"
                )
            return str(organization_id)
        carried = self._carried_organization_id()
        if carried:
            return carried
        raise ValueError(self._ORG_REFUSAL % (user_id or "<none>"))

    async def _resolve_write_organization_id_async(
        self, user_id: str, organization_id: str | None = None
    ) -> str:
        if organization_id and organization_id == self._carried_organization_id():
            # See the sync twin: the admitted organization is not a claim.
            return str(organization_id)
        if organization_id:
            allowed = await self._db._rpc(
                "iam",
                "has_org_access_for",
                user_id,
                organization_id,
            )
            if not allowed:
                raise PermissionError(
                    f"user {user_id} is not a member of organization {organization_id}"
                )
            return str(organization_id)
        carried = self._carried_organization_id()
        if carried:
            return carried
        raise ValueError(self._ORG_REFUSAL % (user_id or "<none>"))

    async def _free_path_when_row_is_in_unreachable_org_async(
        self,
        uid: str,
        file_path: str,
        existing: dict | None,
        requested_org_id: str | None,
    ) -> tuple[dict | None, str]:
        """Never adopt a path row of an organization the writer cannot write into.

        ``cld_files`` is unique on ``(created_by, file_path)``, so a person's earlier file at the
        same path in ANOTHER organization is found by the path lookup. Writing "over" it adopted
        that row's organization and refused with "user ... is not a member of organization ..."
        when the person has since left it (production 2026-10-24: a brand photo upload
        ``Images/People/square.png`` met the person's old row of an organization they no longer
        belong to). A row of an organization the writer is still a member of keeps the ordinary
        converge-on-the-row rule; a row of one they cannot reach is not theirs to update, so
        the write becomes a new file in the REQUESTED organization at the first free
        ``name (n).ext`` beside it, announced in the log.
        """
        if existing is None or not requested_org_id:
            return existing, file_path
        existing_org = existing.get("organization_id")
        if existing_org is None or str(existing_org) == str(requested_org_id):
            return existing, file_path
        if str(existing_org) == str(self._carried_organization_id() or ""):
            return existing, file_path
        allowed = await self._db._rpc("iam", "has_org_access_for", uid, str(existing_org))
        if allowed:
            return existing, file_path
        stem, dot, ext = file_path.rpartition(".") if "." in basename(file_path) else (file_path, "", "")
        n = 2
        while True:
            candidate = f"{stem} ({n}){dot}{ext}"
            if await self._db.get_file_by_path_async(uid, candidate) is None:
                break
            n += 1
        logger.warning(
            "matrx-files: %s already exists in organization %s, which user %s cannot write into; "
            "writing a new file for organization %s at %s instead of adopting that row",
            file_path, existing_org, uid, requested_org_id, candidate,
        )
        return None, candidate

    async def _validate_duplicate_target_async(
        self,
        *,
        user_id: str,
        organization_id: str,
        duplicate_of_file_id: str,
        checksum: str | None,
    ) -> None:
        """Require one same-scope canonical row with byte-identical content."""
        target = await self._db.get_file_async(
            duplicate_of_file_id,
            include_deleted=False,
        )
        valid = bool(
            target
            and checksum
            and target.get("checksum")
            and str(target.get("checksum")).lower() == checksum.lower()
            and str(target.get("owner_id") or "") == user_id
            and str(target.get("organization_id") or "") == organization_id
            and target.get("parent_file_id") is None
            and target.get("duplicate_of_file_id") is None
        )
        if not valid:
            raise ValueError(
                "duplicate_of_file_id must reference a canonical file "
                "with identical content in the same owner and organization"
            )

    @staticmethod
    def _reconcile_folder_org(
        existing: dict,
        folder_path: str,
        user_id: str,
        org_id: str,
        exact: bool = False,
    ) -> str:
        """Return the id of the user's folder at ``folder_path`` IN ``org_id``.

        A person's folder tree is per organization (Arman 2026-10-10: every item has one home
        scope and the organization follows the home), so a file and the folder it lives in
        always share an organization. Every lookup that feeds this is keyed on
        ``(owner, organization, path)``; a folder of another organization reaching here is a
        lookup defect and is refused by name — never reused. Until 2026-10-12 a person's upload
        REUSED their other-organization folder at the same path (the 2026-07-27 ruling, made
        when folders were unique per person, not per organization); that left 977 files and
        28,517 folders under another organization's folder and made every real move into such a
        folder fail "cross-organization move refused". ``exact`` is kept for callers that pass
        it; every placement is now exact.
        """
        del exact
        existing_org = str(existing.get("organization_id") or "")
        if existing_org != str(org_id):
            raise FolderOrganizationMismatch(
                f"The folder {folder_path!r} of user {user_id} belongs to organization "
                f"{existing_org or '<none>'}, but this write is for organization {org_id}; a file "
                "lives only in a folder of its own organization, so nothing was written."
            )
        return existing["id"]

    def _ensure_folder(
        self,
        file_path: str,
        user_id: str,
        organization_id: str | None = None,
    ) -> str | None:
        """Ensure the parent folder exists in the database, return its id."""
        folder_path = dirname(file_path)
        if not folder_path or folder_path == ".":
            return None

        org_id = organization_id or self._resolve_write_organization_id(user_id)
        existing = self._db.get_folder_by_path(user_id, folder_path, org_id)
        if existing:
            return self._reconcile_folder_org(existing, folder_path, user_id, org_id)

        # Ensure parent folders recursively
        parent_id = self._ensure_folder(folder_path, user_id, org_id)
        folder_name = basename(folder_path)

        folder_data = {
            "owner_id": user_id,
            "folder_path": folder_path,
            "folder_name": folder_name,
            "parent_id": parent_id,
            "organization_id": org_id,
        }
        try:
            result = self._db.create_folder(folder_data)
        except Exception as exc:
            # Another writer may have created this owner/path between our
            # read and insert. Re-read instead of using an upsert: an upsert
            # could silently MOVE that winner into this request's organization.
            # Reading and reusing it does not.
            winner = self._db.get_folder_by_path(user_id, folder_path, org_id)
            if not winner:
                winner = self._revive_trashed_folder(
                    user_id, folder_path, org_id, insert_exc=exc
                )
            if not winner:
                raise
            return self._reconcile_folder_org(winner, folder_path, user_id, org_id)
        return result["id"]

    async def _ensure_folder_async(
        self,
        file_path: str,
        user_id: str,
        organization_id: str | None = None,
        *,
        exact: bool = False,
    ) -> str | None:
        folder_path = dirname(file_path)
        if not folder_path or folder_path == ".":
            return None

        org_id = organization_id or await self._resolve_write_organization_id_async(user_id)
        existing = await self._db.get_folder_by_path_async(user_id, folder_path, org_id)
        if existing:
            return self._reconcile_folder_org(existing, folder_path, user_id, org_id, exact)

        parent_id = await self._ensure_folder_async(folder_path, user_id, org_id, exact=exact)
        folder_name = basename(folder_path)

        folder_data = {
            "owner_id": user_id,
            "folder_path": folder_path,
            "folder_name": folder_name,
            "parent_id": parent_id,
            "organization_id": org_id,
        }
        try:
            result = await self._db.create_folder_async(folder_data)
        except Exception as exc:
            # Never OVERWRITE the winner's organization scope — but reusing the
            # owner's own folder is not an overwrite.
            winner = await self._db.get_folder_by_path_async(user_id, folder_path, org_id)
            if not winner:
                winner = await self._revive_trashed_folder_async(
                    user_id, folder_path, org_id, insert_exc=exc
                )
            if not winner:
                raise
            return self._reconcile_folder_org(winner, folder_path, user_id, org_id, exact)
        return result["id"]

    async def ensure_labelled_folder_chain_async(
        self,
        *,
        owner_id: str,
        organization_id: str,
        segments: list[tuple[str, str]],
    ) -> tuple[str, str]:
        """Find or create ONE organization's folder chain, each folder named for a person.

        ``segments`` is ``[(path_segment, folder_name), ...]`` from the root down: the path
        segments are stable keys (an organization id, a table id) so a rerun finds the same
        folder and a rename never forks it; the names are what a person reads ("Record store",
        "Matter"). Every folder is created in ``organization_id``; a folder already at one of
        these paths in ANOTHER organization is refused (:class:`FolderOrganizationMismatch`),
        never reused. A folder already there in this organization is reused and its name is
        left as the person may have changed it. Answers ``(folder_path, folder_id)``.
        """
        if not segments:
            raise ValueError("ensure_labelled_folder_chain_async needs at least one segment")
        parent_id: str | None = None
        path = ""
        for key, label in segments:
            if not key or "/" in key or not str(label or "").strip():
                raise ValueError(
                    f"folder segment {key!r} / {label!r}: a segment is one path key (no '/') "
                    "with a non-empty name"
                )
            path = f"{path}/{key}" if path else key
            existing = await self._db.get_folder_by_path_async(owner_id, path, organization_id)
            if existing:
                parent_id = self._reconcile_folder_org(
                    existing, path, owner_id, organization_id, True
                )
                continue
            data = {
                "owner_id": owner_id,
                "folder_path": path,
                "folder_name": str(label).strip(),
                "parent_id": parent_id,
                "organization_id": organization_id,
            }
            try:
                parent_id = (await self._db.create_folder_async(data))["id"]
            except Exception as exc:
                winner = await self._db.get_folder_by_path_async(owner_id, path, organization_id)
                if not winner:
                    winner = await self._revive_trashed_folder_async(
                        owner_id, path, organization_id, insert_exc=exc
                    )
                if not winner:
                    raise
                parent_id = self._reconcile_folder_org(
                    winner, path, owner_id, organization_id, True
                )
        return path, str(parent_id)

    # ------------------------------------------------------------------
    # THE TRASHED-FOLDER WRITE BARRIER (fixed 2026-08-11)
    #
    # Folder lookups filter ``deleted_at is null``; the
    # ``(created_by, folder_path)`` uniqueness the INSERT collides with does
    # NOT. A soft-deleted folder therefore made every write beneath it fail
    # FOREVER with an unmapped 500: the lookup says absent, the INSERT says
    # duplicate, the live re-read says absent again, so the raw uniqueness
    # error escaped as "File operation failed".
    #
    # Real impact: a 2026-06-14 cleanup trashed ``Transcripts`` and
    # ``Transcripts/Recordings`` for real users. From then on EVERY finished
    # audio recording failed to save (the client retried and gave up) while
    # its 10-second chunks uploaded fine — they land in a different folder.
    #
    # Reviving is the only correct resolution, and it is not a policy call:
    # the row is the caller's OWN, the path is one they are actively writing
    # into, and creating it is exactly what they asked for. Same doctrine as
    # ``_reconcile_folder_org`` — a guard that CAN reconcile MUST reconcile.
    # Loud, because reaching here means a trashed folder was silently
    # blocking writes.
    # ------------------------------------------------------------------

    def _revive_trashed_folder(
        self,
        user_id: str,
        folder_path: str,
        organization_id: str,
        *,
        insert_exc: BaseException,
    ) -> dict | None:
        """Untrash the caller's OWN folder at ``folder_path`` in ``organization_id``, or None."""
        trashed = self._db.get_folder_by_path_any_state(user_id, folder_path, organization_id)
        if not trashed or not trashed.get("deleted_at"):
            return None
        revived = self._db.restore_folder(trashed["id"])
        self._log_folder_revival(user_id, folder_path, trashed, insert_exc)
        return revived or trashed

    async def _revive_trashed_folder_async(
        self,
        user_id: str,
        folder_path: str,
        organization_id: str,
        *,
        insert_exc: BaseException,
    ) -> dict | None:
        """Async ``_revive_trashed_folder``."""
        trashed = await self._db.get_folder_by_path_any_state_async(
            user_id, folder_path, organization_id
        )
        if not trashed or not trashed.get("deleted_at"):
            return None
        revived = await self._db.restore_folder_async(trashed["id"])
        self._log_folder_revival(user_id, folder_path, trashed, insert_exc)
        return revived or trashed

    @staticmethod
    def _log_folder_revival(
        user_id: str,
        folder_path: str,
        trashed: dict,
        insert_exc: BaseException,
    ) -> None:
        logger.warning(
            "[SyncEngine] REVIVED trashed folder %r for user %s (id=%s, trashed at %s) — "
            "it was blocking every write beneath it with %s: %s. Restored the owner's "
            "own folder rather than failing their write.",
            folder_path,
            user_id,
            trashed.get("id"),
            trashed.get("deleted_at"),
            type(insert_exc).__name__,
            insert_exc,
        )

    # ==================================================================
    # AUTO-SYNC — called by FileManager after local operations
    # ==================================================================

    def track_write(
        self,
        file_path: str,
        content: bytes | str | dict | list,
        mime_type: str | None = None,
        user_id: str | None = None,
    ) -> None:
        """Upload to cloud and record in database (FileManager's background sync).

        A save whose bytes another live canonical holds converges on it through
        ``dedup.update_file_converging`` / ``insert_file_converging``. Every
        other failure is logged with its traceback and RE-RAISED — never
        swallowed (the fire-and-forget thread boundary still logs it).
        """
        try:
            uid = self._resolve_user_id(user_id)
            content_bytes = self._to_bytes(content)
            storage_uri = self._storage_uri(file_path, uid)
            # Read the row BEFORE any byte lands: an empty body must never
            # overwrite the stored object of a file that already holds content.
            existing = self._db.get_file_by_path(uid, file_path)
            _refuse_empty_overwrite(existing, content_bytes)

            # Upload to cloud — stamp Content-Type so a bare public URL renders
            # inline (canonical keys are extensionless; pass the mime explicitly).
            self._router.write(
                storage_uri,
                content_bytes,
                content_type=mime_type or self._guess_mime(file_path),
            )

            # Every writer stamps an explicit org: the row's own, or (new path)
            # the owner's personal org exactly like managed_write.
            organization_id = (existing or {}).get(
                "organization_id"
            ) or self._resolve_write_organization_id(uid)
            folder_id = self._ensure_folder(file_path, uid, organization_id)

            # Compute metadata
            checksum = self._checksum(content_bytes)
            # Empty content hashes to the same constant SHA-256 for
            # every caller, forever — treat it as NO checksum so it can
            # never collide with (and silently alias into) an unrelated
            # file that also happens to be empty (production defect,
            # jobs-bar cold-walk-11, 2026-09-18). checksum is nullable.
            if not content_bytes:
                checksum = None
            mime = mime_type or self._guess_mime(file_path)

            if existing:
                new_version = existing["current_version"] + 1
                written = update_file_converging(
                    self._db,
                    existing["id"],
                    {
                        "storage_uri": storage_uri,
                        "size_bytes": len(content_bytes),
                        "checksum": checksum,
                        "mime_type": mime,
                        "current_version": new_version,
                    },
                    current=existing,
                    owner_id=uid,
                    organization_id=organization_id,
                )
                # parent_folder_id left this dict deliberately. The row was
                # found BY file_path and folder_id was ensured FOR that same
                # path, so this is a reconciliation, not a move — but it is
                # still a write to one of the three location columns, and
                # public.move_file is the only thing allowed to make one. It
                # recomputes file_path from the folder, so the stamp can no
                # longer land while file_path says something else.
                self._db.move_file(existing["id"], folder_id)
                file_record = {**existing, **written, "id": existing["id"]}
            else:
                file_record = insert_file_converging(
                    self._db,
                    {
                        "owner_id": uid,
                        "file_path": file_path,
                        "storage_uri": storage_uri,
                        "file_name": basename(file_path),
                        "mime_type": mime,
                        "size_bytes": len(content_bytes),
                        "checksum": checksum,
                        "parent_folder_id": folder_id,
                        "organization_id": organization_id,
                    },
                    owner_id=uid,
                    organization_id=organization_id,
                )

            # Record version
            self.versions.record_version(file_record, content_bytes, checksum=checksum, user_id=uid)

            logger.debug("Synced write: %s → %s", file_path, storage_uri)

        except Exception:
            logger.exception("Cloud sync failed for '%s'", file_path)
            raise

    async def track_write_async(
        self,
        file_path: str,
        content: bytes | str | dict | list,
        mime_type: str | None = None,
        user_id: str | None = None,
    ) -> None:
        """Async version of track_write() — same convergence, same re-raise."""
        try:
            uid = self._resolve_user_id(user_id)
            content_bytes = self._to_bytes(content)
            storage_uri = self._storage_uri(file_path, uid)
            # Read the row BEFORE any byte lands: an empty body must never
            # overwrite the stored object of a file that already holds content.
            existing = await self._db.get_file_by_path_async(uid, file_path)
            _refuse_empty_overwrite(existing, content_bytes)

            await self._router.write_async(
                storage_uri,
                content_bytes,
                content_type=mime_type or self._guess_mime(file_path),
            )

            organization_id = (existing or {}).get(
                "organization_id"
            ) or await self._resolve_write_organization_id_async(uid)
            folder_id = await self._ensure_folder_async(file_path, uid, organization_id)
            checksum = await self._checksum_async(content_bytes)
            # Empty content hashes to the same constant SHA-256 for
            # every caller, forever — treat it as NO checksum so it can
            # never collide with (and silently alias into) an unrelated
            # file that also happens to be empty (production defect,
            # jobs-bar cold-walk-11, 2026-09-18). checksum is nullable.
            if not content_bytes:
                checksum = None
            mime = mime_type or self._guess_mime(file_path)

            if existing:
                new_version = existing["current_version"] + 1
                written = await update_file_converging_async(
                    self._db,
                    existing["id"],
                    {
                        "storage_uri": storage_uri,
                        "size_bytes": len(content_bytes),
                        "checksum": checksum,
                        "mime_type": mime,
                        "current_version": new_version,
                    },
                    current=existing,
                    owner_id=uid,
                    organization_id=organization_id,
                )
                # See the sync twin above: the parent stamp is a location write
                # and goes through public.move_file, which recomputes file_path.
                await self._db.move_file_async(existing["id"], folder_id)
                file_record = {**existing, **written, "id": existing["id"]}
            else:
                file_record = await insert_file_converging_async(
                    self._db,
                    {
                        "owner_id": uid,
                        "file_path": file_path,
                        "storage_uri": storage_uri,
                        "file_name": basename(file_path),
                        "mime_type": mime,
                        "size_bytes": len(content_bytes),
                        "checksum": checksum,
                        "parent_folder_id": folder_id,
                        "organization_id": organization_id,
                    },
                    owner_id=uid,
                    organization_id=organization_id,
                )

            await self.versions.record_version_async(
                file_record, content_bytes, checksum=checksum, user_id=uid
            )

            logger.debug("Synced write: %s → %s", file_path, storage_uri)

        except Exception:
            logger.exception("Cloud sync failed for '%s'", file_path)
            raise

    def track_delete(self, file_path: str, user_id: str | None = None) -> None:
        """Soft-delete in database and optionally remove from cloud."""
        try:
            uid = self._resolve_user_id(user_id)
            existing = self._db.get_file_by_path(uid, file_path)
            if existing:
                self._db.soft_delete_file(existing["id"])
                logger.debug("Synced delete: %s", file_path)
        except Exception:
            logger.warning("Cloud sync delete failed for '%s'", file_path, exc_info=True)

    async def track_delete_async(self, file_path: str, user_id: str | None = None) -> None:
        try:
            uid = self._resolve_user_id(user_id)
            existing = await self._db.get_file_by_path_async(uid, file_path)
            if existing:
                await self._db.soft_delete_file_async(existing["id"])
                logger.debug("Synced delete: %s", file_path)
        except Exception:
            logger.warning("Cloud sync delete failed for '%s'", file_path, exc_info=True)

    def fire_and_forget_write(
        self,
        file_path: str,
        content: bytes | str | dict | list,
        mime_type: str | None = None,
        user_id: str | None = None,
    ) -> None:
        """Run track_write in a background daemon thread.

        Captures the current ContextVar context BEFORE spawning the
        thread so the worker thread sees the same active user. Without
        this, ContextVars revert to defaults inside the thread and the
        sync would write under user_id="" (H17 fix).
        """
        if user_id is None:
            user_id = self._resolve_user_id(None) or None

        import contextvars

        ctx = contextvars.copy_context()

        def _runner():
            ctx.run(self.track_write, file_path, content, mime_type=mime_type, user_id=user_id)

        t = threading.Thread(target=_runner, daemon=True)
        t.start()

    def fire_and_forget_delete(self, file_path: str, user_id: str | None = None) -> None:
        """Run track_delete in a background daemon thread.

        Same context-capture pattern as fire_and_forget_write.
        """
        if user_id is None:
            user_id = self._resolve_user_id(None) or None

        import contextvars

        ctx = contextvars.copy_context()

        def _runner():
            ctx.run(self.track_delete, file_path, user_id=user_id)

        t = threading.Thread(target=_runner, daemon=True)
        t.start()

    # ==================================================================
    # MANAGED OPERATIONS — full control with permission checks
    # ==================================================================

    def _reconcile_existing_result_sync(
        self, *, existing_row: dict, content_bytes: bytes, checksum: str | None,
        share_with: list[str] | None, share_level: str, uid: str,
        published_to_web: bool | None, shown_to: str | None, wants_anyone_link: bool,
    ) -> SyncResult:
        """Sync winner reconciliation; refuse a bucket move before side effects."""
        row = existing_row
        if published_to_web is not None and bool(row.get("published_to_web")) != bool(published_to_web):
            raise ValueError("sync managed_write cannot move storage lanes; use managed_write_async")
        if shown_to is not None and shown_to != row.get("shown_to"):
            self.permissions.require("file", row["id"], "write", uid)
            self._db.update_file(row["id"], {"shown_to": shown_to})
            row = self._db.get_file(row["id"]) or {**row, "shown_to": shown_to}
        result = self._sync_result_for_existing(
            existing_row=row, content_bytes=content_bytes, checksum=checksum,
            share_with=share_with, share_level=share_level, granter_uid=uid,
        )
        if wants_anyone_link:
            self.permissions.require("file", result.file_id, "admin", uid)
            link = self.permissions.create_share_link("file", result.file_id, permission_level="viewer", user_id=uid)
            token = str(link["token"])
            return result.model_copy(update={"share_token": token, "share_url": f"/share/{token}"})
        return result

    async def _reconcile_existing_result_async(
        self, *, existing_row: dict, content_bytes: bytes, checksum: str | None,
        share_with: list[str] | None, share_level: str, uid: str,
        published_to_web: bool | None, shown_to: str | None, wants_anyone_link: bool,
    ) -> SyncResult:
        """Apply requested access to every dedup/race winner before returning it."""
        row = existing_row
        if published_to_web is not None and bool(row.get("published_to_web")) != bool(published_to_web):
            await self.permissions.require_async("file", row["id"], "admin", uid)
            row = await self.set_published_to_web_async(row["id"], bool(published_to_web), user_id=uid)
            if row is None:
                raise RuntimeError("winner vanished while moving storage lane")
        if shown_to is not None and shown_to != row.get("shown_to"):
            await self.permissions.require_async("file", row["id"], "write", uid)
            await self._db.update_file_async(row["id"], {"shown_to": shown_to})
            row = await self._db.get_file_async(row["id"]) or row
        result = await self._sync_result_for_existing_async(
            existing_row=row, content_bytes=content_bytes, checksum=checksum,
            share_with=share_with, share_level=share_level, granter_uid=uid,
        )
        if wants_anyone_link:
            await self.permissions.require_async("file", result.file_id, "admin", uid)
            link = await self.permissions.create_share_link_async("file", result.file_id, permission_level="viewer", user_id=uid)
            token = str(link["token"])
            return result.model_copy(update={"share_token": token, "share_url": f"/share/{token}"})
        return result

    def managed_write(
        self,
        file_path: str,
        content: bytes | str | dict | list,
        *,
        mime_type: str | None = None,
        published_to_web: bool | None = None,
        shown_to: str | None = None,
        visibility: LegacyLevelInput | None = None,
        share_with: list[str] | None = None,
        share_level: str = "read",
        change_summary: str | None = None,
        user_id: str | None = None,
        metadata: dict | None = None,
    ) -> SyncResult:
        """Write a file to cloud with full metadata, versioning, and permissions.

        Unlike the auto-sync methods, this returns a ``SyncResult`` and
        raises on errors rather than swallowing them.
        """
        published_to_web, shown_to, wants_anyone_link = _legacy_write_access(
            published_to_web, shown_to, visibility
        )
        uid = self._resolve_user_id(user_id)
        content_bytes = self._to_bytes(content)
        checksum = self._checksum(content_bytes)
        # Empty content hashes to the same constant SHA-256 for
        # every caller, forever — treat it as NO checksum so it can
        # never collide with (and silently alias into) an unrelated
        # file that also happens to be empty (production defect,
        # jobs-bar cold-walk-11, 2026-09-18). checksum is nullable.
        if not content_bytes:
            checksum = None
        mime = mime_type or self._guess_mime(file_path)

        # Resolve the row before touching bytes. System-managed evidence files
        # are append-only; checking after the PUT would already have corrupted
        # the immutable object even if the metadata update were rejected.
        existing = self._db.get_file_by_path(uid, file_path)
        if existing and (existing.get("metadata") or {}).get("system_immutable"):
            raise PermissionError(
                f"system-managed immutable file cannot be overwritten: {existing['id']}"
            )
        metadata_dict = metadata or {}
        requested_org_id = self._metadata_organization_id(metadata_dict)
        if existing is not None:
            existing_org_id = existing.get("organization_id")
            if (
                requested_org_id is not None
                and existing_org_id is not None
                and str(requested_org_id) != str(existing_org_id)
            ):
                self._warn_write_organization_converges_on_existing_row(
                    file_path, existing_org_id, requested_org_id
                )
            organization_id = self._resolve_write_organization_id(
                uid,
                str(existing_org_id) if existing_org_id else requested_org_id,
            )
            self.permissions.require("file", existing["id"], "write", uid)
            if (
                published_to_web is not None
                and bool(existing.get("published_to_web")) != bool(published_to_web)
            ):
                raise ValueError(
                    "managed_write cannot change published_to_web for an existing file; "
                    "move it with set_published_to_web_async before overwriting"
                )
        else:
            organization_id = self._resolve_write_organization_id(
                uid,
                requested_org_id,
            )

        # Empty content hashes to the same constant SHA-256 (of zero bytes)
        # for every caller, forever — it carries no content to legitimately
        # dedup against, and honoring it here silently hands back whatever
        # UNRELATED file first happened to be uploaded empty in this scope
        # (production defect, jobs-bar cold-walk-11, 2026-09-18: a blank file
        # in a batch upload was silently reattached as a pre-existing,
        # completely unrelated `official-mcat-content-outline.pdf`). A
        # zero-byte root write always creates its own fresh row.
        if existing is None and content_bytes:
            dedup_existing = self._db.get_file_by_checksum(
                checksum,
                owner_id=uid,
                organization_id=organization_id,
            )
            if dedup_existing is not None:
                return self._reconcile_existing_result_sync(
                    existing_row=dedup_existing, content_bytes=content_bytes, checksum=checksum,
                    share_with=share_with, share_level=share_level, uid=uid,
                    published_to_web=published_to_web, shown_to=shown_to,
                    wants_anyone_link=wants_anyone_link,
                )

        _refuse_empty_overwrite(existing, content_bytes)
        new_file_id = str(uuid.uuid4()) if existing is None else None
        if existing is not None:
            storage_uri = (
                existing.get("canonical_storage_uri")
                or existing.get("storage_uri")
                or self._storage_uri(file_path, uid, published_to_web=bool(published_to_web))
            )
        else:
            backend = self._config.storage_backend
            # 🚨 public_bucket_or_raise, never `or resolve_s3_bucket()` — a
            # public asset in the private bucket is a lie the system tells
            # itself. See cdn.public_bucket_or_raise.
            from .cdn import public_bucket_or_raise

            bucket = (
                public_bucket_or_raise("sync_engine.write")
                if published_to_web
                else self._config.resolve_s3_bucket()
            )
            storage_uri = f"{backend}://{bucket}/{uid}/{new_file_id}"

        # Validate/resolve folder placement before touching bytes.
        folder_id = self._ensure_folder(file_path, uid, organization_id)

        # Upload to cloud — stamp Content-Type so a bare public URL renders inline.
        self._router.write(
            storage_uri,
            content_bytes,
            content_type=mime,
        )

        is_new = existing is None

        # Phase 1d.5 — stamp request_id into metadata for realtime dedup.
        effective_metadata = _stamp_request_id(
            metadata_dict or (existing.get("metadata", {}) if existing else {})
        )
        # A machine's file carries the machine-artifact marker from its path, stamped here at the
        # one door so no writer has to remember (matrx_files/user_visible.py § MACHINE-ARTIFACT).
        effective_metadata = stamp_machine_artifact(file_path, effective_metadata)

        if existing:
            new_version = existing["current_version"] + 1
            written = update_file_converging(
                self._db,
                existing["id"],
                {
                    "storage_uri": storage_uri,
                    "size_bytes": len(content_bytes),
                    "checksum": checksum,
                    "mime_type": mime,
                    "current_version": new_version,
                    **row_access_update_columns(published_to_web, shown_to, uid),
                    "parent_folder_id": folder_id,
                    "metadata": effective_metadata,
                    # See the async path above: the columns mirror the JSONB.
                    **artifact_identity_columns(effective_metadata),
                },
                current=existing,
                owner_id=uid,
                organization_id=organization_id,
            )
            file_record = {**existing, **written, "id": existing["id"]}
        else:
            insert_payload = {
                "id": new_file_id,
                "owner_id": uid,
                "file_path": file_path,
                "storage_uri": storage_uri,
                # canonical_storage_uri intentionally not written — migration
                # 007 consolidates it into storage_uri. See managed_write_async.
                "file_name": basename(file_path),
                "mime_type": mime,
                "size_bytes": len(content_bytes),
                "checksum": checksum,
                **row_access_insert_columns(published_to_web, shown_to, uid),
                "parent_folder_id": folder_id,
                "metadata": effective_metadata,
                # See the async path: artifact_kind / provider_session_id are
                # the filterable copy of the metadata identity.
                **artifact_identity_columns(effective_metadata),
                "organization_id": organization_id,
            }
            try:
                file_record = self._db.upsert_file(insert_payload)
            except Exception as insert_exc:
                try:
                    committed = self._db.get_file(
                        str(new_file_id),
                        include_deleted=True,
                    )
                except Exception:
                    # COMMIT outcome is unknown. Never delete the exact object
                    # until the generated row id can be reconciled.
                    raise
                committed_uri = (
                    committed.get("canonical_storage_uri") or committed.get("storage_uri")
                    if committed
                    else None
                )
                if committed is not None and committed_uri == storage_uri:
                    file_record = committed
                else:
                    winner: dict[str, Any] | None = None
                    if self._is_dedup_unique_violation(insert_exc):
                        winner = self._db.get_file_by_checksum(
                            checksum,
                            owner_id=uid,
                            organization_id=organization_id,
                        )
                    elif self._is_path_unique_violation(insert_exc):
                        winner = self._db.get_file_by_path(uid, file_path)

                    self._delete_orphan_or_raise(
                        storage_uri,
                        context="sync INSERT race",
                    )

                    if winner is not None and winner.get("checksum") == checksum:
                        return self._reconcile_existing_result_sync(
                            existing_row=winner, content_bytes=content_bytes, checksum=checksum,
                            share_with=share_with, share_level=share_level, uid=uid,
                            published_to_web=published_to_web, shown_to=shown_to,
                            wants_anyone_link=wants_anyone_link,
                        )
                    raise

        # Record version
        self.versions.record_version(
            file_record,
            content_bytes,
            checksum=checksum,
            change_summary=change_summary,
            user_id=uid,
        )

        # Grant permissions to shared users
        if share_with:
            for grantee_id in share_with:
                self._db.upsert_permission(
                    {
                        "resource_id": file_record["id"],
                        "resource_type": "file",
                        "grantee_id": grantee_id,
                        "grantee_type": "user",
                        "permission_level": share_level,
                        "granted_by": uid,
                    }
                )
            # Canonical sharing model: specific-user access is granted by the
            # iam.permissions rows above (RLS via iam.has_access), never by
            # publishing the file to the web. build_urls returns the durable
            # authenticated route for every unpublished file, so URLs are unaffected.

        # Build the durable URL contract via the central helper.
        synthetic = {
            "id": file_record["id"],
            "storage_uri": storage_uri,
            "published_to_web": bool(file_record.get("published_to_web", published_to_web)),
            "checksum": checksum,
            "file_name": basename(file_path),
            "mime_type": mime,
            "deleted_at": None,
        }
        urls = self.build_urls_for_record(synthetic)

        result = SyncResult(
            file_id=file_record["id"],
            file_path=file_record.get("file_path") or file_path,
            storage_uri=storage_uri,
            version_number=file_record.get("current_version", 1),
            size_bytes=len(content_bytes),
            checksum=checksum,
            is_new=is_new,
            published_to_web=bool(file_record.get("published_to_web", published_to_web)),
            shown_to=file_record.get("shown_to", shown_to),
            url=urls["url"],
            cdn_url=urls["cdn_url"],
            download_url=urls["download_url"],
            parent_file_id=file_record.get("parent_file_id"),
            derivation_kind=file_record.get("derivation_kind"),
        )
        if wants_anyone_link:
            link = self.permissions.create_share_link(
                "file", result.file_id, permission_level="viewer", user_id=uid
            )
            token = str(link["token"])
            return result.model_copy(update={"share_token": token, "share_url": f"/share/{token}"})
        return result

    @staticmethod
    def _is_dedup_unique_violation(exc: BaseException) -> bool:
        """True if ``exc`` is a Postgres 23505 on the dedup canonical index.

        Race fallback: between our checksum lookup and the INSERT, another
        concurrent write of the same content can win the canonical slot.
        The DB-level unique index (migration 0065,
        ``cld_files_dedup_canonical``) rejects the loser. Detect that
        specific case so we can recover gracefully; any other violation
        (e.g. ``owner_id, file_path`` collision) bubbles up as a real bug.
        """
        return db_sqlstate(exc) == "23505" and db_constraint(exc) == "cld_files_dedup_canonical"

    @staticmethod
    def _is_path_unique_violation(exc: BaseException) -> bool:
        """True if ``exc`` is a Postgres 23505 on the (owner_id, file_path) key.

        Race fallback for pinned-id inserts (TUS / AI media / variants):
        between our ``get_file_by_path`` lookup and the INSERT, a concurrent
        write to the SAME ``(owner_id, file_path)`` can win the slot. The
        canonical example is two variant-render passes for the same master
        (content-dedup merges two saves of identical bytes into one master,
        so both passes render ``system-files/variants/<master>/og.jpg``).
        Now that pinned-id inserts are plain inserts (never an
        ``ON CONFLICT DO UPDATE`` that would rewrite the winner's primary
        key), the loser raises this violation and recovers by reading the
        winning row — converging on one variant instead of corrupting the
        winner's id and orphaning its cld_file_versions insert (FK 23503).
        """
        return db_sqlstate(exc) == "23505" and db_constraint(exc) in _PATH_UNIQUE_CONSTRAINTS

    async def _update_file_converging_async(
        self,
        file_id: str,
        updates: dict,
        *,
        owner_id: str,
        organization_id: str | None,
    ) -> dict:
        """UPDATE a row's content, converging on the dedup canonical like an INSERT race.

        New bytes identical to ANOTHER live canonical root of the same
        (organization, owner) violate ``cld_files_dedup_canonical``. Refusing
        would lose the user's save; instead the row keeps its id, path and own
        object and becomes that canonical's alias (``duplicate_of_file_id``).
        Returns the updates actually written.
        """
        try:
            await self._db.update_file_async(file_id, updates)
            return updates
        except Exception as update_exc:
            checksum = updates.get("checksum")
            if not checksum or not self._is_dedup_unique_violation(update_exc):
                raise
            from matrx_files.dedup import lookup_existing_async

            canonical = await lookup_existing_async(
                self._db,
                checksum=checksum,
                owner_id=owner_id,
                organization_id=organization_id,
            )
            if (
                not canonical.has_duplicate
                or canonical.existing is None
                or str(canonical.existing["id"]) == str(file_id)
            ):
                raise
            converged = {**updates, "duplicate_of_file_id": str(canonical.existing["id"])}
            logger.info(
                "file %s now holds bytes identical to canonical %s; kept as its dedup alias",
                file_id,
                canonical.existing["id"],
            )
            await self._db.update_file_async(file_id, converged)
            return converged

    def _update_file_converging(
        self,
        file_id: str,
        updates: dict,
        *,
        owner_id: str,
        organization_id: str | None,
    ) -> dict:
        """Sync twin of :meth:`_update_file_converging_async`."""
        try:
            self._db.update_file(file_id, updates)
            return updates
        except Exception as update_exc:
            checksum = updates.get("checksum")
            if not checksum or not self._is_dedup_unique_violation(update_exc):
                raise
            canonical = self._db.get_file_by_checksum(
                checksum,
                owner_id=owner_id,
                organization_id=organization_id,
            )
            if canonical is None or str(canonical["id"]) == str(file_id):
                raise
            converged = {**updates, "duplicate_of_file_id": str(canonical["id"])}
            logger.info(
                "file %s now holds bytes identical to canonical %s; kept as its dedup alias",
                file_id,
                canonical["id"],
            )
            self._db.update_file(file_id, converged)
            return converged

    def _sync_result_for_existing(
        self,
        *,
        existing_row: dict,
        content_bytes: bytes,
        checksum: str,
        share_with: list[str] | None,
        share_level: str,
        granter_uid: str,
    ) -> SyncResult:
        """Sync result for a dedupe/path-race winner without a second version."""
        existing_id = str(existing_row["id"])
        if share_with:
            for grantee_id in share_with:
                self._db.upsert_permission(
                    {
                        "resource_id": existing_id,
                        "resource_type": "file",
                        "grantee_id": grantee_id,
                        "grantee_type": "user",
                        "permission_level": share_level,
                        "granted_by": granter_uid,
                    }
                )

        urls = self.build_urls_for_record(existing_row)
        storage_uri = existing_row.get("canonical_storage_uri") or existing_row.get("storage_uri")
        return SyncResult(
            file_id=existing_id,
            file_path=existing_row.get("file_path"),
            storage_uri=storage_uri,
            version_number=int(existing_row.get("current_version") or 1),
            size_bytes=len(content_bytes),
            checksum=checksum,
            is_new=False,
            published_to_web=bool(existing_row.get("published_to_web")),
            shown_to=existing_row.get("shown_to"),
            url=urls["url"],
            cdn_url=urls["cdn_url"],
            download_url=urls["download_url"],
            parent_file_id=existing_row.get("parent_file_id"),
            derivation_kind=existing_row.get("derivation_kind"),
        )

    async def _sync_result_for_existing_async(
        self,
        *,
        existing_row: dict,
        content_bytes: bytes,
        checksum: str,
        share_with: list[str] | None,
        share_level: str,
        granter_uid: str,
    ) -> SyncResult:
        """Build a SyncResult for an already-canonical row (dedup hit).

        No bytes are written to S3; the existing storage_uri is reused
        verbatim. Caller-supplied ``share_with`` grants are still applied
        so a caller that expected "upload + share with X" still gets the
        share. Bytes are pushed into the in-process byte cache so the
        typical "upload then immediately use" flow doesn't refetch from
        S3 — they're in hand right now.
        """
        existing_id = str(existing_row["id"])

        if share_with:
            for grantee_id in share_with:
                await self._db.upsert_permission_async(
                    {
                        "resource_id": existing_id,
                        "resource_type": "file",
                        "grantee_id": grantee_id,
                        "grantee_type": "user",
                        "permission_level": share_level,
                        "granted_by": granter_uid,
                    }
                )
            # Specific-user access comes from the iam.permissions rows above
            # (RLS via iam.has_access); the web lane stays as-is.

        urls = await self.build_urls_for_record_async(existing_row)

        try:
            from matrx_files.cloud_sync.byte_cache import get_byte_cache

            get_byte_cache().put(
                existing_id,
                bytes_=content_bytes,
                mime_type=existing_row.get("mime_type"),
                owner_id=str(existing_row.get("owner_id") or granter_uid),
                file_path=existing_row.get("file_path"),
            )
        except Exception:
            logger.debug("byte cache populate failed (dedup alias)", exc_info=True)

        storage_uri = existing_row.get("canonical_storage_uri") or existing_row.get("storage_uri")
        return SyncResult(
            file_id=existing_id,
            file_path=existing_row.get("file_path"),
            storage_uri=storage_uri,
            version_number=int(existing_row.get("current_version") or 1),
            size_bytes=len(content_bytes),
            checksum=checksum,
            is_new=False,
            published_to_web=bool(existing_row.get("published_to_web")),
            shown_to=existing_row.get("shown_to"),
            url=urls["url"],
            cdn_url=urls["cdn_url"],
            download_url=urls["download_url"],
            parent_file_id=existing_row.get("parent_file_id"),
            derivation_kind=existing_row.get("derivation_kind"),
        )

    async def managed_write_async(
        self,
        file_path: str,
        content: bytes | str | dict | list,
        *,
        mime_type: str | None = None,
        published_to_web: bool | None = None,
        shown_to: str | None = None,
        visibility: LegacyLevelInput | None = None,
        share_with: list[str] | None = None,
        share_level: str = "read",
        change_summary: str | None = None,
        user_id: str | None = None,
        metadata: dict | None = None,
        organization_id: str | None = None,
        file_id: str | None = None,
        parent_file_id: str | None = None,
        derivation_kind: str | None = None,
        derivation_metadata: dict[str, Any] | None = None,
        duplicate_of_file_id: str | None = None,
        create_only: bool = False,
        origin_device_id: str | None = None,
        client_modified_at: datetime | None = None,
        exact_folder_organization: bool = False,
    ) -> SyncResult:
        """Async version of managed_write().

        Every folder on the path is the file's organization's own (created there when missing);
        another organization's folder at the same path is never used.
        ``exact_folder_organization`` is accepted for existing callers; placement is always exact.

        When ``file_id`` is supplied the row id AND the S3 key are pinned
        to that UUID — the S3 key becomes ``<owner_id>/<file_id>`` (the
        canonical scheme) instead of ``<owner_id>/<file_path>``. This
        skips the legacy-then-rekey dance entirely: ``storage_uri`` and
        ``canonical_storage_uri`` both equal the canonical URI from day
        one, and any URL minted from the row carries the file_id in its
        path. Use this when the caller already owns a stable file_id
        (TUS, AI-generated media, anything fresh) — leave ``file_id``
        unset for the legacy path-based scheme (back-compat for routes
        that update an existing row by ``(owner_id, file_path)``).

        Dedup (Phase 1, migration 0065): brand-new ROOT inserts
        (no existing row at this ``file_path``, no ``parent_file_id``)
        consult the content-hash dedup table first. A scope-matching
        hit short-circuits — no S3 write, no INSERT, returns the
        canonical row's SyncResult with ``is_new=False``. Implicit
        alias_existing semantics for back-compat with the thousands of
        legacy callers; the strict-intent variants (create / force_new)
        live on ``FileService.upload_with_intent``. Derivative writes
        (parent_file_id set) skip dedup — variants of the same master
        are intentionally separate rows.
        """
        published_to_web, shown_to, wants_anyone_link = _legacy_write_access(
            published_to_web, shown_to, visibility
        )
        uid = self._resolve_user_id(user_id)
        metadata_dict = metadata or {}
        lineage = resolve_file_lineage(
            parent_file_id=parent_file_id,
            derivation_kind=derivation_kind,
            metadata=metadata_dict,
        )
        parent_file_id = lineage.parent_file_id
        derivation_kind = (
            lineage.derivation_kind.value if lineage.derivation_kind is not None else None
        )
        metadata_duplicate_id = metadata_dict.get("duplicate_of_file_id")
        if (
            duplicate_of_file_id is not None
            and metadata_duplicate_id is not None
            and str(duplicate_of_file_id) != str(metadata_duplicate_id)
        ):
            raise ValueError(
                "Conflicting duplicate_of_file_id values in write arguments and metadata"
            )
        if duplicate_of_file_id is None and metadata_duplicate_id is not None:
            duplicate_of_file_id = str(metadata_duplicate_id)

        # A parent conveys derivation/provenance and therefore requires normal
        # read access. A duplicate target is different: it conveys only byte
        # equivalence, and is validated below by the stricter same-owner,
        # same-organization, identical-checksum canonical-root contract.
        #
        # Requiring contextual read access for duplicate_of_file_id made fresh
        # evidence artifacts impossible to copy before their enclosing domain
        # row existed. Callers then worked around that denial by deleting the
        # supposedly "orphaned" target, which could delete an earlier artifact
        # from the same in-progress capture.
        referenced_parent_ids = {
            str(file_id) for file_id in (parent_file_id,) if file_id is not None
        }
        for referenced_file_id in referenced_parent_ids:
            await self.permissions.require_async(
                "file",
                referenced_file_id,
                "read",
                uid,
            )
        content_bytes = self._to_bytes(content)
        checksum = await self._checksum_async(content_bytes)
        # Empty content hashes to the same constant SHA-256 for
        # every caller, forever — treat it as NO checksum so it can
        # never collide with (and silently alias into) an unrelated
        # file that also happens to be empty (production defect,
        # jobs-bar cold-walk-11, 2026-09-18). checksum is nullable.
        if not content_bytes:
            checksum = None
        mime = mime_type or self._guess_mime(file_path)

        # Path-keyed lookup: preserves the legacy "save over an existing
        # file at this path" semantics (new version, in-place update).
        # Has to come BEFORE the dedup check so a caller updating a file
        # with the same content as another file in the scope doesn't get
        # silently redirected to that other file.
        existing = await self._db.get_file_by_path_async(uid, file_path)
        is_new = existing is None
        if existing and (existing.get("metadata") or {}).get("system_immutable"):
            raise PermissionError(
                f"system-managed immutable file cannot be overwritten: {existing['id']}"
            )
        _refuse_empty_overwrite(existing, content_bytes)

        # Content-hash dedup short-circuit — runs only for brand-new
        # ROOT inserts. Derivatives bypass: variants of the same master
        # can legitimately share a checksum (asset variant thumbnails are
        # byte-identical when source images are identical; rendered
        # blank pages from different PDFs are byte-identical), and the
        # lineage contract depends on getting a FRESH row id back from
        # the write.
        #
        # Only a validated parent or canonical duplicate target bypasses root
        # dedupe. A caller-controlled derivation_kind alone remains a root and
        # cannot opt out. resolve_file_lineage() promotes legacy metadata into
        # the canonical columns before any storage or DB work.
        # Resolve one authorized organization before lookup, folder creation,
        # and insert. Metadata may request a placement but never grants it.
        # ``organization_id=`` is the EXPLICIT thread from the API edge and is
        # read BEFORE the metadata dict on purpose: a caller that resolved the
        # organization once, at the edge, from the admitted request must never
        # depend on some intermediate layer having remembered to copy it into a
        # metadata dict (production outage 2026-09-19 — see
        # ``matrx_files/request_organization.py``).
        requested_org_id = organization_id or self._metadata_organization_id(metadata_dict)
        existing, file_path = await self._free_path_when_row_is_in_unreachable_org_async(
            uid, file_path, existing, requested_org_id
        )
        is_new = existing is None
        if existing is not None:
            existing_org_id = existing.get("organization_id")
            if (
                requested_org_id is not None
                and existing_org_id is not None
                and str(requested_org_id) != str(existing_org_id)
            ):
                self._warn_write_organization_converges_on_existing_row(
                    file_path, existing_org_id, requested_org_id
                )
            org_id_for_dedup = await self._resolve_write_organization_id_async(
                uid,
                str(existing_org_id) if existing_org_id else requested_org_id,
            )
        else:
            org_id_for_dedup = await self._resolve_write_organization_id_async(
                uid,
                requested_org_id,
            )
        if duplicate_of_file_id is not None:
            await self._validate_duplicate_target_async(
                user_id=uid,
                organization_id=org_id_for_dedup,
                duplicate_of_file_id=duplicate_of_file_id,
                checksum=checksum,
            )
        if existing is not None:
            if create_only:
                from matrx_files.dedup import FilePathConflictError

                raise FilePathConflictError(file_path=file_path)
            await self.permissions.require_async("file", existing["id"], "write", uid)
            if (
                published_to_web is not None
                and bool(existing.get("published_to_web")) != bool(published_to_web)
            ):
                await self.permissions.require_async("file", existing["id"], "admin", uid)
                await self.set_published_to_web_async(
                    str(existing["id"]), bool(published_to_web), user_id=uid
                )
                existing = await self._db.get_file_by_path_async(uid, file_path)
                if existing is None:
                    raise RuntimeError(
                        "file vanished while moving its storage lane before overwrite"
                    )
        is_derivative_write = parent_file_id is not None or duplicate_of_file_id is not None
        # Empty content hashes to the same constant SHA-256 (of zero bytes)
        # for every caller, forever — it carries no content to legitimately
        # dedup against, and honoring it here silently hands back whatever
        # UNRELATED file first happened to be uploaded empty in this scope
        # (production defect, jobs-bar cold-walk-11, 2026-09-18: a blank file
        # in a batch upload was silently reattached as a pre-existing,
        # completely unrelated `official-mcat-content-outline.pdf`). A
        # zero-byte root write always creates its own fresh row. See the
        # sync twin above.
        if is_new and not is_derivative_write and checksum and content_bytes:
            from matrx_files.dedup import lookup_existing_async

            dedup_lookup = await lookup_existing_async(
                self._db,
                checksum=checksum,
                owner_id=uid,
                organization_id=org_id_for_dedup,
            )
            if dedup_lookup.has_duplicate and dedup_lookup.existing is not None:
                return await self._reconcile_existing_result_async(
                    existing_row=dedup_lookup.existing, content_bytes=content_bytes, checksum=checksum,
                    share_with=share_with, share_level=share_level, uid=uid,
                    published_to_web=published_to_web, shown_to=shown_to,
                    wants_anyone_link=wants_anyone_link,
                )

        # Resolve the canonical row id / S3 key.
        #   - caller-supplied file_id  → pin to it (TUS, AI media).
        #   - brand-new insert (is_new) → mint a fresh UUID and use the
        #     canonical <owner>/<file_id> key. CRITICAL (P0-2): the old
        #     path-derived key <owner>/<file_path> let two concurrent NEW
        #     uploads to the SAME path target the SAME S3 object — the
        #     second PUT overwrote the first's bytes, then lost the
        #     (owner_id, file_path) INSERT race, leaving the first row
        #     pointing at the second's bytes (silent corruption). A
        #     per-write UUID key makes every concurrent writer target a
        #     distinct object; the loser's INSERT still fails cleanly and
        #     its orphan object is cleaned up below.
        #   - existing-version update  → keep the legacy path-derived key
        #     so in-place version overwrites keep their established URI.
        effective_file_id: str | None
        if file_id is not None:
            effective_file_id = file_id
        elif is_new:
            effective_file_id = str(uuid.uuid4())
        else:
            effective_file_id = None

        if effective_file_id is not None:
            backend = self._config.storage_backend
            # 🚨 public_bucket_or_raise, never `or resolve_s3_bucket()` — a
            # public asset in the private bucket is a lie the system tells
            # itself. See cdn.public_bucket_or_raise.
            from .cdn import public_bucket_or_raise

            bucket = (
                public_bucket_or_raise("sync_engine.write")
                if published_to_web
                else self._config.resolve_s3_bucket()
            )
            storage_uri = f"{backend}://{bucket}/{uid}/{effective_file_id}"
        else:
            # Version update of an existing row (existing is not None here):
            # overwrite the SAME object the row already references. Do NOT
            # recompute a path key — the row may have been created with a
            # canonical <owner>/<file_id> key, and recomputing would rekey it
            # to a path key, orphaning the canonical object and churning the URI.
            storage_uri = (
                existing.get("canonical_storage_uri")
                or existing.get("storage_uri")
                or self._storage_uri(file_path, uid, published_to_web=bool(published_to_web))
            )

        # Validate/resolve folder placement before touching bytes: the folder chain is the
        # file's own organization's (a person's folder tree is per organization).
        folder_id = await self._ensure_folder_async(
            file_path, uid, org_id_for_dedup, exact=exact_folder_organization
        )

        # mime computed above (mime_type or guessed). Stamp it onto the object so
        # the canonical extensionless <owner>/<file_id> key still renders inline.
        await self._router.write_async(storage_uri, content_bytes, content_type=mime)

        # Phase 1d.5 — stamp the inbound request_id into metadata so the
        # FE's realtime echo carries the round-trip id back for dedup.
        # Caller-supplied metadata.request_id wins. See _stamp_request_id.
        effective_metadata = _stamp_request_id(
            metadata or existing.get("metadata", {}) if existing else metadata
        )
        # A machine's file carries the machine-artifact marker from its path, stamped here at the
        # one door so no writer has to remember (matrx_files/user_visible.py § MACHINE-ARTIFACT).
        effective_metadata = stamp_machine_artifact(file_path, effective_metadata)

        if existing:
            new_version = existing["current_version"] + 1
            written = await update_file_converging_async(
                self._db,
                existing["id"],
                {
                    "storage_uri": storage_uri,
                    "size_bytes": len(content_bytes),
                    "checksum": checksum,
                    "mime_type": mime,
                    "current_version": new_version,
                    **row_access_update_columns(published_to_web, shown_to, uid),
                    "parent_folder_id": folder_id,
                    "metadata": effective_metadata,
                    # The filterable copy of this row's produced-artifact
                    # identity, derived from the metadata being written — see
                    # matrx_files/artifact_identity.py. On an update too,
                    # because the columns must never disagree with the JSONB
                    # they mirror.
                    **artifact_identity_columns(effective_metadata),
                    # Device provenance (SPEC-SERVER §2.2). Written on EVERY
                    # write, including an update: the feed entry must say which
                    # device produced the version a replica is now looking at,
                    # or a daemon cannot tell its own echo from someone else's
                    # change. Both are pre-validated (device belongs to this
                    # caller; clock is not absurd) -- see device_writes.py.
                    "origin_device_id": origin_device_id,
                    "client_modified_at": client_modified_at,
                },
                current=existing,
                owner_id=uid,
                organization_id=org_id_for_dedup,
            )
            file_record = {**existing, **written, "id": existing["id"]}
        else:
            insert_payload = {
                "owner_id": uid,
                "file_path": file_path,
                "storage_uri": storage_uri,
                "file_name": basename(file_path),
                "mime_type": mime,
                "size_bytes": len(content_bytes),
                "checksum": checksum,
                **row_access_insert_columns(published_to_web, shown_to, uid),
                "parent_folder_id": folder_id,
                "metadata": effective_metadata,
                # The filterable copy of this row's produced-artifact identity
                # (artifact_kind / provider_session_id), derived from the
                # metadata being written — matrx_files/artifact_identity.py.
                # This is the ONE door, so the placement-alias rows a dedup'd
                # upload creates (duplicate_of_file_id) are stamped here too.
                **artifact_identity_columns(effective_metadata),
                # K0-1: stamp the validated explicit org or personal-org default
                # so every file participates in the Knowledge/Scope system.
                "organization_id": org_id_for_dedup,
                # Device provenance (SPEC-SERVER §2.2); NULL means "not written
                # by a registered device" -- a browser upload, or a pre-2026-09-13
                # row. The engine treats NULL as "not mine" and applies the change.
                "origin_device_id": origin_device_id,
                "client_modified_at": client_modified_at,
            }
            # Phase 1d.3 — lineage columns must be settable at insert time
            # (e.g. variants set parent_file_id=master_id +
            # derivation_kind='variant') so consumers can identify
            # derived rows by data shape without inspecting metadata.
            if parent_file_id is not None:
                insert_payload["parent_file_id"] = parent_file_id
            if derivation_kind is not None:
                insert_payload["derivation_kind"] = derivation_kind
            if derivation_metadata is not None:
                insert_payload["derivation_metadata"] = derivation_metadata
            if duplicate_of_file_id is not None:
                insert_payload["duplicate_of_file_id"] = duplicate_of_file_id
            if effective_file_id is not None:
                # Pin the row id to the canonical UUID (caller-owned for
                # file_id writes, or the freshly-minted one for new inserts)
                # so row id == S3 key uuid. See P0-2 note above.
                insert_payload["id"] = effective_file_id
            # NOTE: we no longer write canonical_storage_uri. Migration 007
            # consolidates it INTO storage_uri (rename), making storage_uri
            # the single authoritative URI. A fresh insert's storage_uri is
            # already that URI, so there is nothing else to set. Readers use
            # `record.get("canonical_storage_uri") or record["storage_uri"]`,
            # which resolves correctly before AND after 007.
            insert_cancelled = False
            insert_exc: Exception | None = None
            insert_task = asyncio.create_task(self._db.upsert_file_async(insert_payload))
            try:
                file_record = await asyncio.shield(insert_task)
            except asyncio.CancelledError:
                # A canceled database request may still COMMIT. Observe the
                # actual terminal result before deciding whether this
                # UUID-key object is referenced or safe to compensate.
                insert_cancelled = True
                try:
                    file_record = await insert_task
                except Exception as exc:
                    insert_exc = exc
            except Exception as exc:
                insert_exc = exc

            if insert_exc is not None:
                try:
                    committed = await self._db.get_file_async(
                        str(effective_file_id),
                        include_deleted=True,
                    )
                except Exception:
                    # COMMIT outcome is unknown. Preserve the exact UUID-key
                    # object for a later reconciliation instead of corrupting
                    # a possibly committed row.
                    raise
                committed_uri = (
                    committed.get("canonical_storage_uri") or committed.get("storage_uri")
                    if committed
                    else None
                )
                if committed is not None and committed_uri == storage_uri:
                    file_record = committed
                else:
                    # Race: a concurrent write of the same content won the
                    # canonical slot between our dedup lookup and this INSERT.
                    # Recover by re-querying for the winner; delete the orphan
                    # S3 object we just PUT. Re-raise anything else.
                    #
                    # Only applies to root inserts (derivatives are excluded
                    # by the dedup-canonical index predicate, so they cannot
                    # violate it).
                    if (
                        not is_derivative_write
                        and checksum
                        and self._is_dedup_unique_violation(insert_exc)
                    ):
                        from matrx_files.dedup import lookup_existing_async

                        winner_lookup = await lookup_existing_async(
                            self._db,
                            checksum=checksum,
                            owner_id=uid,
                            organization_id=org_id_for_dedup,
                        )
                        if winner_lookup.has_duplicate and winner_lookup.existing is not None:
                            await self._delete_orphan_or_raise_async(
                                storage_uri,
                                context="async dedup race",
                            )
                            recovered = await self._reconcile_existing_result_async(
                                existing_row=winner_lookup.existing, content_bytes=content_bytes,
                                checksum=checksum, share_with=share_with, share_level=share_level,
                                uid=uid, published_to_web=published_to_web, shown_to=shown_to,
                                wants_anyone_link=wants_anyone_link,
                            )
                            if insert_cancelled:
                                raise asyncio.CancelledError
                            return recovered
                    # Path-unique race: a concurrent pinned-id insert won the
                    # (owner_id, file_path) slot between our lookup and this
                    # INSERT. Recover only when byte identity also matches.
                    if self._is_path_unique_violation(insert_exc):
                        winner = await self._db.get_file_by_path_async(uid, file_path)
                        if winner is not None:
                            await self._delete_orphan_or_raise_async(
                                storage_uri,
                                context="async path collision",
                            )
                            if winner.get("checksum") != checksum:
                                if create_only:
                                    from matrx_files.dedup import FilePathConflictError

                                    raise FilePathConflictError(file_path=file_path) from insert_exc
                                raise insert_exc
                            recovered = await self._reconcile_existing_result_async(
                                existing_row=winner, content_bytes=content_bytes, checksum=checksum,
                                share_with=share_with, share_level=share_level, uid=uid,
                                published_to_web=published_to_web, shown_to=shown_to,
                                wants_anyone_link=wants_anyone_link,
                            )
                            if insert_cancelled:
                                raise asyncio.CancelledError
                            return recovered
                    try:
                        await self._delete_orphan_or_raise_async(
                            storage_uri,
                            context="async INSERT failure",
                        )
                    except OrphanCleanupError as cleanup_exc:
                        raise cleanup_exc from insert_exc
                    raise insert_exc

        await self.versions.record_version_async(
            file_record,
            content_bytes,
            checksum=checksum,
            change_summary=change_summary,
            user_id=uid,
        )

        if share_with:
            for grantee_id in share_with:
                await self._db.upsert_permission_async(
                    {
                        "resource_id": file_record["id"],
                        "resource_type": "file",
                        "grantee_id": grantee_id,
                        "grantee_type": "user",
                        "permission_level": share_level,
                        "granted_by": uid,
                    }
                )
            # Specific-user access comes from the iam.permissions rows above
            # (RLS via iam.has_access), never by publishing to the web. build_urls
            # returns the durable authenticated route for unpublished files.

        # Build the durable URL contract via the central helper.
        synthetic = {
            "id": file_record["id"],
            "storage_uri": storage_uri,
            "published_to_web": bool(file_record.get("published_to_web", published_to_web)),
            "checksum": checksum,
            "file_name": basename(file_path),
            "mime_type": mime,
            "deleted_at": None,
        }
        urls = await self.build_urls_for_record_async(synthetic)

        # Populate the in-process byte cache so the typical
        # "upload then immediately submit AI request" flow doesn't have to
        # re-fetch from S3. The bytes are in hand right now — cache them.
        # Failure here is non-fatal (cache is best-effort).
        try:
            from matrx_files.cloud_sync.byte_cache import get_byte_cache

            get_byte_cache().put(
                file_record["id"],
                bytes_=content_bytes,
                mime_type=mime,
                owner_id=uid,
                file_path=file_path,
                version=file_record.get("current_version"),
            )
        except Exception:
            logger.debug("byte cache populate failed", exc_info=True)

        if not existing and insert_cancelled:
            raise asyncio.CancelledError

        result = SyncResult(
            file_id=file_record["id"],
            file_path=file_record.get("file_path") or file_path,
            storage_uri=storage_uri,
            version_number=file_record.get("current_version", 1),
            size_bytes=len(content_bytes),
            checksum=checksum,
            is_new=is_new,
            published_to_web=bool(file_record.get("published_to_web", published_to_web)),
            shown_to=file_record.get("shown_to", shown_to),
            url=urls["url"],
            cdn_url=urls["cdn_url"],
            download_url=urls["download_url"],
            parent_file_id=file_record.get("parent_file_id"),
            derivation_kind=file_record.get("derivation_kind"),
        )
        if wants_anyone_link:
            link = await self.permissions.create_share_link_async(
                "file", result.file_id, permission_level="viewer", user_id=uid
            )
            token = str(link["token"])
            return result.model_copy(update={"share_token": token, "share_url": f"/share/{token}"})
        return result

    # ==================================================================
    # IN-PLACE REPLACE BY FILE_ID
    # ==================================================================
    #
    # Why this exists separately from ``managed_write_async``:
    #
    # ``managed_write_async`` is keyed by ``(owner_id, file_path)`` — it
    # cannot update a row owned by someone else even when the caller has
    # an explicit write grant, because its initial lookup filters by
    # ``owner_id``. ``replace_file_async`` is keyed by ``file_id`` and
    # honors share-grants via PermissionsManager. It is the right
    # primitive for "transform a file and write the result back" flows
    # (compress, redact, AI-edit, collaborative document apps, etc.).
    # ==================================================================

    async def replace_file_async(
        self,
        file_id: str,
        content: bytes | str | dict | list,
        *,
        user_id: str,
        change_summary: str | None = None,
        mime_type: str | None = None,
        metadata_patch: dict | None = None,
        new_file_name: str | None = None,
    ) -> SyncResult:
        """Replace the contents of an existing cld_files row in place.

        Bumps ``current_version`` on the file row, archives the new bytes
        into ``cld_file_versions`` (so the prior version is restorable
        via ``versions.restore_version_async``), and updates the row's
        size / checksum / mime / metadata in one flow.

        ``metadata_patch`` is shallow-merged into the existing metadata
        JSONB. Pass ``{}`` (not None) to overwrite with an empty dict.

        ``new_file_name`` renames the row THROUGH ``public.rename_file``, so
        ``file_path`` is recomputed with it and the two can never disagree.
        The storage URI is unchanged — identity is the row id, not the path —
        so existing references keep working. Use for things like prefixing
        "optimized_" after a compression replace.
        """
        existing = await self._db.get_file_async(file_id)
        if not existing:
            raise ValueError(f"File '{file_id}' not found or soft-deleted.")
        if (existing.get("metadata") or {}).get("system_immutable"):
            raise PermissionError(f"system-managed immutable file cannot be replaced: {file_id}")

        await self.permissions.require_async("file", file_id, "write", user_id)

        content_bytes = self._to_bytes(content)
        _refuse_empty_overwrite(existing, content_bytes)
        storage_uri = existing["storage_uri"]

        await self._router.write_async(
            storage_uri,
            content_bytes,
            content_type=mime_type
            or existing.get("mime_type")
            or self._guess_mime(existing["file_path"]),
        )

        checksum = await self._checksum_async(content_bytes)
        # Empty content hashes to the same constant SHA-256 for
        # every caller, forever — treat it as NO checksum so it can
        # never collide with (and silently alias into) an unrelated
        # file that also happens to be empty (production defect,
        # jobs-bar cold-walk-11, 2026-09-18). checksum is nullable.
        if not content_bytes:
            checksum = None
        mime = mime_type or existing.get("mime_type") or self._guess_mime(existing["file_path"])
        new_version = existing["current_version"] + 1

        updates: dict = {
            "size_bytes": len(content_bytes),
            "checksum": checksum,
            "mime_type": mime,
            "current_version": new_version,
        }
        # Phase 1d.5 — always stamp request_id on metadata; merge with the
        # caller's patch + the existing row's metadata so the round-trip
        # FE dedup works for in-place replace operations too.
        base_meta = existing.get("metadata") or {}
        merged_meta = {**base_meta, **(metadata_patch or {})}
        updates["metadata"] = _stamp_request_id(merged_meta)

        # 🚨 A RENAME GOES THROUGH THE RENAME PRIMITIVE, AND IN THE SAME
        # TRANSACTION AS THE CONTENT WRITE. The rename used to be one more line
        # in the `updates` dict above -- `updates["file_name"] = new_file_name`
        # -- written straight through update_file_async with NO recomputation of
        # `file_path`: exactly the shape migration 031 had to repair (22 rows
        # whose file_name disagreed with the basename of their own file_path,
        # which is half the unique key AND what every replica holds on disk).
        #
        # The first fix made it two statements, and the re-verify named the new
        # hazard: public.rename_file raises 23505 on a name collision, and by
        # then the content/metadata half had already committed -- the caller got
        # a 409 on a row that was half written, with new bytes under the old
        # name. One transaction, so the collision rolls the whole replace back.
        from matrx_orm import transaction

        async with transaction(database=self._db._db_name()):
            updates = await update_file_converging_async(
                self._db,
                file_id,
                updates,
                current=existing,
                owner_id=str(existing.get("owner_id") or user_id),
                organization_id=existing.get("organization_id"),
            )
            if new_file_name is not None:
                receipt = await self._db.rename_file_async(file_id, new_file_name)
                updates["file_name"] = receipt["file_name"]
                updates["file_path"] = receipt["new_path"]

        file_record = {
            **existing,
            **updates,
            "id": file_id,
        }

        await self.versions.record_version_async(
            file_record,
            content_bytes,
            checksum=checksum,
            change_summary=change_summary,
            user_id=user_id,
        )

        try:
            from matrx_files.cloud_sync.byte_cache import get_byte_cache

            get_byte_cache().invalidate(file_id)
            get_byte_cache().put(
                file_id,
                bytes_=content_bytes,
                mime_type=mime,
                owner_id=existing["owner_id"],
                file_path=existing["file_path"],
                version=new_version,
            )
        except Exception:
            logger.debug("byte cache update failed on replace", exc_info=True)

        # Mint URL flavours via the central helper — same contract as
        # managed_write_async. The replaced file_id keeps its web lane
        # and file_name from the existing row.
        synthetic = {
            "id": existing["id"],
            "storage_uri": storage_uri,
            "published_to_web": bool(existing.get("published_to_web")),
            "checksum": checksum,
            "file_name": file_record.get("file_name") or basename(existing["file_path"]),
            "mime_type": mime,
            "deleted_at": None,
        }
        urls = await self.build_urls_for_record_async(synthetic)

        return SyncResult(
            file_id=file_id,
            file_path=existing.get("file_path"),
            storage_uri=storage_uri,
            version_number=new_version,
            size_bytes=len(content_bytes),
            checksum=checksum,
            is_new=False,
            published_to_web=synthetic["published_to_web"],
            shown_to=existing.get("shown_to"),
            url=urls["url"],
            cdn_url=urls["cdn_url"],
            download_url=urls["download_url"],
            parent_file_id=existing.get("parent_file_id"),
            derivation_kind=existing.get("derivation_kind"),
        )

    # ==================================================================
    # PUBLISH TO THE WEB — moves the object between the public and private buckets
    # ==================================================================

    async def set_published_to_web_async(
        self,
        file_id: str,
        published: bool,
        *,
        user_id: str | None = None,
    ) -> dict | None:
        """Publish a file to the web (or take it off) AND move its bytes to the matching bucket.

        ``published_to_web`` is the only anonymous lane (access ladder T-13); a published
        file's bytes live in the public bucket behind the CDN, an unpublished file's in the
        private bucket.

        Steps:
          1. Load the files row.
          2. Unchanged → no-op (return record).
          3. Swap only the bucket of the stored key.
          4. Server-side S3 copy old → new (no download).
          5. Update the row (storage_uri + published_to_web and its stamps).
          6. Delete the old object; purge the old CDN URL.

        Either the new URI exists and the row points at it, or the old URI is intact and
        the error surfaces.
        """
        record = await self._db.get_file_async(file_id)
        if not record:
            return None
        if (record.get("metadata") or {}).get("system_immutable"):
            raise PermissionError(
                f"system-managed immutable file cannot be published or unpublished: {file_id}"
            )
        was_published = bool(record.get("published_to_web"))
        if was_published == bool(published):
            return record

        uid = self._resolve_user_id(user_id) or None
        columns = publish_columns(published, uid)
        old_uri = record["storage_uri"]
        # Rekey-safe: preserve the OLD URI's key (everything after the bucket) and swap
        # ONLY the bucket. 🚨 Publishing must land the bytes in the public bucket or fail
        # (public_bucket_or_raise) — a row saying "published" over private bytes is the
        # worst version of the bug, because the person explicitly asked to publish.
        from .cdn import public_bucket_or_raise

        try:
            scheme, rest = old_uri.split("://", 1)
        except ValueError:
            scheme, rest = "s3", old_uri
        old_bucket, _, key = rest.partition("/")
        if published:
            target_bucket = public_bucket_or_raise("set_published_to_web")
        else:
            target_bucket = self._config.resolve_s3_bucket()
        new_uri = f"{scheme}://{target_bucket}/{key}" if key else old_uri
        if new_uri == old_uri:
            await self._db.update_file_async(file_id, columns)
            return await self._db.get_file_async(file_id)

        # Stage 1: copy the bytes BEFORE touching anything else.
        await self._router.copy_async(old_uri, new_uri)

        # Stage 2: point the row at the new URI.
        await self._db.update_file_async(file_id, {"storage_uri": new_uri, **columns})

        # Stage 3: delete the old object (an orphan here is a lifecycle chore, the row is right).
        try:
            await self._router.delete_async(old_uri)
        except Exception:
            logger.warning(
                "set_published_to_web_async: orphaned old key %s after move",
                old_uri,
                exc_info=True,
            )

        # Stage 4: purge the CDN URL cached against the OLD storage URI (no-op unless wired).
        try:
            from matrx_utils.conf import get_cdn_purger

            purger = get_cdn_purger()
            if purger is not None:
                from .cdn import public_url_for

                old_cdn_url = public_url_for(
                    {
                        "published_to_web": was_published,
                        "storage_uri": old_uri,
                        "checksum": record.get("checksum"),
                        "deleted_at": None,
                    }
                )
                if old_cdn_url:
                    purger([old_cdn_url])
        except Exception:
            logger.debug("CDN purge dispatch failed", exc_info=True)

        return await self._db.get_file_async(file_id)

    async def change_visibility_async(
        self, file_id: str, visibility: LegacyLevelInput, *, user_id: str | None = None
    ) -> dict | None:
        """Compatibility door for retiring visibility mutations.

        Public/private transitions delegate to the bucket-moving primitive;
        ``link`` creates a usable Anyone-link token without publishing bytes.
        """
        uid = self._resolve_user_id(user_id)
        record = await self._db.get_file_async(file_id)
        if record is None:
            return None
        if (record.get("metadata") or {}).get("system_immutable"):
            raise PermissionError(f"system-managed immutable file visibility cannot change: {file_id}")
        await self.permissions.require_async("file", file_id, "admin", uid)
        published, shown_to, wants_anyone_link = _legacy_write_access(None, None, visibility)
        if published is not None and bool(record.get("published_to_web")) != published:
            record = await self.set_published_to_web_async(file_id, published, user_id=uid)
            if record is None:
                return None
        if shown_to is not None:
            await self._db.update_file_async(file_id, {"shown_to": shown_to})
            record = await self._db.get_file_async(file_id)
        if wants_anyone_link:
            link = await self.permissions.create_share_link_async(
                "file", file_id, permission_level="viewer", user_id=uid
            )
            return {**(record or {}), "share_token": link["token"], "share_url": f"/share/{link['token']}"}
        return record

    def managed_read(
        self,
        file_path: str,
        *,
        user_id: str | None = None,
        version: int | None = None,
    ) -> bytes:
        """Read a file from cloud, checking permissions.

        If *version* is given, reads that specific version.
        Raises PermissionError if the user lacks read access.
        """
        uid = self._resolve_user_id(user_id)
        file_record = self._db.get_file_by_path(uid, file_path)

        if not file_record:
            # Try to find a file shared with this user
            # (owned by someone else but shared via permissions)
            raise FileNotFoundError(f"File '{file_path}' not found for user '{uid}'.")

        self.permissions.require("file", file_record["id"], "read", uid)

        if version is not None:
            content = self.versions.read_version(file_record["id"], version)
            if content is None:
                raise ValueError(f"Version {version} not found for '{file_path}'.")
            return content

        return self._router.read(file_record["storage_uri"])

    async def managed_read_async(
        self,
        file_path: str,
        *,
        user_id: str | None = None,
        version: int | None = None,
    ) -> bytes:
        """Async version of managed_read()."""
        uid = self._resolve_user_id(user_id)
        file_record = await self._db.get_file_by_path_async(uid, file_path)

        if not file_record:
            raise FileNotFoundError(f"File '{file_path}' not found for user '{uid}'.")

        await self.permissions.require_async("file", file_record["id"], "read", uid)

        if version is not None:
            content = await self.versions.read_version_async(file_record["id"], version)
            if content is None:
                raise ValueError(f"Version {version} not found for '{file_path}'.")
            return content

        return await self._router.read_async(file_record["storage_uri"])

    async def reconcile_missing_object_async(
        self,
        file_path: str,
        *,
        user_id: str | None = None,
    ) -> bool:
        """Hide a live metadata row after storage definitively reports it missing.

        A missing backing object is not a transient read failure: leaving the row
        active makes every list/open cycle advertise a file that can never load.
        Soft-delete keeps the metadata recoverable and preserves its storage claim
        for reconciliation while removing the broken entry from normal file views.
        """
        uid = self._resolve_user_id(user_id)
        file_record = await self._db.get_file_by_path_async(uid, file_path)
        if not file_record:
            return False

        await self.permissions.require_async("file", file_record["id"], "read", uid)
        reconciled = await self._db.soft_delete_file_async(file_record["id"])
        if reconciled:
            self._invalidate_byte_cache(file_record["id"])
        return reconciled

    # ------------------------------------------------------------------
    # Hard-delete — the ONE primitive.  Cascade the DB row + versions +
    # permissions + share-links via the SQL fn, THEN purge every storage
    # object it reported and drop the byte cache.  Every hard-delete path
    # (managed_delete, FileService.hard_delete, orphan cleanup) MUST route
    # through here — calling ``db.hard_delete_file[_async]`` directly deletes
    # the rows but strands the S3 objects (the C10 orphan-data leak).  The
    # boundary guard ``scripts/audit_hard_delete_purge.py`` fails the build on
    # any direct DB-fn call outside this method.
    #
    # The D23 tombstone-retention escape (migration 033) is NOT set here: it is
    # a transaction-local GUC and has to ride the same transaction as the
    # DELETE, so ``DatabaseClient.hard_delete_file[_fallback]_async`` open it
    # around their own work. Every delete-forever surface inherits it by routing
    # through this method. See ``cloud_sync/purge_escape.py``.
    # ------------------------------------------------------------------

    @staticmethod
    def _purge_uris_from(storage_uri: object, purge: object, *, file_id: object = None) -> list[str]:
        """The storage objects a hard-delete may remove: exactly the ``main`` +
        ``versions`` the database report CLEARED, minus anything it ``retained``.

        FAIL-SAFE (AD239): only a report carrying a ``retained`` list proves the
        database checked which objects a surviving row still references — the SQL
        fn returns it to a service-role caller, a JWT caller gets counts only. No
        list (no report, the JWT shape, a partial report) purges NOTHING and says
        so; a stranded object is recoverable, a purged referenced one is not.

        The caller's ``storage_uri`` is never purged on its own authority: every
        producer reports the row's own object as ``main`` or ``retained``, so one
        that is neither (a stale record, a row the function did not find) was
        never proven unreferenced and is left in place, loudly.

        ONE retention rule: nothing the report lists in ``retained`` is purged.
        ``main_retained`` is not consulted — every producer sets it exactly when
        the row's own ``storage_uri`` is in ``retained``."""
        retained_list = purge.get("retained") if isinstance(purge, dict) else None
        if not isinstance(retained_list, (list, tuple)):
            logger.error(
                "[hard-delete] storage purge SKIPPED for file %s: the database report "
                "carries no `retained` list (report: %r), so no object can be proven "
                "unreferenced by a surviving row. Storage was left in place. Remedy: "
                "run the hard delete as a service-role caller (only then does "
                "files.hard_delete_file return main/versions/retained) and sweep the "
                "stranded objects with scripts/reconcile_orphan_objects.py.",
                file_id,
                sorted(purge) if isinstance(purge, dict) else purge,
            )
            return []
        retained = set(retained_list)
        uris: list[str] = []
        for u in [purge.get("main"), *(purge.get("versions") or [])]:
            if isinstance(u, str) and u and u not in retained and u not in uris:
                uris.append(u)
        if isinstance(storage_uri, str) and storage_uri and storage_uri not in uris and storage_uri not in retained:
            logger.error(
                "[hard-delete] storage object %s of file %s was neither cleared nor "
                "retained by the database report; it was NOT purged (never proven "
                "unreferenced). Remedy: sweep it with scripts/reconcile_orphan_objects.py.",
                storage_uri,
                file_id,
            )
        return uris

    def hard_delete_and_purge(self, file_id: str, storage_uri: object) -> dict | None:
        """Cascade-delete the row/versions/perms/links, then purge every
        storage object. Returns the SQL fn's purge report. Raises before
        touching storage if both DB paths fail, or after attempting every
        object if any storage purge fails. The single sanctioned hard-delete
        entry point."""
        try:
            purge = self._db.hard_delete_file(file_id)
        except Exception:
            logger.warning(
                "hard_delete_file SQL fn failed for %s; using ORM fallback",
                file_id,
                exc_info=True,
            )
            try:
                purge = self._db.hard_delete_file_fallback(file_id)
            except Exception as fallback_exc:
                logger.exception(
                    "hard_delete_file ORM fallback failed for %s; storage left untouched",
                    file_id,
                )
                raise HardDeleteDatabaseError(
                    f"database cascade failed for file {file_id!r}; storage was not modified"
                ) from fallback_exc
        failed_uris: list[str] = []
        for uri in self._purge_uris_from(storage_uri, purge, file_id=file_id):
            try:
                deleted = self._router.delete(uri)
                if deleted is False:
                    raise RuntimeError("storage backend returned delete=False")
            except Exception:
                failed_uris.append(uri)
                logger.exception("Failed to delete storage object during hard-delete: %s", uri)
        self._invalidate_byte_cache(file_id)
        if failed_uris:
            raise HardDeleteStorageError(file_id, failed_uris)
        return purge

    async def hard_delete_and_purge_async(self, file_id: str, storage_uri: object) -> dict | None:
        """Async twin of :meth:`hard_delete_and_purge`."""
        try:
            purge = await self._db.hard_delete_file_async(file_id)
        except Exception:
            logger.warning(
                "hard_delete_file_async SQL fn failed for %s; using ORM fallback",
                file_id,
                exc_info=True,
            )
            try:
                purge = await self._db.hard_delete_file_fallback_async(file_id)
            except Exception as fallback_exc:
                logger.exception(
                    "hard_delete_file_async ORM fallback failed for %s; storage left untouched",
                    file_id,
                )
                raise HardDeleteDatabaseError(
                    f"database cascade failed for file {file_id!r}; storage was not modified"
                ) from fallback_exc
        failed_uris: list[str] = []
        for uri in self._purge_uris_from(storage_uri, purge, file_id=file_id):
            try:
                deleted = await self._router.delete_async(uri)
                if deleted is False:
                    raise RuntimeError("storage backend returned delete=False")
            except Exception:
                failed_uris.append(uri)
                logger.exception("Failed to delete storage object during hard-delete: %s", uri)
        self._invalidate_byte_cache(file_id)
        if failed_uris:
            raise HardDeleteStorageError(file_id, failed_uris)
        return purge

    @staticmethod
    def _invalidate_byte_cache(file_id: str) -> None:
        try:
            from matrx_files.cloud_sync.byte_cache import get_byte_cache

            get_byte_cache().invalidate(file_id)
        except Exception:
            pass

    def managed_delete(
        self,
        file_path: str,
        *,
        user_id: str | None = None,
        hard_delete: bool = False,
        allow_system_purge: bool = False,
    ) -> bool:
        """Delete a file (soft by default).  Requires admin access."""
        uid = self._resolve_user_id(user_id)
        file_record = self._db.get_file_by_path(uid, file_path)
        if not file_record:
            return False
        if (file_record.get("metadata") or {}).get("system_immutable") and not allow_system_purge:
            raise PermissionError(
                f"system-managed immutable file cannot be deleted: {file_record['id']}"
            )

        self.permissions.require("file", file_record["id"], "admin", uid)

        if hard_delete:
            self.hard_delete_and_purge(file_record["id"], file_record["storage_uri"])
            return True

        ok = self._db.soft_delete_file(file_record["id"])
        self._invalidate_byte_cache(file_record["id"])
        return ok

    async def managed_delete_async(
        self,
        file_path: str,
        *,
        user_id: str | None = None,
        hard_delete: bool = False,
        allow_system_purge: bool = False,
    ) -> bool:
        """Async version of managed_delete()."""
        uid = self._resolve_user_id(user_id)
        file_record = await self._db.get_file_by_path_async(uid, file_path)
        if not file_record:
            return False
        if (file_record.get("metadata") or {}).get("system_immutable") and not allow_system_purge:
            raise PermissionError(
                f"system-managed immutable file cannot be deleted: {file_record['id']}"
            )

        await self.permissions.require_async("file", file_record["id"], "admin", uid)

        if hard_delete:
            await self.hard_delete_and_purge_async(file_record["id"], file_record["storage_uri"])
            return True

        ok = await self._db.soft_delete_file_async(file_record["id"])
        self._invalidate_byte_cache(file_record["id"])
        return ok

    # ------------------------------------------------------------------
    # Listing / querying
    # ------------------------------------------------------------------

    def list_files(
        self,
        folder_path: str | None = None,
        user_id: str | None = None,
    ) -> list[dict]:
        """List files owned by the user, optionally filtered by folder."""
        uid = self._resolve_user_id(user_id)
        folder_id = None
        if folder_path:
            folders = self._db.get_folders_by_path(uid, folder_path)
            if not folders:
                return []
            folder_id = [f["id"] for f in folders]
        return self._db.list_files(uid, folder_id)

    async def list_files_async(
        self,
        folder_path: str | None = None,
        user_id: str | None = None,
    ) -> list[dict]:
        uid = self._resolve_user_id(user_id)
        folder_id = None
        if folder_path:
            folders = await self._db.get_folders_by_path_async(uid, folder_path)
            if not folders:
                return []
            folder_id = [f["id"] for f in folders]
        return await self._db.list_files_async(uid, folder_id)

    async def list_changed_files_async(
        self,
        since_iso: str,
        limit: int = 1000,
        user_id: str | None = None,
        *,
        include_system: bool = True,
        organization_id: str,
    ) -> list[dict]:
        """``organization_id`` (REQUIRED) scopes the feed to one tenant, in SQL."""
        uid = self._resolve_user_id(user_id)
        return await self._db.list_changed_files_async(
            uid,
            since_iso,
            limit,
            include_system=include_system,
            organization_id=organization_id,
        )

    async def list_sync_changes_async(
        self,
        *,
        cursor_ts: datetime | None = None,
        cursor_id: str | None = None,
        include_deleted: bool = False,
        include_system: bool = False,
        limit: int = 500,
        user_id: str | None = None,
    ) -> list[dict]:
        uid = self._resolve_user_id(user_id)
        return await self._db.list_sync_changes_async(
            uid,
            cursor_ts=cursor_ts,
            cursor_id=cursor_id,
            include_deleted=include_deleted,
            include_system=include_system,
            limit=limit,
        )

    async def list_all_folders_async(
        self,
        *,
        cursor_ts: datetime | None = None,
        cursor_id: str | None = None,
        include_deleted: bool = False,
        include_system: bool = False,
        limit: int = 500,
        user_id: str | None = None,
    ) -> list[dict]:
        uid = self._resolve_user_id(user_id)
        return await self._db.list_all_folders_async(
            uid,
            cursor_ts=cursor_ts,
            cursor_id=cursor_id,
            include_deleted=include_deleted,
            include_system=include_system,
            limit=limit,
        )

    async def list_files_paginated_async(
        self,
        prefix: str | None = None,
        limit: int = 1000,
        user_id: str | None = None,
        *,
        include_system: bool = True,
        organization_id: str,
    ) -> list[dict]:
        """``organization_id`` (REQUIRED) scopes the listing to one tenant, in SQL."""
        uid = self._resolve_user_id(user_id)
        return await self._db.list_files_paginated_async(
            uid,
            prefix,
            limit,
            include_system=include_system,
            organization_id=organization_id,
        )

    async def get_storage_usage_async(
        self, user_id: str | None = None, *, organization_id: str
    ) -> dict:
        """``organization_id`` (REQUIRED) scopes the usage figures to one tenant."""
        uid = self._resolve_user_id(user_id)
        return await self._db.get_storage_usage_async(uid, organization_id=organization_id)

    def list_folders(
        self,
        parent_path: str | None = None,
        user_id: str | None = None,
    ) -> list[dict]:
        uid = self._resolve_user_id(user_id)
        parent_id = None
        if parent_path:
            parents = self._db.get_folders_by_path(uid, parent_path)
            if not parents:
                return []
            parent_id = [p["id"] for p in parents]
        return self._db.list_folders(uid, parent_id)

    async def list_folders_async(
        self,
        parent_path: str | None = None,
        user_id: str | None = None,
    ) -> list[dict]:
        uid = self._resolve_user_id(user_id)
        parent_id = None
        if parent_path:
            parents = await self._db.get_folders_by_path_async(uid, parent_path)
            if not parents:
                return []
            parent_id = [p["id"] for p in parents]
        return await self._db.list_folders_async(uid, parent_id)

    def get_file_info(self, file_path: str, user_id: str | None = None) -> dict | None:
        """Get file metadata from the database."""
        uid = self._resolve_user_id(user_id)
        return self._db.get_file_by_path(uid, file_path)

    async def get_file_info_async(self, file_path: str, user_id: str | None = None) -> dict | None:
        uid = self._resolve_user_id(user_id)
        return await self._db.get_file_by_path_async(uid, file_path)

    def get_file_url(
        self,
        file_path: str,
        user_id: str | None = None,
    ) -> str:
        """Durable render URL for a tracked file, with permission check.

        Returns the always-renderable ``url`` from the durable contract
        (CDN when public, authenticated ``/files/{id}/download?inline=1``
        otherwise). NEVER a signed URL — see cloud_sync/render_urls.py.
        """
        uid = self._resolve_user_id(user_id)
        file_record = self._db.get_file_by_path(uid, file_path)
        if not file_record:
            raise FileNotFoundError(f"File '{file_path}' not found for user '{uid}'.")
        self.permissions.require("file", file_record["id"], "read", uid)
        url = self.build_urls_for_record(file_record)["url"]
        if not url:
            raise RuntimeError(f"No durable URL could be built for '{file_path}'.")
        return url

    async def get_file_url_async(
        self,
        file_path: str,
        user_id: str | None = None,
    ) -> str:
        uid = self._resolve_user_id(user_id)
        file_record = await self._db.get_file_by_path_async(uid, file_path)
        if not file_record:
            raise FileNotFoundError(f"File '{file_path}' not found for user '{uid}'.")
        await self.permissions.require_async("file", file_record["id"], "read", uid)
        url = self.build_urls_for_record(file_record)["url"]
        if not url:
            raise RuntimeError(f"No durable URL could be built for '{file_path}'.")
        return url
