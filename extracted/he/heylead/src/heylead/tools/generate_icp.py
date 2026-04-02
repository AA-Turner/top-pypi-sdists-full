"""Tool: generate_icp — Create a rich Ideal Customer Profile.

Generates 2-4 ICP personas with pain points, fears, barriers,
LinkedIn search parameters (include/exclude), and confidence scores.
Persists the result for reuse with create_campaign.
"""

from __future__ import annotations

import json
import logging
from typing import Any

from ..ai.icp_generator_v2 import generate_icp_v2
from ..ai.icp_schemas import IcpResult, SingleIcp, icp_result_from_dict, icp_result_to_json
from ..config import get_tier, is_backend_mode
from ..constants import (
    FREE_MAX_ICP_V2_GENERATIONS,
    TIER_PRO,
)
from ..db.queries import (
    get_monthly_usage,
    get_setting,
    increment_usage,
    list_icps,
    save_icp,
)
from ..formatter import stars
from ..db.async_bridge import run_db

logger = logging.getLogger(__name__)


async def _enrich_result_if_needed(result: IcpResult) -> None:
    """Enrich ICPs with LinkedIn parameter codes if not already enriched.

    Checks whether any ICP already has enriched params; if not, resolves
    human-readable values (e.g., "Financial Services") to LinkedIn codes
    via the Unipile search/parameters API.
    """
    if not result.icps:
        return

    # Skip if already enriched
    already_enriched = any(
        icp.linkedin_enriched_params
        and (
            (icp.linkedin_enriched_params.industries and icp.linkedin_enriched_params.industries.include)
            or (icp.linkedin_enriched_params.locations and icp.linkedin_enriched_params.locations.include)
            or (icp.linkedin_enriched_params.job_titles and icp.linkedin_enriched_params.job_titles.include)
        )
        for icp in result.icps
    )
    if already_enriched:
        logger.info("ICPs already have enriched LinkedIn codes — skipping enrichment")
        return

    # Delegate to the shared enrichment function in icp_generator_v2
    from ..ai.icp_generator_v2 import _enrich_result
    await _enrich_result(result)


async def generate_icp_result_for_campaign(
    target_description: str,
    company_context: str = "",
    focus_query: str = "",
    user_context: dict[str, Any] | None = None,
) -> IcpResult:
    """Generate an ICP (IcpResult) for use in campaign creation. No persist, no formatting.

    Shared logic for run_generate_icp and create_campaign when generating ICP inline.
    """
    ctx = user_context or {}
    use_pipeline = bool(
        company_context
        and (company_context.strip().startswith("http") or len(company_context) > 200)
    )
    if use_pipeline and is_backend_mode():
        from ..linkedin import get_linkedin_client
        from ..linkedin.backend_client import BackendClient
        client = get_linkedin_client()
        if isinstance(client, BackendClient):
            raw = await client.generate_icp_rag(
                target_description=target_description,
                company_context=company_context,
                focus_query=focus_query,
                user_context=ctx,
            )
            result = icp_result_from_dict(raw)
            # Enrich with LinkedIn codes (backend RAG may not have enriched)
            await _enrich_result_if_needed(result)
            return result
        from ..ai.icp_pipeline import run_icp_pipeline
        return await run_icp_pipeline(
            target_description=target_description,
            company_context=company_context,
            focus_query=focus_query,
            user_profile=ctx,
        )
    if use_pipeline:
        from ..ai.icp_pipeline import run_icp_pipeline
        return await run_icp_pipeline(
            target_description=target_description,
            company_context=company_context,
            focus_query=focus_query,
            user_profile=ctx,
        )
    # generate_icp_v2 includes enrichment internally
    return await generate_icp_v2(
        target_description=target_description,
        company_context=company_context,
        focus_query=focus_query,
        user_profile=ctx,
    )


async def run_generate_icp(
    target_description: str,
    company_context: str = "",
    focus_query: str = "",
) -> str:
    """Generate a rich ICP and persist it.

    Flow:
    1. Check setup is complete
    2. Check free tier ICP generation limit
    3. Generate ICP via LLM (Phase 1: prompt-only; Phase 4: RAG)
    4. Persist to DB
    5. Format output
    """

    # ── Step 0: Check setup ──
    setup_done = await run_db(get_setting, "setup_complete", False)
    if not setup_done:
        return (
            "Setup required before generating ICPs.\n\n"
            "Please run setup_profile first — it connects your LinkedIn account and "
            "analyzes your writing style so messages sound like you.\n\n"
            "If you haven't started setup yet, say 'set up my profile' and I'll walk "
            "you through it step by step (takes about 2 minutes)."
        )

    # ── Step 1: Free tier limits ──
    tier = get_tier()
    if tier != TIER_PRO:
        usage = await run_db(get_monthly_usage)
        if usage.get("icps_generated", 0) >= FREE_MAX_ICP_V2_GENERATIONS:
            return (
                f"Free tier limit: {FREE_MAX_ICP_V2_GENERATIONS} ICP generations per month.\n\n"
                "Options:\n"
                "  Use create_campaign instead (includes basic ICP generation)\n"
                "  Wait until next month\n"
                "  Upgrade to Pro ($29/mo) for unlimited ICPs"
            )

    # ── Step 2: Get user context ──
    profile = await run_db(get_setting, "profile", {})
    expertise = await run_db(get_setting, "expertise_map", {})
    user_context = {**profile, **expertise}

    # ── Step 3: Generate ICP ──
    try:
        result = await generate_icp_result_for_campaign(
            target_description=target_description,
            company_context=company_context,
            focus_query=focus_query,
            user_context=user_context,
        )
    except Exception as e:
        logger.error(f"ICP generation failed: {e}", exc_info=True)
        return (
            f"ICP generation failed: {e}\n\n"
            "Check your LLM API key configuration."
        )

    if not result.icps:
        return (
            "Could not generate any ICPs meeting the confidence threshold.\n\n"
            f"Searched for: \"{target_description}\"\n"
            "Try a more specific or different target description."
        )

    # ── Step 4: Persist to DB ──
    best_confidence = max(icp.overall_confidence for icp in result.icps)
    icp_id = await run_db(save_icp, name=result.campaign_name or target_description[:40],
        icp_json=icp_result_to_json(result),
        target_desc=target_description,
        source_url=company_context if company_context.startswith("http") else "",
        confidence=best_confidence,)

    # Track usage
    await run_db(increment_usage, "icps_generated")

    # ── Step 5: Auto-create signal watchlists from ICP keywords ──
    watchlist_info = ""
    try:
        from ..services.signal_service import create_watchlists_from_icp
        icp_json_str = icp_result_to_json(result)
        wl_ids = create_watchlists_from_icp(
            icp_json=icp_json_str,
            icp_name=result.campaign_name or target_description[:40],
        )
        if wl_ids:
            watchlist_info = f"\n\nSignal monitoring: Created {len(wl_ids)} watchlist(s) from ICP keywords. The scheduler will monitor LinkedIn posts for these terms."
    except Exception as e:
        logger.debug("Auto-watchlist creation failed: %s", e)

    # ── Step 6: Format output ──
    output = _format_icp_output(result, icp_id, target_description)
    if watchlist_info:
        output += watchlist_info
    return output


def _format_icp_output(
    result: IcpResult, icp_id: str, target_description: str,
) -> str:
    """Format the ICP result for MCP tool output."""
    lines = [
        f"ICP Generated: **{result.campaign_name or target_description[:40]}**",
        f"ICP ID: `{icp_id[:8]}...`",
        "",
    ]

    if result.summary:
        lines.append(f"Summary: {result.summary}")
    if result.relevance_hook:
        lines.append(f"Relevance: {result.relevance_hook}")

    # Show source info if RAG was used
    src = result.source_info
    if src.get("evidence_count"):
        lines.append(
            f"Evidence: {src['evidence_count']} snippets from "
            f"{src.get('chunks_ingested', 0)} chunks"
        )

    lines.append(f"Processing time: {result.processing_time:.1f}s")
    lines.append("")

    for i, icp in enumerate(result.icps, 1):
        lines.extend(_format_single_icp(i, icp))
        lines.append("")

    lines.extend([
        "---",
        "Next steps:",
        f"  create_campaign(icp_id=\"{icp_id[:8]}...\") to find prospects using this ICP",
        "  generate_icp with different target to compare segments",
        "  show_status() to see all saved ICPs",
    ])

    return "\n".join(lines)


def _format_single_icp(index: int, icp: SingleIcp) -> list[str]:
    """Format a single ICP persona for display."""
    conf = stars(icp.overall_confidence)
    lines = [
        f"### Persona {index}: {icp.name} ({conf} {icp.overall_confidence:.0%})",
    ]

    if icp.description:
        lines.append(f"  {icp.description}")
        lines.append("")

    # Pain points
    if icp.pain_points:
        lines.append("  Pain points:")
        for pp in icp.pain_points:
            lines.append(f"    - {pp}")

    # Fears
    if icp.fears:
        lines.append("  Fears:")
        for f in icp.fears:
            lines.append(f"    - {f}")

    # Barriers
    if icp.barriers:
        lines.append("  Barriers:")
        for b in icp.barriers:
            lines.append(f"    - {b}")

    lines.append("")

    # LinkedIn parameters
    lines.append("  LinkedIn targeting:")
    _add_param(lines, "Industries", icp.industries)
    _add_param(lines, "Job titles", icp.job_titles)
    _add_param(lines, "Locations", icp.locations)
    _add_param(lines, "Seniority", icp.seniority)

    if icp.departments and icp.departments.include:
        _add_param(lines, "Departments", icp.departments)

    if icp.company_headcount.min or icp.company_headcount.max:
        hc = icp.company_headcount
        range_str = f"{hc.min or '?'}-{hc.max or '?'} employees"
        lines.append(f"    Company size: {range_str}")

    if icp.company_types:
        lines.append(f"    Company types: {', '.join(icp.company_types)}")

    if icp.tenure.min or icp.tenure.max:
        t = icp.tenure
        lines.append(f"    Tenure: {t.min or 0}-{t.max or '?'} years")

    if icp.keywords:
        lines.append(f"    Keywords: {', '.join(icp.keywords)}")

    # Enriched LinkedIn codes (if available)
    if icp.linkedin_enriched_params:
        ep = icp.linkedin_enriched_params
        has_enriched = any([
            ep.industries and ep.industries.include,
            ep.job_titles and ep.job_titles.include,
            ep.locations and ep.locations.include,
            ep.departments and ep.departments.include,
        ])
        if has_enriched:
            lines.append("")
            lines.append("  Enriched LinkedIn codes:")
            _add_enriched(lines, "Industries", ep.industries)
            _add_enriched(lines, "Job titles", ep.job_titles)
            _add_enriched(lines, "Locations", ep.locations)
            _add_enriched(lines, "Departments", ep.departments)

    # Evidence citations (if available)
    if icp.field_evidence:
        cited_fields = [fe for fe in icp.field_evidence if fe.citations]
        if cited_fields:
            lines.append("")
            lines.append("  Evidence:")
            for fe in cited_fields[:4]:  # Show top 4 cited fields
                for cit in fe.citations[:1]:  # One citation per field
                    source = cit.source_url or "source"
                    lines.append(
                        f"    {fe.field_name}: \"{cit.snippet[:80]}...\" "
                        f"({source}, {cit.confidence:.0%})"
                    )

    # Confidence breakdown
    lines.append("")
    lines.append(
        f"  Confidence: overall={icp.overall_confidence:.0%} "
        f"completeness={icp.data_completeness:.0%} "
        f"evidence={icp.evidence_strength:.0%}"
    )

    return lines


def _add_param(lines: list[str], label: str, param: Any) -> None:
    """Add an include/exclude LinkedIn parameter to output lines."""
    if param is None:
        return
    include = getattr(param, "include", []) or []
    exclude = getattr(param, "exclude", []) or []

    if include:
        lines.append(f"    {label}: {', '.join(include)}")
    if exclude:
        lines.append(f"    {label} (exclude): {', '.join(exclude)}")


def _add_enriched(lines: list[str], label: str, field: Any) -> None:
    """Add enriched LinkedIn codes to output lines."""
    if field is None:
        return
    include = getattr(field, "include", []) or []
    if include:
        codes = [f"{p.name} ({p.code})" for p in include if p.name and p.code]
        if codes:
            lines.append(f"    {label}: {', '.join(codes)}")
