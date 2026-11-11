# Copyright (c) 2026 Airbyte, Inc., all rights reserved.
"""Golden verdict and markdown parity across report surfaces."""

from __future__ import annotations

import json
import re
from pathlib import Path

import pytest

from airbyte_ops_mcp.regression_tests.ci_output import (
    generate_action_test_comparison_report,
    generate_single_version_report,
)
from airbyte_ops_mcp.regression_tests.regression.comparators import (
    ComparisonResult,
    RecordComparisonSummary,
)
from airbyte_ops_mcp.regression_tests.report import (
    build_comparison_report_model,
    build_markdown_comparison_model,
    build_single_version_report_model,
)
from airbyte_ops_mcp.regression_tests.repro_case import (
    ReproductionVerdict,
    SideEvaluation,
    SideOutcome,
)

CASES = (
    "pass",
    "regression",
    "both_failed",
    "errored",
    "not_exercised",
    "could_not_test",
    "setup_error",
    "cap",
    "timeout",
    "stopped_not_exercised",
    "reproduction_pass",
    "reproduction_fail",
)
GOLDEN = Path(__file__).parent / "fixtures" / "regression_verdict_golden.json"


@pytest.mark.parametrize("name", ["Catalog schema", "Record schema (new streams)"])
@pytest.mark.parametrize("kind", ["inconclusive", "strict", "mixed", "warn", "empty"])
@pytest.mark.parametrize("record_checks_regression", [None, False, True])
def test_standalone_markdown_inconclusive_findings(
    tmp_path, name, kind, record_checks_regression
):
    result = {"success": True, "exit_code": 0}
    if record_checks_regression is not None:
        result["record_checks_regression"] = record_checks_regression
    original_result = dict(result)
    finding = f"{name}: comparison errored"
    findings = (
        [] if kind == "empty" else [("warn" if kind == "warn" else "fail", finding)]
    )
    inconclusive = [] if kind == "strict" else [finding]
    if kind == "mixed":
        findings.append(("fail", f"{name}: schema changed"))
    inputs = {
        "target_image": "source-test:2",
        "control_image": "source-test:1",
        "command": "read",
        "target_result": result,
        "control_result": result,
        "comparison_findings": findings,
        "inconclusive_findings": inconclusive,
    }
    path = generate_action_test_comparison_report(**inputs, output_dir=tmp_path)
    line = next(
        line for line in path.read_text().splitlines() if line.startswith("**Result:**")
    )
    model = build_markdown_comparison_model(
        **inputs, record_comparison=None, reproduction=None, target_only_streams=()
    )
    assert result == original_result
    strict = kind in {"strict", "mixed"}
    assert model.passed is (kind in {"warn", "empty"})
    assert model.strict_failed is strict
    assert model.regression_detected is strict
    assert model.comparison_errored is (kind == "inconclusive")
    if kind == "inconclusive":
        assert line == (
            "**Result:** FAIL (inconclusive) — Target succeeded, control succeeded; "
            "the record comparison errored, so it is inconclusive"
        )
    elif strict:
        assert model.verdict_label == "FAIL (regression)"
        assert line == (
            "**Result:** Target succeeded, control succeeded, and the comparison "
            "found 1 problem — **REGRESSION DETECTED**"
        )
    else:
        assert model.verdict_label == "PASS"
        assert line == "**Result:** Both versions succeeded (no regression)"


def capture(case: str, single: bool, output_dir: Path) -> dict:
    target = {"success": True, "exit_code": 0, "record_counts_per_stream": {"items": 2}}
    control = dict(target)
    streams = ()
    comparison = None
    reproduction = None
    if case.startswith("reproduction"):
        passed = case == "reproduction_pass"
        side = SideEvaluation(SideOutcome.INCONCLUSIVE, "Case evidence")
        reproduction = ReproductionVerdict(
            passed,
            not passed,
            "FIXED" if passed else "NOT FIXED",
            "Case result",
            side,
            side,
        )
    if case in {"regression", "both_failed"}:
        target.update(success=False, exit_code=1)
    if case == "both_failed":
        control.update(success=False, exit_code=1)
    if case == "errored":
        comparison = RecordComparisonSummary(
            passed=False,
            errored=True,
            count_comparison=ComparisonResult(
                passed=False, message="Comparison errored"
            ),
        )
    if case in {"not_exercised", "stopped_not_exercised"}:
        streams = ("new_stream",)
    if case in {"setup_error", "could_not_test"}:
        target[case] = True
        target[f"{case}_detail"] = "Target could not read."
        target["setup_error_clears_regression"] = True
    if case in {"cap", "timeout", "stopped_not_exercised"}:
        target["stopped_early"] = {
            "reason": "cap" if case == "cap" else "timeout",
            "records_seen": 2,
            "elapsed_s": 10,
        }
    if single:
        model = build_single_version_report_model(
            connector_image="source-test:2",
            command="read",
            result=target,
        )
        path = generate_single_version_report(
            "source-test:2",
            "read",
            target,
            output_dir,
        )
    else:
        model = build_comparison_report_model(
            target_image="source-test:2",
            control_image="source-test:1",
            command="read",
            target_result=target,
            control_result=control,
            target_only_streams=streams,
            record_comparison=comparison,
            reproduction=reproduction,
        )
        path = generate_action_test_comparison_report(
            "source-test:2",
            "source-test:1",
            "read",
            target,
            control,
            output_dir,
            target_only_streams=streams,
            record_comparison=comparison.to_dict() if comparison else None,
            reproduction=reproduction,
        )
    markdown = re.sub(r"^- \*\*Test Date:\*\*.*$", "DATE", path.read_text(), flags=re.M)
    markdown = re.sub(r"^- \*\*Tester:\*\*.*$", "TESTER", markdown, flags=re.M)
    return {"passed": model.passed, "label": model.verdict_label, "markdown": markdown}


@pytest.mark.parametrize("case", CASES)
@pytest.mark.parametrize("single", [False, True])
def test_verdict_markdown_matches_main(case, single, tmp_path, monkeypatch):
    for name in ("GITHUB_SERVER_URL", "GITHUB_REPOSITORY", "GITHUB_RUN_ID"):
        monkeypatch.delenv(name, raising=False)
    expected = json.loads(GOLDEN.read_text())[f"{case}:{single}"]
    assert capture(case, single, tmp_path) == expected


@pytest.mark.parametrize("success", [False, True])
def test_reproduction_flags_override_command_failures(success):
    result = {"success": False, "exit_code": 1}
    side = SideEvaluation(SideOutcome.INCONCLUSIVE, "Case evidence")
    reproduction = ReproductionVerdict(
        success,
        not success,
        "FIXED" if success else "NOT FIXED",
        "Case result",
        side,
        side,
    )
    model = build_comparison_report_model(
        target_image="source-test:2",
        control_image="source-test:1",
        command="read",
        target_result=result,
        control_result=result,
        reproduction=reproduction,
    )
    assert model.verdict_flags() == {
        "exercised_partial": False,
        "success": success,
        "regression_detected": not success,
        "both_failed": False,
        "incomplete": False,
        "not_exercised": False,
        "setup_error": False,
        "could_not_test": False,
        "strict_failed": False,
        "comparison_errored": False,
    }
