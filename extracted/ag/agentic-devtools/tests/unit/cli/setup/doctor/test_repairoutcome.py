"""Tests for RepairOutcome.applied field."""

from __future__ import annotations

from agentic_devtools.cli.setup.dependency_checker import DependencyStatus
from agentic_devtools.cli.setup.doctor import RepairOutcome
from agentic_devtools.cli.setup.fixloop import ErrorClass


class TestRepairOutcomeApplied:
    """RepairOutcome.applied field tracks whether mutation occurred."""

    def test_default_applied_is_true(self) -> None:
        """Default value of applied is True for backward compat."""
        dep = DependencyStatus(name="test", found=True, required=True)
        outcome = RepairOutcome(
            error_class=ErrorClass.MISSING_DEPENDENCY,
            dependency=dep,
            success=True,
        )
        assert outcome.applied is True

    def test_applied_false_when_set_explicitly(self) -> None:
        """applied can be set to False explicitly."""
        dep = DependencyStatus(name="test", found=True, required=True)
        outcome = RepairOutcome(
            error_class=ErrorClass.MISSING_DEPENDENCY,
            dependency=dep,
            success=True,
            applied=False,
        )
        assert outcome.applied is False

    def test_applied_true_when_set_explicitly(self) -> None:
        """applied can be set to True explicitly."""
        dep = DependencyStatus(name="test", found=True, required=True)
        outcome = RepairOutcome(
            error_class=ErrorClass.MISSING_DEPENDENCY,
            dependency=dep,
            success=True,
            applied=True,
        )
        assert outcome.applied is True

    def test_details_defaults_to_empty_dict(self) -> None:
        """details defaults to empty dict."""
        dep = DependencyStatus(name="test", found=True, required=True)
        outcome = RepairOutcome(
            error_class=ErrorClass.MISSING_DEPENDENCY,
            dependency=dep,
            success=True,
        )
        assert outcome.details == {}

    def test_details_isolation(self) -> None:
        """Each RepairOutcome has its own details dict."""
        dep = DependencyStatus(name="test", found=True, required=True)
        o1 = RepairOutcome(error_class=ErrorClass.MISSING_DEPENDENCY, dependency=dep, success=True)
        o2 = RepairOutcome(error_class=ErrorClass.MISSING_DEPENDENCY, dependency=dep, success=True)
        o1.details["key"] = "val"
        assert o2.details == {}
