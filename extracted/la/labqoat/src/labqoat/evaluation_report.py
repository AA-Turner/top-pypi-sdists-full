"""Versioned complete-case evaluation reports transported as ordinary typed Run results."""

import math
from collections.abc import Sequence
from dataclasses import dataclass
from typing import Literal

from labqoat.evaluation_case import EvaluationCase
from labqoat.references import ResourceId
from labqoat.training.metric_batch import MetricBatch


@dataclass(frozen=True)
class EvaluationReport:
    """Retain explicit membership, scoring evidence and reproducible equal-weight means for presentation."""

    dataset_id: str
    expected: tuple[str, ...]
    results: tuple[EvaluationCase, ...]
    metrics: dict[str, float]
    source_run_id: str | None = None
    kind: Literal["evaluation"] = "evaluation"
    version: int = 1

    def __post_init__(self) -> None:
        """Validate decoded reports as strictly as authored ones without changing Run completion rules."""
        ResourceId.parse(self.dataset_id)
        if self.source_run_id is not None:
            ResourceId.parse(self.source_run_id)
        if self.kind != "evaluation" or self.version != 1:
            raise ValueError("Unsupported evaluation report version")
        if self.metrics != self.aggregate(self.expected, self.results):
            raise ValueError("Evaluation aggregates do not match case evidence")

    @classmethod
    def complete(
        cls,
        dataset_id: str,
        expected: Sequence[str],
        results: Sequence[EvaluationCase],
        *,
        source_run_id: str | None = None,
    ) -> "EvaluationReport":
        """Validate all planned cases and return a portable result with no network calls or hidden state."""
        ordered = tuple(sorted(results, key=cls._key))
        keys = tuple(sorted(expected))
        return cls(dataset_id, keys, ordered, cls.aggregate(keys, ordered), source_run_id)

    @staticmethod
    def aggregate(expected: Sequence[str], results: Sequence[EvaluationCase]) -> dict[str, float]:
        """Reject missing, duplicate, extra or inconsistent case evidence before averaging any score."""
        keys = [case.key for case in results]
        if not 1 <= len(expected) <= 10_000 or len(set(expected)) != len(expected):
            raise ValueError("Evaluation requires bounded unique expected membership")
        if len(keys) != len(expected) or set(keys) != set(expected):
            raise ValueError("Evaluation did not complete every expected case exactly once")
        names = set(results[0].metrics)
        if any(set(case.metrics) != names for case in results):
            raise ValueError("Evaluation cases must have consistent metric names")
        metrics = {name: math.fsum(case.metrics[name] / len(results) for case in results) for name in sorted(names)}
        MetricBatch(step=0, metrics=tuple(metrics.items()))
        return metrics

    @staticmethod
    def _key(case: EvaluationCase) -> str:
        """Canonicalize case ordering independently of asynchronous completion order."""
        return case.key
