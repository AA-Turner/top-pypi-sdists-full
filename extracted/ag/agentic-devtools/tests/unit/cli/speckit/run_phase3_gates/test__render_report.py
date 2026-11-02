"""Tests for report rendering from the persisted gate result model."""

import pytest

from agentic_devtools.cli.speckit.run_phase3_gates import _render_report


def test_renders_required_sections_skips_findings_and_metrics() -> None:
    result = {
        "hierarchy_level": "epic",
        "spec_dir": "specs/001",
        "status": "passed_with_warnings",
        "gates": {
            "fr_validation": {"status": "skipped", "skip_reason": "epic level", "findings": [], "metrics": {}},
            "test_coverage": {"status": "skipped", "skip_reason": "epic level", "findings": [], "metrics": {}},
            "artifact_path_verification": {
                "status": "skipped",
                "skip_reason": "epic level",
                "findings": [],
                "metrics": {},
            },
            "pass_g": {
                "status": "passed_with_warnings",
                "findings": [
                    {
                        "severity": "HIGH",
                        "status": "invalid",
                        "reference": {"text": "missing.py", "plan_location": "L10"},
                        "candidates": [],
                        "explanation": "No matching file exists.",
                    }
                ],
                "metrics": {},
            },
        },
    }

    report = _render_report(result)

    for heading in (
        "## Coverage Summary",
        "## E.2 Test Coverage",
        "## Artifact Path Verification",
        "## Pass G Findings",
    ):
        assert heading in report
    assert "Skipped: epic level" in report
    assert "HIGH" in report
    assert "missing.py" in report


def test_rejects_non_string_test_coverage_summary_table() -> None:
    result = {
        "hierarchy_level": "feature",
        "spec_dir": "specs/001",
        "status": "passed",
        "gates": {
            "fr_validation": {"status": "passed", "findings": [], "metrics": {}},
            "test_coverage": {
                "status": "passed",
                "findings": [],
                "metrics": {"summary_table": None},
            },
            "artifact_path_verification": {"status": "passed", "findings": [], "metrics": {}},
            "pass_g": {"status": "passed", "findings": [], "metrics": {}},
        },
    }

    with pytest.raises(RuntimeError, match="summary_table must be a string"):
        _render_report(result)


def test_renders_artifact_path_findings() -> None:
    result = {
        "hierarchy_level": "feature",
        "spec_dir": "specs/001",
        "status": "failed",
        "gates": {
            "fr_validation": {"status": "passed", "findings": [], "metrics": {}},
            "test_coverage": {"status": "passed", "findings": [], "metrics": {"summary_table": ""}},
            "artifact_path_verification": {
                "status": "failed",
                "findings": [{"check": "referenced-path", "detail": "missing file"}],
                "metrics": {"checks_run": ["referenced-path"]},
            },
            "pass_g": {"status": "passed", "findings": [], "metrics": {}},
        },
    }

    report = _render_report(result)

    assert "**HIGH** referenced-path: missing file" in report
