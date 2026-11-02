"""Tests for parse_failed_step_logs()."""

from agentic_devtools.cli.ci.job_logs import parse_failed_step_logs
from agentic_devtools.cli.ci.models import FailedStepLog


class TestParseFailedStepLogs:
    """Tests for parsing ``gh run view --log-failed`` output into per-step logs."""

    def test_empty_input_returns_empty_list(self) -> None:
        assert parse_failed_step_logs("") == []

    def test_single_step(self) -> None:
        raw = "job\tRun tests\tError: boom"
        result = parse_failed_step_logs(raw)
        assert result == [FailedStepLog(step_name="Run tests", condensed_log="Error: boom")]

    def test_multiple_steps_preserve_first_appearance_order(self) -> None:
        raw = "\n".join(
            [
                "job\tStep A\tline a1",
                "job\tStep A\tline a2",
                "job\tStep B\tline b1",
            ]
        )
        result = parse_failed_step_logs(raw)
        assert [s.step_name for s in result] == ["Step A", "Step B"]
        assert result[0].condensed_log == "line a1\nline a2"
        assert result[1].condensed_log == "line b1"

    def test_repeated_step_name_merges_preserving_first_order(self) -> None:
        raw = "\n".join(
            [
                "job\tStep A\ta1",
                "job\tStep B\tb1",
                "job\tStep A\ta2",
            ]
        )
        result = parse_failed_step_logs(raw)
        # Step A keeps its first-appearance position; its lines are merged.
        assert [s.step_name for s in result] == ["Step A", "Step B"]
        assert result[0].condensed_log == "a1\na2"
        assert result[1].condensed_log == "b1"

    def test_continuation_line_attaches_to_current_step(self) -> None:
        raw = "\n".join(
            [
                "job\tStep A\tfirst line",
                "second line with no tabs",
            ]
        )
        result = parse_failed_step_logs(raw)
        assert len(result) == 1
        assert result[0].step_name == "Step A"
        assert result[0].condensed_log == "first line\nsecond line with no tabs"

    def test_leading_line_without_tabs_is_dropped(self) -> None:
        raw = "\n".join(
            [
                "noise before any step",
                "job\tStep A\treal content",
            ]
        )
        result = parse_failed_step_logs(raw)
        assert len(result) == 1
        assert result[0].step_name == "Step A"
        assert result[0].condensed_log == "real content"

    def test_content_may_contain_tabs(self) -> None:
        raw = "job\tStep A\tcol1\tcol2"
        result = parse_failed_step_logs(raw)
        assert result[0].condensed_log == "col1\tcol2"

    def test_unknown_step_treated_as_normal_step(self) -> None:
        raw = "job\tUNKNOWN STEP\tdangling log"
        result = parse_failed_step_logs(raw)
        assert result == [FailedStepLog(step_name="UNKNOWN STEP", condensed_log="dangling log")]
