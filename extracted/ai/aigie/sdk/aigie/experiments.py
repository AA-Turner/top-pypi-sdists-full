"""
Experiments API for A/B testing and variant comparison

Enables running experiments with multiple variants, comparing results,
and selecting winners based on metrics
"""

import asyncio
import time
from collections.abc import Callable
from dataclasses import dataclass, field
from typing import Any, Generic, Protocol, TypeVar

from aigie.evaluation import EvaluationResult, Evaluator

T_Input = TypeVar("T_Input")
T_Output = TypeVar("T_Output")
T_Config = TypeVar("T_Config")


@dataclass
class ExperimentVariant(Generic[T_Config]):
    """Experiment variant configuration"""

    name: str
    config: T_Config
    description: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class VariantResult(Generic[T_Input, T_Output]):
    """Result from a single variant run"""

    variant_name: str
    input: T_Input
    output: T_Output | None = None
    evaluations: list[EvaluationResult] = field(default_factory=list)
    duration: float = 0.0
    error: Exception | None = None


@dataclass
class VariantStatistics:
    """Aggregated statistics for a variant"""

    variant_name: str
    total_runs: int
    success_rate: float
    average_score: float
    average_duration: float
    error_rate: float
    evaluator_scores: dict[str, float] = field(default_factory=dict)


@dataclass
class WinnerInfo:
    """Information about experiment winner"""

    variant_name: str
    reason: str
    confidence: float


@dataclass
class ExperimentResult(Generic[T_Input, T_Output]):
    """Experiment result with all variants"""

    experiment_name: str
    variants: list[VariantStatistics]
    winner: WinnerInfo | None = None
    results: list[VariantResult[T_Input, T_Output]] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)


class CustomSelector(Protocol):
    """Protocol for custom winner selection function"""

    def __call__(self, variants: list[VariantStatistics]) -> WinnerInfo: ...


class Semaphore:
    """Semaphore for concurrency control"""

    def __init__(self, permits: int):
        self._permits = permits
        self._semaphore = asyncio.Semaphore(permits)

    async def acquire(self, fn: Callable):
        """Acquire permit and execute function"""
        async with self._semaphore:
            return await fn()


class ExperimentsClient:
    """
    Experiments client for managing A/B tests

    Example:
        >>> from aigie.experiments import ExperimentsClient, ExperimentVariant
        >>>
        >>> experiments = ExperimentsClient()
        >>>
        >>> # Define variants
        >>> variants = [
        ...     ExperimentVariant(
        ...         name='gpt-4',
        ...         config={'model': 'gpt-4', 'temperature': 0.7}
        ...     ),
        ...     ExperimentVariant(
        ...         name='gpt-3.5',
        ...         config={'model': 'gpt-3.5-turbo', 'temperature': 0.7}
        ...     ),
        ... ]
        >>>
        >>> # Run experiment
        >>> result = await experiments.run(
        ...     'model-comparison',
        ...     variants,
        ...     lambda variant, input: generate_text(variant.config, input),
        ...     [{'input': 'test prompt'}]
        ... )
        >>>
        >>> print(f"Winner: {result.winner.variant_name}")
    """

    async def run(
        self,
        experiment_name: str,
        variants: list[ExperimentVariant],
        fn: Callable[[ExperimentVariant, Any], Any],
        test_cases: list[dict[str, Any]],
        evaluators: list[Evaluator] | None = None,
        concurrency: int = 5,
        selection_strategy: str = "highest_score",
        custom_selector: CustomSelector | None = None,
        confidence_threshold: float = 0.8,
        track_in_aigie: bool = True,
    ) -> ExperimentResult:
        """
        Run an experiment with multiple variants

        Args:
            experiment_name: Name of the experiment
            variants: List of variants to test
            fn: Function that takes a variant and input and returns output
            test_cases: Test cases to run for each variant
            evaluators: Evaluators to use for comparing variants
            concurrency: Maximum number of concurrent runs (default: 5)
            selection_strategy: Winner selection strategy (default: 'highest_score')
            custom_selector: Custom selection function (required if strategy is 'custom')
            confidence_threshold: Minimum confidence for winner (0-1, default: 0.8)
            track_in_aigie: Whether to track experiment in Aigie (default: True)

        Returns:
            Experiment result with statistics and winner
        """
        evaluators = evaluators or []

        # Import Aigie client
        from aigie.client import get_aigie

        aigie = get_aigie() if track_in_aigie else None
        experiment_trace_id: str | None = None

        # Create experiment trace
        if aigie and aigie._enabled:
            import uuid

            experiment_trace_id = str(uuid.uuid4())

            await aigie._send_trace(
                {
                    "id": experiment_trace_id,
                    "name": f"experiment:{experiment_name}",
                    "type": "chain",
                    "status": "pending",
                    "tags": ["experiment", "ab-test"],
                    "metadata": {
                        "experimentName": experiment_name,
                        "variants": [v.name for v in variants],
                        "testCases": len(test_cases),
                    },
                    "startTime": time.time(),
                    "createdAt": time.time(),
                }
            )

        try:
            all_results: list[VariantResult] = []

            # Run all variant+testCase combinations
            semaphore = Semaphore(concurrency)
            tasks = []

            for variant in variants:
                for test_case in test_cases:

                    async def run_variant_test(v=variant, tc=test_case):
                        start_time = time.time()

                        try:
                            # Execute function
                            input_data = tc["input"]
                            expected = tc.get("expected")

                            # Call function (handle both sync and async)
                            if asyncio.iscoroutinefunction(fn):
                                output = await fn(v, input_data)
                            else:
                                output = fn(v, input_data)

                            duration = time.time() - start_time

                            # Run evaluators
                            evaluations = []
                            for evaluator in evaluators:
                                eval_result = await evaluator.evaluate(input_data, output, expected)
                                evaluations.append(eval_result)

                            all_results.append(
                                VariantResult(
                                    variant_name=v.name,
                                    input=input_data,
                                    output=output,
                                    evaluations=evaluations,
                                    duration=duration,
                                )
                            )

                        except Exception as error:
                            duration = time.time() - start_time

                            all_results.append(
                                VariantResult(
                                    variant_name=v.name,
                                    input=tc["input"],
                                    evaluations=[],
                                    duration=duration,
                                    error=error,
                                )
                            )

                    tasks.append(semaphore.acquire(run_variant_test))

            await asyncio.gather(*tasks)

            # Calculate statistics for each variant
            variant_stats = self._calculate_variant_statistics(all_results, variants, evaluators)

            # Select winner
            winner: WinnerInfo | None = None

            if selection_strategy == "custom" and custom_selector:
                winner = custom_selector(variant_stats)
            else:
                winner = self._select_winner(
                    variant_stats, selection_strategy, confidence_threshold
                )

            result = ExperimentResult(
                experiment_name=experiment_name,
                variants=variant_stats,
                winner=winner,
                results=all_results,
                metadata={
                    "testCases": len(test_cases),
                    "variantCount": len(variants),
                    "evaluatorCount": len(evaluators),
                },
            )

            # Update experiment trace
            if experiment_trace_id and aigie and aigie._enabled:
                await aigie._update_trace(
                    experiment_trace_id,
                    {
                        "status": "success",
                        "output": {
                            "winner": winner.variant_name if winner else None,
                            "variants": [
                                {
                                    "name": v.variant_name,
                                    "score": v.average_score,
                                    "duration": v.average_duration,
                                }
                                for v in variant_stats
                            ],
                        },
                        "endTime": time.time(),
                    },
                )

            return result

        except Exception as error:
            # Update experiment trace with error
            if experiment_trace_id and aigie and aigie._enabled:
                await aigie._update_trace(
                    experiment_trace_id,
                    {
                        "status": "failed",
                        "errorMessage": str(error),
                        "endTime": time.time(),
                    },
                )

            raise

    def _calculate_variant_statistics(
        self,
        results: list[VariantResult],
        variants: list[ExperimentVariant],
        evaluators: list[Evaluator],
    ) -> list[VariantStatistics]:
        """Calculate statistics for each variant"""
        stats = []

        for variant in variants:
            variant_results = [r for r in results if r.variant_name == variant.name]

            total_runs = len(variant_results)
            successful_runs = [r for r in variant_results if not r.error]
            success_rate = (len(successful_runs) / total_runs) * 100 if total_runs > 0 else 0
            error_rate = (
                ((total_runs - len(successful_runs)) / total_runs) * 100 if total_runs > 0 else 0
            )

            # Calculate average score across all evaluators
            total_score = 0.0
            score_count = 0

            evaluator_scores: dict[str, float] = {}

            for run in successful_runs:
                for evaluation in run.evaluations:
                    total_score += evaluation.score
                    score_count += 1

                    if evaluation.name not in evaluator_scores:
                        evaluator_scores[evaluation.name] = 0.0

                    evaluator_scores[evaluation.name] += evaluation.score

            # Average evaluator scores
            for name in evaluator_scores:
                evaluator_scores[name] /= len(successful_runs) or 1

            average_score = total_score / score_count if score_count > 0 else 0.0

            # Calculate average duration
            total_duration = sum(r.duration for r in variant_results)
            average_duration = total_duration / total_runs if total_runs > 0 else 0.0

            stats.append(
                VariantStatistics(
                    variant_name=variant.name,
                    total_runs=total_runs,
                    success_rate=success_rate,
                    average_score=average_score,
                    average_duration=average_duration,
                    error_rate=error_rate,
                    evaluator_scores=evaluator_scores,
                )
            )

        return stats

    def _select_winner(
        self,
        variants: list[VariantStatistics],
        strategy: str,
        confidence_threshold: float,
    ) -> WinnerInfo | None:
        """Select winner based on strategy"""
        if not variants:
            return None

        # Sort variants based on strategy
        sorted_variants = sorted(
            variants,
            key=lambda v: v.average_score if strategy == "highest_score" else -v.average_duration,
            reverse=True,
        )

        winner = sorted_variants[0]
        runner_up = sorted_variants[1] if len(sorted_variants) > 1 else None

        # Calculate confidence based on difference from runner-up
        confidence = 1.0
        reason = ""

        if strategy == "highest_score":
            if runner_up:
                diff = winner.average_score - runner_up.average_score
                confidence = (
                    min(1.0, diff / winner.average_score) if winner.average_score > 0 else 0.0
                )
            reason = f"Highest average score: {winner.average_score:.3f}"

        elif strategy == "lowest_duration":
            if runner_up:
                diff = runner_up.average_duration - winner.average_duration
                confidence = (
                    min(1.0, diff / runner_up.average_duration)
                    if runner_up.average_duration > 0
                    else 0.0
                )
            reason = f"Lowest average duration: {winner.average_duration:.0f}ms"

        # Only return winner if confidence exceeds threshold
        if confidence >= confidence_threshold:
            return WinnerInfo(
                variant_name=winner.variant_name, reason=reason, confidence=confidence
            )

        return None

    async def compare(
        self,
        experiment_name: str,
        variant_a: ExperimentVariant,
        variant_b: ExperimentVariant,
        fn: Callable[[ExperimentVariant, Any], Any],
        test_cases: list[dict[str, Any]],
        **kwargs,
    ) -> ExperimentResult:
        """
        Compare two specific variants

        Args:
            experiment_name: Name of the experiment
            variant_a: First variant to compare
            variant_b: Second variant to compare
            fn: Function that takes a variant and input and returns output
            test_cases: Test cases to run for each variant
            **kwargs: Additional options passed to run()

        Returns:
            Experiment result comparing the two variants
        """
        return await self.run(experiment_name, [variant_a, variant_b], fn, test_cases, **kwargs)


def create_experiments_client() -> ExperimentsClient:
    """Create an experiments client"""
    return ExperimentsClient()


def generate_experiment_report(result: ExperimentResult) -> str:
    """
    Generate a comparison report from experiment results

    Args:
        result: Experiment result

    Returns:
        Formatted report string

    Example:
        >>> result = await experiments.run(...)
        >>> report = generate_experiment_report(result)
        >>> print(report)
    """
    report = f"=== Experiment Report: {result.experiment_name} ===\n\n"

    # Winner
    if result.winner:
        report += f"Winner: {result.winner.variant_name}\n"
        report += f"Reason: {result.winner.reason}\n"
        report += f"Confidence: {result.winner.confidence * 100:.1f}%\n\n"
    else:
        report += "No clear winner (confidence threshold not met)\n\n"

    # Variant statistics
    report += "--- Variant Statistics ---\n"

    for variant in result.variants:
        report += f"\n{variant.variant_name}:\n"
        report += f"  Total Runs: {variant.total_runs}\n"
        report += f"  Success Rate: {variant.success_rate:.2f}%\n"
        report += f"  Average Score: {variant.average_score:.3f}\n"
        report += f"  Average Duration: {variant.average_duration:.0f}ms\n"
        report += f"  Error Rate: {variant.error_rate:.2f}%\n"

        if variant.evaluator_scores:
            report += "  Evaluator Scores:\n"
            for name, score in variant.evaluator_scores.items():
                report += f"    {name}: {score:.3f}\n"

    return report
