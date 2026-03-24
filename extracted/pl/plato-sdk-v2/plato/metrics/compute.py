"""Metric computation dispatcher."""

from __future__ import annotations

import json
import logging
from typing import TYPE_CHECKING, Any

from plato.metrics.specs import (
    HumanAgreement,
    LLMComparison,
    MetricResult,
    MetricSpec,
    SessionResultField,
    VerifierPassRate,
    VerifierScore,
)

if TYPE_CHECKING:
    from plato.chronos.sdk import AsyncChronos
    from plato.llm import LLMClient

logger = logging.getLogger(__name__)


async def compute_metric(
    spec: MetricSpec,
    session_id: str,
    chronos: AsyncChronos,
    llm_client: LLMClient | None = None,
) -> MetricResult:
    """Compute a metric for a completed session.

    Args:
        spec: The metric specification (discriminated union).
        session_id: The Chronos session to evaluate.
        chronos: An authenticated AsyncChronos client.
        llm_client: Optional LLM client for LLMComparison metrics.

    Returns:
        MetricResult with the computed value and breakdown details.
    """
    if isinstance(spec, VerifierPassRate):
        return await _compute_verifier_pass_rate(session_id, chronos)
    elif isinstance(spec, VerifierScore):
        return await _compute_verifier_score(session_id, chronos)
    elif isinstance(spec, HumanAgreement):
        return await _compute_human_agreement(session_id, chronos)
    elif isinstance(spec, LLMComparison):
        return await _compute_llm_comparison(spec, session_id, chronos, llm_client)
    elif isinstance(spec, SessionResultField):
        return await _compute_session_result_field(spec, session_id, chronos)
    else:
        raise ValueError(f"Unknown metric spec type: {type(spec)}")


async def _compute_verifier_pass_rate(
    session_id: str,
    chronos: AsyncChronos,
) -> MetricResult:
    """Count annotations with signal=pass vs total with any signal."""
    annotations = await _fetch_annotations(session_id, chronos)

    with_signal = [a for a in annotations if a.get("signal")]
    if not with_signal:
        return MetricResult(value=0.0, details={"error": "No annotations with signal found"})

    passed = sum(1 for a in with_signal if a["signal"] == "pass")
    total = len(with_signal)

    return MetricResult(
        value=passed / total if total > 0 else 0.0,
        details={
            "passed": passed,
            "total": total,
            "by_signal": _count_by_signal(with_signal),
        },
    )


async def _compute_verifier_score(
    session_id: str,
    chronos: AsyncChronos,
) -> MetricResult:
    """Average numeric scores from annotation data fields."""
    annotations = await _fetch_annotations(session_id, chronos)

    scores: list[float] = []
    for ann in annotations:
        data = ann.get("data")
        if isinstance(data, dict) and data.get("type") == "score":
            score_val = data.get("score")
            if isinstance(score_val, (int, float)):
                scores.append(float(score_val))

    if not scores:
        return MetricResult(value=0.0, details={"error": "No score data found in annotations"})

    avg = sum(scores) / len(scores)
    return MetricResult(
        value=avg,
        details={
            "scores": scores,
            "count": len(scores),
            "min": min(scores),
            "max": max(scores),
        },
    )


async def _compute_human_agreement(
    session_id: str,
    chronos: AsyncChronos,
) -> MetricResult:
    """Agreement rate: how often humans approve verifier findings."""
    resp = await chronos._client.request(
        method="GET",
        url="/api/annotations/metrics",
        params={"session_id": session_id},
    )
    resp.raise_for_status()
    metrics = resp.json()

    agreement = metrics.get("human_agreement", {})
    rate = agreement.get("agreement_rate", 0.0)

    return MetricResult(
        value=float(rate),
        details={
            "total_reviewed": agreement.get("total_reviewed", 0),
            "agreed": agreement.get("agreed", 0),
            "disagreed": agreement.get("disagreed", 0),
            "total_with_signal": metrics.get("total_with_signal", 0),
            "by_signal": metrics.get("by_signal", {}),
        },
    )


async def _compute_llm_comparison(
    spec: LLMComparison,
    session_id: str,
    chronos: AsyncChronos,
    llm_client: LLMClient | None,
) -> MetricResult:
    """Ask an LLM to score the session against criteria or a reference."""
    if not llm_client:
        # Create a temporary client from spec
        from plato.llm import LLMClient as _LLMClient
        from plato.worlds.config import LLMConfig

        config = LLMConfig(model=spec.llm_model, api_key=spec.llm_api_key or "")
        llm_client = _LLMClient(config)

    # Fetch target session result
    session = await _fetch_session(session_id, chronos)
    session_result = json.dumps(session.get("result", {}), indent=2, default=str)

    # Fetch reference if specified
    reference_result = ""
    if spec.reference_session_id:
        ref_session = await _fetch_session(spec.reference_session_id, chronos)
        reference_result = json.dumps(ref_session.get("result", {}), indent=2, default=str)

    prompt = spec.comparison_prompt.format(
        session_result=session_result,
        reference_result=reference_result,
    )

    response = await llm_client(
        messages=[{"role": "user", "content": prompt}],
        system=("You are evaluating a session's results. " 'Respond with JSON: {"score": 0.0-1.0, "evidence": "..."}'),
        max_tokens=1024,
    )

    try:
        parsed = json.loads(response.text.strip())
        score = max(0.0, min(1.0, float(parsed.get("score", 0.0))))
        evidence = str(parsed.get("evidence", ""))
    except (json.JSONDecodeError, ValueError):
        score = 0.0
        evidence = f"Failed to parse LLM response: {response.text[:200]}"

    return MetricResult(
        value=score,
        details={"evidence": evidence, "llm_model": spec.llm_model},
    )


async def _compute_session_result_field(
    spec: SessionResultField,
    session_id: str,
    chronos: AsyncChronos,
) -> MetricResult:
    """Extract a numeric field from session.result by dot path."""
    session = await _fetch_session(session_id, chronos)
    result = session.get("result", {})

    # Navigate dot path
    value: Any = result
    for key in spec.field_path.split("."):
        if isinstance(value, dict):
            value = value.get(key)
        else:
            value = None
            break

    if value is None:
        return MetricResult(
            value=0.0,
            details={"error": f"Field path '{spec.field_path}' not found in session result"},
        )

    try:
        numeric = float(value)
    except (TypeError, ValueError):
        return MetricResult(
            value=0.0,
            details={"error": f"Field '{spec.field_path}' is not numeric: {value}"},
        )

    return MetricResult(
        value=numeric,
        details={"field_path": spec.field_path, "raw_value": value},
    )


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


async def _fetch_annotations(session_id: str, chronos: AsyncChronos) -> list[dict[str, Any]]:
    """Fetch all annotations for a session."""
    resp = await chronos._client.request(
        method="GET",
        url="/api/annotations",
        params={"session_id": session_id},
    )
    resp.raise_for_status()
    data = resp.json()
    return data.get("annotations", [])


async def _fetch_session(session_id: str, chronos: AsyncChronos) -> dict[str, Any]:
    """Fetch a session by ID."""
    resp = await chronos._client.request(
        method="GET",
        url=f"/api/sessions/{session_id}",
    )
    resp.raise_for_status()
    return resp.json()


def _count_by_signal(annotations: list[dict[str, Any]]) -> dict[str, int]:
    """Count annotations by signal value."""
    counts: dict[str, int] = {}
    for ann in annotations:
        signal = ann.get("signal", "unknown")
        counts[signal] = counts.get(signal, 0) + 1
    return counts
