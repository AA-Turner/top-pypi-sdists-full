"""
Enhanced batch evaluation with concurrency control, progress tracking, and analytics
"""

import asyncio
import time
from collections.abc import Callable
from dataclasses import dataclass, field
from typing import Any, Protocol, TypeVar

from aigie.evaluation import EvaluationResult, Evaluator


@dataclass
class BatchProgress:
    """Progress information for batch evaluation"""

    completed: int
    total: int
    succeeded: int
    failed: int
    percentage: float
    current_case: str | None = None


@dataclass
class TestCaseResult:
    """Result of a single test case evaluation"""

    input: Any
    output: Any | None = None
    expected: Any | None = None
    evaluations: list[EvaluationResult] = field(default_factory=list)
    error: Exception | None = None
    duration: float = 0.0


@dataclass
class EvaluatorStatistics:
    """Statistics for a single evaluator"""

    average_score: float
    pass_rate: float
    total: int


@dataclass
class BatchStatistics:
    """Aggregated statistics for batch evaluation"""

    total: int
    succeeded: int
    failed: int
    average_score: float
    pass_rate: float
    average_duration: float
    total_duration: float
    by_evaluator: dict[str, EvaluatorStatistics] = field(default_factory=dict)


@dataclass
class BatchEvaluationResult:
    """Result of a batch evaluation"""

    results: list[TestCaseResult]
    statistics: BatchStatistics
    passed: list[TestCaseResult] = field(default_factory=list)
    failed: list[TestCaseResult] = field(default_factory=list)


class ProgressCallback(Protocol):
    """Protocol for progress callback"""

    def __call__(self, progress: BatchProgress) -> None: ...


T_Input = TypeVar("T_Input")
T_Output = TypeVar("T_Output")


class Semaphore:
    """Semaphore for concurrency control"""

    def __init__(self, permits: int):
        self._permits = permits
        self._semaphore = asyncio.Semaphore(permits)

    async def acquire(self, fn: Callable):
        """Acquire permit and execute function"""
        async with self._semaphore:
            return await fn()


async def enhanced_batch_evaluate(
    fn: Callable[[Any], Any],
    evaluators: list[Evaluator],
    test_cases: list[dict[str, Any]],
    concurrency: int = 10,
    on_progress: ProgressCallback | None = None,
    continue_on_error: bool = True,
    retries: int = 0,
    retry_delay: float = 1.0,
    tags: list[str] | None = None,
    metadata: dict[str, Any] | None = None,
) -> BatchEvaluationResult:
    """
    Enhanced batch evaluation with concurrency control and progress tracking

    Args:
        fn: Function to evaluate
        evaluators: List of evaluators to run
        test_cases: List of test cases with 'input', 'expected', and optional 'name'
        concurrency: Maximum number of concurrent evaluations (default: 10)
        on_progress: Progress callback function
        continue_on_error: Whether to continue on errors (default: True)
        retries: Number of retries for failed evaluations (default: 0)
        retry_delay: Delay between retries in seconds (default: 1.0)
        tags: Tags to apply to all evaluations
        metadata: Metadata to attach to all evaluations

    Returns:
        Batch evaluation result with statistics

    Example:
        >>> from aigie.batch_evaluation import enhanced_batch_evaluate
        >>> from aigie.evaluation import ExactMatchEvaluator
        >>>
        >>> async def my_agent(input: str) -> str:
        ...     return f"Processed: {input}"
        >>>
        >>> result = await enhanced_batch_evaluate(
        ...     my_agent,
        ...     [ExactMatchEvaluator()],
        ...     [
        ...         {'input': 'test 1', 'expected': 'output 1'},
        ...         {'input': 'test 2', 'expected': 'output 2'},
        ...     ],
        ...     concurrency=5,
        ...     on_progress=lambda p: print(f"Progress: {p.percentage}%")
        ... )
        >>>
        >>> print(f"Pass rate: {result.statistics.pass_rate}%")
        >>> print(f"Average score: {result.statistics.average_score}")
    """
    results: list[TestCaseResult] = []
    completed = 0
    succeeded = 0
    failed = 0

    def update_progress(current_case: str | None = None):
        """Update progress and call callback"""
        if on_progress:
            on_progress(
                BatchProgress(
                    completed=completed,
                    total=len(test_cases),
                    succeeded=succeeded,
                    failed=failed,
                    percentage=(completed / len(test_cases)) * 100,
                    current_case=current_case,
                )
            )

    # Create semaphore for concurrency control
    semaphore = Semaphore(concurrency)

    async def evaluate_test_case(test_case: dict[str, Any], index: int):
        """Evaluate a single test case"""
        nonlocal completed, succeeded, failed

        case_name = test_case.get("name", f"Test Case {index + 1}")
        update_progress(case_name)

        start_time = time.time()
        attempt = 0
        last_error: Exception | None = None

        while attempt <= retries:
            try:
                # Execute function
                input_data = test_case["input"]
                expected = test_case.get("expected")

                # Call function (handle both sync and async)
                if asyncio.iscoroutinefunction(fn):
                    output = await fn(input_data)
                else:
                    output = fn(input_data)

                # Run evaluators
                evaluation_results = []
                for evaluator in evaluators:
                    eval_result = await evaluator.evaluate(input_data, output, expected)
                    evaluation_results.append(eval_result)

                duration = time.time() - start_time

                results.append(
                    TestCaseResult(
                        input=input_data,
                        output=output,
                        expected=expected,
                        evaluations=evaluation_results,
                        duration=duration,
                    )
                )

                succeeded += 1
                completed += 1
                update_progress()
                return

            except Exception as error:
                last_error = error
                attempt += 1

                if attempt <= retries:
                    # Wait before retrying
                    await asyncio.sleep(retry_delay)

        # All retries failed
        duration = time.time() - start_time

        if continue_on_error:
            results.append(
                TestCaseResult(
                    input=test_case["input"],
                    expected=test_case.get("expected"),
                    evaluations=[],
                    error=last_error,
                    duration=duration,
                )
            )

            failed += 1
            completed += 1
            update_progress()
        else:
            raise last_error

    # Process test cases with concurrency control
    tasks = [
        semaphore.acquire(lambda tc=tc, i=i: evaluate_test_case(tc, i))
        for i, tc in enumerate(test_cases)
    ]

    await asyncio.gather(*tasks)

    # Calculate statistics
    statistics = _calculate_statistics(results, evaluators)

    # Separate passed and failed
    passed: list[TestCaseResult] = []
    failed_cases: list[TestCaseResult] = []

    for result in results:
        if result.error:
            failed_cases.append(result)
        elif all(e.passed for e in result.evaluations):
            passed.append(result)
        else:
            failed_cases.append(result)

    return BatchEvaluationResult(
        results=results, statistics=statistics, passed=passed, failed=failed_cases
    )


def _calculate_statistics(
    results: list[TestCaseResult], evaluators: list[Evaluator]
) -> BatchStatistics:
    """Calculate aggregated statistics from batch evaluation results"""
    total = len(results)
    succeeded = len([r for r in results if not r.error])
    failed = total - succeeded

    # Calculate average score and pass rate
    total_score = 0.0
    total_passed = 0
    total_duration = 0.0

    for result in results:
        total_duration += result.duration

        if not result.error and result.evaluations:
            avg_score = sum(e.score for e in result.evaluations) / len(result.evaluations)
            total_score += avg_score

            if all(e.passed for e in result.evaluations):
                total_passed += 1

    average_score = total_score / succeeded if succeeded > 0 else 0.0
    pass_rate = (total_passed / total) * 100 if total > 0 else 0.0
    average_duration = total_duration / total if total > 0 else 0.0

    # Calculate per-evaluator statistics
    by_evaluator: dict[str, EvaluatorStatistics] = {}

    for evaluator in evaluators:
        evaluator_results = [
            next((e for e in r.evaluations if e.name == evaluator.name), None)
            for r in results
            if not r.error
        ]
        evaluator_results = [e for e in evaluator_results if e is not None]

        if evaluator_results:
            avg_score = sum(e.score for e in evaluator_results) / len(evaluator_results)
            passed_count = len([e for e in evaluator_results if e.passed])
            rate = (passed_count / len(evaluator_results)) * 100

            by_evaluator[evaluator.name] = EvaluatorStatistics(
                average_score=avg_score, pass_rate=rate, total=len(evaluator_results)
            )

    return BatchStatistics(
        total=total,
        succeeded=succeeded,
        failed=failed,
        average_score=average_score,
        pass_rate=pass_rate,
        average_duration=average_duration,
        total_duration=total_duration,
        by_evaluator=by_evaluator,
    )


def generate_batch_report(result: BatchEvaluationResult) -> str:
    """
    Generate a summary report from batch evaluation results

    Args:
        result: Batch evaluation result

    Returns:
        Formatted report string

    Example:
        >>> result = await enhanced_batch_evaluate(...)
        >>> report = generate_batch_report(result)
        >>> print(report)
    """
    statistics = result.statistics

    report = "=== Batch Evaluation Report ===\n\n"

    # Overall statistics
    report += f"Total Test Cases: {statistics.total}\n"
    report += f"Succeeded: {statistics.succeeded}\n"
    report += f"Failed: {statistics.failed}\n"
    report += f"Pass Rate: {statistics.pass_rate:.2f}%\n"
    report += f"Average Score: {statistics.average_score:.3f}\n"
    report += f"Average Duration: {statistics.average_duration:.0f}ms\n"
    report += f"Total Duration: {statistics.total_duration:.0f}ms\n\n"

    # Per-evaluator statistics
    report += "--- Per-Evaluator Statistics ---\n"
    for name, stats in statistics.by_evaluator.items():
        report += f"\n{name}:\n"
        report += f"  Average Score: {stats.average_score:.3f}\n"
        report += f"  Pass Rate: {stats.pass_rate:.2f}%\n"
        report += f"  Total: {stats.total}\n"

    # Failed cases
    if result.failed:
        report += "\n--- Failed Test Cases ---\n"
        for index, test_case in enumerate(result.failed, 1):
            report += f"\n{index}. Input: {test_case.input}\n"
            if test_case.error:
                report += f"   Error: {test_case.error}\n"
            else:
                for evaluation in test_case.evaluations:
                    if not evaluation.passed:
                        report += f"   {evaluation.name}: {evaluation.reasoning}\n"

    return report


def export_batch_results(result: BatchEvaluationResult) -> str:
    """
    Export batch evaluation results to JSON

    Args:
        result: Batch evaluation result

    Returns:
        JSON string
    """
    import json

    return json.dumps(
        {
            "results": [
                {
                    "input": r.input,
                    "output": r.output,
                    "expected": r.expected,
                    "evaluations": [
                        {
                            "name": e.name,
                            "score": e.score,
                            "passed": e.passed,
                            "reasoning": e.reasoning,
                            "metadata": e.metadata,
                        }
                        for e in r.evaluations
                    ],
                    "error": str(r.error) if r.error else None,
                    "duration": r.duration,
                }
                for r in result.results
            ],
            "statistics": {
                "total": result.statistics.total,
                "succeeded": result.statistics.succeeded,
                "failed": result.statistics.failed,
                "average_score": result.statistics.average_score,
                "pass_rate": result.statistics.pass_rate,
                "average_duration": result.statistics.average_duration,
                "total_duration": result.statistics.total_duration,
                "by_evaluator": {
                    name: {
                        "average_score": stats.average_score,
                        "pass_rate": stats.pass_rate,
                        "total": stats.total,
                    }
                    for name, stats in result.statistics.by_evaluator.items()
                },
            },
        },
        indent=2,
    )


def export_batch_results_to_csv(result: BatchEvaluationResult, evaluator_names: list[str]) -> str:
    """
    Export batch evaluation results to CSV

    Args:
        result: Batch evaluation result
        evaluator_names: List of evaluator names for columns

    Returns:
        CSV string
    """
    import csv
    import io

    output = io.StringIO()
    writer = csv.writer(output)

    # Write headers
    headers = ["Input", "Output", "Expected", "Duration"] + evaluator_names + ["Passed", "Error"]
    writer.writerow(headers)

    # Write rows
    for r in result.results:
        row = [
            str(r.input),
            str(r.output) if r.output else "",
            str(r.expected) if r.expected else "",
            f"{r.duration:.2f}",
        ]

        # Add evaluator scores
        for name in evaluator_names:
            evaluation = next((e for e in r.evaluations if e.name == name), None)
            row.append(str(evaluation.score) if evaluation else "")

        # Add passed status
        row.append(str(all(e.passed for e in r.evaluations)))

        # Add error
        row.append(str(r.error) if r.error else "")

        writer.writerow(row)

    return output.getvalue()
