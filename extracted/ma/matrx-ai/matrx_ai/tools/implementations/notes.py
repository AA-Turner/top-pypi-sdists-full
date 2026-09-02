from __future__ import annotations

import logging
import time
import traceback
from typing import Any

from pydantic import ValidationError

from matrx_ai.config.read_only_resources import READ_ONLY_TOOL_MESSAGE, is_resource_read_only
from matrx_ai.tools._dispatch_util import format_args_error
from matrx_ai.tools.arg_models import NoteArgs
from matrx_ai.tools.models import ToolContext, ToolError, ToolResult

logger = logging.getLogger(__name__)


async def _note_access_allowed(note_id: str, user_id: str, level: str) -> bool:
    """Canonical access check — ``iam.has_access_for(user, 'note', id, level)``.

    ACCESS, not ownership. The agent acts AS the user, so it must reach exactly
    what the user can reach in the UI — notes shared directly, via org, or
    conveyed through scope tagging all resolve inside the one SECURITY DEFINER
    body (see common-docs/systems/platform/access/STATE.md). Never re-implement
    any of that here. Fail-closed: any error reads as no access.

    The DB name is borrowed from the injection registry the same way
    ``database.py`` does — never hardcoded (package boundary).
    """
    try:
        from matrx_orm import call_function

        from matrx_ai.db._registry import get_model as get_db_model

        database = get_db_model("Notes")._database
        result = await call_function(
            database, "iam", "has_access_for",
            user_id, "note", note_id, level, mode="scalar",
        )
        return bool(result)
    except Exception:  # noqa: BLE001 — fail closed, never raise into the tool
        logger.warning("note access check failed for %s (level=%s)", note_id, level, exc_info=True)
        return False


async def _authorized_note(note_id: str, ctx: ToolContext, level: str) -> dict[str, Any] | None:
    """Fetch the note the caller may act on at ``level``, or None.

    Owner passes immediately (created_by); everyone else resolves through
    ``iam.has_access_for``. Levels mirror the canonical RLS policies: read =
    viewer, write = editor, delete = admin. Returns None for missing AND
    unauthorized alike — callers surface both as the same content-free
    not-found, so unauthorized probes learn nothing.
    """
    from matrx_ai.db.content_types.notes import notes_manager_instance

    result = await notes_manager_instance.get_note(note_id)
    if not result.get("success"):
        return None
    n = result["note"]
    if str(n.get("created_by") or "") == str(ctx.user_id):
        return n
    if await _note_access_allowed(note_id, str(ctx.user_id), level):
        return n
    return None


def _note_not_found(tool_name: str, started_at: float, ctx: ToolContext) -> ToolResult:
    """The ONE content-free not-found shape — identical for missing and unauthorized."""
    return ToolResult(
        success=False,
        error=ToolError(error_type="not_found", message="Note not found."),
        started_at=started_at, completed_at=time.time(),
        tool_name=tool_name, call_id=ctx.call_id,
    )


def _read_only_result(tool_name: str, started_at: float, ctx: ToolContext) -> ToolResult:
    return ToolResult(
        success=False,
        error=ToolError(error_type="read_only", message=READ_ONLY_TOOL_MESSAGE),
        started_at=started_at,
        completed_at=time.time(),
        tool_name=tool_name,
        call_id=ctx.call_id,
    )


async def note_get(args: dict[str, Any], ctx: ToolContext) -> ToolResult:
    started_at = time.time()
    note_id = args.get("note_id", "").strip()
    if not note_id:
        return ToolResult(
            success=False,
            error=ToolError(error_type="validation", message="note_id is required."),
            started_at=started_at, completed_at=time.time(),
            tool_name="note_get", call_id=ctx.call_id,
        )
    try:
        # Owner OR shared-with-user at viewer level; missing and unauthorized
        # return the same content-free not-found.
        n = await _authorized_note(note_id, ctx, "viewer")
        if n is None:
            return _note_not_found("note_get", started_at, ctx)
        return ToolResult(
            success=True,
            output={
                "id": n.get("id"),
                "label": n.get("label"),
                "folder_name": n.get("folder_name"),
                "content": n.get("content"),
                "tags": n.get("tags", []),
                "visibility": n.get("visibility"),
                "is_public": n.get("visibility") == "public",
                "created_at": n.get("created_at"),
                "updated_at": n.get("updated_at"),
            },
            started_at=started_at, completed_at=time.time(),
            tool_name="note_get", call_id=ctx.call_id,
        )
    except Exception as e:
        return ToolResult(
            success=False,
            error=ToolError(error_type="execution", message=str(e), traceback=traceback.format_exc(), is_retryable=True),
            started_at=started_at, completed_at=time.time(),
            tool_name="note_get", call_id=ctx.call_id,
        )


async def note_list(args: dict[str, Any], ctx: ToolContext) -> ToolResult:
    started_at = time.time()
    try:
        from matrx_ai.db.content_types.notes import notes_manager_instance
        from matrx_ai.tools.output_caps import TOOL_LIST_DEFAULT_LIMIT, cap_list
        limit = TOOL_LIST_DEFAULT_LIMIT
        result = await notes_manager_instance.list_notes_for_user(ctx.user_id)
        if not result.get("success"):
            return ToolResult(
                success=False,
                error=ToolError(error_type="execution", message=result.get("error", "Failed to list notes.")),
                started_at=started_at, completed_at=time.time(),
                tool_name="note_list", call_id=ctx.call_id,
            )
        notes = [
            {
                "id": n.get("id"),
                "label": n.get("label"),
                "folder_name": n.get("folder_name"),
                "tags": n.get("tags", []),
                "updated_at": n.get("updated_at"),
            }
            for n in result.get("notes", [])
        ]
        notes, info = cap_list(notes, limit=limit)
        output: dict[str, Any] = {"notes": notes, "count": info.total, "shown": info.shown}
        if info.truncated:
            output["truncated"] = True
            output["note"] = f"showing the {info.shown} most recent of {info.total} notes."
        return ToolResult(
            success=True,
            output=output,
            output_self_capped=True,  # compact rows + count cap ⇒ bounded result
            started_at=started_at, completed_at=time.time(),
            tool_name="note_list", call_id=ctx.call_id,
        )
    except Exception as e:
        return ToolResult(
            success=False,
            error=ToolError(error_type="execution", message=str(e), traceback=traceback.format_exc(), is_retryable=True),
            started_at=started_at, completed_at=time.time(),
            tool_name="note_list", call_id=ctx.call_id,
        )


async def note_create(args: dict[str, Any], ctx: ToolContext) -> ToolResult:
    started_at = time.time()
    label = args.get("label", "").strip()
    content = args.get("content", "").strip()
    if not label:
        return ToolResult(
            success=False,
            error=ToolError(error_type="validation", message="label is required.", suggested_action="Provide a title for the note."),
            started_at=started_at, completed_at=time.time(),
            tool_name="note_create", call_id=ctx.call_id,
        )
    try:
        from matrx_ai.db.content_types.notes import notes_manager_instance
        result = await notes_manager_instance.create_note(
            user_id=ctx.user_id,
            label=label,
            content=content,
            folder_name=args.get("folder_name", ""),
            tags=args.get("tags", []),
            is_public=args.get("is_public", False),
        )
        if not result.get("success"):
            return ToolResult(
                success=False,
                error=ToolError(error_type="execution", message=result.get("error", "Failed to create note.")),
                started_at=started_at, completed_at=time.time(),
                tool_name="note_create", call_id=ctx.call_id,
            )
        n = result["note"]
        return ToolResult(
            success=True,
            output={"id": n.get("id"), "label": n.get("label"), "folder_name": n.get("folder_name"), "created_at": n.get("created_at")},
            started_at=started_at, completed_at=time.time(),
            tool_name="note_create", call_id=ctx.call_id,
        )
    except Exception as e:
        return ToolResult(
            success=False,
            error=ToolError(error_type="execution", message=str(e), traceback=traceback.format_exc(), is_retryable=False),
            started_at=started_at, completed_at=time.time(),
            tool_name="note_create", call_id=ctx.call_id,
        )


async def note_update(args: dict[str, Any], ctx: ToolContext) -> ToolResult:
    started_at = time.time()
    note_id = args.get("note_id", "").strip()
    if not note_id:
        return ToolResult(
            success=False,
            error=ToolError(error_type="validation", message="note_id is required."),
            started_at=started_at, completed_at=time.time(),
            tool_name="note_update", call_id=ctx.call_id,
        )
    if is_resource_read_only(note_id):
        return _read_only_result("note_update", started_at, ctx)
    updates = {k: v for k, v in args.items() if k != "note_id"}
    if not updates:
        return ToolResult(
            success=False,
            error=ToolError(error_type="validation", message="At least one field to update is required.", suggested_action="Provide one or more of: label, content, folder_name, tags, is_public."),
            started_at=started_at, completed_at=time.time(),
            tool_name="note_update", call_id=ctx.call_id,
        )
    try:
        from matrx_ai.db.content_types.notes import notes_manager_instance
        if await _authorized_note(note_id, ctx, "editor") is None:
            return _note_not_found("note_update", started_at, ctx)
        result = await notes_manager_instance.update_note(note_id, **updates)
        if not result.get("success"):
            return ToolResult(
                success=False,
                error=ToolError(error_type="execution", message=result.get("error", "Update failed.")),
                started_at=started_at, completed_at=time.time(),
                tool_name="note_update", call_id=ctx.call_id,
            )
        n = result["note"]
        out: dict[str, Any] = {"id": n.get("id"), "label": n.get("label"), "updated_at": n.get("updated_at")}
        if result.get("warning_stripped_immutable"):
            out["warning"] = f"Ignored immutable fields: {result['warning_stripped_immutable']}"
        return ToolResult(
            success=True, output=out,
            started_at=started_at, completed_at=time.time(),
            tool_name="note_update", call_id=ctx.call_id,
        )
    except Exception as e:
        return ToolResult(
            success=False,
            error=ToolError(error_type="execution", message=str(e), traceback=traceback.format_exc(), is_retryable=True),
            started_at=started_at, completed_at=time.time(),
            tool_name="note_update", call_id=ctx.call_id,
        )


async def note_patch(args: dict[str, Any], ctx: ToolContext) -> ToolResult:
    started_at = time.time()
    note_id = args.get("note_id", "").strip()
    search_text = args.get("search_text", "")
    replacement_text = args.get("replacement_text", "")
    if not note_id:
        return ToolResult(
            success=False,
            error=ToolError(error_type="validation", message="note_id is required."),
            started_at=started_at, completed_at=time.time(),
            tool_name="note_patch", call_id=ctx.call_id,
        )
    if is_resource_read_only(note_id):
        return _read_only_result("note_patch", started_at, ctx)
    if not search_text:
        return ToolResult(
            success=False,
            error=ToolError(error_type="validation", message="search_text is required.", suggested_action="Provide a verbatim excerpt from the note content to find and replace."),
            started_at=started_at, completed_at=time.time(),
            tool_name="note_patch", call_id=ctx.call_id,
        )
    try:
        from matrx_ai.db.content_types.notes import notes_manager_instance
        if await _authorized_note(note_id, ctx, "editor") is None:
            return _note_not_found("note_patch", started_at, ctx)
        result = await notes_manager_instance.patch_note_content(note_id, search_text, replacement_text)
        if not result.get("success"):
            return ToolResult(
                success=False,
                error=ToolError(
                    error_type="not_found",
                    message=result.get("message", "No match found for the search text."),
                    suggested_action="Use note_get to read the current content and provide an exact excerpt.",
                ),
                started_at=started_at, completed_at=time.time(),
                tool_name="note_patch", call_id=ctx.call_id,
            )
        n = result["note"]
        return ToolResult(
            success=True,
            output={
                "id": n.get("id"),
                "matched_at_pass": result.get("matched_at_pass"),
                "updated_at": n.get("updated_at"),
            },
            started_at=started_at, completed_at=time.time(),
            tool_name="note_patch", call_id=ctx.call_id,
        )
    except Exception as e:
        return ToolResult(
            success=False,
            error=ToolError(error_type="execution", message=str(e), traceback=traceback.format_exc(), is_retryable=True),
            started_at=started_at, completed_at=time.time(),
            tool_name="note_patch", call_id=ctx.call_id,
        )


async def note_delete(args: dict[str, Any], ctx: ToolContext) -> ToolResult:
    started_at = time.time()
    note_id = args.get("note_id", "").strip()
    if not note_id:
        return ToolResult(
            success=False,
            error=ToolError(error_type="validation", message="note_id is required."),
            started_at=started_at, completed_at=time.time(),
            tool_name="note_delete", call_id=ctx.call_id,
        )
    if is_resource_read_only(note_id):
        return _read_only_result("note_delete", started_at, ctx)
    try:
        from matrx_ai.db.content_types.notes import notes_manager_instance
        if await _authorized_note(note_id, ctx, "admin") is None:
            return _note_not_found("note_delete", started_at, ctx)
        result = await notes_manager_instance.delete_note(note_id)
        if not result.get("success"):
            return ToolResult(
                success=False,
                error=ToolError(error_type="execution", message=result.get("error", "Delete failed.")),
                started_at=started_at, completed_at=time.time(),
                tool_name="note_delete", call_id=ctx.call_id,
            )
        return ToolResult(
            success=True,
            output={"deleted": True, "note_id": note_id},
            started_at=started_at, completed_at=time.time(),
            tool_name="note_delete", call_id=ctx.call_id,
        )
    except Exception as e:
        return ToolResult(
            success=False,
            error=ToolError(error_type="execution", message=str(e), traceback=traceback.format_exc(), is_retryable=False),
            started_at=started_at, completed_at=time.time(),
            tool_name="note_delete", call_id=ctx.call_id,
        )


# ---------------------------------------------------------------------------
# note — unified action dispatcher
# ---------------------------------------------------------------------------

# Valid `note` actions are enforced by the NoteArgs discriminated union
# (arg_models/dispatcher_args.py) + tool_def.parameters."$variants" — the source of truth.


def _note_stamp(result: ToolResult, started_at: float, ctx: ToolContext) -> ToolResult:
    result.tool_name = "note"
    result.call_id = ctx.call_id
    if not result.started_at:
        result.started_at = started_at
    if not result.completed_at:
        result.completed_at = time.time()
    return result


def _note_validation_error(message: str, started_at: float, ctx: ToolContext) -> ToolResult:
    return ToolResult(
        success=False,
        error=ToolError(error_type="validation", message=message),
        started_at=started_at,
        completed_at=time.time(),
        tool_name="note",
        call_id=ctx.call_id,
    )


async def note(args: dict[str, Any], ctx: ToolContext) -> ToolResult:
    started_at = time.time()
    try:
        parsed = NoteArgs.model_validate(args).root
    except ValidationError as exc:
        return _note_validation_error(format_args_error(exc), started_at, ctx)

    action = parsed.action
    inner_args = parsed.model_dump(exclude={"action"}, exclude_unset=True)

    impl = {
        "list": note_list,
        "get": note_get,
        "create": note_create,
        "update": note_update,
        "patch": note_patch,
        "delete": note_delete,
    }[action]

    return _note_stamp(await impl(inner_args, ctx), started_at, ctx)
