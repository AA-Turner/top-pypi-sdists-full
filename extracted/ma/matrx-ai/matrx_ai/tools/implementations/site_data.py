"""``site_data`` tool — structured records for covered sites, via matrx-scraper's site-data door.

The model passes ``url`` (any covered page) or ``site`` + ``query``/``location``/``inputs``
(a discover mode such as an Indeed job search). The door lives in
``matrx_scraper.features.site_data``; cost recording and the spend gate are the
host's (aidream wires the Bright Data client, observer and guard).
"""

from __future__ import annotations

import json
import time
from typing import Any

from matrx_ai.tools.arg_models.web_args import SiteDataArgs
from matrx_ai.tools.implementations._dataset_door import is_chat_door, slower_dataset_line
from matrx_ai.tools.implementations._web_read_caps import RESULT_BUDGET_CHARS
from matrx_ai.tools.kinds.data_fetch import DataFetchNotStarted
from matrx_ai.tools.models import ToolContext, ToolError, ToolResult
from matrx_ai.tools.streaming import ToolStreamManager

_RENDER_CHARS = 16_000

_POINTS_LIMIT_MESSAGE = "You've used all your points for now. Upgrade your plan to keep going."

_REMEDY = {
    "usage_limit": "Do not retry. Tell the user their points are used up and a plan upgrade would unlock more.",
    "unavailable": "Use web with action='read' on the page URL instead.",
    "not_configured": "Use web with action='read' on the page URL instead.",
    "no_match": "Use web with action='read' for this URL, or pass one of the listed site keys.",
    "input_error": "Call site_data again with the named fields in inputs (or query/location).",
    "timeout": "Call site_data again later with fewer inputs or a smaller max_records.",
    "error": "Use web with action='read' on the page URL instead.",
}


def _fail(status: str, message: str, ctx: ToolContext, started_at: float) -> ToolResult:
    return ToolResult(
        success=False,
        error=ToolError(
            error_type="validation" if status in ("input_error", "no_match") else "execution",
            message=message,
            is_retryable=status in ("timeout", "error"),
            suggested_action=_REMEDY.get(status),
        ),
        started_at=started_at,
        completed_at=time.time(),
        tool_name="site_data",
        call_id=ctx.call_id,
    )


def _fit_records(output: dict[str, Any], budget: int) -> dict[str, Any]:
    """Drop records from the tail until the serialized result fits; say how many remain."""
    records = output["records"]
    total = len(records)
    while records and len(json.dumps(output, default=str)) > budget:
        records.pop()
    if len(records) < total:
        output["records_included"] = len(records)
        output["records_note"] = (
            f"{total - len(records)} of {total} records were left out of `records` to fit the result "
            "size; every record is summarized in `rendering` up to its own limit."
        )
    return output


async def site_data(args: dict[str, Any], ctx: ToolContext) -> ToolResult:
    started_at = time.time()
    parsed = SiteDataArgs.model_validate(args)
    if not parsed.url and not parsed.site:
        return _fail("input_error", "Pass url, or site with query/location/inputs.", ctx, started_at)
    from matrx_scraper.features import site_data as door
    from matrx_scraper.vendors.brightdata import BrightDataRecorderMissing, current_limits

    # Chat never starts a slow dataset (owner ruling 2026-10-16): one line back, nothing fetched or billed.
    if is_chat_door(unknown_is_chat=True):
        model = DataFetchNotStarted
        legacy_output = {"status": "not_started", "message": slower_dataset_line(parsed.site or parsed.url)}
        typed_output = model.model_validate({"__kind": model.kind_slug, **legacy_output})
        return ToolResult(
            success=True,
            output=typed_output.model_dump(mode="json", by_alias=True, exclude_unset=True),
            output_kind=model.kind_slug,
            started_at=started_at, completed_at=time.time(), tool_name="site_data", call_id=ctx.call_id,
        )

    # The ceiling is the host's limit (aidream: the knob the data-sources screen also obeys);
    # checked here first so the agent gets a typed answer. The client enforces it again.
    limits = await current_limits()
    n_inputs = len(parsed.inputs) if parsed.inputs else 1
    if n_inputs > limits.max_inputs or n_inputs * parsed.max_records > limits.max_total_records:
        return _fail(
            "input_error",
            f"{n_inputs} inputs x max_records={parsed.max_records} could return {n_inputs * parsed.max_records} "
            f"records; the limit is {limits.max_inputs} inputs and {limits.max_total_records} records in total "
            "per call. Send fewer inputs or a smaller max_records.",
            ctx, started_at,
        )

    stream = ToolStreamManager(ctx.emitter, ctx.call_id, "site_data")
    await stream.progress(f"Fetching site data: {parsed.site or parsed.url}"[:80])
    try:
        if parsed.save_to_table:
            # The host's writer (aidream: data_fetch.run_fetch) owns the job, the meter, the limits and the
            # table write; this package only resolves the source and renders the records.
            async def _progress(label: str) -> None:
                await stream.progress(label[:80])

            res = await door.fetch_to_table(
                url=parsed.url, site=parsed.site, query=parsed.query, location=parsed.location,
                inputs=parsed.inputs, max_records=parsed.max_records, table_id=parsed.table_id,
                table_name=parsed.table_name, progress=_progress, render_chars=_RENDER_CHARS,
            )
        else:
            res = await door.fetch(
                url=parsed.url,
                site=parsed.site,
                query=parsed.query,
                location=parsed.location,
                inputs=parsed.inputs,
                max_records=parsed.max_records,
                render_chars=_RENDER_CHARS,
            )
    except BrightDataRecorderMissing:
        return _fail("unavailable", "Site data is unavailable on this server right now (its cost "
                     "recording is not set up), so nothing was fetched or billed.", ctx, started_at)
    except Exception as exc:  # noqa: BLE001 - only spend-gate refusals are typed here; the rest is a real error
        if not getattr(exc, "is_caller_refusal", False):
            raise
        if "UsageLimit" in type(exc).__name__:
            return _fail("usage_limit", _POINTS_LIMIT_MESSAGE, ctx, started_at)
        return _fail("unavailable", str(exc) or "Site data was refused by a platform guard.", ctx, started_at)
    if res.status == "no_match":
        known = ", ".join(f"{s['key']} ({s['label']})" for s in door.covered_sites())
        return _fail("no_match", f"{res.message} Covered sites: {known}.", ctx, started_at)
    if res.status not in ("success", "empty"):
        return _fail(res.status, res.message, ctx, started_at)
    if parsed.save_to_table and res.status == "empty":
        return _fail("error", res.message or "No records came back, so no table was written.", ctx, started_at)

    saved = (
        {k: res.table.get(k) for k in ("table_id", "table_name", "rows_created", "rows_updated", "records_billed")}
        if res.table else {}
    )
    output = _fit_records(
        {
            **saved,
            "status": res.status,
            "message": res.message,
            "site": res.entry_key,
            "label": res.label,
            "record_count": len(res.records),
            "rendering": res.rendering,
            "rendering_truncated": res.rendering_truncated,
            "records": list(res.records),
            "provenance": res.provenance,
        },
        RESULT_BUDGET_CHARS,
    )
    return ToolResult(
        success=True,
        output=output,
        started_at=started_at,
        completed_at=time.time(),
        tool_name="site_data",
        call_id=ctx.call_id,
        output_self_capped=True,
    )
