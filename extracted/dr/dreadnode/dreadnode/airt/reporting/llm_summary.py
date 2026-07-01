"""Optional LLM-generated executive summary.

Falls back to a deterministic template when no LLM is available (e.g.
air-gapped environments).  The LLM receives only pre-computed metrics --
it adds narrative, not new analysis.
"""

from __future__ import annotations

from loguru import logger

from dreadnode.airt.analytics.types import CampaignAnalytics, Severity


def _template_summary(analytics: CampaignAnalytics) -> str:
    """Deterministic executive summary from computed metrics."""
    stats = analytics.execution_stats
    sev = analytics.severity_breakdown
    n_critical = sev.get(Severity.CRITICAL, 0)
    n_high = sev.get(Severity.HIGH, 0)

    parts: list[str] = []

    # Overall posture
    if stats.overall_asr >= 0.7:
        parts.append(
            f"The target model exhibits significant vulnerability to adversarial attacks "
            f"with an overall Attack Success Rate of {stats.overall_asr:.0%}."
        )
    elif stats.overall_asr >= 0.3:
        parts.append(
            f"The target model shows moderate resilience with an overall Attack Success Rate "
            f"of {stats.overall_asr:.0%}."
        )
    else:
        parts.append(
            f"The target model demonstrates strong resilience with an overall Attack Success Rate "
            f"of {stats.overall_asr:.0%}."
        )

    # Critical / high counts
    if n_critical:
        parts.append(
            f"{n_critical} critical-severity finding{'s' if n_critical != 1 else ''} "
            f"require{'s' if n_critical == 1 else ''} immediate attention."
        )
    if n_high:
        parts.append(
            f"{n_high} high-severity finding{'s' if n_high != 1 else ''} "
            f"should be prioritised for remediation."
        )

    # Top finding detail
    if analytics.top_findings:
        top = analytics.top_findings[0]
        parts.append(
            f"The most impactful finding is a {top.severity.value}-severity "
            f"{top.goal_category.value.replace('_', ' ')} attack "
            f"({top.attack_name}) achieving a score of {top.score:.2f}."
        )

    # Transform insight
    transform_entries = analytics.asr_by_transform.entries
    if "baseline" in transform_entries and len(transform_entries) > 1:
        baseline_asr = transform_entries["baseline"].asr
        best_transform = max(
            ((k, v) for k, v in transform_entries.items() if k != "baseline"),
            key=lambda kv: kv[1].asr,
            default=None,
        )
        if best_transform and best_transform[1].asr > baseline_asr:
            lift = best_transform[1].asr - baseline_asr
            parts.append(
                f"The most effective transform is '{best_transform[0]}' "
                f"with a {lift:.0%} ASR lift over baseline."
            )

    # Coverage
    matrix = analytics.compliance_matrix
    tested_owasp = sum(1 for e in matrix.owasp_llm.values() if e.tested)
    total_owasp = len(matrix.owasp_llm)
    if total_owasp:
        parts.append(f"OWASP LLM Top 10 coverage: {tested_owasp}/{total_owasp} categories tested.")

    # Recommendations count
    if analytics.recommendations:
        parts.append(
            f"{len(analytics.recommendations)} recommendation{'s' if len(analytics.recommendations) != 1 else ''} "
            f"generated across {len({r.category for r in analytics.recommendations})} "
            f"finding categor{'ies' if len({r.category for r in analytics.recommendations}) != 1 else 'y'}."
        )

    parts.append(
        f"Campaign executed {stats.total_attacks} attack{'s' if stats.total_attacks != 1 else ''} "
        f"with {stats.total_trials} total trials in {stats.total_execution_time_s:.1f}s."
    )

    return " ".join(parts)


def _build_llm_prompt(analytics: CampaignAnalytics) -> str:
    """Build the prompt sent to the LLM for narrative generation."""
    stats = analytics.execution_stats
    sev = analytics.severity_breakdown

    findings_text = ""
    for f in analytics.top_findings[:5]:
        findings_text += (
            f"- [{f.severity.value.upper()}] {f.attack_name} targeting "
            f"{f.goal_category.value}: score {f.score:.2f}\n"
        )

    recs_text = ""
    for r in analytics.recommendations[:5]:
        recs_text += f"- [{r.severity.value.upper()}] {r.title}\n"

    return f"""You are a security analyst writing an executive summary for an AI red team campaign report.

METRICS (all pre-computed, do not recalculate):
- Overall ASR: {stats.overall_asr:.1%}
- Total trials: {stats.total_trials}
- Successful: {stats.successful_attacks}
- Severity breakdown: critical={sev.get(Severity.CRITICAL, 0)}, high={sev.get(Severity.HIGH, 0)}, medium={sev.get(Severity.MEDIUM, 0)}, low={sev.get(Severity.LOW, 0)}, info={sev.get(Severity.INFO, 0)}

TOP FINDINGS:
{findings_text}
RECOMMENDATIONS:
{recs_text}
Write a 3-5 sentence executive summary for a security team. Be direct and specific about risks. Reference the actual numbers. Do not add metrics beyond what is provided."""


async def generate_executive_summary(
    analytics: CampaignAnalytics,
    *,
    generator: object | None = None,
) -> str:
    """Generate an executive summary.

    If *generator* is provided and has a ``generate`` method, produces an
    LLM-enhanced narrative.  Otherwise returns the deterministic template.

    Args:
        analytics: Populated campaign analytics.
        generator: Optional LLM generator instance with an async
            ``generate(prompt: str) -> str`` method.

    Returns:
        Executive summary text.
    """
    if generator is not None and hasattr(generator, "generate"):
        prompt = _build_llm_prompt(analytics)
        try:
            result = await generator.generate(prompt)  # ty: ignore[call-non-callable]
            if isinstance(result, str) and result.strip():
                return result.strip()
        except Exception:
            logger.debug("LLM executive summary generation failed, using template")

    return _template_summary(analytics)
