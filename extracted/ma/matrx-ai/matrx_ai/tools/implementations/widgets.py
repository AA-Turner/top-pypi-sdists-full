"""Widget tools — native matrx_ai tools for widget-scoped content edits.

These 10 tools (``widget_text_replace``, ``widget_text_append``,
``widget_attach_media``, ``widget_create_artifact``, etc.) are plain native
tools just like every other tool in this package. They are registered in the
DB with ``source_kind='native'`` and a ``tool_binding`` row to executor
``matrx-ai-core``; the implementation lives in the module-level async
functions below.

How they work
-------------
Each widget tool is a thin server-side wrapper over ``context_patch`` / the
``context`` tool's create action (``ctx_create``).
The caller is expected to seed a well-known ContextObject in the request's
``context`` dict (marked ``mutable=true``) per widget:

    widget_content   — primary string the widget edits (used by widget_text_*)
    widget_record    — underlying record (used by widget_update_field / _record)
    widget_media     — list of attached media (used by widget_attach_media)
    widget_artifacts — list of structured artifacts (used by widget_create_artifact)

If the expected context object is not present in the manifest, the tool returns
a structured ``missing_context`` error telling the model which key to ask for.

Clients that prefer to execute these themselves (the most common case) simply
pass the widget tool names in ``client_tools`` and the executor short-circuits
before reaching this module — exactly the same mechanism used by every other
tool the client chooses to own.

Why keep the 10 names rather than forcing everyone onto ``context_patch``?
----------------------------------------------------------------------
1. The frontend's UX already maps widget affordances onto these names.
2. Smaller / cheaper models dispatch narrow tools more reliably than a single
   multi-command ``context_patch``.
3. It keeps the client free to execute them when it wants; the server-side
   implementation is just a safety net when the model asks us to run them.
"""

from __future__ import annotations

import time
from typing import Any

from matrx_ai.tools.implementations.ctx_write import context_patch, ctx_create
from matrx_ai.tools.models import ToolContext, ToolError, ToolResult

WIDGET_CONTENT_KEY = "widget_content"
WIDGET_RECORD_KEY = "widget_record"
WIDGET_MEDIA_KEY = "widget_media"
WIDGET_ARTIFACTS_KEY = "widget_artifacts"


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


async def _has_manifest_key(key: str) -> bool:
    """Return True if the current request's manifest exposes ``key``."""
    try:
        from matrx_ai._ext import get_ext
        from matrx_ai.context.app_context import get_app_context

        app_ctx = get_app_context()
        load_manifest_from_ctx = get_ext("load_manifest_from_ctx")
        manifest = load_manifest_from_ctx(app_ctx)
    except Exception:
        return False
    if manifest is None:
        return False
    return manifest.get(key) is not None


def _missing_context_error(tool_name: str, call_id: str, key: str) -> ToolResult:
    now = time.time()
    return ToolResult(
        success=False,
        error=ToolError(
            error_type="missing_context",
            message=(
                f"Tool '{tool_name}' needs a mutable '{key}' context object, "
                "but the request did not include one."
            ),
            is_retryable=False,
            suggested_action=(
                f"Ask the caller to add '{key}' to the request's context with "
                "mutable=true, or use context_patch directly against a context "
                "object the user controls."
            ),
        ),
        tool_name=tool_name,
        call_id=call_id,
        started_at=now,
        completed_at=now,
    )


def _validation_error(tool_name: str, call_id: str, message: str) -> ToolResult:
    now = time.time()
    return ToolResult(
        success=False,
        error=ToolError(
            error_type="validation",
            message=message,
            is_retryable=False,
        ),
        tool_name=tool_name,
        call_id=call_id,
        started_at=now,
        completed_at=now,
    )


async def _forward_to_patch(
    tool_name: str, ctx: ToolContext, patch_args: dict[str, Any]
) -> ToolResult:
    result = await context_patch(patch_args, ctx)
    result.tool_name = tool_name
    return result


async def _forward_to_create(
    tool_name: str, ctx: ToolContext, create_args: dict[str, Any]
) -> ToolResult:
    result = await ctx_create(create_args, ctx)
    result.tool_name = tool_name
    return result


# ---------------------------------------------------------------------------
# Text manipulation — operate on WIDGET_CONTENT_KEY
# ---------------------------------------------------------------------------


async def widget_text_replace(args: dict[str, Any], ctx: ToolContext) -> ToolResult:
    from matrx_ai.tools._generated_declarations import WidgetTextReplaceArgs

    WidgetTextReplaceArgs.model_validate(
        args
    )  # enforce the declared arg contract (common-docs/systems/agents/agent-tools/HANDOFF.md)
    tool_name = "widget_text_replace"
    if not await _has_manifest_key(WIDGET_CONTENT_KEY):
        return _missing_context_error(tool_name, ctx.call_id, WIDGET_CONTENT_KEY)
    return await _forward_to_patch(
        tool_name,
        ctx,
        {
            "key": WIDGET_CONTENT_KEY,
            "command": "overwrite",
            "new_str": args.get("text", ""),
        },
    )


async def widget_text_insert_before(args: dict[str, Any], ctx: ToolContext) -> ToolResult:
    from matrx_ai.tools._generated_declarations import WidgetTextInsertBeforeArgs

    WidgetTextInsertBeforeArgs.model_validate(
        args
    )  # enforce the declared arg contract (common-docs/systems/agents/agent-tools/HANDOFF.md)
    tool_name = "widget_text_insert_before"
    if not await _has_manifest_key(WIDGET_CONTENT_KEY):
        return _missing_context_error(tool_name, ctx.call_id, WIDGET_CONTENT_KEY)
    return await _forward_to_patch(
        tool_name,
        ctx,
        {
            "key": WIDGET_CONTENT_KEY,
            "command": "prepend",
            "new_str": args.get("text", ""),
        },
    )


async def widget_text_insert_after(args: dict[str, Any], ctx: ToolContext) -> ToolResult:
    from matrx_ai.tools._generated_declarations import WidgetTextInsertAfterArgs

    WidgetTextInsertAfterArgs.model_validate(
        args
    )  # enforce the declared arg contract (common-docs/systems/agents/agent-tools/HANDOFF.md)
    tool_name = "widget_text_insert_after"
    if not await _has_manifest_key(WIDGET_CONTENT_KEY):
        return _missing_context_error(tool_name, ctx.call_id, WIDGET_CONTENT_KEY)
    return await _forward_to_patch(
        tool_name,
        ctx,
        {
            "key": WIDGET_CONTENT_KEY,
            "command": "append",
            "new_str": args.get("text", ""),
        },
    )


async def widget_text_prepend(args: dict[str, Any], ctx: ToolContext) -> ToolResult:
    from matrx_ai.tools._generated_declarations import WidgetTextPrependArgs

    WidgetTextPrependArgs.model_validate(
        args
    )  # enforce the declared arg contract (common-docs/systems/agents/agent-tools/HANDOFF.md)
    tool_name = "widget_text_prepend"
    if not await _has_manifest_key(WIDGET_CONTENT_KEY):
        return _missing_context_error(tool_name, ctx.call_id, WIDGET_CONTENT_KEY)
    return await _forward_to_patch(
        tool_name,
        ctx,
        {
            "key": WIDGET_CONTENT_KEY,
            "command": "prepend",
            "new_str": args.get("text", ""),
        },
    )


async def widget_text_append(args: dict[str, Any], ctx: ToolContext) -> ToolResult:
    from matrx_ai.tools._generated_declarations import WidgetTextAppendArgs

    WidgetTextAppendArgs.model_validate(
        args
    )  # enforce the declared arg contract (common-docs/systems/agents/agent-tools/HANDOFF.md)
    tool_name = "widget_text_append"
    if not await _has_manifest_key(WIDGET_CONTENT_KEY):
        return _missing_context_error(tool_name, ctx.call_id, WIDGET_CONTENT_KEY)
    return await _forward_to_patch(
        tool_name,
        ctx,
        {
            "key": WIDGET_CONTENT_KEY,
            "command": "append",
            "new_str": args.get("text", ""),
        },
    )


async def widget_text_patch(args: dict[str, Any], ctx: ToolContext) -> ToolResult:
    from matrx_ai.tools._generated_declarations import WidgetTextPatchArgs

    WidgetTextPatchArgs.model_validate(
        args
    )  # enforce the declared arg contract (common-docs/systems/agents/agent-tools/HANDOFF.md)
    tool_name = "widget_text_patch"
    if not await _has_manifest_key(WIDGET_CONTENT_KEY):
        return _missing_context_error(tool_name, ctx.call_id, WIDGET_CONTENT_KEY)
    return await _forward_to_patch(
        tool_name,
        ctx,
        {
            "key": WIDGET_CONTENT_KEY,
            "command": "str_replace",
            "old_str": args.get("search_text", ""),
            "new_str": args.get("replacement_text", ""),
        },
    )


# ---------------------------------------------------------------------------
# Record manipulation — operate on WIDGET_RECORD_KEY
# ---------------------------------------------------------------------------


async def widget_update_field(args: dict[str, Any], ctx: ToolContext) -> ToolResult:
    from matrx_ai.tools._generated_declarations import WidgetUpdateFieldArgs

    WidgetUpdateFieldArgs.model_validate(
        args
    )  # enforce the declared arg contract (common-docs/systems/agents/agent-tools/HANDOFF.md)
    tool_name = "widget_update_field"
    if not await _has_manifest_key(WIDGET_RECORD_KEY):
        return _missing_context_error(tool_name, ctx.call_id, WIDGET_RECORD_KEY)
    field = args.get("field")
    if not isinstance(field, str) or not field:
        return _validation_error(tool_name, ctx.call_id, "field must be a non-empty string")
    return await _forward_to_patch(
        tool_name,
        ctx,
        {
            "key": WIDGET_RECORD_KEY,
            "command": "json_merge",
            "patch": {field: args.get("value")},
        },
    )


async def widget_update_record(args: dict[str, Any], ctx: ToolContext) -> ToolResult:
    from matrx_ai.tools._generated_declarations import WidgetUpdateRecordArgs

    WidgetUpdateRecordArgs.model_validate(
        args
    )  # enforce the declared arg contract (common-docs/systems/agents/agent-tools/HANDOFF.md)
    tool_name = "widget_update_record"
    if not await _has_manifest_key(WIDGET_RECORD_KEY):
        return _missing_context_error(tool_name, ctx.call_id, WIDGET_RECORD_KEY)
    patch = args.get("patch")
    if not isinstance(patch, dict):
        return _validation_error(tool_name, ctx.call_id, "patch must be a JSON object")
    return await _forward_to_patch(
        tool_name,
        ctx,
        {
            "key": WIDGET_RECORD_KEY,
            "command": "json_merge",
            "patch": patch,
        },
    )


# ---------------------------------------------------------------------------
# Media / artifacts — list-typed context objects, create on demand
# ---------------------------------------------------------------------------


async def widget_attach_media(args: dict[str, Any], ctx: ToolContext) -> ToolResult:
    from matrx_ai.tools._generated_declarations import WidgetAttachMediaArgs

    WidgetAttachMediaArgs.model_validate(
        args
    )  # enforce the declared arg contract (common-docs/systems/agents/agent-tools/HANDOFF.md)
    tool_name = "widget_attach_media"
    media_item = {
        "url": args.get("url"),
        "mimeType": args.get("mimeType"),
        "title": args.get("title"),
        "alt": args.get("alt"),
        "position": args.get("position"),
    }
    media_item = {k: v for k, v in media_item.items() if v is not None}

    if await _has_manifest_key(WIDGET_MEDIA_KEY):
        return await _forward_to_patch(
            tool_name,
            ctx,
            {
                "key": WIDGET_MEDIA_KEY,
                "command": "json_patch",
                "operations": [{"op": "add", "path": "/-", "value": media_item}],
            },
        )

    return await _forward_to_create(
        tool_name,
        ctx,
        {
            "key": WIDGET_MEDIA_KEY,
            "content": [media_item],
            "type": "json",
            "label": "Widget Media",
            "description": "List of media attached to the focused widget this turn.",
            "mutable": True,
            "persist": "client",
        },
    )


async def widget_create_artifact(args: dict[str, Any], ctx: ToolContext) -> ToolResult:
    from matrx_ai.tools._generated_declarations import WidgetCreateArtifactArgs

    WidgetCreateArtifactArgs.model_validate(
        args
    )  # enforce the declared arg contract (common-docs/systems/agents/agent-tools/HANDOFF.md)
    tool_name = "widget_create_artifact"
    kind = args.get("kind")
    if not kind:
        return _validation_error(tool_name, ctx.call_id, "kind is required")

    artifact = {"kind": kind, "data": args.get("data")}

    if await _has_manifest_key(WIDGET_ARTIFACTS_KEY):
        return await _forward_to_patch(
            tool_name,
            ctx,
            {
                "key": WIDGET_ARTIFACTS_KEY,
                "command": "json_patch",
                "operations": [{"op": "add", "path": "/-", "value": artifact}],
            },
        )

    return await _forward_to_create(
        tool_name,
        ctx,
        {
            "key": WIDGET_ARTIFACTS_KEY,
            "content": [artifact],
            "type": "json",
            "label": "Widget Artifacts",
            "description": "Artifacts created by the agent for the focused widget this turn.",
            "mutable": True,
            "persist": "client",
        },
    )
