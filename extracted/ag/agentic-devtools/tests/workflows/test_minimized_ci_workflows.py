"""Tests for minimized CI workflow YAMLs."""

import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
AI_PR_LOOP = REPO_ROOT / ".github" / "workflows" / "ai-pr-loop.yml"
AI_PR_LOOP_LINT = REPO_ROOT / ".github" / "workflows" / "ai-pr-loop-lint.yml"
GENERATE_SPEC_FROM_ISSUE = REPO_ROOT / ".github" / "scripts" / "speckit-trigger" / "generate-spec-from-issue.sh"
RESOLVE_CASCADE_TARGET = REPO_ROOT / ".github" / "scripts" / "speckit-trigger" / "resolve-cascade-target.sh"
SPECKIT_TRIGGER = REPO_ROOT / ".github" / "workflows" / "speckit-issue-trigger.yml"
SPECKIT_PHASE_PROGRESSION = REPO_ROOT / ".github" / "workflows" / "speckit-phase-progression.yml"
WORKFLOW_APPROVAL_MONITOR = REPO_ROOT / ".github" / "workflows" / "workflow-approval-monitor.yml"
SQUASH_WAIT_SCHEDULER = REPO_ROOT / ".github" / "workflows" / "squash-wait-scheduler.yml"
AI_PR_LOOP_CONFIG = REPO_ROOT / ".github" / "ai-pr-loop-config.json"
SPECKIT_IMPLEMENT_TRIGGER = REPO_ROOT / ".github" / "workflows" / "speckit-implement-trigger.yml"
SUPPRESSED_TRIAGE_REAP = REPO_ROOT / ".github" / "workflows" / "suppressed-triage-reap.yml"


def _non_empty_line_count(path: Path) -> int:
    return sum(1 for line in path.read_text(encoding="utf-8").splitlines() if line.strip())


class TestMinimizedCiWorkflows:
    """Validates minimized workflow structure and limits."""

    def test_ai_pr_loop_is_within_line_limit(self) -> None:
        assert _non_empty_line_count(AI_PR_LOOP) <= 150

    def test_speckit_trigger_is_within_line_limit(self) -> None:
        assert _non_empty_line_count(SPECKIT_TRIGGER) <= 230

    def test_ai_pr_loop_uses_single_command_with_feature_flag(self) -> None:
        content = AI_PR_LOOP.read_text(encoding="utf-8")
        assert 'AGDT_USE_PYTHON_ORCHESTRATOR: "1"' in content
        assert content.count("agdt-ai-pr-loop") == 1

    def test_speckit_trigger_dispatches_to_phase_progression(self) -> None:
        content = SPECKIT_TRIGGER.read_text(encoding="utf-8")
        assert "gh api" in content
        assert "speckit-phase-progression.yml" in content

    def test_ai_pr_loop_has_required_setup_steps(self) -> None:
        content = AI_PR_LOOP.read_text(encoding="utf-8")
        assert "actions/setup-python" in content
        assert "pip install" in content
        assert "actions/checkout" in content

    def test_ai_pr_loop_run_name_renders_pr_number(self) -> None:
        """A literal '#' truncates the rendered run name, hiding the PR number."""
        content = AI_PR_LOOP.read_text(encoding="utf-8")
        assert "run-name: AI PR Loop (PR ${{ inputs.pr_number }})" in content
        assert "PR #${{ inputs.pr_number }}" not in content

    def test_ai_pr_loop_caches_dependency_installs(self) -> None:
        content = AI_PR_LOOP.read_text(encoding="utf-8")
        assert "cache: 'pip'" in content
        assert "enable-cache: true" in content
        assert "cache-dependency-glob: 'pyproject.toml'" in content

    def test_ai_pr_loop_uses_writer_token_for_rate_limit_redispatch(self) -> None:
        content = AI_PR_LOOP.read_text(encoding="utf-8")
        assert "id: run-loop" in content
        assert 'echo "exit_code=${exit_code}" >> "$GITHUB_OUTPUT"' in content
        assert "COOLDOWN_ACTIVE: ${{ steps.cooldown-gate.outputs.cooldown_active }}" in content
        assert "LOOP_EXIT_CODE: ${{ steps.run-loop.outputs.exit_code }}" in content
        assert 'export GH_TOKEN="${REPO_VARIABLE_WRITER_PAT}"' in content

    def test_ai_pr_loop_configures_loop_git_identity(self) -> None:
        content = AI_PR_LOOP.read_text(encoding="utf-8")
        assert 'git config user.name "AMARSNIK_swica"' in content
        assert 'git config user.email "AMARSNIK_swica@users.noreply.github.com"' in content

    def test_speckit_trigger_is_dispatch_only(self) -> None:
        content = SPECKIT_TRIGGER.read_text(encoding="utf-8")
        assert "timeout-minutes: 5" in content
        assert "actions/setup-python" not in content
        assert "pip install" not in content
        assert "actions/checkout" not in content

    def test_ai_pr_loop_has_concurrency_group(self) -> None:
        content = AI_PR_LOOP.read_text(encoding="utf-8")
        assert "concurrency:" in content
        assert "group: ai-pr-loop-${{ inputs.pr_number }}" in content
        assert "replace(replace(replace(" not in content
        assert 'pr_number="${pr_number#"${pr_number%%[! ]*}"}"' not in content

    def test_scheduling_workflows_use_distinct_concurrency_groups(self) -> None:
        """Ensure one scheduling workflow cannot replace another pending run."""
        workflow_dir = REPO_ROOT / ".github" / "workflows"
        expected_groups = {
            "ai-pr-loop-throttler.yml": "ai-pr-loop-throttler",
            "ai-pr-loop-redispatch.yml": "ai-pr-loop-redispatch",
            "ai-pr-loop-watchdog.yml": "ai-pr-loop-watchdog",
        }
        for workflow, group in expected_groups.items():
            content = (workflow_dir / workflow).read_text(encoding="utf-8")
            assert f"group: {group}" in content
            assert "cancel-in-progress: false" in content

    def test_ai_pr_loop_uses_workflow_dispatch_only(self) -> None:
        content = AI_PR_LOOP.read_text(encoding="utf-8")
        assert "workflow_dispatch:" in content
        assert "pull_request:" not in content
        assert "issue_comment:" not in content
        assert "workflow_run:" not in content

    def test_redundant_ai_pr_loop_workflows_are_removed(self) -> None:
        assert not AI_PR_LOOP_LINT.exists()

    def test_workflow_approval_monitor_deleted(self) -> None:
        assert not WORKFLOW_APPROVAL_MONITOR.exists()

    def test_squash_wait_scheduler_deleted(self) -> None:
        assert not SQUASH_WAIT_SCHEDULER.exists()

    def test_ai_pr_loop_config_deleted(self) -> None:
        assert not AI_PR_LOOP_CONFIG.exists()

    def test_copilot_review_gate_workflow_deleted(self) -> None:
        """copilot-review-gate.yml must be removed (logic ported into pipeline v2)."""
        gate = REPO_ROOT / ".github" / "workflows" / "copilot-review-gate.yml"
        assert not gate.exists(), "copilot-review-gate.yml should be deleted — its logic lives in gate_verdict.py"

    def test_speckit_trigger_has_concurrency_group(self) -> None:
        content = SPECKIT_TRIGGER.read_text(encoding="utf-8")
        assert "concurrency:" in content

    def test_suppressed_triage_reap_has_concurrency_group(self) -> None:
        content = SUPPRESSED_TRIAGE_REAP.read_text(encoding="utf-8")
        assert "concurrency:" in content
        assert "suppressed-triage-reap" in content

    def test_speckit_trigger_filters_specs_tree_to_spec_markdown(self) -> None:
        content = SPECKIT_TRIGGER.read_text(encoding="utf-8")
        assert ".filter(t => t.type === 'blob' && t.path.endsWith('/spec.md'))" in content

    def test_speckit_trigger_rejection_removes_configured_label_for_manual_runs(self) -> None:
        content = SPECKIT_TRIGGER.read_text(encoding="utf-8")
        assert "TRIGGER_LABEL: ${{ vars.SPECKIT_TRIGGER_LABEL || 'speckit' }}" in content
        assert "const triggerLabel = context.payload.label?.name || process.env.TRIGGER_LABEL || 'speckit';" in content

    def test_speckit_implement_trigger_validates_assignment_token(self) -> None:
        content = SPECKIT_IMPLEMENT_TRIGGER.read_text(encoding="utf-8")
        assert "- name: Validate Agent Assignment Token" in content
        assert "SPECKIT_PR_TOKEN: ${{ secrets.SPECKIT_PR_TOKEN }}" in content
        assert "COPILOT_GITHUB_TOKEN: ${{ secrets.COPILOT_GITHUB_TOKEN }}" in content
        assert "Neither SPECKIT_PR_TOKEN nor COPILOT_GITHUB_TOKEN is configured" in content

    def test_speckit_implement_trigger_uses_cli_assignment_and_followups(self) -> None:
        content = SPECKIT_IMPLEMENT_TRIGGER.read_text(encoding="utf-8")
        token_line = "github-token: ${{ secrets.SPECKIT_PR_TOKEN || secrets.COPILOT_GITHUB_TOKEN }}"
        assert "steps.validate-token.outcome == 'success'" in content
        assert "agdt-assign-implementation-agent" in content
        assert "SPEC_DIR: ${{ steps.discover.outputs.spec_dir }}" in content
        assert "--spec-context" in content
        assert '--spec-dir "$SPEC_DIR"' in content
        assert '--spec-dir "${{ steps.discover.outputs.spec_dir }}"' not in content
        assert "actions/setup-python@v5" in content
        assert "pip install -e ." in content
        assert token_line in content
        assert content.count(token_line) >= 2
        assert "response.data?.agent_assignment" not in content
        assert "PATCH /repos/{owner}/{repo}/issues/{issue_number}" not in content

    def test_speckit_implement_trigger_collects_both_task_directory_naming_forms(self) -> None:
        content = SPECKIT_IMPLEMENT_TRIGGER.read_text(encoding="utf-8")
        assert (
            'find "$SPECS_DIR" -type d -name "${ISSUE_NUMBER}-*"\n'
            '                find "$SPECS_DIR" -type d -name "${ISSUE_NUMBER}"'
        ) in content
        assert "} | sort -u" in content

    def test_speckit_implement_trigger_rejects_multiple_valid_artifact_matches(self) -> None:
        content = SPECKIT_IMPLEMENT_TRIGGER.read_text(encoding="utf-8")
        assert "VALID_SPEC_CANDIDATES=()" in content
        assert 'candidate="${dir}|${resolved_level}"' in content
        assert "Multiple implementation spec directories match issue" in content

    def test_speckit_implement_trigger_checks_override_conflict_before_epic_skip(self) -> None:
        content = SPECKIT_IMPLEMENT_TRIGGER.read_text(encoding="utf-8")
        conflict_check = (
            'if [[ -n "$OVERRIDE_LEVEL" && -n "$AUTHORITATIVE_LEVEL" && '
            '"$OVERRIDE_LEVEL" != "$AUTHORITATIVE_LEVEL" ]]; then'
        )
        canonical_epic_skip = 'if [[ "$OVERRIDE_LEVEL" == "epic" ]]; then'
        assert conflict_check in content
        assert canonical_epic_skip in content
        assert content.index(conflict_check) < content.index(canonical_epic_skip)

    def test_speckit_implement_trigger_short_circuits_authoritative_epics_before_override_validation(self) -> None:
        content = SPECKIT_IMPLEMENT_TRIGGER.read_text(encoding="utf-8")
        override_gate = 'if [[ -n "$SPEC_DIR_OVERRIDE" ]]; then'
        epic_skip = 'if [[ "$AUTHORITATIVE_LEVEL" == "epic" ]]; then'
        validation_banner = 'echo "Validating provided spec_dir override"'
        assert content.index(override_gate) < content.index(epic_skip) < content.index(validation_banner)

    def test_speckit_implement_trigger_marks_discovery_epic_conflicts_unknown(self) -> None:
        content = SPECKIT_IMPLEMENT_TRIGGER.read_text(encoding="utf-8")
        assert (
            'if [[ "$level" == "epic" && -n "$AUTHORITATIVE_LEVEL" && "$AUTHORITATIVE_LEVEL" != "epic" ]]; then'
        ) in content
        assert 'resolved_level="unknown"' in content

    def test_speckit_implement_trigger_only_ignores_missing_needs_implementation_label(self) -> None:
        content = SPECKIT_IMPLEMENT_TRIGGER.read_text(encoding="utf-8")
        removal_call = (
            "await github.rest.issues.removeLabel({\n"
            "                owner: context.repo.owner,\n"
            "                repo: context.repo.repo,\n"
            "                issue_number: issueNumber,\n"
            "                name: 'speckit:needs-implementation'"
        )
        guarded_removals = re.findall(
            r"await github\.rest\.issues\.removeLabel\(\{\n"
            r"\s+owner: context\.repo\.owner,\n"
            r"\s+repo: context\.repo\.repo,\n"
            r"\s+issue_number: issueNumber,\n"
            r"\s+name: 'speckit:needs-implementation'\n"
            r"\s+\}\);\n"
            r"\s+\} catch \(e\) \{\n"
            r"\s+if \(e\.status !== 404\) \{\n"
            r"\s+(?:throw e|core\.warning\()",
            content,
        )
        assert guarded_removals
        assert content.count(removal_call) == len(guarded_removals)
        # Skip-cleanup steps must use warning instead of throw so a non-404 error
        # cannot trigger the global failure handler and apply speckit:failed.
        assert "Could not remove speckit:needs-implementation label (non-404):" in content

    def test_speckit_implement_trigger_hierarchy_parser_is_quote_aware(self) -> None:
        content = SPECKIT_IMPLEMENT_TRIGGER.read_text(encoding="utf-8")
        assert "python3 - \"$yml\" <<'PY'" in content
        assert "pattern = re.compile" in content
        assert "sed 's/[[:space:]]*#.*//'" not in content

    def test_speckit_implement_trigger_validates_discovered_output_paths_as_single_line(self) -> None:
        content = SPECKIT_IMPLEMENT_TRIGGER.read_text(encoding="utf-8")
        assert "write_single_line_output()" in content
        assert 'write_single_line_output "spec_context" "$PARENT_DIR/spec.md"' in content
        assert 'write_single_line_output "spec_dir" "$SPEC_DIR"' in content
        assert 'echo "spec_context=$PARENT_DIR/spec.md" >> "$GITHUB_OUTPUT"' not in content
        assert 'echo "spec_dir=$SPEC_DIR" >> "$GITHUB_OUTPUT"' not in content

    def test_speckit_phase_progression_uses_top_level_python_c_script(self) -> None:
        content = SPECKIT_PHASE_PROGRESSION.read_text(encoding="utf-8")
        assert "python3 -c $'import json, os, sys" in content
        assert r"\ntry:\n" in content
        assert "json.JSONDecodeError" in content
        assert 'skip_map.get(os.environ["LEVEL"], [])' in content
        assert "sys.exit(1)" in content
        assert 'python3 -c "\n          import sys, json' not in content

    def test_generate_spec_handles_parent_context_errors_inside_if(self) -> None:
        content = GENERATE_SPEC_FROM_ISSUE.read_text(encoding="utf-8")
        assert 'if resolve_parent_context "$SPEC_DIR"; then' in content
        assert 'resolve_parent_context "$SPEC_DIR"\n        local resolve_status=$?' not in content

    def test_speckit_phase_progression_uses_level_aware_final_phase_skip_copy(self) -> None:
        content = SPECKIT_PHASE_PROGRESSION.read_text(encoding="utf-8")
        assert "const finalPhaseCompletionSummary = levelSkipped" in content
        assert "Phase 3 does not apply for hierarchy level" in content
        assert "✅ Skipped (not applicable for" in content

    def test_speckit_phase_progression_extracts_pr_routing_via_shared_helper(self) -> None:
        content = SPECKIT_PHASE_PROGRESSION.read_text(encoding="utf-8")
        assert "extract-phase-info.js" in content
        assert "github.paginate(github.rest.pulls.listFiles" not in content
        assert "github.rest.repos.getContent" not in content

    def test_speckit_phase_progression_validates_token_for_cascade_paths(self) -> None:
        content = SPECKIT_PHASE_PROGRESSION.read_text(encoding="utf-8")
        expected = (
            "Neither SPECKIT_PR_TOKEN nor COPILOT_GITHUB_TOKEN is configured. "
            "Cascade trigger requires one of these secrets."
        )
        assert content.count(expected) == 2

    def test_speckit_phase_progression_uses_null_delimited_hierarchy_search(self) -> None:
        # The find + while-loop logic lives in the shared resolve-cascade-target.sh script.
        script_content = RESOLVE_CASCADE_TARGET.read_text(encoding="utf-8")
        assert 'find "$SPEC_BASE_PATH" -name "hierarchy.yml" -type f -print0' in script_content
        assert script_content.count("while IFS= read -r -d '' yml; do") == 2
        assert (
            'if [[ "$DIR_NAME" == "$DECLARED_PARENT_NUMBER" || "$DIR_NAME" == "$DECLARED_PARENT_NUMBER-"* ]]; then'
            in script_content
        )
        assert "| sed -nE \\" in script_content
        assert "sed 's/.*level:[[:space:]]*//'" not in script_content
        assert 'PARENT_YML="$yml"\n            break' not in script_content
        assert re.search(r"for\s+\w+\s+in\s+\$\( ?find\b", script_content, flags=re.IGNORECASE) is None
        # The workflow itself must not use the unsafe for-in-$(find) pattern either.
        workflow_content = SPECKIT_PHASE_PROGRESSION.read_text(encoding="utf-8")
        assert re.search(r"for\s+\w+\s+in\s+\$\( ?find\b", workflow_content, flags=re.IGNORECASE) is None
