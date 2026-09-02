from __future__ import annotations

import asyncio
import time
from typing import Any

from pydantic import ValidationError

from matrx_ai.tools._dispatch_util import format_args_error
from matrx_ai.tools.arg_models import CloudFileArgs
from matrx_ai.tools.models import ToolContext, ToolError, ToolResult


def _get_sync_engine():
    """The host-injected FileManager's SyncEngine — the ONE sanctioned
    cloud-file layer. Hard-delete MUST go through its purge primitive
    (``hard_delete_and_purge_async``), never the raw DB fn, or S3 objects are
    orphaned (the C10 leak). See matrx_utils/file_handling/FEATURE.md."""
    from matrx_ai._ext import get_ext

    return get_ext("get_cloud_file_manager")().sync_engine


def _get_file_db():
    """The canonical cloud-file DB client (matrx-utils DatabaseClient), reached
    through the host-injected FileManager. This is the ONE sanctioned file-access
    layer — it binds the ``files`` schema in one place and speaks the canonical
    ``created_by`` column. Never hand-roll a supabase ``.table()`` at the dead
    ``cld_files`` name or the annihilated ``owner_id`` column again."""
    return _get_sync_engine().db


# Keys a client / agent may see per file row. Mirrors the canonical
# SAFE_FILE_FIELDS (created_by, NOT the annihilated owner_id alias; never the
# server-only storage_uri — files are identified by `id`; see
# matrx_utils/file_handling/FEATURE.md). Used to project get_file_async's
# SELECT * down to the safe outbound surface.
_SAFE_KEYS = frozenset(
    {
        "id", "created_by", "organization_id", "parent_folder_id", "file_path",
        "file_name", "mime_type", "size_bytes", "checksum", "visibility",
        "current_version", "width", "height", "duration_ms", "metadata",
        "created_at", "updated_at", "deleted_at",
    }
)


def _project_safe(row: dict) -> dict:
    """Strip a raw file row to the safe outbound surface (drops storage_uri,
    the legacy owner_id alias, and any other internal column)."""
    return {k: v for k, v in row.items() if k in _SAFE_KEYS}


def _stamp(result: ToolResult, started_at: float, ctx: ToolContext) -> ToolResult:
    result.tool_name = "cloud_file"
    result.call_id = ctx.call_id
    if not result.started_at:
        result.started_at = started_at
    if not result.completed_at:
        result.completed_at = time.time()
    return result


def _validation_error(message: str, started_at: float, ctx: ToolContext) -> ToolResult:
    return ToolResult(
        success=False,
        error=ToolError(error_type="validation", message=message),
        started_at=started_at,
        completed_at=time.time(),
        tool_name="cloud_file",
        call_id=ctx.call_id,
    )


def _not_found_error(file_id: str, started_at: float, ctx: ToolContext) -> ToolResult:
    return ToolResult(
        success=False,
        error=ToolError(
            error_type="not_found",
            message=f"File '{file_id}' not found or you do not own it.",
        ),
        started_at=started_at,
        completed_at=time.time(),
        tool_name="cloud_file",
        call_id=ctx.call_id,
    )


async def _authorized(file_id: str, user_id: str, level: str) -> dict | None:
    """Fetch a file the caller may act on at ``level``, or None.

    ACCESS, not ownership. The agent acts AS the user, so it must see exactly
    what the user can see — a file shared with them, granted to their org, or
    reachable through a container is legitimately theirs to read. The decision
    is the ONE DB policy (iam.has_access_for) behind the file layer's gate;
    never compare created_by here (that denies every shared file).
    """
    try:
        return await _get_sync_engine().get_authorized_record_async(
            file_id, user_id=user_id, level=level
        )
    except (FileNotFoundError, PermissionError):
        return None


async def _fetch_one(db, file_id: str, user_id: str) -> dict | None:
    """Fetch one non-deleted file the caller may READ, projected to the safe surface."""
    record = await _authorized(file_id, user_id, "read")
    return _project_safe(record) if record else None


async def _soft_delete(db, file_id: str, user_id: str) -> bool:
    """Access-checked soft delete — deleting requires ``admin`` on the file."""
    if await _authorized(file_id, user_id, "admin") is None:
        return False
    return await db.soft_delete_file_async(file_id)


async def _hard_delete(db, file_id: str, user_id: str) -> bool:
    """Access-checked hard delete (row + versions + S3) via the canonical purge
    primitive — cascades the DB rows AND purges every storage object. Requires
    ``admin`` on the file. Falls back to soft delete if the primitive raises."""
    record = await _authorized(file_id, user_id, "admin")
    if not record:
        return False
    try:
        await _get_sync_engine().hard_delete_and_purge_async(file_id, record.get("storage_uri"))
        return True
    except Exception:
        return await _soft_delete(db, file_id, user_id)


# ---------------------------------------------------------------------------
# cloud_file — unified action dispatcher
# ---------------------------------------------------------------------------

# Valid `cloud_file` actions are enforced by the CloudFileArgs discriminated union
# (arg_models/dispatcher_args.py) + tool_def.parameters."$variants" — the source of truth.


async def cloud_file(args: dict[str, Any], ctx: ToolContext) -> ToolResult:
    started_at = time.time()
    try:
        parsed = CloudFileArgs.model_validate(args).root
    except ValidationError as exc:
        return _validation_error(format_args_error(exc), started_at, ctx)
    action = parsed.action

    db = _get_file_db()
    user_id = ctx.user_id

    if action == "list":
        limit = max(1, min(int(args.get("limit", 50)), 500))
        offset = max(0, int(args.get("offset", 0)))
        folder_id = args.get("folder_id") or args.get("parent_folder_id")
        mime_prefix = args.get("mime_prefix")
        try:
            files = await db.list_files_filtered_async(
                user_id,
                folder_id=folder_id,
                mime_prefix=mime_prefix,
                offset=offset,
                limit=limit,
            )
            return _stamp(
                ToolResult(success=True, output={"files": files, "count": len(files), "offset": offset, "limit": limit}),
                started_at, ctx,
            )
        except Exception as exc:
            return _stamp(
                ToolResult(success=False, error=ToolError.from_exception(
                    exc,error_type="database", message=f"List failed: {exc}")),
                started_at, ctx,
            )

    if action == "get":
        file_id = (args.get("file_id") or "").strip()
        if not file_id:
            return _validation_error("file_id is required for action=get.", started_at, ctx)
        try:
            record = await _fetch_one(db, file_id, user_id)
            if not record:
                return _not_found_error(file_id, started_at, ctx)
            return _stamp(ToolResult(success=True, output={"file": record}), started_at, ctx)
        except Exception as exc:
            return _stamp(
                ToolResult(success=False, error=ToolError.from_exception(
                    exc,error_type="database", message=f"Get failed: {exc}")),
                started_at, ctx,
            )

    if action == "delete":
        file_id = (args.get("file_id") or "").strip()
        hard = bool(args.get("hard", False))
        if not file_id:
            return _validation_error("file_id is required for action=delete.", started_at, ctx)
        try:
            ok = await (_hard_delete(db, file_id, user_id) if hard else _soft_delete(db, file_id, user_id))
            if not ok:
                return _not_found_error(file_id, started_at, ctx)
            return _stamp(
                ToolResult(success=True, output={"deleted": True, "file_id": file_id, "hard": hard}),
                started_at, ctx,
            )
        except Exception as exc:
            return _stamp(
                ToolResult(success=False, error=ToolError.from_exception(
                    exc,error_type="database", message=f"Delete failed: {exc}")),
                started_at, ctx,
            )

    if action == "batch_get":
        file_ids = args.get("file_ids") or []
        if not isinstance(file_ids, list) or not file_ids:
            return _validation_error(
                "file_ids must be a non-empty list of UUID strings for action=batch_get.",
                started_at, ctx,
            )
        try:
            results = await asyncio.gather(*[_fetch_one(db, fid, user_id) for fid in file_ids])
            found = [r for r in results if r is not None]
            missing = [fid for fid, r in zip(file_ids, results, strict=False) if r is None]
            return _stamp(
                ToolResult(
                    success=True,
                    output={
                        "files": found,
                        "count": len(found),
                        "missing": missing,
                        "missing_count": len(missing),
                    },
                ),
                started_at, ctx,
            )
        except Exception as exc:
            return _stamp(
                ToolResult(success=False, error=ToolError.from_exception(
                    exc,error_type="database", message=f"Batch get failed: {exc}")),
                started_at, ctx,
            )

    # action == "batch_delete"
    file_ids = args.get("file_ids") or []
    hard = bool(args.get("hard", False))
    if not isinstance(file_ids, list) or not file_ids:
        return _validation_error(
            "file_ids must be a non-empty list of UUID strings for action=batch_delete.",
            started_at, ctx,
        )
    try:
        op = _hard_delete if hard else _soft_delete
        results = await asyncio.gather(*[op(db, fid, user_id) for fid in file_ids])
        deleted = [fid for fid, ok in zip(file_ids, results, strict=False) if ok]
        failed = [fid for fid, ok in zip(file_ids, results, strict=False) if not ok]
        return _stamp(
            ToolResult(
                success=True,
                output={
                    "deleted": deleted,
                    "deleted_count": len(deleted),
                    "failed": failed,
                    "failed_count": len(failed),
                    "hard": hard,
                },
            ),
            started_at, ctx,
        )
    except Exception as exc:
        return _stamp(
            ToolResult(success=False, error=ToolError.from_exception(
                exc,error_type="database", message=f"Batch delete failed: {exc}")),
            started_at, ctx,
        )
