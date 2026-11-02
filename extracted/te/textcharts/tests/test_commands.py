"""Tests for the shared command layer: registry, parsers, executor, and introspection."""

from __future__ import annotations

import pytest

from textcharts.commands import (
    CommandInfo,
    describe_command,
    execute_command,
    get_command,
    get_input_schema,
    list_commands,
)
from textcharts.commands.parsers import ParseError, parse_input
from textcharts.commands.registry import COMMON_OPTIONS, REGISTRY

# ---------------------------------------------------------------------------
# Registry tests
# ---------------------------------------------------------------------------


class TestRegistry:
    def test_all_15_commands_registered(self):
        assert len(REGISTRY) == 15

    def test_expected_command_names(self):
        expected = {
            "bar", "histogram", "heatmap", "boxplot", "line", "scatter",
            "comparison", "diverging", "summary", "percentile", "speedup",
            "stacked", "sparkline", "cdf", "rank",
        }
        assert set(REGISTRY.keys()) == expected

    def test_get_command_valid(self):
        cmd = get_command("bar")
        assert isinstance(cmd, CommandInfo)
        assert cmd.name == "bar"
        assert cmd.chart_class == "BarChart"

    def test_get_command_unknown_raises(self):
        with pytest.raises(KeyError, match="Unknown command 'nope'"):
            get_command("nope")

    def test_command_info_fields_populated(self):
        for name, cmd in REGISTRY.items():
            assert cmd.name == name
            assert cmd.description
            assert cmd.chart_module.startswith("textcharts.")
            assert cmd.chart_class
            assert cmd.data_param_name
            assert len(cmd.data_fields) > 0

    def test_common_options_defined(self):
        assert len(COMMON_OPTIONS) == 8
        names = {p.name for p in COMMON_OPTIONS}
        assert "width" in names
        assert "use_color" in names
        assert "theme" in names
        assert "outlier_cap" in names


# ---------------------------------------------------------------------------
# Introspection tests
# ---------------------------------------------------------------------------


class TestIntrospection:
    def test_list_commands_returns_all(self):
        cmds = list_commands()
        assert len(cmds) == 15
        assert all(isinstance(c, tuple) and len(c) == 2 for c in cmds)

    def test_list_commands_sorted(self):
        cmds = list_commands()
        names = [c[0] for c in cmds]
        assert names == sorted(names)

    def test_describe_command_structure(self):
        desc = describe_command("bar")
        assert desc["name"] == "bar"
        assert "description" in desc
        assert "data_fields" in desc
        assert "chart_params" in desc
        assert "common_options" in desc
        assert len(desc["common_options"]) == 8

    def test_describe_command_unknown_raises(self):
        with pytest.raises(KeyError):
            describe_command("nope")

    def test_get_input_schema_structure(self):
        schema = get_input_schema("bar")
        assert schema["type"] == "object"
        assert "data" in schema["properties"]
        assert schema["required"] == ["data"]

    def test_get_input_schema_list_type(self):
        schema = get_input_schema("bar")
        data_schema = schema["properties"]["data"]
        assert data_schema["type"] == "array"
        assert "items" in data_schema

    def test_get_input_schema_object_type(self):
        schema = get_input_schema("summary")
        data_schema = schema["properties"]["data"]
        assert data_schema["type"] == "object"
        assert "properties" in data_schema

    def test_get_input_schema_includes_chart_params(self):
        schema = get_input_schema("bar")
        assert "sort_by" in schema["properties"]
        assert "metric_label" in schema["properties"]

    def test_get_input_schema_includes_common_options(self):
        schema = get_input_schema("bar")
        assert "width" in schema["properties"]
        assert "use_color" in schema["properties"]
        assert "theme" in schema["properties"]


# ---------------------------------------------------------------------------
# Parser tests
# ---------------------------------------------------------------------------


class TestParsers:
    def test_parse_bar_valid(self):
        result = parse_input("bar", [{"label": "A", "value": 10}, {"label": "B", "value": 20}])
        assert len(result) == 2
        assert result[0].label == "A"
        assert result[0].value == 10.0

    def test_parse_bar_coerces_types(self):
        result = parse_input("bar", [{"label": "A", "value": "42.5"}])
        assert result[0].value == 42.5

    def test_parse_bar_missing_field(self):
        with pytest.raises(ParseError, match="missing required fields: value"):
            parse_input("bar", [{"label": "A"}])

    def test_parse_bar_empty_list(self):
        with pytest.raises(ParseError, match="must not be empty"):
            parse_input("bar", [])

    def test_parse_bar_not_list(self):
        with pytest.raises(ParseError, match="expected a list"):
            parse_input("bar", {"label": "A", "value": 10})

    def test_parse_bar_invalid_value(self):
        with pytest.raises(ParseError, match="must be numeric"):
            parse_input("bar", [{"label": "A", "value": "not_a_number"}])

    def test_parse_histogram_valid(self):
        result = parse_input("histogram", [
            {"label": "Q1", "value": 100},
            {"label": "Q2", "value": 200},
        ])
        assert len(result) == 2
        assert result[0].label == "Q1"

    def test_parse_heatmap_valid(self):
        result = parse_input("heatmap", {
            "matrix": [[1.0, 2.0], [3.0, 4.0]],
            "row_labels": ["R1", "R2"],
            "col_labels": ["C1", "C2"],
        })
        assert isinstance(result, dict)
        assert "matrix" in result
        assert len(result["matrix"]) == 2

    def test_parse_heatmap_dimension_mismatch(self):
        with pytest.raises(ParseError, match="row_labels has 1 entries"):
            parse_input("heatmap", {
                "matrix": [[1, 2], [3, 4]],
                "row_labels": ["R1"],
                "col_labels": ["C1", "C2"],
            })

    def test_parse_heatmap_null_values(self):
        result = parse_input("heatmap", {
            "matrix": [[1.0, None], [None, 4.0]],
            "row_labels": ["R1", "R2"],
            "col_labels": ["C1", "C2"],
        })
        assert result["matrix"][0][1] is None
        assert result["matrix"][1][0] is None

    def test_parse_boxplot_valid(self):
        result = parse_input("boxplot", [
            {"name": "Series A", "values": [1, 2, 3, 4, 5]},
        ])
        assert len(result) == 1
        assert result[0].name == "Series A"
        assert len(result[0].values) == 5

    def test_parse_line_valid(self):
        result = parse_input("line", [
            {"series": "S1", "x": 1, "y": 10},
            {"series": "S1", "x": 2, "y": 20},
        ])
        assert len(result) == 2
        assert result[0].x == 1.0

    def test_parse_line_string_x(self):
        result = parse_input("line", [{"series": "S1", "x": "Jan", "y": 10}])
        assert result[0].x == "Jan"

    def test_parse_scatter_valid(self):
        result = parse_input("scatter", [
            {"name": "P1", "x": 1.0, "y": 2.0},
            {"name": "P2", "x": 3.0, "y": 4.0, "is_pareto": True},
        ])
        assert len(result) == 2
        assert result[1].is_pareto is True

    def test_parse_comparison_valid(self):
        result = parse_input("comparison", [
            {"label": "Q1", "baseline_value": 100, "comparison_value": 80},
        ])
        assert result[0].baseline_name == "Baseline"

    def test_parse_diverging_valid(self):
        result = parse_input("diverging", [
            {"label": "Q1", "pct_change": -15.5},
            {"label": "Q2", "pct_change": 10.2},
        ])
        assert result[0].pct_change == -15.5

    def test_parse_summary_valid(self):
        result = parse_input("summary", {
            "title": "Test Summary",
            "primary_value": 42.5,
            "num_items": 10,
        })
        assert result.title == "Test Summary"
        assert result.primary_value == 42.5
        assert result.num_items == 10

    def test_parse_summary_empty(self):
        result = parse_input("summary", {})
        assert isinstance(result.title, str) and result.title

    def test_parse_percentile_valid(self):
        result = parse_input("percentile", [
            {"name": "Q1", "p50": 10, "p90": 20, "p95": 25, "p99": 30},
        ])
        assert result[0].p50 == 10.0

    def test_parse_speedup_valid(self):
        result = parse_input("speedup", [
            {"name": "DuckDB", "ratio": 2.5},
            {"name": "SQLite", "ratio": 1.0, "is_baseline": True},
        ])
        assert result[1].is_baseline is True

    def test_parse_stacked_valid(self):
        result = parse_input("stacked", [
            {
                "label": "Query 1",
                "segments": [
                    {"phase_name": "Parse", "value": 10},
                    {"phase_name": "Execute", "value": 90},
                ],
            },
        ])
        assert len(result[0].segments) == 2
        assert result[0].segments[0].phase_name == "Parse"

    def test_parse_sparkline_valid(self):
        result = parse_input("sparkline", {
            "rows": ["DuckDB", "SQLite"],
            "columns": [
                {"name": "Latency", "values": {"DuckDB": 10, "SQLite": 20}},
                {"name": "Throughput", "values": {"DuckDB": 100, "SQLite": 50}, "higher_is_better": True},
            ],
        })
        assert len(result.rows) == 2
        assert len(result.columns) == 2

    def test_parse_cdf_valid(self):
        result = parse_input("cdf", [
            {"name": "Series A", "values": [1, 2, 3, 4, 5]},
        ])
        assert result[0].name == "Series A"

    def test_parse_rank_valid(self):
        result = parse_input("rank", {
            "items": ["Q1", "Q2"],
            "groups": ["DuckDB", "SQLite"],
            "values": {
                "DuckDB,Q1": 10, "DuckDB,Q2": 20,
                "SQLite,Q1": 15, "SQLite,Q2": 25,
            },
        })
        assert result.values[("DuckDB", "Q1")] == 10.0

    def test_parse_rank_bad_key_format(self):
        with pytest.raises(ParseError, match="must be 'group,item' format"):
            parse_input("rank", {
                "items": ["Q1"],
                "groups": ["DuckDB"],
                "values": {"bad_key": 10},
            })

    def test_parse_unknown_command(self):
        with pytest.raises(ParseError, match="No parser for command 'nope'"):
            parse_input("nope", [])


# ---------------------------------------------------------------------------
# Executor tests — round-trip rendering for all 15 chart types
# ---------------------------------------------------------------------------


SAMPLE_DATA = {
    "bar": [
        {"label": "A", "value": 10},
        {"label": "B", "value": 20},
        {"label": "C", "value": 15},
    ],
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
    "summary": {
        "title": "Test Summary",
        "primary_value": 42.5,
        "secondary_value": 40.0,
        "num_items": 10,
    },
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
        {
            "label": "Q1",
            "segments": [
                {"phase_name": "Parse", "value": 10},
                {"phase_name": "Execute", "value": 90},
            ],
        },
        {
            "label": "Q2",
            "segments": [
                {"phase_name": "Parse", "value": 20},
                {"phase_name": "Execute", "value": 80},
            ],
        },
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
        "values": {
            "DuckDB,Q1": 10, "DuckDB,Q2": 20,
            "SQLite,Q1": 15, "SQLite,Q2": 25,
        },
    },
}


class TestExecutor:
    @pytest.mark.parametrize("command", sorted(SAMPLE_DATA.keys()))
    def test_execute_renders_all_chart_types(self, command):
        result = execute_command(
            command,
            SAMPLE_DATA[command],
            title=f"Test {command}",
            options={"use_color": False},
        )
        assert isinstance(result, str)
        assert len(result) > 0

    def test_execute_unknown_command(self):
        with pytest.raises(KeyError, match="Unknown command"):
            execute_command("nope", [])

    def test_execute_invalid_data(self):
        with pytest.raises(ParseError):
            execute_command("bar", "not a list")

    def test_execute_with_chart_params(self):
        result = execute_command(
            "bar",
            SAMPLE_DATA["bar"],
            sort_by="label",
            metric_label="Score",
        )
        assert isinstance(result, str)
        assert "Score" in result

    def test_execute_with_options(self):
        result = execute_command(
            "bar",
            SAMPLE_DATA["bar"],
            options={"use_color": False, "use_unicode": False, "width": 60},
        )
        assert isinstance(result, str)

    def test_execute_with_title(self):
        result = execute_command(
            "bar",
            SAMPLE_DATA["bar"],
            title="Custom Title",
            options={"use_color": False},
        )
        assert "Custom Title" in result

    def test_execute_with_subject(self):
        result = execute_command(
            "bar",
            SAMPLE_DATA["bar"],
            subject="Revenue",
            options={"use_color": False},
        )
        assert "Revenue Bar Chart" in result

    def test_execute_title_wins_over_subject(self):
        result = execute_command(
            "bar",
            SAMPLE_DATA["bar"],
            title="Explicit",
            subject="Ignored",
            options={"use_color": False},
        )
        assert "Explicit" in result
        assert "Ignored" not in result

    def test_execute_heatmap_matrix_input(self):
        result = execute_command("heatmap", SAMPLE_DATA["heatmap"], options={"use_color": False})
        assert isinstance(result, str)
        assert len(result) > 0

    def test_execute_summary_single_object(self):
        result = execute_command("summary", SAMPLE_DATA["summary"], options={"use_color": False})
        assert "Test Summary" in result

    def test_execute_sparkline_single_object(self):
        result = execute_command("sparkline", SAMPLE_DATA["sparkline"], options={"use_color": False})
        assert isinstance(result, str)

    def test_execute_rank_single_object(self):
        result = execute_command("rank", SAMPLE_DATA["rank"], options={"use_color": False})
        assert isinstance(result, str)
