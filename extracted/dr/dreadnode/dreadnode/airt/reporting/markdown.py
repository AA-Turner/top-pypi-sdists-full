"""Markdown report generator.

Renders a :class:`CampaignAnalytics` instance into a structured Markdown
document suitable for human review or conversion to HTML/PDF.
"""

from __future__ import annotations

from datetime import UTC, datetime

from dreadnode.airt.analytics.types import (
    ASRBreakdown,
    CampaignAnalytics,
    ComplianceEntry,
    Finding,
    Severity,
)


def _severity_badge(severity: Severity) -> str:
    return f"**{severity.value.upper()}**"


def _pct(value: float) -> str:
    return f"{value * 100:.1f}%"


def _fmt_score(value: float) -> str:
    return f"{value:.3f}"


def _truncate(text: str, max_len: int = 500) -> str:
    if len(text) <= max_len:
        return text
    return text[:max_len] + "..."


# ---------------------------------------------------------------------------
# Section renderers
# ---------------------------------------------------------------------------


def _render_header(analytics: CampaignAnalytics) -> str:
    now = datetime.now(tz=UTC).strftime("%Y-%m-%d %H:%M:%S UTC")
    stats = analytics.execution_stats
    return (
        "# AIRT Campaign Report\n\n"
        f"Generated: {now}\n\n"
        f"| Metric | Value |\n"
        f"|--------|-------|\n"
        f"| Risk Score | **{analytics.risk_score:.1f}/10** |\n"
        f"| Overall ASR | {_pct(stats.overall_asr)} |\n"
        f"| Total Attacks | {stats.total_attacks} |\n"
        f"| Successful Attacks | {stats.successful_attacks} |\n"
        f"| Total Trials | {stats.total_trials} |\n"
        f"| Execution Time | {stats.total_execution_time_s:.1f}s |\n"
        f"| Avg Trial Time | {stats.avg_trial_time_ms:.0f}ms |\n"
    )


def _render_severity_breakdown(analytics: CampaignAnalytics) -> str:
    lines = ["## Severity Breakdown\n", "| Severity | Count |", "|----------|-------|"]
    for sev in Severity:
        count = analytics.severity_breakdown.get(sev, 0)
        lines.append(f"| {_severity_badge(sev)} | {count} |")
    return "\n".join(lines) + "\n"


def _render_asr_table(breakdown: ASRBreakdown) -> str:
    lines = [
        f"## ASR by {breakdown.dimension.title()}\n",
        "| Name | Attacks | Successful | ASR | Trials | Avg Trials/Attack | Best Score | Min Score |",
        "|------|---------|------------|-----|--------|-------------------|------------|-----------|",
    ]
    for name, entry in sorted(breakdown.entries.items(), key=lambda x: -x[1].asr):
        lines.append(
            f"| {name} | {entry.total_attacks} | {entry.successful_attacks} "
            f"| {_pct(entry.asr)} | {entry.total_trials} | {entry.avg_trials_per_attack:.1f} "
            f"| {_fmt_score(entry.best_score)} | {_fmt_score(entry.min_score)} |"
        )
    return "\n".join(lines) + "\n"


def _render_findings(findings: list[Finding]) -> str:
    if not findings:
        return "## Top Findings\n\nNo findings above threshold.\n"

    lines = ["## Top Findings\n"]
    for f in findings:
        lines.append(f"### #{f.rank} {_severity_badge(f.severity)} -- {f.attack_name}")
        lines.append("")
        lines.append(f"- **Goal**: {f.goal}")
        lines.append(f"- **Category**: {f.goal_category}")
        lines.append(f"- **Score**: {_fmt_score(f.score)}")
        if f.transforms_applied:
            lines.append(f"- **Transforms**: {', '.join(f.transforms_applied)}")
        if f.compliance_tags:
            tags = ", ".join(f"{k}: {v}" for k, v in f.compliance_tags.items())
            lines.append(f"- **Compliance**: {tags}")
        lines.append("")
        lines.append("**Prompt:**")
        lines.append(f"> {_truncate(f.candidate)}")
        lines.append("")
        if f.response:
            lines.append("**Response:**")
            lines.append(f"> {_truncate(f.response)}")
            lines.append("")
        if f.secondary_scores:
            scores_str = ", ".join(f"{k}={v:.3f}" for k, v in f.secondary_scores.items())
            lines.append(f"- **Secondary scores**: {scores_str}")
            lines.append("")
    return "\n".join(lines) + "\n"


def _render_compliance_section(
    title: str,
    entries: dict[str, ComplianceEntry],
) -> str:
    lines = [
        f"### {title}\n",
        "| Category | Tested | ASR | Max Severity | Trials | Attacks |",
        "|----------|--------|-----|-------------|--------|---------|",
    ]
    for cat_id, entry in entries.items():
        tested = "Yes" if entry.tested else "No"
        asr = _pct(entry.asr) if entry.tested else "--"
        sev = _severity_badge(entry.max_severity) if entry.tested else "--"
        trials = str(entry.total_trials) if entry.tested else "--"
        attacks = ", ".join(entry.attacks_used) if entry.attacks_used else "--"
        lines.append(f"| {cat_id} | {tested} | {asr} | {sev} | {trials} | {attacks} |")
    return "\n".join(lines) + "\n"


def _render_compliance_matrix(analytics: CampaignAnalytics) -> str:
    matrix = analytics.compliance_matrix
    parts = ["## Compliance Matrix\n"]
    parts.append(_render_compliance_section("OWASP LLM Top 10", matrix.owasp_llm))
    parts.append(_render_compliance_section("OWASP Agentic Top 10", matrix.owasp_agentic))
    parts.append(_render_compliance_section("MITRE ATLAS", matrix.atlas))
    parts.append(_render_compliance_section("NIST AI RMF", matrix.nist))
    parts.append(_render_compliance_section("Google SAIF", matrix.saif))
    return "\n".join(parts)


def _render_transform_lift(analytics: CampaignAnalytics) -> str:
    lift = analytics.transform_lift
    if not lift:
        return ""
    lines = [
        "## Transform Effectiveness\n",
        "| Transform | ASR | Lift vs Baseline |",
        "|-----------|-----|-----------------|",
    ]
    entries = analytics.asr_by_transform.entries
    baseline_asr = entries["baseline"].asr if "baseline" in entries else 0.0
    lines.append(f"| baseline | {_pct(baseline_asr)} | -- |")
    for name, delta in sorted(lift.items(), key=lambda x: -x[1]):
        asr = entries[name].asr if name in entries else 0.0
        sign = "+" if delta >= 0 else ""
        lines.append(f"| {name} | {_pct(asr)} | {sign}{delta * 100:.1f}pp |")
    return "\n".join(lines) + "\n"


def _render_coverage_summary(analytics: CampaignAnalytics) -> str:
    lines = [
        "## Coverage Summary\n",
        "| Framework | Tested | Total | Coverage |",
        "|-----------|--------|-------|----------|",
    ]
    framework_labels = {
        "owasp_llm": "OWASP LLM Top 10",
        "owasp_agentic": "OWASP Agentic Top 10",
        "atlas": "MITRE ATLAS",
        "nist": "NIST AI RMF",
        "saif": "Google SAIF",
    }
    for key, label in framework_labels.items():
        cs = analytics.coverage_summary.get(key)
        if cs:
            lines.append(
                f"| {label} | {cs.tested_categories} | {cs.total_categories} "
                f"| {_pct(cs.coverage_pct)} |"
            )
    return "\n".join(lines) + "\n"


def _render_recommendations(analytics: CampaignAnalytics) -> str:
    if not analytics.recommendations:
        return "## Recommendations\n\nNo recommendations -- all tests passed.\n"

    lines = ["## Recommendations\n"]
    for idx, rec in enumerate(analytics.recommendations, start=1):
        lines.append(f"### {idx}. {_severity_badge(rec.severity)} {rec.title}")
        lines.append("")
        lines.append(rec.description)
        lines.append("")
        if rec.attack_vectors:
            lines.append(f"- **Effective attacks**: {', '.join(rec.attack_vectors)}")
        if rec.compliance_refs:
            lines.append(f"- **References**: {', '.join(rec.compliance_refs)}")
        lines.append("")
    return "\n".join(lines) + "\n"


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------


def generate_markdown_report(
    analytics: CampaignAnalytics,
    *,
    include_appendix: bool = True,
) -> str:
    """Render a full Markdown report from campaign analytics.

    Args:
        analytics: Populated :class:`CampaignAnalytics` from :func:`analyze`.
        include_appendix: If ``True``, append execution details.

    Returns:
        Complete Markdown document as a string.
    """
    sections = [
        _render_header(analytics),
        _render_severity_breakdown(analytics),
        _render_asr_table(analytics.asr_by_attack),
        _render_asr_table(analytics.asr_by_category),
        _render_asr_table(analytics.asr_by_transform),
        _render_asr_table(analytics.asr_by_goal),
        _render_transform_lift(analytics),
        _render_findings(analytics.top_findings),
        _render_coverage_summary(analytics),
        _render_compliance_matrix(analytics),
        _render_recommendations(analytics),
    ]

    if include_appendix:
        stats = analytics.execution_stats
        sections.append(
            "## Execution Details\n\n"
            f"| Metric | Value |\n"
            f"|--------|-------|\n"
            f"| Total Attacks | {stats.total_attacks} |\n"
            f"| Successful Attacks | {stats.successful_attacks} |\n"
            f"| Overall ASR | {_pct(stats.overall_asr)} |\n"
            f"| Total Trials | {stats.total_trials} |\n"
            f"| Pruned Trials | {stats.total_pruned} ({_pct(stats.pruning_rate)}) |\n"
            f"| Failed Trials | {stats.total_failed} ({_pct(stats.failure_rate)}) |\n"
            f"| Total Time | {stats.total_execution_time_s:.1f}s |\n"
            f"| Avg Trial Time | {stats.avg_trial_time_ms:.0f}ms |\n"
        )

    return "\n".join(sections)
