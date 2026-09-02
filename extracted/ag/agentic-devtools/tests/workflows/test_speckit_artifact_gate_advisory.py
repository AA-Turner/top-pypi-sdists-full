"""Tests for the advisory-mode wiring of the SpecKit artifact verification gate.

The gate must not silently become blocking again: when it still reports
violations after its retry budget, the phase artifacts are committed, the pull
request is opened as a draft, ``@copilot`` is asked on that PR to fix the
violations, and auto-merge is suppressed.
"""

import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
GENERATE_SPEC_FROM_ISSUE = REPO_ROOT / ".github" / "scripts" / "speckit-trigger" / "generate-spec-from-issue.sh"
PHASE_PROGRESSION = REPO_ROOT / ".github" / "workflows" / "speckit-phase-progression.yml"
ISSUE_TRIGGER = REPO_ROOT / ".github" / "workflows" / "speckit-issue-trigger.yml"
IMPLEMENT_TRIGGER = REPO_ROOT / ".github" / "workflows" / "speckit-implement-trigger.yml"
EXTRACT_PHASE_INFO = REPO_ROOT / ".github" / "scripts" / "speckit-trigger" / "extract-phase-info.js"
CREATE_SPEC_PR = REPO_ROOT / ".github" / "scripts" / "speckit-trigger" / "create-spec-pr.sh"
COMMIT_LEGACY_MIGRATION = REPO_ROOT / ".github" / "scripts" / "speckit-trigger" / "commit-legacy-migration.sh"


class TestArtifactGateAdvisoryMode:
    """The generator script defaults to advisory mode and publishes its outcome."""

    def test_gate_mode_defaults_to_advisory(self) -> None:
        content = GENERATE_SPEC_FROM_ISSUE.read_text(encoding="utf-8")
        assert 'case "${SPECKIT_ARTIFACT_GATE_MODE:-advisory}" in' in content
        assert 'ARTIFACT_GATE_MODE="advisory"' in content

    def test_block_mode_remains_available(self) -> None:
        content = GENERATE_SPEC_FROM_ISSUE.read_text(encoding="utf-8")
        assert "advisory | block)" in content
        assert "No pull request will be opened." in content

    def test_gate_publishes_step_outputs(self) -> None:
        content = GENERATE_SPEC_FROM_ISSUE.read_text(encoding="utf-8")
        assert "publish_artifact_gate_outcome() {" in content
        assert 'echo "artifact_gate_result=$status"' in content
        # Phase number/name outputs use accumulated values so that all failing
        # sub-phases within a merged pipeline phase are reported together.
        assert (
            'echo "artifact_gate_phase_number=${ARTIFACT_GATE_PHASE_NUMBERS:-${ARTIFACT_GATE_PHASE_NUMBER:-}}"'
            in content
        )
        assert 'echo "artifact_gate_phase_name=${ARTIFACT_GATE_PHASE_NAMES:-${ARTIFACT_GATE_PHASE_NAME:-}}"' in content
        assert 'echo "artifact_gate_violations<<AGDT_ARTIFACT_VIOLATIONS_EOF"' in content

    def test_gate_accumulates_phase_numbers_across_multiple_failures(self) -> None:
        """Multiple sub-phase failures accumulate phase IDs rather than overwriting them."""
        content = GENERATE_SPEC_FROM_ISSUE.read_text(encoding="utf-8")
        assert "ARTIFACT_GATE_PHASE_NUMBERS" in content
        assert "ARTIFACT_GATE_PHASE_NAMES" in content
        # Deduplication guard: a phase is not appended twice for the same ID.
        assert '",${ARTIFACT_GATE_PHASE_NUMBERS}," != *",${cur_phase_num},"*' in content
        # Empty-phase-number guard: phases with no ID are skipped to prevent
        # stray commas that would break parallel number/name lists.
        assert 'if [[ -n "$cur_phase_num" ]]; then' in content

    def test_phase3_reconciles_artifact_verification_json_when_gate_failed(self) -> None:
        """After all phase-3 sub-steps an unscoped verification re-run reconciles the JSON report."""
        content = GENERATE_SPEC_FROM_ISSUE.read_text(encoding="utf-8")
        # The reconciliation block must appear in the phase 3 case, before markdownlint.
        # Use the merged-planning-phase comment as the anchor (unique to phase 3).
        phase3_start = content.index("# Merged planning phase: plan")
        markdownlint_start = content.index("=== Markdownlint Validation ===", phase3_start)
        phase3_body = content[phase3_start:markdownlint_start]
        assert 'ARTIFACT_GATE_STATUS:-}" == "fail"' in phase3_body
        assert "=== Artifact Verification — Final Consolidated Report ===" in phase3_body
        # Unscoped call: run_artifact_verification "" — the empty-string argument produces an
        # all-checks report that reflects the combined artifact state of all sub-steps.
        assert 'run_artifact_verification "" || final_verify_rc=$?' in phase3_body
        # Accumulated gate state must be reset before the final check so that a pass can
        # propagate to GITHUB_OUTPUT even though publish_artifact_gate_outcome normally
        # blocks pass-over-fail rewrites.
        assert 'ARTIFACT_GATE_STATUS=""' in phase3_body
        assert 'ARTIFACT_GATE_VIOLATIONS=""' in phase3_body
        # The singular ARTIFACT_GATE_PHASE_NUMBER/NAME must also be reset so that stale
        # last-scoped-gate values (e.g. 4/tasks) cannot pollute the consolidated output.
        # They are then set to the merged pipeline phase identity (3/plan-tasks-analyze) so
        # repair metadata correctly names the phase regardless of which sub-step failed.
        assert 'ARTIFACT_GATE_PHASE_NUMBER="3"' in phase3_body
        assert 'ARTIFACT_GATE_PHASE_NAME="plan-tasks-analyze"' in phase3_body
        # The final result must be published so GITHUB_OUTPUT agrees with the committed JSON.
        assert "publish_artifact_gate_outcome pass" in phase3_body
        assert "publish_artifact_gate_outcome fail" in phase3_body


class TestArtifactGateWorkflowWiring:
    """The workflow reacts to a failed gate without discarding the artifacts."""

    def test_gate_mode_is_passed_to_the_generator(self) -> None:
        content = PHASE_PROGRESSION.read_text(encoding="utf-8")
        assert "SPECKIT_ARTIFACT_GATE_MODE: ${{ vars.SPECKIT_ARTIFACT_GATE_MODE }}" in content

    def test_workflow_dispatch_hierarchy_level_defaults_to_auto(self) -> None:
        content = PHASE_PROGRESSION.read_text(encoding="utf-8")
        assert "default: 'auto'" in content
        assert (
            "auto resolves from hierarchy.yml first, then falls back to unknown "
            "(fail-closed — does not apply speckit:needs-implementation)." in content
        )

    def test_hierarchy_resolution_treats_auto_as_unspecified(self) -> None:
        content = PHASE_PROGRESSION.read_text(encoding="utf-8")
        assert 'if [[ "${LEVEL,,}" == "auto" ]]; then' in content
        assert 'LEVEL=""' in content

    def test_timeout_budget_covers_merged_phase_three_retries(self) -> None:
        content = PHASE_PROGRESSION.read_text(encoding="utf-8")
        assert "timeout-minutes: 330" in content
        assert 'SPECKIT_VALIDATE_MAX_RETRIES: "1"' in content

    def test_monolithic_path_reconciles_sticky_gate_status_before_final_unscoped_check(self) -> None:
        content = GENERATE_SPEC_FROM_ISSUE.read_text(encoding="utf-8")
        # Use the monolithic-path marker to isolate the non---phase branch.
        monolithic_start = content.index("# Run all phases sequentially (backward compatible)")
        monolithic_end = content.index('run_artifact_verification_with_retry "" "" || exit $?', monolithic_start)
        monolithic_body = content[monolithic_start:monolithic_end]
        assert "=== Artifact Verification — Final Consolidated Report ===" in monolithic_body
        assert 'ARTIFACT_GATE_STATUS=""' in monolithic_body
        assert 'ARTIFACT_GATE_VIOLATIONS=""' in monolithic_body
        assert 'ARTIFACT_GATE_PHASE_NUMBERS=""' in monolithic_body
        assert 'ARTIFACT_GATE_PHASE_NAMES=""' in monolithic_body
        assert 'ARTIFACT_GATE_PHASE_NUMBER=""' in monolithic_body
        assert 'ARTIFACT_GATE_PHASE_NAME=""' in monolithic_body

    def test_failed_gate_opens_the_pr_as_a_draft(self) -> None:
        content = PHASE_PROGRESSION.read_text(encoding="utf-8")
        assert 'elif [[ "${ARTIFACT_GATE_RESULT:-}" == "fail" ]]; then' in content

    def test_failed_gate_reenforces_draft_state_for_existing_prs(self) -> None:
        content = PHASE_PROGRESSION.read_text(encoding="utf-8")
        assert "--enforce-draft-state" in content
        assert "Pre-Push Draft Existing PR for Advisory Artifact Gate" in content
        assert (
            'gh pr view "$EXISTING_PR_NUMBER" --repo "$GITHUB_REPOSITORY" --json isDraft --jq \'.isDraft\'' in content
        )
        assert 'if [[ "$IS_DRAFT" != "true" ]]; then' in content
        assert 'gh pr ready "$EXISTING_PR_NUMBER" --undo' in content
        assert '--remove-label "ai-auto-merge-allowed"' in content
        assert content.index("Pre-Push Draft Existing PR for Advisory Artifact Gate") < content.index("Push Branch")

    def test_failed_gate_requests_a_copilot_fix_on_the_pr(self) -> None:
        content = PHASE_PROGRESSION.read_text(encoding="utf-8")
        assert "Request Copilot Fix for Artifact Violations" in content
        assert "steps.generate.outputs.artifact_gate_result == 'fail'" in content
        # The orchestration lives in a tested CLI command, not in the YAML.
        assert "agdt-speckit-request-artifact-fix" in content

    def test_copilot_fix_comment_carries_the_violations(self) -> None:
        content = PHASE_PROGRESSION.read_text(encoding="utf-8")
        assert "VIOLATIONS: ${{ steps.generate.outputs.artifact_gate_violations }}" in content
        assert '--violations "${VIOLATIONS:-}"' in content
        assert '--hierarchy-level "${HIERARCHY_LEVEL:-}"' in content

    def test_copilot_fix_comment_uses_the_failing_internal_gate_phase_when_available(self) -> None:
        content = PHASE_PROGRESSION.read_text(encoding="utf-8")
        assert (
            "PHASE_NUMBER: ${{ steps.generate.outputs.artifact_gate_phase_number || steps.extract.outputs.next_phase }}"
        ) in content
        assert (
            "PHASE_NAME: ${{ steps.generate.outputs.artifact_gate_phase_name || "
            "steps.extract.outputs.next_phase_name }}"
        ) in content

    def test_failed_gate_suppresses_auto_merge(self) -> None:
        content = PHASE_PROGRESSION.read_text(encoding="utf-8")
        assert content.count("steps.generate.outputs.artifact_gate_result != 'fail'") == 2

    def test_final_phase_uses_terminal_artifacts_to_disambiguate_merged_phase_three(self) -> None:
        workflow_content = PHASE_PROGRESSION.read_text(encoding="utf-8")
        helper_content = EXTRACT_PHASE_INFO.read_text(encoding="utf-8")
        assert "extract-phase-info.js" in workflow_content
        assert "github.paginate(github.rest.pulls.listFiles" in helper_content
        assert "const completedPhaseMatch = findFirstLabelMatch(labels, /^speckit:phase-(\\d+)$/);" in helper_content
        assert "const hierarchyLabelMatches = labels" in helper_content
        assert "const activeFiles = changedFiles.filter(file => file.status !== 'removed');" in helper_content
        assert "const candidateSpecDirs = new Set(" in helper_content
        assert "github.rest.repos.getContent" in helper_content
        assert "ref: mergeCommitSha," in helper_content
        assert "const hasHierarchyEntry = hierarchyEntries.length > 0;" in helper_content
        assert "const hierarchyContent = typeof hierarchyEntries[0]?.content === 'string'" in helper_content
        assert "const SUPPORTED_LEVELS = new Set(['epic', 'feature', 'task']);" in helper_content
        assert "const HIERARCHY_LEVEL_PATTERN =" in helper_content
        assert "const HIERARCHY_LEVEL_PATTERN = /^level:" in helper_content
        assert "for (const line of hierarchyContent.split(/\\r?\\n/)) {" in helper_content
        assert "if (rawLevel !== null) {" in helper_content
        assert "return returnMetadata ? { level: fallbackLevel, valid: false } : fallbackLevel;" in helper_content
        assert "hierarchyMatch.slice(1).find(group => group !== undefined).trim().toLowerCase()" in helper_content
        assert (
            "const valid = declarationCount === 1 && parsedDeclarationCount === 1 && SUPPORTED_LEVELS.has(rawLevel);"
            in helper_content
        )
        assert "hasTerminalArtifactSet(level, hasPlanArtifact, hasTasksArtifact, hasAnalysisReport)" in helper_content
        assert "core.setOutput('terminal_hierarchy_level', terminalHierarchyLevel);" in helper_content

    def test_implement_trigger_hierarchy_reader_matches_only_top_level_level_key(self) -> None:
        content = (REPO_ROOT / ".github" / "workflows" / "speckit-implement-trigger.yml").read_text(encoding="utf-8")
        assert 'pattern = re.compile(r"^level:' in content
        assert (
            "const levelPattern = /^level:[ \\t]*(?:"
            '"([^"]*)"'
            "|'([^']*)'|([^#\"'\\n]*?))(?:[ \\t]+#.*)?[ \\t]*$/gm;" in content
        )

    def test_final_completion_comment_uses_the_derived_terminal_hierarchy_level(self) -> None:
        content = PHASE_PROGRESSION.read_text(encoding="utf-8")
        assert "const hierarchyLevel = '${{ steps.extract.outputs.terminal_hierarchy_level }}';" in content
        assert (
            "All applicable phases of the SpecKit pipeline have been completed "
            "(Phase 3 was already present — skipped generation)." in content
        )

    def test_create_pr_step_passes_hierarchy_level_for_pr_label_persistence(self) -> None:
        content = PHASE_PROGRESSION.read_text(encoding="utf-8")
        assert "HIERARCHY_LEVEL: ${{ steps.hierarchy.outputs.hierarchy_level }}" in content

    def test_final_phase_complete_cascade_prerequisites_skip_unknown_hierarchy(self) -> None:
        content = PHASE_PROGRESSION.read_text(encoding="utf-8")
        assert "steps.extract.outputs.terminal_hierarchy_level != 'unknown'" in content

    def test_final_phase_skipped_cascade_prerequisites_skip_unknown_hierarchy(self) -> None:
        content = PHASE_PROGRESSION.read_text(encoding="utf-8")
        assert "steps.hierarchy.outputs.hierarchy_level != 'unknown'" in content

    def test_spec_generation_pipeline_steps_gate_on_unknown_hierarchy(self) -> None:
        """Spec generation must not run for unknown hierarchy — generate-spec-from-issue.sh
        converts unknown→feature at lines 175-178, so the workflow must stop before reaching it.
        Verify that all live generation steps carry the fail-closed unknown guard."""
        content = PHASE_PROGRESSION.read_text(encoding="utf-8")
        guard = (
            "steps.idempotency.outputs.skipped != 'true' "
            "&& steps.phase_applicable.outputs.phase_skipped != 'true' "
            "&& steps.hierarchy.outputs.hierarchy_level != 'unknown'"
        )
        assert guard in content

    def test_phase_progression_preserves_explicit_non_epic_hierarchy_input(self) -> None:
        content = PHASE_PROGRESSION.read_text(encoding="utf-8")
        assert 'elif [[ -z "$LEVEL" && -n "$EXTRACT_LEVEL" ]]; then' in content

    def test_issue_trigger_resolves_unknown_fail_closed_and_protects_authoritative_epics(self) -> None:
        content = ISSUE_TRIGGER.read_text(encoding="utf-8")
        assert "let level = 'unknown';" in content
        assert "github.rest.issues.get" in content
        assert "recursive: '1'" in content
        assert "let authoritativeLevel = '', authoritativeConflict = false;" in content
        assert "authoritativeConflict = true;" in content
        assert "authoritativeLevel === 'epic'" in content
        assert "} else if (authoritativeConflict) {" in content
        assert "authoritativeLevel === 'epic' ? 'epic' : 'unknown';" in content
        assert "if (authoritativeLevel === 'epic') { level = 'epic'; }" in content
        assert (
            "const hierarchyLevelPattern = /^level:[ \\t]*(?:"
            '"([^"]*)"'
            "|'([^']*)'|([^#\"'\\n]*?))(?:[ \\t]+#.*)?[ \\t]*$/gm;" in content
        )
        assert "using first sorted match" not in content

    def test_implementation_trigger_rechecks_hierarchy_before_assignment(self) -> None:
        content = IMPLEMENT_TRIGGER.read_text(encoding="utf-8")
        gate = content.index("- name: Final Hierarchy Gate")
        assignment = content.index("agdt-assign-implementation-agent")
        assert gate < assignment
        assert "steps.final-gate.outputs.allowed == 'true'" in content
        assert "issueReadSucceeded = true;" in content
        assert "const nonEpicLevels = ['task', 'feature'].filter(level => values.includes(level));" in content
        assert "Issue #${issueNumber} has conflicting authoritative levels:" in content
        assert "hierarchy metadata conflicts with issue metadata; failing closed as unknown." in content
        assert "Missing canonical hierarchy metadata for issue #${issueNumber}; failing closed." in content
        assert "skip_reason=unknown" in content
        assert "without adding speckit:failed" in content

    def test_implementation_trigger_failure_handlers_skip_confirmed_assignments(self) -> None:
        content = IMPLEMENT_TRIGGER.read_text(encoding="utf-8")
        comment_guard = "".join(
            [
                "if: failure() && steps.assign-agent.outputs.assigned != 'true'",
                " && vars.SPECKIT_COMMENT_ON_ISSUE != 'false'",
            ]
        )
        assert "if: failure() && steps.assign-agent.outputs.assigned != 'true'" in content
        assert comment_guard in content

    def test_extract_phase_info_rejects_conflicting_non_epic_hierarchy_sources(self) -> None:
        content = EXTRACT_PHASE_INFO.read_text(encoding="utf-8")
        assert "canonicalLevel !== authoritativeLevel" in content
        assert "return 'unknown';" in content
        assert "const resolvedHierarchyLevel = resolveValidatedHierarchyLevel({" in content
        assert "authoritativeLevel === 'epic'" in content
        assert "!ambiguous && (!hasHierarchyEntry || parsedHierarchy.valid)" in content
        assert "fallbackLevel:" in content
        assert "authReadSucceeded && !workspaceResult.ambiguous" in content
        assert (
            "if ((workspaceResult.level && !workspaceResult.ambiguous)"
            " || (authReadSucceeded && (authoritativeLevel || labeledLevel))) {" in content
        )


class TestCreateSpecPrDraftEnforcement:
    """Recovered draft PRs stay non-mergeable after advisory gate failures."""

    def test_script_accepts_enforce_draft_state_flag(self) -> None:
        content = CREATE_SPEC_PR.read_text(encoding="utf-8")
        assert "--enforce-draft-state)" in content

    def test_script_reverts_pr_to_draft_and_strips_auto_merge_label(self) -> None:
        content = CREATE_SPEC_PR.read_text(encoding="utf-8")
        assert 'gh pr ready "$pr_selector" --undo --repo "$REPO_SLUG"' in content
        assert '--remove-label "ai-auto-merge-allowed"' in content

    def test_phase3_title_uses_hierarchy_neutral_artifact_label(self) -> None:
        content = CREATE_SPEC_PR.read_text(encoding="utf-8")
        assert '3) PHASE_ARTIFACT="planning artifacts" ;;' in content

    def test_final_phase_next_steps_are_hierarchy_neutral(self) -> None:
        content = CREATE_SPEC_PR.read_text(encoding="utf-8")
        assert "Review the generated planning artifacts for accuracy and completeness" in content

    def test_phase_prs_persist_the_normalized_hierarchy_level_as_a_label(self) -> None:
        content = CREATE_SPEC_PR.read_text(encoding="utf-8")
        assert 'HIERARCHY_LEVEL="${HIERARCHY_LEVEL:-}"' in content
        assert 'HIERARCHY_LABEL="speckit:level-${HIERARCHY_LEVEL}"' in content


class TestLegacyMigrationFlow:
    """Phase-5 migration commits must follow the branch/PR flow."""

    def test_migration_script_no_longer_pushes_directly_to_main(self) -> None:
        content = COMMIT_LEGACY_MIGRATION.read_text(encoding="utf-8")
        assert "git push origin HEAD:main" not in content

    def test_phase_progression_routes_migration_commit_to_standard_push_and_pr_steps(self) -> None:
        content = PHASE_PROGRESSION.read_text(encoding="utf-8")
        assert "id: commit_legacy_migration" in content
        assert (
            '.github/scripts/speckit-trigger/commit-legacy-migration.sh "$ISSUE_NUMBER" "$SPEC_DIR" "$BRANCH_NAME"'
            in content
        )
        assert "steps.commit_legacy_migration.outputs.branch_name" in content
        assert "steps.commit_legacy_migration.outputs.spec_dir" in content

    def test_downstream_post_pr_steps_accept_the_migration_commit_path(self) -> None:
        content = PHASE_PROGRESSION.read_text(encoding="utf-8")
        migration_success = (
            "steps.commit_legacy_migration.outcome == 'success' && "
            "steps.commit_legacy_migration.outputs.commit_created == 'true'"
        )
        for step_name in (
            "Add ai-auto-merge-allowed label (non-clarify phases)",
            "Auto-Merge (if configured)",
            "Post Phase Progress Comment",
        ):
            step_start = content.find(f"- name: {step_name}")
            assert step_start != -1, f"Step {step_name!r} not found in workflow file"
            next_step = re.search(r"^\s+- name:", content[step_start + 1 :], flags=re.MULTILINE)
            step_end = -1 if next_step is None else step_start + 1 + next_step.start()
            step_block = content[step_start:] if step_end == -1 else content[step_start:step_end]
            assert migration_success in step_block

    def test_phase_progress_comment_uses_migration_branch_fallback(self) -> None:
        content = PHASE_PROGRESSION.read_text(encoding="utf-8")
        assert (
            "BRANCH_NAME_OUTPUT: ${{ steps.commit.outputs.branch_name || "
            "steps.commit_legacy_migration.outputs.branch_name }}"
        ) in content
        assert "const branchName = process.env.BRANCH_NAME_OUTPUT;" in content


class TestExtractPhaseInfoGeneratedDiagnostics:
    """extract-phase-info.js must treat all generated/ files as spec-dir candidates."""

    def test_all_generated_files_are_treated_as_spec_dir_candidates(self) -> None:
        """A migration-only Phase 3 PR may only change fr-coverage.json or test-coverage.json.

        If those files are ignored, specDir becomes empty and the phase is
        incorrectly routed through Phase 3 recovery instead of the completion
        sentinel.  The fix generalises the generated/ match so any file under
        that subdirectory contributes its parent directory as a candidate.
        """
        content = EXTRACT_PHASE_INFO.read_text(encoding="utf-8")
        # The general regex covers all generated/ files, including diagnostic JSON.
        assert r"/^(.*)\/generated\/[^/]+$/" in content
        # The old analysis-report.md-specific branch must be gone.
        assert "endsWith('/generated/analysis-report.md')" not in content


class TestGeneratorNestedDirectoryReuse:
    """generate-spec-from-issue.sh must reuse nested task directories (specs/{epic}/{feature}/{task})."""

    def test_generator_has_nested_numeric_directory_fallback(self) -> None:
        """Without this fallback the generator creates a new top-level directory for an issue
        that already has a nested spec directory, causing Phase 3 to miss hierarchy.yml and
        parent context.
        """
        content = GENERATE_SPEC_FROM_ISSUE.read_text(encoding="utf-8")
        # The nested-directory fallback searches for the issue number at any depth.
        assert 'find "$REPO_ROOT/$SPEC_BASE_PATH" -type d -name "${ISSUE_NUMBER}"' in content
        assert "NESTED_MATCHING_DIRS" in content

    def test_generator_exempts_nested_fallback_from_3digit_collision_guard(self) -> None:
        """Nested task directories (e.g. specs/10/42/123) never contain spec.md or
        requirements.md, so the legacy 3-digit collision guard must not apply to them.
        The exact directory-name match used by the nested fallback is already unambiguous.
        """
        content = GENERATE_SPEC_FROM_ISSUE.read_text(encoding="utf-8")
        # A dedicated flag must be set when the nested fallback is used.
        assert "NESTED_FALLBACK_USED=true" in content
        # The 3-digit guard condition must reference the flag so nested directories bypass it.
        assert 'NESTED_FALLBACK_USED" != "true"' in content
