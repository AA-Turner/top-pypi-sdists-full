"""Typed metric specifications for evaluation and hill-climbing.

Metrics are pluggable computations that evaluate a completed session
and return a numeric value. Used by the hill-climb world to measure
progress across iterations.

Usage:
    from plato.metrics import MetricSpec, VerifierPassRate, compute_metric

    spec = VerifierPassRate()
    result = await compute_metric(spec, session_id="...", chronos=client)
    print(result.value)  # 0.85
"""

from plato.metrics.compute import compute_metric
from plato.metrics.specs import (
    HumanAgreement,
    LLMComparison,
    MetricResult,
    MetricSpec,
    SessionResultField,
    VerifierPassRate,
    VerifierScore,
)

__all__ = [
    "HumanAgreement",
    "LLMComparison",
    "MetricResult",
    "MetricSpec",
    "SessionResultField",
    "VerifierPassRate",
    "VerifierScore",
    "compute_metric",
]
