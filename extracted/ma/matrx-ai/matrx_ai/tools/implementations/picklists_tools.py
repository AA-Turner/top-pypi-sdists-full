from __future__ import annotations

import asyncio
import time
from typing import Any

from matrx_utils import vcprint
from pydantic import ValidationError

from matrx_ai.tools._dispatch_util import format_args_error
from matrx_ai.tools.arg_models import PicklistArgs
from matrx_ai.tools.models import ToolContext, ToolError, ToolResult
from matrx_ai.tools.organization_hold import (
    carried_organization_id,
    organization_required_result,
)


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


# ---------------------------------------------------------------------------
# May THIS PERSON open this list? — RLS answers, never this module
# ---------------------------------------------------------------------------
#
# The list reads below (``picklists_get`` / ``picklists_get_items`` on the live views)
# run on the privileged connection, so by themselves they would hand ANY list to anyone
# who names its id. Before a list's contents are read, the person's own database session
# is asked whether the list exists for them: ``workbench.udt_structured_lists`` under
# the caller's RLS (``as_the_person``). No owner comparison, no has_access call here.

LIST_IN_STORE_UNREADABLE = (
    "List {list_id} lives in the new system (its organization switched its Data tables), "
    "and the picklist tool cannot yet read a list there as you, so nothing was read. "
    "Open it from the Lists page, where the store's own doors decide."
)


def _list_not_found(list_id: str) -> ToolResult:
    return ToolResult(
        success=False,
        error=ToolError(
            error_type="not_found",
            message=f"List {list_id} was not found, or you do not have access to it.",
        ),
    )


async def _list_open_to_person(list_id: str) -> str:
    """``visible`` / ``hidden`` / ``in_store`` for ``list_id``, decided by the database.

    ``visible`` — the older list row answers inside the caller's RLS session.
    ``in_store`` — the older row does not answer, and the arm (in the person's seat)
    says the id lives in the record store; this tool cannot read it as the person yet.
    ``hidden`` — anything else: missing and not-yours read the same.
    """
    from matrx_ai.db._registry import get_model as get_db_model
    from matrx_ai.tools.person_session import as_the_person

    lists = get_db_model("UdtStructuredLists")
    async with as_the_person():
        row = await lists.get_or_none(use_cache=False, id=str(list_id))
    if row is not None and getattr(row, "deleted_at", None) is None:
        return "visible"
    arm = _picklist_store_arm()
    if arm is not None:
        try:
            if await arm.list_lives_in(str(list_id)) == "record":
                return "in_store"
        except Exception:  # noqa: BLE001 — an unanswered home is not a visible list
            return "hidden"
    return "hidden"


# ---------------------------------------------------------------------------
# Where does this list live? — the record-store arm (lane LISTS-AFTER-SWITCH)
# ---------------------------------------------------------------------------
#
# After an organization switches its Data tables to the new system its lists live in the
# record store as Tables of choices (same ids). The READS below already answer from wherever
# a list lives (user_data/picklists_queries.py reads the views workbench.pick_list_live /
# pick_list_item_live). The WRITES go through the host-injected arm when the list (or the new
# list's organization) is in the store, so a write never lands in an archived older list.

#: The ``_ext`` key the host's record-store arm for lists is registered under.
PICKLIST_STORE_ARM_EXT_KEY = "picklist_store_arm"

_picklist_arm_announced: set[str] = set()


def _picklist_store_arm() -> Any | None:
    """The host's record-store arm for lists, or ``None`` on a host with no record store.

    Unwired is ANNOUNCED once, by name: without it a switched organization's list writes are
    refused by the database (never silently landed), and the tool says why.
    """
    from matrx_ai._ext import get_ext, has_ext

    if has_ext(PICKLIST_STORE_ARM_EXT_KEY):
        return get_ext(PICKLIST_STORE_ARM_EXT_KEY)
    if "unwired" not in _picklist_arm_announced:
        _picklist_arm_announced.add("unwired")
        import logging

        logging.getLogger(__name__).warning(
            "matrx-ai has no '%s' configured, so the picklist tool writes ONLY the older "
            "lists; a list that lives in the record store (its organization switched its Data "
            "tables) is refused by the database instead of written. REMEDY: "
            "aidream/package_integration.py, matrx_ai.configure(picklist_store_arm=PicklistStoreArm()).",
            PICKLIST_STORE_ARM_EXT_KEY,
        )
    return None


def _held_result(exc: Exception) -> ToolResult:
    """A change the organization asks a person to approve: NOT done, and not an error to retry."""
    answer = getattr(exc, "answer", {}) or {}
    return ToolResult(
        success=True,
        output={
            "applied": False,
            "awaiting_approval": answer.get("awaiting_approval"),
            "message": (
                "HELD FOR APPROVAL — not an error. Nothing was written yet: the change is in this "
                "organization's approval queue and lands when a person approves it. Do NOT call the "
                "tool again for this change; tell the person it is waiting for their approval."
            ),
        },
    )


async def _choice_lives_in_store(item_id: str) -> bool:
    """Does this choice belong to a list that lives in the record store?"""
    from matrx_orm.sql_executor import execute_standard_query

    rows = await asyncio.to_thread(lambda: execute_standard_query("picklists_item_home", {"item_id": item_id}))
    row = (rows or [None])[0] if isinstance(rows, list) else rows
    return bool(row) and str((row or {}).get("lives_in")) == "record"


async def _born_in_store() -> Any | None:
    """The arm, when a NEW list of this organization is made in the store; else None."""
    arm = _picklist_store_arm()
    if arm is None:
        return None
    return arm if await arm.lists_are_born_in_store() else None


async def userlist_create(args: dict[str, Any], ctx: ToolContext) -> ToolResult:

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
        if not carried_organization_id(ctx):
            return organization_required_result(
                what="create a list", tool_name="picklist", ctx=ctx
            )
        arm = await _born_in_store()
        if arm is not None:
            # lane LISTS-AFTER-SWITCH: this organization's lists live in the record store.
            result = await arm.create_list(list_name=list_name, description=description, items=items)
        else:
            from matrx_ai._ext import get_ext

            PicklistCreator = get_ext("PicklistCreator")
            creator = PicklistCreator(ctx.user_id, organization_id=ctx.organization_id)
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
        if not carried_organization_id(ctx):
            return organization_required_result(
                what="create a list", tool_name="picklist", ctx=ctx
            )
        arm = await _born_in_store()
        if arm is not None:
            # lane LISTS-AFTER-SWITCH: this organization's lists live in the record store.
            result = await arm.create_list(
                list_name=list_name,
                description=description,
                items=[{"label": label, "group_name": group_name} for label in labels],
            )
        else:
            from matrx_ai._ext import get_ext

            PicklistCreator = get_ext("PicklistCreator")
            creator = PicklistCreator(ctx.user_id, organization_id=ctx.organization_id)
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

    from matrx_ai.tools.person_session import PersonSessionUnavailable

    try:
        seat = await _list_open_to_person(str(list_id))
    except PersonSessionUnavailable as e:
        return ToolResult(success=False, error=ToolError(error_type="unavailable", message=str(e)))
    if seat == "hidden":
        return _list_not_found(str(list_id))
    if seat == "in_store":
        return ToolResult(
            success=False,
            error=ToolError(
                error_type="unavailable",
                message=LIST_IN_STORE_UNREADABLE.format(list_id=list_id),
            ),
        )

    try:
        list_data = execute_standard_query("picklists_get", {"list_id": list_id})
        if not list_data:
            return _list_not_found(str(list_id))

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
        if await _choice_lives_in_store(str(item_id)):
            # lane LISTS-AFTER-SWITCH: the choice's list lives in the record store.
            arm = _picklist_store_arm()
            if arm is None:
                return ToolResult(
                    success=False,
                    error=ToolError(
                        error_type="execution",
                        message="This choice's list moved to the new system and this server cannot write there yet; nothing was changed.",
                    ),
                )
            try:
                await arm.update_choice(str(item_id), update_fields)
            except Exception as exc:  # noqa: BLE001 — a held change is not a failure
                if type(exc).__name__ == "ChangeWaits":
                    return _held_result(exc)
                raise
            return ToolResult(
                success=True,
                output={"item_id": item_id, "message": "Item updated successfully."},
            )
        updated = execute_standard_query(
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
        if not updated:
            # UPDATE ... RETURNING id matched no row: nothing changed. Never report success.
            return ToolResult(
                success=False,
                error=ToolError(
                    error_type="not_found",
                    message=f"Choice {item_id} was not found, or you may not change it; nothing was changed.",
                ),
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
            if await _choice_lives_in_store(str(item_id)):
                # lane LISTS-AFTER-SWITCH: the choice's list lives in the record store.
                arm = _picklist_store_arm()
                if arm is None:
                    failed_items.append({"item_id": item_id, "error": "This choice's list moved to the new system and this server cannot write there yet; nothing was changed."})
                    continue
                try:
                    await arm.update_choice(str(item_id), {k: item.get(k) for k in ("label", "description", "help_text", "group_name", "icon_name")})
                except Exception as exc:  # noqa: BLE001 — a held change is not a failure
                    if type(exc).__name__ == "ChangeWaits":
                        failed_items.append({"item_id": item_id, "error": "held for approval; nothing written yet"})
                        continue
                    raise
                success_count += 1
                continue
            updated = execute_standard_query(
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
            if not updated:
                failed_items.append({"item_id": item_id, "error": f"Choice {item_id} was not found, or you may not change it; nothing was changed."})
                continue
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


#: What a choice receipt shows — the fields the live view carries for every home.
_CHOICE_FIELDS = ("label", "description", "help_text", "group_name", "icon_name")


async def _read_choices(list_id: str, item_ids: set[str]) -> dict[str, dict[str, Any]]:
    """item id → its fields, for ``item_ids`` of ``list_id``, from the live view
    (``workbench.pick_list_item_live`` — answers wherever the list lives)."""
    from matrx_orm.sql_executor import execute_standard_query

    # A receipt never shows a list the person cannot open (the read is privileged).
    if await _list_open_to_person(list_id) != "visible":
        raise LookupError(f"List {list_id} is not open to this person; no receipt is read.")
    rows = await asyncio.to_thread(
        lambda: execute_standard_query("picklists_get_items", {"list_id": list_id})
    )
    return {
        str(r.get("id")): {k: r.get(k) for k in _CHOICE_FIELDS}
        for r in _make_serializable(rows or [])
        if str(r.get("id")) in item_ids
    }


async def _choice_list_id(item_id: str) -> str:
    from matrx_orm.sql_executor import execute_standard_query

    rows = await asyncio.to_thread(
        lambda: execute_standard_query("picklists_item_home", {"item_id": item_id})
    )
    row = (rows or [None])[0] if isinstance(rows, list) else rows
    if not row or not row.get("list_id"):
        raise LookupError(f"choice {item_id} has no list")
    return str(row["list_id"])


async def _choices_before(list_id: str | None, item_ids: set[str]) -> tuple[str | None, Any]:
    """(list id, prior choices) for a receipt; ``(…, None)`` when unreadable."""
    from matrx_ai.tools.structured_surface_write import read_prior

    if list_id is None:
        list_id = await read_prior(
            lambda: _choice_list_id(next(iter(item_ids))), what=f"picklist choice {item_ids}"
        )
        if list_id is None:
            return None, None
    return list_id, await read_prior(
        lambda: _read_choices(list_id, item_ids), what=f"picklist {list_id} choices"
    )


async def _choices_surface_write(
    result: ToolResult,
    list_id: str | None,
    item_ids: set[str],
    prior: dict[str, dict[str, Any]] | None,
    keys: tuple[str, ...],
) -> ToolResult:
    """Before → after of the choices this write touched. A change HELD for approval
    wrote nothing, so it carries no receipt."""
    from matrx_ai.tools.structured_surface_write import read_prior, structured_surface_write

    if not result.success or prior is None or list_id is None:
        return result
    if isinstance(result.output, dict) and result.output.get("applied") is False:
        return result
    after = await read_prior(
        lambda: _read_choices(list_id, item_ids), what=f"picklist {list_id} choices (after)"
    )
    single = len(item_ids) == 1
    if single and after is not None:
        only = next(iter(item_ids))
        before_view, after_view = prior.get(only, {}), after.get(only, {})
        label = str(after_view.get("label") or before_view.get("label") or only)
        return structured_surface_write(
            result,
            before=before_view,
            after=after_view,
            target_type="picklist_choice",
            target_id=only,
            target_label=label,
            keys=keys,
        )
    return structured_surface_write(
        result,
        before=prior,
        after=after,
        target_type="picklist_choices",
        target_id=list_id,
        target_label=f"{len(item_ids)} choice(s)",
        keys=tuple(item_ids),
        edits=len(item_ids),
    )


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
        ids = {str(item_id)}
        list_id, prior = await _choices_before(None, ids)
        result = await userlist_update_item({"item_id": item_id, **passthrough}, ctx)
        return _picklist_stamp(
            await _choices_surface_write(
                result, list_id, ids, prior, tuple(k for k in passthrough if k in _CHOICE_FIELDS)
            ),
            started_at,
            ctx,
        )

    # action == "batch_update"
    picklist_id = args.get("picklist_id")
    if not picklist_id:
        return _picklist_validation_error(
            "picklist_id is required for action=batch_update.", started_at, ctx
        )
    items = args.get("items", []) or []
    ids = {str(i["id"]) for i in items if isinstance(i, dict) and i.get("id")}
    list_id, prior = await _choices_before(str(picklist_id), ids) if ids else (None, None)
    result = await userlist_batch_update({"list_id": picklist_id, "items": items}, ctx)
    return _picklist_stamp(
        await _choices_surface_write(result, list_id, ids, prior, ()),
        started_at,
        ctx,
    )
