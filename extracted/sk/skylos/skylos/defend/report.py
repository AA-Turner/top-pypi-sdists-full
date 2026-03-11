from __future__ import annotations

import json
from collections import defaultdict
from datetime import datetime, timezone
from typing import Any

from skylos.defend.result import DefenseResult, DefenseScore, OpsScore
from skylos.defend.scoring import compute_defense_score, SEVERITY_WEIGHTS
from skylos.defend.policy import compute_owasp_coverage


def format_defense_table(
    results: list[DefenseResult],
    score: DefenseScore,
    integrations_count: int = 0,
    files_scanned: int = 0,
    owasp_coverage: dict | None = None,
    ops_score: OpsScore | None = None,
) -> str:
    lines = []

    lines.append("")
    lines.append("┌" + "─" * 74 + "┐")
    lines.append(
        f"│ {'Skylos AI Defense Report':<73}│"
    )
    lines.append(
        f"│ Scanned: {files_scanned} files | "
        f"Found: {integrations_count} LLM integration(s) | "
        f"Score: {score.score_pct}% ({score.risk_rating})"
        + " " * max(0, 74 - 31 - len(str(files_scanned)) - len(str(integrations_count)) - len(str(score.score_pct)) - len(score.risk_rating))
        + "│"
    )
    lines.append("├" + "─" * 74 + "┤")

    by_integration: dict[str, list[DefenseResult]] = defaultdict(list)
    for r in results:
        by_integration[r.integration_location].append(r)

    idx = 0
    for integ_loc, integ_results in by_integration.items():
        idx += 1
        integ_score = compute_defense_score(integ_results)

        lines.append("")
        lines.append(
            f"Integration {idx}: {integ_loc}"
        )
        lines.append(
            f"  Weighted Score: {integ_score.weighted_score}/{integ_score.weighted_max} "
            f"({integ_score.score_pct}%) — {integ_score.risk_rating} RISK"
        )

        sorted_results = sorted(
            integ_results, key=lambda r: (r.passed, -r.weight)
        )

        for r in sorted_results:
            mark = "✓" if r.passed else "✗"
            weight_str = f"[+{r.weight}]" if r.passed else f"[-{r.weight}]"
            lines.append(
                f"  {mark} {r.plugin_id:<24} {r.message:<40} {weight_str}"
            )

    lines.append("")
    lines.append("─" * 74)
    lines.append("")
    lines.append(
        f"AI Defense Score: {score.score_pct}% ({score.risk_rating})"
    )
    lines.append(
        f"  {score.weighted_score}/{score.weighted_max} weighted points | "
        f"{score.passed}/{score.total} checks passing"
    )

    if ops_score and ops_score.total > 0:
        lines.append("")
        lines.append(
            f"AI Ops Score: {ops_score.score_pct}% ({ops_score.rating})"
        )
        lines.append(
            f"  {ops_score.passed}/{ops_score.total} ops checks passing"
        )

    if owasp_coverage:
        lines.append("")
        lines.append("OWASP LLM Top 10 Coverage:")
        for owasp_id, info in owasp_coverage.items():
            if info["status"] == "not_applicable":
                continue
            status_icon = {
                "covered": "✓",
                "partial": "◐",
                "uncovered": "✗",
            }.get(info["status"], "?")
            pct_str = f"{info['coverage_pct']}%" if info['coverage_pct'] is not None else "N/A"
            lines.append(
                f"  {status_icon} {owasp_id} {info['name']:<35} {pct_str:>5} "
                f"({info['passed']}/{info['total']})"
            )

    lines.append("")
    return "\n".join(lines)


def format_defense_json(
    results: list[DefenseResult],
    score: DefenseScore,
    integrations_count: int = 0,
    files_scanned: int = 0,
    project_path: str = ".",
    owasp_coverage: dict | None = None,
    ops_score: OpsScore | None = None,
) -> str:
    by_severity: dict[str, dict[str, int]] = {}
    for sev in ("critical", "high", "medium", "low"):
        sev_results = [r for r in results if r.severity == sev]
        by_severity[sev] = {
            "passed": sum(1 for r in sev_results if r.passed),
            "failed": sum(1 for r in sev_results if not r.passed),
            "weight": SEVERITY_WEIGHTS[sev],
        }

    data: dict[str, Any] = {
        "version": "1.0",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "project": project_path,
        "summary": {
            "integrations_found": integrations_count,
            "files_scanned": files_scanned,
            "total_checks": score.total,
            "passed": score.passed,
            "failed": score.total - score.passed,
            "weighted_score": score.weighted_score,
            "weighted_max": score.weighted_max,
            "score_pct": score.score_pct,
            "risk_rating": score.risk_rating,
            "by_severity": by_severity,
        },
        "findings": [r.to_dict() for r in results],
    }

    if owasp_coverage:
        data["owasp_coverage"] = owasp_coverage

    if ops_score:
        data["ops_score"] = ops_score.to_dict()

    return json.dumps(data, indent=2)
