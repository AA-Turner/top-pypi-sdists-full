"""Tests for _reconcile_results function."""

from agentic_devtools.cli.github.pr_checks_status import _reconcile_results


def _make_classification(**overrides):
    """Build a check classification with empty defaults."""
    base = {
        "passed": 0,
        "failed": 0,
        "pending": 0,
        "skipped": 0,
        "cancelled": 0,
        "total": 0,
        "failedChecks": [],
        "pendingChecks": [],
    }
    base.update(overrides)
    return base


def _make_required_checks(**overrides):
    """Build complete, green required-check evidence."""
    evidence = {"complete": True, "ready": True, "checkRuns": [], "diagnostics": []}
    evidence.update(overrides)
    return evidence


class TestReconcileResults:
    """Tests for status reconciliation and required-check gating."""

    def test_all_pass_requires_verified_required_checks(self):
        classification = _make_classification(passed=5, total=5)
        result = _reconcile_results(classification, _make_required_checks())
        assert result["status"] == "all-pass"
        assert result["requiredChecksDiagnostics"] == []

    def test_unavailable_required_check_evidence_stays_pending(self):
        classification = _make_classification(passed=5, total=5)
        evidence = _make_required_checks(
            complete=False,
            ready=False,
            diagnostics=["Required-check resolution failed"],
        )
        result = _reconcile_results(classification, evidence)
        assert result["status"] == "pending"
        assert result["requiredChecksDiagnostics"] == ["Required-check resolution failed"]

    def test_missing_required_check_stays_pending(self):
        classification = _make_classification(passed=5, total=5)
        evidence = _make_required_checks(
            ready=False,
            diagnostics=["Missing required check 'build'"],
        )
        result = _reconcile_results(classification, evidence)
        assert result["status"] == "pending"
        assert result["requiredChecksDiagnostics"] == ["Missing required check 'build'"]

    def test_non_required_run_failure_blocks_and_is_diagnostic(self):
        classification = _make_classification(passed=5, total=5)
        evidence = _make_required_checks(
            ready=False,
            checkRuns=[{"name": "optional", "status": "completed", "conclusion": "failure"}],
            diagnostics=["Blocking check 'optional'"],
        )
        result = _reconcile_results(classification, evidence)
        assert result["status"] == "failed"
        assert result["requiredChecksDiagnostics"] == ["Blocking check 'optional'"]

    def test_non_required_run_pending_blocks(self):
        classification = _make_classification(passed=5, total=5)
        evidence = _make_required_checks(
            ready=False,
            checkRuns=[{"name": "optional", "status": "in_progress", "conclusion": None}],
            diagnostics=["Blocking check 'optional'"],
        )
        result = _reconcile_results(classification, evidence)
        assert result["status"] == "pending"

    def test_timed_out_and_cancelled_runs_remain_blocking(self):
        classification = _make_classification(passed=5, total=5)
        for conclusion, expected in (("timed_out", "failed"), ("cancelled", "cancelled")):
            evidence = _make_required_checks(
                ready=False,
                checkRuns=[{"name": "required", "status": "completed", "conclusion": conclusion}],
                diagnostics=[f"Blocking check conclusion {conclusion}"],
            )
            result = _reconcile_results(classification, evidence)
            assert result["status"] == expected

    def test_failure_run_takes_priority_over_cancelled_run(self):
        classification = _make_classification(passed=5, total=5)
        evidence = _make_required_checks(
            ready=False,
            checkRuns=[
                {"name": "failed", "status": "completed", "conclusion": "failure"},
                {"name": "cancelled", "status": "completed", "conclusion": "cancelled"},
            ],
        )
        result = _reconcile_results(classification, evidence)
        assert result["status"] == "failed"

    def test_real_run_pending_and_failure_take_priority(self):
        for classification, expected in (
            (_make_classification(pending=1, total=1), "pending"),
            (_make_classification(failed=1, total=1, failedChecks=["lint"]), "failed"),
            (_make_classification(cancelled=1, total=1), "cancelled"),
        ):
            result = _reconcile_results(classification, _make_required_checks())
            assert result["status"] == expected

    def test_output_contains_classified_counts(self):
        classification = _make_classification(
            passed=3,
            failed=1,
            pending=1,
            skipped=2,
            cancelled=1,
            total=8,
            failedChecks=["x"],
            pendingChecks=["y"],
        )
        result = _reconcile_results(classification, _make_required_checks())
        assert result["totalChecks"] == 8
        assert result["passed"] == 3
        assert result["failed"] == 1
        assert result["pending"] == 1
        assert result["skipped"] == 2
        assert result["cancelled"] == 1
        assert result["failedChecks"] == ["x"]
        assert result["pendingChecks"] == ["y"]
