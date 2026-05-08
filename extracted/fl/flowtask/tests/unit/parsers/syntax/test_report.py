"""Unit tests for flowtask.parsers.syntax.report."""
import orjson
import pytest

from flowtask.parsers.syntax.report import SyntaxIssue, SyntaxReport


def _issue(**kw):
    """Helper to build a SyntaxIssue with minimal required fields."""
    base = {"severity": "error", "code": "E_X", "message": "m"}
    base.update(kw)
    return SyntaxIssue(**base)


def test_empty_report_has_no_errors():
    """An empty report with ok=True should have no issues and no errors."""
    r = SyntaxReport(file="task.yaml", fmt="yaml", ok=True)
    assert r.has_errors() is False
    assert r.issues == []


def test_has_errors_truth_table():
    """has_errors returns True only when at least one issue is severity=error."""
    r1 = SyntaxReport(file="t", fmt="yaml", ok=False, issues=[_issue()])
    r2 = SyntaxReport(
        file="t", fmt="yaml", ok=True,
        issues=[_issue(severity="warning", code="W_X")]
    )
    r3 = SyntaxReport(
        file="t", fmt="yaml", ok=True,
        issues=[_issue(severity="info", code="I_X")]
    )
    assert r1.has_errors() is True
    assert r2.has_errors() is False
    assert r3.has_errors() is False


def test_to_text_groups_by_step_ascending():
    """Issues must appear grouped by step_index in ascending order, general last."""
    r = SyntaxReport(
        file="task.yaml", fmt="yaml", ok=False,
        issues=[
            _issue(step_index=2, component="AddDataset"),
            _issue(step_index=0, component="DateList"),
            _issue(step_index=None, code="E_PARSE"),  # general
        ],
    )
    text = r.to_text()
    pos_step0 = text.find("Step 0")
    pos_step2 = text.find("Step 2")
    pos_general = text.find("<General>")
    assert pos_step0 >= 0, "Step 0 section not found"
    assert pos_step2 >= 0, "Step 2 section not found"
    assert pos_general >= 0, "<General> section not found"
    assert pos_step0 < pos_step2 < pos_general


def test_to_text_orders_errors_before_warnings():
    """Within a step block, errors appear before warnings."""
    r = SyntaxReport(
        file="task.yaml", fmt="yaml", ok=False,
        issues=[
            _issue(step_index=0, severity="warning", code="W_A"),
            _issue(step_index=0, severity="error", code="E_A"),
        ],
    )
    text = r.to_text()
    assert text.find("E_A") < text.find("W_A")


def test_to_text_header_has_summary_counts():
    """Second line of to_text must contain error and warning counts."""
    r = SyntaxReport(
        file="task.yaml", fmt="yaml", ok=False,
        issues=[
            _issue(severity="error"),
            _issue(severity="warning", code="W_X"),
        ],
    )
    header_line = r.to_text().splitlines()[1]  # summary is second line
    assert "1 error" in header_line and "1 warning" in header_line


def test_to_text_ok_report_shows_ok():
    """A clean report should show OK in the summary."""
    r = SyntaxReport(file="task.yaml", fmt="yaml", ok=True)
    text = r.to_text()
    assert "OK" in text


def test_to_text_includes_file_and_format():
    """The header line must contain the filename and format."""
    r = SyntaxReport(file="my_task.yaml", fmt="yaml", ok=True)
    text = r.to_text()
    first_line = text.splitlines()[0]
    assert "my_task.yaml" in first_line
    assert "yaml" in first_line


def test_to_json_round_trips():
    """to_json output must round-trip via orjson without data loss."""
    r = SyntaxReport(
        file="t", fmt="yaml", ok=False,
        issues=[_issue(step_index=0, component="X")],
    )
    parsed = orjson.loads(r.to_json())
    assert parsed["file"] == "t"
    assert parsed["fmt"] == "yaml"
    assert parsed["ok"] is False
    assert parsed["issues"][0]["component"] == "X"


def test_to_json_has_trailing_newline():
    """to_json must end with a newline character for clean shell output."""
    r = SyntaxReport(file="t", fmt="yaml", ok=True)
    assert r.to_json().endswith("\n")


def test_to_json_has_required_keys():
    """to_json output must have file, fmt, ok, and issues keys."""
    r = SyntaxReport(file="t", fmt="json", ok=True)
    parsed = orjson.loads(r.to_json())
    assert set(parsed.keys()) >= {"file", "fmt", "ok", "issues"}
