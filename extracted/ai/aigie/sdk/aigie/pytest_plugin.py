"""
Pytest plugin for Aigie SDK.

Enables native pytest integration for AI evaluation testing.

Usage:
    @pytest.mark.aigie(evaluators=[AnswerRelevancyEvaluator()])
    def test_qa_system(aigie_test_case):
        result = my_qa_system(aigie_test_case.input)
        aigie_test_case.actual_output = result
        aigie_assert(aigie_test_case)

    # Run: pytest --aigie
"""

from dataclasses import dataclass, field
from typing import Any

import pytest

from .evaluation import EvaluationResult
from .evaluation.scorers import BaseScorer as Evaluator


@dataclass
class AigieTestCase:
    """Test case for Aigie evaluation."""

    input: Any
    """Input to the system"""

    actual_output: Any | None = None
    """Actual output from the system"""

    expected_output: Any | None = None
    """Expected output"""

    context: dict[str, Any] = field(default_factory=dict)
    """Additional context"""

    evaluators: list[Evaluator] = field(default_factory=list)
    """Evaluators to run"""

    metadata: dict[str, Any] = field(default_factory=dict)
    """Test metadata"""


class AigiePlugin:
    """Pytest plugin for Aigie."""

    def __init__(self):
        self.test_results: list[dict[str, Any]] = []
        self.enabled = False

    def pytest_addoption(self, parser):
        """Add command-line options."""
        group = parser.getgroup("aigie")
        group.addoption(
            "--aigie", action="store_true", default=False, help="Enable Aigie evaluation"
        )
        group.addoption(
            "--aigie-verbose", action="store_true", default=False, help="Verbose Aigie output"
        )

    def pytest_configure(self, config):
        """Configure pytest."""
        self.enabled = config.getoption("--aigie")
        self.verbose = config.getoption("--aigie-verbose", False)

        # Register marker
        config.addinivalue_line(
            "markers", "aigie(evaluators=None): mark test as Aigie evaluation test"
        )

    def pytest_collection_modifyitems(self, config, items):
        """Modify collected items."""
        if not self.enabled:
            skip_aigie = pytest.mark.skip(reason="Need --aigie option to run")
            for item in items:
                if "aigie" in item.keywords:
                    item.add_marker(skip_aigie)

    @pytest.fixture
    def aigie_test_case(self, request):
        """Fixture to provide test case."""
        # Get evaluators from marker
        marker = request.node.get_closest_marker("aigie")
        evaluators = []

        if marker:
            evaluators = marker.kwargs.get("evaluators", [])

        return AigieTestCase(input=None, evaluators=evaluators)

    def pytest_terminal_summary(self, terminalreporter, exitstatus, config):
        """Add summary to terminal output."""
        if not self.enabled or not self.test_results:
            return

        terminalreporter.section("Aigie Evaluation Summary")

        total_tests = len(self.test_results)
        total_evaluations = sum(len(r["results"]) for r in self.test_results)
        passed = sum(
            1
            for r in self.test_results
            if all(res.metadata.get("passed", True) for res in r["results"])
        )
        failed = total_tests - passed

        terminalreporter.write_line(f"Total tests: {total_tests}")
        terminalreporter.write_line(f"Total evaluations: {total_evaluations}")
        terminalreporter.write_line(f"Passed: {passed}")
        terminalreporter.write_line(f"Failed: {failed}")

        if self.verbose:
            for result in self.test_results:
                terminalreporter.write_line(f"\nTest: {result['test_name']}")
                for eval_result in result["results"]:
                    status = "✓" if eval_result.metadata.get("passed", True) else "✗"
                    terminalreporter.write_line(
                        f"  {status} Score: {eval_result.score:.2f} - {eval_result.explanation}"
                    )


# Global plugin instance
_plugin = AigiePlugin()


def pytest_addoption(parser):
    """Add command-line options."""
    _plugin.pytest_addoption(parser)


def pytest_configure(config):
    """Configure pytest."""
    _plugin.pytest_configure(config)


def pytest_collection_modifyitems(config, items):
    """Modify collected items."""
    _plugin.pytest_collection_modifyitems(config, items)


@pytest.fixture
def aigie_test_case(request):
    """Fixture to provide test case."""
    return _plugin.aigie_test_case(request)


def pytest_terminal_summary(terminalreporter, exitstatus, config):
    """Add summary to terminal output."""
    _plugin.pytest_terminal_summary(terminalreporter, exitstatus, config)


async def aigie_assert(test_case: AigieTestCase, fail_on_low_score: bool = True):
    """
    Assert that test case passes all evaluations.

    Args:
        test_case: Test case to evaluate
        fail_on_low_score: Fail if any evaluator score is low

    Raises:
        AssertionError: If evaluation fails
    """
    if not test_case.evaluators:
        return

    results: list[EvaluationResult] = []

    for evaluator in test_case.evaluators:
        result = await evaluator.evaluate(
            test_case.expected_output, test_case.actual_output, test_case.context
        )
        results.append(result)

    # Store results for summary
    _plugin.test_results.append(
        {
            "test_name": "test",  # TODO: Get actual test name from pytest
            "results": results,
        }
    )

    # Check if any evaluations failed
    if fail_on_low_score:
        failed = [r for r in results if not r.metadata.get("passed", True)]
        if failed:
            messages = [f"{r.score_type.value}: {r.score:.2f} - {r.explanation}" for r in failed]
            raise AssertionError("Aigie evaluation failed:\n" + "\n".join(messages))


def assert_test(test_case: AigieTestCase, evaluators: list[Evaluator] | None = None):
    """
    Synchronous wrapper for aigie_assert.

    Args:
        test_case: Test case to evaluate
        evaluators: Evaluators to run (overrides test_case.evaluators)
    """
    import asyncio

    if evaluators:
        test_case.evaluators = evaluators

    # Run async assertion
    loop = asyncio.get_event_loop()
    if loop.is_running():
        # Already in async context
        raise RuntimeError("Use aigie_assert() in async context")
    loop.run_until_complete(aigie_assert(test_case))
