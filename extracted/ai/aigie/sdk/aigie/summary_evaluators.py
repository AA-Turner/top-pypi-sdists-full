"""
Summary Evaluators for Aigie SDK.

Summary evaluators aggregate metrics across entire datasets,
providing dataset-level insights for experiments and A/B tests.
"""

import statistics
from abc import ABC, abstractmethod
from collections.abc import Callable
from dataclasses import dataclass, field
from typing import Any


@dataclass
class RunData:
    """Run data for summary evaluation."""

    id: str
    """Run ID"""

    input: Any
    """Input to the system"""

    output: Any
    """Output from the system"""

    expected: Any | None = None
    """Expected/reference output (if available)"""

    metadata: dict[str, Any] = field(default_factory=dict)
    """Metadata"""

    evaluations: list[Any] = field(default_factory=list)
    """Per-example evaluation results"""


@dataclass
class SummaryEvaluationResult:
    """Summary evaluation result."""

    name: str
    """Name of the summary metric"""

    score: float
    """Aggregated score"""

    metrics: dict[str, float] = field(default_factory=dict)
    """Additional metrics"""

    reasoning: str | None = None
    """Explanation"""

    metadata: dict[str, Any] = field(default_factory=dict)
    """Metadata"""


# Type for summary evaluator function
SummaryEvaluatorFunction = Callable[
    [list[RunData]], SummaryEvaluationResult | list[SummaryEvaluationResult]
]


class SummaryEvaluator(ABC):
    """Base Summary Evaluator class."""

    def __init__(self, name: str, description: str | None = None):
        """
        Initialize summary evaluator.

        Args:
            name: Evaluator name
            description: Optional description
        """
        self.name = name
        self.description = description

    @abstractmethod
    async def evaluate(
        self, runs: list[RunData]
    ) -> SummaryEvaluationResult | list[SummaryEvaluationResult]:
        """
        Evaluate across all runs.

        Args:
            runs: List of run data

        Returns:
            Summary evaluation result(s)
        """
        raise NotImplementedError

    @staticmethod
    def from_function(
        name: str, fn: SummaryEvaluatorFunction, description: str | None = None
    ) -> "FunctionSummaryEvaluator":
        """
        Create summary evaluator from function.

        Args:
            name: Evaluator name
            fn: Evaluation function
            description: Optional description

        Returns:
            Function-based summary evaluator
        """
        return FunctionSummaryEvaluator(name, fn, description)


class FunctionSummaryEvaluator(SummaryEvaluator):
    """Function-based summary evaluator."""

    def __init__(self, name: str, fn: SummaryEvaluatorFunction, description: str | None = None):
        super().__init__(name, description)
        self.fn = fn

    async def evaluate(
        self, runs: list[RunData]
    ) -> SummaryEvaluationResult | list[SummaryEvaluationResult]:
        """Execute the function."""
        return self.fn(runs)


class AccuracySummaryEvaluator(SummaryEvaluator):
    """
    Accuracy Summary Evaluator.

    Calculates overall accuracy across dataset by checking
    if outputs match expected values.
    """

    def __init__(
        self,
        output_key: str | None = None,
        expected_key: str | None = None,
        case_sensitive: bool = True,
    ):
        """
        Initialize accuracy summary evaluator.

        Args:
            output_key: Key to extract from output
            expected_key: Key to extract from expected
            case_sensitive: Case sensitive comparison
        """
        super().__init__("accuracy_summary", "Overall accuracy across dataset")
        self.output_key = output_key
        self.expected_key = expected_key
        self.case_sensitive = case_sensitive

    async def evaluate(self, runs: list[RunData]) -> SummaryEvaluationResult:
        """Calculate accuracy across runs."""
        runs_with_expected = [r for r in runs if r.expected is not None]

        if not runs_with_expected:
            return SummaryEvaluationResult(
                name=self.name,
                score=0.0,
                metrics={"total": len(runs), "with_expected": 0},
                reasoning="No runs have expected values",
            )

        correct = 0
        for run in runs_with_expected:
            output = (
                run.output.get(self.output_key)
                if self.output_key and isinstance(run.output, dict)
                else run.output
            )
            expected = (
                run.expected.get(self.expected_key)
                if self.expected_key and isinstance(run.expected, dict)
                else run.expected
            )

            output_str = str(output)
            expected_str = str(expected)

            if not self.case_sensitive:
                output_str = output_str.lower()
                expected_str = expected_str.lower()

            if output_str == expected_str:
                correct += 1

        accuracy = correct / len(runs_with_expected)

        return SummaryEvaluationResult(
            name=self.name,
            score=accuracy,
            metrics={
                "correct": correct,
                "total": len(runs_with_expected),
                "accuracy": accuracy,
                "coverage": len(runs_with_expected) / len(runs),
            },
            reasoning=f"{correct}/{len(runs_with_expected)} predictions correct ({accuracy * 100:.1f}%)",
        )


class PrecisionSummaryEvaluator(SummaryEvaluator):
    """
    Precision Summary Evaluator.

    Calculates precision from per-example evaluation results.
    """

    def __init__(self, evaluator_name: str | None = None):
        """
        Initialize precision summary evaluator.

        Args:
            evaluator_name: Name of evaluator to use (if None, uses first)
        """
        super().__init__("precision_summary", "Precision across dataset")
        self.evaluator_name = evaluator_name

    async def evaluate(self, runs: list[RunData]) -> SummaryEvaluationResult:
        """Calculate precision across runs."""
        true_positives = 0
        false_positives = 0

        for run in runs:
            if not run.evaluations:
                continue

            eval_result = None
            if self.evaluator_name:
                eval_result = next(
                    (
                        e
                        for e in run.evaluations
                        if hasattr(e, "name") and e.name == self.evaluator_name
                    ),
                    None,
                )
            else:
                eval_result = run.evaluations[0] if run.evaluations else None

            if not eval_result:
                continue

            passed = getattr(eval_result, "passed", None)
            if passed is None:
                score = getattr(eval_result, "score", 0)
                passed = score >= 0.5

            if passed:
                true_positives += 1
            else:
                false_positives += 1

        precision = (
            true_positives / (true_positives + false_positives)
            if (true_positives + false_positives) > 0
            else 0.0
        )

        return SummaryEvaluationResult(
            name=self.name,
            score=precision,
            metrics={
                "precision": precision,
                "true_positives": true_positives,
                "false_positives": false_positives,
            },
            reasoning=f"Precision: {precision * 100:.1f}% (TP: {true_positives}, FP: {false_positives})",
        )


class AverageScoreSummaryEvaluator(SummaryEvaluator):
    """
    Average Score Summary Evaluator.

    Calculates mean score across all per-example evaluations.
    """

    def __init__(self, evaluator_name: str | None = None):
        """
        Initialize average score summary evaluator.

        Args:
            evaluator_name: Name of evaluator to use (if None, uses first)
        """
        super().__init__("average_score_summary", "Average score across dataset")
        self.evaluator_name = evaluator_name

    async def evaluate(self, runs: list[RunData]) -> SummaryEvaluationResult:
        """Calculate average score across runs."""
        scores: list[float] = []

        for run in runs:
            if not run.evaluations:
                continue

            eval_result = None
            if self.evaluator_name:
                eval_result = next(
                    (
                        e
                        for e in run.evaluations
                        if hasattr(e, "name") and e.name == self.evaluator_name
                    ),
                    None,
                )
            else:
                eval_result = run.evaluations[0] if run.evaluations else None

            if eval_result and hasattr(eval_result, "score"):
                scores.append(eval_result.score)

        if not scores:
            return SummaryEvaluationResult(
                name=self.name,
                score=0.0,
                metrics={"count": 0},
                reasoning="No evaluation scores found",
            )

        mean = statistics.mean(scores)
        median = statistics.median(scores)
        min_score = min(scores)
        max_score = max(scores)
        std = statistics.stdev(scores) if len(scores) > 1 else 0.0

        sorted_scores = sorted(scores)
        p25 = sorted_scores[int(len(sorted_scores) * 0.25)]
        p75 = sorted_scores[int(len(sorted_scores) * 0.75)]
        p95 = sorted_scores[int(len(sorted_scores) * 0.95)]

        return SummaryEvaluationResult(
            name=self.name,
            score=mean,
            metrics={
                "mean": mean,
                "median": median,
                "min": min_score,
                "max": max_score,
                "std": std,
                "count": len(scores),
                "p25": p25,
                "p75": p75,
                "p95": p95,
            },
            reasoning=f"Mean score: {mean:.3f} (median: {median:.3f}, std: {std:.3f})",
        )


class PassRateSummaryEvaluator(SummaryEvaluator):
    """
    Pass Rate Summary Evaluator.

    Calculates percentage of runs that passed evaluation.
    """

    def __init__(self, evaluator_name: str | None = None, threshold: float = 0.5):
        """
        Initialize pass rate summary evaluator.

        Args:
            evaluator_name: Name of evaluator to use (if None, uses first)
            threshold: Score threshold for pass/fail
        """
        super().__init__("pass_rate_summary", "Pass rate across dataset")
        self.evaluator_name = evaluator_name
        self.threshold = threshold

    async def evaluate(self, runs: list[RunData]) -> SummaryEvaluationResult:
        """Calculate pass rate across runs."""
        passed = 0
        total = 0

        for run in runs:
            if not run.evaluations:
                continue

            eval_result = None
            if self.evaluator_name:
                eval_result = next(
                    (
                        e
                        for e in run.evaluations
                        if hasattr(e, "name") and e.name == self.evaluator_name
                    ),
                    None,
                )
            else:
                eval_result = run.evaluations[0] if run.evaluations else None

            if not eval_result:
                continue

            total += 1
            did_pass = getattr(eval_result, "passed", None)
            if did_pass is None:
                score = getattr(eval_result, "score", 0)
                did_pass = score >= self.threshold

            if did_pass:
                passed += 1

        pass_rate = passed / total if total > 0 else 0.0

        return SummaryEvaluationResult(
            name=self.name,
            score=pass_rate,
            metrics={
                "pass_rate": pass_rate,
                "passed": passed,
                "total": total,
                "failed": total - passed,
            },
            reasoning=f"{passed}/{total} runs passed ({pass_rate * 100:.1f}%)",
        )


class CostSummaryEvaluator(SummaryEvaluator):
    """
    Cost Summary Evaluator.

    Aggregates cost metrics across all runs.
    """

    def __init__(self):
        super().__init__("cost_summary", "Total cost across dataset")

    async def evaluate(self, runs: list[RunData]) -> SummaryEvaluationResult:
        """Calculate cost summary across runs."""
        total_cost = 0.0
        total_input_tokens = 0
        total_output_tokens = 0
        runs_with_cost = 0

        for run in runs:
            cost = None
            if "cost" in run.metadata:
                cost = run.metadata["cost"].get("total_cost") or run.metadata["cost"].get(
                    "totalCost"
                )

            usage = run.metadata.get("usage", {})
            input_tokens = usage.get("input_tokens", 0) or usage.get("inputTokens", 0)
            output_tokens = usage.get("output_tokens", 0) or usage.get("outputTokens", 0)

            if cost is not None:
                total_cost += cost
                runs_with_cost += 1

            total_input_tokens += input_tokens
            total_output_tokens += output_tokens

        avg_cost = total_cost / runs_with_cost if runs_with_cost > 0 else 0.0
        total_tokens = total_input_tokens + total_output_tokens

        return SummaryEvaluationResult(
            name=self.name,
            score=total_cost,
            metrics={
                "total_cost": total_cost,
                "average_cost": avg_cost,
                "total_input_tokens": total_input_tokens,
                "total_output_tokens": total_output_tokens,
                "total_tokens": total_tokens,
                "runs_with_cost": runs_with_cost,
                "total_runs": len(runs),
            },
            reasoning=f"Total cost: ${total_cost:.4f} across {runs_with_cost} runs (avg: ${avg_cost:.4f})",
        )


class LatencySummaryEvaluator(SummaryEvaluator):
    """
    Latency Summary Evaluator.

    Aggregates latency metrics across all runs.
    """

    def __init__(self):
        super().__init__("latency_summary", "Latency statistics across dataset")

    async def evaluate(self, runs: list[RunData]) -> SummaryEvaluationResult:
        """Calculate latency summary across runs."""
        latencies: list[float] = []

        for run in runs:
            latency = run.metadata.get("latency") or run.metadata.get("duration")
            if latency is not None and isinstance(latency, (int, float)):
                latencies.append(float(latency))

        if not latencies:
            return SummaryEvaluationResult(
                name=self.name, score=0.0, metrics={"count": 0}, reasoning="No latency data found"
            )

        sorted_latencies = sorted(latencies)
        mean = statistics.mean(latencies)
        median = statistics.median(latencies)
        min_lat = min(latencies)
        max_lat = max(latencies)

        return SummaryEvaluationResult(
            name=self.name,
            score=mean,
            metrics={
                "mean_latency": mean,
                "median_latency": median,
                "min_latency": min_lat,
                "max_latency": max_lat,
                "p50": sorted_latencies[int(len(sorted_latencies) * 0.50)],
                "p90": sorted_latencies[int(len(sorted_latencies) * 0.90)],
                "p95": sorted_latencies[int(len(sorted_latencies) * 0.95)],
                "p99": sorted_latencies[int(len(sorted_latencies) * 0.99)],
                "count": len(latencies),
            },
            reasoning=f"Mean latency: {mean:.2f}ms (p50: {median:.2f}ms, p95: {sorted_latencies[int(len(sorted_latencies) * 0.95)]:.2f}ms)",
        )


async def run_summary_evaluators(
    runs: list[RunData], evaluators: list[SummaryEvaluator | SummaryEvaluatorFunction]
) -> list[SummaryEvaluationResult]:
    """
    Run summary evaluators on a dataset.

    Args:
        runs: List of run data
        evaluators: List of summary evaluators

    Returns:
        List of summary evaluation results
    """
    results: list[SummaryEvaluationResult] = []

    for evaluator in evaluators:
        if callable(evaluator) and not isinstance(evaluator, SummaryEvaluator):
            # It's a function
            result = evaluator(runs)
        else:
            # It's a SummaryEvaluator instance
            result = await evaluator.evaluate(runs)

        if isinstance(result, list):
            results.extend(result)
        else:
            results.append(result)

    return results


def create_standard_summary_evaluators() -> list[SummaryEvaluator]:
    """
    Create standard summary evaluators for common use cases.

    Returns:
        List of standard summary evaluators
    """
    return [
        AccuracySummaryEvaluator(),
        AverageScoreSummaryEvaluator(),
        PassRateSummaryEvaluator(),
        CostSummaryEvaluator(),
        LatencySummaryEvaluator(),
    ]
