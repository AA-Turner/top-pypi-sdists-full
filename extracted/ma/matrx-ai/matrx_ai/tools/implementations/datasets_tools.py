"""Datasets tool implementations.

Provides full CRUD access to a user's structured datasets
(stored in workbench.udt_datasets / workbench.udt_dataset_fields / workbench.udt_dataset_rows).

A "dataset" here is a user-owned tabular data store created by the AI on
behalf of the user. All operations are scoped to ctx.user_id automatically.

The exposed tool names retain the ``usertable_*`` prefix so existing agent
definitions and the persisted tools registry keep working unchanged.

TWO STORES, ONE TOOL (CUTOVER-PLAN rev 3, row A1). A table moved to the record store keeps
its dataset id, and its older copy is archived. So every verb that names a table first asks
WHERE THAT TABLE LIVES — the host-injected record-store arm (``dataset_store_arm``, wired in
``aidream/package_integration.py`` to ``matrx_records.agent.dataset_arm.DatasetStoreArm``,
which asks ``matrx_records.server.table_home``, the same answer the frontend's
``whereThisTableLives`` gives). A moved table is served through the store's own doors under
the operating person's principal; an older table keeps the body below. ``create`` is born in
the record store once the organization's tables have moved. Arguments and answers are the
same shape on both arms, so none of the agents that carry this tool changes. After the flip
the older arm is removed.
"""

from __future__ import annotations

import asyncio
import json
import logging
import time
import traceback
from typing import Any

from pydantic import ValidationError

from matrx_ai.tools._dispatch_util import format_args_error
from matrx_ai.tools.arg_models import DatasetArgs
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


def _self_capped(result: ToolResult) -> ToolResult:
    result.output_self_capped = True
    return result


# ---------------------------------------------------------------------------
# Where does this table live? — the record-store arm (row A1)
# ---------------------------------------------------------------------------

#: The ``_ext`` key the host's record-store arm is registered under.
STORE_ARM_EXT_KEY = "dataset_store_arm"

_arm_announced: set[str] = set()


def _store_arm() -> Any | None:
    """The host's record-store arm, or ``None`` on a host that has no record store.

    Unwired is ANNOUNCED once, by name: a host that forgets the wiring would otherwise read
    every moved table from its archived older copy, silently.
    """
    from matrx_ai._ext import get_ext, has_ext

    if has_ext(STORE_ARM_EXT_KEY):
        return get_ext(STORE_ARM_EXT_KEY)
    if "unwired" not in _arm_announced:
        _arm_announced.add("unwired")
        import logging

        logging.getLogger(__name__).warning(
            "matrx-ai has no '%s' configured, so the dataset tool reads and writes ONLY the "
            "older tables; a table moved to the record store is answered from its archived "
            "copy. REMEDY: aidream/package_integration.py, "
            "matrx_ai.configure(dataset_store_arm=DatasetStoreArm()).",
            STORE_ARM_EXT_KEY,
        )
    return None


class _ArmFailed(Exception):
    def __init__(self, result: ToolResult) -> None:
        self.result = result
        super().__init__(result.error.message if result.error else "the record store failed")


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


async def _moved(table_id: str) -> Any | None:
    """The arm when ``table_id`` lives in the record store, else ``None`` (an older table).

    A store that could not be asked RAISES :class:`_ArmFailed` carrying the error: answering
    "older" to a failed question would send a moved table's write to its archived copy.
    """
    arm = _store_arm()
    if arm is None or not table_id:
        return None
    try:
        home = await arm.home(table_id)
    except Exception as exc:  # noqa: BLE001 — carried out whole, never swallowed
        raise _ArmFailed(_arm_error(exc)) from exc
    return arm if getattr(home, "in_the_record_store", False) else None


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _run_query(query_name: str, params: dict[str, Any]) -> list[dict]:
    from matrx_orm.sql_executor import execute_query

    result = execute_query(query_name, params)
    return result if isinstance(result, list) else []


def _run_batch(query_name: str, batch_params: list[dict], batch_size: int = 50) -> list[dict]:
    from matrx_orm.sql_executor import execute_query

    result = execute_query(query_name, batch_params=batch_params, batch_size=batch_size)
    return result if isinstance(result, list) else []


# ---------------------------------------------------------------------------
# get_personal_tables
# ---------------------------------------------------------------------------


async def usertable_get_all(args: dict[str, Any], ctx: ToolContext) -> ToolResult:
    try:
        rows = await asyncio.to_thread(
            _run_query,
            "datasets_list_for_user",
            {"user_id": ctx.user_id},
        )
        tables = [
            {
                "table_id": str(r.get("id", "")),
                "table_name": r.get("table_name", ""),
                "description": r.get("description", ""),
                "row_count": r.get("row_count", 0),
                "created_at": str(r.get("created_at", "")),
            }
            for r in rows
        ]
        # THE RECORD STORE'S TABLES TOO. A moved table's older copy is archived, so the
        # older list no longer carries it; without this a table the person can open on the
        # new screen would vanish from the one list the agent can see.
        arm = _store_arm()
        if arm is not None:
            try:
                in_store = await arm.list_tables()
            except Exception as exc:  # noqa: BLE001 — carried out whole
                return _arm_error(exc)
            seen = {t["table_id"] for t in in_store}
            tables = in_store + [t for t in tables if t["table_id"] not in seen]
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
    except Exception as e:
        return ToolResult(
            success=False,
            error=ToolError(
                error_type="database", message=str(e), traceback=traceback.format_exc()
            ),
        )


# ---------------------------------------------------------------------------
# get_personal_table_metadata
# ---------------------------------------------------------------------------


async def usertable_get_metadata(args: dict[str, Any], ctx: ToolContext) -> ToolResult:
    table_id = args.get("table_id", "").strip()
    if not table_id:
        return ToolResult(
            success=False,
            error=ToolError(error_type="validation", message="table_id is required."),
        )

    try:
        arm = await _moved(table_id)
        if arm is not None:
            meta = (await arm.get(table_id, include="metadata"))["metadata"]
            return ToolResult(
                success=True,
                output={
                    "table_id": meta["dataset_id"],
                    "table_name": meta["dataset_name"],
                    **{k: v for k, v in meta.items() if k not in {"dataset_id", "dataset_name"}},
                },
            )
        rows = await asyncio.to_thread(
            _run_query,
            "datasets_get_metadata",
            {"table_id": table_id},
        )
        if not rows:
            return ToolResult(
                success=False,
                error=ToolError(
                    error_type="not_found",
                    message=f"No table found with id '{table_id}'.",
                ),
            )
        r = rows[0]
        return ToolResult(
            success=True,
            output={
                "table_id": str(r.get("id", "")),
                "table_name": r.get("table_name", ""),
                "description": r.get("description", ""),
                "version": r.get("version", 1),
                "is_public": r.get("is_public", False),
                "authenticated_read": r.get("authenticated_read", False),
                "row_count": r.get("row_count", 0),
                "created_at": str(r.get("created_at", "")),
                "updated_at": str(r.get("updated_at", "")),
            },
        )
    except Exception as e:
        return ToolResult(
            success=False,
            error=ToolError(
                error_type="database", message=str(e), traceback=traceback.format_exc()
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


# ---------------------------------------------------------------------------
# get_personal_table_fields
# ---------------------------------------------------------------------------


async def usertable_get_fields(args: dict[str, Any], ctx: ToolContext) -> ToolResult:
    table_id = args.get("table_id", "").strip()
    if not table_id:
        return ToolResult(
            success=False,
            error=ToolError(error_type="validation", message="table_id is required."),
        )

    try:
        arm = await _moved(table_id)
        if arm is not None:
            fields = await arm.fields(table_id)
            return _self_capped(
                ToolResult(
                    success=True,
                    output={
                        "fields": fields[:200],
                        "count": len(fields),
                        "truncated": len(fields) > 200,
                    },
                )
            )
        rows = await asyncio.to_thread(
            _run_query,
            "datasets_get_fields",
            {"table_id": table_id},
        )
        fields = [
            {
                "field_id": str(r.get("id", "")),
                "field_name": r.get("field_name", ""),
                "display_name": r.get("display_name", ""),
                "data_type": r.get("data_type", "string"),
                "field_order": r.get("field_order", 0),
                "is_required": r.get("is_required", False),
            }
            for r in rows
        ]
        return _self_capped(
            ToolResult(
                success=True,
                output={
                    "fields": fields[:200],
                    "count": len(fields),
                    "truncated": len(fields) > 200,
                },
            )
        )
    except Exception as e:
        return ToolResult(
            success=False,
            error=ToolError(
                error_type="database", message=str(e), traceback=traceback.format_exc()
            ),
        )


# ---------------------------------------------------------------------------
# get_personal_table_data
# ---------------------------------------------------------------------------


async def usertable_get_data(args: dict[str, Any], ctx: ToolContext) -> ToolResult:
    table_id = args.get("table_id", "").strip()
    if not table_id:
        return ToolResult(
            success=False,
            error=ToolError(error_type="validation", message="table_id is required."),
        )

    limit = int(args.get("limit", 50))
    offset = int(args.get("offset", 0))
    sort_field = args.get("sort_field") or None
    sort_direction = (args.get("sort_direction") or "asc").lower()

    if sort_field:
        query_name = (
            "datasets_get_rows_sorted_asc"
            if sort_direction != "desc"
            else "datasets_get_rows_sorted_desc"
        )
        params: dict[str, Any] = {
            "table_id": table_id,
            "limit": limit,
            "offset": offset,
            "sort_field": sort_field,
        }
    else:
        query_name = "datasets_get_rows"
        params = {"table_id": table_id, "limit": limit, "offset": offset}

    try:
        arm = await _moved(table_id)
        if arm is not None:
            got = await arm.get(
                table_id,
                include="data",
                limit=limit,
                offset=offset,
                sort_by=sort_field,
                sort_order=sort_direction,
            )
            rows = [
                {"id": r["row_id"], "data": r["data"], "created_at": r["created_at"]}
                for r in got["rows"]
            ]
        else:
            rows = await asyncio.to_thread(
                _run_query,
                query_name,
                params,
            )
        data = [
            {
                "row_id": str(r.get("id", "")),
                "data": r.get("data", {}),
                "created_at": str(r.get("created_at", "")),
            }
            for r in rows
        ]
        data = await _rows_in_words(table_id, data, ctx)
        page_count = len(data)
        data, cap = _bounded_dataset_rows(data)
        return _self_capped(
            ToolResult(
                success=True,
                output={
                    "rows": data,
                    "count": page_count,
                    "offset": offset,
                    "limit": limit,
                    "cap": cap,
                },
            )
        )
    except Exception as e:
        return ToolResult(
            success=False,
            error=ToolError(
                error_type="database", message=str(e), traceback=traceback.format_exc()
            ),
        )


# ---------------------------------------------------------------------------
# search_personal_table_data
# ---------------------------------------------------------------------------


async def usertable_search_data(args: dict[str, Any], ctx: ToolContext) -> ToolResult:
    table_id = args.get("table_id", "").strip()
    search_term = args.get("search_term", "").strip()
    if not table_id:
        return ToolResult(
            success=False,
            error=ToolError(error_type="validation", message="table_id is required."),
        )
    if not search_term:
        return ToolResult(
            success=False,
            error=ToolError(error_type="validation", message="search_term is required."),
        )

    limit = int(args.get("limit", 50))
    offset = int(args.get("offset", 0))

    wildcard_term = f"%{search_term}%" if "%" not in search_term else search_term

    try:
        arm = await _moved(table_id)
        if arm is not None:
            rows = [
                {"id": r["row_id"], "data": r["data"], "created_at": r["created_at"]}
                for r in await arm.search(
                    table_id, term=search_term, limit=limit, offset=offset
                )
            ]
        else:
            rows = await asyncio.to_thread(
                _run_query,
                "datasets_search_rows",
                {
                    "table_id": table_id,
                    "search_term": wildcard_term,
                    "limit": limit,
                    "offset": offset,
                },
            )
        data = [
            {
                "row_id": str(r.get("id", "")),
                "data": r.get("data", {}),
                "created_at": str(r.get("created_at", "")),
            }
            for r in rows
        ]
        data = await _rows_in_words(table_id, data, ctx)
        page_count = len(data)
        data, cap = _bounded_dataset_rows(data)
        return _self_capped(
            ToolResult(
                success=True,
                output={
                    "rows": data,
                    "count": page_count,
                    "search_term": search_term,
                    "cap": cap,
                },
            )
        )
    except Exception as e:
        return ToolResult(
            success=False,
            error=ToolError(
                error_type="database", message=str(e), traceback=traceback.format_exc()
            ),
        )


# ---------------------------------------------------------------------------
# add_personal_table_rows
# ---------------------------------------------------------------------------


async def usertable_add_rows(args: dict[str, Any], ctx: ToolContext) -> ToolResult:
    table_id = args.get("table_id", "").strip()
    rows_input = args.get("rows")
    if not table_id:
        return ToolResult(
            success=False,
            error=ToolError(error_type="validation", message="table_id is required."),
        )
    if not rows_input or not isinstance(rows_input, list):
        return ToolResult(
            success=False,
            error=ToolError(
                error_type="validation",
                message="rows must be a non-empty list of dicts.",
            ),
        )

    from matrx_ai.config.read_only_resources import READ_ONLY_TOOL_MESSAGE, is_resource_read_only

    if is_resource_read_only(table_id):
        return ToolResult(
            success=False,
            error=ToolError(error_type="read_only", message=READ_ONLY_TOOL_MESSAGE),
        )

    try:
        arm = await _moved(table_id)
    except _ArmFailed as failed:
        return failed.result
    if arm is not None:
        try:
            return ToolResult(success=True, output=await arm.add_rows(table_id, rows_input))
        except Exception as exc:  # noqa: BLE001 — a refusal or a wait, said as such
            return _arm_error(exc)

    batch_params = [
        {"table_id": table_id, "data": json.dumps(row), "user_id": ctx.user_id}
        for row in rows_input
    ]

    try:
        inserted = await asyncio.to_thread(
            _run_batch,
            "datasets_add_rows_batch",
            batch_params,
        )
        return ToolResult(
            success=True,
            output={
                "inserted": len(inserted),
                "table_id": table_id,
                "row_ids": [str(r.get("id", "")) for r in inserted],
            },
        )
    except Exception as e:
        return ToolResult(
            success=False,
            error=ToolError(
                error_type="database", message=str(e), traceback=traceback.format_exc()
            ),
        )


# ---------------------------------------------------------------------------
# update_personal_table_row
# ---------------------------------------------------------------------------


async def usertable_update_row(args: dict[str, Any], ctx: ToolContext) -> ToolResult:
    row_id = args.get("row_id", "").strip()
    table_id = args.get("table_id", "").strip()
    data = args.get("data")
    if not row_id:
        return ToolResult(
            success=False,
            error=ToolError(error_type="validation", message="row_id is required."),
        )
    if not table_id:
        return ToolResult(
            success=False,
            error=ToolError(error_type="validation", message="table_id is required."),
        )
    if not data or not isinstance(data, dict):
        return ToolResult(
            success=False,
            error=ToolError(
                error_type="validation", message="data must be a dict of field values."
            ),
        )

    from matrx_ai.config.read_only_resources import READ_ONLY_TOOL_MESSAGE, is_resource_read_only

    if is_resource_read_only(table_id) or is_resource_read_only(row_id):
        return ToolResult(
            success=False,
            error=ToolError(error_type="read_only", message=READ_ONLY_TOOL_MESSAGE),
        )

    try:
        arm = await _moved(table_id)
    except _ArmFailed as failed:
        return failed.result
    if arm is not None:
        try:
            return ToolResult(success=True, output=await arm.update_row(table_id, row_id, data))
        except Exception as exc:  # noqa: BLE001 — a refusal or a wait, said as such
            return _arm_error(exc)

    try:
        result = await asyncio.to_thread(
            _run_query,
            "datasets_update_row",
            {
                "id": row_id,
                "table_id": table_id,
                "data": json.dumps(data),
                "user_id": ctx.user_id,
            },
        )
        if not result:
            return ToolResult(
                success=False,
                error=ToolError(
                    error_type="not_found",
                    message=f"Row '{row_id}' not found in table '{table_id}' or you do not own it.",
                ),
            )
        return ToolResult(success=True, output={"updated_row_id": str(result[0].get("id", row_id))})
    except Exception as e:
        return ToolResult(
            success=False,
            error=ToolError(
                error_type="database", message=str(e), traceback=traceback.format_exc()
            ),
        )


# ---------------------------------------------------------------------------
# delete_personal_table_row
# ---------------------------------------------------------------------------


async def usertable_delete_row(args: dict[str, Any], ctx: ToolContext) -> ToolResult:
    row_id = args.get("row_id", "").strip()
    table_id = args.get("table_id", "").strip()
    if not row_id:
        return ToolResult(
            success=False,
            error=ToolError(error_type="validation", message="row_id is required."),
        )
    if not table_id:
        return ToolResult(
            success=False,
            error=ToolError(error_type="validation", message="table_id is required."),
        )

    from matrx_ai.config.read_only_resources import READ_ONLY_TOOL_MESSAGE, is_resource_read_only

    if is_resource_read_only(table_id) or is_resource_read_only(row_id):
        return ToolResult(
            success=False,
            error=ToolError(error_type="read_only", message=READ_ONLY_TOOL_MESSAGE),
        )

    try:
        arm = await _moved(table_id)
    except _ArmFailed as failed:
        return failed.result
    if arm is not None:
        try:
            return ToolResult(success=True, output=await arm.delete_row(table_id, row_id))
        except Exception as exc:  # noqa: BLE001 — a refusal or a wait, said as such
            return _arm_error(exc)

    try:
        from matrx_ai.db._registry import get_model as get_db_model
        from matrx_ai.tools.soft_delete import archive_where

        # Soft-delete law: the row is archived through deleted_at (restorable from /trash),
        # never removed. The server readers already skip archived rows.
        UdtDatasetRows = get_db_model("UdtDatasetRows")
        deleted_count = await archive_where(
            UdtDatasetRows, {"id": row_id, "table_id": table_id, "user_id": ctx.user_id}
        )
        if not deleted_count:
            return ToolResult(
                success=False,
                error=ToolError(
                    error_type="not_found",
                    message=f"Row '{row_id}' not found or you do not own it.",
                ),
            )
        return ToolResult(success=True, output={"deleted_row_id": row_id, "archived": True})
    except Exception as e:
        return ToolResult(
            success=False,
            error=ToolError(
                error_type="database", message=str(e), traceback=traceback.format_exc()
            ),
        )


# ---------------------------------------------------------------------------
# create_personal_table  (alias of old create_user_generated_table)
# ---------------------------------------------------------------------------


async def usertable_create_advanced(args: dict[str, Any], ctx: ToolContext) -> ToolResult:
    from matrx_ai._ext import get_ext

    DatasetCreator = get_ext("DatasetCreator")

    table_name = args.get("table_name", "").strip()
    description = args.get("description", "")
    data = args.get("data")

    if not table_name:
        return ToolResult(
            success=False,
            error=ToolError(error_type="validation", message="table_name is required."),
        )
    if not data or not isinstance(data, list):
        return ToolResult(
            success=False,
            error=ToolError(
                error_type="validation",
                message="data must be a non-empty list of dicts, each representing a row.",
            ),
        )

    try:
        creator = DatasetCreator(
            user_id=ctx.user_id, organization_id=carried_organization_id(ctx)
        )
        result = await asyncio.to_thread(
            creator.create_table_from_data,
            data,
            table_name,
            description,
        )
        if not result.get("success"):
            return ToolResult(
                success=False,
                error=ToolError(
                    error_type="execution",
                    message=result.get("error", "Unknown error."),
                ),
            )
        return ToolResult(
            success=True,
            output={
                "table_id": str(result.get("table_id", "")),
                "table_name": result.get("table_name", table_name),
                "description": description,
                "row_count": result.get("row_count", len(data)),
                "field_count": result.get("field_count", 0),
                "already_existed": result.get("existing", False),
            },
        )
    except Exception as e:
        return ToolResult(
            success=False,
            error=ToolError(
                error_type="execution", message=str(e), traceback=traceback.format_exc()
            ),
        )


# ---------------------------------------------------------------------------
# usertable_create — simple variant: infer schema from rows of dicts.
# ---------------------------------------------------------------------------


async def usertable_create(args: dict[str, Any], ctx: ToolContext) -> ToolResult:
    from matrx_ai._ext import get_ext

    DatasetCreator = get_ext("DatasetCreator")

    table_name = args.get("table_name", "")
    description = args.get("description", "")
    data = args.get("data")

    if not table_name:
        return ToolResult(
            success=False,
            error=ToolError(error_type="validation", message="table_name is required."),
        )
    if not data or not isinstance(data, list):
        return ToolResult(
            success=False,
            error=ToolError(
                error_type="validation",
                message="data must be a non-empty list of dictionaries, each representing a row.",
            ),
        )

    try:
        creator = DatasetCreator(
            user_id=ctx.user_id, organization_id=carried_organization_id(ctx)
        )
        result = await asyncio.to_thread(
            creator.create_table_from_data,
            data,
            table_name,
            description,
        )
        return ToolResult(
            success=True,
            output={
                "table_id": str(result.get("table_id", "")),
                "table_name": result.get("table_name", table_name),
                "description": description,
                "row_count": result.get("row_count", len(data)),
                "field_count": result.get("field_count", 0),
                "already_existed": result.get("existing", False),
            },
        )
    except Exception as e:
        return ToolResult(
            success=False,
            error=ToolError(
                error_type="execution",
                message=f"Failed to create dataset '{table_name}': {e}",
                traceback=traceback.format_exc(),
            ),
        )


# ---------------------------------------------------------------------------
# dataset — unified action dispatcher
# ---------------------------------------------------------------------------

# Valid `dataset` actions are enforced by the DatasetArgs discriminated union
# (arg_models/dispatcher_args.py) + tool_def.parameters."$variants" — the source of truth.


async def _read_row_data(table_id: str, row_id: str) -> dict[str, Any]:
    """One row's ``data`` from an OLDER table (``datasets_get_row_by_id``)."""
    rows = await asyncio.to_thread(
        _run_query, "datasets_get_row_by_id", {"table_id": table_id, "row_id": row_id}
    )
    if not rows:
        raise LookupError(f"row {row_id} of table {table_id} not found")
    data = rows[0].get("data")
    if isinstance(data, str):
        data = json.loads(data)
    return json.loads(json.dumps(dict(data or {}), default=str))


async def _prior_row_data(table_id: str, row_id: str) -> dict[str, Any] | None:
    """The row's data before ``update_row``, or ``None`` (no receipt).

    A table that moved to the record store has no single-row read on the arm yet;
    reading its archived older copy would show a stale "before", so the receipt
    is skipped there and the skip is logged by name."""
    from matrx_ai.tools.structured_surface_write import read_prior

    async def read() -> dict[str, Any] | None:
        if await _moved(table_id) is not None:
            logger.warning(
                "[dataset] update_row %s/%s: table lives in the record store, which has no "
                "single-row read yet; no before/after receipt",
                table_id,
                row_id,
            )
            return None
        return await _read_row_data(table_id, row_id)

    return await read_prior(read, what=f"dataset row {table_id}/{row_id}")


async def _row_surface_write(
    result: ToolResult, table_id: str, row_id: str, prior: dict[str, Any] | None
) -> ToolResult:
    """Before → after of the row's fields that ``update_row`` (a REPLACE) moved."""
    from matrx_ai.tools.structured_surface_write import read_prior, structured_surface_write

    if not result.success or prior is None:
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

    output: dict[str, Any] = {"dataset_id": dataset_id}

    try:
        arm = await _moved(dataset_id)
        if arm is not None:
            output = await arm.get(
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
            return _self_capped(
                ToolResult(
                    success=True,
                    output=output,
                    started_at=started_at,
                    completed_at=time.time(),
                    tool_name="dataset",
                    call_id=ctx.call_id,
                )
            )
        if include in {"metadata", "all"}:
            meta_rows = await asyncio.to_thread(
                _run_query, "datasets_get_metadata", {"table_id": dataset_id}
            )
            if not meta_rows:
                return ToolResult(
                    success=False,
                    error=ToolError(
                        error_type="not_found",
                        message=f"No dataset found with id '{dataset_id}'.",
                    ),
                    started_at=started_at,
                    completed_at=time.time(),
                    tool_name="dataset",
                    call_id=ctx.call_id,
                )
            r = meta_rows[0]
            output["metadata"] = {
                "dataset_id": str(r.get("id", "")),
                "dataset_name": r.get("table_name", ""),
                "description": r.get("description", ""),
                "version": r.get("version", 1),
                "is_public": r.get("is_public", False),
                "authenticated_read": r.get("authenticated_read", False),
                "row_count": r.get("row_count", 0),
                "created_at": str(r.get("created_at", "")),
                "updated_at": str(r.get("updated_at", "")),
            }

        if include in {"fields", "all"}:
            field_rows = await asyncio.to_thread(
                _run_query, "datasets_get_fields", {"table_id": dataset_id}
            )
            output["fields"] = [
                {
                    "field_id": str(r.get("id", "")),
                    "field_name": r.get("field_name", ""),
                    "display_name": r.get("display_name", ""),
                    "data_type": r.get("data_type", "string"),
                    "field_order": r.get("field_order", 0),
                    "is_required": r.get("is_required", False),
                }
                for r in field_rows
            ]

        if include in {"data", "all"}:
            limit = int(args.get("limit", 50))
            offset = int(args.get("offset", 0))
            sort_by = args.get("sort_by") or None
            sort_order = (args.get("sort_order") or "asc").lower()

            if sort_by:
                query_name = (
                    "datasets_get_rows_sorted_desc"
                    if sort_order == "desc"
                    else "datasets_get_rows_sorted_asc"
                )
                params: dict[str, Any] = {
                    "table_id": dataset_id,
                    "limit": limit,
                    "offset": offset,
                    "sort_field": sort_by,
                }
            else:
                query_name = "datasets_get_rows"
                params = {"table_id": dataset_id, "limit": limit, "offset": offset}

            row_records = await asyncio.to_thread(_run_query, query_name, params)
            raw_rows = [
                {
                    "row_id": str(r.get("id", "")),
                    "data": r.get("data", {}),
                    "created_at": str(r.get("created_at", "")),
                }
                for r in row_records
            ]
            output["rows"], output["cap"] = _bounded_dataset_rows(raw_rows)
            output["count"] = len(raw_rows)
            output["offset"] = offset
            output["limit"] = limit

        return _self_capped(
            ToolResult(
                success=True,
                output=output,
                started_at=started_at,
                completed_at=time.time(),
                tool_name="dataset",
                call_id=ctx.call_id,
            )
        )
    except Exception as e:
        return ToolResult(
            success=False,
            error=ToolError(
                error_type="database", message=str(e), traceback=traceback.format_exc()
            ),
            started_at=started_at,
            completed_at=time.time(),
            tool_name="dataset",
            call_id=ctx.call_id,
        )


async def dataset(args: dict[str, Any], ctx: ToolContext) -> ToolResult:
    started_at = time.time()
    try:
        parsed = DatasetArgs.model_validate(args).root
    except ValidationError as exc:
        return _validation_error(format_args_error(exc), started_at, ctx)
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
        # A dataset belongs to the organization this conversation CARRIES
        # (workbench.udt_datasets.organization_id is NOT NULL). No organization →
        # the one organization hold, before either store is touched. Never
        # defaulted, never the personal organization.
        if not carried_organization_id(ctx):
            return organization_required_result(
                what="create a dataset", tool_name="dataset", ctx=ctx, started_at=started_at
            )
        # BIRTHS (CUTOVER-PLAN Step 2). Once this organization's tables have moved, a new
        # table is born in the record store — otherwise it would be made in a store nobody
        # reads any more. Until then it is made beside the organization's other tables.
        arm = _store_arm()
        if arm is not None:
            try:
                born_there, _why = await arm.born_in_the_store()
                if born_there:
                    table_name = (args.get("dataset_name") or "").strip()
                    data = args.get("data")
                    if not table_name:
                        return _validation_error("table_name is required.", started_at, ctx)
                    if not data or not isinstance(data, list):
                        return _validation_error(
                            "data must be a non-empty list of dicts, each representing a row.",
                            started_at,
                            ctx,
                        )
                    made = await arm.create(
                        name=table_name,
                        description=args.get("description", "") or "",
                        data=data,
                    )
                    return _stamp(ToolResult(success=True, output=made), started_at, ctx)
            except Exception as exc:  # noqa: BLE001 — a refusal or a wait, said as such
                return _stamp(_arm_error(exc), started_at, ctx)
        impl = usertable_create_advanced if args.get("typed") else usertable_create
        return _stamp(
            await impl(
                {
                    "table_name": args.get("dataset_name", ""),
                    "description": args.get("description", ""),
                    "data": args.get("data"),
                },
                ctx,
            ),
            started_at,
            ctx,
        )

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
