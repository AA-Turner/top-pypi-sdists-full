"""Database client for the cloud sync layer — matrx-orm edition.

Typed access to the file tables, which live in the dedicated ``files``
Postgres schema (the 2026 DB canonicalization moved them out of ``public``
and dropped the ``cld_`` prefix): ``files.files``, ``files.folders``,
``files.file_versions``, ``files.uploads_inflight``,
``files.idempotency``, ``files.user_account``, ``files.account_tiers``,
``files.user_storage_usage``, ``files.file_rag_jobs`` and siblings.

Permissions are NOT a file-schema table — file ACLs live in the canonical
``iam.permissions`` table and resolve through the ``iam.has_access`` /
``public.has_access_as`` SECURITY DEFINER functions (see permissions.py).

2026-07-13 (Phase 2 of the matrx-files carve-out): ALL access now goes
through **matrx-orm** — the package's own generated models
(``matrx_files.db.models_files`` / ``models_iam``, ``_database="matrx_files"``)
plus the ORM's ``call_function`` primitive for the SECURITY DEFINER RPCs.
The Supabase PostgREST client is GONE from this layer. The pool the models
hit is decided once at startup: hosted → ``matrx_files.db.bind_to_host``
alias; standalone → ``matrx_files.db.bootstrap_db``. Connections use the
service role either way; RLS is enforced only for client-side access.

The public surface (method names, signatures, dict row shapes — including
ISO-8601 strings for timestamps, exactly as PostgREST returned them) is
UNCHANGED from the PostgREST edition, so sync_engine / service / permissions
call sites are untouched. Both sync and async APIs are provided; prefer
async in FastAPI routes (the sync twins refuse to run inside a live loop).
"""

from __future__ import annotations

import logging
import secrets
from datetime import UTC, date, datetime, timedelta
from enum import Enum
from typing import Any
from uuid import UUID


from matrx_files.derivations import normalize_derivation_payload
from matrx_files.user_visible import stamp_system_folder

from matrx_orm import ConflictTarget

from .config import CloudSyncConfig
from .purge_escape import drive_sync, purge_escaped

logger = logging.getLogger(__name__)

# The Postgres schemas (informational — the generated models carry their own
# ``_db_schema``; these names are used only for RPC calls).
SCHEMA_FILES = "files"
SCHEMA_IAM = "iam"

# Safe outbound file fields — everything a client / agent tool may see.
# Deliberately EXCLUDES the server-only ``storage_uri`` (must never leave the
# server — files are identified by ``id``; see common-docs systems/files/file-service/FILE_HANDLING_LAWS.md) and
# the legacy ``owner_id`` alias (annihilated — the canonical column is
# ``created_by``). Consumed by ``list_files_filtered_async``.
SAFE_FILE_FIELDS = (
    "id",
    "created_by",
    "organization_id",
    "parent_folder_id",
    "file_path",
    "file_name",
    "mime_type",
    "size_bytes",
    "checksum",
    "published_to_web",
    "shown_to",
    "current_version",
    "width",
    "height",
    "duration_ms",
    "metadata",
    "created_at",
    "updated_at",
    "deleted_at",
)

# Narrow column set for sync/changed listings (loop-stall guard: small rows,
# hard limit — the 2026-06-12 ``event_loop_stall`` lesson).
# ON CONFLICT must name the PARTIAL unique indexes (``WHERE deleted_at IS NULL``)
# exactly: Postgres cannot infer a partial index from bare columns and raises
# "no unique or exclusion constraint matching the ON CONFLICT specification"
# (live 500 on /files/finalize-upload, 2026-10-27). Live indexes:
# cld_files_owner_id_file_path_key (created_by, file_path) and
# folders_owner_org_path_key (created_by, organization_id, folder_path).
_FILES_PATH_CONFLICT = ConflictTarget.partial(
    ["created_by", "file_path"], where_is_null=("deleted_at",)
)
_FOLDERS_PATH_CONFLICT = ConflictTarget.partial(
    ["created_by", "organization_id", "folder_path"], where_is_null=("deleted_at",)
)

_SYNC_LIST_FIELDS = (
    "id",
    "file_path",
    "size_bytes",
    "mime_type",
    "current_version",
    "checksum",
    "updated_at",
    "created_at",
)

# The sandbox polling feed is replay-safe and should yield to infrastructure
# readiness well before the latter's five-second database budget. The ORM
# retries a timed-out read once on a freshly acquired connection, so this
# two-second command timeout bounds the complete feed read to roughly four
# seconds rather than letting one stale TLS/database operation hold a pool
# connection for the default ten seconds.
CHANGE_FEED_STATEMENT_TIMEOUT_SECONDS = 2.0

# Everything a device replica needs to maintain a local file index —
# includes ``deleted_at`` (tombstones ride the change feed) and excludes the
# server-only ``storage_uri`` and the potentially-large ``metadata`` blob.
_SYNC_CHANGE_FIELDS = (
    "id",
    "file_path",
    "file_name",
    "mime_type",
    "size_bytes",
    "checksum",
    "published_to_web",
    "shown_to",
    "current_version",
    "parent_folder_id",
    "created_at",
    "updated_at",
    "deleted_at",
    # Feed v2 (SPEC-SERVER §2.3). Nothing was removed.
    # Which device wrote the row, so a daemon recognizes its own echo instead of
    # re-downloading it; NULL = not written by a registered device.
    "origin_device_id",
    # What the client's clock said when it last changed on disk. Conflict
    # presentation only -- the feed orders by updated_at and nothing else.
    "client_modified_at",
    # NOT optional on the entry: v1 scoping stays on created_by (D13), but every
    # entry says which organization the row belongs to so the engine can stamp its
    # writes EXPLICITLY (no-db-assigned-org) and v1.1 org scoping is a filter
    # change, not a shape change.
    "organization_id",
)

_SYNC_FOLDER_FIELDS = (
    "id",
    "folder_path",
    "folder_name",
    "parent_id",
    "published_to_web",
    "shown_to",
    "is_system",
    "created_at",
    "updated_at",
    "deleted_at",
)


def _models():
    """Lazy model access — also the loud not-bound gate.

    Import is deferred so ``matrx_files`` package import never requires a
    bound database; the FIRST actual DB call screams via ensure_bound() if
    startup wiring forgot bind_to_host()/bootstrap_db().
    """
    from matrx_files.db import ensure_bound

    ensure_bound()
    from matrx_files.db import models_files, models_iam

    return models_files, models_iam


def _norm(value: Any) -> Any:
    """Normalize a DB value to the wire shape PostgREST used to return."""
    if isinstance(value, datetime | date):
        return value.isoformat()
    if isinstance(value, UUID):
        return str(value)
    if isinstance(value, Enum):
        return value.value
    return value


def _row(instance: Any) -> dict | None:
    if instance is None:
        return None
    return {k: _norm(v) for k, v in instance.to_dict().items()}


def _rows(instances: list[Any] | None) -> list[dict]:
    return [_row(i) for i in (instances or [])]


def _vals(dicts: list[dict] | None) -> list[dict]:
    return [{k: _norm(v) for k, v in d.items()} for d in (dicts or [])]



def _with_system_folder_marker(data: dict) -> dict:
    """THE folder door's stamp: a folder the system owns carries ``metadata.system_artifact``.

    Derived from the folder's path (:func:`matrx_files.user_visible.system_folder_marker`), so no
    writer has to remember it; ``platform._inventory_filter`` hides a stamped folder unless the
    person turned ``files.show_system_files`` on.
    """
    stamped = stamp_system_folder(data.get("folder_path"), data.get("metadata"))
    if stamped is data.get("metadata"):
        return data
    return {**data, "metadata": stamped}


class DatabaseClient:
    """File-system DB access through the package's own matrx-orm models."""

    def __init__(self, config: CloudSyncConfig) -> None:
        self._config = config

    # ------------------------------------------------------------------
    # RPC plumbing — SECURITY DEFINER functions via the ORM primitive
    # ------------------------------------------------------------------

    @staticmethod
    def _db_name() -> str:
        from matrx_files.db import ensure_bound

        return ensure_bound()

    async def _rpc(self, schema: str, function: str, *args: Any, mode: str = "scalar") -> Any:
        from matrx_orm import call_function

        return await call_function(self._db_name(), schema, function, *args, mode=mode)

    def _rpc_sync(self, schema: str, function: str, *args: Any, mode: str = "scalar") -> Any:
        from matrx_orm import call_function_sync

        return call_function_sync(self._db_name(), schema, function, *args, mode=mode)

    # ------------------------------------------------------------------
    # Generic helpers
    # ------------------------------------------------------------------

    @staticmethod
    def _strip_none(data: dict) -> dict:
        """Remove keys with None values so Postgres uses defaults."""
        return {k: v for k, v in data.items() if v is not None}

    # ------------------------------------------------------------------
    # owner_id <-> created_by boundary shim (files / folders only)
    # ------------------------------------------------------------------
    # The 2026 DB canonicalization renamed the owner column on the entity
    # tables (files.files / files.folders) from ``owner_id`` to the
    # canonical ``created_by``. The whole Python layer (CloudFile/CloudFolder
    # models, sync_engine, every aidream caller — 200+ references) still
    # speaks ``owner_id``, so we translate in EXACTLY ONE place: here, at the
    # DB boundary. Writes map owner_id -> created_by on the way in; reads add
    # owner_id back from created_by on the way out, so callers that construct
    # models OR read ``row["owner_id"]`` directly are unchanged.
    # Sibling tables keep their own owner columns and never touch this shim:
    # uploads_inflight / idempotency / webhooks -> owner_id (unchanged);
    # user_account / user_storage_usage / file_rag_jobs -> user_id;
    # file_versions -> created_by (its model already uses it); share links
    # live in canonical platform.share_links (created_by there too).

    @classmethod
    def _owner_to_db(cls, data: dict) -> dict:
        """files/folders write-prep: owner_id->created_by."""
        out = data
        if "owner_id" in out:
            out = {k: v for k, v in out.items() if k != "owner_id"}
            out["created_by"] = data["owner_id"]
        return out

    @staticmethod
    def _owner_from_db(row: dict | None) -> dict | None:
        """files/folders read: expose created_by (DB) as owner_id (Python)."""
        if row is not None and "created_by" in row and "owner_id" not in row:
            return {**row, "owner_id": row["created_by"]}
        return row

    @classmethod
    def _owner_from_db_many(cls, rows: list[dict] | None) -> list[dict]:
        return [cls._owner_from_db(r) for r in (rows or [])]

    # ==================================================================
    # FILES
    # ==================================================================

    def get_file(self, file_id: str, *, include_deleted: bool = False) -> dict | None:
        mf, _ = _models()
        flt: dict[str, Any] = {"id": file_id}
        if not include_deleted:
            flt["deleted_at__isnull"] = True
        return self._owner_from_db(_row(mf.Files.filter(**flt).first_sync()))

    async def get_file_async(
        self, file_id: str, *, include_deleted: bool = False
    ) -> dict[str, Any] | None:
        mf, _ = _models()
        flt: dict[str, Any] = {"id": file_id}
        if not include_deleted:
            flt["deleted_at__isnull"] = True
        return self._owner_from_db(_row(await mf.Files.filter(**flt).first()))

    def get_file_by_path(self, owner_id: str, file_path: str) -> dict | None:
        mf, _ = _models()
        return self._owner_from_db(
            _row(
                mf.Files.filter(
                    created_by=owner_id, file_path=file_path, deleted_at__isnull=True
                ).first_sync()
            )
        )

    async def get_file_by_path_async(self, owner_id: str, file_path: str) -> dict[str, Any] | None:
        mf, _ = _models()
        return self._owner_from_db(
            _row(
                await mf.Files.filter(
                    created_by=owner_id, file_path=file_path, deleted_at__isnull=True
                ).first()
            )
        )

    async def get_tombstone_by_path_async(
        self, owner_id: str, file_path: str
    ) -> dict[str, Any] | None:
        """The most recently trashed row at ``file_path``, or None.

        The path-keyed twin of :meth:`get_file_by_path_async` for the one
        question a replica write must answer before it lands where no live row
        exists: "did the cloud just remove a file at this path?" A replica that
        missed that removal still holds the bytes and would otherwise put the
        file back as a brand-new row (Lane E defect b, 2026-10-21).
        """
        mf, _ = _models()
        return self._owner_from_db(
            _row(
                await mf.Files.filter(
                    created_by=owner_id, file_path=file_path, deleted_at__isnull=False
                )
                .order_by("-deleted_at")
                .first()
            )
        )

    async def find_derivative_async(
        self,
        *,
        parent_file_id: str,
        derivation_kind: str,
        metadata_key: str,
        metadata_value: str,
        owner_id: str | None = None,
    ) -> dict[str, Any] | None:
        """Find one live derivative by lineage plus an exact JSONB key.

        This is the reusable cache lookup for deterministic derivatives such
        as PDF page selections and rendered variants. ``owner_id`` is optional
        because some internal derivatives remain owned by the source owner,
        while user-triggered exports are owned by the requesting user.
        """
        mf, _ = _models()
        filters: dict[str, Any] = {
            "parent_file_id": parent_file_id,
            "derivation_kind": derivation_kind,
            "derivation_metadata__json_key": (metadata_key, metadata_value),
            "deleted_at__isnull": True,
        }
        if owner_id is not None:
            filters["created_by"] = owner_id
        row = await mf.Files.filter(**filters).order_by("created_at").first()
        return self._owner_from_db(_row(row))

    # ------------------------------------------------------------------
    # Dedup lookups by content hash. Used by the FileService intent
    # contract (intent='create' / 'alias_existing' / 'force_new_copy').
    # Returns the OLDEST non-deleted, non-duplicate row in the scope so
    # the keeper is stable across calls.
    # ------------------------------------------------------------------

    def _checksum_query(self, checksum: str, owner_id: str | None, organization_id: str | None):
        mf, _ = _models()
        q = mf.Files.filter(
            checksum=checksum,
            deleted_at__isnull=True,
            duplicate_of_file_id__isnull=True,
            parent_file_id__isnull=True,
        )
        if organization_id is not None:
            # The live uniqueness invariant is (organization, owner,
            # checksum), not organization-wide. Cross-member aliasing would
            # return another member's private row without granting access.
            if owner_id is None:
                return None
            q = q.filter(organization_id=organization_id, created_by=owner_id)
        elif owner_id is not None:
            q = q.filter(created_by=owner_id, organization_id__isnull=True)
        else:
            return None
        return q.order_by("created_at").limit(1)

    def get_file_by_checksum(
        self,
        checksum: str,
        *,
        owner_id: str | None = None,
        organization_id: str | None = None,
    ) -> dict | None:
        if not checksum:
            return None
        q = self._checksum_query(checksum, owner_id, organization_id)
        if q is None:
            return None
        return self._owner_from_db(_row(q.first_sync()))

    async def get_file_by_checksum_async(
        self,
        checksum: str,
        *,
        owner_id: str | None = None,
        organization_id: str | None = None,
    ) -> dict | None:
        """Find the canonical (oldest, non-deleted, non-duplicate-alias)
        files.files row for a given content checksum.

        When ``organization_id`` is provided, the canonical scope is that
        owner inside that organization. Otherwise it is the owner's personal
        library. Derivatives are never canonical uploads. Returns ``None`` if
        no match.
        """
        if not checksum:
            return None
        q = self._checksum_query(checksum, owner_id, organization_id)
        if q is None:
            return None
        return self._owner_from_db(_row(await q.first()))

    def upsert_file(self, data: dict) -> dict:
        mf, _ = _models()
        cleaned = self._owner_to_db(self._strip_none(normalize_derivation_payload(data)))
        if "id" in cleaned:
            # Pinned-id insert — plain insert, never an ON CONFLICT upsert.
            # See upsert_file_async for the full rationale (a concurrent
            # collision would otherwise rewrite the winning row's primary
            # key and orphan its pending file_versions insert).
            return self._owner_from_db(_row(mf.Files.create_sync(**cleaned)))
        return self._owner_from_db(
            _row(mf.Files.upsert_sync(cleaned, on_conflict=_FILES_PATH_CONFLICT))
        )

    async def upsert_file_async(self, data: dict) -> dict:
        mf, _ = _models()
        cleaned = self._owner_to_db(self._strip_none(normalize_derivation_payload(data)))
        if "id" in cleaned:
            # Pinned-id insert (canonical-key scheme: TUS / AI media /
            # variants). A pinned id means a brand-new row — it must NEVER
            # be an ``ON CONFLICT (owner_id, file_path) DO UPDATE`` upsert.
            # On a concurrent collision that upsert runs ``SET id=<new uuid>``
            # against the row that already won (owner_id, file_path),
            # rewriting THAT row's primary key (the FK to file_versions
            # is ON DELETE CASCADE with no ON UPDATE, so a not-yet-referenced
            # id is freely mutable) and orphaning the winner's pending
            # file_versions insert (FK 23503). A plain insert instead raises
            # a unique-violation on a genuine path collision, which the
            # caller's race-recovery path resolves by reading the winning row.
            return self._owner_from_db(_row(await mf.Files.create(**cleaned)))
        return self._owner_from_db(
            _row(await mf.Files.upsert(cleaned, on_conflict=_FILES_PATH_CONFLICT))
        )

    def update_file(
        self, file_id: str, updates: dict, *, clear_columns: tuple[str, ...] = ()
    ) -> dict | None:
        """``updates`` drops None values (the column keeps its value). A column
        that must become NULL is named in ``clear_columns`` — explicit, never
        inferred from a None."""
        mf, _ = _models()
        cleaned = self._owner_to_db(self._strip_none(normalize_derivation_payload(updates)))
        cleaned.update(dict.fromkeys(clear_columns))
        result = mf.Files.update_where_sync({"id": file_id}, **cleaned)
        if not result.rows_affected:
            return None
        return self.get_file(file_id, include_deleted=True)

    async def update_file_async(
        self, file_id: str, updates: dict, *, clear_columns: tuple[str, ...] = ()
    ) -> dict | None:
        """Async twin of :meth:`update_file` (``clear_columns`` = explicit NULLs)."""
        mf, _ = _models()
        cleaned = self._owner_to_db(self._strip_none(normalize_derivation_payload(updates)))
        cleaned.update(dict.fromkeys(clear_columns))
        result = await mf.Files.update_where({"id": file_id}, **cleaned)
        if not result.rows_affected:
            return None
        return await self.get_file_async(file_id, include_deleted=True)

    def soft_delete_file(self, file_id: str) -> bool:
        # Prefer the cascade-aware SQL function which also deactivates share
        # links pointing at the file. Falls back to the column-only update if
        # the RPC isn't installed (older schemas).
        try:
            return bool(self._rpc_sync("files", "soft_delete_file", file_id))
        except Exception:
            mf, _ = _models()
            result = mf.Files.update_where_sync({"id": file_id}, deleted_at=datetime.now(UTC))
            return bool(result.rows_affected)

    async def soft_delete_file_async(self, file_id: str) -> bool:
        try:
            return bool(await self._rpc("files", "soft_delete_file", file_id))
        except Exception:
            mf, _ = _models()
            result = await mf.Files.update_where({"id": file_id}, deleted_at=datetime.now(UTC))
            return bool(result.rows_affected)

    # Hard delete: returns the storage URIs that need to be purged from S3.
    #
    # Both entries run inside ``purge_escape(file_id)`` — one transaction
    # carrying ``matrx.purge_root_id`` — because migration 033 put a BEFORE
    # DELETE trigger on ``files.files`` refusing any row whose tombstone is
    # younger than ``files.min_tombstone_retention_days()`` (D23, 90-day floor).
    # A delete-forever is the lawful exception and names the ROOT of its
    # cascade, so the trigger permits that root and every descendant of it;
    # ``hard_delete_file`` soft-stamps each row it is about to delete, so a
    # single-id escape would abort on the first never-trashed child. The escape
    # must be set in the SAME transaction as the delete, which is why it lives
    # here at the DB boundary and not in a route.
    def hard_delete_file(self, file_id: str) -> dict | None:
        return drive_sync(lambda: self.hard_delete_file_async(file_id))

    async def hard_delete_file_async(self, file_id: str) -> dict | None:
        async def _call() -> dict | None:
            data = await self._rpc("files", "hard_delete_file", file_id)
            return data if isinstance(data, dict) else None

        return await purge_escaped(file_id, _call)

    # ------------------------------------------------------------------
    # THE ONLY LAWFUL RENAME / MOVE PATH (SPEC-SERVER §4.2, §4.3)
    # ------------------------------------------------------------------
    # ``file_path`` is NOT NULL, is half of the unique key
    # ``cld_files_owner_id_file_path_key (created_by, file_path) WHERE
    # deleted_at IS NULL``, and is the field the sync feed sends to devices.
    # Writing ``file_name`` or ``parent_folder_id`` without recomputing it
    # corrupts the row silently — that is the defect these two wrappers exist
    # to make unrepeatable. Nothing anywhere may pass ``file_name`` /
    # ``file_path`` / ``parent_folder_id`` to ``update_file_async``; the
    # blocking guard is ``aidream/scripts/check_single_rename_path.py``, whose
    # allowlist is exactly these two methods.

    # Postgres SQLSTATE → the typed Python error the ONE api mapper
    # (matrx_files.api.errors.map_exception) turns into the right HTTP status.
    #
    # BOTH no-data spellings are listed on purpose. `RAISE ... USING
    # ERRCODE='no_data_found'` inside plpgsql resolves to the PL/pgSQL condition
    # NO_DATA_FOUND, which is SQLSTATE **P0002** — NOT the SQL-standard 02000 the
    # name suggests. Matching only 02000 turned every "file not found" from these
    # RPCs into an unmapped 500 (caught by test_rename_move_file.py, which
    # asserted the wrong one first and was corrected by the live database).
    _RENAME_MOVE_SQLSTATE_HTTP = {
        "42501": 403,  # insufficient_privilege     -> PermissionError
        "P0002": 404,  # plpgsql NO_DATA_FOUND      -> FileNotFoundError
        "02000": 404,  # SQL-standard no_data_found -> FileNotFoundError
        "23505": 409,  # unique_violation           -> FilePathConflictError
        "22023": 400,  # invalid_parameter_value    -> ValueError
    }

    @staticmethod
    def _raise_rename_move(exc: Exception, *, file_id: str) -> None:
        """Re-raise an RPC failure as the typed error its SQLSTATE means.

        Never swallows: an unrecognised SQLSTATE (or no SQLSTATE at all) is
        re-raised untouched so the ONE mapper logs it with a traceback.
        """
        sqlstate = getattr(exc, "sqlstate", None) or getattr(exc, "pgcode", None)
        message = str(exc).strip() or type(exc).__name__
        if sqlstate == "42501":
            raise PermissionError(message) from exc
        if sqlstate in ("P0002", "02000"):
            raise FileNotFoundError(message) from exc
        if sqlstate == "23505":
            from matrx_files.dedup import FilePathConflictError

            raise FilePathConflictError(file_path=message) from exc
        if sqlstate == "22023":
            raise ValueError(message) from exc
        raise exc

    async def rename_file_async(self, file_id: str, new_name: str) -> dict[str, Any]:
        """``public.rename_file`` — rename in place, ``file_path`` recomputed.

        Returns the RPC receipt ``{file_id, old_path, new_path, file_name}``.
        ``file_id`` is stable; ``organization_id`` is never touched.
        """
        try:
            receipt = await self._rpc("public", "rename_file", file_id, new_name)
        except Exception as exc:
            self._raise_rename_move(exc, file_id=file_id)
            raise  # unreachable — _raise_rename_move always raises
        return self._rpc_dict(receipt)

    async def move_file_async(self, file_id: str, new_parent_folder_id: str | None) -> dict[str, Any]:
        """``public.move_file`` — reparent, ``file_path`` recomputed from the folder.

        ``new_parent_folder_id=None`` means the organization's user-visible
        root. Returns ``{file_id, old_path, new_path, folder_id}``; when
        ``old_path`` and ``new_path`` differ by more than the last segment the
        caller MUST show the user where the file lands before moving it (S20).
        """
        try:
            receipt = await self._rpc("public", "move_file", file_id, new_parent_folder_id)
        except Exception as exc:
            self._raise_rename_move(exc, file_id=file_id)
            raise  # unreachable — _raise_rename_move always raises
        return self._rpc_dict(receipt)

    def rename_file(self, file_id: str, new_name: str) -> dict[str, Any]:
        """Sync twin of :meth:`rename_file_async` (sync contexts only)."""
        try:
            receipt = self._rpc_sync("public", "rename_file", file_id, new_name)
        except Exception as exc:
            self._raise_rename_move(exc, file_id=file_id)
            raise  # unreachable
        return self._rpc_dict(receipt)

    def move_file(self, file_id: str, new_parent_folder_id: str | None) -> dict[str, Any]:
        """Sync twin of :meth:`move_file_async` (sync contexts only)."""
        try:
            receipt = self._rpc_sync("public", "move_file", file_id, new_parent_folder_id)
        except Exception as exc:
            self._raise_rename_move(exc, file_id=file_id)
            raise  # unreachable
        return self._rpc_dict(receipt)

    @staticmethod
    def _merge_hard_delete_purge(
        primary: dict | None,
        extra: dict | None,
    ) -> dict[str, object]:
        merged: dict[str, object] = {
            "main": None,
            "versions": [],
            "main_retained": False,
            "retained": [],
        }
        for report in (primary, extra):
            if not report:
                continue
            if report.get("main") and merged["main"] is None:
                merged["main"] = report["main"]
            elif report.get("main"):
                merged["versions"] = [
                    *list(merged["versions"]),
                    report["main"],
                ]
            merged["versions"] = [
                *list(merged["versions"]),
                *(report.get("versions") or []),
            ]
            merged["main_retained"] = bool(merged["main_retained"]) or bool(
                report.get("main_retained")
            )
            merged["retained"] = [
                *list(merged["retained"]),
                *(report.get("retained") or []),
            ]
        return merged

    @staticmethod
    def _alias_groups(rows: list[dict[str, Any]]) -> list[list[dict[str, Any]]]:
        groups: dict[tuple[object, object, object], list[dict[str, Any]]] = {}
        for row in rows:
            key = (row.get("organization_id"), row.get("created_by"), row.get("checksum"))
            groups.setdefault(key, []).append(row)
        return list(groups.values())

    @staticmethod
    def _alias_heir(rows: list[dict[str, Any]]) -> dict[str, Any]:
        return min(
            rows,
            key=lambda row: (
                row.get("deleted_at") is not None,
                str(row.get("created_at") or ""),
                str(row["id"]),
            ),
        )

    def _rehome_aliases_for_hard_delete(self, mf: Any, file_id: str) -> None:
        aliases = mf.Files.filter(duplicate_of_file_id=file_id).values_sync(
            "id", "organization_id", "created_by", "checksum", "created_at", "deleted_at"
        )
        if not aliases:
            return
        mf.Files.update_where_sync(
            {"id": file_id}, deleted_at=datetime.now(UTC)
        )
        for group in self._alias_groups(aliases):
            sample = group[0]
            root = mf.Files.filter(
                organization_id=sample.get("organization_id"),
                created_by=sample.get("created_by"),
                checksum=sample.get("checksum"),
                duplicate_of_file_id=None,
                parent_file_id=None,
                deleted_at=None,
            ).first_sync()
            root_id = _row(root).get("id") if root is not None else None
            if root_id is None:
                heir = self._alias_heir(group)
                root_id = heir["id"]
                mf.Files.update_where_sync({"id": root_id}, duplicate_of_file_id=None)
            for alias in group:
                if alias["id"] != root_id:
                    mf.Files.update_where_sync(
                        {"id": alias["id"]}, duplicate_of_file_id=root_id
                    )

    async def _rehome_aliases_for_hard_delete_async(self, mf: Any, file_id: str) -> None:
        aliases = await mf.Files.filter(duplicate_of_file_id=file_id).values(
            "id", "organization_id", "created_by", "checksum", "created_at", "deleted_at"
        )
        if not aliases:
            return
        await mf.Files.update_where({"id": file_id}, deleted_at=datetime.now(UTC))
        for group in self._alias_groups(aliases):
            sample = group[0]
            root = await mf.Files.filter(
                organization_id=sample.get("organization_id"),
                created_by=sample.get("created_by"),
                checksum=sample.get("checksum"),
                duplicate_of_file_id=None,
                parent_file_id=None,
                deleted_at=None,
            ).first()
            root_id = _row(root).get("id") if root is not None else None
            if root_id is None:
                heir = self._alias_heir(group)
                root_id = heir["id"]
                await mf.Files.update_where({"id": root_id}, duplicate_of_file_id=None)
            for alias in group:
                if alias["id"] != root_id:
                    await mf.Files.update_where(
                        {"id": alias["id"]}, duplicate_of_file_id=root_id
                    )

    def _partition_referenced_uris(self, mf: Any, uris: list[str]) -> tuple[list[str], list[str]]:
        purge: list[str] = []
        retained: list[str] = []
        for uri in dict.fromkeys(uris):
            referenced = mf.Files.filter(storage_uri=uri).first_sync() is not None
            if not referenced:
                referenced = mf.FileVersions.filter(storage_uri=uri).first_sync() is not None
            (retained if referenced else purge).append(uri)
        return purge, retained

    async def _partition_referenced_uris_async(
        self, mf: Any, uris: list[str]
    ) -> tuple[list[str], list[str]]:
        purge: list[str] = []
        retained: list[str] = []
        for uri in dict.fromkeys(uris):
            referenced = await mf.Files.filter(storage_uri=uri).first() is not None
            if not referenced:
                referenced = await mf.FileVersions.filter(storage_uri=uri).first() is not None
            (retained if referenced else purge).append(uri)
        return purge, retained

    def hard_delete_file_fallback(self, file_id: str) -> dict | None:
        """ORM cascade fallback for when the SQL fn is unavailable.

        Delegates to the async twin rather than running a sync cascade of its
        own: the D23 retention escape is a transaction-local GUC, and every
        ``*_sync`` ORM call is its own transaction, where such a GUC has no
        meaning. One escaped transaction, both twins.
        """
        return drive_sync(lambda: self.hard_delete_file_fallback_async(file_id))

    async def hard_delete_file_fallback_async(self, file_id: str) -> dict | None:
        return await purge_escaped(file_id, lambda: self._hard_delete_cascade_async(file_id))

    async def _hard_delete_cascade_async(self, file_id: str) -> dict | None:
        """The ORM cascade itself. Recurses into children; ``purge_escape`` is
        re-entrant, so the root's transaction and root id cover every level."""
        mf, mi = _models()
        child_purge: dict | None = None
        for child in await mf.Files.filter(parent_file_id=file_id).values("id"):
            child_purge = self._merge_hard_delete_purge(
                child_purge,
                await self._hard_delete_cascade_async(child["id"]),
            )

        row = await self.get_file_async(file_id, include_deleted=True)
        if row is None:
            # Nothing more is deleted here, so the children's retained decisions hold.
            return child_purge or {"main": None, "versions": [], "main_retained": False, "retained": []}
        # AD238: the children decided ``retained`` while THIS row still existed. Those
        # URIs are re-checked below, after this row is deleted — retained only if a
        # SURVIVING row still names them. Only the children's purge URIs merge as-is.
        child_retained = list((child_purge or {}).get("retained") or [])
        child_cleared = (
            {"main": child_purge.get("main"), "versions": child_purge.get("versions") or []}
            if child_purge
            else None
        )
        version_rows = await mf.FileVersions.filter(file_id=file_id).values("storage_uri")
        version_uris = [r["storage_uri"] for r in version_rows if r.get("storage_uri")]
        await self._rehome_aliases_for_hard_delete_async(mf, file_id)
        await self._share_model().delete_where(resource_id=file_id, resource_type="file")
        await mi.Permissions.delete_where(resource_id=file_id, resource_type="file")
        await mf.UploadsInflight.delete_where(file_id=file_id)
        await mf.FileRagJobs.delete_where(file_id=file_id)
        # hard-delete-ok: system purge executor (hard_delete_and_purge), never a person's button
        await mf.PageAnnotations.delete_where(file_id=file_id)
        # hard-delete-ok: system purge executor (hard_delete_and_purge), never a person's button
        await mf.Entities.delete_where(file_id=file_id)
        # hard-delete-ok: system purge executor (hard_delete_and_purge), never a person's button
        await mf.Overrides.delete_where(file_id=file_id)
        # hard-delete-ok: system purge executor (hard_delete_and_purge), never a person's button
        await mf.AnalysisResult.delete_where(file_id=file_id)
        # hard-delete-ok: system purge executor (hard_delete_and_purge), never a person's button
        await mf.Pages.delete_where(file_id=file_id)
        # hard-delete-ok: system purge executor (hard_delete_and_purge), never a person's button
        await mf.Analysis.delete_where(file_id=file_id)
        await mf.Structure.delete_where(file_id=file_id)
        await mf.FileVersions.delete_where(file_id=file_id)
        # hard-delete-ok: system purge executor (hard_delete_and_purge), never a person's button
        await mf.Files.delete_where(id=file_id)
        candidates = [u for u in [row.get("storage_uri"), *version_uris, *child_retained] if u]
        purge_uris, retained = await self._partition_referenced_uris_async(mf, candidates)
        main_uri = row.get("storage_uri")
        main_retained = bool(main_uri and main_uri in retained)
        return self._merge_hard_delete_purge(
            {
                "main": None if main_retained else main_uri,
                "versions": [u for u in purge_uris if u != main_uri],
                "main_retained": main_retained,
                "retained": retained,
            },
            child_cleared,
        )

    @staticmethod
    def _rpc_dict(data: Any) -> dict[str, Any]:
        if isinstance(data, dict):
            return data
        if isinstance(data, list) and data and isinstance(data[0], dict):
            return data[0]
        return {}

    async def get_user_limits_async(self, user_id: str, is_guest: bool = False) -> dict[str, Any]:
        return self._rpc_dict(await self._rpc("billing", "get_user_limits", user_id, is_guest))

    async def check_upload_quota_async(
        self,
        user_id: str,
        size_bytes: int,
        is_guest: bool = False,
    ) -> dict[str, Any]:
        return self._rpc_dict(
            await self._rpc("files", "check_upload_quota", user_id, size_bytes, is_guest)
        )

    async def apply_usage_delta_async(
        self,
        user_id: str,
        *,
        bytes_delta: int,
        files_delta: int,
        record_upload: bool = False,
        upload_bytes: int = 0,
    ) -> None:
        await self._rpc(
            "billing",
            "apply_usage_delta",
            user_id,
            bytes_delta,
            files_delta,
            record_upload,
            upload_bytes,
        )

    async def get_usage_status_async(
        self,
        user_id: str,
        is_guest: bool = False,
    ) -> dict[str, Any]:
        return self._rpc_dict(await self._rpc("billing", "get_usage_status", user_id, is_guest))

    async def check_rate_limit_async(
        self,
        actor_id: str,
        kind: str,
        limit: int,
    ) -> dict[str, Any]:
        try:
            data = await self._rpc("files", "check_file_rate_limit", actor_id, kind, limit)
        except Exception:
            data = await self._rpc("billing", "check_rate_limit", actor_id, kind, limit)
        return self._rpc_dict(data)

    async def append_event_async(
        self,
        event_type: str,
        *,
        actor_id: str | None,
        organization_id: str | None = None,
        actor_type: str = "user",
        resource_type: str | None = None,
        resource_id: str | None = None,
        payload: dict[str, Any] | None = None,
        request_id: str | None = None,
        ip_address: str | None = None,
    ) -> None:
        if actor_id is None:
            logger.warning(
                "Dropping activity event %s because no actor_id was supplied",
                event_type,
            )
            return
        # The event's organization is the one the caller names, else the one
        # the request context CARRIES. It is never the actor's personal
        # workspace: an activity row parked in the wrong tenant is invisible to
        # the organization that the action actually happened in, and nothing
        # reports it (context-is-carried-never-rebuilt.md rule 4).
        event_organization_id = organization_id
        if event_organization_id is None:
            from matrx_utils.ctx import get_active_organization_id

            carried = get_active_organization_id()
            event_organization_id = str(carried) if carried else None
        if event_organization_id is None:
            logger.warning(
                "Dropping activity event %s for actor %s: no organization was "
                "carried. Pass organization_id= (the row's own organization) or "
                "run it inside a request context that carries one — an activity "
                "row is never filed in the actor's personal organization.",
                event_type,
                actor_id,
            )
            return
        event_payload = {
            **(payload or {}),
            "actor_id": actor_id,
            "actor_type": actor_type,
            "request_id": request_id,
            "ip_address": ip_address,
        }
        await self._rpc(
            "platform",
            "log_activity",
            event_organization_id,
            event_type,
            resource_type,
            resource_id,
            event_payload,
            actor_id,
            mode="none",
        )

    def list_files(self, owner_id: str, folder_id: str | list[str] | None = None) -> list[dict]:
        mf, _ = _models()
        q = mf.Files.filter(created_by=owner_id, deleted_at__isnull=True)
        if isinstance(folder_id, list):
            q = q.filter(parent_folder_id__in=folder_id)
        elif folder_id is not None:
            q = q.filter(parent_folder_id=folder_id)
        return self._owner_from_db_many(_rows(q.order_by("file_path").all_sync()))

    async def list_files_async(
        self, owner_id: str, folder_id: str | list[str] | None = None
    ) -> list[dict]:
        mf, _ = _models()
        q = mf.Files.filter(created_by=owner_id, deleted_at__isnull=True)
        if isinstance(folder_id, list):
            q = q.filter(parent_folder_id__in=folder_id)
        elif folder_id is not None:
            q = q.filter(parent_folder_id=folder_id)
        return self._owner_from_db_many(_rows(await q.order_by("file_path").all()))

    async def list_files_paginated_async(
        self,
        owner_id: str,
        prefix: str | None = None,
        limit: int = 1000,
        *,
        include_system: bool = True,
        organization_id: str,
    ) -> list[dict]:
        """Bounded listing for a user's files in ONE organization, optional path prefix.

        Pushes the prefix filter + ``limit`` into the database instead of
        pulling every row and filtering in Python — same loop-stall class as
        ``list_changed_files_async``.

        ``organization_id`` is REQUIRED and pushed into the query: an absent
        organization would read every tenant this owner belongs to, and
        filtering a page in Python after the ``limit`` has been applied returns
        a short page that looks like the end of the list.
        """
        if not organization_id:
            raise ValueError(
                "organization_id is required: an absent organization is a refusal, "
                "never every tenant. Read it off the carried request context "
                "(context_organization_id) and pass it."
            )
        mf, _ = _models()
        q = mf.Files.filter(
            created_by=owner_id, organization_id=organization_id, deleted_at__isnull=True
        )
        if prefix:
            q = q.filter(file_path__startswith=prefix)
        if not include_system:
            from matrx_orm import Q

            from matrx_files.system_paths import SystemPathRegistry

            for root in SystemPathRegistry.roots():
                q = q.filter(~Q(file_path__startswith=f"{root}/"))
        rows = await q.order_by("file_path").limit(limit).values(*_SYNC_LIST_FIELDS)
        return self._owner_from_db_many(_vals(rows))

    async def list_files_filtered_async(
        self,
        created_by: str,
        *,
        folder_id: str | None = None,
        mime_prefix: str | None = None,
        offset: int = 0,
        limit: int = 50,
    ) -> list[dict]:
        """Owner-scoped file listing with folder + mime-prefix filters and
        offset pagination — the canonical primitive behind the ``cloud_file``
        agent tool's ``list`` action.

        Scoped by the canonical ``created_by`` column (NEVER the legacy
        ``owner_id`` alias, which is being annihilated). Selects an explicit
        safe field set — ``SAFE_FILE_FIELDS`` — so the server-only
        ``storage_uri`` can never leave the server, and returns rows AS-IS
        (no ``owner_id`` shim re-added). Newest first.
        """
        mf, _ = _models()
        q = mf.Files.filter(created_by=created_by, deleted_at__isnull=True)
        if folder_id:
            q = q.filter(parent_folder_id=folder_id)
        if mime_prefix:
            q = q.filter(mime_type__startswith=mime_prefix)
        rows = await q.order_by("-created_at").offset(offset).limit(limit).values(*SAFE_FILE_FIELDS)
        return _vals(rows)

    async def get_storage_usage_async(self, owner_id: str, *, organization_id: str) -> dict:
        """Total bytes + file count for a user IN ONE ORGANIZATION, parsed lean.

        Selects only ``size_bytes`` (not ``*``) so even for a user with many
        files the response is tiny and its parse can't stall the loop.
        """
        if not organization_id:
            raise ValueError(
                "organization_id is required: an absent organization is a refusal, "
                "never every tenant. Read it off the carried request context "
                "(context_organization_id) and pass it."
            )
        mf, _ = _models()
        rows = await mf.Files.filter(
            created_by=owner_id, organization_id=organization_id, deleted_at__isnull=True
        ).values(
            "size_bytes"
        )
        total = sum(int(r.get("size_bytes") or 0) for r in rows)
        return {"used_bytes": total, "files_count": len(rows)}

    async def list_changed_files_async(
        self,
        owner_id: str,
        since_iso: str,
        limit: int = 1000,
        *,
        include_system: bool = True,
        organization_id: str,
    ) -> list[dict]:
        """Server-side "changes since" query for the down-sync poll fallback.

        Filters ``updated_at > since`` and bounds the result set in the
        database — instead of pulling every one of a user's rows and filtering
        in Python. A narrow column set + a hard ``limit`` keeps the response
        small enough that parsing can never stall the event loop (the
        2026-06-12 ``event_loop_stall``). ``organization_id`` is REQUIRED — the
        feed a sandbox down-syncs is one tenant's, never every tenant the owner
        belongs to.
        """
        if not organization_id:
            raise ValueError(
                "organization_id is required: an absent organization is a refusal, "
                "never every tenant. Read it off the carried request context "
                "(context_organization_id) and pass it."
            )
        mf, _ = _models()
        from matrx_orm import Q

        from matrx_files.system_paths import SystemPathRegistry

        since = datetime.fromisoformat(since_iso.replace("Z", "+00:00"))
        q = mf.Files.filter(
            created_by=owner_id,
            organization_id=organization_id,
            deleted_at__isnull=True,
            updated_at__gt=since,
        )
        if not include_system:
            for root in SystemPathRegistry.roots():
                q = q.filter(~Q(file_path__startswith=f"{root}/"))
        rows = await (
            q.order_by("updated_at")
            .limit(limit)
            .timeout(CHANGE_FEED_STATEMENT_TIMEOUT_SECONDS)
            .replay_safe_empty()
            .values(*_SYNC_LIST_FIELDS)
        )
        return self._owner_from_db_many(_vals(rows))

    async def list_sync_changes_async(
        self,
        owner_id: str,
        *,
        cursor_ts: datetime | None = None,
        cursor_id: str | None = None,
        include_deleted: bool = False,
        include_system: bool = False,
        limit: int = 500,
    ) -> list[dict]:
        """Keyset-paginated change feed for device replicas (desktop sync).

        Ordered by ``(updated_at, id)`` with a composite cursor so pages can
        never skip rows that share an ``updated_at`` timestamp. Tombstones
        (``deleted_at`` set) are INCLUDED when ``include_deleted`` — the
        ``platform._touch_row`` trigger stamps ``updated_at`` on soft-delete
        and restore, so deletions ride the same cursor. System-path content
        (``generations/``, ``system-files/`` — see ``system_paths``) is
        excluded unless ``include_system``: it is app-managed, never part of
        a user's visible file tree.
        """
        from matrx_orm import Q
        from matrx_orm.core.expressions import DbFunction, F, Is

        from matrx_files.user_visible import path_visible_filters, row_visible_filters

        mf, _ = _models()
        q = mf.Files.filter(created_by=owner_id)
        # Stability lag: rows stamped within the last few seconds may belong
        # to transactions that were not yet visible when an earlier page ran —
        # advancing a cursor past them would skip rows forever. The feed
        # simply never serves the newest sliver; the next poll gets it.
        stability_cutoff = datetime.now(UTC) - timedelta(seconds=10)
        q = q.filter(updated_at__lte=stability_cutoff)
        if not include_deleted:
            q = q.filter(deleted_at__isnull=True)
        # The "not derived" half of THE rule is unconditional: `include_system`
        # means "ignore the path half", and it never re-admits derivative rows
        # (824 alive rows are parentless variants, so both columns are needed).
        q = q.filter(**row_visible_filters())
        if not include_system:
            # The path half, one declaration (matrx_files.user_visible).
            # `file_path__user_visible` is matrx-orm's registered path-family lookup:
            # it emits `files.is_user_visible_path(file_path) = $n` verbatim, which is
            # the SAME expression idx_files_sync_feed_owner_updated_id is partial over.
            # Spelling it as NOT LIKE conjuncts does not imply the index predicate and
            # costs the scan (measured live: 11,177 with a Sort against 13.83).
            q = q.filter(**path_visible_filters())
        # Crawl artifacts are a PROVENANCE test, not an access shape (S2), so they
        # stay a separate conjunct and are excluded even when include_system is on:
        # scraped page bytes are never a user's file. The partial index has already
        # narrowed the scan, so this per-row cross-schema EXISTS runs over the page,
        # not the table (0 of 8,868 candidate rows on the heaviest owner).
        q = q.filter(Is(DbFunction("files.is_crawl_artifact", F("id")), False))
        if cursor_ts is not None:
            if cursor_id:
                q = q.filter(
                    Q(updated_at__gt=cursor_ts) | (Q(updated_at=cursor_ts) & Q(id__gt=cursor_id))
                )
            else:
                q = q.filter(updated_at__gt=cursor_ts)
        rows = await q.order_by("updated_at", "id").limit(limit).values(*_SYNC_CHANGE_FIELDS)
        return _vals(rows)

    async def list_all_folders_async(
        self,
        owner_id: str,
        *,
        cursor_ts: datetime | None = None,
        cursor_id: str | None = None,
        include_deleted: bool = False,
        include_system: bool = False,
        limit: int = 500,
    ) -> list[dict]:
        """Keyset-paginated folder feed — the folder half of a device replica.

        Adopts the file feed's contract verbatim (SPEC-SERVER §2.4): the same
        ``(updated_at, id)`` keyset, the same 10 s stability lag, the same
        bootstrap-alive-then-tombstone-aware flip, the same opaque cursor codec.

        It is NOT "small cardinality": one live account holds 42,756 folders,
        so the old single bounded page of 5,000 could never build that replica
        at all — it returned ``truncated: true`` and there was no way forward.
        """
        from matrx_orm import Q

        mf, _ = _models()
        q = mf.Folders.filter(created_by=owner_id)
        # Same stability lag as the file feed, for the same reason: a row
        # stamped inside the window may belong to a transaction that was not
        # visible when an earlier page ran, and advancing the cursor past it
        # would skip it forever.
        q = q.filter(updated_at__lte=datetime.now(UTC) - timedelta(seconds=10))
        if not include_deleted:
            q = q.filter(deleted_at__isnull=True)
        if not include_system:
            # THE folder rule, one declaration (matrx_files.user_visible
            # FOLDER_CONJUNCTS -> files.is_user_visible_folder_path): the system
            # namespaces AND the machine namespaces (coding-sessions/, tool-images/),
            # the same call the browser tree's folder branch makes (D16).
            from matrx_orm.core.expressions import DbFunction, F, Is

            from matrx_files.user_visible import FOLDER_PREDICATE_FUNCTION

            q = q.filter(Is(DbFunction(FOLDER_PREDICATE_FUNCTION, F("folder_path")), True))
        if cursor_ts is not None:
            if cursor_id:
                q = q.filter(
                    Q(updated_at__gt=cursor_ts) | (Q(updated_at=cursor_ts) & Q(id__gt=cursor_id))
                )
            else:
                q = q.filter(updated_at__gt=cursor_ts)
        rows = await q.order_by("updated_at", "id").limit(limit).values(*_SYNC_FOLDER_FIELDS)
        return _vals(rows)

    async def list_folder_subtree_async(
        self,
        owner_id: str,
        folder_id: str,
        folder_path: str,
        *,
        include_deleted: bool = True,
    ) -> list[dict]:
        """One folder and every folder beneath it — UNBOUNDED, by design.

        Separate from the sync folder feed on purpose. The feed is a paged,
        stability-lagged replica stream; a subtree purge needs the WHOLE tree at
        this instant, and a page bound would silently purge part of it (one live
        account holds 42,756 folders, so the feed's old 5,000-row cap was
        already a silent short read here).
        """
        from matrx_orm import Q

        mf, _ = _models()
        q = mf.Folders.filter(created_by=owner_id)
        if not include_deleted:
            q = q.filter(deleted_at__isnull=True)
        q = q.filter(Q(id=folder_id) | Q(folder_path__startswith=f"{folder_path}/"))
        rows = await q.order_by("folder_path").values(*_SYNC_FOLDER_FIELDS)
        return _vals(rows)

    async def list_files_in_folders_async(
        self,
        folder_ids: list[str],
        *,
        include_deleted: bool = False,
    ) -> list[dict]:
        """Every file whose parent folder is in ``folder_ids``.

        Trash-purge of a folder tree needs ``include_deleted=True`` —
        soft-deleted children live in the same folders.
        """
        if not folder_ids:
            return []
        mf, _ = _models()
        q = mf.Files.filter(parent_folder_id__in=list(folder_ids))
        if not include_deleted:
            q = q.filter(deleted_at__isnull=True)
        return self._owner_from_db_many(_rows(await q.all()))

    def list_variants_by_master(self, master_file_id: str) -> list[dict]:
        """Every files.files row whose metadata.derived_from == master_file_id.

        Backs the VariantsService 'look before render' check — given a
        master, returns the catalog of already-rendered variants so we
        can skip the encoder for keys that already exist.
        """
        mf, _ = _models()
        return self._owner_from_db_many(
            _rows(
                mf.Files.filter(
                    metadata__json_key=("derived_from", master_file_id),
                    deleted_at__isnull=True,
                ).all_sync()
            )
        )

    async def list_variants_by_master_async(self, master_file_id: str) -> list[dict]:
        mf, _ = _models()
        return self._owner_from_db_many(
            _rows(
                await mf.Files.filter(
                    metadata__json_key=("derived_from", master_file_id),
                    deleted_at__isnull=True,
                ).all()
            )
        )

    # ==================================================================
    # FOLDERS
    # ==================================================================

    def get_folder(self, folder_id: str, *, include_deleted: bool = False) -> dict | None:
        mf, _ = _models()
        flt: dict[str, Any] = {"id": folder_id}
        if not include_deleted:
            flt["deleted_at__isnull"] = True
        return self._owner_from_db(_row(mf.Folders.filter(**flt).first_sync()))

    async def get_folder_async(
        self, folder_id: str, *, include_deleted: bool = False
    ) -> dict | None:
        """One folder by id, owner-shimmed.

        ``include_deleted`` mirrors ``get_file_async`` and exists so trash paths
        stop hand-rolling `_row(Folders.filter(...))`: the bare row carries the
        DB's `created_by` but NOT the `owner_id` alias every consumer reads, so
        those hand-rolled reads raised `KeyError: 'owner_id'`. Always come
        through here — the shim lives in exactly one place.
        """
        mf, _ = _models()
        flt: dict[str, Any] = {"id": folder_id}
        if not include_deleted:
            flt["deleted_at__isnull"] = True
        return self._owner_from_db(_row(await mf.Folders.filter(**flt).first()))

    # A person's folder tree is PER ORGANIZATION (Arman 2026-10-10: every item has one home
    # scope; the organization follows the home). Folder identity is (owner, organization, path)
    # — unique key ``folders_owner_org_path_key`` — so a lookup that will PLACE something names
    # the organization; another organization's folder at the same path is never the answer.

    def get_folder_by_path(
        self, owner_id: str, folder_path: str, organization_id: str
    ) -> dict | None:
        mf, _ = _models()
        return self._owner_from_db(
            _row(
                mf.Folders.filter(
                    created_by=owner_id,
                    organization_id=organization_id,
                    folder_path=folder_path,
                    deleted_at__isnull=True,
                ).first_sync()
            )
        )

    async def get_folder_by_path_async(
        self, owner_id: str, folder_path: str, organization_id: str
    ) -> dict | None:
        mf, _ = _models()
        return self._owner_from_db(
            _row(
                await mf.Folders.filter(
                    created_by=owner_id,
                    organization_id=organization_id,
                    folder_path=folder_path,
                    deleted_at__isnull=True,
                ).first()
            )
        )

    def get_folders_by_path(self, owner_id: str, folder_path: str) -> list[dict]:
        """Every live folder the owner has at ``folder_path`` — one per organization. For READS
        (listing a path), which never narrow to one organization."""
        mf, _ = _models()
        return self._owner_from_db_many(
            _rows(
                mf.Folders.filter(
                    created_by=owner_id, folder_path=folder_path, deleted_at__isnull=True
                ).all_sync()
            )
        )

    async def get_folders_by_path_async(self, owner_id: str, folder_path: str) -> list[dict]:
        """Async ``get_folders_by_path``."""
        mf, _ = _models()
        return self._owner_from_db_many(
            _rows(
                await mf.Folders.filter(
                    created_by=owner_id, folder_path=folder_path, deleted_at__isnull=True
                ).all()
            )
        )

    # ------------------------------------------------------------------
    # Soft-deleted folder recovery.
    #
    # The (created_by, organization_id, folder_path) uniqueness that ``create_folder`` collides
    # with does NOT exclude soft-deleted rows, while every lookup above filters
    # ``deleted_at__isnull=True``. A trashed folder therefore becomes a
    # permanent write barrier: the lookup says "absent", the INSERT says
    # "duplicate", and the caller has no live row to fall back to. The pair
    # below closes that gap — see ``SyncEngine._ensure_folder``.
    # ------------------------------------------------------------------

    def get_folder_by_path_any_state(
        self, owner_id: str, folder_path: str, organization_id: str
    ) -> dict | None:
        """Owner's folder at ``folder_path`` in ``organization_id``, trashed or not (live wins)."""
        mf, _ = _models()
        return self._owner_from_db(
            _row(
                mf.Folders.filter(
                    created_by=owner_id, organization_id=organization_id, folder_path=folder_path
                )
                .order_by("-deleted_at")
                .first_sync()
            )
        )

    async def get_folder_by_path_any_state_async(
        self, owner_id: str, folder_path: str, organization_id: str
    ) -> dict | None:
        """Async ``get_folder_by_path_any_state``."""
        mf, _ = _models()
        return self._owner_from_db(
            _row(
                await mf.Folders.filter(
                    created_by=owner_id, organization_id=organization_id, folder_path=folder_path
                )
                .order_by("-deleted_at")
                .first()
            )
        )

    def restore_folder(self, folder_id: str) -> dict | None:
        """Clear ``deleted_at`` on a folder, returning the live row."""
        mf, _ = _models()
        result = mf.Folders.update_where_sync({"id": folder_id}, deleted_at=None)
        if not result.rows_affected:
            return None
        return self.get_folder(folder_id)

    async def restore_folder_async(self, folder_id: str) -> dict | None:
        """Async ``restore_folder``."""
        mf, _ = _models()
        result = await mf.Folders.update_where({"id": folder_id}, deleted_at=None)
        if not result.rows_affected:
            return None
        return await self.get_folder_async(folder_id)

    def create_folder(self, data: dict) -> dict:
        """Insert a folder without overwriting a concurrent path winner."""
        mf, _ = _models()
        cleaned = self._owner_to_db(self._strip_none(_with_system_folder_marker(data)))
        return self._owner_from_db(_row(mf.Folders.create_sync(**cleaned)))

    async def create_folder_async(self, data: dict) -> dict:
        """Insert a folder without overwriting a concurrent path winner."""
        mf, _ = _models()
        cleaned = self._owner_to_db(self._strip_none(_with_system_folder_marker(data)))
        return self._owner_from_db(_row(await mf.Folders.create(**cleaned)))

    def upsert_folder(self, data: dict) -> dict:
        mf, _ = _models()
        cleaned = self._owner_to_db(self._strip_none(data))
        return self._owner_from_db(
            _row(mf.Folders.upsert_sync(cleaned, on_conflict=_FOLDERS_PATH_CONFLICT))
        )

    async def upsert_folder_async(self, data: dict) -> dict:
        mf, _ = _models()
        cleaned = self._owner_to_db(self._strip_none(data))
        return self._owner_from_db(
            _row(await mf.Folders.upsert(cleaned, on_conflict=_FOLDERS_PATH_CONFLICT))
        )

    def list_folders(self, owner_id: str, parent_id: str | list[str] | None = None) -> list[dict]:
        mf, _ = _models()
        q = mf.Folders.filter(created_by=owner_id, deleted_at__isnull=True)
        if isinstance(parent_id, list):
            q = q.filter(parent_id__in=parent_id)
        elif parent_id is not None:
            q = q.filter(parent_id=parent_id)
        return self._owner_from_db_many(_rows(q.order_by("folder_path").all_sync()))

    async def list_folders_async(
        self, owner_id: str, parent_id: str | list[str] | None = None
    ) -> list[dict]:
        mf, _ = _models()
        q = mf.Folders.filter(created_by=owner_id, deleted_at__isnull=True)
        if isinstance(parent_id, list):
            q = q.filter(parent_id__in=parent_id)
        elif parent_id is not None:
            q = q.filter(parent_id=parent_id)
        return self._owner_from_db_many(_rows(await q.order_by("folder_path").all()))

    # ==================================================================
    # VERSIONS
    # ==================================================================

    def create_version(self, data: dict) -> dict:
        mf, _ = _models()
        return _row(mf.FileVersions.create_sync(**self._strip_none(data)))

    async def create_version_async(self, data: dict) -> dict:
        mf, _ = _models()
        return _row(await mf.FileVersions.create(**self._strip_none(data)))

    def list_versions(self, file_id: str) -> list[dict]:
        mf, _ = _models()
        return _rows(mf.FileVersions.filter(file_id=file_id).order_by("-version_number").all_sync())

    async def list_versions_async(self, file_id: str) -> list[dict]:
        mf, _ = _models()
        return _rows(
            await mf.FileVersions.filter(file_id=file_id).order_by("-version_number").all()
        )

    def get_version(self, file_id: str, version_number: int) -> dict | None:
        mf, _ = _models()
        return _row(
            mf.FileVersions.filter(file_id=file_id, version_number=version_number).first_sync()
        )

    async def get_version_async(self, file_id: str, version_number: int) -> dict | None:
        mf, _ = _models()
        return _row(
            await mf.FileVersions.filter(file_id=file_id, version_number=version_number).first()
        )

    # ==================================================================
    # PERMISSIONS  (canonical iam.permissions)
    # ==================================================================
    #
    # File ACLs moved off the deprecated ``cld_file_permissions`` table
    # onto the canonical ``iam.permissions`` (resource_type + resource_id
    # + granted_to_user_id / granted_to_organization_id, permission_level
    # enum viewer<editor<admin, created_by, status='active'). The user-group
    # feature is dead — only direct user grants (and, for completeness, org
    # grants) are supported here.
    #
    # The method signatures + the dict shape callers pass/receive are kept
    # stable (resource_id, resource_type, grantee_id, grantee_type,
    # permission_level in read/write/admin, granted_by, expires_at) so call
    # sites in service.py / sync_engine.py / permissions.py are unchanged.
    # Translation to/from the canonical columns happens here, in one place.

    # legacy file-ACL level  <->  canonical permission_level enum
    _LEVEL_TO_CANONICAL = {"read": "viewer", "write": "editor", "admin": "admin"}
    # Keyed by the canonical ladder, so it must cover EVERY level — a missing
    # key made `.get(level, level)` hand the legacy caller a canonical word it
    # does not speak, silently. `commenter` maps to `read`: the legacy file-ACL
    # vocabulary has no comment tier, and a commenter can certainly read.
    _LEVEL_FROM_CANONICAL = {
        "viewer": "read",
        "commenter": "read",
        "editor": "write",
        "admin": "admin",
    }

    @classmethod
    def _to_canonical_permission(cls, data: dict) -> dict:
        """Map a legacy file-ACL grant dict onto a iam.permissions row."""
        grantee_type = data.get("grantee_type") or "user"
        if grantee_type not in ("user", "organization"):
            # 'group' (and anything else) is the dead user-group path.
            raise ValueError(
                f"Unsupported grantee_type {grantee_type!r}; the user-group "
                "ACL path is removed — only 'user'/'organization' grants exist."
            )
        level = data.get("permission_level") or "read"
        row: dict[str, Any] = {
            "resource_type": data["resource_type"],
            "resource_id": data["resource_id"],
            "permission_level": cls._LEVEL_TO_CANONICAL.get(level, level),
            "created_by": data.get("granted_by"),
            "status": "active",
            "expires_at": data.get("expires_at"),
        }
        if grantee_type == "organization":
            row["granted_to_organization_id"] = data["grantee_id"]
        else:
            row["granted_to_user_id"] = data["grantee_id"]
        return row

    @classmethod
    def _from_canonical_permission(cls, row: dict) -> dict:
        """Map a iam.permissions row back to the legacy file-ACL shape
        that callers expect (permission_level read/write/admin, grantee_*)."""
        if row.get("granted_to_organization_id"):
            grantee_type = "organization"
            grantee_id = row.get("granted_to_organization_id")
        else:
            grantee_type = "user"
            grantee_id = row.get("granted_to_user_id")
        level = row.get("permission_level")
        return {
            **row,
            "grantee_type": grantee_type,
            "grantee_id": grantee_id,
            "permission_level": cls._LEVEL_FROM_CANONICAL.get(level, level),
            "granted_by": row.get("created_by"),
        }

    @staticmethod
    def _permission_conflict_cols(grantee_type: str) -> list[str]:
        return (
            ["resource_type", "resource_id", "granted_to_organization_id"]
            if grantee_type == "organization"
            else ["resource_type", "resource_id", "granted_to_user_id"]
        )

    def upsert_permission(self, data: dict) -> dict:
        _, mi = _models()
        row = self._strip_none(self._to_canonical_permission(data))
        conflict = self._permission_conflict_cols(data.get("grantee_type") or "user")
        return self._from_canonical_permission(
            _row(mi.Permissions.upsert_sync(row, on_conflict=conflict))
        )

    async def upsert_permission_async(self, data: dict) -> dict:
        _, mi = _models()
        row = self._strip_none(self._to_canonical_permission(data))
        conflict = self._permission_conflict_cols(data.get("grantee_type") or "user")
        return self._from_canonical_permission(
            _row(await mi.Permissions.upsert(row, on_conflict=conflict))
        )

    @staticmethod
    def _permission_delete_filters(
        resource_id: str, resource_type: str, grantee_id: str, grantee_type: str
    ) -> dict:
        flt: dict[str, Any] = {
            "resource_type": resource_type,
            "resource_id": resource_id,
        }
        if grantee_type == "organization":
            flt["granted_to_organization_id"] = grantee_id
        else:
            flt["granted_to_user_id"] = grantee_id
        return flt

    def delete_permission(
        self,
        resource_id: str,
        resource_type: str,
        grantee_id: str,
        grantee_type: str = "user",
    ) -> bool:
        _, mi = _models()
        count = mi.Permissions.delete_where_sync(
            **self._permission_delete_filters(resource_id, resource_type, grantee_id, grantee_type)
        )
        return bool(count)

    async def delete_permission_async(
        self,
        resource_id: str,
        resource_type: str,
        grantee_id: str,
        grantee_type: str = "user",
    ) -> bool:
        _, mi = _models()
        count = await mi.Permissions.delete_where(
            **self._permission_delete_filters(resource_id, resource_type, grantee_id, grantee_type)
        )
        return bool(count)

    def list_permissions(self, resource_id: str, resource_type: str) -> list[dict]:
        _, mi = _models()
        rows = _rows(
            mi.Permissions.filter(
                resource_type=resource_type, resource_id=resource_id, status="active"
            ).all_sync()
        )
        return [self._from_canonical_permission(r) for r in rows]

    async def list_permissions_async(self, resource_id: str, resource_type: str) -> list[dict]:
        _, mi = _models()
        rows = _rows(
            await mi.Permissions.filter(
                resource_type=resource_type, resource_id=resource_id, status="active"
            ).all()
        )
        return [self._from_canonical_permission(r) for r in rows]

    def get_user_permission(
        self,
        resource_id: str,
        resource_type: str,
        user_id: str,
    ) -> dict | None:
        """Get the direct user permission for a resource, if any."""
        _, mi = _models()
        row = _row(
            mi.Permissions.filter(
                resource_type=resource_type,
                resource_id=resource_id,
                granted_to_user_id=user_id,
                status="active",
            ).first_sync()
        )
        return self._from_canonical_permission(row) if row else None

    async def get_user_permission_async(
        self,
        resource_id: str,
        resource_type: str,
        user_id: str,
    ) -> dict | None:
        _, mi = _models()
        row = _row(
            await mi.Permissions.filter(
                resource_type=resource_type,
                resource_id=resource_id,
                granted_to_user_id=user_id,
                status="active",
            ).first()
        )
        return self._from_canonical_permission(row) if row else None

    def has_platform_viewer_access(
        self,
        user_id: str,
        resource_type: str,
        resource_id: str,
    ) -> bool:
        """Ask ``public.has_access_as`` — the platform judge with an explicit user.

        Used for Shared Knowledge / reachability cascades (e.g. industry grant
        on a data_store → member file). Service-role connections cannot use
        ``iam.has_access`` (``auth.uid()`` is NULL); this function takes
        ``p_user``. Viewer only — never elevates to write/admin.
        """
        if not user_id or not resource_id:
            return False
        return bool(
            self._rpc_sync("public", "has_access_as", user_id, resource_type, resource_id, "viewer")
        )

    async def has_platform_viewer_access_async(
        self,
        user_id: str,
        resource_type: str,
        resource_id: str,
    ) -> bool:
        """Async twin of :meth:`has_platform_viewer_access`."""
        if not user_id or not resource_id:
            return False
        return bool(
            await self._rpc(
                "public", "has_access_as", user_id, resource_type, resource_id, "viewer"
            )
        )

    # ==================================================================
    # SHARE LINKS
    # ==================================================================

    @staticmethod
    def _share_model():
        """The canonical share-link model — ``platform.share_links``.

        Share links live in the ONE platform-wide table (hand-maintained
        model, see ``matrx_files/db/models_platform.py``); the legacy
        ``files.share_links`` lane is retired.
        """
        from matrx_files.db import models_platform

        return models_platform.PlatformShareLinks

    @staticmethod
    def _prepared_share_link(data: dict, org_id: str | None) -> dict:
        """Fill token + organization_id before insert.

        Token format matches the canonical ``create_share_link`` RPC
        (64 hex chars). organization_id is resolved from the resource's org
        when the caller didn't supply one.
        """
        out = dict(data)
        if not out.get("token"):
            out["token"] = secrets.token_hex(32)
        if not out.get("organization_id") and org_id:
            out["organization_id"] = org_id
        return out

    def _resolve_resource_org_sync(self, resource_type: str, resource_id: str) -> str | None:
        mf, _ = _models()
        model = mf.Files if resource_type == "file" else mf.Folders
        rows = model.filter(id=resource_id).limit(1).values_sync("organization_id")
        return str(rows[0]["organization_id"]) if rows and rows[0].get("organization_id") else None

    async def _resolve_resource_org(self, resource_type: str, resource_id: str) -> str | None:
        mf, _ = _models()
        model = mf.Files if resource_type == "file" else mf.Folders
        rows = await model.filter(id=resource_id).limit(1).values("organization_id")
        return str(rows[0]["organization_id"]) if rows and rows[0].get("organization_id") else None

    def create_share_link(self, data: dict) -> dict:
        org = self._resolve_resource_org_sync(
            data.get("resource_type", "file"), data.get("resource_id", "")
        )
        prepared = self._prepared_share_link(self._strip_none(data), org)
        return _row(self._share_model().create_sync(**prepared))

    async def create_share_link_async(self, data: dict) -> dict:
        org = await self._resolve_resource_org(
            data.get("resource_type", "file"), data.get("resource_id", "")
        )
        prepared = self._prepared_share_link(self._strip_none(data), org)
        return _row(await self._share_model().create(**prepared))

    def _share_link_query(self, token: str):
        # Inline the is_active + expires_at filter so callers don't have to
        # defensively re-check (closes the C3 leak where deactivated /
        # expired links continued to resolve).
        from matrx_orm import Q

        return (
            self._share_model()
            .filter(token=token, is_active=True)
            .filter(Q(expires_at__isnull=True) | Q(expires_at__gt=datetime.now(UTC)))
        )

    @staticmethod
    def _unexhausted(link: dict | None) -> dict | None:
        """None-out a link whose max_uses budget is spent (read paths don't
        consume, so exhaustion is checked here rather than in SQL)."""
        if not link:
            return None
        max_uses = link.get("max_uses")
        if max_uses is not None and (link.get("use_count") or 0) >= max_uses:
            return None
        return link

    def get_share_link(self, token: str) -> dict | None:
        """Validate (active, unexpired, unexhausted) WITHOUT consuming a use."""
        return self._unexhausted(_row(self._share_link_query(token).first_sync()))

    async def get_share_link_async(self, token: str) -> dict | None:
        return self._unexhausted(_row(await self._share_link_query(token).first()))

    def list_share_links(self, resource_id: str, resource_type: str) -> list[dict]:
        return _rows(
            self._share_model()
            .filter(resource_id=resource_id, resource_type=resource_type, is_active=True)
            .all_sync()
        )

    async def list_share_links_async(self, resource_id: str, resource_type: str) -> list[dict]:
        return _rows(
            await self._share_model()
            .filter(resource_id=resource_id, resource_type=resource_type, is_active=True)
            .all()
        )

    def deactivate_share_link(self, token: str) -> bool:
        result = self._share_model().update_where_sync({"token": token}, is_active=False)
        return bool(result.rows_affected)

    async def deactivate_share_link_async(self, token: str) -> bool:
        result = await self._share_model().update_where({"token": token}, is_active=False)
        return bool(result.rows_affected)

    @staticmethod
    def _consumed_link(data: Any) -> dict | None:
        if not data or not isinstance(data, dict) or not data.get("success"):
            return None
        return {
            "resource_type": data.get("resource_type"),
            "resource_id": data.get("resource_id"),
            "permission_level": data.get("permission_level"),
        }

    def consume_share_link(self, token: str) -> dict | None:
        """Atomically validate + consume one use of a share token.

        Delegates to the canonical ``iam.resolve_share_token(TEXT)`` RPC —
        the SAME resolver the FE ``/s/[token]`` page uses — which performs the
        revoked / expired / exhausted checks and the ``use_count`` increment
        in one statement. Returns ``{resource_type, resource_id,
        permission_level}`` or None when the token authorizes nothing.
        """
        return self._consumed_link(self._rpc_sync("iam", "resolve_share_token", token))

    async def consume_share_link_async(self, token: str) -> dict | None:
        return self._consumed_link(await self._rpc("iam", "resolve_share_token", token))

    async def share_link_child_file_async(self, token: str, file_id: str) -> dict | None:
        """Authorize ONE child file of a shared record for a share token.

        Delegates to ``iam.share_link_child_file(token, file_id)`` (access
        ladder T-19b): the token must be live (active, unexpired, within its use
        limit, type still link-shareable) and ``file_id`` must be a media part of
        a visible message of the ONE conversation that token shares. Does NOT
        consume a use — the page view did. Returns ``{file_id, resource_type,
        resource_id}`` or None when the token does not reach that file.
        """
        import uuid

        try:
            file_uuid = uuid.UUID(str(file_id))
        except (ValueError, TypeError):
            return None
        data = await self._rpc("iam", "share_link_child_file", token, file_uuid)
        if isinstance(data, str):
            import json

            data = json.loads(data)
        if not data or not isinstance(data, dict) or not data.get("success"):
            return None
        return {
            "file_id": str(data.get("file_id")),
            "resource_type": data.get("resource_type"),
            "resource_id": data.get("resource_id"),
        }

    # NOTE: the user-group ACL feature (cld_user_groups / cld_user_group_members)
    # was removed in the 2026 DB canonicalization — those tables are
    # deprecated and the group methods that used them are gone. File ACLs
    # are direct user/org grants in iam.permissions only.
