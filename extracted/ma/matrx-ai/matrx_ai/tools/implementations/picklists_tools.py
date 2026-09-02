from __future__ import annotations

import asyncio
import time
from typing import Any

from matrx_utils import vcprint
from pydantic import ValidationError

from matrx_ai.tools._dispatch_util import format_args_error
from matrx_ai.tools.arg_models import PicklistArgs
from matrx_ai.tools.models import ToolContext, ToolError, ToolResult


async def _picklist_item_is_read_only(item_id: str) -> bool:
    """Check both the item lock and its parent-list lock before a write."""
    from matrx_ai.config.read_only_resources import has_read_only_resources, is_resource_read_only

    if is_resource_read_only(item_id):
        return True
    if not has_read_only_resources():
        return False

    from matrx_ai.db._registry import get_model as get_db_model

    item_model = get_db_model("UdtStructuredListItems")
    try:
        item = await item_model.get_by_id(item_id, use_cache=False)
    except Exception:  # noqa: BLE001 — a lock-parent lookup must fail closed
        return True
    return is_resource_read_only(str(getattr(item, "list_id", "") or ""))


async def userlist_create(args: dict[str, Any], ctx: ToolContext) -> ToolResult:
    from matrx_ai._ext import get_ext
    PicklistCreator = get_ext("PicklistCreator")

    list_name = args.get("list_name", "")
    description = args.get("description", "")
    items = args.get("items", [])

    if not list_name:
        return ToolResult(
            success=False,
            error=ToolError(error_type="validation", message="list_name is required."),
        )
    if not items:
        return ToolResult(
            success=False,
            error=ToolError(
                error_type="validation", message="items must be a non-empty list."
            ),
        )

    for idx, item in enumerate(items):
        if not isinstance(item, dict) or not item.get("label"):
            return ToolResult(
                success=False,
                error=ToolError(
                    error_type="validation",
                    message=f"Item at index {idx} must be an object with a 'label' field.",
                ),
            )

    try:
        creator = PicklistCreator(ctx.user_id)
        result = await asyncio.to_thread(
            lambda: creator.create_list_with_items(
                items=items, list_name=list_name, description=description
            )
        )
        return ToolResult(
            success=True,
            output={
                "list_id": str(result.get("list_id", "")),
                "list_name": result.get("list_name", list_name),
                "item_count": result.get("item_count", len(items)),
                "already_existed": result.get("existing", False),
                "message": f"List '{list_name}' created with {len(items)} items.",
            },
        )
    except Exception as e:
        vcprint(str(e), "userlist_create error", color="red")
        return ToolResult(
            success=False, error=ToolError(error_type="execution", message=str(e))
        )


async def userlist_create_simple(args: dict[str, Any], ctx: ToolContext) -> ToolResult:
    from matrx_ai._ext import get_ext
    PicklistCreator = get_ext("PicklistCreator")

    list_name = args.get("list_name", "")
    description = args.get("description", "")
    labels = args.get("labels", [])
    group_name = args.get("group_name")

    if not list_name:
        return ToolResult(
            success=False,
            error=ToolError(error_type="validation", message="list_name is required."),
        )
    if not labels or not isinstance(labels, list):
        return ToolResult(
            success=False,
            error=ToolError(
                error_type="validation",
                message="labels must be a non-empty list of strings.",
            ),
        )

    for idx, label in enumerate(labels):
        if not isinstance(label, str) or not label.strip():
            return ToolResult(
                success=False,
                error=ToolError(
                    error_type="validation",
                    message=f"Label at index {idx} must be a non-empty string.",
                ),
            )

    try:
        creator = PicklistCreator(ctx.user_id)
        result = await asyncio.to_thread(
            lambda: creator.create_simple_list(
                labels=labels,
                list_name=list_name,
                description=description,
                group_name=group_name,
            )
        )
        return ToolResult(
            success=True,
            output={
                "list_id": str(result.get("list_id", "")),
                "list_name": result.get("list_name", list_name),
                "item_count": result.get("item_count", len(labels)),
                "already_existed": result.get("existing", False),
                "message": f"Simple list '{list_name}' created with {len(labels)} items.",
            },
        )
    except Exception as e:
        vcprint(str(e), "userlist_create_simple error", color="red")
        return ToolResult(
            success=False, error=ToolError(error_type="execution", message=str(e))
        )


def _make_serializable(obj: Any) -> Any:
    import uuid
    from datetime import date, datetime

    if isinstance(obj, uuid.UUID):
        return str(obj)
    if isinstance(obj, datetime):
        return obj.isoformat()
    if isinstance(obj, date):
        return obj.isoformat()
    if isinstance(obj, dict):
        return {k: _make_serializable(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [_make_serializable(i) for i in obj]
    return obj


async def userlist_get_all(args: dict[str, Any], ctx: ToolContext) -> ToolResult:
    from matrx_orm.sql_executor import execute_standard_query

    page = max(1, args.get("page", 1))
    page_size = min(100, max(1, args.get("page_size", 50)))
    search_term = args.get("search_term")

    try:
        if search_term:
            offset = (page - 1) * page_size
            result = execute_standard_query(
                "picklists_search",
                {
                    "user_id": ctx.user_id,
                    "search_term": f"%{search_term}%",
                    "limit": page_size,
                    "offset": offset,
                },
            )
        else:
            raw = execute_standard_query(
                "picklists_list_for_user", {"user_id": ctx.user_id}
            )
            all_lists = _make_serializable(raw) if raw else []
            offset = (page - 1) * page_size
            result = (
                all_lists[offset : offset + page_size]
                if isinstance(all_lists, list)
                else all_lists
            )

        lists = _make_serializable(result) if result else []
        return ToolResult(
            success=True,
            output={
                "lists": lists,
                "page": page,
                "page_size": page_size,
                "count": len(lists) if isinstance(lists, list) else 0,
            },
        )
    except Exception as e:
        error_mesage = str(e)
        vcprint(error_mesage, "error_mesage", color="red")
        return ToolResult(
            success=False, error=ToolError(error_type="execution", message=error_mesage)
        )


async def userlist_get_details(args: dict[str, Any], ctx: ToolContext) -> ToolResult:
    from matrx_orm.sql_executor import execute_standard_query

    list_id = args.get("list_id")
    group_by = args.get("group_by", False)

    if not list_id:
        return ToolResult(
            success=False,
            error=ToolError(error_type="validation", message="list_id is required."),
        )

    try:
        list_data = execute_standard_query("picklists_get", {"list_id": list_id})
        if not list_data:
            return ToolResult(
                success=False,
                error=ToolError(
                    error_type="not_found", message=f"List '{list_id}' not found."
                ),
            )

        query_name = (
            "picklists_get_items_grouped"
            if group_by
            else "picklists_get_items"
        )
        items = execute_standard_query(query_name, {"list_id": list_id})

        return ToolResult(
            success=True,
            output=_make_serializable(
                {
                    "list": list_data,
                    "items": items or [],
                    "is_grouped": group_by,
                }
            ),
        )
    except Exception as e:
        error_mesage = str(e)
        vcprint(error_mesage, "error_mesage", color="red")
        return ToolResult(
            success=False, error=ToolError(error_type="execution", message=str(e))
        )


async def userlist_update_item(args: dict[str, Any], ctx: ToolContext) -> ToolResult:
    from matrx_orm.sql_executor import execute_standard_query

    item_id = args.get("item_id")
    if not item_id:
        return ToolResult(
            success=False,
            error=ToolError(error_type="validation", message="item_id is required."),
        )

    update_fields = {
        k: args[k]
        for k in (
            "label",
            "description",
            "help_text",
            "group_name",
            "is_public",
            "authenticated_read",
            "public_read",
            "icon_name",
        )
        if k in args
    }
    if not update_fields:
        return ToolResult(
            success=False,
            error=ToolError(
                error_type="validation",
                message="At least one field to update is required.",
            ),
        )

    from matrx_ai.config.read_only_resources import READ_ONLY_TOOL_MESSAGE

    if await _picklist_item_is_read_only(str(item_id)):
        return ToolResult(
            success=False,
            error=ToolError(error_type="read_only", message=READ_ONLY_TOOL_MESSAGE),
        )

    try:
        execute_standard_query(
            "picklists_update_item",
            {
                "item_id": item_id,
                "user_id": ctx.user_id,
                "label": update_fields.get("label"),
                "description": update_fields.get("description"),
                "help_text": update_fields.get("help_text"),
                "group_name": update_fields.get("group_name"),
                "is_public": args.get("is_public"),
                "authenticated_read": args.get("authenticated_read"),
                "public_read": args.get("public_read"),
                "icon_name": args.get("icon_name"),
            },
        )
        return ToolResult(
            success=True,
            output={"item_id": item_id, "message": "Item updated successfully."},
        )
    except Exception as e:
        error_mesage = str(e)
        vcprint(error_mesage, "error_mesage", color="red")
        return ToolResult(
            success=False, error=ToolError(error_type="execution", message=str(e))
        )


async def userlist_batch_update(args: dict[str, Any], ctx: ToolContext) -> ToolResult:
    from matrx_orm.sql_executor import execute_standard_query

    list_id = args.get("list_id")
    items = args.get("items", [])

    if not list_id:
        return ToolResult(
            success=False,
            error=ToolError(error_type="validation", message="list_id is required."),
        )
    if not items:
        return ToolResult(
            success=False,
            error=ToolError(
                error_type="validation", message="items must be a non-empty list."
            ),
        )

    from matrx_ai.config.read_only_resources import READ_ONLY_TOOL_MESSAGE, is_resource_read_only

    if is_resource_read_only(str(list_id)):
        return ToolResult(
            success=False,
            error=ToolError(error_type="read_only", message=READ_ONLY_TOOL_MESSAGE),
        )

    success_count = 0
    failed_items: list[dict[str, Any]] = []

    for item in items:
        item_id = item.get("id")
        if not item_id:
            failed_items.append({"item": item, "error": "Missing 'id' field."})
            continue
        if await _picklist_item_is_read_only(str(item_id)):
            failed_items.append({"item_id": item_id, "error": READ_ONLY_TOOL_MESSAGE})
            continue
        try:
            execute_standard_query(
                "picklists_update_item",
                {
                    "item_id": item_id,
                    "user_id": ctx.user_id,
                    "label": item.get("label"),
                    "description": item.get("description"),
                    "help_text": item.get("help_text"),
                    "group_name": item.get("group_name"),
                    "is_public": item.get("is_public"),
                    "authenticated_read": item.get("authenticated_read"),
                    "public_read": item.get("public_read"),
                    "icon_name": item.get("icon_name"),
                },
            )
            success_count += 1
        except Exception as e:
            error_mesage = str(e)
            vcprint(error_mesage, "error_mesage", color="red")
            failed_items.append({"item_id": item_id, "error": error_mesage})

    return ToolResult(
        success=True,
        output={
            "success_count": success_count,
            "failed_count": len(failed_items),
            "failed_items": failed_items,
            "message": f"Updated {success_count} items, {len(failed_items)} failed.",
        },
    )


# ---------------------------------------------------------------------------
# picklist — unified action dispatcher
# ---------------------------------------------------------------------------

# Valid `picklist` actions are enforced by the PicklistArgs discriminated union
# (arg_models/dispatcher_args.py) + tool_def.parameters."$variants" — the source of truth.


def _picklist_stamp(result: ToolResult, started_at: float, ctx: ToolContext) -> ToolResult:
    result.tool_name = "picklist"
    result.call_id = ctx.call_id
    if not result.started_at:
        result.started_at = started_at
    if not result.completed_at:
        result.completed_at = time.time()
    return result


def _picklist_validation_error(message: str, started_at: float, ctx: ToolContext) -> ToolResult:
    return ToolResult(
        success=False,
        error=ToolError(error_type="validation", message=message),
        started_at=started_at,
        completed_at=time.time(),
        tool_name="picklist",
        call_id=ctx.call_id,
    )


async def picklist(args: dict[str, Any], ctx: ToolContext) -> ToolResult:
    # KindModel result (KIND_TOOL_LEDGER): one stamp funnel over every branch.
    from matrx_ai.tools.kind_stamp import stamp_result_kind
    from matrx_ai.tools.kinds.workbench import PicklistToolResult

    return stamp_result_kind(await _picklist_impl(args, ctx), PicklistToolResult)


async def _picklist_impl(args: dict[str, Any], ctx: ToolContext) -> ToolResult:
    started_at = time.time()
    try:
        parsed = PicklistArgs.model_validate(args).root
    except ValidationError as exc:
        return _picklist_validation_error(format_args_error(exc), started_at, ctx)
    action = parsed.action

    if action == "list":
        return _picklist_stamp(
            await userlist_get_all(
                {
                    "page": args.get("page", 1),
                    "page_size": args.get("page_size", 50),
                    "search_term": args.get("search_term"),
                },
                ctx,
            ),
            started_at,
            ctx,
        )

    if action == "get":
        picklist_id = args.get("picklist_id")
        if not picklist_id:
            return _picklist_validation_error(
                "picklist_id is required for action=get.", started_at, ctx
            )
        return _picklist_stamp(
            await userlist_get_details(
                {"list_id": picklist_id, "group_by": args.get("group_by", False)},
                ctx,
            ),
            started_at,
            ctx,
        )

    if action == "create":
        items = args.get("items") or []
        if not items:
            return _picklist_validation_error(
                "items is required for action=create (array of strings or objects).",
                started_at,
                ctx,
            )
        # Dispatch on item shape: strings → simple list, objects → structured.
        if all(isinstance(i, str) for i in items):
            return _picklist_stamp(
                await userlist_create_simple(
                    {
                        "list_name": args.get("picklist_name", ""),
                        "description": args.get("description", ""),
                        "labels": items,
                        "group_name": args.get("group_name"),
                    },
                    ctx,
                ),
                started_at,
                ctx,
            )
        return _picklist_stamp(
            await userlist_create(
                {
                    "list_name": args.get("picklist_name", ""),
                    "description": args.get("description", ""),
                    "items": items,
                },
                ctx,
            ),
            started_at,
            ctx,
        )

    if action == "update_item":
        item_id = args.get("item_id")
        if not item_id:
            return _picklist_validation_error(
                "item_id is required for action=update_item.", started_at, ctx
            )
        passthrough = {
            k: args[k]
            for k in ("label", "help_text", "group_name", "description",
                      "is_public", "authenticated_read", "public_read", "icon_name")
            if k in args
        }
        return _picklist_stamp(
            await userlist_update_item({"item_id": item_id, **passthrough}, ctx),
            started_at,
            ctx,
        )

    # action == "batch_update"
    picklist_id = args.get("picklist_id")
    if not picklist_id:
        return _picklist_validation_error(
            "picklist_id is required for action=batch_update.", started_at, ctx
        )
    return _picklist_stamp(
        await userlist_batch_update(
            {"list_id": picklist_id, "items": args.get("items", [])}, ctx
        ),
        started_at,
        ctx,
    )
