"""FileService — the single public entry point for file handling.

A high-level facade over the matrx-utils file_handling stack. Hosts
construct one ``FileService`` at startup and delegate every file
operation through it. Eliminates the pattern where routers reach into
``fm.sync_engine.db.get_file_async(...)`` because the underlying
facade exposes everything they need.

Usage in a host application:

    from matrx_utils import configure_settings, configure_context
    from matrx_files import FileService

    configure_settings(my_settings)
    configure_context(get_active_user_id)
    file_service = FileService.from_env()

    # Reads with authorization in one call:
    record = await file_service.read_record(file_id, user_id=uid)

    # URL minting — never re-implement.
    asset = await file_service.build_asset_envelope(record)

    # Soft delete + restore.
    await file_service.soft_delete(file_id, user_id=uid)

The facade composes:
  * ``SyncEngine`` — managed_write_async, set_published_to_web_async,
    build_urls_for_record_async (centralized URL minting).
  * ``PermissionsManager`` — share-links, grants, group ACL.
  * ``VersionManager`` — version history + restore.

Plus host-injected callbacks (``configure_cdn_purger``,
``configure_quota_check``, ``configure_audit_logger``) so the same
service handles host-specific concerns without the matrx-utils code
importing from any host.

This file replaces the audit-flagged "27 files reach into ``_db``"
anti-pattern: every method here is the public API a caller should use.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from matrx_utils import supervised_task
from matrx_utils.row_access import SHOWN_TO_VALUES, legacy_level_echo, stated_row_access

from .derivations import assert_no_client_policy_metadata
from .file_manager import FileManager
from .asset_envelope import Asset, AssetVariant
from .user_visible import CARRIED_ROOTS as _CARRIED_ROOTS

if TYPE_CHECKING:
    from .asset_envelope import FileRef
    from .audio_extract import AudioExtractionRequest, AudioExtractionResult
    from .external_objects import (
        ExternalObjectAdoptionRequest,
        ExternalObjectAdoptionResult,
        ExternalObjectCustodyCanaryResult,
        ExternalObjectDeleteResult,
        ExternalObjectReadResult,
    )
    from .office_pdf import OfficePdfRequest, OfficePdfResult
    from .pdf_pages import PdfPageSelectionRequest, PdfPageSelectionResult
    from .retention import TemporaryFileRetentionPolicy


def directory_change_needs_move(record: dict, target_dir: str) -> bool:
    """True only when a rename/PATCH really changes the file's directory (or must
    repair a drifted parent pointer). A pure rename is NOT a move and must never
    reach ``move_file`` -- whose cross-organization refusal would block renaming a
    file whose folder is in another organization (the folder unique key is
    ``(created_by, folder_path)``, not per-organization)."""
    target_dir = (target_dir or "").strip("/")
    current_path = str(record.get("file_path") or "")
    current_dir = "/".join(current_path.split("/")[:-1])
    if target_dir != current_dir:
        return True
    # Same directory: the pointer must already agree (set for a nested file,
    # unset for a root file); otherwise let move_file repair the drift.
    return bool(record.get("parent_folder_id")) != bool(target_dir)


class FileOwnerMissing(ValueError):
    """A buffered save with no owner: no explicit user, none baked, none in the request context.

    ``files.files.created_by`` is that person; sending ``''`` only fails inside Postgres
    with a uuid syntax error that names nothing. Refused by name before any read or write."""

    error_type = "file_owner_missing"

    def __init__(self, file_path: str) -> None:
        super().__init__(
            f"cannot save {file_path!r}: no signed-in person is active in this context, "
            "so the file has no owner"
        )
        self.file_path = file_path


class FileService:
    """High-level facade for file handling. The single entry point.

    Construct via ``FileService.from_env()`` to read S3 settings from
    ``configure_settings()`` / environment variables and bootstrap a
    process-wide singleton.
    """

    _instance: "FileService | None" = None

    def __init__(self, file_manager: FileManager) -> None:
        if file_manager.sync_engine is None:
            raise RuntimeError(
                "FileService requires a FileManager with cloud_sync configured. "
                "Pass cloud_sync=CloudSyncConfig(...) when constructing."
            )
        self._fm = file_manager

    @staticmethod
    def _share_link_info(row: dict | None) -> dict | None:
        """Normalize a ``platform.share_links`` row to the envelope's
        ``ShareLinkInfo`` shape. ``url`` is the app-relative canonical
        share-page path (``/s/{token}``) — the FE prefixes its own origin.
        """
        if not row or not row.get("token"):
            return None
        return {
            "token": row["token"],
            "url": f"/s/{row['token']}",
            "expires_at": str(row["expires_at"]) if row.get("expires_at") else None,
            "max_uses": row.get("max_uses"),
        }

    # ------------------------------------------------------------------
    # Construction
    # ------------------------------------------------------------------

    @classmethod
    def from_env(cls, *, app_name: str = "matrx-files") -> "FileService":
        """Build a process-wide singleton from env-vars / ``configure_settings``.

        Reads ``AWS_S3_DEFAULT_BUCKET`` through the matrx-utils settings
        registry. Idempotent — subsequent calls return the cached instance.
        """
        if cls._instance is not None:
            return cls._instance
        from .cloud_sync.config import CloudSyncConfig

        fm = FileManager(app_name, cloud_sync=CloudSyncConfig(auto_sync=True))
        cls._instance = cls(fm)
        return cls._instance

    @classmethod
    def for_file_manager(cls, fm: FileManager) -> "FileService":
        """Wrap a caller-constructed FileManager. Use in tests or for
        per-app-name isolation where the singleton is the wrong shape."""
        return cls(fm)

    # ------------------------------------------------------------------
    # Sub-component accessors (so callers don't drill through to
    # ``service._fm.sync_engine.permissions``).
    # ------------------------------------------------------------------

    @property
    def file_manager(self) -> FileManager:
        return self._fm

    @property
    def sync_engine(self) -> Any:
        return self._fm.sync_engine

    @property
    def db(self) -> Any:
        return self._fm.sync_engine.db

    @property
    def router(self) -> Any:
        return self._fm.sync_engine.router

    @property
    def permissions(self) -> Any:
        return self._fm.sync_engine.permissions

    @property
    def versions(self) -> Any:
        return self._fm.sync_engine.versions

    @property
    def image_handler(self) -> Any:
        return self._fm.image_handler

    # ------------------------------------------------------------------
    # Authorization-aware reads
    # ------------------------------------------------------------------

    async def read_record(
        self,
        file_id: str,
        *,
        user_id: str,
        level: str = "read",
    ) -> dict:
        """Fetch a cld_files row after enforcing access in one call.

        Raises ``FileNotFoundError`` if the row is missing,
        ``PermissionError`` if the caller lacks the requested level.
        """
        return await self._fm.sync_engine.get_authorized_record_async(
            file_id, user_id=user_id, level=level
        )

    async def read_record_unchecked(self, file_id: str) -> dict | None:
        """Load a cld_files row WITHOUT authorization. For background
        tasks that already verified access (thumbnails, rekey, audit
        dispatcher). Never use in a request handler."""
        return await self._fm.sync_engine.db.get_file_async(file_id)

    async def read_record_for_active_user(
        self, file_id: str, *, level: str = "read"
    ) -> dict | None:
        """Load a cld_files row, enforcing access for the AMBIENT request user.

        The same ACCESS GATE contract as resolve_media, for byte-serving paths
        that resolve a user-supplied ``file_id`` but do not go through
        resolve_media (preview, pdf-compress, …):

        FAIL-CLOSED, matching the resolve_media gate:
          * request user present → enforce owner / public / shared; raises
            ``PermissionError`` on denial.
          * an explicit ``matrx_utils.ctx.system_file_access("<reason>")`` scope
            (internal/background job that declared itself) → trusted lookup.
          * otherwise (anonymous HTTP, OR a no-context call with no marker) →
            ``PermissionError``. No identity + no declared system scope = denied.

        Use this instead of ``db.get_file_async`` anywhere a request handler
        turns a client-supplied file_id into bytes.
        """
        from matrx_utils.ctx import get_active_context, get_system_file_access_reason

        ctx = get_active_context()
        uid = (getattr(ctx, "user_id", None) or "") if ctx is not None else ""
        if uid:
            return await self._fm.sync_engine.get_authorized_record_async(
                file_id, user_id=uid, level=level
            )
        if get_system_file_access_reason():
            return await self._fm.sync_engine.db.get_file_async(file_id)  # explicit internal job
        raise PermissionError(
            "file access requires an authenticated user or an explicit "
            "matrx_utils.ctx.system_file_access() scope (fail-closed)"
        )

    async def read_by_path(self, owner_id: str, file_path: str) -> dict | None:
        """UNGATED path lookup. Prefer ``read_record_by_path`` in any path that
        serves a caller — this one decides nothing about who may see the row."""
        return await self._fm.sync_engine.db.get_file_by_path_async(owner_id, file_path)

    async def read_record_by_path(
        self,
        owner_id: str,
        file_path: str,
        *,
        user_id: str,
        level: str = "read",
        organization_id: str | None = None,
    ) -> dict | None:
        """Resolve a path to its cld_files row THROUGH the access gate.

        The path-shaped twin of :meth:`read_record`: the row the path names is
        located first, then ``get_authorized_record_async`` decides whether this
        caller may have it, and the row that comes BACK is the gate's, never the
        raw lookup's.

        ORDER IS THE CONTRACT, and both halves of it are load-bearing:

        * access is decided BEFORE the tenant filter, so a caller who may not
          see the row gets ``PermissionError`` — the denial is never downgraded
          to a polite ``None``, which would tell an unauthorized caller only
          that "there is nothing here" while the gate had actually refused;
        * the tenant filter is applied AFTER, so a row that exists and the
          caller may read but that belongs to another organization reads as
          ``None`` — absent, not refused.

        Returns ``None`` when the path names no row at all.
        """
        row = await self._fm.sync_engine.db.get_file_by_path_async(owner_id, file_path)
        if row is None:
            return None
        authorized = await self._fm.sync_engine.get_authorized_record_async(
            row["id"], user_id=user_id, level=level
        )
        if (
            organization_id is not None
            and authorized.get("organization_id") != organization_id
        ):
            return None
        return authorized

    async def adopt_external_object(
        self,
        request: ExternalObjectAdoptionRequest,
        *,
        retention_policy: TemporaryFileRetentionPolicy,
    ) -> ExternalObjectAdoptionResult:
        """Adopt an already-written S3 object without copying its bytes."""
        from .external_objects import adopt_external_object

        return await adopt_external_object(
            self._fm.sync_engine,
            request,
            retention_policy=retention_policy,
        )

    async def read_external_object_with_receipt(
        self,
        *,
        file_id: str,
        user_id: str,
    ) -> ExternalObjectReadResult:
        """Owner-authorized read with checksummed activity-log evidence."""
        from .external_objects import read_external_object_with_receipt

        return await read_external_object_with_receipt(
            self._fm.sync_engine,
            file_id=file_id,
            user_id=user_id,
        )

    async def delete_external_object_with_receipt(
        self,
        *,
        file_id: str,
        user_id: str,
    ) -> ExternalObjectDeleteResult:
        """Governed hard-delete with durable authorization/completion receipts."""
        from .external_objects import delete_external_object_with_receipt

        return await delete_external_object_with_receipt(
            self._fm.sync_engine,
            file_id=file_id,
            user_id=user_id,
        )

    async def run_external_object_custody_canary(
        self,
        request: ExternalObjectAdoptionRequest,
        *,
        retention_policy: TemporaryFileRetentionPolicy,
    ) -> ExternalObjectCustodyCanaryResult:
        """Prove adopt, owner read, checksum, governed purge, and receipts."""
        from .external_objects import run_external_object_custody_canary

        return await run_external_object_custody_canary(
            self._fm.sync_engine,
            request,
            retention_policy=retention_policy,
        )

    # ------------------------------------------------------------------
    # URL building (centralized — see SyncEngine.build_urls_for_record_async).
    # ------------------------------------------------------------------

    async def build_urls(self, record: dict) -> dict:
        """Return the durable ``{url, cdn_url, download_url}`` for a record.

        Never call ``router.get_url_async`` directly — that mints an
        expiring signed URL, which no client-facing shape may carry.
        """
        return await self._fm.sync_engine.build_urls_for_record_async(record)

    async def build_file_ref(self, record: dict) -> FileRef:
        """Project an internal file row into the canonical safe ``FileRef``."""
        from .asset_envelope import FileRef

        urls = await self.build_urls(record)
        metadata = record.get("metadata") or {}
        return FileRef(
            file_id=str(record["id"]),
            published_to_web=bool(record.get("published_to_web")),
            shown_to=record.get("shown_to"),
            visibility=legacy_level_echo(record),
            file_name=record.get("file_name"),
            mime_type=record.get("mime_type"),
            size_bytes=record.get("size_bytes"),
            url=urls.get("url"),
            cdn_url=urls.get("cdn_url"),
            download_url=urls.get("download_url"),
            thumbnail_url=record.get("thumbnail_url") or metadata.get("thumbnail_url"),
        )

    async def select_pdf_pages(
        self,
        file_id: str,
        *,
        user_id: str,
        request: PdfPageSelectionRequest,
    ) -> PdfPageSelectionResult:
        """Create or reuse a one-file PDF containing selected source pages."""
        from .pdf_pages import select_pdf_pages

        return await select_pdf_pages(
            self,
            file_id=file_id,
            user_id=user_id,
            request=request,
        )

    async def extract_audio(
        self,
        file_id: str,
        *,
        user_id: str,
        request: AudioExtractionRequest | None = None,
    ) -> AudioExtractionResult:
        """Create or reuse the ``audio_extracted`` derivative of a video."""
        from .audio_extract import extract_audio

        return await extract_audio(
            self,
            file_id=file_id,
            user_id=user_id,
            request=request,
        )

    async def convert_office_pdf(
        self,
        file_id: str,
        *,
        user_id: str,
        request: OfficePdfRequest | None = None,
    ) -> OfficePdfResult:
        """Create or reuse the ``pdf_conversion`` derivative of an Office file."""
        from .office_pdf import convert_office_pdf

        return await convert_office_pdf(
            self,
            file_id=file_id,
            user_id=user_id,
            request=request,
        )

    async def build_asset_envelope(
        self,
        record: dict,
        *,
        preset_name: str | None = None,
        primary_key: str | None = None,
        include_variants: bool = True,
        master_width: int | None = None,
        master_height: int | None = None,
    ) -> Asset:
        """Build a full ``Asset`` envelope for a master record.

        Loads sibling variant rows (when present) and assembles the
        canonical wire shape consumed by every FE. Self-contained — no
        host dependency. The renderer (``_render_image_variants_to_cloud``
        that writes new variants) still lives in the host's asset router
        for now since it carries account-tier + quota concerns.
        """
        from .asset_builder import build_asset_from_master

        return await build_asset_from_master(
            self._fm,
            record,
            preset_name=preset_name,
            primary_key=primary_key,
            include_variants=include_variants,
            master_width=master_width,
            master_height=master_height,
        )

    # ------------------------------------------------------------------
    # Writes
    # ------------------------------------------------------------------

    async def write(
        self,
        content: bytes | str | dict | list,
        *,
        file_path: str,
        mime_type: str | None = None,
        published_to_web: bool | None = None,
        shown_to: str | None = None,
        share_with: list[str] | None = None,
        share_level: str = "read",
        change_summary: str | None = None,
        user_id: str | None = None,
        metadata: dict | None = None,
    ) -> Any:
        """Buffered write through the canonical engine path.

        Returns a ``SyncResult`` with the durable URL envelope already
        populated (``url`` / ``cdn_url`` / ``download_url`` / ``published_to_web``).
        """
        return await self._fm.sync_engine.managed_write_async(
            file_path,
            content,
            mime_type=mime_type,
            published_to_web=published_to_web,
            shown_to=shown_to,
            share_with=share_with,
            share_level=share_level,
            change_summary=change_summary,
            user_id=user_id,
            metadata=metadata,
        )

    async def replace_file(
        self,
        file_id: str,
        content: bytes | str | dict | list,
        *,
        user_id: str,
        change_summary: str | None = None,
        mime_type: str | None = None,
        metadata_patch: dict | None = None,
        new_file_name: str | None = None,
    ) -> Any:
        """In-place replace by file_id — preserves storage_uri + version-bumps."""
        return await self._fm.sync_engine.replace_file_async(
            file_id,
            content,
            user_id=user_id,
            change_summary=change_summary,
            mime_type=mime_type,
            metadata_patch=metadata_patch,
            new_file_name=new_file_name,
        )

    # ------------------------------------------------------------------
    # Publishing / list filter / sharing
    # ------------------------------------------------------------------

    async def set_published_to_web(
        self,
        file_id: str,
        *,
        user_id: str,
        published: bool,
    ) -> dict | None:
        """Publish a file to the web or take it off (moves the S3 object between buckets)."""
        # Authorization: writer-level access required.
        record = await self.read_record(file_id, user_id=user_id, level="write")
        result = await self._fm.sync_engine.set_published_to_web_async(
            file_id, published, user_id=user_id
        )
        self._audit("file.published_to_web_changed", record, user_id, published_to_web=published)
        return result

    async def set_shown_to(
        self,
        file_id: str,
        *,
        user_id: str,
        shown_to: str,
    ) -> dict | None:
        """Change who a file is shown to in lists (a list filter — never row security)."""
        if shown_to not in SHOWN_TO_VALUES:
            raise ValueError(f"unknown shown_to {shown_to!r}; expected one of {SHOWN_TO_VALUES}")
        record = await self.read_record(file_id, user_id=user_id, level="write")
        await self._fm.sync_engine.db.update_file_async(file_id, {"shown_to": shown_to})
        self._audit("file.shown_to_changed", record, user_id, shown_to=shown_to)
        return await self.db.get_file_async(file_id)

    async def grant_permission(
        self,
        *,
        file_id: str,
        user_id: str,  # grantor
        grantee_id: str,
        level: str = "read",
        grantee_type: str = "user",
    ) -> dict:
        """Grant access to another user. Grantor must be admin/owner."""
        record = await self.read_record(file_id, user_id=user_id, level="admin")
        result = await self._fm.sync_engine.db.upsert_permission_async(
            {
                "resource_id": file_id,
                "resource_type": "file",
                "grantee_id": grantee_id,
                "grantee_type": grantee_type,
                "permission_level": level,
                "granted_by": user_id,
            }
        )
        self._audit(
            "permission.granted",
            record,
            user_id,
            grantee_id=grantee_id,
            grantee_type=grantee_type,
            level=level,
        )
        return result

    async def revoke_permission(
        self,
        *,
        file_id: str,
        user_id: str,
        grantee_id: str,
        grantee_type: str = "user",
    ) -> bool:
        record = await self.read_record(file_id, user_id=user_id, level="admin")
        result = await self._fm.sync_engine.db.delete_permission_async(
            resource_id=file_id,
            resource_type="file",
            grantee_id=grantee_id,
            grantee_type=grantee_type,
        )
        self._audit(
            "permission.revoked", record, user_id, grantee_id=grantee_id, grantee_type=grantee_type
        )
        return result

    # ------------------------------------------------------------------
    # Soft / hard delete
    # ------------------------------------------------------------------

    def _audit(self, event_type: str, record: dict | None, user_id: str, **extras: Any) -> None:
        """Fire a file-mutation audit event through the host-configured
        logger (``fire_audit_event`` is a no-op when none is wired, and
        never raises). The actor (``user_id``) is what lets the event
        match owner-scoped webhooks downstream."""
        from .cloud_sync.events import fire_audit_event

        record = record or {}
        fire_audit_event(
            event_type,
            {
                "resource_id": record.get("id"),
                "resource_type": "file",
                "organization_id": record.get("organization_id"),
                "user_id": user_id,
                **extras,
            },
        )

    async def soft_delete(self, file_id: str, *, user_id: str) -> bool:
        """Mark a file deleted (recoverable via /restore)."""
        record = await self.read_record(file_id, user_id=user_id, level="admin")
        result = await self._fm.sync_engine.db.soft_delete_file_async(record["id"])
        self._audit("file.deleted", record, user_id)
        return result

    async def restore(self, file_id: str, *, user_id: str) -> bool:
        """Undo a soft-delete. Requires admin on the file."""
        # We can't read the record through the public path (it's soft-deleted).
        # Pull via raw DB, then send even the owner through the canonical judge.
        # Contextual system artifacts intentionally do not grant their
        # historical created_by value unconditional access.
        record = await self._fm.sync_engine.db.get_file_async(file_id, include_deleted=True)
        if not record:
            raise FileNotFoundError(f"File {file_id!r} not found")
        await self.permissions.require_async("file", file_id, "admin", user_id)
        # Direct model update: update_file_async strips None values (so
        # Postgres defaults apply on normal writes), but restore NEEDS to
        # set deleted_at back to NULL explicitly — update_where does.
        from .cloud_sync.db import _models

        mf, _ = _models()
        await mf.Files.update_where({"id": file_id}, deleted_at=None)
        self._audit("file.restored", record, user_id)
        return True

    # ------------------------------------------------------------------
    # Backfill conveniences (delegate to the cloud_sync.backfill module).
    # ------------------------------------------------------------------

    # ------------------------------------------------------------------
    # Sub-component accessors — host code reaches portable primitives.
    # ------------------------------------------------------------------

    @property
    def tus(self) -> Any:
        """TUS resumable-upload manager. See cloud_sync/transports/tus.py."""
        return self.sync_engine.tus

    @property
    def presigned(self) -> Any:
        """Presigned PUT upload coordinator. See cloud_sync/transports/presigned.py."""
        return self.sync_engine.presigned

    @property
    def streamer(self) -> Any:
        """Range-aware download streamer. See cloud_sync/download_stream.py."""
        return self.sync_engine.streamer

    @property
    def variants(self) -> Any:
        """Idempotent variant rendering. See cloud_sync/variants_service.py."""
        return self.sync_engine.variants

    # ------------------------------------------------------------------
    # Buffered upload (single-POST). The portable orchestration; hosts
    # supply quota policy + post-upload hooks.
    # ------------------------------------------------------------------

    async def _placement_alias_target(
        self, content: bytes, *, file_path: str, user_id: str, organization_id: str | None
    ) -> str | None:
        """The canonical file id when these bytes live at another path and nothing lives here."""
        if not content or not isinstance(content, (bytes, bytearray)):
            return None
        if await self.sync_engine.db.get_file_by_path_async(user_id, file_path) is not None:
            return None  # a new version of the file at this path
        from .dedup import compute_checksum, lookup_existing_async

        org = await self.sync_engine._resolve_write_organization_id_async(user_id, organization_id)
        lookup = await lookup_existing_async(
            self.sync_engine.db,
            checksum=compute_checksum(bytes(content)),
            owner_id=user_id,
            organization_id=org,
        )
        existing = lookup.existing if lookup.has_duplicate else None
        if not existing or existing.get("file_path") == file_path:
            return None
        return str(existing["id"])

    async def upload_simple(
        self,
        content: bytes,
        *,
        file_path: str,
        user_id: str,
        mime_type: str | None = None,
        published_to_web: bool | None = None,
        shown_to: str | None = None,
        visibility: str | None = None,
        share_with: list[str] | None = None,
        share_level: str = "read",
        change_summary: str | None = None,
        metadata: dict | None = None,
        organization_id: str | None = None,
        auto_thumbnail: bool = True,
        auto_rekey: bool = True,
        on_complete: Any = None,
        file_id: str | None = None,
        origin_device_id: str | None = None,
        client_modified_at: Any = None,
        exact_folder_organization: bool = False,
    ) -> Any:
        """Buffered upload + automatic post-write orchestration.

        Every folder on ``file_path`` is ``organization_id``'s own (a person's folder tree is
        per organization); another organization's folder at the same path is never used.
        ``exact_folder_organization`` is accepted for existing callers.

        Always:
          - calls ``managed_write_async`` with the canonical write path
          - fires the thumbnail processor (if ``auto_thumbnail=True``)
          - fires the canonical-key rekey (if ``auto_rekey=True``)

        Optionally calls the host-supplied ``on_complete(result)`` callable
        — async or sync — for host-specific work (quota delta, custom
        analysis dispatch, audit emission). The callback is fire-and-forget;
        its failure logs but does not propagate.

        Returns the ``SyncResult`` from ``managed_write_async``.

        A path is never collapsed into another file. Content this owner already
        holds at a DIFFERENT path still gets a row at ``file_path``, linked by
        ``duplicate_of_file_id`` (main's ruling 2026-10-21: dedupe is a storage
        concern, never "no row"). The live probe found both buffered doors --
        this package's ``POST /files/upload`` and aidream's -- answering b.txt
        with a.txt's id. The engine's own implicit alias is left as it is.
        """
        # The owner is resolved ONCE, here, before anything reads by it: the explicit
        # argument, else the engine's baked user, else the request context. The shared
        # host FileManager bakes no user, so callers pass ``''`` and rely on the context;
        # the path lookup below once read the raw ``''`` and every paid media save failed
        # with ``invalid input syntax for type uuid: ""`` (8f11a14e77, 2026-10-21).
        user_id = self.sync_engine._resolve_user_id(user_id)
        if not user_id:
            raise FileOwnerMissing(file_path)
        duplicate_of_file_id = await self._placement_alias_target(
            content, file_path=file_path, user_id=user_id, organization_id=organization_id
        )
        result = await self.sync_engine.managed_write_async(
            file_path,
            content,
            duplicate_of_file_id=duplicate_of_file_id,
            mime_type=mime_type,
            published_to_web=published_to_web,
            shown_to=shown_to,
            visibility=visibility,
            share_with=share_with,
            share_level=share_level,
            change_summary=change_summary,
            metadata=metadata,
            # The organization this REQUEST was admitted with, resolved ONCE at
            # the API edge and threaded explicitly. Never re-derived here, and
            # never left to a metadata dict an intermediate layer may not have
            # filled (production outage 2026-09-19 — see
            # ``matrx_files/request_organization.py``).
            organization_id=organization_id,
            user_id=user_id,
            file_id=file_id,
            # Device provenance (SPEC-SERVER §2.2), pre-validated at the edge:
            # the device is known to belong to this caller and the client clock
            # is not absurd. NULL means "no registered device" -- a browser
            # upload -- which the sync engine reads as "not mine".
            origin_device_id=origin_device_id,
            client_modified_at=client_modified_at,
            exact_folder_organization=exact_folder_organization,
        )
        if auto_thumbnail:
            try:
                from .cloud_sync.processing import generate_thumbnail_for_file

                supervised_task(
                    generate_thumbnail_for_file(self._fm, result.file_id),
                    kind="file_thumbnail_generation_failed",
                    name=f"thumbnail:{result.file_id}",
                    context={"file_id": result.file_id},
                )
            except Exception:
                pass
        # Rekey only when the caller used the legacy path scheme. When a
        # file_id is pinned the row is born canonical — nothing to copy.
        if auto_rekey and file_id is None:
            try:
                from .cloud_sync.backfill import rekey_one_file

                supervised_task(
                    rekey_one_file(self._fm, result.file_id),
                    kind="file_rekey_failed",
                    name=f"rekey:{result.file_id}",
                    context={"file_id": result.file_id},
                )
            except Exception:
                pass
        if on_complete is not None:
            try:
                ret = on_complete(result)
                if hasattr(ret, "__await__"):
                    supervised_task(
                        ret,
                        kind="file_upload_completion_hook_failed",
                        name=f"file-complete:{result.file_id}",
                        context={"file_id": result.file_id},
                    )
            except Exception as e:
                from matrx_utils import vcprint

                vcprint(
                    f"[FileService.upload_simple] on_complete hook failed: {e!r}",
                    color="yellow",
                )
        return result

    # ------------------------------------------------------------------
    # A file carried FOR an organization (FILES-FOLDER-ORG, 2026-09-25)
    #
    # A person has ONE folder namespace across every organization
    # (``files.folders`` is unique on ``(created_by, folder_path)``), so a service that writes a
    # file for organization X as a person who is also in organization Y must not pick a path Y
    # may already hold: the old ``record-store/...`` path found admin's own folder and the
    # Castellano & Reyes file landed half in admin's tree (COERCED, 2026-09-25 09:11 UTC). The
    # destination below is keyed by X's id, created in X, named for a person, and a mismatch
    # anywhere on it is refused, never coerced.
    # ------------------------------------------------------------------

    #: The root of every carried file's tree: one per organization, one per service kind. The key
    #: is the stable path segment (suffixed with the organization id on disk); the value is the
    #: name a person reads in that organization's file tree.
    #: Declared once in :mod:`matrx_files.user_visible` (the Recents rule is spelled from it).
    CARRIED_ROOTS: dict[str, str] = _CARRIED_ROOTS

    async def ensure_organization_folder_async(
        self,
        *,
        owner_id: str,
        organization_id: str,
        root: str,
        source_key: str,
        source_label: str,
    ) -> tuple[str, str]:
        """``<Root label> / <source label>`` in ``organization_id``'s own tree; ``(path, id)``.

        ``root`` is a key of :data:`CARRIED_ROOTS` ("record-store" -> "Record store");
        ``source_key`` is the stable id of where the files came from (a table or scope id) and
        ``source_label`` its name. Idempotent: one folder per (organization, root, source).
        """
        if root not in self.CARRIED_ROOTS:
            raise ValueError(
                f"{root!r} is not a carried-file root; known roots: {sorted(self.CARRIED_ROOTS)}"
            )
        if not organization_id:
            raise ValueError("a file carried for an organization needs that organization's id")
        return await self.sync_engine.ensure_labelled_folder_chain_async(
            owner_id=owner_id,
            organization_id=str(organization_id),
            segments=[
                (f"{root}-{organization_id}", self.CARRIED_ROOTS[root]),
                (str(source_key), source_label),
            ],
        )

    async def upload_for_organization(
        self,
        content: bytes,
        *,
        owner_id: str,
        organization_id: str,
        root: str,
        source_key: str,
        source_label: str,
        file_name: str,
        sub_folders: tuple[str, ...] | list[str] = (),
        intent: str | None = None,
        reason: str | None = None,
        **kwargs: Any,
    ) -> Any:
        """Write a file FOR ``organization_id`` into its own ``<Root> / <source>`` folder.

        ``sub_folders`` are extra path keys under the source folder (a crawl session, a capture);
        they are created in the same organization, and an other-organization folder there refuses.
        ``intent`` (``create`` / ``alias_existing`` / ``force_new_copy``, with ``reason`` for the
        last) routes through :meth:`upload_with_intent` and answers its dict; without it the bytes
        go through :meth:`upload_simple` and the answer is its ``SyncResult``.

        The one door for a service carrying a file on an organization's behalf (the record
        store's big values; any exporter or tool that writes for an organization it does not act
        as). The folder is resolved first (:meth:`ensure_organization_folder_async`), then the
        bytes go through :meth:`upload_simple` with ``exact_folder_organization=True`` — a folder
        of any other organization refuses the write with a sentence. ``kwargs`` are
        :meth:`upload_simple`'s (``mime_type``, ``published_to_web``, ``file_id``, ``metadata`` ...).
        """
        if not file_name or "/" in file_name:
            raise ValueError(f"file_name {file_name!r} must be one name, no '/'")
        for key in sub_folders:
            if not key or "/" in str(key):
                raise ValueError(f"sub folder {key!r} must be one path key, no '/'")
        folder_path, _folder_id = await self.ensure_organization_folder_async(
            owner_id=owner_id,
            organization_id=organization_id,
            root=root,
            source_key=source_key,
            source_label=source_label,
        )
        file_path = "/".join([folder_path, *[str(k) for k in sub_folders], file_name])
        if intent is not None:
            return await self.upload_with_intent(
                content,
                intent=intent,
                reason=reason,
                file_path=file_path,
                owner_id=owner_id,
                organization_id=str(organization_id),
                exact_folder_organization=True,
                **kwargs,
            )
        return await self.upload_simple(
            content,
            file_path=file_path,
            user_id=owner_id,
            organization_id=str(organization_id),
            exact_folder_organization=True,
            **kwargs,
        )

    # ------------------------------------------------------------------
    # Intent-aware dedup upload (Phase 2.0 strict-intent contract).
    # ------------------------------------------------------------------

    async def find_by_checksum(
        self,
        *,
        checksum: str,
        owner_id: str | None = None,
        organization_id: str | None = None,
    ) -> dict | None:
        """Look up the canonical cld_files row for a given content hash.

        Returns ``None`` if no match (or if both scope params are NULL).
        Org-scope wins when ``organization_id`` is provided. Owner-scope
        is used for personal libraries outside any org. The returned row
        is the OLDEST non-deleted, non-aliased row — the canonical
        across re-uploads.
        """
        return await self._fm.sync_engine.db.get_file_by_checksum_async(
            checksum,
            owner_id=owner_id,
            organization_id=organization_id,
        )

    async def upload_with_intent(
        self,
        content: bytes,
        *,
        intent: str,
        file_path: str,
        owner_id: str,
        organization_id: str | None = None,
        mime_type: str | None = None,
        published_to_web: bool | None = None,
        shown_to: str | None = None,
        visibility: str | None = None,
        share_with: list[str] | None = None,
        share_level: str = "read",
        change_summary: str | None = None,
        metadata: dict | None = None,
        reason: str | None = None,
        auto_thumbnail: bool = True,
        auto_rekey: bool = True,
        on_complete: Any = None,
        exact_folder_organization: bool = False,
    ) -> dict:
        """Strict-intent dedup-aware upload.

        ``exact_folder_organization`` as :meth:`upload_simple`; services writing FOR an
        organization reach it through :meth:`upload_for_organization`.

        Three intents, no upsert ambiguity:

        * ``intent='create'``         — fail-loud if a duplicate exists.
          Raises ``DuplicateFileError`` (HTTP 409 mappable). The caller
          (UI) should surface the conflict and re-submit with a
          different intent.

        * ``intent='alias_existing'`` — return the existing row when a
          duplicate is found; create a new row when not. No new bytes
          are written if a duplicate is found.

        * ``intent='force_new_copy'`` — create a deliberate parallel
          copy. Requires a ``reason`` (>= 4 chars). The new row's
          ``duplicate_of_file_id`` points at the canonical, and
          ``metadata.force_new_copy_reason`` records the justification.

        Returns a dict with shape::

            {
              "outcome": "created" | "aliased" | "force_copy_created",
              "file_id": str,
              "file_path": str,
              "checksum": str,
              "duplicate_of_file_id": str | None,
              "result": SyncResult | None,   # present only when bytes
                                              # were actually written
            }

        For ``aliased`` outcomes, ``result`` is None because no write
        happened — the existing row is returned as-is.
        """
        from .dedup import (
            DedupDecision,
            DuplicateFileError,
            UploadIntent,
            compute_checksum,
            resolve_async,
        )
        import uuid as _uuid

        checksum = compute_checksum(content)
        resolved_organization_id = (
            await self.sync_engine._resolve_write_organization_id_async(
                owner_id,
                organization_id,
            )
        )
        decision: DedupDecision = await resolve_async(
            self._fm.sync_engine.db,
            intent=intent,
            content=content,
            owner_id=owner_id,
            organization_id=resolved_organization_id,
            reason=reason,
            precomputed_checksum=checksum,
            file_path=file_path,
        )

        if decision.action == "return_existing":
            existing = decision.lookup.existing or {}
            return {
                "outcome": "aliased",
                "file_id": str(existing.get("id")),
                "file_path": existing.get("file_path"),
                "checksum": checksum,
                "duplicate_of_file_id": None,
                "result": None,
                "scope": decision.lookup.scope,
                "message": (
                    f"File with this content already exists "
                    f"(uploaded {existing.get('created_at')}). Reusing it."
                ),
            }

        # Both write_new and write_alias write bytes; the difference is
        # whether duplicate_of_file_id gets stamped on the new row.
        write_metadata = dict(metadata or {})
        if decision.intent is UploadIntent.FORCE_NEW_COPY:
            write_metadata["force_new_copy_reason"] = decision.reason
        if decision.action == "write_alias":
            write_metadata["duplicate_of_file_id"] = decision.canonical_file_id

        # Propagate the server-validated organization through the one write
        # path. Metadata carries placement context but never grants it — and
        # since 2026-09-19 the value also rides the EXPLICIT ``organization_id=``
        # argument below, so the write never depends on this dict having been
        # filled (see ``matrx_files/request_organization.py``).
        write_metadata["organization_id"] = resolved_organization_id

        sync_result = await self.sync_engine.managed_write_async(
            file_path,
            content,
            organization_id=resolved_organization_id,
            mime_type=mime_type,
            published_to_web=published_to_web,
            shown_to=shown_to,
            visibility=visibility,
            share_with=share_with,
            share_level=share_level,
            change_summary=change_summary,
            metadata=write_metadata,
            user_id=owner_id,
            file_id=str(_uuid.uuid4()),
            create_only=True,
            duplicate_of_file_id=(
                decision.canonical_file_id if decision.action == "write_alias" else None
            ),
            exact_folder_organization=exact_folder_organization,
        )
        effective_duplicate_id = (
            decision.canonical_file_id if decision.action == "write_alias" else None
        )
        if decision.intent is UploadIntent.FORCE_NEW_COPY and not sync_result.is_new:
            # A canonical row can win after the strict-intent preflight but
            # before managed_write_async performs its own lookup/insert. The
            # inner layer correctly returns that winner; force-new semantics
            # require one more insert, now explicitly marked as its alias so
            # the dedup index permits a distinct immutable row.
            effective_duplicate_id = sync_result.file_id
            write_metadata["duplicate_of_file_id"] = effective_duplicate_id
            sync_result = await self.sync_engine.managed_write_async(
                file_path,
                content,
                # The retry carries the same organization as the first write — without it the
                # engine re-derives one and a carried copy could land in the person's own.
                organization_id=resolved_organization_id,
                mime_type=mime_type,
                published_to_web=published_to_web,
                shown_to=shown_to,
                visibility=visibility,
                share_with=share_with,
                share_level=share_level,
                change_summary=change_summary,
                metadata=write_metadata,
                user_id=owner_id,
                file_id=str(_uuid.uuid4()),
                create_only=True,
                duplicate_of_file_id=effective_duplicate_id,
                exact_folder_organization=exact_folder_organization,
            )
            if not sync_result.is_new:
                raise RuntimeError("force_new_copy failed to create a distinct canonical file row")

        if not sync_result.is_new and decision.intent is UploadIntent.CREATE:
            existing = await self._fm.sync_engine.db.get_file_async(
                sync_result.file_id,
                include_deleted=False,
            )
            raise DuplicateFileError(
                checksum=checksum,
                existing_file_id=sync_result.file_id,
                existing_path=(existing or {}).get("file_path"),
                existing_created_at=(existing or {}).get("created_at"),
                scope="org",
            )

        if not sync_result.is_new and decision.intent is UploadIntent.ALIAS_EXISTING:
            existing = await self._fm.sync_engine.db.get_file_async(
                sync_result.file_id,
                include_deleted=False,
            )
            return {
                "outcome": "aliased",
                "file_id": sync_result.file_id,
                "file_path": (existing or {}).get("file_path", file_path),
                "checksum": checksum,
                "duplicate_of_file_id": None,
                "result": None,
                "scope": "org",
                "message": "A concurrent upload created this content first. Reusing it.",
            }

        # Best-effort post-write hooks (matching upload_simple).
        if auto_thumbnail:
            try:
                from .cloud_sync.processing import generate_thumbnail_for_file

                supervised_task(
                    generate_thumbnail_for_file(self._fm, sync_result.file_id),
                    kind="file_thumbnail_generation_failed",
                    name=f"thumbnail:{sync_result.file_id}",
                    context={"file_id": sync_result.file_id},
                )
            except Exception:
                pass
        if auto_rekey:
            try:
                from .cloud_sync.backfill import rekey_one_file

                supervised_task(
                    rekey_one_file(self._fm, sync_result.file_id),
                    kind="file_rekey_failed",
                    name=f"rekey:{sync_result.file_id}",
                    context={"file_id": sync_result.file_id},
                )
            except Exception:
                pass
        if on_complete is not None:
            try:
                ret = on_complete(sync_result)
                if hasattr(ret, "__await__"):
                    supervised_task(
                        ret,
                        kind="file_upload_completion_hook_failed",
                        name=f"file-complete:{sync_result.file_id}",
                        context={"file_id": sync_result.file_id},
                    )
            except Exception as e:
                from matrx_utils import vcprint

                vcprint(
                    f"[FileService.upload_with_intent] on_complete hook failed: {e!r}",
                    color="yellow",
                )

        outcome = "force_copy_created" if effective_duplicate_id is not None else "created"
        return {
            "outcome": outcome,
            "file_id": sync_result.file_id,
            "file_path": file_path,
            "checksum": checksum,
            "duplicate_of_file_id": effective_duplicate_id,
            "result": sync_result,
            "scope": decision.lookup.scope,
        }

    # ------------------------------------------------------------------
    # Range-aware streaming download.
    # ------------------------------------------------------------------

    async def open_stream(
        self,
        file_id: str,
        *,
        user_id: str,
        range_header: str | None = None,
        version: int | None = None,
        allow_inline: bool = False,
        require_bounded: bool = False,
        expected_storage_etag: str | None = None,
    ) -> Any:
        """Open a streaming download for a file the user has read-access to.

        Authorizes via :meth:`SyncEngine.get_authorized_record_async`, then
        delegates to :class:`DownloadStreamer` for the Range / ETag /
        Content-Disposition logic. Returns a
        :class:`matrx_files.cloud_sync.download_stream.StreamingResult`
        that the FastAPI router converts to ``StreamingResponse`` (or any
        other web framework's equivalent). ``require_bounded=True`` refuses
        non-streaming storage before a whole-file read. Historical versions
        use the same range contract.
        """
        record = await self.sync_engine.get_authorized_record_async(
            file_id,
            user_id=user_id,
            level="read",
        )
        return await self.streamer.open_stream(
            record,
            range_header=range_header,
            version=version,
            allow_inline=allow_inline,
            require_bounded=require_bounded,
            expected_storage_etag=expected_storage_etag,
        )

    async def rekey_one(self, file_id: str) -> bool:
        from .cloud_sync.backfill import rekey_one_file

        return await rekey_one_file(self._fm, file_id)

    async def generate_thumbnail(self, file_id: str) -> bool:
        from .cloud_sync.processing import generate_thumbnail_for_file

        return await generate_thumbnail_for_file(self._fm, file_id)

    # ==================================================================
    # COMBINED OPERATIONS (FE-team A.1 / A.2 / A.3)
    # ==================================================================
    # Each method runs an upload / mutation / bulk-op as ONE call from
    # the FE's perspective, with best-effort atomicity:
    #   * Upload (write or mutation) always lands first.
    #   * Sub-operations (share-link create, permission grants, variant
    #     renders) run after, sequentially. Failures surface in
    #     ``errors`` on the returned envelope; we do NOT roll back the
    #     successful sub-ops.
    #   * Idempotency: when ``idempotency_key`` is set the entire bundled
    #     response is memoized in ``cld_idempotency``. Retry with the
    #     same key + same body returns the cached envelope verbatim.
    # The FE handles partial-success by reading the ``errors`` array.
    # ==================================================================

    async def upload_with_options(
        self,
        content: bytes | str | dict | list,
        *,
        file_path: str,
        owner_id: str,
        mime_type: str | None = None,
        published_to_web: bool | None = None,
        shown_to: str | None = None,
        metadata: dict | None = None,
        # Bundled sub-ops:
        share: dict
        | None = None,  # {"permission_level": "viewer"|"editor", "expires_at"?: iso, "max_uses"?: int}
        permissions: list[dict]
        | None = None,  # [{"grantee_id", "grantee_type"?, "permission_level", "expires_at"?}]
        variants: list[str] | list[dict] | None = None,  # preset variant keys OR ImageVariant dicts
        preset: str | None = None,
        # Idempotency:
        idempotency_key: str | None = None,
        request_payload_for_idempotency: dict | None = None,
    ) -> dict:
        """Upload + share-link + permissions + variants in one call.

        Returns ``{"asset": Asset, "share_link": dict|None, "errors": [{"sub_op", "message"}]}``.
        Best-effort atomic — the upload always lands. Sub-op failures
        appear in ``errors``; the FE decides whether to retry them.

        ``idempotency_key`` memoizes the WHOLE bundled response so a
        flaky-network retry with the same key returns the same envelope.
        """
        from .cloud_sync.idempotency import IdempotencyStore, IdempotencyConflict
        from .asset_builder import build_asset_from_master

        store = IdempotencyStore(self._fm) if idempotency_key else None
        if store:
            try:
                cached = await store.lookup(
                    owner_id=owner_id,
                    key=idempotency_key,
                    endpoint="upload_with_options",
                    body=request_payload_for_idempotency,
                )
                if cached is not None:
                    return cached["response_body"]
            except IdempotencyConflict:
                raise

        errors: list[dict] = []

        # Stage 1: write the master.
        result = await self.write(
            content,
            file_path=file_path,
            mime_type=mime_type,
            published_to_web=published_to_web,
            shown_to=shown_to,
            metadata=metadata,
            user_id=owner_id,
        )
        master_record = await self.db.get_file_async(result.file_id)
        if not master_record:
            raise RuntimeError(f"Master record disappeared after write: {result.file_id}")

        # Stage 2: render variants (best-effort).
        if variants:
            try:
                # variants can be either a list of preset keys (strings)
                # OR a list of ImageVariant dicts. The asset_router uses
                # this path with custom_variants_json; we keep that
                # signature for consistency.
                from .specific_handlers.image_handler import compose_preset, SOCIAL_BASELINE

                variant_specs: list[dict] = []
                if isinstance(variants, list) and variants and isinstance(variants[0], str):
                    # treat as preset name
                    # caller can pass a single string in a list to apply one preset
                    for name in variants:
                        try:
                            _, specs = compose_preset(name)
                            variant_specs.extend(specs)
                        except KeyError:
                            errors.append(
                                {"sub_op": "variants", "message": f"unknown preset {name!r}"}
                            )
                else:
                    variant_specs = list(variants)  # type: ignore[arg-type]
                if variant_specs:
                    rendered = await self._render_variants_via_image_handler(
                        master_record,
                        variant_specs,
                    )
                    # rendered is a dict[key, AssetVariant] — we don't
                    # need to inline them here; build_asset_from_master
                    # picks up the sibling rows from the DB.
            except Exception as e:
                errors.append({"sub_op": "variants", "message": str(e)})

        # Stage 3: share link (best-effort).
        share_link: dict | None = None
        if share:
            try:
                share_link = await self.permissions.create_share_link_async(
                    "file",
                    result.file_id,
                    permission_level=share.get("permission_level", "viewer"),
                    expires_at=share.get("expires_at"),
                    max_uses=share.get("max_uses"),
                    user_id=owner_id,
                )
            except Exception as e:
                errors.append({"sub_op": "share_link", "message": str(e)})

        # Stage 4: per-user permissions (best-effort).
        if permissions:
            for grant in permissions:
                try:
                    await self.db.upsert_permission_async(
                        {
                            "resource_id": result.file_id,
                            "resource_type": "file",
                            "grantee_id": grant["grantee_id"],
                            "grantee_type": grant.get("grantee_type", "user"),
                            "permission_level": grant.get("permission_level", "read"),
                            "granted_by": owner_id,
                            "expires_at": grant.get("expires_at"),
                        }
                    )
                except Exception as e:
                    errors.append(
                        {
                            "sub_op": "permission",
                            "grantee_id": grant.get("grantee_id"),
                            "message": str(e),
                        }
                    )

        # Build the canonical envelope.
        asset = await build_asset_from_master(
            self._fm,
            master_record,
            preset_name=preset,
        )

        envelope: dict = {
            "asset": asset.model_dump(),
            "share_link": self._share_link_info(share_link),
            "errors": errors,
        }

        if store:
            await store.persist(
                owner_id=owner_id,
                key=idempotency_key,
                endpoint="upload_with_options",
                body=request_payload_for_idempotency,
                status_code=200,
                response_body=envelope,
                resource_id=result.file_id,
                resource_type="file",
            )

        return envelope

    async def _render_variants_via_image_handler(
        self,
        master_record: dict,
        variants_to_render: list[dict],
    ) -> dict:
        """Internal: render image variants for a master via the registered
        image handler + persist each as a cld_files row under the
        deterministic ``{master_dir}/v/`` subfolder.

        Idempotent — delegates to :class:`VariantsService` which checks
        for ``(master_id, variant_key)`` rows in cld_files BEFORE
        invoking the image encoder. Reused variants skip the encoder
        and the S3 write entirely.
        """
        if not variants_to_render:
            return {}
        engine = self._fm.sync_engine
        if engine is None:
            return {}
        asset_variants = await engine.variants.render_async(
            master_record,
            variants_specs=variants_to_render,
        )
        # Legacy callers expect dict[str, dict] of url envelopes; keep that
        # shape for back-compat. New callers should use the variants service
        # directly to get AssetVariant pydantic objects.
        return {
            key: {
                "file_id": av.file_id,
                "url": av.url,
                "cdn_url": av.cdn_url,
                "download_url": av.download_url,
            }
            for key, av in asset_variants.items()
        }

    async def mutate_file(
        self,
        file_id: str,
        *,
        user_id: str,
        # Union body — every field optional:
        name: str | None = None,
        folder: str | None = None,
        published_to_web: bool | None = None,
        shown_to: str | None = None,
        visibility: str | None = None,
        metadata: dict | None = None,
        # False (default) = merge into the existing jsonb (only sent keys
        # touched). True = the sent blob REPLACES the metadata — except
        # server-stamped policy keys, which always survive a client replace.
        metadata_replace: bool = False,
        share: dict | None = None,
        share_revoke: bool = False,
        permissions: list[dict] | None = None,
        permissions_revoke: list[dict] | None = None,
        variants: list[str] | list[dict] | None = None,
        restore_version: int | None = None,
        restore_from_trash: bool = False,
        copy_to: str | None = None,
        # Idempotency:
        idempotency_key: str | None = None,
        request_payload_for_idempotency: dict | None = None,
    ) -> dict:
        """One-shot PATCH covering every common file mutation.

        Returns ``{"asset": Asset, "share_link": dict|None, "errors": [{"sub_op", "message"}]}``.
        Best-effort atomic — every sub-op runs sequentially; failures
        accumulate in ``errors``; successful sub-ops persist.

        Sub-op order: restore_from_trash → restore_version → rename →
        move → publish/shown_to → metadata → share_revoke → share → permissions
        → permissions_revoke → variants → copy_to. The order is chosen
        so a partial failure leaves the most useful subset committed
        (e.g. a rename succeeds before a permission failure).
        """
        from .cloud_sync.idempotency import IdempotencyStore, IdempotencyConflict
        from .asset_builder import build_asset_from_master

        store = IdempotencyStore(self._fm) if idempotency_key else None
        if store:
            try:
                cached = await store.lookup(
                    owner_id=user_id,
                    key=idempotency_key,
                    endpoint=f"mutate_file:{file_id}",
                    body=request_payload_for_idempotency,
                )
                if cached is not None:
                    return cached["response_body"]
            except IdempotencyConflict:
                raise

        errors: list[dict] = []
        # S20: every rename/move receipt carries old_path AND new_path, so a
        # move that flattens a parentless nested path is visible to the caller
        # (and to the UI) rather than renaming the file on every replica in
        # silence. Surfaced on the envelope as ``path_changes``.
        move_receipts: list[dict] = []

        # Authorize once. Admin level required when publishing to / taking off
        # the web or creating / revoking a share link; write otherwise.
        published_to_web, shown_to = stated_row_access(
            published_to_web=published_to_web,
            shown_to=shown_to,
            legacy_level=visibility,
            boundary="FileService.mutate_file",
        )
        legacy_link = visibility == "link" and published_to_web is False and shown_to is None
        required_level = "admin" if (published_to_web is not None or legacy_link or share or share_revoke) else "write"
        record = await self.read_record(file_id, user_id=user_id, level=required_level)

        # Stage 0: restore from trash.
        if restore_from_trash:
            try:
                await self.restore(file_id, user_id=user_id)
                record = await self.db.get_file_async(file_id) or record
            except Exception as e:
                errors.append({"sub_op": "restore_from_trash", "message": str(e)})

        # Stage 1: restore a version.
        if restore_version is not None:
            try:
                await self.versions.restore_version_async(
                    file_id,
                    restore_version,
                    user_id=user_id,
                )
                record = await self.db.get_file_async(file_id) or record
            except Exception as e:
                errors.append(
                    {
                        "sub_op": "restore_version",
                        "version": restore_version,
                        "message": str(e),
                    }
                )

        # Stage 2: rename + move — THE ONLY LAWFUL PATH (SPEC-SERVER §4.2/§4.3).
        #
        # This stage RAISES. It used to collect its failures into ``errors[]``
        # and return 200, so a rename that was refused, conflicted or hit a
        # missing row read as success to every caller — a direct hit on
        # "nothing fails silently". The typed errors the RPC wrappers raise are
        # mapped by the ONE api mapper to 403 (42501), 404 (no_data_found),
        # 409 (23505) and 400 (22023). ``errors[]`` survives for the other
        # sub-ops; it can no longer name "rename" or "move".
        #
        # Both halves run in ONE transaction, so a move that lands and a rename
        # that then conflicts leave the row where it started. Move runs first:
        # ``move_file`` recomputes ``file_path`` from the target folder, so the
        # subsequent rename operates on the final directory.
        if name is not None or folder is not None:
            from matrx_orm import transaction

            # AD240: a folder the chain CREATES carries an explicit organization — the
            # FILE's own. ``move_file`` refuses a cross-organization move, so the file's
            # organization is the only one the destination can lawfully have; it is read
            # from the row authorized above, never resolved, defaulted or left to a trigger.
            if folder is not None and not directory_change_needs_move(record, folder):
                folder = None  # same directory: a rename, not a move
            folder_organization_id = record.get("organization_id") if folder is not None else None
            if folder is not None and not folder_organization_id:
                raise ValueError(
                    f"mutate_file({file_id}): the file row carries no organization_id, so the "
                    f"destination folder {folder!r} cannot be given one; the move is refused "
                    "rather than letting the database choose an organization"
                )

            # On the matrx-files pool, the one every RPC below runs on: a bare
            # ``transaction()`` opens on the host's FIRST configured database,
            # and the move would commit alone when the rename then conflicts.
            async with transaction(database=self.db._db_name()):
                if folder is not None:
                    # S9: the folder chain is resolved (and created when
                    # missing) as an EXPLICIT, separately reported step, then
                    # move_file is called with an id. A path typo can no longer
                    # grow a folder tree as an invisible side effect of a move.
                    new_folder_id = await self.db._rpc(
                        "files", "ensure_folder_chain", user_id, folder, str(folder_organization_id)
                    )
                    move_receipt = await self.db.move_file_async(file_id, new_folder_id or None)
                    move_receipts.append(move_receipt)
                if name is not None:
                    rename_receipt = await self.db.rename_file_async(file_id, name)
                    move_receipts.append(rename_receipt)
            record = await self.db.get_file_async(file_id) or record

        share_link: dict | None = None

        # Stage 3: publish to / take off the web (moves bytes), then the list filter.
        if published_to_web is not None and bool(published_to_web) != bool(record.get("published_to_web")):
            try:
                record = (
                    await self.set_published_to_web(
                        file_id,
                        user_id=user_id,
                        published=bool(published_to_web),
                    )
                    or record
                )
                # Cascade to variants (best-effort).
                from .asset_builder import _list_existing_variants_for_master

                for v in await _list_existing_variants_for_master(self._fm, record):
                    try:
                        await self.set_published_to_web(
                            v["id"],
                            user_id=user_id,
                            published=bool(published_to_web),
                        )
                    except Exception as ev:
                        errors.append(
                            {
                                "sub_op": "variant_published_to_web",
                                "variant_id": v["id"],
                                "message": str(ev),
                            }
                        )
            except Exception as e:
                errors.append({"sub_op": "published_to_web", "message": str(e)})
        if shown_to is not None and shown_to != record.get("shown_to"):
            try:
                record = await self.set_shown_to(file_id, user_id=user_id, shown_to=shown_to) or record
            except Exception as e:
                errors.append({"sub_op": "shown_to", "message": str(e)})

        if legacy_link:
            try:
                share_link = await self.permissions.create_share_link_async(
                    "file", file_id, permission_level="viewer", user_id=user_id
                )
                share_link = {**share_link, "url": f"/share/{share_link['token']}"}
            except Exception as e:
                errors.append({"sub_op": "share_link", "message": str(e)})

        # Stage 4: metadata merge. Policy keys (system_artifact / artifact_domain
        # / web_site_id / …) are server-stamped authorization inputs — a client
        # merge that introduces or changes one is refused loudly, never merged.
        if metadata is not None:
            try:
                existing_meta = record.get("metadata") or {}
                assert_no_client_policy_metadata(
                    metadata,
                    existing=existing_meta,
                    context=f"mutate_file({file_id}) metadata "
                    + ("replace" if metadata_replace else "merge"),
                )
                if metadata_replace:
                    # Replace, but server-stamped policy keys always survive —
                    # a client replace that omits one must not wipe an
                    # authorization input.
                    from .derivations import SYSTEM_POLICY_METADATA_KEYS

                    preserved = {
                        k: existing_meta[k]
                        for k in SYSTEM_POLICY_METADATA_KEYS
                        if k in existing_meta
                    }
                    merged = {**metadata, **preserved}
                else:
                    merged = {**existing_meta, **metadata}
                await self.db.update_file_async(file_id, {"metadata": merged})
            except Exception as e:
                errors.append({"sub_op": "metadata", "message": str(e)})

        # Stage 5: share-link revoke (do this before share create so the
        # caller can revoke-then-recreate in one PATCH).
        if share_revoke:
            try:
                links = await self.db.list_share_links_async("file", file_id)
                for link in links or []:
                    if link.get("is_active"):
                        await self.db.deactivate_share_link_async(link["token"])
            except Exception as e:
                errors.append({"sub_op": "share_revoke", "message": str(e)})

        if share:
            try:
                share_link = await self.permissions.create_share_link_async(
                    "file",
                    file_id,
                    permission_level=share.get("permission_level", "viewer"),
                    expires_at=share.get("expires_at"),
                    max_uses=share.get("max_uses"),
                    user_id=user_id,
                )
            except Exception as e:
                errors.append({"sub_op": "share_link", "message": str(e)})

        # Stage 6: permission grants + revokes.
        if permissions:
            for grant in permissions:
                try:
                    await self.db.upsert_permission_async(
                        {
                            "resource_id": file_id,
                            "resource_type": "file",
                            "grantee_id": grant["grantee_id"],
                            "grantee_type": grant.get("grantee_type", "user"),
                            "permission_level": grant.get("permission_level", "read"),
                            "granted_by": user_id,
                            "expires_at": grant.get("expires_at"),
                        }
                    )
                except Exception as e:
                    errors.append(
                        {
                            "sub_op": "permission",
                            "grantee_id": grant.get("grantee_id"),
                            "message": str(e),
                        }
                    )
        if permissions_revoke:
            for revoke in permissions_revoke:
                try:
                    await self.db.delete_permission_async(
                        resource_id=file_id,
                        resource_type="file",
                        grantee_id=revoke["grantee_id"],
                        grantee_type=revoke.get("grantee_type", "user"),
                    )
                except Exception as e:
                    errors.append(
                        {
                            "sub_op": "permission_revoke",
                            "grantee_id": revoke.get("grantee_id"),
                            "message": str(e),
                        }
                    )

        # Stage 7: variants (only meaningful for image masters).
        if variants:
            try:
                from .specific_handlers.image_handler import compose_preset

                specs: list[dict] = []
                if variants and isinstance(variants[0], str):
                    for name_v in variants:
                        try:
                            _, items = compose_preset(name_v)
                            specs.extend(items)
                        except KeyError:
                            errors.append(
                                {"sub_op": "variants", "message": f"unknown preset {name_v!r}"}
                            )
                else:
                    specs = list(variants)  # type: ignore[arg-type]
                if specs:
                    await self._render_variants_via_image_handler(record, specs)
            except Exception as e:
                errors.append({"sub_op": "variants", "message": str(e)})

        # Stage 8: copy_to — duplicate the master at a new logical path.
        # The result must be surfaced in the response envelope so the FE
        # can find the new row (audit-flagged Bug B1).
        copy_result: dict | None = None
        if copy_to:
            try:
                src_bytes = await self.router.read_async(record["storage_uri"])
                cr = await self.write(
                    src_bytes,
                    file_path=copy_to,
                    mime_type=record.get("mime_type"),
                    published_to_web=bool(record.get("published_to_web")),
                    shown_to=record.get("shown_to"),
                    user_id=user_id,
                    metadata={"copied_from": file_id},
                )
                copy_result = {
                    "file_id": cr.file_id,
                    "file_path": copy_to,
                    "url": cr.url,
                    "cdn_url": cr.cdn_url,
                    "download_url": cr.download_url,
                    "published_to_web": cr.published_to_web,
                    "size_bytes": cr.size_bytes,
                    "checksum": cr.checksum,
                }
            except Exception as e:
                errors.append({"sub_op": "copy_to", "message": str(e)})

        # Build the final envelope from the (now-updated) master.
        record = await self.db.get_file_async(file_id)
        asset = await build_asset_from_master(self._fm, record)

        envelope: dict = {
            "asset": asset.model_dump(),
            "share_link": self._share_link_info(share_link),
            "copy": copy_result,  # Bug B1 fix — new file_id is surfaced when copy_to was requested
            # S20: the rename/move receipts, each {file_id, old_path, new_path}.
            # A move that flattens a parentless nested path (a/b/c.txt -> c.txt)
            # is correct but renames the file on every replica, so the two paths
            # are always reported and never inferred.
            "path_changes": move_receipts,
            "errors": errors,
        }

        if store:
            await store.persist(
                owner_id=user_id,
                key=idempotency_key,
                endpoint=f"mutate_file:{file_id}",
                body=request_payload_for_idempotency,
                status_code=200,
                response_body=envelope,
                resource_id=file_id,
                resource_type="file",
            )

        return envelope

    async def bulk_op(
        self,
        *,
        user_id: str,
        ids: list[str],
        op: str,  # "move" | "delete" | "restore" | "publish" | "shown_to" | "share" (+ transitional "visibility")
        args: dict | None = None,
        idempotency_key: str | None = None,
        request_payload_for_idempotency: dict | None = None,
    ) -> dict:
        """Bulk operation with a discriminator. Returns per-item status.

        Response shape:
            {
              "op": "delete",
              "results": [
                {"file_id": "...", "ok": true},
                {"file_id": "...", "ok": false, "error": "permission_denied"},
                ...
              ],
              "errors": [],   # operation-level (non-per-id) errors
            }
        """
        from .cloud_sync.idempotency import IdempotencyStore, IdempotencyConflict

        store = IdempotencyStore(self._fm) if idempotency_key else None
        if store:
            try:
                cached = await store.lookup(
                    owner_id=user_id,
                    key=idempotency_key,
                    endpoint=f"bulk_op:{op}",
                    body=request_payload_for_idempotency,
                )
                if cached is not None:
                    return cached["response_body"]
            except IdempotencyConflict:
                raise

        args = args or {}
        results: list[dict] = []
        op_errors: list[dict] = []

        for fid in ids:
            try:
                if op == "delete":
                    # Delete means archive: always Trash. A legacy ``hard``
                    # arg is ignored — there is no hard delete of a file.
                    await self.soft_delete(fid, user_id=user_id)
                    results.append({"file_id": fid, "ok": True})
                elif op == "restore":
                    await self.restore(fid, user_id=user_id)
                    results.append({"file_id": fid, "ok": True})
                elif op == "move":
                    # SPEC-SERVER §4.3 path 2. This wrote parent_folder_id and
                    # NOTHING ELSE, leaving file_path pointing at the old
                    # folder — the same defect the spec exists to kill, and a
                    # shape the §4.4 file_name drift census cannot even see.
                    new_folder = args.get("target_folder_id")
                    await self.read_record(fid, user_id=user_id, level="write")
                    receipt = await self.db.move_file_async(fid, new_folder or None)
                    results.append(
                        {
                            "file_id": fid,
                            "ok": True,
                            "old_path": receipt.get("old_path"),
                            "new_path": receipt.get("new_path"),
                        }
                    )
                elif op in ("publish", "shown_to", "visibility"):
                    published, shown = stated_row_access(
                        published_to_web=args.get("published_to_web"),
                        shown_to=args.get("shown_to"),
                        legacy_level=args.get("visibility"),  # T-13 transitional wire input
                        boundary="POST /files/bulk",
                    )
                    if published is not None:
                        await self.set_published_to_web(fid, user_id=user_id, published=published)
                    if shown is not None:
                        await self.set_shown_to(fid, user_id=user_id, shown_to=shown)
                    results.append({"file_id": fid, "ok": True})
                elif op == "share":
                    link = await self.permissions.create_share_link_async(
                        "file",
                        fid,
                        permission_level=args.get("permission_level", "viewer"),
                        expires_at=args.get("expires_at"),
                        max_uses=args.get("max_uses"),
                        user_id=user_id,
                    )
                    results.append(
                        {"file_id": fid, "ok": True, "share_link": self._share_link_info(link)}
                    )
                else:
                    op_errors.append({"error": f"unknown_op:{op}"})
                    break
            except Exception as e:
                results.append({"file_id": fid, "ok": False, "error": str(e)})

        envelope = {"op": op, "results": results, "errors": op_errors}

        if store:
            await store.persist(
                owner_id=user_id,
                key=idempotency_key,
                endpoint=f"bulk_op:{op}",
                body=request_payload_for_idempotency,
                status_code=200,
                response_body=envelope,
                resource_id=None,
                resource_type=None,
            )

        return envelope

    # ==================================================================
    # PREVIEW + PDF-COMPRESS (FE-team E.16 / E.17)
    # ==================================================================

    async def render_preview(
        self,
        source: bytes | dict,  # bytes OR {"file_id": "..."} MediaRef
        variants: list[dict],  # [{width, height, format, quality, fit}]
        *,
        max_inline_bytes: int = 256 * 1024,
    ) -> list[dict]:
        """Render image variants WITHOUT persisting. Returns one entry per
        spec, each with:

            {
              "preset_id": str,        # echoed from the request spec
              "width": int,
              "height": int,
              "format": "jpeg"|"png"|"webp"|"avif",
              "quality": int | None,
              "size": int,             # encoded bytes
              "notes": [str],          # soft warnings from the renderer

              # Exactly ONE of the next two is present:
              "data_url": "data:image/...;base64,...",  # when size <= max_inline_bytes
              "ephemeral_url": "https://...",           # ephemeral 5-min URL otherwise
              "expires_in": 300,                        # seconds (with ephemeral_url)
            }

        Error entries surface as ``{"preset_id": "...", "error": "..."}``.

        ``source`` is bytes OR a MediaRef-shaped dict with ``file_id``
        (resolved via the router server-side). Used by the FE Image
        Studio preview flow so Sharp leaves the Vercel side.

        Specs format mirrors ``StudioRenderSpec`` — preset_id, width,
        height, format, quality, fit, position, background_color.
        """
        import base64

        # Resolve source bytes.
        if isinstance(source, dict):
            file_id = source.get("file_id")
            if not file_id:
                raise ValueError("preview source dict must contain file_id")
            # ACCESS GATE — a preview is a byte read; enforce access for the
            # requesting user (owner/public/shared), trusted only for internal jobs.
            record = await self.read_record_for_active_user(file_id, level="read")
            if not record:
                raise FileNotFoundError(f"File {file_id!r} not found")
            image_bytes = await self.router.read_async(record["storage_uri"])
        else:
            image_bytes = source

        # Render each spec via the image handler's studio render.
        import asyncio as _asyncio

        results: list[dict] = []
        for spec in variants:
            try:
                rendered = await _asyncio.to_thread(
                    self.image_handler.render_studio_variant,
                    image_bytes,
                    spec,
                )
            except Exception as e:
                results.append(
                    {
                        "preset_id": spec.get("preset_id"),
                        "error": str(e),
                    }
                )
                continue
            payload = {
                "preset_id": rendered["preset_id"],
                "width": rendered["width"],
                "height": rendered["height"],
                "format": rendered["format"],
                "quality": rendered.get("quality"),
                "size": rendered["size"],
                "fit": rendered.get("fit"),
                "position": rendered.get("position"),
                "notes": rendered.get("notes") or [],
            }
            if rendered["size"] <= max_inline_bytes:
                mime = f"image/{rendered['format'].lower()}"
                if rendered["format"].upper() == "JPEG":
                    mime = "image/jpeg"
                b64 = base64.b64encode(rendered["bytes"]).decode("ascii")
                payload["data_url"] = f"data:{mime};base64,{b64}"
            else:
                # Larger preview — stash under the canonical PREVIEWS
                # system folder (system-files/previews/...) + a 5-min
                # signed URL. No cld_files row is persisted; the
                # row-less ephemeral object is atomically tagged for the
                # package-owned, prefix-independent lifecycle policy.
                from .ephemeral_objects import PREVIEW_RENDER_POLICY
                from .system_paths import PREVIEWS

                preview_filename = (
                    f"{rendered['preset_id']}-{rendered['width']}x"
                    f"{rendered['height']}.{rendered['format'].lower()}"
                )
                ephemeral_path = PREVIEWS.path(preview_filename)
                bucket = self._fm.sync_engine.config.resolve_s3_bucket()
                from matrx_utils.ctx import get_active_user_id

                uid = get_active_user_id() or "anonymous"
                full_uri = f"s3://{bucket}/{uid}/{ephemeral_path}"
                await self.router.write_ephemeral_async(
                    full_uri,
                    rendered["bytes"],
                    policy=PREVIEW_RENDER_POLICY,
                    content_type=f"image/{rendered['format'].lower()}",
                )
                # Row-less scratch: a 5-minute ephemeral URL is the lawful
                # exception (no file row exists to address by id) — see
                # cloud_sync/render_urls.py. NEVER persist this value.
                url = await self.router.get_url_async(
                    full_uri,
                    expires_in=5 * 60,
                    response_content_type=f"image/{rendered['format'].lower()}",
                    response_content_disposition='inline; filename="preview.jpg"',
                )
                payload["ephemeral_url"] = url
                payload["expires_in"] = 5 * 60
            results.append(payload)
        return results

    async def compress_pdf(
        self,
        source: bytes | dict,
        *,
        level: int = 3,
        max_size_bytes: int | None = None,
        max_inline_bytes: int = 256 * 1024,
    ) -> dict:
        """Compress a PDF WITHOUT persisting a row. Returns ``{"data_url"}``
        for small results, ``{"ephemeral_url", "expires_in"}`` for larger.

        ``source`` is bytes OR a dict with ``file_id``. ``level`` is the
        compression tier (1 = mildest, 5 = most aggressive). Uses the
        matrx-utils PDF subsystem under the hood.
        """
        import base64

        # Resolve source bytes.
        if isinstance(source, dict):
            file_id = source.get("file_id")
            if not file_id:
                raise ValueError("compress_pdf source dict must contain file_id")
            # ACCESS GATE — enforce access for the requesting user before reading.
            record = await self.read_record_for_active_user(file_id, level="read")
            if not record:
                raise FileNotFoundError(f"File {file_id!r} not found")
            pdf_bytes = await self.router.read_async(record["storage_uri"])
        else:
            pdf_bytes = source

        # Delegate to the matrx-utils PDF handler.
        from .specific_handlers.pdf import compress_pdf_bytes_capped_async

        result = await compress_pdf_bytes_capped_async(
            pdf_bytes,
            level=level,
            max_size_bytes=max_size_bytes,
        )
        compressed = result.content
        original_size = len(pdf_bytes)
        compressed_size = len(compressed)
        ratio = round(1 - compressed_size / original_size, 4) if original_size > 0 else 0

        # Key MUST be ``reduction_ratio`` — AssetPdfCompressResponse requires
        # it; the old ``ratio`` key failed response validation and 500'd every
        # /assets/pdf-compress call. Tier metadata from CompressResult rides
        # along so callers can show what actually happened.
        payload: dict = {
            "level_requested": level,
            "level_used": result.level_used,
            "cap_satisfied": result.cap_satisfied,
            "strategy_used": result.strategy_used,
            "original_size": original_size,
            "compressed_size": compressed_size,
            "reduction_ratio": ratio,
        }
        if compressed_size <= max_inline_bytes:
            b64 = base64.b64encode(compressed).decode("ascii")
            payload["data_url"] = f"data:application/pdf;base64,{b64}"
        else:
            from .ephemeral_objects import PREVIEW_RENDER_POLICY
            from .system_paths import PREVIEWS
            from matrx_utils.ctx import get_active_user_id

            uid = get_active_user_id() or "anonymous"
            bucket = self._fm.sync_engine.config.resolve_s3_bucket()
            ephemeral_path = PREVIEWS.path(f"compressed-{level}.pdf")
            full_uri = f"s3://{bucket}/{uid}/{ephemeral_path}"
            await self.router.write_ephemeral_async(
                full_uri,
                compressed,
                policy=PREVIEW_RENDER_POLICY,
                content_type="application/pdf",
            )
            url = await self.router.get_url_async(
                full_uri,
                expires_in=5 * 60,
                response_content_type="application/pdf",
                response_content_disposition='inline; filename="compressed.pdf"',
            )
            payload["ephemeral_url"] = url
            payload["expires_in"] = 5 * 60
        return payload


__all__ = ["FileOwnerMissing", "FileService"]
