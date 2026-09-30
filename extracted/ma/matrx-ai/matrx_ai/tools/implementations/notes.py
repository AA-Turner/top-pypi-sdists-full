"""The `note` tool — list/get/create/update/patch/delete on workbench.notes.

EVERY ACTION RUNS AS THE PERSON. Each action opens the caller's RLS session
(``matrx_ai.tools.person_session.acts_as_the_person``) around its ORM work, so
Postgres row-level security decides which notes exist for them and which they
may change. This module never re-implements access — no owner comparison, no
``iam.has_access_for`` call. A note the caller may not see answers
``not_found`` naming its id; one they can see but may not change answers
``no_access``.
"""

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
from matrx_ai.tools.person_session import acts_as_the_person
from matrx_ai.tools.surface_write import attach_surface_write

logger = logging.getLogger(__name__)


_ACCESS_ERROR_TYPES = frozenset({"not_found", "no_access"})


def _manager_error(result: dict[str, Any], default: str, fallback: str) -> ToolError:
    """Carry the manager's access answer (not_found / no_access, naming the id)
    through unchanged; anything else keeps the caller's default type."""
    error_type = result.get("error_type")
    return ToolError(
        error_type=error_type if error_type in _ACCESS_ERROR_TYPES else default,
        message=result.get("error") or fallback,
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


@acts_as_the_person("note_get", subject="your notes")
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
        from matrx_ai.db.content_types.notes import notes_manager_instance

        result = await notes_manager_instance.get_note(note_id)
        if not result.get("success"):
            return ToolResult(
                success=False,
                error=_manager_error(result, "execution", f"Note {note_id} could not be read."),
                started_at=started_at, completed_at=time.time(),
                tool_name="note_get", call_id=ctx.call_id,
            )
        n = result["note"]
        return ToolResult(
            success=True,
            output={
                "id": n.get("id"),
                "label": n.get("label"),
                "folder_name": n.get("folder_name"),
                "content": n.get("content"),
                "tags": n.get("tags", []),
                "published_to_web": bool(n.get("published_to_web")),
                "shown_to": n.get("shown_to"),
                "is_public": bool(n.get("published_to_web")),
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


@acts_as_the_person("note_list", subject="your notes")
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


@acts_as_the_person("note_create", subject="your notes")
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
    """A locked id is refused at the tool boundary before any session opens."""
    note_id = str(args.get("note_id") or "").strip()
    if note_id and is_resource_read_only(note_id):
        return _read_only_result("note_update", time.time(), ctx)
    return await _note_update_as_the_person(args, ctx)


@acts_as_the_person("note_update", subject="your notes")
async def _note_update_as_the_person(args: dict[str, Any], ctx: ToolContext) -> ToolResult:
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
        before = await notes_manager_instance.get_note(note_id)
        if not before.get("success"):
            return ToolResult(
                success=False,
                error=_manager_error(before, "execution", f"Note {note_id} could not be read."),
                started_at=started_at, completed_at=time.time(),
                tool_name="note_update", call_id=ctx.call_id,
            )
        prior = before["note"]
        result = await notes_manager_instance.update_note(note_id, actor_id=ctx.user_id, **updates)
        if not result.get("success"):
            return ToolResult(
                success=False,
                error=_manager_error(result, "execution", "Update failed."),
                started_at=started_at, completed_at=time.time(),
                tool_name="note_update", call_id=ctx.call_id,
            )
        n = result["note"]
        out: dict[str, Any] = {"id": n.get("id"), "label": n.get("label"), "updated_at": n.get("updated_at")}
        if result.get("warning_stripped_immutable"):
            out["warning"] = f"Ignored immutable fields: {result['warning_stripped_immutable']}"
        done = ToolResult(
            success=True, output=out,
            started_at=started_at, completed_at=time.time(),
            tool_name="note_update", call_id=ctx.call_id,
        )
        if "content" in updates:
            # A full-content update OVERWRITES the note: the card shows what it replaced.
            attach_surface_write(
                done,
                before=str(prior.get("content") or ""),
                after=str(n.get("content") if n.get("content") is not None else updates.get("content") or ""),
                target_type="note",
                target_id=note_id,
                target_label=str(n.get("label") or prior.get("label") or ""),
                mode="overwrite",
                content_format="markdown",
            )
        return done
    except Exception as e:
        return ToolResult(
            success=False,
            error=ToolError(error_type="execution", message=str(e), traceback=traceback.format_exc(), is_retryable=True),
            started_at=started_at, completed_at=time.time(),
            tool_name="note_update", call_id=ctx.call_id,
        )


async def note_patch(args: dict[str, Any], ctx: ToolContext) -> ToolResult:
    """A locked id is refused at the tool boundary before any session opens."""
    note_id = str(args.get("note_id") or "").strip()
    if note_id and is_resource_read_only(note_id):
        return _read_only_result("note_patch", time.time(), ctx)
    return await _note_patch_as_the_person(args, ctx)


@acts_as_the_person("note_patch", subject="your notes")
async def _note_patch_as_the_person(args: dict[str, Any], ctx: ToolContext) -> ToolResult:
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
        before = await notes_manager_instance.get_note(note_id)
        if not before.get("success"):
            return ToolResult(
                success=False,
                error=_manager_error(before, "execution", f"Note {note_id} could not be read."),
                started_at=started_at, completed_at=time.time(),
                tool_name="note_patch", call_id=ctx.call_id,
            )
        prior = before["note"]
        result = await notes_manager_instance.patch_note_content(note_id, search_text, replacement_text)
        if not result.get("success") and result.get("error_type") in _ACCESS_ERROR_TYPES:
            return ToolResult(
                success=False,
                error=_manager_error(result, "execution", "Patch failed."),
                started_at=started_at, completed_at=time.time(),
                tool_name="note_patch", call_id=ctx.call_id,
            )
        if not result.get("success"):
            error_type = str(result.get("error") or "patch_no_match")
            return ToolResult(
                success=False,
                error=ToolError(
                    error_type=error_type,
                    message=result.get("message", "No match found for the search text."),
                    suggested_action=(
                        "Widen search_text with the surrounding lines so it matches exactly one place."
                        if error_type == "patch_ambiguous"
                        else "Call note with action='get' to read the current content and provide an exact excerpt."
                    ),
                    is_retryable=True,
                ),
                started_at=started_at, completed_at=time.time(),
                tool_name="note_patch", call_id=ctx.call_id,
            )
        n = result["note"]
        return attach_surface_write(
            ToolResult(
                success=True,
                output_kind="note_tool_result",
                output={
                    "id": n.get("id"),
                    "matched_at_pass": result.get("matched_at_pass"),
                    "updated_at": n.get("updated_at"),
                },
                started_at=started_at, completed_at=time.time(),
                tool_name="note_patch", call_id=ctx.call_id,
            ),
            before=str(prior.get("content") or ""),
            after=str(n.get("content") or ""),
            target_type="note",
            target_id=note_id,
            target_label=str(n.get("label") or prior.get("label") or ""),
            mode="patch",
            content_format="markdown",
            edits=1,
        )
    except Exception as e:
        return ToolResult(
            success=False,
            error=ToolError(error_type="execution", message=str(e), traceback=traceback.format_exc(), is_retryable=True),
            started_at=started_at, completed_at=time.time(),
            tool_name="note_patch", call_id=ctx.call_id,
        )


async def note_delete(args: dict[str, Any], ctx: ToolContext) -> ToolResult:
    """A locked id is refused at the tool boundary before any session opens."""
    note_id = str(args.get("note_id") or "").strip()
    if note_id and is_resource_read_only(note_id):
        return _read_only_result("note_delete", time.time(), ctx)
    return await _note_delete_as_the_person(args, ctx)


@acts_as_the_person("note_delete", subject="your notes")
async def _note_delete_as_the_person(args: dict[str, Any], ctx: ToolContext) -> ToolResult:
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
        result = await notes_manager_instance.delete_note(note_id)
        if not result.get("success"):
            return ToolResult(
                success=False,
                error=_manager_error(result, "execution", "Delete failed."),
                started_at=started_at, completed_at=time.time(),
                tool_name="note_delete", call_id=ctx.call_id,
            )
        return ToolResult(
            success=True,
            output_kind="note_tool_result",
            output={
                "deleted": True,
                "archived": True,
                "note_id": note_id,
                "message": "Note archived (recoverable) — it no longer appears in note lists.",
            },
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
