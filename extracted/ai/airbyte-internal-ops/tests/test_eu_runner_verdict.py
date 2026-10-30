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
        "schema_version": 2,
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
        "totals": {
            "stream_count": 1,
            "control_record_count": 2,
            "target_record_count": 2,
        },
        "checks": [{"check_name": "Record counts", "passed": True}],
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
        {"check_name": "Command execution", "passed": True},
        {"check_name": "Spec compatibility", "passed": True},
    ]
    assert verdict["not_exercised"] is True
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
        lambda verdict: verdict.update({"not_exercised": "true"}),
        lambda verdict: verdict.update({"schema_version": 1}),
    ],
)
def test_verdict_requires_schema_v2_and_not_exercised_boolean(mutate) -> None:
    verdict = _valid_verdict()
    mutate(verdict)

    with pytest.raises(ValueError):
        validate_verdict(verdict)


@pytest.mark.parametrize("flag", ["incomplete", "not_exercised"])
def test_verdict_rejects_success_with_incomplete_or_not_exercised(flag) -> None:
    verdict = _valid_verdict()
    verdict.update({"success": True, flag: True})

    with pytest.raises(ValueError, match="success cannot be true"):
        validate_verdict(verdict)


@pytest.mark.parametrize("flag", ["incomplete", "not_exercised"])
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
        ({"regression_detected": True}, "failed"),
        ({"both_failed": True}, "failed"),
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
    for name in ("secret_stream_a", "secret_stream_b", "secret_stream_c"):
        assert name not in json.dumps(verdict)
        assert name not in summary
