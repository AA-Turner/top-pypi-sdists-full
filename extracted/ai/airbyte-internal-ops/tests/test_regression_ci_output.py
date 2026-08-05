# Copyright (c) 2025 Airbyte, Inc., all rights reserved.
"""Unit tests for regression test comparison outcome evaluation."""

import pytest

from airbyte_ops_mcp.regression_tests.ci_output import (
    command_result_succeeded,
    evaluate_comparison_outcome,
    generate_action_test_comparison_report,
    generate_single_version_report,
)


def _expected(
    *,
    success: bool,
    regression_detected: bool = False,
    both_failed: bool = False,
    control_failed_only: bool = False,
    check_improvement: bool = False,
    both_succeeded: bool = False,
) -> dict[str, bool]:
    """Build a full expected-outcome mapping, defaulting every flag to False."""
    return {
        "success": success,
        "regression_detected": regression_detected,
        "both_failed": both_failed,
        "control_failed_only": control_failed_only,
        "check_improvement": check_improvement,
        "both_succeeded": both_succeeded,
    }


@pytest.mark.parametrize(
    "command,target_result,control_result,expected",
    [
        pytest.param(
            "spec",
            {"success": False},
            {"success": False},
            _expected(success=False, both_failed=True),
            id="both-failed",
        ),
        pytest.param(
            "discover",
            {"success": False},
            {"success": True},
            _expected(success=False, regression_detected=True),
            id="target-fails-control-succeeds",
        ),
        pytest.param(
            "read",
            {"success": True},
            {"success": False},
            _expected(success=False, control_failed_only=True),
            id="control-fails-target-succeeds-is-inconclusive",
        ),
        pytest.param(
            "check",
            {"success": True, "connection_status": "SUCCEEDED"},
            {"success": True, "connection_status": "FAILED"},
            _expected(success=True, control_failed_only=True, check_improvement=True),
            id="check-improvement",
        ),
        pytest.param(
            "check",
            {"success": True, "connection_status": "FAILED"},
            {"success": True, "connection_status": "SUCCEEDED"},
            _expected(success=False, regression_detected=True),
            id="check-regression",
        ),
        pytest.param(
            "check",
            {"success": True, "connection_status": "FAILED"},
            {"success": True, "connection_status": "FAILED"},
            _expected(success=False, both_failed=True),
            id="check-both-failed",
        ),
        pytest.param(
            "spec",
            {"success": True},
            {"success": True},
            _expected(success=True, both_succeeded=True),
            id="both-succeed",
        ),
        pytest.param(
            "check",
            {"success": False},
            {"success": True},
            _expected(success=False, both_failed=True),
            id="check-missing-status-fails-closed",
        ),
        pytest.param(
            "check",
            {"success": False},
            {"success": True, "connection_status": "SUCCEEDED"},
            _expected(success=False, regression_detected=True),
            id="check-target-crash-control-succeeds",
        ),
        pytest.param(
            "check",
            {"success": False, "connection_status": "SUCCEEDED"},
            {"success": True, "connection_status": "FAILED"},
            _expected(success=False, both_failed=True),
            id="check-target-status-succeeds-but-exit-fails",
        ),
        pytest.param(
            "check",
            {"success": True, "connection_status": "SUCCEEDED"},
            {"success": True},
            _expected(success=False, control_failed_only=True),
            id="check-control-status-missing-is-inconclusive-not-an-improvement",
        ),
        pytest.param(
            "check",
            {"success": False, "connection_status": "SUCCEEDED"},
            {"success": True, "connection_status": "SUCCEEDED"},
            _expected(success=False, regression_detected=True),
            id="check-target-crashed-after-succeeded-status",
        ),
        pytest.param(
            "check",
            {"success": True, "connection_status": "SUCCEEDED"},
            {"success": False, "connection_status": "FAILED"},
            _expected(success=False, control_failed_only=True),
            id="check-control-crashed-is-not-an-improvement",
        ),
    ],
)
def test_evaluate_comparison_outcome(command, target_result, control_result, expected):
    outcome = evaluate_comparison_outcome(command, target_result, control_result)

    assert {
        "success": outcome.success,
        "regression_detected": outcome.regression_detected,
        "both_failed": outcome.both_failed,
        "control_failed_only": outcome.control_failed_only,
        "check_improvement": outcome.check_improvement,
        "both_succeeded": outcome.both_succeeded,
    } == expected


@pytest.mark.parametrize(
    "command,target_result,control_result",
    [
        ("spec", {"success": True}, {"success": True}),
        ("read", {"success": True}, {"success": False}),
        ("read", {"success": False}, {"success": True}),
        ("read", {"success": False}, {"success": False}),
        (
            "check",
            {"success": True, "connection_status": "SUCCEEDED"},
            {"success": True, "connection_status": "FAILED"},
        ),
        (
            "check",
            {"success": True, "connection_status": "FAILED"},
            {"success": True, "connection_status": "FAILED"},
        ),
        ("check", {"success": True}, {"success": True}),
    ],
)
def test_outcome_states_are_mutually_exclusive(command, target_result, control_result):
    """Exactly one of the four terminal states holds, and only a pass is a pass."""
    outcome = evaluate_comparison_outcome(command, target_result, control_result)

    states = [
        outcome.both_succeeded,
        outcome.regression_detected,
        outcome.both_failed,
        outcome.control_failed_only,
    ]
    assert sum(states) == 1

    # check_improvement is a sub-case of control_failed_only, and is the only
    # way a run that is not both_succeeded can still pass.
    assert not outcome.check_improvement or outcome.control_failed_only
    assert outcome.success == (outcome.both_succeeded or outcome.check_improvement)


def _run_result(success: bool, **extra) -> dict:
    """Build a minimal run-result dict of the shape the report generator expects."""
    return {"success": success, "exit_code": 0 if success else 1, **extra}


@pytest.mark.parametrize(
    "command,target_result,control_result,expected_fragment",
    [
        pytest.param(
            "read",
            _run_result(True),
            _run_result(True),
            "Both versions succeeded (no regression)",
            id="both-succeed",
        ),
        pytest.param(
            "read",
            _run_result(False),
            _run_result(True),
            "Target failed (exit 1), control succeeded — **REGRESSION DETECTED**",
            id="regression",
        ),
        pytest.param(
            "read",
            _run_result(False),
            _run_result(False),
            "Target failed (exit 1), control failed (exit 1) — **TEST FAILED**",
            id="both-failed-is-not-a-pass",
        ),
        pytest.param(
            "read",
            _run_result(True),
            _run_result(False),
            "Target succeeded, control failed (exit 1) — **TEST FAILED**",
            id="control-only-failure-is-not-an-improvement",
        ),
        pytest.param(
            "check",
            _run_result(True, connection_status="SUCCEEDED"),
            _run_result(True, connection_status="FAILED"),
            "Target connectionStatus SUCCEEDED, control connectionStatus FAILED — improvement",
            id="check-improvement",
        ),
        pytest.param(
            "check",
            {"success": False, "exit_code": 137, "connection_status": "SUCCEEDED"},
            _run_result(True, connection_status="SUCCEEDED"),
            "Target exited 137 after reporting connectionStatus SUCCEEDED",
            id="check-target-crashed-after-succeeded-is-not-described-as-failed",
        ),
        pytest.param(
            "check",
            {"success": False, "exit_code": 1},
            _run_result(True, connection_status="SUCCEEDED"),
            "Target exited 1 with no connectionStatus",
            id="check-target-missing-status-is-described-as-missing",
        ),
        pytest.param(
            "check",
            _run_result(True, connection_status="SUCCEEDED"),
            _run_result(True),
            "control exited 0 but reported no connectionStatus",
            id="check-control-clean-exit-without-status",
        ),
    ],
)
def test_report_result_line(
    tmp_path, command, target_result, control_result, expected_fragment
):
    """The report's Result line matches the verdict, including the failure cases."""
    report = generate_action_test_comparison_report(
        target_image="airbyte/source-test:2.0.0",
        control_image="airbyte/source-test:1.0.0",
        command=command,
        target_result=target_result,
        control_result=control_result,
        output_dir=tmp_path,
    )

    assert expected_fragment in report.read_text()


def test_a_comparison_failure_overrides_the_both_succeeded_result_line(tmp_path):
    """Two clean exits are not a pass when the comparison found a change.

    The markdown report derives its own Result line, so a finding that reaches
    the CLI verdict and the HTML report has to reach this one too -- otherwise
    the same run is a pass in one artifact and a regression in the other.
    """
    report = generate_action_test_comparison_report(
        target_image="airbyte/source-test:2.0.0",
        control_image="airbyte/source-test:1.0.0",
        command="spec",
        target_result=_run_result(True),
        control_result=_run_result(True),
        output_dir=tmp_path,
        comparison_findings=[
            ("fail", "Spec compatibility: `properties.start_date` was removed")
        ],
    )
    content = report.read_text()

    assert "**REGRESSION DETECTED**" in content
    assert "no regression" not in content
    assert "- ❌ Spec compatibility: `properties.start_date` was removed" in content


def test_a_comparison_warning_is_listed_without_changing_the_verdict(tmp_path):
    """An additive catalog change does not gate, but it is not invisible either.

    This file is the copy people paste around, and it was the one surface that
    showed nothing at all where the report and the step summary showed a warning.
    """
    report = generate_action_test_comparison_report(
        target_image="airbyte/source-test:2.0.0",
        control_image="airbyte/source-test:1.0.0",
        command="discover",
        target_result=_run_result(True),
        control_result=_run_result(True),
        output_dir=tmp_path,
        comparison_findings=[
            ("warn", "Catalog schema: Discovered catalog: 1 stream new in the target")
        ],
    )
    content = report.read_text()

    assert "**Result:** Both versions succeeded (no regression)" in content
    assert "**REGRESSION DETECTED**" not in content
    assert "- ⚠️ Catalog schema: Discovered catalog: 1 stream new in the target" in (
        content
    )


@pytest.mark.parametrize(
    "command,result,expected",
    [
        pytest.param("spec", {"success": True}, True, id="spec-clean-exit-passes"),
        pytest.param("read", {"success": False}, False, id="read-nonzero-exit-fails"),
        pytest.param(
            "check",
            {"success": True, "connection_status": "SUCCEEDED"},
            True,
            id="check-connected",
        ),
        pytest.param(
            "check",
            {"success": True, "connection_status": "FAILED"},
            False,
            id="check-failed-status-despite-clean-exit",
        ),
        pytest.param(
            "check",
            {"success": True, "connection_status": None},
            False,
            id="check-missing-status-fails-closed",
        ),
        pytest.param(
            "check",
            {"success": False, "connection_status": "SUCCEEDED"},
            False,
            id="check-nonzero-exit-fails-despite-status",
        ),
    ],
)
def test_command_result_succeeded(command, result, expected):
    """The per-version rule: clean exit, plus SUCCEEDED connectionStatus for check."""
    assert command_result_succeeded(command, result) is expected


@pytest.mark.parametrize(
    "command,result,expected_fragment",
    [
        pytest.param(
            "spec",
            _run_result(True),
            "**Result:** PASS",
            id="single-version-pass",
        ),
        pytest.param(
            "read",
            _run_result(False),
            "**Result:** FAIL",
            id="single-version-fail",
        ),
        pytest.param(
            "check",
            _run_result(True, connection_status="SUCCEEDED"),
            "**Result:** PASS",
            id="single-version-check-connected",
        ),
        pytest.param(
            "check",
            _run_result(True, connection_status="FAILED"),
            "**Result:** FAIL",
            id="single-version-check-failed-status-is-not-a-pass",
        ),
        pytest.param(
            "check",
            _run_result(True),
            "**Result:** FAIL",
            id="single-version-check-missing-status-fails-closed",
        ),
    ],
)
def test_single_version_report_result_line(
    tmp_path, command, result, expected_fragment
):
    """Single-version mode must not call a failed CHECK a pass just because exit==0."""
    report = generate_single_version_report(
        connector_image="airbyte/source-test:2.0.0",
        command=command,
        result=result,
        output_dir=tmp_path,
    )

    assert expected_fragment in report.read_text()


@pytest.mark.parametrize(
    "command,target_result,control_result,expected_control_row,expected_target_row",
    [
        pytest.param(
            "check",
            _run_result(True, connection_status="SUCCEEDED"),
            _run_result(True),
            "| 0 | N/A — | ❌ |",
            "| 0 | SUCCEEDED ✅ | ✅ |",
            id="check-control-clean-exit-without-status-is-not-a-pass",
        ),
        pytest.param(
            "check",
            _run_result(True),
            _run_result(True, connection_status="SUCCEEDED"),
            "| 0 | SUCCEEDED ✅ | ✅ |",
            "| 0 | N/A — | ❌ |",
            id="check-target-clean-exit-without-status-is-not-a-pass",
        ),
        pytest.param(
            "check",
            {"success": False, "exit_code": 137, "connection_status": "SUCCEEDED"},
            _run_result(True, connection_status="SUCCEEDED"),
            "| 0 | SUCCEEDED ✅ | ✅ |",
            "| 137 | SUCCEEDED ✅ | ❌ |",
            id="check-crash-after-succeeded-status-is-not-a-pass",
        ),
        pytest.param(
            "check",
            _run_result(True, connection_status="SUCCEEDED"),
            _run_result(True, connection_status="FAILED"),
            "| 0 | FAILED ❌ | ❌ |",
            "| 0 | SUCCEEDED ✅ | ✅ |",
            id="check-improvement-rows",
        ),
        pytest.param(
            "read",
            _run_result(True),
            _run_result(False),
            "| 1 | ❌ |",
            "| 0 | ✅ |",
            id="read-rows-use-the-exit-code",
        ),
    ],
)
def test_report_per_version_rows_agree_with_the_verdict(
    tmp_path,
    command,
    target_result,
    control_result,
    expected_control_row,
    expected_target_row,
):
    """The per-version table's Result column must not contradict the verdict.

    It is the column a developer scans to see which side broke, so it has to
    apply the same rule as `command_result_succeeded` -- a `check` that exits 0
    without reporting a connectionStatus is a failure, not a pass.
    """
    report = generate_action_test_comparison_report(
        target_image="airbyte/source-test:2.0.0",
        control_image="airbyte/source-test:1.0.0",
        command=command,
        target_result=target_result,
        control_result=control_result,
        output_dir=tmp_path,
    ).read_text()

    control_row = next(line for line in report.splitlines() if "| Control (" in line)
    target_row = next(line for line in report.splitlines() if "| Target (" in line)

    assert control_row.endswith(expected_control_row)
    assert target_row.endswith(expected_target_row)
