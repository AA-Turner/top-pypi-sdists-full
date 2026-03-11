from __future__ import annotations

from skylos.defend.result import DefenseResult, DefenseScore, OpsScore

SEVERITY_WEIGHTS: dict[str, int] = {
    "critical": 8,
    "high": 5,
    "medium": 3,
    "low": 1,
}


def compute_defense_score(results: list[DefenseResult]) -> DefenseScore:
    defense_results = [r for r in results if r.category == "defense"]
    if not defense_results:
        return DefenseScore(
            weighted_score=0,
            weighted_max=0,
            score_pct=100,
            risk_rating="SECURE",
            passed=0,
            total=0,
        )

    weighted_max = sum(r.weight for r in defense_results)
    weighted_score = sum(r.weight for r in defense_results if r.passed)
    pct = round(weighted_score / weighted_max * 100) if weighted_max > 0 else 100

    if pct < 25:
        risk = "CRITICAL"
    elif pct < 50:
        risk = "HIGH"
    elif pct < 75:
        risk = "MEDIUM"
    elif pct < 90:
        risk = "LOW"
    else:
        risk = "SECURE"

    return DefenseScore(
        weighted_score=weighted_score,
        weighted_max=weighted_max,
        score_pct=pct,
        risk_rating=risk,
        passed=sum(1 for r in defense_results if r.passed),
        total=len(defense_results),
    )


def compute_ops_score(results: list[DefenseResult]) -> OpsScore:
    ops_results = [r for r in results if r.category == "ops"]
    if not ops_results:
        return OpsScore(passed=0, total=0, score_pct=100, rating="EXCELLENT")

    passed = sum(1 for r in ops_results if r.passed)
    total = len(ops_results)
    pct = round(passed / total * 100) if total > 0 else 100

    if pct >= 80:
        rating = "EXCELLENT"
    elif pct >= 60:
        rating = "GOOD"
    elif pct >= 40:
        rating = "FAIR"
    else:
        rating = "POOR"

    return OpsScore(passed=passed, total=total, score_pct=pct, rating=rating)
