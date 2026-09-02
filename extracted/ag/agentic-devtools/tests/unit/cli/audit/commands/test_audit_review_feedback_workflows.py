"""Compliance tests for audit workflow YAML files."""

from __future__ import annotations

from pathlib import Path


def _read_workflow(path: str) -> str:
    repo_root = Path(__file__).resolve().parents[5]
    return (repo_root / ".github" / "workflows" / path).read_text(encoding="utf-8")


class TestAuditWorkflowYamlCompliance:
    """Ensure audit workflows stay thin and delegate logic to CLI commands."""

    def test_review_feedback_workflow_uses_cli_not_direct_api_calls(self) -> None:
        content = _read_workflow("audit-review-feedback.yml")
        assert "agdt-audit-prepare" in content
        assert "agdt-audit-dispatch-evaluation" in content
        assert "gh api" not in content
        assert "curl -X" not in content

    def test_review_feedback_workflow_limits_default_token_permissions(self) -> None:
        content = _read_workflow("audit-review-feedback.yml")
        assert "pull-requests: read" in content
        assert "issues: read" in content
        assert "GH_TOKEN: ${{ secrets.SPECKIT_PR_TOKEN }}" in content

    def test_apply_workflow_uses_audit_apply_command(self) -> None:
        content = _read_workflow("audit-review-feedback-apply.yml")
        assert "agdt-audit-apply" in content
        assert "gh api" not in content
        assert "curl -X" not in content

    def test_apply_workflow_validates_batch_meta_contract(self) -> None:
        content = _read_workflow("audit-review-feedback-apply.yml")
        assert "Expected exactly one batch-meta.json under audit-batches/" in content
        assert "batch-meta.json batch_branch mismatch" not in content
        assert "batch-meta.json is missing batch_id" in content
        assert 'expected_output_dir = f"audit-batches/{batch_id}"' in content
        assert '.replace("\\r", "").replace("\\n", "").strip()' in content

    def test_apply_workflow_triggers_via_pull_request_target_on_eval_prs(self) -> None:
        # The evaluation output is produced by the Copilot cloud coding agent on a
        # copilot/** branch. Its pushes/PR events (GITHUB_TOKEN-class actor) do not
        # start on:push / on:pull_request runs, so the apply must react via
        # pull_request_target (same mechanism as ai-pr-loop-dispatcher.yml).
        content = _read_workflow("audit-review-feedback-apply.yml")
        assert "pull_request_target:" in content
        assert "on:\n  push:" not in content
        assert "synchronize" in content
        assert "ready_for_review" in content
        assert '- "audit-batches/**/agent-output/**"' in content
        # Same-repo guard + head-branch gating for the agent's copilot/** (and the
        # audit/batch-* staging) branches.
        assert "github.event.pull_request.head.repo.full_name == github.repository" in content
        assert "github.event.pull_request.head.ref, 'copilot/'" in content
        assert "github.event.pull_request.head.ref, 'audit/batch-'" in content

    def test_apply_workflow_has_required_token_permissions(self) -> None:
        content = _read_workflow("audit-review-feedback-apply.yml")
        # The apply-audit job needs write permissions so the ambient GITHUB_TOKEN
        # can push the instruction-update branch (split-identity: push via
        # GITHUB_TOKEN, PR creation via SPECKIT_PR_TOKEN).
        assert "contents: write" in content
        assert "pull-requests: write" in content
        assert "issues: write" in content
        assert "GH_TOKEN: ${{ secrets.SPECKIT_PR_TOKEN }}" in content

    def test_takeover_workflow_uses_cli_and_not_raw_api_calls(self) -> None:
        content = _read_workflow("audit-takeover-eval-prs.yml")
        assert "agdt-audit-takeover-eval-prs" in content
        assert "gh api" not in content
        assert "curl -X" not in content

    def test_takeover_workflow_runs_every_four_hours_one_at_a_time(self) -> None:
        content = _read_workflow("audit-takeover-eval-prs.yml")
        assert "schedule:" in content
        assert '- cron: "23 */4 * * *"' in content
        # Default to reclaiming a single PR per run to avoid bursts.
        assert 'default: "1"' in content
        assert "--max-prs" in content

    def test_takeover_workflow_reclaims_under_human_identity_with_token(self) -> None:
        content = _read_workflow("audit-takeover-eval-prs.yml")
        # A human git identity is required so the reclaim commit/force-push emits a
        # human synchronize event that un-gates the apply workflow.
        assert 'git config user.name "AMARSNIK_swica"' in content
        assert "token: ${{ secrets.SPECKIT_PR_TOKEN }}" in content
        assert "fetch-depth: 0" in content
        assert "SPECKIT_PR_TOKEN secret is not configured or empty" in content
        assert "GH_TOKEN: ${{ secrets.SPECKIT_PR_TOKEN }}" in content
