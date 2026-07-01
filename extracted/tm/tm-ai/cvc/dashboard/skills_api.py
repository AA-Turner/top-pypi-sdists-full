"""
cvc.dashboard.skills_api — REST surface for the CVC skill substrate.

Exposes aggregate insights over the same ``.usage.json`` sidecar that
``cvc skills`` reads. The CLI command and the dashboard hit the *same*
pure engine (``cvc.skills.insights.compute_insights``), so what users
see in the terminal is identical to what they see in the React UI.

Endpoints
---------
    GET /api/skills/insights
        Aggregate report — hot / fading / dead / fresh buckets, plus
        aggregate counters (total views, uses, patches, wasted-context
        share, agent-created vs bundled/hub split).

    GET /api/skills/insights/summary
        One-line summary — for the dashboard header chip and the bot
        status command. Cheap to poll.

Mounted by gateway.py via ``app.include_router(_skills_router)``.
"""

from __future__ import annotations

import logging
from typing import Any, Dict

from fastapi import APIRouter

from cvc.skills.insights import compute_insights, to_jsonable
from cvc.skills.usage import load_usage

__all__ = ["register_skills_routes"]

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/skills", tags=["skills"])


def register_skills_routes(app) -> None:
    """Mount the skills router on the given FastAPI ``app``."""
    app.include_router(router)
    logger.debug("Mounted /api/skills router (insights + summary)")


@router.get("/insights")
def get_skill_insights() -> Dict[str, Any]:
    """Return the full :class:`SkillInsightsReport` as JSON."""
    usage = load_usage()
    report = compute_insights(usage)
    return to_jsonable(report)


@router.get("/insights/summary")
def get_skill_insights_summary() -> Dict[str, Any]:
    """Return just the one-liner + a few counters for header chips."""
    usage = load_usage()
    report = compute_insights(usage)
    return {
        "generated_at": report.generated_at,
        "summary": report.summary_one_liner,
        "total_skills": report.total_skills,
        "active_count": report.active_count,
        "hot_count": len(report.hot),
        "fading_count": len(report.fading),
        "dead_count": len(report.dead),
        "wasted_context_share": report.wasted_context_share,
        "agent_created_count": report.agent_created_count,
        "total_views": report.total_views,
        "total_uses": report.total_uses,
    }
