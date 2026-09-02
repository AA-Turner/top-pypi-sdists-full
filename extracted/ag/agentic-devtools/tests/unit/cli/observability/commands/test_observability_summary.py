"""Tests for agdt-observability-summary CLI command."""

import json
from pathlib import Path
from typing import Any
from unittest.mock import patch

from agentic_devtools.cli.observability.commands import (
    _format_summary_from_events,
    _parse_events,
    observability_summary_command,
)


class TestParseEvents:
    """Tests for _parse_events."""

    def test_parses_valid_jsonl(self, tmp_path: Path) -> None:
        log_file = tmp_path / "test.jsonl"
        log_file.write_text('{"type": "node"}\n{"type": "llm_call"}\n')
        events = list(_parse_events(log_file))
        assert len(events) == 2

    def test_skips_invalid_json_lines(self, tmp_path: Path) -> None:
        log_file = tmp_path / "test.jsonl"
        log_file.write_text('{"type": "node"}\nnot valid json\n{"type": "llm_call"}\n')
        events = list(_parse_events(log_file))
        assert len(events) == 2

    def test_skips_empty_lines(self, tmp_path: Path) -> None:
        log_file = tmp_path / "test.jsonl"
        log_file.write_text('{"type": "node"}\n\n\n{"type": "llm_call"}\n')
        events = list(_parse_events(log_file))
        assert len(events) == 2

    def test_skips_non_object_json_values(self, tmp_path: Path) -> None:
        log_file = tmp_path / "test.jsonl"
        log_file.write_text('{"type": "node"}\n"plain-string"\n123\n[1,2,3]\n{"type": "llm_call"}\n')
        events = list(_parse_events(log_file))
        assert len(events) == 2
        assert all(isinstance(event, dict) for event in events)

    def test_skips_entry_when_redactor_returns_none(self, tmp_path: Path) -> None:
        """Events are dropped when redact() returns None (deep-copy failure)."""
        log_file = tmp_path / "test.jsonl"
        log_file.write_text('{"type": "node"}\n{"type": "llm_call"}\n')
        with patch("agentic_devtools.cli.observability.commands._DEFAULT_REDACTOR") as mock_redactor:
            mock_redactor.redact.return_value = None
            events = list(_parse_events(log_file))
        assert events == []


class TestFormatSummaryFromEvents:
    """Tests for _format_summary_from_events."""

    def test_node_success_counted(self) -> None:
        events = [{"type": "node", "status": "success", "node_name": "n1"}]
        summary = _format_summary_from_events(events)
        assert "1 success" in summary

    def test_node_failure_counted_with_error(self) -> None:
        events = [
            {
                "type": "node",
                "status": "failure",
                "node_name": "n1",
                "error_class": "transient",
                "error_message": "Connection failed",
            }
        ]
        summary = _format_summary_from_events(events)
        assert "1 failed" in summary
        assert "Errors (1)" in summary
        assert "[transient]" in summary

    def test_node_skipped_counted(self) -> None:
        events = [
            {"type": "node", "status": "skipped", "node_name": "n1"},
            {"type": "node", "status": "success", "node_name": "n2"},
        ]
        summary = _format_summary_from_events(events)
        assert "1 skipped" in summary
        assert "1 success" in summary

    def test_node_unknown_status_ignored(self) -> None:
        """Unknown node status is simply ignored."""
        events = [
            {"type": "node", "status": "unknown_state", "node_name": "n1"},
            {"type": "node", "status": "success", "node_name": "n2"},
        ]
        summary = _format_summary_from_events(events)
        assert "1 success" in summary

    def test_no_events_shows_none(self) -> None:
        summary = _format_summary_from_events([])
        assert "0 executed (none)" in summary

    def test_unknown_event_type_ignored(self) -> None:
        """Events with unknown type are skipped silently."""
        events = [
            {"type": "unknown_event_xyz", "data": "ignored"},
            {"type": "node", "status": "success", "node_name": "n1"},
        ]
        summary = _format_summary_from_events(events)
        assert "1 success" in summary

    def test_tool_call_events_counted(self) -> None:
        """tool_call events are aggregated and shown in summary."""
        events = [
            {
                "type": "tool_call",
                "tool_name": "git_push",
                "success": True,
                "duration_ms": 500.0,
            },
            {
                "type": "tool_call",
                "tool_name": "jira_comment",
                "success": True,
                "duration_ms": 300.0,
            },
        ]
        summary = _format_summary_from_events(events)
        assert "Tools:" in summary
        assert "2 calls" in summary

    def test_tool_call_failures_reported(self) -> None:
        """Failed tool calls are reflected in the Tools line."""
        events = [
            {
                "type": "tool_call",
                "tool_name": "git_push",
                "success": False,
                "duration_ms": 100.0,
            },
        ]
        summary = _format_summary_from_events(events)
        assert "1 failed" in summary

    def test_tool_call_duration_shown(self) -> None:
        """Total tool duration is shown in seconds."""
        events = [
            {
                "type": "tool_call",
                "tool_name": "git_push",
                "success": True,
                "duration_ms": 2500.0,
            },
        ]
        summary = _format_summary_from_events(events)
        assert "2.5s total" in summary

    def test_no_tool_calls_omits_tools_line(self) -> None:
        """When no tool_call events, Tools line is absent."""
        events = [{"type": "node", "status": "success", "node_name": "n1"}]
        summary = _format_summary_from_events(events)
        assert "Tools:" not in summary

    def test_tool_call_with_non_numeric_duration_is_ignored(self) -> None:
        events = [
            {"type": "tool_call", "tool_name": "t1", "success": True, "duration_ms": "bad"},
            {"type": "tool_call", "tool_name": "t_bool", "success": True, "duration_ms": True},
            {"type": "tool_call", "tool_name": "t_missing", "success": True},
            {"type": "tool_call", "tool_name": "t2", "success": True, "duration_ms": 200.0},
        ]
        summary = _format_summary_from_events(events)
        assert "Tools: 4 calls, 0.2s total" in summary

    def test_error_long_prefix_clamped_to_78_chars(self) -> None:
        """A very long node_name/error_class combination is clamped at 78 chars."""
        events = [
            {
                "type": "node",
                "status": "failure",
                "node_name": "n" * 55,
                "error_class": "e" * 20,
                "error_message": "msg",
            }
        ]
        summary = _format_summary_from_events(events)
        for line in summary.split("\n"):
            assert len(line) <= 80, f"Line too long ({len(line)} chars): {line!r}"

    def test_error_tiny_budget_message_hard_clamped(self) -> None:
        """When prefix leaves 1–3 chars, message is sliced without '...' suffix."""
        # "e"*20 + "n"*49 → prefix len 76, available=2 (0 < 2 <= 3)
        events = [
            {
                "type": "node",
                "status": "failure",
                "node_name": "n" * 49,
                "error_class": "e" * 20,
                "error_message": "Hello world",
            }
        ]
        summary = _format_summary_from_events(events)
        for line in summary.split("\n"):
            assert len(line) <= 80, f"Line too long ({len(line)} chars): {line!r}"

    def test_error_none_node_name_handled(self) -> None:
        """None node_name / error_class values don't crash the formatter."""
        events = [
            {
                "type": "node",
                "status": "failure",
                "node_name": None,
                "error_class": None,
                "error_message": "Something went wrong",
            }
        ]
        summary = _format_summary_from_events(events)
        assert "Errors (1)" in summary

    def test_llm_call_with_tokens(self) -> None:
        events = [
            {
                "type": "llm_call",
                "model": "gpt-4o",
                "input_tokens": 1000,
                "output_tokens": 500,
                "estimated_cost_usd": 0.0075,
            }
        ]
        summary = _format_summary_from_events(events)
        assert "LLM calls: 1" in summary
        assert "1,000 input" in summary
        assert "500 output" in summary
        assert "$0.0075" in summary

    def test_llm_call_without_tokens(self) -> None:
        events = [
            {
                "type": "llm_call",
                "model": "gpt-4o",
                "input_tokens": None,
                "output_tokens": None,
                "estimated_cost_usd": None,
            }
        ]
        summary = _format_summary_from_events(events)
        assert "1 without token data" in summary

    def test_llm_call_with_non_numeric_tokens_treated_as_missing(self) -> None:
        events = [
            {
                "type": "llm_call",
                "model": "gpt-4o",
                "input_tokens": "1000",
                "output_tokens": "500",
                "estimated_cost_usd": 0.01,
            },
            {
                "type": "llm_call",
                "model": "gpt-4o",
                "input_tokens": True,
                "output_tokens": False,
                "estimated_cost_usd": True,
            },
            {
                "type": "llm_call",
                "model": "gpt-4o",
                "input_tokens": 200,
                "output_tokens": 100,
                "estimated_cost_usd": 0.002,
            },
        ]
        summary = _format_summary_from_events(events)
        assert "LLM calls: 3 (2 without token data)" in summary
        assert "Tokens: 200 input | 100 output" in summary
        assert "1,200 input" not in summary

    def test_llm_call_with_integer_float_tokens_counted(self) -> None:
        events = [
            {
                "type": "llm_call",
                "model": "gpt-4o",
                "input_tokens": 1000.0,
                "output_tokens": 500.0,
                "estimated_cost_usd": 0.0075,
            }
        ]
        summary = _format_summary_from_events(events)
        assert "LLM calls: 1" in summary
        assert "Tokens: 1,000 input | 500 output" in summary

    def test_llm_calls_with_cost_and_excluded(self) -> None:
        events: list[dict[str, Any]] = [
            {
                "type": "llm_call",
                "model": "gpt-4o",
                "input_tokens": 1000,
                "output_tokens": 500,
                "estimated_cost_usd": 0.01,
            },
            {
                "type": "llm_call",
                "model": "gpt-4o",
                "input_tokens": None,
                "output_tokens": None,
                "estimated_cost_usd": None,
            },
        ]
        summary = _format_summary_from_events(events)
        assert "lower bound" in summary
        assert "1 call excluded" in summary

    def test_multiple_excluded_uses_plural(self) -> None:
        events: list[dict[str, Any]] = [
            {
                "type": "llm_call",
                "model": "gpt-4o",
                "input_tokens": 100,
                "output_tokens": 50,
                "estimated_cost_usd": 0.001,
            },
            {
                "type": "llm_call",
                "model": "gpt-4o",
                "input_tokens": None,
                "output_tokens": None,
                "estimated_cost_usd": None,
            },
            {
                "type": "llm_call",
                "model": "gpt-4o",
                "input_tokens": None,
                "output_tokens": None,
                "estimated_cost_usd": None,
            },
        ]
        summary = _format_summary_from_events(events)
        assert "2 calls excluded" in summary

    def test_multiple_models_shows_breakdown(self) -> None:
        events = [
            {
                "type": "llm_call",
                "model": "gpt-4o",
                "input_tokens": 1000,
                "output_tokens": 500,
                "estimated_cost_usd": 0.01,
            },
            {
                "type": "llm_call",
                "model": "gpt-4o-mini",
                "input_tokens": 500,
                "output_tokens": 200,
                "estimated_cost_usd": 0.001,
            },
        ]
        summary = _format_summary_from_events(events)
        assert "Per-model breakdown" in summary
        assert "gpt-4o:" in summary
        assert "gpt-4o-mini:" in summary

    def test_per_model_line_clamped_to_80_cols_with_long_model_name(self) -> None:
        """A 75-char model name must not push the per-model line past 80 columns."""
        long_model = "m" * 75
        events = [
            {
                "type": "llm_call",
                "model": long_model,
                "input_tokens": 1000,
                "output_tokens": 500,
                "estimated_cost_usd": 0.01,
            },
            {
                "type": "llm_call",
                "model": "gpt-4o",
                "input_tokens": 500,
                "output_tokens": 200,
                "estimated_cost_usd": 0.001,
            },
        ]
        summary = _format_summary_from_events(events)
        assert "Per-model breakdown" in summary
        for line in summary.split("\n"):
            assert len(line) <= 80, f"Line too long ({len(line)} chars): {line!r}"

    def test_estimated_cost_line_clamped_to_80_columns(self) -> None:
        """Estimated cost line with long lower-bound note is clamped to 80 columns."""
        events = [
            {
                "type": "llm_call",
                "model": "gpt-4o",
                "input_tokens": 100,
                "output_tokens": 50,
                "estimated_cost_usd": 0.001,
            }
        ]
        # Add many excluded calls to make lower-bound note very long.
        excluded_event: dict[str, object] = {
            "type": "llm_call",
            "model": "gpt-4o",
            "input_tokens": None,
            "output_tokens": None,
            "estimated_cost_usd": None,
        }
        events.extend([excluded_event] * 100_000)
        summary = _format_summary_from_events(events)
        for line in summary.split("\n"):
            assert len(line) <= 80, f"Line too long ({len(line)} chars): {line!r}"

    def test_single_model_no_breakdown(self) -> None:
        events = [
            {
                "type": "llm_call",
                "model": "gpt-4o",
                "input_tokens": 1000,
                "output_tokens": 500,
                "estimated_cost_usd": 0.01,
            },
        ]
        summary = _format_summary_from_events(events)
        assert "Per-model breakdown" not in summary

    def test_same_model_multiple_calls_accumulates_cost(self) -> None:
        """Multiple calls to the same model accumulate cost."""
        events = [
            {
                "type": "llm_call",
                "model": "gpt-4o",
                "input_tokens": 1000,
                "output_tokens": 500,
                "estimated_cost_usd": 0.01,
            },
            {
                "type": "llm_call",
                "model": "gpt-4o",
                "input_tokens": 2000,
                "output_tokens": 800,
                "estimated_cost_usd": 0.02,
            },
        ]
        summary = _format_summary_from_events(events)
        assert "LLM calls: 2" in summary

    def test_model_with_no_cost(self) -> None:
        events = [
            {
                "type": "llm_call",
                "model": "gpt-4o",
                "input_tokens": 100,
                "output_tokens": 50,
                "estimated_cost_usd": 0.001,
            },
            {
                "type": "llm_call",
                "model": "unknown",
                "input_tokens": 100,
                "output_tokens": 50,
                "estimated_cost_usd": None,
            },
        ]
        summary = _format_summary_from_events(events)
        assert "n/a" in summary

    def test_model_with_zero_cost(self) -> None:
        events = [
            {
                "type": "llm_call",
                "model": "free-model",
                "input_tokens": 0,
                "output_tokens": 0,
                "estimated_cost_usd": 0.0,
            },
            {
                "type": "llm_call",
                "model": "paid-model",
                "input_tokens": 100,
                "output_tokens": 50,
                "estimated_cost_usd": 0.001,
            },
        ]
        summary = _format_summary_from_events(events)
        assert "cost=$0.0000" in summary

    def test_per_model_ignores_non_numeric_token_and_cost_values(self) -> None:
        events: list[dict[str, Any]] = [
            {
                "type": "llm_call",
                "model": "bad-model",
                "input_tokens": "n/a",
                "output_tokens": "n/a",
                "estimated_cost_usd": "n/a",
            },
            {
                "type": "llm_call",
                "model": "good-model",
                "input_tokens": 100,
                "output_tokens": 50,
                "estimated_cost_usd": 0.001,
            },
        ]
        summary = _format_summary_from_events(events)
        assert "Per-model breakdown" in summary
        assert "bad-model: 1 calls, 0 in / 0 out, cost=n/a" in summary
        assert "good-model: 1 calls, 100 in / 50 out, cost=$0.0010" in summary

    def test_per_model_tokens_excluded_when_either_count_missing(self) -> None:
        """Per-model token totals are 0 when either token count is absent, matching overall totals."""
        events: list[dict[str, Any]] = [
            # input present but output missing — excluded from both overall and per-model
            {
                "type": "llm_call",
                "model": "gpt-4o",
                "input_tokens": 1000,
                "output_tokens": None,
                "estimated_cost_usd": None,
            },
            # both tokens present — counted in both overall and per-model
            {
                "type": "llm_call",
                "model": "gpt-4o",
                "input_tokens": 200,
                "output_tokens": 100,
                "estimated_cost_usd": 0.001,
            },
            # second model so per-model breakdown is rendered
            {
                "type": "llm_call",
                "model": "gpt-4o-mini",
                "input_tokens": 50,
                "output_tokens": 25,
                "estimated_cost_usd": 0.0001,
            },
        ]
        summary = _format_summary_from_events(events)
        assert "LLM calls: 3 (1 without token data)" in summary
        # Overall tokens reflect only the complete calls
        assert "Tokens: 250 input | 125 output" in summary
        # Per-model tokens are consistent: the partial call contributes 0 tokens
        assert "gpt-4o: 2 calls, 200 in / 100 out" in summary

    def test_llm_call_model_labels_are_normalized_to_safe_strings(self) -> None:
        """None/empty models default to unknown; non-string values are stringified."""
        events: list[dict[str, Any]] = [
            {
                "type": "llm_call",
                "model": None,
                "input_tokens": 100,
                "output_tokens": 50,
                "estimated_cost_usd": 0.001,
            },
            {
                "type": "llm_call",
                "model": "",
                "input_tokens": 100,
                "output_tokens": 50,
                "estimated_cost_usd": 0.001,
            },
            {
                "type": "llm_call",
                "model": 42,
                "input_tokens": 100,
                "output_tokens": 50,
                "estimated_cost_usd": 0.001,
            },
        ]
        summary = _format_summary_from_events(events)
        assert "Per-model breakdown" in summary
        assert "unknown: 2 calls" in summary
        assert "42: 1 calls" in summary

    def test_error_message_truncation(self) -> None:
        events = [
            {
                "type": "node",
                "status": "failure",
                "node_name": "n1",
                "error_class": "permanent",
                "error_message": "A" * 200,
            }
        ]
        summary = _format_summary_from_events(events)
        # Verify message is truncated
        for line in summary.split("\n"):
            assert len(line) <= 80 or "=" * 60 in line

    def test_error_message_short_not_truncated(self) -> None:
        """Short error messages pass through without truncation."""
        events = [
            {
                "type": "node",
                "status": "failure",
                "node_name": "n1",
                "error_class": "tool",
                "error_message": "Short error",
            }
        ]
        summary = _format_summary_from_events(events)
        assert "Short error" in summary


class TestObservabilitySummaryCommand:
    """Tests for the CLI command."""

    def _write_log_file(self, path: Path, events: list[dict]) -> None:
        with open(path, "w") as f:
            for event in events:
                f.write(json.dumps(event) + "\n")

    def test_prints_summary_from_log_file(self, tmp_path: Path, capsys: object) -> None:
        log_file = tmp_path / "test.jsonl"
        self._write_log_file(
            log_file,
            [
                {
                    "version": 1,
                    "event_seq": 1,
                    "type": "node",
                    "run_id": "r1",
                    "timestamp": "2024-01-01T00:00:01+00:00",
                    "node_name": "fetch",
                    "status": "success",
                    "duration_ms": 1000,
                },
                {
                    "version": 1,
                    "event_seq": 2,
                    "type": "llm_call",
                    "run_id": "r1",
                    "timestamp": "2024-01-01T00:00:02+00:00",
                    "node_name": "analyze",
                    "model": "gpt-4o",
                    "input_tokens": 1000,
                    "output_tokens": 500,
                    "latency_ms": 2000,
                    "estimated_cost_usd": 0.0075,
                },
            ],
        )

        with patch("sys.argv", ["agdt-observability-summary", str(log_file)]):
            observability_summary_command()

        # The command prints to stdout - verify it ran without error

    def test_exits_on_missing_file(self, tmp_path: Path) -> None:
        missing = tmp_path / "nonexistent.jsonl"
        with patch("sys.argv", ["agdt-observability-summary", str(missing)]):
            try:
                observability_summary_command()
                assert False, "Should have called sys.exit"  # noqa: B011
            except SystemExit as e:
                assert e.code == 1

    def test_exits_on_empty_file(self, tmp_path: Path) -> None:
        empty_file = tmp_path / "empty.jsonl"
        empty_file.write_text("")
        with patch("sys.argv", ["agdt-observability-summary", str(empty_file)]):
            try:
                observability_summary_command()
                assert False, "Should have called sys.exit"  # noqa: B011
            except SystemExit as e:
                assert e.code == 1

    def test_exits_on_unicode_decode_error_reading_log_file(self, tmp_path: Path) -> None:
        """Non-UTF-8 bytes in the log file produce a clean error + exit 1."""
        import io

        log_file = tmp_path / "test.jsonl"
        log_file.write_bytes(b"\xff\xfe invalid utf-8\n")

        captured_stderr = io.StringIO()
        with patch("sys.stderr", captured_stderr):
            with patch("sys.argv", ["agdt-observability-summary", str(log_file)]):
                try:
                    observability_summary_command()
                    assert False, "Should have called sys.exit"  # noqa: B011
                except SystemExit as e:
                    assert e.code == 1
        assert "Failed to read" in captured_stderr.getvalue()

    def test_exits_on_io_error_reading_log_file(self, tmp_path: Path) -> None:
        """I/O errors when reading the log file produce a clean error + exit 1."""
        import io
        from unittest.mock import mock_open
        from unittest.mock import patch as mock_patch

        log_file = tmp_path / "test.jsonl"
        log_file.write_text('{"type": "node"}\n')

        captured_stderr = io.StringIO()
        with mock_patch("builtins.open", mock_open(read_data="")) as m:
            m.side_effect = PermissionError("Permission denied")
            with mock_patch("sys.stderr", captured_stderr):
                with mock_patch("sys.argv", ["agdt-observability-summary", str(log_file)]):
                    try:
                        observability_summary_command()
                        assert False, "Should have called sys.exit"  # noqa: B011
                    except SystemExit as e:
                        assert e.code == 1
        assert "Failed to read" in captured_stderr.getvalue()

    def test_exits_on_mid_iteration_os_error(self, tmp_path: Path) -> None:
        """An OSError raised after the first event is yielded produces a clean error + exit 1."""
        import io
        from collections.abc import Iterator
        from typing import Any
        from unittest.mock import patch as mock_patch

        log_file = tmp_path / "test.jsonl"
        log_file.write_text('{"type": "node", "status": "success"}\n')

        def _raise_mid_iteration() -> Iterator[dict[str, Any]]:
            yield {"type": "node", "status": "success"}
            raise OSError("Disk read error mid-file")

        captured_stderr = io.StringIO()
        with mock_patch(
            "agentic_devtools.cli.observability.commands._parse_events",
            return_value=_raise_mid_iteration(),
        ):
            with mock_patch("sys.stderr", captured_stderr):
                with mock_patch("sys.argv", ["agdt-observability-summary", str(log_file)]):
                    try:
                        observability_summary_command()
                        assert False, "Should have called sys.exit"  # noqa: B011
                    except SystemExit as e:
                        assert e.code == 1
        assert "Failed to read" in captured_stderr.getvalue()

    def test_exits_on_mid_iteration_unicode_decode_error(self, tmp_path: Path) -> None:
        """A UnicodeDecodeError raised after the first event is yielded produces a clean error + exit 1."""
        import io
        from collections.abc import Iterator
        from typing import Any
        from unittest.mock import patch as mock_patch

        log_file = tmp_path / "test.jsonl"
        log_file.write_text('{"type": "node", "status": "success"}\n')

        def _raise_mid_iteration() -> Iterator[dict[str, Any]]:
            yield {"type": "node", "status": "success"}
            raise UnicodeDecodeError("utf-8", b"\xff", 0, 1, "invalid start byte")

        captured_stderr = io.StringIO()
        with mock_patch(
            "agentic_devtools.cli.observability.commands._parse_events",
            return_value=_raise_mid_iteration(),
        ):
            with mock_patch("sys.stderr", captured_stderr):
                with mock_patch("sys.argv", ["agdt-observability-summary", str(log_file)]):
                    try:
                        observability_summary_command()
                        assert False, "Should have called sys.exit"  # noqa: B011
                    except SystemExit as e:
                        assert e.code == 1
        assert "Failed to read" in captured_stderr.getvalue()


class TestAsBool:
    """Tests for _as_bool."""

    def test_true_returns_true(self) -> None:
        from agentic_devtools.cli.observability.commands import _as_bool

        assert _as_bool(True) is True

    def test_false_returns_false(self) -> None:
        from agentic_devtools.cli.observability.commands import _as_bool

        assert _as_bool(False) is False

    def test_int_one_returns_none(self) -> None:
        from agentic_devtools.cli.observability.commands import _as_bool

        assert _as_bool(1) is None

    def test_int_zero_returns_none(self) -> None:
        from agentic_devtools.cli.observability.commands import _as_bool

        assert _as_bool(0) is None

    def test_string_true_returns_none(self) -> None:
        from agentic_devtools.cli.observability.commands import _as_bool

        assert _as_bool("true") is None

    def test_none_returns_none(self) -> None:
        from agentic_devtools.cli.observability.commands import _as_bool

        assert _as_bool(None) is None


class TestStrictBoolSuccess:
    """Tests that tool_call success is parsed strictly as bool."""

    def test_success_false_counted_as_failure(self) -> None:
        events = [{"type": "tool_call", "tool_name": "t1", "success": False, "duration_ms": 100.0}]
        summary = _format_summary_from_events(events)
        assert "1 failed" in summary

    def test_success_true_not_counted_as_failure(self) -> None:
        events = [{"type": "tool_call", "tool_name": "t1", "success": True, "duration_ms": 100.0}]
        summary = _format_summary_from_events(events)
        assert "failed" not in summary

    def test_success_zero_int_not_counted_as_failure(self) -> None:
        """int 0 is falsy but not a real bool — must not be counted as failure."""
        events = [{"type": "tool_call", "tool_name": "t1", "success": 0, "duration_ms": 100.0}]
        summary = _format_summary_from_events(events)
        assert "failed" not in summary

    def test_success_empty_string_not_counted_as_failure(self) -> None:
        """Empty string is falsy but not a real bool — must not be counted as failure."""
        events = [{"type": "tool_call", "tool_name": "t1", "success": "", "duration_ms": 100.0}]
        summary = _format_summary_from_events(events)
        assert "failed" not in summary

    def test_success_missing_not_counted_as_failure(self) -> None:
        """Missing success field must not be counted as failure."""
        events = [{"type": "tool_call", "tool_name": "t1", "duration_ms": 100.0}]
        summary = _format_summary_from_events(events)
        assert "failed" not in summary

    def test_success_none_not_counted_as_failure(self) -> None:
        """None success field must not be counted as failure."""
        events = [{"type": "tool_call", "tool_name": "t1", "success": None, "duration_ms": 100.0}]
        summary = _format_summary_from_events(events)
        assert "failed" not in summary


class TestParseEventsRedaction:
    """Tests that _parse_events redacts sensitive fields in log entries."""

    def test_error_message_with_bearer_token_redacted(self, tmp_path: Path) -> None:
        """****** embedded in error_message are stripped before stdout."""
        log_file = tmp_path / "test.jsonl"
        log_file.write_text(
            json.dumps(
                {
                    "type": "node",
                    "status": "failure",
                    "node_name": "fetch",
                    "error_class": "llm",
                    "error_message": "Request failed: ghp_abc123xyz",
                }
            )
            + "\n"
        )
        events = list(_parse_events(log_file))
        assert len(events) == 1
        msg = events[0].get("error_message", "")
        assert "ghp_abc123xyz" not in msg
        assert "[REDACTED]" in msg

    def test_sensitive_key_redacted(self, tmp_path: Path) -> None:
        """Fields with sensitive key names (e.g. 'token') are redacted."""
        log_file = tmp_path / "test.jsonl"
        log_file.write_text(json.dumps({"type": "node", "status": "success", "token": "super-secret-value"}) + "\n")
        events = list(_parse_events(log_file))
        assert len(events) == 1
        assert events[0].get("token") == "[REDACTED]"

    def test_non_sensitive_fields_preserved(self, tmp_path: Path) -> None:
        """Normal fields are passed through unchanged."""
        log_file = tmp_path / "test.jsonl"
        log_file.write_text(json.dumps({"type": "node", "status": "success", "node_name": "fetch"}) + "\n")
        events = list(_parse_events(log_file))
        assert len(events) == 1
        assert events[0]["node_name"] == "fetch"
        assert events[0]["status"] == "success"
