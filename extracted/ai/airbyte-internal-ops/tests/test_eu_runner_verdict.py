# Copyright (c) 2026 Airbyte, Inc., all rights reserved.
"""Metadata-only EU verdict schema tests."""

from __future__ import annotations

import json

import pytest

from airbyte_ops_mcp.regression_tests.eu_runner.cli import render_summary
from airbyte_ops_mcp.regression_tests.eu_runner.verdict import (
    build_verdict,
    validate_verdict,
)


def _valid_verdict() -> dict:
    return {
        "schema_version": 3,
        "output_mode": "masked",
        "commands": [
            {
                "command": "read",
                "control_exit_code": 0,
                "target_exit_code": 0,
                "passed": True,
            }
        ],
        "success": True,
        "regression_detected": False,
        "both_failed": False,
        "incomplete": False,
        "not_exercised": False,
        "setup_error": False,
        "could_not_test": False,
        "strict_failed": False,
        "comparison_errored": False,
        "totals": {
            "stream_count": 1,
            "control_record_count": 2,
            "target_record_count": 2,
        },
        "checks": [{"check_name": "Record counts", "passed": True, "status": "pass"}],
    }


def test_verdict_projects_cli_report_to_metadata(tmp_path) -> None:
    command_dir = tmp_path / "read"
    command_dir.mkdir()
    report = {
        "output_mode": "masked",
        "target": {"exit_code": 0, "record_counts_per_stream": {"private_stream": 2}},
        "control": {"exit_code": 0, "record_counts_per_stream": {"private_stream": 2}},
        "success": True,
        "regression_detected": False,
        "both_failed": False,
        "incomplete": False,
        "not_exercised": True,
        "comparison": {"spec": {"passed": True}},
    }
    (command_dir / "regression_report.json").write_text(json.dumps(report))
    (tmp_path / "summary.json").write_text(json.dumps({"success": True}))

    verdict = build_verdict(tmp_path)

    validate_verdict(verdict)
    assert verdict["commands"][0]["command"] == "read"
    assert verdict["totals"] == {
        "stream_count": 1,
        "control_record_count": 2,
        "target_record_count": 2,
    }
    assert verdict["checks"] == [
        {
            "check_name": "Command execution",
            "passed": True,
            "status": "pass",
        },
    ]
    assert verdict["not_exercised"] is True
    assert verdict["setup_error"] is False
    assert verdict["could_not_test"] is False
    assert verdict["strict_failed"] is False
    assert verdict["comparison_errored"] is False
    assert "private_stream" not in json.dumps(verdict)


def test_spec_only_verdict_validates_as_success_and_summarizes_only_spec(
    tmp_path, capsys
) -> None:
    spec_dir = tmp_path / "spec"
    spec_dir.mkdir()
    report = {
        "output_mode": "masked",
        "target": {"exit_code": 0},
        "control": {"exit_code": 0},
        "success": True,
        "regression_detected": False,
        "both_failed": False,
        "incomplete": False,
        "comparison": {"spec": {"passed": True}},
    }
    (spec_dir / "regression_report.json").write_text(json.dumps(report))
    (tmp_path / "summary.json").write_text(
        json.dumps(
            {
                "success": True,
                "both_failed": False,
                "incomplete": False,
                "commands": [{"command": "spec", "exit_code": 0, "passed": True}],
            }
        )
    )

    verdict = build_verdict(tmp_path)

    validate_verdict(verdict)
    assert verdict["success"] is True
    assert verdict["not_exercised"] is False
    assert [item["command"] for item in verdict["commands"]] == ["spec"]

    verdict_path = tmp_path / "verdict.json"
    verdict_path.write_text(json.dumps(verdict))
    render_summary(
        batch_url="batch",
        logs_url="logs",
        report_url="report",
        verdict=verdict_path,
    )

    summary = capsys.readouterr().out
    assert "- **Result:** passed" in summary
    assert "| spec |" in summary
    assert "| check |" not in summary
    assert "| discover |" not in summary
    assert "- **Not exercised:** False" in summary


def test_verdict_reads_not_exercised_from_summary(tmp_path) -> None:
    (tmp_path / "summary.json").write_text(
        json.dumps({"success": False, "not_exercised": True})
    )

    verdict = build_verdict(tmp_path)

    assert verdict["not_exercised"] is True


@pytest.mark.parametrize("flag", ["strict_failed", "comparison_errored"])
def test_verdict_aggregates_label_inputs_from_reports_only(tmp_path, flag) -> None:
    read_dir = tmp_path / "read"
    read_dir.mkdir()
    (read_dir / "regression_report.json").write_text(
        json.dumps(
            {
                "output_mode": "masked",
                "success": True,
                flag: True,
            }
        )
    )
    (tmp_path / "summary.json").write_text(json.dumps({"success": True, flag: False}))

    verdict = build_verdict(tmp_path)

    assert verdict[flag] is True
    validate_verdict(verdict)


@pytest.mark.parametrize("flag", ["strict_failed", "comparison_errored"])
def test_verdict_does_not_read_label_inputs_from_summary(tmp_path, flag) -> None:
    (tmp_path / "summary.json").write_text(json.dumps({"success": True, flag: True}))

    verdict = build_verdict(tmp_path)

    assert verdict[flag] is False
    validate_verdict(verdict)


@pytest.mark.parametrize(
    ("source", "flag"),
    [
        ("report", "setup_error"),
        ("report", "could_not_test"),
        ("summary", "setup_error"),
        ("summary", "could_not_test"),
    ],
)
def test_verdict_reads_setup_and_config_errors_from_report_and_summary(
    tmp_path, source, flag
) -> None:
    if source == "report":
        read_dir = tmp_path / "read"
        read_dir.mkdir()
        (read_dir / "regression_report.json").write_text(
            json.dumps(
                {
                    "output_mode": "masked",
                    "success": False,
                    "regression_detected": False,
                    flag: True,
                }
            )
        )
        (tmp_path / "summary.json").write_text(json.dumps({"success": True}))
    else:
        (tmp_path / "summary.json").write_text(
            json.dumps({"success": False, flag: True})
        )

    verdict = build_verdict(tmp_path)

    assert verdict[flag] is True
    assert verdict["success"] is False


@pytest.mark.parametrize(
    ("name", "passed", "severity", "expected_status", "report_success"),
    [
        ("Record schema (new streams)", False, "diagnostic", "warn", True),
        ("Record schema (new streams)", False, "strict", "fail", False),
        ("Catalog schema", False, "diagnostic", "warn", True),
    ],
)
def test_verdict_projects_check_results_with_severity(
    tmp_path, name, passed, severity, expected_status, report_success
) -> None:
    read_dir = tmp_path / "read"
    read_dir.mkdir()
    (read_dir / "regression_report.json").write_text(
        json.dumps(
            {
                "output_mode": "masked",
                "target": {"exit_code": 0},
                "control": {"exit_code": 0},
                "success": report_success,
                "regression_detected": expected_status == "fail",
                "check_results": [
                    {"name": name, "passed": passed, "severity": severity}
                ],
            }
        )
    )
    (tmp_path / "summary.json").write_text(json.dumps({"success": True}))

    verdict = build_verdict(tmp_path)

    assert verdict["success"] is (expected_status != "fail")
    assert verdict["checks"][-1] == {
        "check_name": name,
        "passed": passed,
        "status": expected_status,
    }


def test_verdict_drops_unknown_and_invalid_check_results(tmp_path) -> None:
    read_dir = tmp_path / "read"
    read_dir.mkdir()
    (read_dir / "regression_report.json").write_text(
        json.dumps(
            {
                "output_mode": "masked",
                "target": {"exit_code": 0},
                "success": True,
                "check_results": [
                    {"name": "unrecognized", "passed": True, "severity": "strict"},
                    {
                        "name": "Record schema (new streams)",
                        "passed": "true",
                        "severity": "strict",
                    },
                ],
            }
        )
    )
    (tmp_path / "summary.json").write_text(json.dumps({"success": True}))

    verdict = build_verdict(tmp_path)

    assert verdict["checks"] == [
        {
            "check_name": "Command execution",
            "passed": True,
            "status": "pass",
        }
    ]


@pytest.mark.parametrize(
    ("report_success", "regression_detected", "summary_success"),
    [
        (False, True, True),
        (False, False, True),
        (True, True, True),
        (True, False, False),
    ],
    ids=[
        "regression-the-summary-passed",
        "report-success-false",
        "regression-detected-alone",
        "summary-failed",
    ],
)
def test_a_failing_cli_report_fails_the_verdict_whatever_the_summary_says(
    tmp_path, report_success, regression_detected, summary_success
) -> None:
    """The CLI exits 0 on a failed verdict, so the runner's summary can say
    success beside a report that found a regression (a spec compatibility
    failure did exactly that). A report can fail the verdict; it cannot pass
    one the summary failed, since a command that crashed wrote no report."""
    spec_dir = tmp_path / "spec"
    spec_dir.mkdir()
    report = {
        "output_mode": "masked",
        "target": {"exit_code": 0},
        "control": {"exit_code": 0},
        "success": report_success,
        "regression_detected": regression_detected,
        "both_failed": False,
        "incomplete": False,
        "comparison": {"spec": {"passed": not regression_detected}},
    }
    (spec_dir / "regression_report.json").write_text(json.dumps(report))
    (tmp_path / "summary.json").write_text(
        json.dumps(
            {
                "exit_code": 0,
                "success": summary_success,
                "both_failed": False,
                "incomplete": False,
                "commands": [
                    {"command": "spec", "exit_code": 0, "passed": summary_success}
                ],
            }
        )
    )

    verdict = build_verdict(tmp_path)

    validate_verdict(verdict)
    assert verdict["success"] is False
    assert verdict["regression_detected"] is regression_detected


def test_verdict_refuses_a_non_masked_cli_report(tmp_path) -> None:
    command_dir = tmp_path / "spec"
    command_dir.mkdir()
    (command_dir / "regression_report.json").write_text(
        json.dumps({"output_mode": "raw"})
    )

    with pytest.raises(ValueError, match="output_mode"):
        build_verdict(tmp_path)


@pytest.mark.parametrize(
    "mutate",
    [
        lambda verdict: verdict.update({"customer_name": "Alice"}),
        lambda verdict: verdict["commands"][0].update({"detail": "customer record"}),
        lambda verdict: verdict["commands"][0].update({"command": "private_stream"}),
        lambda verdict: verdict["totals"].update(
            {"target_record_count": "record-data"}
        ),
        lambda verdict: verdict["checks"][0].update({"check_name": "private_field"}),
        lambda verdict: verdict["checks"][0].update({"status": "private_value"}),
        lambda verdict: verdict["checks"][0].update({"status": "bad-status"}),
        lambda verdict: verdict["checks"][0].update({"passed": False}),
    ],
)
def test_verdict_rejects_unknown_or_record_like_values(mutate) -> None:
    verdict = _valid_verdict()
    mutate(verdict)

    with pytest.raises(ValueError):
        validate_verdict(verdict)


@pytest.mark.parametrize(
    "mutate",
    [
        lambda verdict: verdict.pop("not_exercised"),
        lambda verdict: verdict.pop("setup_error"),
        lambda verdict: verdict.update({"not_exercised": "true"}),
        lambda verdict: verdict.update({"setup_error": 1}),
        lambda verdict: verdict.update({"could_not_test": None}),
        lambda verdict: verdict.pop("strict_failed"),
        lambda verdict: verdict.pop("comparison_errored"),
        lambda verdict: verdict.update({"strict_failed": 1}),
        lambda verdict: verdict.update({"comparison_errored": "false"}),
        lambda verdict: verdict.update({"schema_version": 2}),
    ],
)
def test_verdict_requires_schema_v3_and_boolean_flags(mutate) -> None:
    verdict = _valid_verdict()
    mutate(verdict)

    with pytest.raises(ValueError):
        validate_verdict(verdict)


@pytest.mark.parametrize(
    "flag", ["incomplete", "not_exercised", "setup_error", "could_not_test"]
)
def test_verdict_rejects_success_with_incomplete_or_not_exercised(flag) -> None:
    verdict = _valid_verdict()
    verdict.update({"success": True, flag: True})

    with pytest.raises(ValueError, match="success cannot be true"):
        validate_verdict(verdict)


def test_verdict_allows_label_inputs_on_a_successful_report() -> None:
    verdict = _valid_verdict()
    verdict.update({"strict_failed": True, "comparison_errored": True})

    validate_verdict(verdict)


@pytest.mark.parametrize(
    "flag", ["incomplete", "not_exercised", "setup_error", "could_not_test"]
)
def test_build_verdict_forces_failure_for_incomplete_or_not_exercised(
    tmp_path, flag
) -> None:
    (tmp_path / "summary.json").write_text(json.dumps({"success": True, flag: True}))

    verdict = build_verdict(tmp_path)

    assert verdict["success"] is False
    assert verdict[flag] is True


def test_render_summary_uses_validated_verdict(tmp_path, capsys) -> None:
    verdict = _valid_verdict()
    verdict.update({"success": False, "both_failed": True, "incomplete": True})
    verdict_path = tmp_path / "verdict.json"
    verdict_path.write_text(json.dumps(verdict))

    render_summary(
        batch_url="batch",
        logs_url="logs",
        report_url="report",
        verdict=verdict_path,
    )

    summary = capsys.readouterr().out
    assert "- **Result:** INCOMPLETE" in summary
    assert "- **Both failed:** True" in summary
    assert "- **Incomplete:** True" in summary
    assert "- **Not exercised:** False" in summary


@pytest.mark.parametrize(
    ("flags", "expected"),
    [
        ({}, "NOT EXERCISED"),
        ({"regression_detected": True}, "FAIL (regression)"),
        ({"both_failed": True}, "FAIL (inconclusive)"),
        ({"incomplete": True}, "INCOMPLETE"),
    ],
)
def test_render_summary_ranks_not_exercised_below_fail(
    tmp_path, capsys, flags, expected
) -> None:
    verdict = _valid_verdict()
    verdict.update({"success": False, "not_exercised": True, **flags})
    verdict_path = tmp_path / "verdict.json"
    verdict_path.write_text(json.dumps(verdict))

    render_summary(
        batch_url="batch",
        logs_url="logs",
        report_url="report",
        verdict=verdict_path,
    )

    summary = capsys.readouterr().out
    assert f"- **Result:** {expected}\n" in summary
    assert "- **Not exercised:** True" in summary


@pytest.mark.parametrize(
    ("flag", "expected"),
    [
        ("setup_error", "SETUP ERROR"),
        ("could_not_test", "COULD NOT TEST (config error)"),
    ],
)
def test_render_summary_shows_setup_and_config_error_labels(
    tmp_path, capsys, flag, expected
) -> None:
    verdict = _valid_verdict()
    verdict.update({"success": False, flag: True})
    verdict_path = tmp_path / "verdict.json"
    verdict_path.write_text(json.dumps(verdict))

    render_summary(
        batch_url="batch",
        logs_url="logs",
        report_url="report",
        verdict=verdict_path,
    )

    summary = capsys.readouterr().out
    assert f"- **Result:** {expected}" in summary
    assert f"- **Setup error:** {flag == 'setup_error'}" in summary
    assert f"- **Could not test:** {flag == 'could_not_test'}" in summary


@pytest.mark.parametrize(
    ("strict_failed", "expected"),
    [
        (True, "FAIL (regression)"),
        (False, "COULD NOT TEST (config error)"),
    ],
)
def test_render_summary_ranks_strict_check_failure_with_could_not_test(
    tmp_path, capsys, strict_failed, expected
) -> None:
    verdict = _valid_verdict()
    verdict.update(
        {
            "success": False,
            "regression_detected": False,
            "could_not_test": True,
            "strict_failed": strict_failed,
            "comparison_errored": False,
            "checks": [
                {
                    "check_name": "Record counts",
                    "passed": False,
                    "status": "fail",
                }
            ],
        }
    )
    verdict_path = tmp_path / "verdict.json"
    verdict_path.write_text(json.dumps(verdict))

    render_summary(
        batch_url="batch",
        logs_url="logs",
        report_url="report",
        verdict=verdict_path,
    )

    summary = capsys.readouterr().out
    assert f"- **Result:** {expected}" in summary


def test_render_summary_uses_comparison_error_flag_with_not_exercised(
    tmp_path, capsys
) -> None:
    verdict = _valid_verdict()
    verdict.update(
        {
            "success": False,
            "not_exercised": True,
            "strict_failed": False,
            "comparison_errored": True,
            "checks": [
                {
                    "check_name": "Record counts",
                    "passed": False,
                    "status": "fail",
                }
            ],
        }
    )
    verdict_path = tmp_path / "verdict.json"
    verdict_path.write_text(json.dumps(verdict))

    render_summary(
        batch_url="batch",
        logs_url="logs",
        report_url="report",
        verdict=verdict_path,
    )

    summary = capsys.readouterr().out
    assert "- **Result:** FAIL (inconclusive)" in summary


def test_render_summary_does_not_echo_invalid_verdict(tmp_path, capsys) -> None:
    verdict_path = tmp_path / "verdict.json"
    verdict_path.write_text('{"success": "private customer data"}')

    render_summary(
        batch_url="batch",
        logs_url="logs",
        report_url="report",
        verdict=verdict_path,
    )

    summary = capsys.readouterr().out
    assert "verdict missing or invalid" in summary
    assert "private customer data" not in summary


def test_not_exercised_stream_names_do_not_enter_verdict_or_summary(
    tmp_path, capsys
) -> None:
    read_dir = tmp_path / "read"
    read_dir.mkdir()
    report = {
        "output_mode": "masked",
        "target": {"exit_code": 0, "record_counts_per_stream": {"secret_stream_a": 0}},
        "control": {"exit_code": 0},
        "success": False,
        "regression_detected": False,
        "both_failed": False,
        "incomplete": False,
        "not_exercised": True,
        "not_exercised_streams": ["secret_stream_a"],
        "checks": [
            {
                "check_name": "Record counts",
                "passed": True,
                "stream": "secret_stream_b",
            }
        ],
        "record_checks": {"secret_stream_d": {"secret_field": "secret_value"}},
        "record_comparison": {
            "checks": {"secret_stream_e": {"secret_field": "secret_value"}},
            "streams": ["secret_stream_f"],
        },
        "comparison": {
            "final_state": {
                "secret_stream_g": {"passed": False, "value": "secret_value"}
            }
        },
        "check_results": [
            {
                "name": "Record schema (new streams)",
                "passed": False,
                "severity": "diagnostic",
                "stream": "secret_stream_h",
                "summary": "secret_value",
            }
        ],
    }
    (read_dir / "regression_report.json").write_text(json.dumps(report))
    (read_dir / "stream_injection.json").write_text(
        json.dumps({"new_streams": ["secret_stream_c"]})
    )

    verdict = build_verdict(tmp_path)
    verdict_path = tmp_path / "verdict.json"
    verdict_path.write_text(json.dumps(verdict))
    render_summary(
        batch_url="batch",
        logs_url="logs",
        report_url="report",
        verdict=verdict_path,
    )

    summary = capsys.readouterr().out
    assert "- **Result:** NOT EXERCISED" in summary
    for name in (
        "secret_stream_a",
        "secret_stream_b",
        "secret_stream_c",
        "secret_stream_d",
        "secret_stream_e",
        "secret_stream_f",
        "secret_stream_g",
        "secret_stream_h",
        "secret_value",
    ):
        assert name not in json.dumps(verdict)
        assert name not in summary
