from __future__ import annotations

import time
import traceback
from datetime import date, timedelta
from typing import Any

from pydantic import ValidationError

from matrx_ai.tools._dispatch_util import format_args_error
from matrx_ai.tools.arg_models import SeoArgs
from matrx_ai.tools.models import ToolContext, ToolError, ToolResult
from matrx_ai.tools.output_models.seo import (
    SeoKeywordDataOutput,
    normalize_keyword_item,
)


async def seo_check_meta_titles(args: dict[str, Any], ctx: ToolContext) -> ToolResult:
    from matrx_scraper.meta_metrics import calculate_meta_title_metrics

    titles = args.get("titles", [])
    if isinstance(titles, str):
        titles = [titles]
    if not titles:
        return ToolResult(
            success=False,
            error=ToolError(
                error_type="validation",
                message="titles must be a non-empty string or list of strings.",
            ),
        )

    try:
        analysis = []
        for title in titles:
            metrics = calculate_meta_title_metrics(title)
            analysis.append(
                {
                    "title": title,
                    "pixel_width": metrics.get("pixel_width"),
                    "character_count": metrics.get("character_count"),
                    "desktop_ok": metrics.get("desktop_ok"),
                    "mobile_ok": metrics.get("mobile_ok"),
                    "seo_length_ok": metrics.get("seo_length_ok"),
                    "too_short": metrics.get("too_short"),
                    "issues": metrics.get("issues", []),
                    "title_ok": metrics.get("title_ok"),
                }
            )
        return ToolResult(success=True, output={"title_analysis": analysis, "count": len(analysis)})
    except Exception as e:
        return ToolResult(
            success=False,
            error=ToolError(
                error_type="execution", message=str(e), traceback=traceback.format_exc()
            ),
        )


async def seo_check_meta_descriptions(args: dict[str, Any], ctx: ToolContext) -> ToolResult:
    from matrx_scraper.meta_metrics import calculate_meta_description_metrics

    descriptions = args.get("descriptions", [])
    if isinstance(descriptions, str):
        descriptions = [descriptions]
    if not descriptions:
        return ToolResult(
            success=False,
            error=ToolError(
                error_type="validation",
                message="descriptions must be a non-empty string or list of strings.",
            ),
        )

    try:
        analysis = []
        for desc in descriptions:
            metrics = calculate_meta_description_metrics(desc)
            analysis.append(
                {
                    "description": desc,
                    "pixel_width": metrics.get("pixel_width"),
                    "character_count": metrics.get("character_count"),
                    "desktop_ok": metrics.get("desktop_ok"),
                    "mobile_ok": metrics.get("mobile_ok"),
                    "seo_length_ok": metrics.get("seo_length_ok"),
                    "too_short": metrics.get("too_short"),
                    "issues": metrics.get("issues", []),
                    "description_ok": metrics.get("description_ok"),
                }
            )
        return ToolResult(
            success=True,
            output={"description_analysis": analysis, "count": len(analysis)},
        )
    except Exception as e:
        return ToolResult(
            success=False,
            error=ToolError(
                error_type="execution", message=str(e), traceback=traceback.format_exc()
            ),
        )


async def seo_check_meta_tags_batch(args: dict[str, Any], ctx: ToolContext) -> ToolResult:
    from matrx_scraper.meta_metrics import analyze_meta_tags_batch

    meta_data = args.get("meta_data", [])
    if not meta_data or not isinstance(meta_data, list):
        return ToolResult(
            success=False,
            error=ToolError(
                error_type="validation",
                message="meta_data must be a non-empty list of objects with 'title' and/or 'description'.",
            ),
        )

    for idx, item in enumerate(meta_data):
        if not isinstance(item, dict) or ("title" not in item and "description" not in item):
            return ToolResult(
                success=False,
                error=ToolError(
                    error_type="validation",
                    message=f"Item at index {idx} must have at least 'title' or 'description'.",
                ),
            )

    try:
        result = analyze_meta_tags_batch(meta_data)
        return ToolResult(success=True, output={"batch_analysis": result, "count": len(meta_data)})
    except Exception as e:
        return ToolResult(
            success=False,
            error=ToolError(
                error_type="execution", message=str(e), traceback=traceback.format_exc()
            ),
        )


async def seo_get_keyword_data(args: dict[str, Any], ctx: ToolContext) -> ToolResult:
    """Keyword volume/CPC data through the host's SEO vertical service
    (host-injected via the `keyword_research` ext seam — one durable
    collection run per unique request; repeats reuse the persisted run).
    Returns the DataForSEO live response body."""
    from matrx_ai._ext import get_ext
    from matrx_ai.context.app_context import get_app_context

    keyword_research = get_ext("keyword_research")

    keywords = args.get("keywords", [])
    date_from_str = args.get("date_from", "")
    date_to_str = args.get("date_to", "")
    location_code = args.get("location_code", 2840)
    language_code = args.get("language_code", "en")
    search_partners = args.get("search_partners", True)
    sort_by = args.get("sort_by", "search_volume")

    if not keywords or not isinstance(keywords, list):
        return ToolResult(
            success=False,
            error=ToolError(
                error_type="validation",
                message="keywords must be a non-empty list of strings.",
            ),
        )
    if not date_from_str or not date_to_str:
        return ToolResult(
            success=False,
            error=ToolError(
                error_type="validation",
                message="date_from and date_to are required (YYYY-MM-DD).",
            ),
        )

    try:
        d_from = date.fromisoformat(date_from_str.strip())
        d_to = date.fromisoformat(date_to_str.strip())
    except ValueError:
        return ToolResult(
            success=False,
            error=ToolError(
                error_type="validation",
                message="date_from and date_to must be valid dates in YYYY-MM-DD format.",
            ),
        )

    today = date.today()
    if d_from > today or d_to > today:
        return ToolResult(
            success=False,
            error=ToolError(
                error_type="validation",
                message="date_from and date_to must be in the past. Google Ads does not return data for future dates.",
                suggested_action="Use past dates only, e.g. date_from='2024-01-01', date_to='2024-12-31'.",
            ),
        )
    if d_from > d_to:
        return ToolResult(
            success=False,
            error=ToolError(
                error_type="validation",
                message="date_from must be before or equal to date_to.",
                suggested_action="Ensure date_from is the start of the range and date_to is the end, e.g. date_from='2024-01-01', date_to='2024-12-31'.",
            ),
        )
    four_years_ago = today - timedelta(days=4 * 365)
    if d_from < four_years_ago:
        return ToolResult(
            success=False,
            error=ToolError(
                error_type="validation",
                message=f"date_from cannot be older than 4 years. Minimum allowed: {four_years_ago.isoformat()}.",
                suggested_action=f"Use date_from >= {four_years_ago.isoformat()}.",
            ),
        )

    date_from = date_from_str.strip()
    date_to = date_to_str.strip()

    try:
        data = await keyword_research(
            user_id=ctx.user_id,
            organization_id=get_app_context().organization_id,
            keywords=keywords,
            date_from=date_from,
            date_to=date_to,
            location_code=location_code,
            language_code=language_code,
            search_partners=search_partners,
            sort_by=sort_by,
        )

        tasks = data.get("tasks", [])
        if not tasks or tasks[0].get("status_code") != 20000:
            return ToolResult(
                success=False,
                error=ToolError(
                    error_type="api_error",
                    message=f"DataForSEO API error: {tasks[0].get('status_message', 'Unknown') if tasks else 'No tasks returned'}",
                ),
            )

        result_data = tasks[0].get("result", []) or []
        keywords_data = [
            normalize_keyword_item(item) for item in result_data if isinstance(item, dict)
        ]
        output = SeoKeywordDataOutput(
            keywords_data=keywords_data,
            total_keywords=len(keywords),
            date_range={"from": date_from, "to": date_to},
            search_parameters={
                "location_code": location_code,
                "language_code": language_code,
            },
        )
        return ToolResult(success=True, output=output.model_dump())
    except Exception as e:
        return ToolResult(
            success=False,
            error=ToolError(
                error_type="execution", message=str(e), traceback=traceback.format_exc()
            ),
        )


async def seo_collect_rank(args: dict[str, Any], ctx: ToolContext) -> ToolResult:
    """Durable SERP-rank collection through the host's SEO vertical service
    (host-injected via the `seo_collect_rank` ext seam — the receipt is the
    persisted seo.* collection run)."""
    from matrx_ai._ext import get_ext
    from matrx_ai.context.app_context import get_app_context

    runner = get_ext("seo_collect_rank")
    try:
        receipt = await runner(
            user_id=ctx.user_id,
            organization_id=get_app_context().organization_id,
            provider=args["provider"],
            keyword=args["keyword"],
            target_domain=args.get("target_domain"),
            country=args.get("country", "US"),
            language=args.get("language", "en"),
            device=args.get("device", "desktop"),
            location=args.get("location"),
            host_site_id=args.get("site_id"),
            search_type=args.get("search_type", "organic"),
            engine=args.get("engine"),
        )
    except ValueError as e:
        return ToolResult(
            success=False,
            error=ToolError.from_exception(e, error_type="validation", message=str(e)),
        )
    except Exception as e:
        return ToolResult(
            success=False,
            error=ToolError.from_exception(e, error_type="execution", message=str(e)),
        )
    return ToolResult(success=True, output={"receipt": receipt})


# ---------------------------------------------------------------------------
# seo — unified action dispatcher
# ---------------------------------------------------------------------------

# Valid `seo` actions are enforced by the SeoArgs discriminated union
# (arg_models/dispatcher_args.py) + tool_def.parameters."$variants" — the source of truth.


def _seo_stamp(result: ToolResult, started_at: float, ctx: ToolContext) -> ToolResult:
    result.tool_name = "seo"
    result.call_id = ctx.call_id
    if not result.started_at:
        result.started_at = started_at
    if not result.completed_at:
        result.completed_at = time.time()
    return result


def _seo_validation_error(message: str, started_at: float, ctx: ToolContext) -> ToolResult:
    return ToolResult(
        success=False,
        error=ToolError(error_type="validation", message=message),
        started_at=started_at,
        completed_at=time.time(),
        tool_name="seo",
        call_id=ctx.call_id,
    )


async def seo(args: dict[str, Any], ctx: ToolContext) -> ToolResult:
    started_at = time.time()
    try:
        parsed = SeoArgs.model_validate(args).root
    except ValidationError as exc:
        return _seo_validation_error(format_args_error(exc), started_at, ctx)

    action = parsed.action
    inner_args = parsed.model_dump(exclude={"action"}, exclude_unset=True)
    impl = {
        "check_titles": seo_check_meta_titles,
        "check_descriptions": seo_check_meta_descriptions,
        "check_batch": seo_check_meta_tags_batch,
        "keyword_data": seo_get_keyword_data,
        "collect_rank": seo_collect_rank,
    }[action]

    return _seo_stamp(await impl(inner_args, ctx), started_at, ctx)
