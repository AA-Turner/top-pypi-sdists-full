"""Integration tests for the textcharts CLI.

Tests invoke the CLI via textcharts.cli.main() directly (for speed and coverage)
and verify rendering, error handling, and meta-commands.
"""

from __future__ import annotations

import json
from io import StringIO
from unittest import mock

import pytest

from textcharts.cli import main

# Sample data for each chart type (matches test_commands.py SAMPLE_DATA)
SAMPLE_DATA = {
    "bar": [{"label": "A", "value": 10}, {"label": "B", "value": 20}, {"label": "C", "value": 15}],
    "histogram": [
        {"label": "Q1", "value": 100},
        {"label": "Q2", "value": 200},
        {"label": "Q3", "value": 150},
    ],
    "heatmap": {
        "matrix": [[10, 20], [30, 40]],
        "row_labels": ["Q1", "Q2"],
        "col_labels": ["DuckDB", "SQLite"],
    },
    "boxplot": [
        {"name": "A", "values": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]},
        {"name": "B", "values": [5, 6, 7, 8, 9, 10, 11, 12, 13, 14]},
    ],
    "line": [
        {"series": "S1", "x": 1, "y": 10},
        {"series": "S1", "x": 2, "y": 20},
        {"series": "S1", "x": 3, "y": 15},
    ],
    "scatter": [
        {"name": "P1", "x": 1, "y": 10},
        {"name": "P2", "x": 2, "y": 20},
        {"name": "P3", "x": 3, "y": 15},
    ],
    "comparison": [
        {"label": "Q1", "baseline_value": 100, "comparison_value": 80},
        {"label": "Q2", "baseline_value": 200, "comparison_value": 150},
    ],
    "diverging": [
        {"label": "Q1", "pct_change": -20},
        {"label": "Q2", "pct_change": 15},
        {"label": "Q3", "pct_change": -5},
    ],
    "summary": {"title": "Test Summary", "primary_value": 42.5, "secondary_value": 40.0, "num_items": 10},
    "percentile": [
        {"name": "Q1", "p50": 10, "p90": 20, "p95": 25, "p99": 30},
        {"name": "Q2", "p50": 15, "p90": 25, "p95": 30, "p99": 40},
    ],
    "speedup": [
        {"name": "DuckDB", "ratio": 2.5},
        {"name": "Postgres", "ratio": 1.5},
        {"name": "SQLite", "ratio": 1.0, "is_baseline": True},
    ],
    "stacked": [
        {"label": "Q1", "segments": [{"phase_name": "Parse", "value": 10}, {"phase_name": "Execute", "value": 90}]},
        {"label": "Q2", "segments": [{"phase_name": "Parse", "value": 20}, {"phase_name": "Execute", "value": 80}]},
    ],
    "sparkline": {
        "rows": ["DuckDB", "SQLite"],
        "columns": [
            {"name": "Latency (ms)", "values": {"DuckDB": 10, "SQLite": 20}},
            {"name": "Throughput", "values": {"DuckDB": 100, "SQLite": 50}, "higher_is_better": True},
        ],
    },
    "cdf": [
        {"name": "A", "values": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]},
        {"name": "B", "values": [2, 4, 6, 8, 10, 12, 14, 16, 18, 20]},
    ],
    "rank": {
        "items": ["Q1", "Q2"],
        "groups": ["DuckDB", "SQLite"],
        "values": {"DuckDB,Q1": 10, "DuckDB,Q2": 20, "SQLite,Q1": 15, "SQLite,Q2": 25},
    },
}


def _run_cli(argv: list[str], stdin_data: str | None = None) -> tuple[str, str, int]:
    """Run CLI and capture stdout, stderr, exit code."""
    stdout = StringIO()
    stderr = StringIO()
    exit_code = 0

    stdin_mock = StringIO(stdin_data) if stdin_data else StringIO()
    # If no stdin_data, make it look like a tty (no data)
    if stdin_data is None:
        stdin_mock.isatty = lambda: True
    else:
        stdin_mock.isatty = lambda: False

    with mock.patch("sys.stdout", stdout), mock.patch("sys.stderr", stderr), mock.patch("sys.stdin", stdin_mock):
        try:
            main(argv)
        except SystemExit as e:
            exit_code = e.code if isinstance(e.code, int) else 1

    return stdout.getvalue(), stderr.getvalue(), exit_code


# ---------------------------------------------------------------------------
# Meta-command tests
# ---------------------------------------------------------------------------


class TestListCommand:
    def test_list_shows_all_chart_types(self):
        out, _, code = _run_cli(["list"])
        assert code == 0
        for name in SAMPLE_DATA:
            assert name in out

    def test_list_shows_15_entries(self):
        out, _, code = _run_cli(["list"])
        assert code == 0
        lines = [line for line in out.strip().split("\n") if line.strip()]
        assert len(lines) == 15


class TestHelpOutput:
    def test_no_command_shows_help(self):
        _, _, code = _run_cli([])
        assert code == 1

    def test_subcommand_help(self):
        out, _, code = _run_cli(["bar", "--help"])
        # argparse --help calls sys.exit(0)
        assert code == 0
        assert "Data fields:" in out
        assert "label" in out
        assert "value" in out
        assert "Example:" in out


# ---------------------------------------------------------------------------
# Rendering tests — stdin input for all 15 chart types
# ---------------------------------------------------------------------------


class TestRenderingFromStdin:
    @pytest.mark.parametrize("command", sorted(SAMPLE_DATA.keys()))
    def test_render_chart_type(self, command):
        data_json = json.dumps(SAMPLE_DATA[command])
        out, err, code = _run_cli([command, "--no-color"], stdin_data=data_json)
        assert code == 0, f"stderr: {err}"
        assert len(out.strip()) > 0

    def test_render_with_title(self):
        data_json = json.dumps(SAMPLE_DATA["bar"])
        out, _, code = _run_cli(["bar", "--no-color", "--title", "My Chart"], stdin_data=data_json)
        assert code == 0
        assert "My Chart" in out

    def test_render_with_chart_params(self):
        data_json = json.dumps(SAMPLE_DATA["bar"])
        out, _, code = _run_cli(
            ["bar", "--no-color", "--sort-by", "label", "--metric-label", "Score"],
            stdin_data=data_json,
        )
        assert code == 0
        assert "Score" in out

    def test_render_with_width(self):
        data_json = json.dumps(SAMPLE_DATA["bar"])
        out, _, code = _run_cli(["bar", "--no-color", "--width", "60"], stdin_data=data_json)
        assert code == 0
        # Lines should be roughly bounded by width
        max_line = max(len(line) for line in out.split("\n") if line.strip())
        assert max_line <= 80  # some tolerance for labels

    def test_render_with_theme(self):
        data_json = json.dumps(SAMPLE_DATA["bar"])
        out, _, code = _run_cli(["bar", "--no-color", "--theme", "dark"], stdin_data=data_json)
        assert code == 0
        assert len(out.strip()) > 0

    def test_render_with_outlier_cap(self):
        data = [{"label": f"B{i}", "value": v} for i, v in enumerate([10, 11, 12, 13, 14, 15, 5000])]
        data_json = json.dumps(data)
        capped, _, capped_code = _run_cli(
            ["bar", "--no-color", "--no-unicode", "--outlier-cap", "20"], stdin_data=data_json
        )
        assert capped_code == 0
        uncapped, _, uncapped_code = _run_cli(
            ["bar", "--no-color", "--no-unicode", "--outlier-cap", "0"], stdin_data=data_json
        )
        assert uncapped_code == 0
        assert capped != uncapped

    def test_diverging_lower_is_better_flag(self):
        data_json = json.dumps(SAMPLE_DATA["diverging"])
        out, _, code = _run_cli(
            ["diverging", "--no-color", "--no-lower-is-better"], stdin_data=data_json
        )
        assert code == 0
        assert "Worse" in out
        assert "Better" in out


# ---------------------------------------------------------------------------
# File input tests
# ---------------------------------------------------------------------------


class TestFileInput:
    def test_render_from_file(self, tmp_path):
        data_file = tmp_path / "data.json"
        data_file.write_text(json.dumps(SAMPLE_DATA["bar"]))
        out, _, code = _run_cli(["bar", "--no-color", "-f", str(data_file)])
        assert code == 0
        assert len(out.strip()) > 0

    def test_file_not_found(self):
        _, err, code = _run_cli(["bar", "-f", "/nonexistent/path.json"])
        assert code == 1
        assert "file not found" in err.lower()

    def test_invalid_json_file(self, tmp_path):
        bad_file = tmp_path / "bad.json"
        bad_file.write_text("not json {{{")
        _, err, code = _run_cli(["bar", "-f", str(bad_file)])
        assert code == 1
        assert "invalid json" in err.lower()


# ---------------------------------------------------------------------------
# Error handling tests
# ---------------------------------------------------------------------------


class TestErrorHandling:
    def test_no_stdin_data(self):
        _, err, code = _run_cli(["bar"])
        assert code == 1
        assert "no input data" in err.lower()

    def test_empty_stdin(self):
        _, err, code = _run_cli(["bar"], stdin_data="")
        assert code == 1
        assert "empty input" in err.lower()

    def test_invalid_json_stdin(self):
        _, err, code = _run_cli(["bar"], stdin_data="not json")
        assert code == 1
        assert "invalid json" in err.lower()

    def test_wrong_data_format(self):
        # Bar expects a list, not a dict
        _, err, code = _run_cli(["bar", "--no-color"], stdin_data='{"label": "A", "value": 10}')
        assert code == 1
        assert "error" in err.lower()

    def test_missing_required_field(self):
        _, err, code = _run_cli(["bar", "--no-color"], stdin_data='[{"label": "A"}]')
        assert code == 1
        assert "error" in err.lower()
