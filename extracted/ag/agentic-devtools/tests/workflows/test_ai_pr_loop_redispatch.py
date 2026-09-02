"""Tests for ai-pr-loop-redispatch.yml workflow structure."""

from pathlib import Path

import yaml

REPO_ROOT = Path(__file__).resolve().parents[2]
AI_PR_LOOP_REDISPATCH = REPO_ROOT / ".github" / "workflows" / "ai-pr-loop-redispatch.yml"


class TestAiPrLoopRedispatch:
    """Validates ai-pr-loop-redispatch workflow structure and requirements."""

    def test_workflow_file_exists(self) -> None:
        assert AI_PR_LOOP_REDISPATCH.exists()

    def test_valid_yaml(self) -> None:
        content = AI_PR_LOOP_REDISPATCH.read_text(encoding="utf-8")
        parsed = yaml.safe_load(content)
        assert parsed is not None
        assert "jobs" in parsed
        assert "smart-redispatch" in parsed["jobs"]

    def test_has_only_workflow_dispatch_trigger(self) -> None:
        content = AI_PR_LOOP_REDISPATCH.read_text(encoding="utf-8")
        parsed = yaml.safe_load(content)
        triggers = set(parsed[True].keys()) if isinstance(parsed[True], dict) else set()
        assert triggers == {"workflow_dispatch"}

    def test_has_required_permissions(self) -> None:
        content = AI_PR_LOOP_REDISPATCH.read_text(encoding="utf-8")
        assert "actions: write" in content
        assert "pull-requests: read" in content
        assert "contents: read" in content

    def test_has_concurrency_group_with_cancel(self) -> None:
        content = AI_PR_LOOP_REDISPATCH.read_text(encoding="utf-8")
        assert "group: ai-pr-loop-redispatch" in content
        assert "cancel-in-progress: false" in content

    def test_has_timeout_minutes_8(self) -> None:
        content = AI_PR_LOOP_REDISPATCH.read_text(encoding="utf-8")
        assert "timeout-minutes: 8" in content

    def test_uses_stop_condition_writer_token_with_fallback(self) -> None:
        content = AI_PR_LOOP_REDISPATCH.read_text(encoding="utf-8")
        check_step = content[
            content.index("- name: Check stop conditions") : content.index("- name: Wait until safe to dispatch")
        ]
        assert "GH_TOKEN: ${{ secrets.REPO_VARIABLE_WRITER_PAT }}" in check_step
        assert "FALLBACK_GH_TOKEN: ${{ secrets.SPECKIT_PR_TOKEN }}" in check_step
        assert "falling back to SPECKIT_PR_TOKEN for stop-condition checks" in check_step

    def test_uses_speckit_pr_token(self) -> None:
        content = AI_PR_LOOP_REDISPATCH.read_text(encoding="utf-8")
        assert "SPECKIT_PR_TOKEN" in content

    def test_uses_independent_writer_for_final_dispatch_with_fallback(self) -> None:
        content = AI_PR_LOOP_REDISPATCH.read_text(encoding="utf-8")
        dispatch_step = content[content.index("- name: Dispatch ai-pr-loop-throttler") :]
        assert "GH_TOKEN: ${{ secrets.REPO_VARIABLE_WRITER_PAT }}" in dispatch_step
        assert "FALLBACK_GH_TOKEN: ${{ secrets.SPECKIT_PR_TOKEN }}" in dispatch_step
        assert "falling back to SPECKIT_PR_TOKEN" in dispatch_step

    def test_checks_for_eligible_open_prs(self) -> None:
        content = AI_PR_LOOP_REDISPATCH.read_text(encoding="utf-8")
        assert "ai-pr-loop-ignore" in content
        assert "should_dispatch=false" in content
        assert "should_dispatch=true" in content

    def test_checks_24_hour_stale_merge_guard(self) -> None:
        content = AI_PR_LOOP_REDISPATCH.read_text(encoding="utf-8")
        assert "24" in content
        assert "HOURS_SINCE_MERGE" in content

    def test_delegates_cooldown_timing_to_watchdog(self) -> None:
        content = AI_PR_LOOP_REDISPATCH.read_text(encoding="utf-8")
        assert "--mode redispatch-wait" in content
        assert 'while [ "$remaining" -gt 0 ]' not in content

    def test_sleeps_before_dispatch(self) -> None:
        content = AI_PR_LOOP_REDISPATCH.read_text(encoding="utf-8")
        assert "--mode redispatch-wait" in content

    def test_dispatches_ai_pr_loop_throttler(self) -> None:
        content = AI_PR_LOOP_REDISPATCH.read_text(encoding="utf-8")
        assert "gh workflow run ai-pr-loop-throttler.yml" in content
        assert "default_branch" in content

    def test_stop_conditions_are_guarded(self) -> None:
        """Stop condition steps only run when should_dispatch is true."""
        content = AI_PR_LOOP_REDISPATCH.read_text(encoding="utf-8")
        assert "steps.check.outputs.should_dispatch == 'true'" in content

    def test_exits_cleanly_on_no_eligible_prs(self) -> None:
        content = AI_PR_LOOP_REDISPATCH.read_text(encoding="utf-8")
        assert "No eligible open PRs" in content

    def test_exits_cleanly_on_stale_main(self) -> None:
        content = AI_PR_LOOP_REDISPATCH.read_text(encoding="utf-8")
        assert "human intervention" in content

    def test_stop_conditions_run_before_cooldown_wait(self) -> None:
        """Stop conditions are checked before the cooldown wait to avoid wasting Actions time."""
        parsed = yaml.safe_load(AI_PR_LOOP_REDISPATCH.read_text(encoding="utf-8"))
        steps = parsed["jobs"]["smart-redispatch"]["steps"]
        step_ids = [s.get("id", "") for s in steps]
        check_idx = step_ids.index("check")
        timing_idx = step_ids.index("timing")
        assert check_idx < timing_idx, "stop-condition 'check' step must precede 'timing' wait step"

    def test_cooldown_wait_gated_on_stop_conditions(self) -> None:
        """Cooldown wait only runs when stop conditions allow dispatch."""
        parsed = yaml.safe_load(AI_PR_LOOP_REDISPATCH.read_text(encoding="utf-8"))
        steps = parsed["jobs"]["smart-redispatch"]["steps"]
        timing_step = next(s for s in steps if s.get("id") == "timing")
        assert "steps.check.outputs.should_dispatch == 'true'" in (timing_step.get("if") or "")

    def test_does_not_duplicate_a_shell_cooldown_gate(self) -> None:
        """Redispatch defers cooldown parsing to the watchdog wait command."""
        parsed = yaml.safe_load(AI_PR_LOOP_REDISPATCH.read_text(encoding="utf-8"))
        step_ids = [step.get("id", "") for step in parsed["jobs"]["smart-redispatch"]["steps"]]
        assert "cooldown-gate" not in step_ids
