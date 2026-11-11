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
from airbyte_ops_mcp.regression_tests.models import StreamError
from airbyte_ops_mcp.regression_tests.report import (
    build_comparison_report_model,
    build_single_version_report_model,
)


@pytest.mark.parametrize("single", [False, True])
@pytest.mark.parametrize("command_passed", [False, True])
@pytest.mark.parametrize("config_error", [False, True])
def test_failed_new_stream_command_label_matches_us(
    tmp_path, capsys, single, command_passed, config_error
):
    target = {
        "success": command_passed,
        "exit_code": 0 if command_passed else 1,
        "record_counts_per_stream": {},
    }
    if single:
        model = build_single_version_report_model(
            connector_image="source-test:2",
            command="read",
            result=target,
            target_only_streams=("new",),
            stream_errors={"new": [StreamError("config_error", "Missing permission")]}
            if config_error
            else {},
            include_report_sections=False,
        )
    else:
        target["could_not_test"] = config_error
        target["excluded_not_exercised_streams"] = ("new",) if config_error else ()
        model = build_comparison_report_model(
            target_image="source-test:2",
            control_image="source-test:1",
            command="read",
            target_result=target,
            control_result={"success": True, "exit_code": 0},
            target_only_streams=("new",),
            include_report_sections=False,
        )
    report = {
        **model.verdict_flags(),
        "command": "read",
        "output_mode": "masked",
        "target": target,
        "check_results": model.check_results(),
    }
    if not single:
        report["control"] = {"success": True, "exit_code": 0}
    (tmp_path / "regression_report.json").write_text(json.dumps(report))
    verdict = build_verdict(tmp_path)
    validate_verdict(verdict)
    verdict_path = tmp_path / "verdict.json"
    verdict_path.write_text(json.dumps(verdict))
    render_summary(
        batch_url="batch", logs_url="logs", report_url="report", verdict=verdict_path
    )
    assert f"- **Result:** {model.verdict_label}\n" in capsys.readouterr().out
    if single and not command_passed:
        assert model.verdict_label == (
            "COULD NOT TEST (config error)" if config_error else "FAIL"
        )
    assert verdict["not_exercised"] is (not config_error)
    assert verdict["could_not_test"] is config_error


@pytest.mark.parametrize("precedence", ["stopped", "setup"])
@pytest.mark.parametrize("command", ["read", "check"])
def test_failed_single_command_retains_stopped_and_setup_labels(
    tmp_path, capsys, precedence, command
):
    result = {"success": False, "exit_code": 1, "record_counts_per_stream": {}}
    if precedence == "stopped":
        result["stopped_early"] = {"reason": "cap", "records_seen": 0, "elapsed_s": 1}
    model = build_single_version_report_model(
        connector_image="source-test:2",
        command=command,
        result=result,
        target_only_streams=("new",),
        stream_statuses={"new": ["INCOMPLETE"]} if precedence == "setup" else {},
        include_report_sections=False,
    )
    assert model.verdict_label == (
        "INCOMPLETE" if precedence == "stopped" else "SETUP ERROR"
    )
    (tmp_path / "regression_report.json").write_text(
        json.dumps(
            {
                **model.verdict_flags(),
                "command": command,
                "output_mode": "masked",
                "target": result,
                "check_results": model.check_results(),
            }
        )
    )
    verdict_path = tmp_path / "verdict.json"
    verdict_path.write_text(json.dumps(build_verdict(tmp_path)))
    render_summary(
        batch_url="batch", logs_url="logs", report_url="report", verdict=verdict_path
    )
    assert f"- **Result:** {model.verdict_label}\n" in capsys.readouterr().out


@pytest.mark.parametrize("single", [False, True])
@pytest.mark.parametrize("warn", [False, True])
def test_model_checks_reach_metadata_only_verdict(tmp_path, single, warn):
    target = {
        "success": True,
        "exit_code": 0,
        "record_counts_per_stream": {} if warn else {"items": 2},
        "http_metrics": {
            "flow_count": 20,
            "replayed_flow_count": 10 if warn else 20,
            "live_flow_count": 10 if warn else 0,
            "replay_source": "private/path",
            "connector_request_count": 40,
            "connector_cache_hits_count": 0 if warn else 20,
        },
    }
    control = {
        "success": True,
        "exit_code": 0,
        "record_counts_per_stream": {} if warn else {"items": 2},
        "http_metrics": {
            "connector_request_count": 40,
            "connector_cache_hits_count": 20,
        },
    }
    if single:
        model = build_single_version_report_model(
            connector_image="source-test:2",
            command="read",
            result=target,
            configured_streams=("items",),
        )
    else:
        model = build_comparison_report_model(
            target_image="source-test:2",
            control_image="source-test:1",
            command="read",
            target_result=target,
            control_result=control,
            configured_streams=("items",),
        )
    report = {
        **model.verdict_flags(),
        "command": "read",
        "output_mode": "masked",
        "target": target,
        "check_results": model.check_results(),
    }
    if not single:
        report["control"] = control
    (tmp_path / "regression_report.json").write_text(json.dumps(report))
    verdict = build_verdict(tmp_path)
    validate_verdict(verdict)
    assert verdict["success"] is True
    assert verdict["commands"][0]["control_exit_code"] == (None if single else 0)
    names = (
        {"Stream coverage"}
        if single
        else {
            "Stream coverage",
            "HTTP replay coverage",
            "Connector cache hit ratio",
        }
    )
    expected = [
        {"check_name": name, "passed": not warn, "status": "warn" if warn else "pass"}
        for name in names
    ]
    assert sorted(
        verdict["checks"][1:], key=lambda check: check["check_name"]
    ) == sorted(expected, key=lambda check: check["check_name"])
    assert all(
        set(row) == {"name", "passed", "severity"} for row in report["check_results"]
    )
    assert all("summary" not in row for row in verdict["checks"])


@pytest.mark.parametrize("records", [0, 2])
def test_new_stream_coverage_is_metadata_only(tmp_path, records):
    stream = "private_new_stream"
    target = {
        "success": True,
        "exit_code": 0,
        "record_counts_per_stream": {stream: records},
    }
    control = {"success": True, "exit_code": 0}
    model = build_comparison_report_model(
        target_image="source-test:2",
        control_image="source-test:1",
        command="read",
        target_result=target,
        control_result=control,
        target_only_streams=(stream,),
        include_report_sections=False,
    )
    report = {
        **model.verdict_flags(),
        "command": "read",
        "output_mode": "masked",
        "target": target,
        "control": control,
        "check_results": model.check_results(),
    }
    (tmp_path / "regression_report.json").write_text(json.dumps(report))
    verdict = build_verdict(tmp_path)
    assert verdict["schema_version"] == 4
    assert {
        "check_name": "Stream coverage (new streams)",
        "passed": bool(records),
        "status": "pass" if records else "fail",
    } in verdict["checks"]
    assert all(
        set(row) == {"check_name", "passed", "status"} for row in verdict["checks"]
    )
    assert stream not in json.dumps(verdict)
    validate_verdict(verdict)


@pytest.mark.parametrize("single", [False, True])
@pytest.mark.parametrize("report_success", [False, True])
@pytest.mark.parametrize(
    ("summary_commands", "summary_passed"),
    [
        ([{"command": "check", "exit_code": 1, "passed": False}], False),
        ([{"command": "check", "exit_code": 0, "passed": True}], True),
        ([{"command": "check", "exit_code": 1, "passed": True}], False),
        ([{"command": "check", "exit_code": 0, "passed": False}], False),
        ([{"command": "check", "exit_code": 1}], False),
        ([{"command": "check", "passed": False}], False),
        ([{"command": "check"}], True),
        ([{"command": "read", "exit_code": 1, "passed": False}], True),
        ([], True),
        (None, True),
    ],
)
def test_report_command_pass_requires_matching_summary_to_pass(
    tmp_path, single, report_success, summary_commands, summary_passed
):
    report = {
        "command": "check",
        "success": report_success,
        "output_mode": "masked",
        "target": {"exit_code": 0},
    }
    if not single:
        report["control"] = {"exit_code": 0}
    (tmp_path / "regression_report.json").write_text(json.dumps(report))
    (tmp_path / "summary.json").write_text(json.dumps({"commands": summary_commands}))

    verdict = build_verdict(tmp_path)

    assert verdict["commands"][0]["passed"] is (report_success and summary_passed)
    assert verdict["success"] is (report_success and summary_passed)
    assert verdict["schema_version"] == 4


@pytest.mark.parametrize("single", [False, True])
@pytest.mark.parametrize("status", ["FAILED", "SUCCEEDED"])
def test_check_execution_row_uses_model_connection_status(tmp_path, single, status):
    target = {"success": True, "exit_code": 0, "connection_status": status}
    control = {"success": True, "exit_code": 0, "connection_status": "SUCCEEDED"}
    if single:
        model = build_single_version_report_model(
            connector_image="source-test:2", command="check", result=target
        )
    else:
        model = build_comparison_report_model(
            target_image="source-test:2",
            control_image="source-test:1",
            command="check",
            target_result=target,
            control_result=control,
        )
    report = {
        **model.verdict_flags(),
        "command": "check",
        "output_mode": "masked",
        "target": target,
        "check_results": model.check_results(),
    }
    if not single:
        report["control"] = control
    (tmp_path / "regression_report.json").write_text(json.dumps(report))

    verdict = build_verdict(tmp_path)

    passed = status == "SUCCEEDED"
    assert verdict["success"] is passed
    assert verdict["commands"][0]["passed"] is passed
    assert verdict["checks"] == [
        {
            "check_name": "Command execution",
            "passed": passed,
            "status": "pass" if passed else "fail",
        }
    ]
    assert report["check_results"] == [
        {"name": "Command execution", "passed": passed, "severity": "strict"}
    ]
    assert verdict["schema_version"] == 4


@pytest.mark.parametrize(
    "check_results",
    [[], [{"name": "Command execution", "passed": "false", "severity": "strict"}]],
)
@pytest.mark.parametrize("exit_code", [0, 1])
def test_command_execution_falls_back_to_exit_code_without_a_valid_report_row(
    tmp_path, check_results, exit_code
):
    report = {
        "command": "check",
        "success": exit_code == 0,
        "output_mode": "masked",
        "target": {"exit_code": exit_code},
        "check_results": check_results,
    }
    (tmp_path / "regression_report.json").write_text(json.dumps(report))

    verdict = build_verdict(tmp_path)

    assert verdict["checks"] == [
        {
            "check_name": "Command execution",
            "passed": exit_code == 0,
            "status": "pass" if exit_code == 0 else "fail",
        }
    ]


def test_schema_four_exports_only_partial_boolean(tmp_path):
    model = build_single_version_report_model(
        connector_image="source-test:2",
        command="read",
        result={
            "success": True,
            "exit_code": 0,
            "record_counts_per_stream": {"private_new_stream": 2},
            "stopped_early": {"reason": "cap", "records_seen": 2, "elapsed_s": 1},
        },
        target_only_streams=("private_new_stream",),
        include_report_sections=False,
    )
    assert model.exercised_partial
    report = {
        **model.verdict_flags(),
        "command": "read",
        "output_mode": "masked",
        "target": {"exit_code": 0},
        "check_results": model.check_results(),
        "partial_streams": list(model.partial_streams),
    }
    (tmp_path / "regression_report.json").write_text(json.dumps(report))
    verdict = build_verdict(tmp_path)
    validate_verdict(verdict)
    assert verdict["schema_version"] == 4
    serialized = json.dumps(verdict)
    assert verdict["exercised_partial"] is True
    assert "partial_streams" not in serialized
    assert "private_new_stream" not in serialized


def _valid_verdict() -> dict:
    return {
        "schema_version": 4,
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
        "exercised_partial": False,
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
        ("Stream coverage", True, "strict", "pass", True),
        ("Stream coverage", False, "diagnostic", "warn", True),
        ("HTTP replay coverage", True, "strict", "pass", True),
        ("HTTP replay coverage", False, "diagnostic", "warn", True),
        ("Connector cache hit ratio", True, "strict", "pass", True),
        ("Connector cache hit ratio", False, "diagnostic", "warn", True),
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
    one the summary failed, including a crash after the report was written."""
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
def test_verdict_requires_supported_schema_and_boolean_flags(mutate) -> None:
    verdict = _valid_verdict()
    mutate(verdict)

    with pytest.raises(ValueError):
        validate_verdict(verdict)


@pytest.mark.parametrize("version", [3, 4])
def test_verdict_schema_round_trip(version):
    verdict = _valid_verdict()
    verdict["schema_version"] = version
    if version == 3:
        verdict.pop("exercised_partial")
    validate_verdict(json.loads(json.dumps(verdict)))


@pytest.mark.parametrize(
    "mutate",
    [
        lambda verdict: verdict.pop("exercised_partial"),
        lambda verdict: verdict.update(exercised_partial="true"),
        lambda verdict: verdict.update(exercised_partial=1),
        lambda verdict: verdict.update(
            exercised_partial=True, incomplete=False, success=False
        ),
        lambda verdict: verdict.update(
            exercised_partial=True, incomplete=True, success=True
        ),
        lambda verdict: verdict.update(schema_version=3),
    ],
)
def test_partial_verdict_requires_exact_version_keys_and_invariants(mutate):
    verdict = _valid_verdict()
    mutate(verdict)
    with pytest.raises(ValueError):
        validate_verdict(verdict)


@pytest.mark.parametrize("flag", [None, False, "true", 1, True])
@pytest.mark.parametrize(
    "incomplete,success", [(False, False), (True, True), (True, False)]
)
def test_partial_projection_requires_valid_report_evidence(
    tmp_path, flag, incomplete, success
):
    report = {
        "command": "read",
        "output_mode": "masked",
        "success": success,
        "incomplete": incomplete,
        "exercised_partial": flag,
    }
    (tmp_path / "regression_report.json").write_text(json.dumps(report))
    verdict = build_verdict(tmp_path)
    assert verdict["exercised_partial"] is (flag is True and incomplete and not success)


@pytest.mark.parametrize("version,partial", [(3, False), (4, False), (4, True)])
def test_render_summary_accepts_both_schema_versions(
    tmp_path, capsys, version, partial
):
    verdict = _valid_verdict()
    verdict.update(schema_version=version, success=not partial, incomplete=partial)
    if version == 3:
        verdict.pop("exercised_partial")
    else:
        verdict["exercised_partial"] = partial
    path = tmp_path / "verdict.json"
    path.write_text(json.dumps(verdict))
    render_summary(
        batch_url="batch", logs_url="logs", report_url="report", verdict=path
    )
    summary = capsys.readouterr().out
    assert (
        "Exercised (partial): New streams emitted records before the read stopped"
        in summary
    ) is partial
    assert ("INCOMPLETE" in summary) is partial


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
