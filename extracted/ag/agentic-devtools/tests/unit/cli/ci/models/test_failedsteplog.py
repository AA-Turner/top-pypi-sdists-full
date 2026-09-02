"""Tests for FailedStepLog dataclass."""

from agentic_devtools.cli.ci.models import FailedStepLog


class TestFailedStepLog:
    """Tests for the FailedStepLog dataclass."""

    def test_holds_step_name_and_log(self) -> None:
        step = FailedStepLog(step_name="Run tests", condensed_log="Error: boom")
        assert step.step_name == "Run tests"
        assert step.condensed_log == "Error: boom"

    def test_empty_step_name_means_whole_job(self) -> None:
        step = FailedStepLog(step_name="", condensed_log="whole job log")
        assert step.step_name == ""
        assert step.condensed_log == "whole job log"

    def test_is_frozen(self) -> None:
        step = FailedStepLog(step_name="x", condensed_log="y")
        try:
            step.step_name = "z"  # type: ignore[misc]
            raise AssertionError("Should have raised FrozenInstanceError")
        except AttributeError:
            pass
