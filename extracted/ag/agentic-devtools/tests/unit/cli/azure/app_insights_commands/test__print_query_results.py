"""Tests for _print_query_results."""

from agentic_devtools.cli.azure.app_insights_commands import _print_query_results


def test_does_not_print_dry_run_result(capsys):
    _print_query_results({"dry_run": True})

    assert capsys.readouterr().out == ""


def test_prints_message_for_missing_tables_or_rows(capsys):
    _print_query_results({})
    _print_query_results({"tables": [{"columns": [], "rows": []}]})

    assert capsys.readouterr().out.splitlines() == [
        "No results found.",
        "No results found.",
    ]


def test_prints_table_rows_with_empty_values(capsys):
    data = {
        "tables": [
            {
                "columns": [{"name": "message"}, {"name": "count"}],
                "rows": [["failed", 0]],
            }
        ]
    }

    _print_query_results(data)

    output = capsys.readouterr().out
    assert "Found 1 results:" in output
    assert "message | count" in output
    assert "failed | " in output


def test_prints_block_rows_and_omits_falsy_values(capsys):
    data = {
        "tables": [
            {
                "columns": [{"name": "message"}, {"name": "count"}],
                "rows": [["failed", 0]],
            }
        ]
    }

    _print_query_results(data, format_type="block")

    output = capsys.readouterr().out
    assert "--- Result 1 ---" in output
    assert "message: failed" in output
    assert "count:" not in output
