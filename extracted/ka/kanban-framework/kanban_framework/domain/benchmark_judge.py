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
    task_id: str = ""
    task_dir: str = ""
    # v0.188: LLM efficiency dimensions (populated from LLMStatsReader)
    llm_calls: int = 0
    llm_tokens_input: int = 0
    llm_tokens_output: int = 0
    llm_tokens_cache_read: int = 0
    llm_tokens_effective: int = 0  # input + output (what actually costs)
    llm_quality_per_call: float = 0.0  # score / calls (higher = more efficient)
    llm_score_per_1k_tokens: float = 0.0  # score per 1K effective tokens
    llm_cache_efficiency: float = 0.0  # cache_read / (cache_read + input)


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


_ACCEPTANCE_STOP_WORDS = {
    "的", "了", "是", "在", "和", "与", "或", "不", "都", "也",
    "the", "a", "an", "is", "are", "be", "to", "of", "in", "and", "or",
}


def _match_acceptance(acceptance: list[str], report_dir: Path) -> list[dict]:
    """Check each acceptance criterion against available sub-agent reports.

    Uses keyword overlap: splits criterion into meaningful words, checks if
    enough appear in reports. Handles mixed Chinese/English acceptance text.
    """
    import re

    results = []
    report_texts = _collect_report_texts(report_dir)
    combined = " ".join(report_texts).lower()

    for criterion in acceptance:
        # Split into words: Chinese chars individually, English/latin words as groups
        words = re.findall(r'[一-鿿]|[a-zA-Z0-9]{2,}', criterion.lower())
        keywords = [w for w in words if w not in _ACCEPTANCE_STOP_WORDS]

        if not keywords:
            # Fallback: original substring check
            matched = criterion.lower()[:30] in combined
        else:
            hits = sum(1 for w in keywords if w in combined)
            matched = (hits / len(keywords)) >= 0.5

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
                # Serialize back with ensure_ascii=False so Chinese chars are
                # preserved as-is for keyword/acronym/pattern matching
                texts.append(json.dumps(data, ensure_ascii=False))
            except Exception:
                pass

    return texts


def score_search_quality(query: str, expected_ids: list[str], biz_tag: str = "") -> dict | None:
    """Measure KB search quality against expected results.

    Runs hybrid search with the query text, compares returned IDs against
    expected_knowledge entries. Returns precision/recall/relevance metrics.
    """
    if not expected_ids:
        return None

    try:
        from kanban_framework.infra.filesystem import Filesystem as FS
        from kanban_framework.domain.knowledge import KnowledgeManager
        root = FS.find_project_root()
        fs = FS(root=root)
        km = KnowledgeManager(fs, read_only=True)

        # Run hybrid search with query
        results = km.search_hybrid(query[:120], limit=20, biz_context=biz_tag or None)

        returned_ids = {r["id"] for r in results}
        expected_set = set(expected_ids)

        relevant = returned_ids & expected_set
        precision = len(relevant) / len(returned_ids) if returned_ids else 0.0
        recall = len(relevant) / len(expected_set) if expected_set else 0.0
        f1 = 2 * precision * recall / (precision + recall) if (precision + recall) > 0 else 0.0

        # Average relevance of matched results
        relevance_scores = [r.get("relevance", 0) for r in results if r["id"] in relevant]
        relevance_avg = round(sum(relevance_scores) / len(relevance_scores), 3) if relevance_scores else 0.0

        return {
            "query": query[:80],
            "expected": sorted(expected_set),
            "returned": sorted(returned_ids)[:10],
            "hits": sorted(relevant),
            "precision": round(precision, 3),
            "recall": round(recall, 3),
            "f1": round(f1, 3),
            "relevance_avg": relevance_avg,
        }
    except Exception:
        return None


def _compute_aggregate_score(dimensions: dict) -> float:
    """Compute weighted average score across dimensions."""
    if not dimensions:
        return 0.0
    return round(sum(dimensions.values()) / len(dimensions), 1)
