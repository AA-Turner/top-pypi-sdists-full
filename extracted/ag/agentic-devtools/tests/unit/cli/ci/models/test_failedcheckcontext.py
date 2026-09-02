"""Tests for FailedCheckContext dataclass."""

from agentic_devtools.cli.ci.models import FailedCheckContext, FailedStepLog


class TestFailedCheckContext:
    """Tests for the FailedCheckContext dataclass."""

    def test_holds_display_name_and_step_logs(self) -> None:
        ctx = FailedCheckContext(
            display_name="WF / Job (pull_request)",
            step_logs=(FailedStepLog(step_name="step", condensed_log="log"),),
        )
        assert ctx.display_name == "WF / Job (pull_request)"
        assert len(ctx.step_logs) == 1
        assert ctx.step_logs[0].step_name == "step"

    def test_empty_step_logs_means_link_only(self) -> None:
        ctx = FailedCheckContext(display_name="", step_logs=())
        assert ctx.display_name == ""
        assert ctx.step_logs == ()

    def test_is_frozen(self) -> None:
        ctx = FailedCheckContext(display_name="x", step_logs=())
        try:
            ctx.display_name = "y"  # type: ignore[misc]
            raise AssertionError("Should have raised FrozenInstanceError")
        except AttributeError:
            pass
