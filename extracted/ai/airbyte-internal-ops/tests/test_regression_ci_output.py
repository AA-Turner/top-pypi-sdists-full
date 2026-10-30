# Copyright (c) 2025 Airbyte, Inc., all rights reserved.
"""Unit tests for regression test comparison outcome evaluation."""

import pytest

from airbyte_ops_mcp.regression_tests.ci_output import (
    LEGACY_NOT_FOUND_MESSAGE,
    _pk_integrity_cell,
    command_result_succeeded,
    config_error_streams,
    could_not_test,
    describe_masking,
    evaluate_comparison_outcome,
    generate_action_test_comparison_report,
    generate_single_version_report,
    new_stream_verdict_label,
    not_exercised_note,
    not_exercised_streams,
    readable_cursor_counts,
    run_readable_fields,
    target_errors_only_from,
    undefined_streams,
)
from airbyte_ops_mcp.regression_tests.models import StreamError


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


def test_undefined_stream_classification_uses_status_records_and_errors():
    assert undefined_streams(("new",), {"new": ["INCOMPLETE"]}, {}, {}) == ("new",)
    assert undefined_streams(("new",), {"new": ["INCOMPLETE"]}, {"new": 1}, {}) == ()
    assert (
        undefined_streams(
            ("new",),
            {"new": ["INCOMPLETE"]},
            {},
            {"new": [StreamError("system_error", "failed")]},
        )
        == ()
    )
    assert undefined_streams(("new",), {"new": ["STARTED", "INCOMPLETE"]}, {}, {}) == ()
    assert undefined_streams(
        ("new",),
        {},
        {},
        {"new": [StreamError("config_error", LEGACY_NOT_FOUND_MESSAGE)]},
    ) == ("new",)


def test_could_not_test_requires_only_target_config_errors_and_aggregate_traces():
    config_error = StreamError("config_error", "HTTP 400, code 4711")
    aggregate = StreamError(
        "config_error",
        "During the sync, the following streams did not sync successfully: new",
    )
    assert could_not_test(("new",), {"new": [config_error], None: [aggregate]})
    assert not could_not_test(
        ("new",),
        {
            "new": [config_error, StreamError("system_error", "system failure")],
            None: [aggregate],
        },
    )
    assert not could_not_test(
        ("new",),
        {"new": [config_error], "shared": [StreamError("config_error", "bad config")]},
    )
    assert not could_not_test(
        ("new",), {"new": [config_error], None: [StreamError("system_error", "other")]}
    )
    assert not could_not_test(("new",), {None: [aggregate]})
    assert config_error_streams(("new",), {"new": [config_error]}) == ("new",)


def test_target_errors_only_from_target_only_streams_and_cdk_aggregates():
    aggregate = StreamError(
        "config_error",
        "During the sync, the following streams did not sync successfully: new",
    )
    assert target_errors_only_from(("new",), {})
    assert target_errors_only_from(
        ("new",), {"new": [StreamError("system_error", "failure")], None: [aggregate]}
    )
    assert not target_errors_only_from(
        ("new",), {"shared": [StreamError("system_error", "failure")]}
    )
    assert not target_errors_only_from(
        ("new",), {None: [StreamError("system_error", "not an aggregate")]}
    )


def _new_stream_verdict_flags(**overrides: bool) -> dict[str, bool]:
    return {
        "stopped": False,
        "setup_error": False,
        "strict_failed": False,
        "regression": False,
        "both_failed": False,
        "comparison_errored": False,
        "could_not_test": False,
        "not_exercised": False,
        **overrides,
    }


@pytest.mark.parametrize(
    "overrides,expected",
    [
        pytest.param(
            {"not_exercised": True},
            "NOT EXERCISED",
            id="not-exercised",
        ),
        pytest.param(
            {"not_exercised": True, "regression": True},
            "FAIL (regression)",
            id="not-exercised-regression",
        ),
        pytest.param(
            {"not_exercised": True, "both_failed": True},
            "FAIL (inconclusive)",
            id="not-exercised-both-failed",
        ),
        pytest.param(
            {"not_exercised": True, "strict_failed": True},
            "FAIL (regression)",
            id="not-exercised-strict-failure",
        ),
        pytest.param(
            {"not_exercised": True, "comparison_errored": True},
            "FAIL (inconclusive)",
            id="not-exercised-comparison-error",
        ),
        pytest.param(
            {"could_not_test": True},
            "COULD NOT TEST (config error)",
            id="could-not-test",
        ),
        pytest.param(
            {"could_not_test": True, "regression": True},
            "COULD NOT TEST (config error)",
            id="could-not-test-suppresses-target-regression",
        ),
        pytest.param(
            {"could_not_test": True, "both_failed": True},
            "FAIL (inconclusive)",
            id="could-not-test-both-failed",
        ),
        pytest.param(
            {"could_not_test": True, "strict_failed": True},
            "FAIL (regression)",
            id="could-not-test-strict-failure",
        ),
        pytest.param(
            {"setup_error": True, "strict_failed": True},
            "SETUP ERROR",
            id="setup-error-strict-failure",
        ),
        pytest.param(
            {
                "stopped": True,
                "setup_error": True,
                "strict_failed": True,
                "regression": True,
                "both_failed": True,
                "comparison_errored": True,
                "could_not_test": True,
                "not_exercised": True,
            },
            "INCOMPLETE",
            id="stopped-precedes-everything",
        ),
        pytest.param({}, None, id="no-new-stream-verdict"),
    ],
)
def test_new_stream_verdict_label_precedence(overrides, expected):
    assert (
        new_stream_verdict_label(**_new_stream_verdict_flags(**overrides)) == expected
    )


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


@pytest.mark.parametrize(
    "mode,fragment",
    [
        pytest.param(
            "masked",
            "- Output mode: masked — record values are type-and-length tokens",
            id="masked",
        ),
        pytest.param(
            "raw",
            "- Output mode: raw — records, HTTP bodies and logs are unmasked",
            id="raw",
        ),
    ],
)
def test_the_markdown_report_says_how_the_output_was_masked(tmp_path, mode, fragment):
    report = generate_action_test_comparison_report(
        target_image="airbyte/source-test:2.0.0",
        control_image="airbyte/source-test:1.0.0",
        command="read",
        target_result=_run_result(True, output_mode=mode),
        control_result=_run_result(True, output_mode=mode),
        output_dir=tmp_path,
    )

    assert fragment in report.read_text()


READABLE_FIELDS = {
    "users": {
        "cursor": ["updated_at"],
        "readable": True,
        "declared": "string/date-time",
        "reason": "readable (string/date-time)",
    },
    "tokens": {
        "cursor": ["token"],
        "readable": False,
        "declared": "string",
        "reason": "masked: type string",
    },
    "events": {
        "cursor": None,
        "readable": False,
        "declared": None,
        "reason": "no cursor",
    },
}


def test_the_masked_line_counts_the_readable_cursors_when_the_run_says():
    with_count = describe_masking("masked", READABLE_FIELDS)
    without = describe_masking("masked")

    assert with_count is not None
    assert "primary keys masked" in with_count
    assert "cursor readable on 1 of 2 streams (integer, date, date-time only)" in (
        with_count
    )
    assert without is not None
    assert "integer or a date" in without
    assert describe_masking("raw", READABLE_FIELDS) == describe_masking("raw")
    assert describe_masking(None, READABLE_FIELDS) is None


def test_the_masked_line_says_debug_logs_are_off():
    """A reader of a masked run's report should not wonder where DEBUG went."""
    assert "debug logs off" in (describe_masking("masked") or "")
    assert "debug logs off" not in (describe_masking("raw") or "")


def test_the_readable_count_ignores_streams_without_a_cursor():
    assert readable_cursor_counts(READABLE_FIELDS) == (1, 2)
    assert readable_cursor_counts({}) == (0, 0)
    assert readable_cursor_counts({"x": "not an entry"}) == (0, 0)


def test_the_readable_fields_come_from_the_first_side_that_has_them():
    assert run_readable_fields({}, {"readable_fields": READABLE_FIELDS}) == (
        READABLE_FIELDS
    )
    assert run_readable_fields({"readable_fields": None}, {}) is None
    assert run_readable_fields() is None


def test_the_markdown_report_carries_the_readable_count(tmp_path):
    report = generate_action_test_comparison_report(
        target_image="airbyte/source-test:2.0.0",
        control_image="airbyte/source-test:1.0.0",
        command="read",
        target_result=_run_result(
            True, output_mode="masked", readable_fields=READABLE_FIELDS
        ),
        control_result=_run_result(True, output_mode="masked"),
        output_dir=tmp_path,
    )

    text = report.read_text()
    assert "cursor readable on 1 of 2 streams" in text
    assert "masked: type string" not in text


def test_a_result_without_a_mode_adds_no_masking_line(tmp_path):
    report = generate_action_test_comparison_report(
        target_image="airbyte/source-test:2.0.0",
        control_image="airbyte/source-test:1.0.0",
        command="read",
        target_result=_run_result(True),
        control_result=_run_result(True),
        output_dir=tmp_path,
    )

    assert "Output mode" not in report.read_text()


def test_the_single_version_report_says_how_the_output_was_masked(tmp_path):
    report = generate_single_version_report(
        connector_image="airbyte/source-test:2.0.0",
        command="read",
        result=_run_result(True, output_mode="masked"),
        output_dir=tmp_path,
    )

    assert "- **Output mode:** masked — " in report.read_text()


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


# ---------------------------------------------------------------------------
# Stopped-early reads: INCOMPLETE, never a pass
# ---------------------------------------------------------------------------

_STOPPED = {"reason": "timeout", "records_seen": 1234, "elapsed_s": 10200.0}


def _stopped_side(**overrides) -> dict:
    return {"success": True, "exit_code": 0, "stopped_early": {**_STOPPED, **overrides}}


def test_the_result_line_of_a_stopped_read_is_incomplete(tmp_path):
    report = generate_action_test_comparison_report(
        target_image="airbyte/source-test:2.0.0",
        control_image="airbyte/source-test:1.0.0",
        command="read",
        target_result=_stopped_side(),
        control_result=_stopped_side(),
        output_dir=tmp_path,
    )
    content = report.read_text()

    assert (
        "**Result:** INCOMPLETE — stopped early (timeout) after 1,234 records per side"
        in content
    )
    assert "REGRESSION DETECTED" not in content
    assert "no regression" not in content
    assert (
        "- Control: stopped early (timeout) after 1,234 records in 10,200 s" in content
    )
    assert (
        "- Target: stopped early (timeout) after 1,234 records in 10,200 s" in content
    )


def test_a_side_stopped_at_its_share_of_the_budget_names_the_share(tmp_path):
    """The control's deadline is not the budget's end; its line says whose it was."""
    report = generate_action_test_comparison_report(
        target_image="airbyte/source-test:2.0.0",
        control_image="airbyte/source-test:1.0.0",
        command="read",
        target_result=_stopped_side(
            records_seen=0, elapsed_s=0.0, share_s=0, budget_s=10_200
        ),
        control_result=_stopped_side(elapsed_s=5760.0, share_s=5760, budget_s=10_200),
        output_dir=tmp_path,
    )
    content = report.read_text()

    assert (
        "**Result:** INCOMPLETE — stopped early (timeout) after 1,234 (control) / "
        "0 (target) records" in content
    )
    assert "REGRESSION DETECTED" not in content
    assert (
        "- Control: stopped early (timeout) after 1,234 records in 5,760 s, at the "
        "end of its 96-minute share of the 170-minute read budget" in content
    )
    assert (
        "- Target: stopped early (timeout) after 0 records in 0 s, without "
        "starting: nothing was left of the 170-minute read budget" in content
    )


@pytest.mark.parametrize(
    ("entry", "expected"),
    [
        pytest.param(
            {"share_s": 5737, "budget_s": 10_200},
            ", at the end of its 96-minute share of the 170-minute read budget",
            id="minutes-rounded",
        ),
        pytest.param(
            {"share_s": 324, "budget_s": 600},
            ", at the end of its 324-second share of the 10-minute read budget",
            id="short-share-in-seconds",
        ),
        pytest.param({}, "", id="no-share-on-a-single-version-or-capped-run"),
    ],
)
def test_a_stopped_sides_note_names_its_share_only_when_it_had_one(
    tmp_path, entry, expected
):
    stopped = {"reason": "timeout", "records_seen": 5, "elapsed_s": 1.0, **entry}
    report = generate_action_test_comparison_report(
        target_image="airbyte/source-test:2.0.0",
        control_image="airbyte/source-test:1.0.0",
        command="read",
        target_result={"success": True, "exit_code": 0},
        control_result={"success": True, "exit_code": 0, "stopped_early": stopped},
        output_dir=tmp_path,
    )

    note = next(
        line
        for line in report.read_text().splitlines()
        if line.startswith("- Control: stopped early")
    )
    assert (
        note == f"- Control: stopped early (timeout) after 5 records in 1 s{expected}"
    )


def test_sides_that_stopped_at_different_points_show_both_counts(tmp_path):
    report = generate_action_test_comparison_report(
        target_image="airbyte/source-test:2.0.0",
        control_image="airbyte/source-test:1.0.0",
        command="read",
        target_result=_stopped_side(records_seen=987, reason="cap"),
        control_result=_stopped_side(),
        output_dir=tmp_path,
    )

    assert (
        "INCOMPLETE — stopped early (control: timeout, target: cap) after "
        "1,234 (control) / 987 (target) records" in report.read_text()
    )


def test_an_errored_comparison_on_a_stopped_read_claims_no_regression(tmp_path):
    report = generate_action_test_comparison_report(
        target_image="airbyte/source-test:2.0.0",
        control_image="airbyte/source-test:1.0.0",
        command="read",
        target_result=_stopped_side(),
        control_result=_stopped_side(),
        output_dir=tmp_path,
        record_comparison={"passed": False, "errored": True, "checks": {}},
    )
    content = report.read_text()

    assert (
        "**Result:** INCOMPLETE — stopped early (timeout) after 1,234 records per "
        "side; the record comparison errored, so it is inconclusive" in content
    )
    assert "REGRESSION DETECTED" not in content


def test_a_strict_failure_on_a_stopped_read_is_still_a_regression(tmp_path):
    report = generate_action_test_comparison_report(
        target_image="airbyte/source-test:2.0.0",
        control_image="airbyte/source-test:1.0.0",
        command="read",
        target_result=_stopped_side(),
        control_result=_stopped_side(),
        output_dir=tmp_path,
        record_comparison={"passed": False, "partial": True, "checks": {}},
    )
    content = report.read_text()

    assert (
        "**Result:** INCOMPLETE — stopped early (timeout) after 1,234 records per "
        "side, and the comparison found 1 problem — **REGRESSION DETECTED**" in content
    )


def test_a_stopped_side_beside_a_crashed_one_is_incomplete_and_a_regression(tmp_path):
    report = generate_action_test_comparison_report(
        target_image="airbyte/source-test:2.0.0",
        control_image="airbyte/source-test:1.0.0",
        command="read",
        target_result={"success": False, "exit_code": 1},
        control_result=_stopped_side(),
        output_dir=tmp_path,
    )
    content = report.read_text()

    assert (
        "**Result:** INCOMPLETE — control stopped early (timeout) after 1,234 "
        "records; target ran to completion; target failed (exit 1), control "
        "succeeded — **REGRESSION DETECTED**" in content
    )


def test_the_partial_record_comparison_section_marks_counts_as_inconclusive(tmp_path):
    record_comparison = {
        "passed": True,
        "partial": True,
        "errors": [],
        "warnings": ["Stream users has 1 fewer records in target (2 vs 3)"],
        "streams_without_pk": [],
        "checks": {
            "record_counts": {
                "passed": False,
                "streams": {
                    "users": {"passed": False, "control_count": 3, "target_count": 2}
                },
            },
            "pk_presence": {
                "passed": False,
                "streams": {"users": {"passed": False, "missing_pk_count": 1}},
            },
            "pk_uniqueness_control": {
                "passed": True,
                "streams": {"users": {"passed": True, "duplicate_pk_count": 0}},
            },
            "pk_uniqueness_target": {
                "passed": True,
                "streams": {"users": {"passed": True, "duplicate_pk_count": 0}},
            },
            "field_values": {
                "passed": True,
                "streams": {"users": {"passed": True, "records_with_value_diff": 0}},
            },
        },
    }
    report = generate_action_test_comparison_report(
        target_image="airbyte/source-test:2.0.0",
        control_image="airbyte/source-test:1.0.0",
        command="read",
        target_result=_stopped_side(),
        control_result=_stopped_side(),
        output_dir=tmp_path,
        record_comparison=record_comparison,
    )
    content = report.read_text()

    assert "**Status:** ✅ PASSED" in content
    assert "record counts and primary key presence are inconclusive here" in content
    assert "| users | 3 → 2 ⚠️ | 1 ⚠️ | 0 ✅ | 0 ✅ | 0 ✅ | ⚠️ |" in content


def test_a_capped_read_with_equal_counts_is_still_inconclusive(tmp_path):
    """Equal counts under a cap are the cap's doing: a tick would overclaim."""
    record_comparison = {
        "passed": True,
        "partial": True,
        "errors": [],
        "warnings": [],
        "streams_without_pk": ["events"],
        "checks": {
            "record_counts": {
                "passed": True,
                "streams": {
                    "users": {
                        "passed": True,
                        "control_count": 10000,
                        "target_count": 10000,
                    },
                    "events": {"passed": True, "control_count": 5, "target_count": 5},
                },
            },
            "pk_presence": {
                "passed": True,
                "streams": {"users": {"passed": True, "missing_pk_count": 0}},
            },
            "pk_uniqueness_control": {
                "passed": True,
                "streams": {"users": {"passed": True, "duplicate_pk_count": 0}},
            },
            "pk_uniqueness_target": {
                "passed": True,
                "streams": {"users": {"passed": True, "duplicate_pk_count": 0}},
            },
            "field_values": {
                "passed": True,
                "streams": {"users": {"passed": True, "records_with_value_diff": 0}},
            },
        },
    }
    report = generate_action_test_comparison_report(
        target_image="airbyte/source-test:2.0.0",
        control_image="airbyte/source-test:1.0.0",
        command="read",
        target_result=_stopped_side(reason="cap", records_seen=10005),
        control_result=_stopped_side(reason="cap", records_seen=10005),
        output_dir=tmp_path,
        record_comparison=record_comparison,
    )
    content = report.read_text()

    assert "| users | 10000 → 10000 ⚠️ | 0 ⚠️ | 0 ✅ | 0 ✅ | 0 ✅ | ⚠️ |" in content
    assert "| events | 5 → 5 ⚠️ | — | — | — | — | ⚠️ |" in content
    assert "✅ |\n" not in content.split("### Record Comparison")[1]


def test_the_single_version_result_line_of_a_stopped_read(tmp_path):
    report = generate_single_version_report(
        connector_image="airbyte/source-test:2.0.0",
        command="read",
        result=_stopped_side(),
        output_dir=tmp_path,
    )
    content = report.read_text()

    assert (
        "**Result:** INCOMPLETE — stopped early (timeout) after 1,234 records"
        in content
    )
    assert "- Run: stopped early (timeout) after 1,234 records in 10,200 s" in content
    assert "**Result:** PASS" not in content


@pytest.mark.parametrize(
    "info,side,expected",
    [
        pytest.param({"passed": True}, "control", "0 ✅", id="clean"),
        pytest.param(
            {"passed": False, "records_missing_pk": 1},
            "control",
            "0, 1 missing PK ❌",
            id="missing-pk-only",
        ),
        pytest.param(
            {
                "passed": True,
                "duplicate_pk_count": 2,
                "pre_existing_duplicate_pk_count": 2,
            },
            "target",
            "2 (pre-existing) ⚠️",
            id="pre-existing",
        ),
        pytest.param(
            {
                "passed": False,
                "duplicate_pk_count": 1,
                "pre_existing_duplicate_pk_count": 1,
                "records_missing_pk": 1,
            },
            "control",
            "1 (pre-existing), 1 missing PK ❌",
            id="pre-existing-and-missing-pk",
        ),
        pytest.param(
            {
                "passed": True,
                "duplicate_pk_count": 1,
                "fixed_duplicate_pk_count": 1,
            },
            "control",
            "1 fixed in target ⚠️",
            id="fixed",
        ),
        pytest.param(
            {
                "passed": True,
                "duplicate_pk_count": 3,
                "pre_existing_duplicate_pk_count": 1,
                "fixed_duplicate_pk_count": 2,
            },
            "control",
            "3 (1 pre-existing, 2 fixed in target) ⚠️",
            id="pre-existing-and-fixed",
        ),
        pytest.param(
            {
                "passed": False,
                "duplicate_pk_count": 2,
                "new_duplicate_pk_count": 2,
            },
            "target",
            "2 new ❌",
            id="new",
        ),
        pytest.param(
            {
                "passed": False,
                "duplicate_pk_count": 3,
                "pre_existing_duplicate_pk_count": 1,
                "new_duplicate_pk_count": 2,
                "records_missing_pk": 4,
            },
            "target",
            "3 (1 pre-existing, 2 new), 4 missing PK ❌",
            id="new-pre-existing-and-missing-pk",
        ),
    ],
)
def test_pk_integrity_cell_ends_with_the_status(
    info: dict, side: str, expected: str
) -> None:
    assert _pk_integrity_cell(info, side) == expected


@pytest.mark.parametrize(
    "info,side,expected",
    [
        pytest.param(
            {
                "passed": True,
                "duplicate_pk_count": 3,
                "pre_existing_duplicate_pk_count": 1,
            },
            "control",
            "3 (1 pre-existing, 2 not duplicated in target (partial read)) ⚠️",
            id="control-only-on-a-partial-read",
        ),
        pytest.param(
            {"passed": True, "duplicate_pk_count": 2},
            "control",
            "2 not duplicated in target (partial read) ⚠️",
            id="control-only-alone",
        ),
        pytest.param(
            {
                "passed": True,
                "duplicate_pk_count": 2,
                "pre_existing_duplicate_pk_count": 1,
                "new_duplicate_pk_count": 1,
            },
            "target",
            "2 (1 pre-existing, 1 new) ⚠️",
            id="target-unchanged",
        ),
    ],
)
def test_pk_integrity_cell_names_control_only_duplicates_neutrally_when_partial(
    info: dict, side: str, expected: str
) -> None:
    """A partial read classifies no control duplicate as fixed or lost."""
    assert _pk_integrity_cell(info, side, partial=True) == expected


def test_the_markdown_report_names_the_request_and_repeated_url_counts(tmp_path):
    """The two numbers every comparison now has, labelled as what they are.

    A "flow" is mitmproxy's word; a reviewer is counting requests. And the
    second number is requests to a URL already requested in the same run -- not
    a cache metric, which is the opposite of what a repeated request is.
    """
    report = generate_action_test_comparison_report(
        target_image="airbyte/source-test:2.0.0",
        control_image="airbyte/source-test:1.0.0",
        command="read",
        target_result=_run_result(
            True, http_metrics={"flow_count": 118, "duplicate_flow_count": 7}
        ),
        control_result=_run_result(
            True, http_metrics={"flow_count": 120, "duplicate_flow_count": 8}
        ),
        output_dir=tmp_path,
    ).read_text()

    lines = report.splitlines()
    header = lines[lines.index("#### HTTP Metrics") + 2]
    assert header.startswith("| Version | Requests | Repeated URLs |")
    assert "| Control | 120 | 8 |" in report
    assert "| Target | 118 | 7 |" in report


def _http_report(tmp_path, control_http: dict | None, target_http: dict | None) -> str:
    """A `read` comparison report whose only interesting content is HTTP metrics."""
    return generate_action_test_comparison_report(
        target_image="airbyte/source-test:2.0.0",
        control_image="airbyte/source-test:1.0.0",
        command="read",
        target_result=_run_result(True, http_metrics=target_http),
        control_result=_run_result(True, http_metrics=control_http),
        output_dir=tmp_path,
    ).read_text()


def _http_rows(report: str) -> dict[str, list[str]]:
    """The HTTP table's two data rows, split into cells."""
    lines = report.splitlines()
    start = lines.index("#### HTTP Metrics")
    return {
        line.split("|")[1].strip(): [cell.strip() for cell in line.split("|")[2:-1]]
        for line in lines[start:]
        if line.startswith(("| Control |", "| Target |"))
    }


_PROXY_ONLY = {
    "flow_count": 120,
    "duplicate_flow_count": 8,
    "replayed_flow_count": 118,
    "live_flow_count": 2,
    "replay_hit_ratio": "98.33%",
}
_CONNECTOR_ONLY = {
    "connector_request_count": 40,
    "connector_cache_hits_count": 10,
    "connector_cache_hit_ratio": "25.00%",
}


def test_the_http_table_reports_both_ratios_separately(tmp_path):
    """The two metrics answer different questions and must both be readable.

    The replay hit ratio is a property of the *harness* -- did the target see the
    same upstream bytes the control recorded. The cache hit ratio is a property
    of the *connector* -- does its own `requests_cache` still work. The legacy
    report conflated them under one name; this table must not.
    """
    report = _http_report(
        tmp_path,
        {**_PROXY_ONLY, **_CONNECTOR_ONLY},
        {
            **_PROXY_ONLY,
            **_CONNECTOR_ONLY,
            "connector_cache_hit_ratio": "24.00%",
            "connector_cache_hits_count": 12,
            "connector_request_count": 50,
        },
    )

    # `Connector requests` sits beside the ratio it is the denominator of: the
    # proxy's `Requests` counts neither a cache hit nor a retry, so `Cache hits`
    # over it would not be the ratio the column shows.
    assert (
        "| Version | Requests | Repeated URLs | Replayed | Live | Replay hit ratio "
        "| Connector requests | Cache hits | Cache hit ratio |" in report
    )
    assert _http_rows(report) == {
        "Control": ["120", "8", "118", "2", "98.33%", "40", "10", "25.00%"],
        "Target": ["120", "8", "118", "2", "98.33%", "50", "12", "24.00%"],
    }


def test_a_silent_connector_reads_as_not_reported_rather_than_zero(tmp_path):
    """The failure mode most likely to mislead a reviewer.

    A Java connector, a connector using its own `requests.Session`, and a
    connector on a CDK predating the counters all report nothing. A `0` or a
    `0.00%` here would read as a version whose caching broke.
    """
    report = _http_report(tmp_path, dict(_PROXY_ONLY), dict(_PROXY_ONLY))

    assert "0.00%" not in report
    silent = ["not reported"] * 3
    assert _http_rows(report) == {
        "Control": ["120", "8", "118", "2", "98.33%", *silent],
        "Target": ["120", "8", "118", "2", "98.33%", *silent],
    }


def test_the_table_appears_without_the_proxy_when_the_connector_reported(tmp_path):
    """The connector's own cache needs no proxy, so a run without one still has data.

    Gating this table on `flow_count` would hide every connector cache metric on
    a run made without `--enable-http-metrics`, which is most of them.
    """
    report = _http_report(tmp_path, dict(_CONNECTOR_ONLY), dict(_CONNECTOR_ONLY))

    assert "#### HTTP Metrics" in report
    no_proxy = ["not captured"] * 5
    assert _http_rows(report) == {
        "Control": [*no_proxy, "40", "10", "25.00%"],
        "Target": [*no_proxy, "40", "10", "25.00%"],
    }


def test_a_captured_side_with_no_requests_reads_zero_not_not_captured(tmp_path):
    """`flow_count: 0` is a proxy that ran and saw nothing, which is a finding."""
    report = _http_report(
        tmp_path,
        dict(_PROXY_ONLY),
        {"flow_count": 0, "duplicate_flow_count": 0},
    )

    rows = _http_rows(report)
    assert rows["Control"][:2] == ["120", "8"]
    assert rows["Target"][:2] == ["0", "0"]
    assert "not captured" not in rows["Target"][:2]


def test_no_http_table_when_nothing_was_measured(tmp_path):
    """A payload holding only a skip reason describes a proxy that never ran."""
    report = _http_report(
        tmp_path, None, {"replay_skipped_reason": "mitmproxy is unavailable"}
    )

    assert "#### HTTP Metrics" not in report
    # The reason still prints, outside the table.
    assert "HTTP replay was requested and skipped" in report


def test_a_side_run_without_the_proxy_is_named_with_its_reason(tmp_path):
    """Without a table to show `not captured` in, the reason is all there is."""
    report = _http_report(
        tmp_path,
        {"capture_skipped_reason": "airbyte/source-jvm:1.0.0 has no certifi bundle"},
        {"capture_skipped_reason": "airbyte/source-jvm:2.0.0 has no certifi bundle"},
    )

    assert "#### HTTP Metrics" not in report
    assert (
        "HTTP traffic was not captured on the control: "
        "airbyte/source-jvm:1.0.0 has no certifi bundle." in report
    )
    assert "not captured on the target: airbyte/source-jvm:2.0.0" in report


def test_unreplayable_flows_are_reported_outside_the_table(tmp_path):
    """Dropped from the table's columns, but never dropped from the report.

    This is the usual reason replay coverage is poor, and its fix
    (`--http-replay-max-body`) is only findable if the number is.
    """
    report = _http_report(
        tmp_path,
        {**_PROXY_ONLY, "unreplayable_flow_count": 0},
        {**_PROXY_ONLY, "unreplayable_flow_count": 7},
    )

    assert "control 0, target 7" in report
    assert "--http-replay-max-body" in report


# ---------------------------------------------------------------------------
# Not-exercised reads: a target-only stream with no records is never a pass
# ---------------------------------------------------------------------------

_NOT_EXERCISED_DETAIL = (
    "1 stream(s) the control did not read returned no records: audit_logs"
)


def _read_side(counts: dict[str, int], **extra) -> dict:
    return {
        "success": True,
        "exit_code": 0,
        "record_counts_per_stream": counts,
        **extra,
    }


def _read_report(tmp_path, target: dict, control: dict, **kwargs) -> str:
    report = generate_action_test_comparison_report(
        target_image="airbyte/source-test:2.0.0",
        control_image="airbyte/source-test:1.0.0",
        command="read",
        target_result=target,
        control_result=control,
        output_dir=tmp_path,
        **kwargs,
    )
    return report.read_text()


def test_the_unexercised_streams_are_the_target_only_ones_with_no_records():
    assert not_exercised_streams(("audit_logs", "orders"), {"orders": 1}) == (
        "audit_logs",
    )
    assert not_exercised_streams(("audit_logs",), {"audit_logs": 0}) == ("audit_logs",)
    assert not_exercised_streams(("audit_logs",), {"audit_logs": 1}) == ()
    assert not_exercised_streams((), {}) == ()
    assert not_exercised_note(()) is None
    assert (
        not_exercised_note(("audit_logs",)) == f"Not exercised: {_NOT_EXERCISED_DETAIL}"
    )


def test_the_result_line_of_an_unexercised_read_is_not_exercised(tmp_path):
    content = _read_report(
        tmp_path,
        _read_side({"users": 3}),
        _read_side({"users": 3}),
        target_only_streams=("audit_logs",),
    )

    assert f"**Result:** NOT EXERCISED — {_NOT_EXERCISED_DETAIL}" in content
    assert "REGRESSION DETECTED" not in content
    assert "no regression" not in content
    assert "- Not exercised:" not in content


def test_a_regression_beside_an_unexercised_stream_is_still_named(tmp_path):
    content = _read_report(
        tmp_path,
        _read_side({"users": 2}),
        _read_side({"users": 3}),
        record_comparison={"passed": False},
        target_only_streams=("audit_logs",),
    )

    assert "**Result:** FAIL (regression) —" in content
    assert _NOT_EXERCISED_DETAIL in content
    assert "and the comparison found 1 problem" in content


def test_a_fail_result_line_mentions_side_text_once(tmp_path):
    target = _read_side({"users": 2})
    target.update(success=False, exit_code=1)
    content = _read_report(
        tmp_path,
        target,
        _read_side({"users": 2}),
        target_only_streams=("audit_logs",),
    )

    result_line = next(
        line for line in content.splitlines() if line.startswith("**Result:**")
    )
    assert result_line.count("Target failed (exit 1), control succeeded") == 1


def test_an_errored_comparison_beside_an_unexercised_stream_claims_no_regression(
    tmp_path,
):
    content = _read_report(
        tmp_path,
        _read_side({"users": 3}),
        _read_side({"users": 3}),
        record_comparison={"passed": False, "errored": True, "checks": {}},
        target_only_streams=("audit_logs",),
    )

    assert (
        f"**Result:** NOT EXERCISED — {_NOT_EXERCISED_DETAIL}; the record "
        "comparison errored, so it is inconclusive" in content
    )
    assert "REGRESSION DETECTED" not in content


def test_a_target_only_stream_with_records_leaves_the_result_line_alone(tmp_path):
    content = _read_report(
        tmp_path,
        _read_side({"users": 3, "audit_logs": 2}),
        _read_side({"users": 3}),
        target_only_streams=("audit_logs",),
    )

    assert "**Result:** Both versions succeeded (no regression)" in content
    assert "NOT EXERCISED" not in content
    assert "Not exercised" not in content


def test_a_stop_keeps_the_incomplete_line_and_notes_the_unexercised_stream(tmp_path):
    content = _read_report(
        tmp_path,
        _read_side({"users": 3}, stopped_early=_STOPPED),
        _read_side({"users": 3}, stopped_early=_STOPPED),
        target_only_streams=("audit_logs",),
    )
    note = f"- Not exercised: {_NOT_EXERCISED_DETAIL}"

    assert (
        "**Result:** INCOMPLETE — stopped early (timeout) after 1,234 records per side"
        in content
    )
    assert "NOT EXERCISED" not in content
    assert note in content
    assert content.index("- Target: stopped early") < content.index(note)
