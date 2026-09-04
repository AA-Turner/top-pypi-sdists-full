"""Contract tests for SpecKit dual-engine workflow routing."""

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
TRIGGER = (REPO_ROOT / ".github/workflows/speckit-issue-trigger.yml").read_text(encoding="utf-8")
PROGRESSION = (REPO_ROOT / ".github/workflows/speckit-phase-progression.yml").read_text(encoding="utf-8")
CLEANUP = (REPO_ROOT / ".github/workflows/speckit-agent-fallback-cleanup.yml").read_text(encoding="utf-8")
EXTRACT_PHASE_INFO = (REPO_ROOT / ".github/scripts/speckit-trigger/extract-phase-info.js").read_text(encoding="utf-8")


def test_dual_engine_defaults_safely_to_legacy() -> None:
    assert "vars.SPECKIT_ENGINE || 'legacy'" in TRIGGER
    assert "unsupported SPECKIT_ENGINE" in TRIGGER
    assert "env.SPECKIT_ENGINE != 'cloud-agent'" in PROGRESSION
    assert "generate-spec-from-issue.sh" in PROGRESSION


def test_concurrency_is_serialized_at_required_scopes() -> None:
    assert "group: speckit-trigger-${{ github.event.issue.number || inputs.issue_number }}" in TRIGGER
    assert "group: speckit-progression" in PROGRESSION
    assert "cancel-in-progress: false" in TRIGGER
    assert "cancel-in-progress: false" in PROGRESSION
    assert "queue: max" not in PROGRESSION


def test_phase_dispatch_matrix_and_marker_contract_are_wired() -> None:
    assert "agdt-assign-speckit-agent" in PROGRESSION, "agdt-assign-speckit-agent invocation not found"
    dispatch_start = PROGRESSION.index("ASSIGN_ARGS=(")
    next_step_offset = PROGRESSION.find("- name:", dispatch_start)
    dispatch_block = (
        PROGRESSION[dispatch_start:next_step_offset] if next_step_offset != -1 else PROGRESSION[dispatch_start:]
    )
    assert "--custom-agent" not in dispatch_block
    assert '--base-branch "$BASE_BRANCH"' in dispatch_block
    assert 'ASSIGN_ARGS+=(--spec-dir "$SPEC_DIR")' in dispatch_block
    assert 'BASE_BRANCH="main"' in PROGRESSION
    assert "speckit:agent-assigned schema_version=1 engine=cloud-agent" in PROGRESSION
    assert "The assigned agent is instructed to copy it into the PR body unchanged." in PROGRESSION


def test_task_trigger_routes_directly_to_phase_three() -> None:
    assert 'if [[ "$ENGINE" == "cloud-agent" && "$HIERARCHY_LEVEL" == "task" ]]; then PHASE=3;' in TRIGGER
    assert "core.setOutput('spec_dir', resolvedSpecDir);" in TRIGGER
    assert '-f "inputs[spec_dir]=$SPEC_DIR"' in TRIGGER
    assert "agdt-speckit-cloud-agent-guard" in TRIGGER
    assert "--phase 0" in TRIGGER
    assert "steps.cloud-inflight.outputs.already != 'true'" in PROGRESSION


def test_hierarchy_resolver_is_recursive_and_matches_nested_tasks() -> None:
    assert "recursive: '1'" in TRIGGER
    assert "dirName === String(issueNumber) || dirName.startsWith(`${issueNumber}-`)" in TRIGGER
    assert "hierarchy.yml files found for issue #" in TRIGGER


def test_cleanup_requires_copilot_marker_and_has_two_hour_timeout() -> None:
    assert "types: [opened, edited]" in CLEANUP
    assert "types: [opened, edited, closed]" not in CLEANUP
    assert "copilot-swe-agent[bot]" in CLEANUP
    assert "const prMarkerMatch = (context.payload.pull_request?.body || '').match(markerRegex);" in CLEANUP
    assert "const expectedBase = (phase === 2)" in CLEANUP
    assert "const trustedAuthorLogins = new Set(['github-actions[bot]']);" in CLEANUP
    assert "trustedAuthorLogins.has(comment?.user?.login || '')" in CLEANUP
    assert "prMatch[0] === markerMatch[0]" in CLEANUP
    assert "search.issuesAndPullRequests" in CLEANUP
    assert "speckit:agent-assigned-phase-${phase}" in CLEANUP
    assert "speckit:agent-timeout" in CLEANUP
    assert "twoHours = 2 * 60 * 60 * 1000" in CLEANUP
    assert "ageMs <= twoHours" in CLEANUP
    assert "speckit:failed" in CLEANUP


def test_cloud_agent_login_set_is_shared_across_guard_consumers() -> None:
    assert "['copilot-swe-agent', 'copilot-swe-agent[bot]']" in EXTRACT_PHASE_INFO
    assert "['copilot-swe-agent', 'copilot-swe-agent[bot]']" in CLEANUP


def test_cloud_dispatch_failure_notice_is_non_blocking() -> None:
    assert "could not post cloud dispatch failure notice" in PROGRESSION
    assert "core.setOutput('handled', 'true');" in PROGRESSION


def test_label_lookup_failure_preserves_tracking_labels() -> None:
    assert "Treating as preserve-on-failure to avoid removing speckit:processing" in PROGRESSION
    assert "Cloud in-flight lookup failed; preserving tracking state" in PROGRESSION
    assert "steps.extract.outputs.next_phase != '4'" in PROGRESSION
    assert "Cloud guard lookup failed; preserving tracking state" in TRIGGER
    assert 'already="true"' in TRIGGER


def test_cloud_guard_is_shared_cli_without_embedded_matching_logic() -> None:
    for workflow in (TRIGGER, PROGRESSION):
        assert "agdt-speckit-cloud-agent-guard" in workflow
        guard_start = workflow.index("- name: Cloud Agent In-Flight Guard")
        next_step = workflow.find("\n      - name:", guard_start + 1)
        guard = workflow[guard_start : next_step if next_step != -1 else None]
        if workflow is PROGRESSION:
            assert "steps.extract.outputs.next_phase != '4'" in guard
        assert "github.paginate(github.rest.issues.listLabelsOnIssue" not in guard
        assert "markerRegex" not in guard
        assert "copilot-swe-agent[bot]" not in guard


def test_cloud_guard_tooling_and_terminal_gating_contract() -> None:
    assert "- name: Check out repository (Cloud Agent Guard)" in TRIGGER
    assert "uses: actions/checkout@v5" in TRIGGER
    assert "python -m pip install ." in TRIGGER
    assert "uvx --from" not in TRIGGER
    assert "if: steps.engine.outputs.value == 'cloud-agent'" in TRIGGER
    assert (
        "if: steps.extract.outcome == 'success' && env.SPECKIT_ENGINE == 'cloud-agent' && "
        "steps.extract.outputs.next_phase != '4'"
    ) in PROGRESSION
    assert (
        "HIERARCHY_LEVEL: ${{ (steps.extract.outputs.terminal_hierarchy_level == 'epic' && 'epic') || "
        "(github.event_name == 'workflow_dispatch' && inputs.hierarchy_level != 'auto' && inputs.hierarchy_level) "
        "|| steps.extract.outputs.terminal_hierarchy_level || 'unknown' }}"
    ) in PROGRESSION


def test_cleanup_poll_includes_phase_only_tracking_labels() -> None:
    assert "labels: `speckit:agent-assigned-phase-${phase}`" in CLEANUP
    assert "const issuesByNumber = new Map();" in CLEANUP
