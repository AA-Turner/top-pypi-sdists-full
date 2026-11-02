"""Tests for condense_job_log()."""

from agentic_devtools.cli.ci.job_logs import condense_job_log


class TestCondenseJobLog:
    """Tests for stripping timestamps/noise and bounding job-log size."""

    def test_strips_rfc3339_timestamp_prefix(self) -> None:
        raw = "2026-06-23T10:00:00.1234567Z hello world"
        assert condense_job_log(raw) == "hello world"

    def test_strips_timestamp_without_fractional_seconds(self) -> None:
        raw = "2026-06-23T10:00:00Z plain line"
        assert condense_job_log(raw) == "plain line"

    def test_keeps_lines_without_timestamp_unchanged(self) -> None:
        raw = "no timestamp here"
        assert condense_job_log(raw) == "no timestamp here"

    def test_drops_passed_test_lines(self) -> None:
        raw = "tests/unit/test_foo.py::TestX::test_y PASSED\nError: boom"
        result = condense_job_log(raw)
        assert "PASSED" not in result
        assert "Error: boom" in result

    def test_drops_pytest_metadata_noise(self) -> None:
        raw = "platform linux -- Python 3.12\nactual failure line"
        result = condense_job_log(raw)
        assert "platform linux" not in result
        assert "actual failure line" in result

    def test_collapses_consecutive_blank_lines(self) -> None:
        raw = "first\n\n\n\nsecond"
        assert condense_job_log(raw) == "first\n\nsecond"

    def test_strips_leading_and_trailing_blank_lines(self) -> None:
        raw = "\n\ncontent line\n\n"
        assert condense_job_log(raw) == "content line"

    def test_truncates_when_exceeding_max_lines_keeps_tail(self) -> None:
        raw = "\n".join(f"line{i}" for i in range(50))
        result = condense_job_log(raw, max_lines=5)
        assert result.startswith("[… earlier output truncated …]")
        assert "line49" in result
        assert "line0\n" not in result

    def test_truncates_when_exceeding_max_chars_keeps_tail(self) -> None:
        raw = "\n".join(["x" * 100, "y" * 100, "TAIL_MARKER"])
        result = condense_job_log(raw, max_chars=20)
        assert result.startswith("[… earlier output truncated …]")
        assert "TAIL_MARKER" in result

    def test_no_truncation_marker_when_within_limits(self) -> None:
        raw = "short\noutput"
        result = condense_job_log(raw)
        assert "earlier output truncated" not in result
        assert result == "short\noutput"

    def test_empty_input_returns_empty(self) -> None:
        assert condense_job_log("") == ""

    def test_blank_only_input_returns_empty(self) -> None:
        assert condense_job_log("\n\n\n") == ""
