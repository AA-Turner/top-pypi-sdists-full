"""Judge module — aggregate sub-agent reports, match against acceptance criteria."""
from __future__ import annotations

import json
from pathlib import Path
from dataclasses import dataclass


@dataclass
class CaseVerdict:
    case_id: str
    verdict: str  # "pass" | "fail" | "error"
    score: float
    dimensions: dict
    acceptance_results: list[dict]
    evidence: str


def judge_case(case_id: str, acceptance: list[str], report_dir: Path) -> CaseVerdict:
    """Collect sub-agent reports and judge against acceptance criteria."""
    dimensions = _collect_dimensions(report_dir)
    acceptance_results = _match_acceptance(acceptance, report_dir)
    score = _compute_aggregate_score(dimensions)
    matched = sum(1 for a in acceptance_results if a["matched"])
    total = len(acceptance_results)
    verdict = "pass" if total == 0 or matched == total else "fail"

    return CaseVerdict(
        case_id=case_id,
        verdict=verdict,
        score=score,
        dimensions=dimensions,
        acceptance_results=acceptance_results,
        evidence=f"Acceptance: {matched}/{total} matched. Dimensions: {list(dimensions.keys())}",
    )


def _collect_dimensions(report_dir: Path) -> dict:
    """Scan report_dir/reviews/*.json for sub-agent reports, extract scores."""
    reviews_dir = report_dir / "reviews"
    dimensions = {}

    search_dirs = [reviews_dir] if reviews_dir.exists() else []
    if report_dir.exists():
        search_dirs.append(report_dir)

    for d in search_dirs:
        if not d.exists():
            continue
        for report_file in sorted(d.glob("*_report.json")):
            role = report_file.stem.replace("_report", "")
            try:
                data = json.loads(report_file.read_text())
                if isinstance(data, dict) and "total" in data:
                    dimensions[role] = float(data["total"])
            except (json.JSONDecodeError, ValueError, TypeError):
                pass

    return dimensions


def _match_acceptance(acceptance: list[str], report_dir: Path) -> list[dict]:
    """Check each acceptance criterion against available sub-agent reports."""
    results = []
    report_texts = _collect_report_texts(report_dir)

    for criterion in acceptance:
        matched = False
        criterion_lower = criterion.lower()
        for text in report_texts:
            # Check if the criterion's key terms appear in any report
            if criterion_lower[:40] in text.lower():
                matched = True
                break
        results.append({"criterion": criterion, "matched": matched})

    return results


def _collect_report_texts(report_dir: Path) -> list[str]:
    """Collect all report file contents as plain text for acceptance matching."""
    texts = []
    reviews_dir = report_dir / "reviews"
    search_dirs = [reviews_dir] if reviews_dir.exists() else []
    if report_dir.exists():
        search_dirs.append(report_dir)

    for d in search_dirs:
        if not d.exists():
            continue
        for f in d.glob("*_report.json"):
            try:
                data = json.loads(f.read_text())
                # Re-serialize with ensure_ascii=False so non-ASCII characters
                # (e.g. Chinese) are preserved for substring matching
                texts.append(json.dumps(data, ensure_ascii=False))
            except Exception:
                pass

    return texts


def _compute_aggregate_score(dimensions: dict) -> float:
    """Compute weighted average score across dimensions."""
    if not dimensions:
        return 0.0
    return round(sum(dimensions.values()) / len(dimensions), 1)
