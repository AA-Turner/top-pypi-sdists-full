"""Datasets tool implementations.

Provides full CRUD access to a user's structured datasets
(stored in workbench.udt_datasets / workbench.udt_dataset_fields / workbench.udt_dataset_rows).

A "dataset" here is a user-owned tabular data store created by the AI on
behalf of the user. All operations are scoped to ctx.user_id automatically.

The exposed tool names retain the ``usertable_*`` prefix so existing agent
definitions and the persisted tools registry keep working unchanged.
"""

from __future__ import annotations

import asyncio
import json
import time
import traceback
from typing import Any

from pydantic import ValidationError

from matrx_ai.tools._dispatch_util import format_args_error
from matrx_ai.tools.arg_models import DatasetArgs
from matrx_ai.tools.models import ToolContext, ToolError, ToolResult

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
        from matrx_ai.db._registry import get_model as get_db_model

        UdtDatasetRows = get_db_model("UdtDatasetRows")
        deleted_count = await UdtDatasetRows.delete_where(
            id=row_id, table_id=table_id, user_id=ctx.user_id
        )
        if not deleted_count:
            return ToolResult(
                success=False,
                error=ToolError(
                    error_type="not_found",
                    message=f"Row '{row_id}' not found or you do not own it.",
                ),
            )
        return ToolResult(success=True, output={"deleted_row_id": row_id})
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
        creator = DatasetCreator(user_id=ctx.user_id)
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
        creator = DatasetCreator(user_id=ctx.user_id)
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
        return _stamp(
            await usertable_update_row(
                {
                    "table_id": args.get("dataset_id", ""),
                    "row_id": args.get("row_id", ""),
                    "data": args.get("data"),
                },
                ctx,
            ),
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
