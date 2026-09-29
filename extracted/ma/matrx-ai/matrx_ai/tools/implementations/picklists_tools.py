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



def _list_not_found(list_id: str) -> ToolResult:
    return ToolResult(
        success=False,
        error=ToolError(
            error_type="not_found",
            message=f"List {list_id} was not found, or you do not have access to it.",
        ),
    )


async def _update_choice_as_the_person(item_id: str, fields: dict[str, Any]) -> str:
    """The shared service's choice write, in the caller's RLS session."""
    from matrx_ai.db.content_types.picklist_access import update_choice_as_the_person

    return await update_choice_as_the_person(str(item_id), fields)


def _choice_refusal(item_id: str, answer: str) -> str:
    if answer == "no_access":
        return f"You can view choice {item_id} but you do not have permission to change it; nothing was changed."
    if answer == "nothing":
        return "Nothing to change: give at least one of label, description, help_text, group_name, is_public, public_read, icon_name."
    return f"Choice {item_id} was not found, or you do not have access to it; nothing was changed."


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
        output_kind="picklist_approval_result",
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
    """The person's own lists, both homes, read AS THE PERSON through the shared service."""
    from matrx_ai.db.content_types.picklist_access import lists_for_person

    page = max(1, args.get("page", 1))
    page_size = min(100, max(1, args.get("page_size", 50)))
    search_term = args.get("search_term")

    try:
        result = await lists_for_person(
            str(ctx.user_id), search=search_term, limit=page_size, offset=(page - 1) * page_size
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
    """One list and its choices AS THE PERSON, wherever it lives (older tables or the record
    store) — the shared service decides; nothing is read on the privileged connection."""
    from matrx_ai.db.content_types.picklist_access import grouped_choices, read_list_as_the_person
    from matrx_ai.tools.person_session import PersonSessionUnavailable

    list_id = args.get("list_id")
    group_by = args.get("group_by", False)
    if not list_id:
        return ToolResult(
            success=False,
            error=ToolError(error_type="validation", message="list_id is required."),
        )
    try:
        listing = await read_list_as_the_person(str(list_id))
    except PersonSessionUnavailable as e:
        return ToolResult(success=False, error=ToolError(error_type="unavailable", message=str(e)))
    if listing is None:
        return _list_not_found(str(list_id))
    items = listing.pop("items")
    return ToolResult(
        success=True,
        output=_make_serializable(
            {
                "list": [listing],
                "items": grouped_choices(items) if group_by else items,
                "is_grouped": group_by,
            }
        ),
    )


async def userlist_update_item(args: dict[str, Any], ctx: ToolContext) -> ToolResult:

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
                output_kind="picklist_item_update_result",
                output={"item_id": item_id, "message": "Item updated successfully."},
            )
        answer = await _update_choice_as_the_person(str(item_id), {**update_fields})
        if answer != "updated":
            return ToolResult(
                success=False,
                error=ToolError(
                    error_type="validation" if answer == "nothing" else answer,
                    message=_choice_refusal(str(item_id), answer),
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
            answer = await _update_choice_as_the_person(str(item_id), item)
            if answer != "updated":
                failed_items.append({"item_id": item_id, "error": _choice_refusal(str(item_id), answer)})
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
    """item id → its fields, for ``item_ids`` of ``list_id``, read AS THE PERSON through the
    shared service (both homes). A list the person cannot open has no receipt."""
    from matrx_ai.db.content_types.picklist_access import read_list_as_the_person

    listing = await read_list_as_the_person(str(list_id))
    if listing is None:
        raise LookupError(f"List {list_id} is not open to this person; no receipt is read.")
    return {
        str(r.get("id")): {k: r.get(k) for k in _CHOICE_FIELDS}
        for r in _make_serializable(listing["items"])
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
