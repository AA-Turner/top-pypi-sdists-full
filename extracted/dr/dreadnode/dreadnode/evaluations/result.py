import json
import statistics
import typing as t
from collections import defaultdict
from dataclasses import dataclass, field
from pathlib import Path

import pandas as pd
import typing_extensions as te

from dreadnode.core.metric import MetricSeries
from dreadnode.evaluations.sample import Sample

In = te.TypeVar("In", default=t.Any)
Out = te.TypeVar("Out", default=t.Any)

EvalStopReason = t.Literal[
    "finished",
    "max_errors_reached",
    "max_consecutive_errors_reached",
    "cancelled",
]


@dataclass
class EvalResult(t.Generic[In, Out]):
    """Result of an evaluation run."""

    samples: list[Sample[In, Out]] = field(default_factory=list)
    """All samples from this evaluation."""
    stop_reason: EvalStopReason | None = None
    """The reason the evaluation stopped."""

    @property
    def passed_count(self) -> int:
        """The number of samples that passed all assertions."""
        return sum(1 for s in self.samples if s.passed)

    @property
    def failed_count(self) -> int:
        """The number of samples that failed any assertions."""
        return sum(1 for s in self.samples if not s.passed)

    @property
    def passed_samples(self) -> list[Sample[In, Out]]:
        """A list of all samples that passed all assertions."""
        return [s for s in self.samples if s.passed]

    @property
    def error_samples(self) -> list[Sample[In, Out]]:
        """A list of all samples that encountered an error during processing."""
        return [s for s in self.samples if s.error is not None]

    @property
    def error_count(self) -> int:
        """The number of samples that encountered an error during processing."""
        return sum(1 for s in self.samples if s.error is not None)

    @property
    def failed_samples(self) -> list[Sample[In, Out]]:
        """A list of all samples that failed at least one assertion."""
        return [s for s in self.samples if not s.passed]

    @property
    def pass_rate(self) -> float:
        """The overall pass rate of the evaluation, from 0.0 to 1.0."""
        if not self.samples:
            return 0.0
        return self.passed_count / len(self.samples)

    @property
    def metrics(self) -> dict[str, list[float]]:
        """Returns a breakdown of all metric values across all samples."""
        breakdown: defaultdict[str, list[float]] = defaultdict(list)

        for sample in self.samples:
            for name, metric_data in sample.metrics.items():
                if isinstance(metric_data, MetricSeries):
                    if metric_data.value is not None:
                        breakdown[name].append(metric_data.value)
                elif isinstance(metric_data, list) and metric_data:
                    breakdown[name].append(metric_data[-1].value)

        return dict(breakdown)

    @property
    def metrics_summary(self) -> dict[str, dict[str, float]]:
        """Calculates and returns a summary of statistics for each metric."""
        summary: dict[str, dict[str, float]] = {}
        for name, values in self.metrics.items():
            if not values:
                continue

            summary[name] = {
                "mean": statistics.mean(values),
                "stdev": statistics.stdev(values) if len(values) > 1 else 0.0,
                "min": min(values),
                "max": max(values),
                "count": len(values),
            }

        return summary

    @property
    def metrics_aggregated(self) -> dict[str, float]:
        """Aggregates metrics by calculating the mean for each metric."""
        return {name: stats["mean"] for name, stats in self.metrics_summary.items()}

    @property
    def assertions_summary(self) -> dict[str, dict[str, float | int]]:
        """Calculates and returns a summary for each assertion across all samples."""
        assertions_results: dict[str, list[bool]] = defaultdict(list)
        for sample in self.samples:
            for name, passed in sample.assertions.items():
                assertions_results[name].append(passed)

        summary: dict[str, dict[str, float | int]] = {}
        for name, results in assertions_results.items():
            if not results:
                continue

            passed_count = sum(1 for r in results if r)
            total_count = len(results)
            pass_rate = passed_count / total_count if total_count > 0 else 0.0

            summary[name] = {
                "passed_count": passed_count,
                "failed_count": total_count - passed_count,
                "pass_rate": pass_rate,
            }
        return summary

    def to_dicts(self) -> list[dict[str, t.Any]]:
        """Flattens the results into a list of dictionaries."""
        return [sample.to_dict() for sample in self.samples]

    def to_dataframe(self) -> "pd.DataFrame":
        """Converts the results into a pandas DataFrame for analysis."""
        return pd.DataFrame(self.to_dicts())

    def to_jsonl(self, path: str | Path) -> None:
        """Saves the results to a JSON Lines (JSONL) file."""
        records = self.to_dicts()
        with Path(path).open("w", encoding="utf-8") as f:
            f.writelines(json.dumps(record) + "\n" for record in records)

    def __repr__(self) -> str:
        parts: list[str] = [f"samples={len(self.samples)}"]

        if self.samples:
            parts.extend(
                [
                    f"passed={self.passed_count}",
                    f"failed={self.failed_count}",
                    f"pass_rate={self.pass_rate:.3f}",
                ]
            )

        return f"{self.__class__.__name__}({', '.join(parts)})"
