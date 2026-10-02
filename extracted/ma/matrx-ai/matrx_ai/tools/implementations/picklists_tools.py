"""The agents' ``picklist`` tool — a person's lists of choices, in the record store.

Every list lives in the record store as a Table of choices. The tool lives in this package,
which must never import matrx-records, so the store half is injected by the host
(``matrx_ai.configure(picklist_store_arm=...)``; aidream wires
``matrx_records.agent.picklist_arm.PicklistStoreArm``) and every read and write is answered
there, in the person's own seat. A host without the arm gets a refusal that names the wiring.
"""

from __future__ import annotations

import logging
import time
from typing import Any

from pydantic import ValidationError

from matrx_ai.tools._dispatch_util import format_args_error
from matrx_ai.tools.arg_models import PicklistArgs
from matrx_ai.tools.models import ToolContext, ToolError, ToolResult
from matrx_ai.tools.organization_hold import (
    carried_organization_id,
    organization_required_result,
)

logger = logging.getLogger(__name__)

#: The ``_ext`` key the host's record-store arm for lists is registered under.
PICKLIST_STORE_ARM_EXT_KEY = "picklist_store_arm"

#: What a host without the arm is told — the one wiring that serves every verb.
UNWIRED_MESSAGE = (
    "This server has no record store wired for the picklist tool, so nothing was read or "
    "written. REMEDY: matrx_ai.configure(picklist_store_arm=PicklistStoreArm())."
)


class _NoArm(Exception):
    """The host never wired the record-store arm for lists."""


def _picklist_store_arm() -> Any:
    """The host's record-store arm for lists; :class:`_NoArm` when it was never wired."""
    from matrx_ai._ext import get_ext, has_ext

    if has_ext(PICKLIST_STORE_ARM_EXT_KEY):
        return get_ext(PICKLIST_STORE_ARM_EXT_KEY)
    logger.error("matrx-ai has no '%s' configured: %s", PICKLIST_STORE_ARM_EXT_KEY, UNWIRED_MESSAGE)
    raise _NoArm(UNWIRED_MESSAGE)


def _failed(exc: Exception) -> ToolResult:
    """A store refusal (or a missing arm) as the tool's own error, in the store's words."""
    name = type(exc).__name__
    if name == "_NoArm" or getattr(exc, "sqlstate", None) == "0A000":
        error_type = "unavailable"
    elif name == "StoreRefusal" and getattr(exc, "sqlstate", None) == "02000":
        error_type = "not_found"
    elif name == "StoreRefusal" and getattr(exc, "sqlstate", None) == "42501":
        error_type = "no_access"
    elif name == "ValueError":
        error_type = "validation"
    else:
        error_type = "execution"
    return ToolResult(success=False, error=ToolError(error_type=error_type, message=str(exc)))


async def _picklist_item_is_read_only(item_id: str) -> bool:
    """Check both the item lock and its parent-list lock before a write."""
    from matrx_ai.config.read_only_resources import has_read_only_resources, is_resource_read_only

    if is_resource_read_only(item_id):
        return True
    if not has_read_only_resources():
        return False
    try:
        list_id = await _picklist_store_arm().list_of_choice(item_id)
    except Exception:  # noqa: BLE001 — a lock-parent lookup must fail closed
        return True
    return list_id is None or is_resource_read_only(list_id)


def _list_not_found(list_id: str) -> ToolResult:
    return ToolResult(
        success=False,
        error=ToolError(
            error_type="not_found",
            message=f"List {list_id} was not found, or you do not have access to it.",
        ),
    )


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


async def _create(list_name: str, description: str, items: list[dict[str, Any]],
                  ctx: ToolContext) -> ToolResult:
    if not carried_organization_id(ctx):
        return organization_required_result(what="create a list", tool_name="picklist", ctx=ctx)
    try:
        result = await _picklist_store_arm().create_list(
            list_name=list_name, description=description, items=items
        )
    except Exception as exc:  # noqa: BLE001 — said in the store's words
        return _failed(exc)
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


async def userlist_create(args: dict[str, Any], ctx: ToolContext) -> ToolResult:
    list_name = args.get("list_name", "")
    items = args.get("items", [])
    if not list_name:
        return ToolResult(
            success=False,
            error=ToolError(error_type="validation", message="list_name is required."),
        )
    if not items:
        return ToolResult(
            success=False,
            error=ToolError(error_type="validation", message="items must be a non-empty list."),
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
    return await _create(list_name, args.get("description", ""), items, ctx)


async def userlist_create_simple(args: dict[str, Any], ctx: ToolContext) -> ToolResult:
    list_name = args.get("list_name", "")
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
                error_type="validation", message="labels must be a non-empty list of strings."
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
    items = [{"label": label, "group_name": group_name} for label in labels]
    return await _create(list_name, args.get("description", ""), items, ctx)


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


def grouped_choices(items: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Choices grouped by ``group_name``."""
    groups: dict[str | None, list[dict[str, Any]]] = {}
    for item in items:
        groups.setdefault(item.get("group_name"), []).append(
            {k: item.get(k) for k in ("id", "label", "description", "help_text", "icon_name")}
        )
    return [
        {"group_name": name, "items": sorted(members, key=lambda m: m.get("label") or "")}
        for name, members in sorted(groups.items(), key=lambda kv: kv[0] or "")
    ]


async def userlist_get_all(args: dict[str, Any], ctx: ToolContext) -> ToolResult:
    """Every list the person may see, in every organization they belong to."""
    page = max(1, args.get("page", 1))
    page_size = min(100, max(1, args.get("page_size", 50)))
    search = (args.get("search_term") or "").lower()
    try:
        index = await _picklist_store_arm().list_index()
    except Exception as exc:  # noqa: BLE001 — said in the store's words
        return _failed(exc)
    lists = [
        {
            "id": str(r.get("id")),
            "list_name": r.get("list_name"),
            "description": r.get("description"),
            "user_id": str(r["created_by"]) if r.get("created_by") else None,
            "organization_id": str(r["organization_id"]) if r.get("organization_id") else None,
            "organization_name": r.get("organization_name"),
            "updated_at": r.get("updated_at"),
            "item_count": int(r.get("item_count") or 0),
        }
        for r in index
        if not search
        or search in (r.get("list_name") or "").lower()
        or search in (r.get("description") or "").lower()
    ]
    lists.sort(key=lambda r: str(r.get("updated_at") or ""), reverse=True)
    chosen = _make_serializable(lists[(page - 1) * page_size : page * page_size])
    return ToolResult(
        success=True,
        output={"lists": chosen, "page": page, "page_size": page_size, "count": len(chosen)},
    )


async def _read_list(list_id: str) -> dict[str, Any] | None:
    return await _picklist_store_arm().read_list(str(list_id))


async def userlist_get_details(args: dict[str, Any], ctx: ToolContext) -> ToolResult:
    """One list and its choices, as the person sees them."""
    list_id = args.get("list_id")
    group_by = args.get("group_by", False)
    if not list_id:
        return ToolResult(
            success=False,
            error=ToolError(error_type="validation", message="list_id is required."),
        )
    try:
        listing = await _read_list(str(list_id))
    except Exception as exc:  # noqa: BLE001 — said in the store's words
        return _failed(exc)
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


#: Choice words a person may set through the tool.
_WRITABLE = ("label", "description", "help_text", "group_name", "icon_name")


def _held(exc: Exception) -> bool:
    return type(exc).__name__ == "ChangeWaits"


async def userlist_update_item(args: dict[str, Any], ctx: ToolContext) -> ToolResult:
    item_id = args.get("item_id")
    if not item_id:
        return ToolResult(
            success=False,
            error=ToolError(error_type="validation", message="item_id is required."),
        )
    update_fields = {k: args[k] for k in _WRITABLE if k in args}
    if not update_fields:
        return ToolResult(
            success=False,
            error=ToolError(
                error_type="validation",
                message="Give at least one of label, description, help_text, group_name, icon_name.",
            ),
        )

    from matrx_ai.config.read_only_resources import READ_ONLY_TOOL_MESSAGE

    if await _picklist_item_is_read_only(str(item_id)):
        return ToolResult(
            success=False,
            error=ToolError(error_type="read_only", message=READ_ONLY_TOOL_MESSAGE),
        )
    try:
        await _picklist_store_arm().update_choice(str(item_id), update_fields)
    except Exception as exc:  # noqa: BLE001 — a held change is not a failure
        if _held(exc):
            return _held_result(exc)
        return _failed(exc)
    return ToolResult(
        success=True,
        output_kind="picklist_item_update_result",
        output={"item_id": item_id, "message": "Item updated successfully."},
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
            error=ToolError(error_type="validation", message="items must be a non-empty list."),
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
            await _picklist_store_arm().update_choice(
                str(item_id), {k: item.get(k) for k in _WRITABLE}
            )
        except Exception as exc:  # noqa: BLE001 — each choice answers for itself
            failed_items.append(
                {
                    "item_id": item_id,
                    "error": "held for approval; nothing written yet" if _held(exc) else str(exc),
                }
            )
            continue
        success_count += 1

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


#: What a choice receipt shows.
_CHOICE_FIELDS = ("label", "description", "help_text", "group_name", "icon_name")


async def _read_choices(list_id: str, item_ids: set[str]) -> dict[str, dict[str, Any]]:
    """item id → its fields, for ``item_ids`` of ``list_id``, read as the person. A list the
    person cannot open has no receipt."""
    listing = await _read_list(str(list_id))
    if listing is None:
        raise LookupError(f"List {list_id} is not open to this person; no receipt is read.")
    return {
        str(r.get("id")): {k: r.get(k) for k in _CHOICE_FIELDS}
        for r in _make_serializable(listing["items"])
        if str(r.get("id")) in item_ids
    }


async def _choice_list_id(item_id: str) -> str:
    list_id = await _picklist_store_arm().list_of_choice(item_id)
    if not list_id:
        raise LookupError(f"choice {item_id} has no list")
    return list_id


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
    # Read the wire model's coerced values (e.g. a JSON-string list decoded), never the
    # raw arguments they were coerced from (the 2026-10-01 dataset update_row class).
    args = {**args, **parsed.model_dump(exclude_unset=True)}
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
            for k in _WRITABLE
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
