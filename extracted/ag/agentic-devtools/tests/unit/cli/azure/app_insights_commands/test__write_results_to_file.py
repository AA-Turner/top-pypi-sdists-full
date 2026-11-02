"""Tests for _write_results_to_file."""

from agentic_devtools.cli.azure.app_insights_commands import _write_results_to_file


def test_writes_no_results_message_and_reports_path(tmp_path, capsys):
    output_file = tmp_path / "nested" / "results.txt"

    _write_results_to_file({}, output_file)

    assert output_file.read_text() == "No results found.\n"
    assert f"Results written to: {output_file}" in capsys.readouterr().out


def test_writes_rows_with_column_fallback_and_omits_falsy_values(tmp_path, capsys):
    output_file = tmp_path / "results.txt"
    data = {
        "tables": [
            {
                "columns": [{"name": "message"}, {}, {"name": "count"}],
                "rows": [["failed", "", 0, "ignored"]],
            }
        ]
    }

    _write_results_to_file(data, output_file)

    contents = output_file.read_text()
    assert "Total: 1 rows" in contents
    assert "--- Result 1 ---" in contents
    assert "message: failed" in contents
    assert "col1:" not in contents
    assert "count:" not in contents
    assert "ignored" not in contents
    assert f"Results written to: {output_file}" in capsys.readouterr().out
