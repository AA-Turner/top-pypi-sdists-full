"""Tests for the separate drift-check status contract."""

from unittest.mock import patch

from agentic_devtools.cli.phase0_review import drift_check


def test_drift_check_classifies_severity_and_status(make_review_case, tmp_path):
    payload, integrity = make_review_case()
    output, status = drift_check.run_drift_check(
        repo_root=tmp_path,
        input_path=payload,
        integrity_path=integrity,
    )
    assert status == 0
    assert "info:" in output

    payload, integrity = make_review_case(issue_title="Wrong")
    output, status = drift_check.run_drift_check(
        repo_root=tmp_path,
        input_path=payload,
        integrity_path=integrity,
    )
    assert status == 1
    assert "error:" in output


def test_main_prints_and_returns_status(capsys):
    with patch.object(drift_check, "run_drift_check", return_value=("info: clean", 0)):
        assert drift_check.main() == 0
    assert capsys.readouterr().out == "info: clean\n"


def test_drift_check_supplies_fallback_when_report_has_no_checks():
    with patch.object(drift_check, "run_review", return_value="## Verdict\nAPPROVED"):
        output, status = drift_check.run_drift_check()
    assert (output, status) == ("info: no drift findings", 0)


def test_drift_check_parses_checklist_lines_without_fixed_slicing():
    report = "- [ ]  template mismatch\n- [x]   clean section"
    with patch.object(drift_check, "run_review", return_value=report):
        output, status = drift_check.run_drift_check()
    assert (output, status) == ("error: template mismatch\ninfo: clean section", 1)
