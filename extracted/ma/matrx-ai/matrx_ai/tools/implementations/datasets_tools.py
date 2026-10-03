"""The agents' ``dataset`` tool — a person's tables, read and written in the record store.

Every table lives in the record store (``custom.*``) under the id it always had. The tool
lives in this package, which must never import matrx-records, so the store half is injected
by the host (``matrx_ai.configure(dataset_store_arm=...)``; aidream wires
``matrx_records.agent.dataset_arm.DatasetStoreArm``) and every verb is answered there, under
the operating person's own principal. A host without the arm gets a refusal that names the
wiring, never a guess. Arguments and answers keep the shape agents were taught.
"""

from __future__ import annotations

import json
import logging
import time
import traceback
from typing import Any

from pydantic import ValidationError

from matrx_ai.tools._dispatch_util import format_args_error
from matrx_ai.tools.arg_models import DatasetArgs
from matrx_ai.tools.arg_models._coercion import coerce_field_values
from matrx_ai.tools.models import ToolContext, ToolError, ToolResult
from matrx_ai.tools.organization_hold import (
    carried_organization_id,
    organization_required_result,
)

logger = logging.getLogger(__name__)

_DATASET_RESULT_BUDGET_CHARS = 40_000
_DATASET_CELL_BUDGET_CHARS = 8_000


def _bounded_dataset_rows(
    rows: list[dict[str, Any]],
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    """Keep arbitrary user JSON structured while bounding one model-visible page."""
    bounded: list[dict[str, Any]] = []
    used = 0
    truncated_cells = 0
    for row in rows:
        data = row.get("data", {})
        data_json = json.dumps(data, default=str, ensure_ascii=True)
        if len(data_json) > _DATASET_CELL_BUDGET_CHARS:
            data = {
                "preview": data_json[:_DATASET_CELL_BUDGET_CHARS],
                "total_chars": len(data_json),
                "truncated": True,
                "remedy": "Request a narrower dataset page or search query.",
            }
            truncated_cells += 1
        candidate = {**row, "data": data}
        candidate_chars = len(json.dumps(candidate, default=str, ensure_ascii=False))
        if bounded and used + candidate_chars > _DATASET_RESULT_BUDGET_CHARS:
            break
        bounded.append(candidate)
        used += candidate_chars
    return bounded, {
        "returned_rows": len(bounded),
        "available_rows_in_page": len(rows),
        "rows_truncated": len(bounded) < len(rows),
        "truncated_cells": truncated_cells,
    }


def _say_the_cut(output: dict[str, Any], cap: dict[str, Any], offset: int) -> dict[str, Any]:
    """A page the size budget CUT says so: its true row count, PARTIAL, and where the rest is.

    VISION-REACH W2 verifier (2026-10-02): `get` with limit 215 on a 215-row table answered
    ``"count": 215`` and no PARTIAL note while carrying 163 rows — the budget above cut the
    other 52 AFTER the page had been judged whole. The count a model reads is the rows it got."""
    if not cap.get("rows_truncated"):
        return output
    shown = int(cap.get("returned_rows") or 0)
    total = output.get("total_rows")
    output["count"] = shown
    output["partial"] = True
    output["totals_note"] = (
        f"PARTIAL: rows {offset + 1}-{offset + shown} of "
        + (f"{total}" if total is not None else "more")
        + f" — this page was cut to fit; the next page starts at offset {offset + shown}. A count, "
        "total, average or list of who/which over the table MUST come from the records tool's "
        "record_aggregate — never count or add up these rows."
    )
    return output


def _self_capped(result: ToolResult) -> ToolResult:
    result.output_self_capped = True
    return result


# ---------------------------------------------------------------------------
# The record-store arm
# ---------------------------------------------------------------------------

#: The ``_ext`` key the host's record-store arm is registered under.
STORE_ARM_EXT_KEY = "dataset_store_arm"

#: What a host without the arm is told — the one wiring that serves every verb.
UNWIRED_MESSAGE = (
    "This server has no record store wired for the dataset tool, so nothing was read or "
    "written. REMEDY: matrx_ai.configure(dataset_store_arm=DatasetStoreArm())."
)


class _NoArm(Exception):
    """The host never wired the record-store arm."""


def _store_arm() -> Any:
    """The host's record-store arm; :class:`_NoArm` when it was never wired."""
    from matrx_ai._ext import get_ext, has_ext

    if has_ext(STORE_ARM_EXT_KEY):
        return get_ext(STORE_ARM_EXT_KEY)
    logger.error("matrx-ai has no '%s' configured: %s", STORE_ARM_EXT_KEY, UNWIRED_MESSAGE)
    raise _NoArm(UNWIRED_MESSAGE)


#: What the agent is told to do with a held write. It is not an error, so it must not retry
#: (a retry files a SECOND wait for the same change) and must not apologise for a failure
#: that did not happen: the change is in the organization's approval queue and a person
#: decides it from the card in the chat or from the table's own page.
HELD_FOR_APPROVAL_GUIDANCE = (
    "HELD FOR APPROVAL — not an error. Nothing was written yet: the change is in this "
    "organization's approval queue and lands the moment a person approves it. Do NOT call "
    "the tool again for this change (that would queue it twice) and do not apologise. Tell "
    "the person, in one sentence, that it is waiting for their approval (name who can "
    "approve it if `approvers` names anyone), and that they can Approve or Refuse it on the "
    "card in this chat or on the table's page."
)


def held_for_approval_output(answer: dict[str, Any], message: str) -> dict[str, Any]:
    """THE output of a held write, for every tool that reports one.

    The store's own wait, plus the three keys that tell a model and a screen it is held
    (not an error) and what to do. Shared so the ``data`` tool's "save as a table" answers
    exactly what this tool answers (lane HELD-WRITE-TAILS, 2026-09-26) — one shape, one
    card (`readRecordChangeWait` in the frontend).
    """
    return {
        **answer,
        "status": "held_for_approval",
        "held_for_approval": True,
        "applied": False,
        "not_done": str(answer.get("not_done") or message),
        "what_to_do": HELD_FOR_APPROVAL_GUIDANCE,
    }


def _held_for_approval(answer: dict[str, Any], message: str) -> ToolResult:
    """A write the store HELD for a person — a success of its own kind, never an error.

    VERIFIER-26 item 5 (2026-09-26): this used to be ``success=False`` with
    ``error_type="approval_required"``. The chat drew it as "The agent sent invalid
    arguments" (the word *required* matched the argument-error pattern), the card that
    lets a person approve never mounted because an error carries no result, and the agent
    read a failure and retried or apologised. The store's own wait — ``approval_id``,
    ``approvers``, the rows, ``not_done`` — is the output, exactly the shape the
    ``records`` tool answers, so one card serves both.
    """
    return ToolResult(success=True, output=held_for_approval_output(answer, message))


def _arm_error(exc: Exception) -> ToolResult:
    """A record-store refusal, as the tool's own error; a held write, as a held write."""
    name = type(exc).__name__
    if name == "_NoArm":
        return ToolResult(
            success=False, error=ToolError(error_type="unavailable", message=str(exc))
        )
    if name == "ChangeWaits":
        answer = getattr(exc, "answer", None)
        if isinstance(answer, dict) and answer.get("awaiting_approval") is True:
            return _held_for_approval(answer, str(exc))
        # Refused AND not queued (the queue itself refused, or nothing could be filed): the
        # change did not happen and nothing is waiting — that IS a refusal, said in the
        # store's own words, and never dressed as a wait nobody filed.
        return ToolResult(
            success=False,
            error=ToolError(error_type="not_written", message=str(exc)),
        )
    if name == "UnknownFieldKeys":
        return ToolResult(
            success=False, error=ToolError(error_type="validation", message=str(exc))
        )
    if name == "NoOperatingPerson":
        return ToolResult(
            success=False, error=ToolError(error_type="authentication", message=str(exc))
        )
    sqlstate = getattr(exc, "sqlstate", None)
    return ToolResult(
        success=False,
        error=ToolError(
            error_type="not_found" if sqlstate == "02000" else "database",
            message=str(exc),
            traceback=traceback.format_exc(),
        ),
    )


async def _rows_in_words(
    table_id: str, rows: list[dict[str, Any]], ctx: ToolContext
) -> list[dict[str, Any]]:
    """Every ``relation`` cell of this page as the WORDS it means, not the id it stores.

    A relation column holds a record's identifier and shows that record's name. Handing a
    model the identifier is the same defect the screen had before OLD-TABLES-3, one layer
    down. The resolver is injected by the host (``matrx_ai.configure(
    relation_words_resolver=...)``) because the one implementation lives in matrx-records,
    which depends on this package — see ``matrx_ai/tools/relation_words.py``.

    Resolution runs under the OPERATING PERSON's identity (``ctx.user_id``) and never on a
    privileged pool: a row this person may not open comes back withheld, never as a name.
    """
    from matrx_ai.tools.relation_words import resolve_relation_columns

    try:
        user_id = ctx.user_id
    except Exception:  # noqa: BLE001 — no request identity ⇒ nothing to resolve AS
        return rows

    indexes = [i for i, row in enumerate(rows) if isinstance(row.get("data"), dict)]
    if not indexes:
        return rows
    resolved = await resolve_relation_columns(
        table_id, [rows[i]["data"] for i in indexes], user_id=user_id
    )
    if len(resolved) != len(indexes):
        return rows
    for position, index in enumerate(indexes):
        rows[index] = {**rows[index], "data": resolved[position]}
    return rows


def _required(value: Any, name: str) -> ToolResult | None:
    if str(value or "").strip():
        return None
    return ToolResult(
        success=False,
        error=ToolError(error_type="validation", message=f"{name} is required."),
    )


def _read_only(*ids: str) -> ToolResult | None:
    from matrx_ai.config.read_only_resources import READ_ONLY_TOOL_MESSAGE, is_resource_read_only

    if any(is_resource_read_only(i) for i in ids):
        return ToolResult(
            success=False,
            error=ToolError(error_type="read_only", message=READ_ONLY_TOOL_MESSAGE),
        )
    return None


def _rows_page(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [
        {
            "row_id": str(r.get("row_id", "")),
            "data": r.get("data", {}),
            "created_at": str(r.get("created_at", "")),
        }
        for r in rows
    ]


# ---------------------------------------------------------------------------
# Reads
# ---------------------------------------------------------------------------


async def usertable_get_all(args: dict[str, Any], ctx: ToolContext) -> ToolResult:
    try:
        tables = await _store_arm().list_tables()
    except Exception as exc:  # noqa: BLE001 — carried out whole
        return _arm_error(exc)
    return _self_capped(
        ToolResult(
            success=True,
            output={
                "tables": tables[:200],
                "count": len(tables),
                "truncated": len(tables) > 200,
            },
        )
    )


async def usertable_get_metadata(args: dict[str, Any], ctx: ToolContext) -> ToolResult:
    table_id = args.get("table_id", "").strip()
    if missing := _required(table_id, "table_id"):
        return missing
    try:
        meta = (await _store_arm().get(table_id, include="metadata"))["metadata"]
    except Exception as exc:  # noqa: BLE001 — carried out whole
        return _arm_error(exc)
    return ToolResult(
        success=True,
        output_kind="dataset_metadata_result",
        output={
            "table_id": meta["dataset_id"],
            "table_name": meta["dataset_name"],
            **{k: v for k, v in meta.items() if k not in {"dataset_id", "dataset_name"}},
        },
    )


async def usertable_get_fields(args: dict[str, Any], ctx: ToolContext) -> ToolResult:
    table_id = args.get("table_id", "").strip()
    if missing := _required(table_id, "table_id"):
        return missing
    try:
        fields = await _store_arm().fields(table_id)
    except Exception as exc:  # noqa: BLE001 — carried out whole
        return _arm_error(exc)
    return _self_capped(
        ToolResult(
            success=True,
            output_kind="dataset_fields_result",
            output={
                "fields": fields[:200],
                "count": len(fields),
                "truncated": len(fields) > 200,
            },
        )
    )


async def usertable_get_data(args: dict[str, Any], ctx: ToolContext) -> ToolResult:
    table_id = args.get("table_id", "").strip()
    if missing := _required(table_id, "table_id"):
        return missing
    limit = int(args.get("limit", 50))
    offset = int(args.get("offset", 0))
    try:
        got = await _store_arm().get(
            table_id,
            include="data",
            limit=limit,
            offset=offset,
            sort_by=args.get("sort_field") or None,
            sort_order=(args.get("sort_direction") or "asc").lower(),
        )
        data = await _rows_in_words(table_id, _rows_page(got["rows"]), ctx)
    except Exception as exc:  # noqa: BLE001 — carried out whole
        return _arm_error(exc)
    page_count = len(data)
    data, cap = _bounded_dataset_rows(data)
    return _self_capped(
        ToolResult(
            success=True,
            output=_say_the_cut(
                {"rows": data, "count": page_count, "offset": offset, "limit": limit,
                 "total_rows": got.get("total_rows"), "cap": cap},
                cap,
                offset,
            ),
        )
    )


async def usertable_search_data(args: dict[str, Any], ctx: ToolContext) -> ToolResult:
    table_id = args.get("table_id", "").strip()
    search_term = args.get("search_term", "").strip()
    if missing := _required(table_id, "table_id") or _required(search_term, "search_term"):
        return missing
    limit = int(args.get("limit", 50))
    offset = int(args.get("offset", 0))
    try:
        hits = await _store_arm().search(table_id, term=search_term, limit=limit, offset=offset)
        data = await _rows_in_words(table_id, _rows_page(hits), ctx)
    except Exception as exc:  # noqa: BLE001 — carried out whole
        return _arm_error(exc)
    page_count = len(data)
    data, cap = _bounded_dataset_rows(data)
    return _self_capped(
        ToolResult(
            success=True,
            output=_say_the_cut(
                {"rows": data, "count": page_count, "search_term": search_term, "cap": cap},
                cap,
                offset,
            ),
        )
    )


# ---------------------------------------------------------------------------
# Writes
# ---------------------------------------------------------------------------


async def usertable_add_rows(args: dict[str, Any], ctx: ToolContext) -> ToolResult:
    table_id = args.get("table_id", "").strip()
    rows_input = args.get("rows")
    if missing := _required(table_id, "table_id"):
        return missing
    if not rows_input or not isinstance(rows_input, list):
        return ToolResult(
            success=False,
            error=ToolError(
                error_type="validation",
                message="rows must be a non-empty list of dicts.",
            ),
        )
    if refused := _read_only(table_id):
        return refused
    try:
        return ToolResult(success=True, output=await _store_arm().add_rows(table_id, rows_input))
    except Exception as exc:  # noqa: BLE001 — a refusal or a wait, said as such
        return _arm_error(exc)


#: What ``update_row`` wants, said with an example — never just "must be a dict".
UPDATE_ROW_DATA_SHAPE = (
    "update_row needs `data`: ONE JSON object of the whole row, field name to value — it "
    "REPLACES the row, so send every field, not only the one you change. Example: "
    '{"action": "update_row", "dataset_id": "<id>", "row_id": "<id>", "data": '
    '{"carrier": "Golden State Movers", "booking_status": "Under way"}}. '
    "Pass the object itself, not a string and not a list."
)



async def usertable_update_row(args: dict[str, Any], ctx: ToolContext) -> ToolResult:
    row_id = args.get("row_id", "").strip()
    table_id = args.get("table_id", "").strip()
    if missing := _required(row_id, "row_id") or _required(table_id, "table_id"):
        return missing
    data = coerce_field_values(args.get("data"))
    if not data or not isinstance(data, dict):
        return ToolResult(
            success=False,
            error=ToolError(error_type="validation", message=UPDATE_ROW_DATA_SHAPE),
        )
    if refused := _read_only(table_id, row_id):
        return refused
    try:
        return ToolResult(
            success=True, output=await _store_arm().update_row(table_id, row_id, data)
        )
    except Exception as exc:  # noqa: BLE001 — a refusal or a wait, said as such
        return _arm_error(exc)


async def usertable_delete_row(args: dict[str, Any], ctx: ToolContext) -> ToolResult:
    row_id = args.get("row_id", "").strip()
    table_id = args.get("table_id", "").strip()
    if missing := _required(row_id, "row_id") or _required(table_id, "table_id"):
        return missing
    if refused := _read_only(table_id, row_id):
        return refused
    try:
        # Archived, never removed: the store's delete is a soft delete, restorable from /trash.
        return ToolResult(success=True, output=await _store_arm().delete_row(table_id, row_id))
    except Exception as exc:  # noqa: BLE001 — a refusal or a wait, said as such
        return _arm_error(exc)


# ---------------------------------------------------------------------------
# dataset — unified action dispatcher
# ---------------------------------------------------------------------------

# Valid `dataset` actions are enforced by the DatasetArgs discriminated union
# (arg_models/dispatcher_args.py) + tool_def.parameters."$variants" — the source of truth.


async def _read_row_data(table_id: str, row_id: str) -> dict[str, Any]:
    """One row's values, JSON-safe, for the before/after receipt of ``update_row``."""
    data = await _store_arm().read_row(table_id, row_id)
    return json.loads(json.dumps(dict(data or {}), default=str))


async def _prior_row_data(table_id: str, row_id: str) -> dict[str, Any] | None:
    """The row's data before ``update_row``, or ``None`` (no receipt)."""
    from matrx_ai.tools.structured_surface_write import read_prior

    return await read_prior(
        lambda: _read_row_data(table_id, row_id), what=f"dataset row {table_id}/{row_id}"
    )


async def _row_surface_write(
    result: ToolResult, table_id: str, row_id: str, prior: dict[str, Any] | None
) -> ToolResult:
    """Before → after of the row's fields that ``update_row`` (a REPLACE) moved."""
    from matrx_ai.tools.structured_surface_write import read_prior, structured_surface_write

    if not result.success or prior is None:
        return result
    if isinstance(result.output, dict) and result.output.get("held_for_approval"):
        return result
    after = await read_prior(
        lambda: _read_row_data(table_id, row_id), what=f"dataset row {table_id}/{row_id} (after)"
    )
    return structured_surface_write(
        result,
        before=prior,
        after=after,
        target_type="dataset_row",
        target_id=row_id,
        target_label=f"row {row_id}",
        ignore=(),
    )


def _stamp(result: ToolResult, started_at: float, ctx: ToolContext) -> ToolResult:
    result.tool_name = "dataset"
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
        tool_name="dataset",
        call_id=ctx.call_id,
    )


async def _dataset_get(args: dict[str, Any], ctx: ToolContext, started_at: float) -> ToolResult:
    dataset_id = (args.get("dataset_id") or "").strip()
    if not dataset_id:
        return _validation_error("dataset_id is required for action=get.", started_at, ctx)

    include = (args.get("include") or "all").lower()
    if include not in {"data", "fields", "metadata", "all"}:
        return _validation_error(
            f"include must be one of: data, fields, metadata, all (got '{include}').",
            started_at,
            ctx,
        )
    try:
        output = await _store_arm().get(
            dataset_id,
            include=include,
            limit=int(args.get("limit", 50)),
            offset=int(args.get("offset", 0)),
            sort_by=args.get("sort_by") or None,
            sort_order=(args.get("sort_order") or "asc").lower(),
        )
        if "rows" in output:
            raw_rows = await _rows_in_words(dataset_id, output["rows"], ctx)
            output["rows"], output["cap"] = _bounded_dataset_rows(raw_rows)
            _say_the_cut(output, output["cap"], int(args.get("offset", 0)))
    except Exception as exc:  # noqa: BLE001 — carried out whole
        return _stamp(_arm_error(exc), started_at, ctx)
    return _self_capped(_stamp(ToolResult(success=True, output=output), started_at, ctx))


async def _dataset_create(args: dict[str, Any], ctx: ToolContext, started_at: float) -> ToolResult:
    # A dataset belongs to the organization this conversation CARRIES. No organization → the
    # one organization hold, before the store is touched. Never defaulted.
    if not carried_organization_id(ctx):
        return organization_required_result(
            what="create a dataset", tool_name="dataset", ctx=ctx, started_at=started_at
        )
    table_name = (args.get("dataset_name") or "").strip()
    data = args.get("data")
    if not table_name:
        return _validation_error("dataset_name is required for action=create.", started_at, ctx)
    if not data or not isinstance(data, list):
        return _validation_error(
            "data must be a non-empty list of dicts, each representing a row.", started_at, ctx
        )
    try:
        made = await _store_arm().create(
            name=table_name, description=args.get("description", "") or "", data=data
        )
    except Exception as exc:  # noqa: BLE001 — a refusal or a wait, said as such
        return _stamp(_arm_error(exc), started_at, ctx)
    return _stamp(ToolResult(success=True, output=made), started_at, ctx)


async def dataset(args: dict[str, Any], ctx: ToolContext) -> ToolResult:
    started_at = time.time()
    try:
        parsed = DatasetArgs.model_validate(args).root
    except ValidationError as exc:
        return _validation_error(format_args_error(exc), started_at, ctx)
    # The wire model's coercions (a JSON-string row decoded, field/value pairs folded)
    # are the contract — read them, never the raw arguments they were coerced from.
    args = {**args, **parsed.model_dump(exclude_unset=True)}
    action = parsed.action

    if action == "list":
        return _stamp(await usertable_get_all({}, ctx), started_at, ctx)

    if action == "get":
        return await _dataset_get(args, ctx, started_at)

    if action == "search":
        query = (args.get("query") or "").strip()
        if not query:
            return _validation_error("query is required for action=search.", started_at, ctx)
        return _stamp(
            await usertable_search_data(
                {
                    "table_id": args.get("dataset_id", ""),
                    "search_term": query,
                    "limit": args.get("limit", 50),
                    "offset": args.get("offset", 0),
                },
                ctx,
            ),
            started_at,
            ctx,
        )

    if action == "create":
        return await _dataset_create(args, ctx, started_at)

    if action == "add_rows":
        return _stamp(
            await usertable_add_rows(
                {"table_id": args.get("dataset_id", ""), "rows": args.get("rows")},
                ctx,
            ),
            started_at,
            ctx,
        )

    if action == "update_row":
        table_id = (args.get("dataset_id") or "").strip()
        row_id = (args.get("row_id") or "").strip()
        prior = await _prior_row_data(table_id, row_id) if table_id and row_id else None
        result = await usertable_update_row(
            {"table_id": table_id, "row_id": row_id, "data": args.get("data")},
            ctx,
        )
        return _stamp(
            await _row_surface_write(result, table_id, row_id, prior),
            started_at,
            ctx,
        )

    # action == "delete_row"
    return _stamp(
        await usertable_delete_row(
            {
                "table_id": args.get("dataset_id", ""),
                "row_id": args.get("row_id", ""),
            },
            ctx,
        ),
        started_at,
        ctx,
    )
