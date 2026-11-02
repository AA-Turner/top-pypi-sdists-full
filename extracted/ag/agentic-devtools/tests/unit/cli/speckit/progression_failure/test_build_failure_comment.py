"""Behavioral tests for SpecKit progression failure comments."""

import json

from agentic_devtools.cli.speckit.progression_failure import build_failure_comment


class TestBuildFailureComment:
    def test_failed_task_restart_guard_requires_fresh_phase_one_dispatch(self) -> None:
        body = build_failure_comment(
            phase="3",
            phase_name="plan-tasks-analyze",
            repo="owner/repo",
            run_id="123",
            gate_result="",
            critical_findings="[]",
            artifact_gate_result="",
            artifact_gate_violations="",
            created_pr_number="",
            created_pr_url="",
            label_setup_status="",
            hierarchy_level="feature",
            task_restart_guard_failed=True,
            hierarchy_reason="parent-spec-missing",
        )

        assert "## ❌ SpecKit: Phase 3 Requires a Fresh Phase 1 Dispatch" in body
        assert "standalone Feature (parent-spec-missing)" in body
        assert "do not retry the current later phase" in body

    def test_critical_failure_without_pr_renders_and_escapes_findings(self) -> None:
        body = build_failure_comment(
            phase="2",
            phase_name="clarify",
            repo="owner/repo",
            run_id="123",
            gate_result="fail",
            critical_findings=json.dumps(
                [{"id": "C1", "summary": "first\nsecond | value", "recommendation": "fix | retry"}]
            ),
            artifact_gate_result="",
            artifact_gate_violations="",
            created_pr_number="",
            created_pr_url="",
            label_setup_status="",
            hierarchy_level="feature",
        )

        assert "## ❌ SpecKit: CRITICAL Gate Failed" in body
        assert "**Phase 2** analysis detected unresolved CRITICAL findings" in body
        assert "| C1 | first second \\| value | fix \\| retry |" in body
        assert "https://github.com/owner/repo/actions/runs/123" in body

    def test_existing_pr_lists_all_merge_blockers_and_recovery_actions(self) -> None:
        body = build_failure_comment(
            phase="2",
            phase_name="clarify",
            repo="owner/repo",
            run_id="123",
            gate_result="fail",
            critical_findings='[{"id":"C1","summary":"critical","recommendation":"fix"}]',
            artifact_gate_result="fail",
            artifact_gate_violations="missing spec.md",
            created_pr_number="43",
            created_pr_url="https://github.com/owner/repo/pull/43",
            label_setup_status="failed",
            hierarchy_level="feature",
        )

        assert "PR Created, Routing Labels Failed" in body
        assert "Do not merge until the required routing labels are present" in body
        assert "the CRITICAL findings are resolved and the analysis gate passes" in body
        assert "the artifact violations are resolved and the artifact gate passes" in body
        assert "`speckit:phase-2`, `speckit:level-feature`" in body
        assert "### CRITICAL Gate Findings" in body
        assert "### Artifact Gate Violations" in body
        assert (
            'gh api --method POST "repos/owner/repo/issues/43/labels" \\\n'
            '  --field "labels[]=speckit:phase-2" \\\n'
            '  --field "labels[]=speckit:level-feature"'
        ) in body
        assert 'gh api --paginate "repos/owner/repo/issues/43/labels"' in body
        assert "Resolve the gate findings above, rerun the applicable checks" in body
        assert "resolve the gate findings and re-run their checks before manually dispatching Phase 3" in body

    def test_existing_pr_without_gate_failures_uses_verified_completion_guidance(self) -> None:
        body = build_failure_comment(
            phase="3",
            phase_name="plan-tasks-analyze",
            repo="owner/repo",
            run_id="123",
            gate_result="pass",
            critical_findings="[]",
            artifact_gate_result="pass",
            artifact_gate_violations="",
            created_pr_number="43",
            created_pr_url="",
            label_setup_status="",
            hierarchy_level="unknown",
        )

        assert "PR Created, Workflow Incomplete" in body
        assert "Check the workflow logs before merging" in body
        assert "speckit:phase-3" in body
        assert "speckit:level-" not in body
        assert "Merge the PR after confirming the workflow completed successfully." in body
        assert "Phase 4 is not a valid dispatch phase." in body
        assert "Gate Findings" not in body

    def test_existing_pr_url_without_number_uses_manual_rest_recovery(self) -> None:
        body = build_failure_comment(
            phase="1",
            phase_name="specify",
            repo="owner/repo",
            run_id="123",
            gate_result="",
            critical_findings="[]",
            artifact_gate_result="",
            artifact_gate_violations="",
            created_pr_number="",
            created_pr_url="https://github.com/owner/repo/pull/43",
            label_setup_status="",
            hierarchy_level="epic",
        )

        assert "Use the PR URL to determine its number" in body
        assert "speckit:level-epic" not in body
        assert 'gh api --paginate "repos/owner/repo/issues/<PR_NUMBER>/labels"' in body
        assert "manually dispatch Phase 2" in body

    def test_generic_failure_and_malformed_critical_findings_are_explained(self) -> None:
        generic = build_failure_comment(
            phase="1",
            phase_name="specify",
            repo="owner/repo",
            run_id="123",
            gate_result="",
            critical_findings="[]",
            artifact_gate_result="",
            artifact_gate_violations="",
            created_pr_number="",
            created_pr_url="",
            label_setup_status="",
            hierarchy_level="unknown",
        )
        malformed = build_failure_comment(
            phase="1",
            phase_name="specify",
            repo="owner/repo",
            run_id="123",
            gate_result="fail",
            critical_findings="not-json",
            artifact_gate_result="",
            artifact_gate_violations="",
            created_pr_number="43",
            created_pr_url="",
            label_setup_status="",
            hierarchy_level="unknown",
        )

        assert "## ❌ SpecKit: Phase 1 (specify) Failed" in generic
        assert "COPILOT_GITHUB_TOKEN secret is configured" in generic
        assert "_Could not parse findings: not-json_" in malformed

    def test_empty_or_invalid_shape_critical_findings_have_safe_fallbacks(self) -> None:
        empty = build_failure_comment(
            phase="1",
            phase_name="specify",
            repo="owner/repo",
            run_id="123",
            gate_result="fail",
            critical_findings="[]",
            artifact_gate_result="",
            artifact_gate_violations="",
            created_pr_number="43",
            created_pr_url="",
            label_setup_status="",
            hierarchy_level="unknown",
        )
        invalid_shape = build_failure_comment(
            phase="1",
            phase_name="specify",
            repo="owner/repo",
            run_id="123",
            gate_result="fail",
            critical_findings="{}",
            artifact_gate_result="",
            artifact_gate_violations="",
            created_pr_number="43",
            created_pr_url="",
            label_setup_status="",
            hierarchy_level="unknown",
        )

        assert "_The CRITICAL gate failed; review the workflow logs for the findings._" in empty
        assert "_Could not parse findings: {}_" in invalid_shape
