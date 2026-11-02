"""Tests for format_run_summary function."""

from unittest.mock import MagicMock

from agentic_devtools.orchestration.observability_summary import format_run_summary


def _make_run(
    *,
    duration_ms: int | float | None = 5000,
    node_success: int = 3,
    node_failure: int = 0,
    node_skipped: int = 0,
    tool_call_count: int = 0,
    tool_failures: int = 0,
    total_tool_duration_ms: float = 0.0,
    llm_call_count: int = 0,
    llm_calls_without_tokens: int = 0,
    total_input_tokens: int = 0,
    total_output_tokens: int = 0,
    total_estimated_cost: float | None = None,
    per_model_stats: dict | None = None,
    errors: list | None = None,
) -> MagicMock:
    run = MagicMock()
    run.total_duration_ms = duration_ms
    run.node_success = node_success
    run.node_failure = node_failure
    run.node_skipped = node_skipped
    run.tool_call_count = tool_call_count
    run.tool_failures = tool_failures
    run.total_tool_duration_ms = total_tool_duration_ms
    run.llm_call_count = llm_call_count
    run.llm_calls_without_tokens = llm_calls_without_tokens
    run.total_input_tokens = total_input_tokens
    run.total_output_tokens = total_output_tokens
    run.total_estimated_cost = total_estimated_cost
    run.per_model_stats = per_model_stats or {}
    run.errors = errors or []
    return run


class TestFormatRunSummary:
    """Tests for format_run_summary."""

    def test_successful_run_summary(self) -> None:
        run = _make_run(node_success=5)
        summary = format_run_summary(run)
        assert "5 success" in summary
        assert "Workflow Run Summary" in summary

    def test_duration_seconds_format(self) -> None:
        run = _make_run(duration_ms=45000)
        summary = format_run_summary(run)
        assert "45.0s" in summary

    def test_duration_minutes_format(self) -> None:
        run = _make_run(duration_ms=90000)
        summary = format_run_summary(run)
        assert "1m 30s" in summary

    def test_duration_minutes_format_floors_seconds_component(self) -> None:
        run = _make_run(duration_ms=119999)
        summary = format_run_summary(run)
        assert "1m 59s" in summary

    def test_duration_omitted_when_missing(self) -> None:
        run = _make_run(duration_ms=None)
        summary = format_run_summary(run)
        assert "Duration:" not in summary

    def test_partial_failure_summary(self) -> None:
        run = _make_run(
            node_success=3,
            node_failure=1,
            node_skipped=1,
            errors=[
                {
                    "node_name": "analyze",
                    "error_class": "transient",
                    "message": "Connection timeout",
                }
            ],
        )
        summary = format_run_summary(run)
        assert "3 success" in summary
        assert "1 failed" in summary
        assert "1 skipped" in summary
        assert "Errors (1)" in summary
        assert "[transient]" in summary

    def test_llm_call_stats(self) -> None:
        run = _make_run(
            llm_call_count=3,
            total_input_tokens=12345,
            total_output_tokens=6789,
            total_estimated_cost=0.42,
        )
        summary = format_run_summary(run)
        assert "LLM calls: 3" in summary
        assert "12,345 input" in summary
        assert "6,789 output" in summary
        assert "$0.42" in summary

    def test_tool_call_stats(self) -> None:
        run = _make_run(
            tool_call_count=3,
            tool_failures=1,
            total_tool_duration_ms=2500.0,
        )
        summary = format_run_summary(run)
        assert "Tools: 3 calls, 1 failed, 2.5s total" in summary

    def test_tool_call_stats_without_failures(self) -> None:
        run = _make_run(
            tool_call_count=2,
            tool_failures=0,
            total_tool_duration_ms=500.0,
        )
        summary = format_run_summary(run)
        assert "Tools: 2 calls, 0.5s total" in summary

    def test_lower_bound_note_when_calls_excluded(self) -> None:
        run = _make_run(
            llm_call_count=3,
            llm_calls_without_tokens=1,
            total_input_tokens=10000,
            total_output_tokens=5000,
            total_estimated_cost=0.30,
        )
        summary = format_run_summary(run)
        assert "lower bound" in summary
        assert "1 call excluded" in summary

    def test_multiple_models_breakdown(self) -> None:
        run = _make_run(
            llm_call_count=4,
            total_input_tokens=5000,
            total_output_tokens=2000,
            total_estimated_cost=0.50,
            per_model_stats={
                "gpt-4o": {"calls": 2, "input_tokens": 3000, "output_tokens": 1000, "cost": 0.40},
                "gpt-4o-mini": {"calls": 2, "input_tokens": 2000, "output_tokens": 1000, "cost": 0.10},
            },
        )
        summary = format_run_summary(run)
        assert "Per-model breakdown" in summary
        assert "gpt-4o:" in summary
        assert "gpt-4o-mini:" in summary

    def test_multiple_models_breakdown_renders_zero_cost(self) -> None:
        run = _make_run(
            llm_call_count=2,
            total_input_tokens=5000,
            total_output_tokens=2000,
            total_estimated_cost=0.10,
            per_model_stats={
                "free-model": {"calls": 1, "input_tokens": 0, "output_tokens": 0, "cost": 0.0},
                "paid-model": {"calls": 1, "input_tokens": 5000, "output_tokens": 2000, "cost": 0.10},
            },
        )
        summary = format_run_summary(run)
        assert "free-model: 1 calls, 0 in / 0 out, cost=$0.0000" in summary

    def test_multiple_models_breakdown_handles_mixed_key_types(self) -> None:
        """Mixed key types in per_model_stats do not crash sorting/rendering."""
        run = _make_run(
            llm_call_count=2,
            total_input_tokens=5000,
            total_output_tokens=2000,
            total_estimated_cost=0.10,
            per_model_stats={
                "gpt-4o": {"calls": 1, "input_tokens": 3000, "output_tokens": 1000, "cost": 0.08},
                42: {"calls": 1, "input_tokens": 2000, "output_tokens": 1000, "cost": 0.02},
            },
        )
        summary = format_run_summary(run)
        assert "Per-model breakdown" in summary
        assert "gpt-4o:" in summary
        assert "42:" in summary

    def test_fits_80_columns(self) -> None:
        run = _make_run(
            node_success=10,
            node_failure=2,
            llm_call_count=5,
            total_input_tokens=50000,
            total_output_tokens=25000,
            total_estimated_cost=1.50,
            errors=[
                {
                    "node_name": "very_long_node_name_that_might_overflow",
                    "error_class": "permanent",
                    "message": "A" * 200,
                }
            ],
        )
        summary = format_run_summary(run)
        for line in summary.split("\n"):
            assert len(line) <= 80, f"Line too long ({len(line)} chars): {line!r}"

    def test_error_long_prefix_clamped(self) -> None:
        """Very long node_name + error_class combination doesn't exceed 80 cols."""
        run = _make_run(
            node_failure=1,
            errors=[
                {
                    "node_name": "n" * 55,
                    "error_class": "e" * 20,
                    "message": "some message",
                }
            ],
        )
        summary = format_run_summary(run)
        for line in summary.split("\n"):
            assert len(line) <= 80, f"Line too long ({len(line)} chars): {line!r}"

    def test_error_tiny_budget_message_hard_clamped(self) -> None:
        """When prefix leaves 1–3 chars, message is sliced without '...' suffix."""
        # "e"*20 + "n"*49 → prefix len 76, available=2 (0 < 2 <= 3)
        run = _make_run(
            node_failure=1,
            errors=[
                {
                    "node_name": "n" * 49,
                    "error_class": "e" * 20,
                    "message": "Hello world",
                }
            ],
        )
        summary = format_run_summary(run)
        for line in summary.split("\n"):
            assert len(line) <= 80, f"Line too long ({len(line)} chars): {line!r}"

    def test_error_none_values_handled(self) -> None:
        """None node_name / error_class / message values don't crash the formatter."""
        run = _make_run(
            node_failure=1,
            errors=[
                {
                    "node_name": None,
                    "error_class": None,
                    "message": None,
                }
            ],
        )
        # Should not raise; summary should include an Errors section
        summary = format_run_summary(run)
        assert "Errors (1)" in summary

    def test_error_message_newlines_are_normalized(self) -> None:
        """Embedded newlines in error messages are normalized to one rendered line."""
        run = _make_run(
            node_failure=1,
            errors=[
                {
                    "node_name": "node",
                    "error_class": "permanent",
                    "message": "first line\nsecond line",
                }
            ],
        )
        summary = format_run_summary(run)
        assert "first line second line" in summary
        assert "first line\nsecond line" not in summary
        for line in summary.split("\n"):
            assert len(line) <= 80, f"Line too long ({len(line)} chars): {line!r}"

    def test_no_llm_calls_omits_section(self) -> None:
        run = _make_run(llm_call_count=0)
        summary = format_run_summary(run)
        assert "LLM calls" not in summary
        assert "Tokens" not in summary

    def test_no_nodes_shows_none(self) -> None:
        """When no nodes executed, shows 'none' detail."""
        run = _make_run(node_success=0, node_failure=0, node_skipped=0)
        summary = format_run_summary(run)
        assert "0 executed (none)" in summary

    def test_llm_calls_with_zero_cost(self) -> None:
        """When cost is 0.0, cost line is omitted."""
        run = _make_run(
            llm_call_count=1,
            total_input_tokens=100,
            total_output_tokens=50,
            total_estimated_cost=0.0,
        )
        summary = format_run_summary(run)
        assert "Estimated cost" not in summary

    def test_llm_calls_with_none_cost(self) -> None:
        """When cost is None, cost line is omitted."""
        run = _make_run(
            llm_call_count=1,
            total_input_tokens=100,
            total_output_tokens=50,
            total_estimated_cost=None,
        )
        summary = format_run_summary(run)
        assert "Estimated cost" not in summary

    def test_per_model_long_name_clamped_to_80_columns(self) -> None:
        """Per-model breakdown lines with very long model names are clamped to 80 cols."""
        long_model_name = "a-very-long-model-name-that-would-push-the-line-past-eighty-columns-easily"
        run = _make_run(
            llm_call_count=2,
            total_input_tokens=1000,
            total_output_tokens=500,
            total_estimated_cost=0.10,
            per_model_stats={
                long_model_name: {"calls": 1, "input_tokens": 500, "output_tokens": 250, "cost": 0.05},
                "short": {"calls": 1, "input_tokens": 500, "output_tokens": 250, "cost": 0.05},
            },
        )
        summary = format_run_summary(run)
        for line in summary.split("\n"):
            assert len(line) <= 80, f"Line too long ({len(line)} chars): {line!r}"

    def test_estimated_cost_line_clamped_to_80_columns(self) -> None:
        """Estimated cost line with long lower-bound note is clamped to 80 columns."""
        run = _make_run(
            llm_call_count=1_000_000,
            llm_calls_without_tokens=999_999,
            total_input_tokens=100,
            total_output_tokens=50,
            total_estimated_cost=0.1234,
        )
        summary = format_run_summary(run)
        for line in summary.split("\n"):
            assert len(line) <= 80, f"Line too long ({len(line)} chars): {line!r}"

    def test_llm_call_and_token_lines_clamped_to_80_columns(self) -> None:
        """LLM call count and token totals stay within 80 columns for extreme values."""
        # Values large enough to force both rendered lines past 80 characters.
        run = _make_run(
            llm_call_count=10**40,
            llm_calls_without_tokens=10**40 - 1,
            total_input_tokens=10**40,
            total_output_tokens=10**40,
            total_estimated_cost=0.1234,
        )
        summary = format_run_summary(run)
        llm_line = next(ln for ln in summary.split("\n") if ln.startswith("LLM calls:"))
        tokens_line = next(ln for ln in summary.split("\n") if ln.startswith("Tokens:"))
        assert llm_line.endswith("..."), "expected line to be clamped"
        assert tokens_line.endswith("..."), "expected line to be clamped"
        for line in summary.split("\n"):
            assert len(line) <= 80, f"Line too long ({len(line)} chars): {line!r}"

    def test_nodes_line_clamped_to_80_columns(self) -> None:
        """Nodes: line is clamped to 80 columns even with extreme counts."""
        # 1 billion each → total=3000000000, detail has three 10-digit numbers.
        # Unclamped line is 86 chars, so the [:77]+"..." branch is exercised.
        run = _make_run(
            node_success=1_000_000_000,
            node_failure=1_000_000_000,
            node_skipped=1_000_000_000,
        )
        summary = format_run_summary(run)
        nodes_line = next(ln for ln in summary.split("\n") if ln.startswith("Nodes:"))
        assert nodes_line.endswith("..."), "expected line to be clamped"
        for line in summary.split("\n"):
            assert len(line) <= 80, f"Line too long ({len(line)} chars): {line!r}"

    def test_tools_line_clamped_to_80_columns(self) -> None:
        """Tools: line is clamped to 80 columns even with extreme counts/duration."""
        # 10**16 calls/failures + matching duration → unclamped line is 83 chars,
        # exercising the [:77]+"..." branch.
        run = _make_run(
            tool_call_count=10**16,
            tool_failures=10**16 - 1,
            total_tool_duration_ms=float(10**16) * 1000.0,
        )
        summary = format_run_summary(run)
        tools_line = next(ln for ln in summary.split("\n") if ln.startswith("Tools:"))
        assert tools_line.endswith("..."), "expected line to be clamped"
        for line in summary.split("\n"):
            assert len(line) <= 80, f"Line too long ({len(line)} chars): {line!r}"


class TestPrintRunSummary:
    """Tests for print_run_summary."""

    def test_prints_to_stdout(self, capsys: object) -> None:
        from agentic_devtools.orchestration.observability_summary import (
            print_run_summary,
        )

        run = _make_run(node_success=1)
        print_run_summary(run)
        captured = capsys.readouterr()  # type: ignore[attr-defined]
        assert "Workflow Run Summary" in captured.out
