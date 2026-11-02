"""Contract tests for SpecKit dual-engine workflow routing."""

import ast
import json
import os
import re
import subprocess
from pathlib import Path
from typing import Any

import yaml

REPO_ROOT = Path(__file__).resolve().parents[2]
TRIGGER = (REPO_ROOT / ".github/workflows/speckit-issue-trigger.yml").read_text(encoding="utf-8")
PROGRESSION = (REPO_ROOT / ".github/workflows/speckit-phase-progression.yml").read_text(encoding="utf-8")
NORMALIZER = (REPO_ROOT / ".github/workflows/speckit-agent-pr-normalizer.yml").read_text(encoding="utf-8")
CLEANUP = (REPO_ROOT / ".github/workflows/speckit-agent-fallback-cleanup.yml").read_text(encoding="utf-8")
IMPLEMENT = (REPO_ROOT / ".github/workflows/speckit-implement-trigger.yml").read_text(encoding="utf-8")
HIERARCHY_RESOLVER = (REPO_ROOT / "agentic_devtools/cli/speckit/resolve_hierarchy.py").read_text(encoding="utf-8")
EXTRACT_PHASE_INFO = (REPO_ROOT / ".github/scripts/speckit-trigger/extract-phase-info.js").read_text(encoding="utf-8")
NORMALIZE_COPILOT_PR = (REPO_ROOT / ".github/scripts/speckit-trigger/normalize-copilot-pr.js").read_text(
    encoding="utf-8"
)
WORKFLOW_README = (REPO_ROOT / ".github/workflows/README.md").read_text(encoding="utf-8")


def test_dual_engine_defaults_safely_to_legacy() -> None:
    assert "vars.SPECKIT_ENGINE || 'legacy'" in TRIGGER
    assert "unsupported SPECKIT_ENGINE" in TRIGGER
    assert "env.SPECKIT_ENGINE != 'cloud-agent'" in PROGRESSION
    assert "generate-spec-from-issue.sh" in PROGRESSION


def test_migration_only_phase_three_prepares_python_for_pr_creation() -> None:
    workflow = yaml.load(PROGRESSION, Loader=yaml.BaseLoader)
    steps = workflow["jobs"]["progress-phase"]["steps"]
    required_steps = {"Set up Python", "Install uv", "Install Dependencies"}

    for step_name in required_steps:
        step = next(step for step in steps if step.get("name") == step_name)
        condition = step["if"]
        assert (
            "(steps.idempotency.outputs.skipped != 'true' || "
            "(steps.extract.outputs.next_phase == '3' && steps.idempotency.outputs.migration_done == 'true'))"
            in condition
        )


def test_normalizer_requires_copilot_identity_and_explicit_speckit_signal() -> None:
    assert "types: [opened, synchronize, ready_for_review, edited, labeled]" in NORMALIZER
    assert "github.event.pull_request.user.login == 'copilot-swe-agent[bot]' &&" in NORMALIZER
    assert "contains(github.event.pull_request.labels.*.name, 'speckit:spec')" in NORMALIZER
    assert (
        "contains(github.event.pull_request.body || '', 'speckit:agent-assigned schema_version=1 engine=cloud-agent')"
    ) in NORMALIZER
    assert "contains(github.event.pull_request.labels.*.name, 'speckit:phase-1')" in NORMALIZER
    assert "authoritativeMarker.match[0] !== markerMatch[0]" in NORMALIZE_COPILOT_PR
    assert "TRUSTED_NORMALIZER_LOGINS = new Set(['AMARSNIK_swica', 'github-actions[bot]'])" in NORMALIZE_COPILOT_PR
    assert "if (!markerMatch && comments.some(comment => {" in NORMALIZE_COPILOT_PR
    assert "&& isTrustedNormalizerComment(comment);" in NORMALIZE_COPILOT_PR
    assert "await postDiagnostic(" in NORMALIZE_COPILOT_PR
    assert "No trusted source issue comment matched correlation ID" in NORMALIZE_COPILOT_PR
    assert "startsWith(github.event.pull_request.head.ref, 'copilot/')" not in NORMALIZER


def test_progression_requires_explicit_speckit_signal_for_merged_prs() -> None:
    gate = PROGRESSION[PROGRESSION.index("github.event.pull_request.merged == true") :]
    assert "startsWith(github.event.pull_request.head.ref, 'copilot/')" not in gate[: gate.index("permissions:")]
    assert "contains(github.event.pull_request.labels.*.name, 'speckit:spec')" in gate
    assert "speckit:agent-assigned schema_version=1 engine=cloud-agent" in gate
    assert "only quotes the cloud-agent marker prefix; skipping phase progression" in EXTRACT_PHASE_INFO
    assert "core.setFailed('Could not extract phase number from PR labels or cloud-agent marker')" in EXTRACT_PHASE_INFO


def _evaluate_progression_guard(expression: str, event: dict[str, Any]) -> bool:
    pull_request = event["pull_request"]
    assert isinstance(pull_request, dict)
    replacements = {
        "github.event.pull_request.labels.*.name": "pull_request_labels",
        "github.event.pull_request.base.ref": "pull_request_base_ref",
        "github.event.pull_request.merged": "pull_request_merged",
        "github.event.pull_request.body": "pull_request_body",
        "github.event_name": "event_name",
    }
    for source, target in replacements.items():
        expression = expression.replace(source, target)
    expression = expression.replace("&&", " and ").replace("||", " or ")
    expression = re.sub(r"\btrue\b", "True", expression)
    expression = re.sub(r"\bstartsWith\(", "starts_with(", expression)
    values = {
        "event_name": event["event_name"],
        "pull_request_labels": [label["name"] for label in pull_request["labels"]],
        "pull_request_base_ref": pull_request["base"]["ref"],
        "pull_request_merged": pull_request["merged"],
        "pull_request_body": pull_request["body"],
    }

    def evaluate(node: ast.expr) -> Any:
        if isinstance(node, ast.BoolOp):
            if isinstance(node.op, ast.And):
                result = True
                for value in node.values:
                    result = evaluate(value)
                    if not result:
                        return result
                return result
            if isinstance(node.op, ast.Or):
                result = False
                for value in node.values:
                    result = evaluate(value)
                    if result:
                        return result
                return result
        elif isinstance(node, ast.Compare) and len(node.ops) == len(node.comparators) == 1:
            if isinstance(node.ops[0], ast.Eq):
                return evaluate(node.left) == evaluate(node.comparators[0])
        elif isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and len(node.args) == 2:
            target, expected = (evaluate(argument) for argument in node.args)
            if node.func.id == "contains":
                return expected in target if isinstance(target, list) else expected.lower() in target.lower()
            if node.func.id == "starts_with":
                return target.startswith(expected)
        elif isinstance(node, ast.Name) and node.id in values:
            return values[node.id]
        elif isinstance(node, ast.Constant):
            return node.value
        raise AssertionError(f"Unsupported workflow expression node: {ast.dump(node)}")

    return bool(evaluate(ast.parse(expression, mode="eval").body))


def _extract_progression_outputs(pr: dict[str, Any]) -> dict[str, Any]:
    script = """
const { resolveEventContext } = require(
  `${process.env.REPO_ROOT}/.github/scripts/speckit-trigger/extract-phase-info.js`
);
const outputs = {};
let failure = null;
const pr = JSON.parse(process.env.MERGED_PR);
const github = {
  rest: {
    pulls: { get: async () => ({ data: pr }) },
    issues: { get: async () => ({ data: { labels: [{ name: 'feature' }] } }) },
  },
};
const context = {
  eventName: 'pull_request',
  repo: { owner: 'swai-factory', repo: 'agentic-devtools' },
  payload: { pull_request: pr },
};
const core = {
  setOutput: (name, value) => { outputs[name] = value; },
  setFailed: (message) => { failure = message; },
  info: () => {},
  warning: () => {},
};
resolveEventContext({ github, context, core }).then(() => {
  process.stdout.write(JSON.stringify({ outputs, failure }));
}).catch((error) => {
  process.stderr.write(error.stack || String(error));
  process.exitCode = 1;
});
"""
    env = {
        **os.environ,
        "REPO_ROOT": str(REPO_ROOT),
        "MERGED_PR": json.dumps(pr),
    }
    result = subprocess.run(
        ["node", "-e", script],
        check=False,
        capture_output=True,
        text=True,
        env=env,
        shell=False,
    )
    assert result.returncode == 0, result.stderr
    return json.loads(result.stdout)


def test_generated_phase_one_pr_passes_actual_merge_guard_and_hands_off_phase_two() -> None:
    workflow = yaml.load(PROGRESSION, Loader=yaml.BaseLoader)
    gate = workflow["jobs"]["resolve-event"]["if"]
    merged_pr = {
        "number": 123,
        "labels": [{"name": "speckit:phase-1"}, {"name": "speckit:level-feature"}],
        "body": "Closes #42",
        "merged": True,
        "head": {"ref": "speckit/42/phase-1-specify"},
        "base": {"ref": "main"},
        "html_url": "https://github.com/swai-factory/agentic-devtools/pull/123",
    }
    event = {"event_name": "pull_request", "pull_request": merged_pr}

    assert _evaluate_progression_guard(gate, event)
    outputs = _extract_progression_outputs(merged_pr)
    assert outputs["failure"] is None
    assert outputs["outputs"]["completed_phase"] == "1"
    assert outputs["outputs"]["next_phase"] == "2"
    assert outputs["outputs"]["next_phase_name"] == "clarify"
    assert outputs["outputs"]["issue_number"] == "42"

    no_signal_event = {
        "event_name": "pull_request",
        "pull_request": {**merged_pr, "labels": [], "body": ""},
    }
    assert not _evaluate_progression_guard(gate, no_signal_event)


def test_progression_readme_describes_spec_or_validated_cloud_agent_trigger() -> None:
    assert "Pull request closed (merged) events that already have an explicit" in WORKFLOW_README
    assert "assignment marker long enough for `extract-phase-info.js` to" in WORKFLOW_README
    assert "- `speckit:phase-N` labels from legacy and normalized PRs" in WORKFLOW_README
    assert "- `speckit:spec` for normalized Cloud Agent PRs" in WORKFLOW_README
    assert "- A PR body containing `speckit:agent-assigned schema_version=1" in WORKFLOW_README
    assert "before using as a fallback while label reconciliation is still" in WORKFLOW_README


def test_concurrency_is_serialized_at_required_scopes() -> None:
    assert "group: speckit-trigger-${{ github.event.issue.number || inputs.issue_number || github.run_id }}" in TRIGGER
    assert (
        "group: speckit-implement-${{ github.event.issue.number || inputs.issue_number || github.run_id }}" in IMPLEMENT
    )
    assert "group: speckit-normalizer-${{ github.event.pull_request.number || github.run_id }}" in NORMALIZER
    assert "concurrency:" not in CLEANUP
    assert "concurrency:" not in PROGRESSION[: PROGRESSION.index("jobs:")]
    assert "resolve-event:" in PROGRESSION
    phase_job = PROGRESSION[PROGRESSION.index("  progress-phase:") :]
    assert "needs: resolve-event" in phase_job
    assert "group: speckit-progression-${{ needs.resolve-event.outputs.issue_number || github.run_id }}" in phase_job
    assert "expectedIssueNumber: process.env.RESOLVED_ISSUE_NUMBER" in phase_job
    assert "cancel-in-progress: false" in TRIGGER
    assert "cancel-in-progress: false" in PROGRESSION


def test_progression_resolves_identity_with_the_shared_extractor_before_locking() -> None:
    resolver = PROGRESSION[PROGRESSION.index("  resolve-event:") : PROGRESSION.index("  progress-phase:")]
    assert "issue_number: ${{ steps.extract.outputs.issue_number }}" in resolver
    assert "extract-phase-info.js" in resolver
    assert "resolveEventContext" in resolver
    assert "workflowDispatchIssueNumber: process.env.ISSUE_NUMBER" in resolver
    assert "workflowDispatchPhase: process.env.PHASE" in resolver
    assert "issues: read" in resolver
    assert "Reconcile Required SpecKit Labels" not in resolver
    assert "Invalid SpecKit dispatch issue number or phase" in EXTRACT_PHASE_INFO
    assert "Resolved issue identity changed before acquiring the issue lock" in EXTRACT_PHASE_INFO


def test_scheduled_cleanup_invokes_stranded_progression_recovery() -> None:
    poll = CLEANUP[CLEANUP.index("  poll-agent-tasks:") :]
    assert "*/15 * * * *" in CLEANUP
    assert "github.event_name == 'schedule' || github.event_name == 'workflow_dispatch'" in poll
    assert "actions: write" in poll
    assert "python -m pip install ." in poll
    assert "agdt-speckit-recover-stranded-progressions" in poll
    assert "GH_TOKEN: ${{ secrets.DEFAULT_CLASSIC_REPO_WORKFLOW_PAT }}" in poll
    workflow = yaml.safe_load(CLEANUP)
    poll_steps = workflow["jobs"]["poll-agent-tasks"]["steps"]
    recovery_steps = workflow["jobs"]["recover-stranded-progressions"]["steps"]
    assert recovery_steps[-1]["run"] == "agdt-speckit-recover-stranded-progressions"
    assert poll_steps[0]["with"]["script"].rstrip().endswith("}\n  }\n}")


def test_resolved_issue_groups_are_independent_but_same_issue_is_serialized() -> None:
    workflow = yaml.safe_load(PROGRESSION)
    assert "concurrency" not in workflow
    job = workflow["jobs"]["progress-phase"]
    assert job["needs"] == "resolve-event"
    group = job["concurrency"]["group"]
    assert group == "speckit-progression-${{ needs.resolve-event.outputs.issue_number || github.run_id }}"
    assert job["concurrency"]["cancel-in-progress"] is False
    expression = "${{ needs.resolve-event.outputs.issue_number || github.run_id }}"
    first = group.replace(expression, "4250")
    other = group.replace(expression, "4251")
    repeated = group.replace(expression, "4250")
    assert first != other
    assert first == repeated
    assert group.replace(expression, "run-1") != group.replace(expression, "run-2")


def test_skipped_phase_redispatch_retains_processing_for_recovery() -> None:
    workflow = yaml.safe_load(PROGRESSION)
    cleanup = next(
        step
        for step in workflow["jobs"]["progress-phase"]["steps"]
        if step["name"] == "Remove Processing Label (Success)"
    )
    assert "steps.idempotency.outputs.skipped != 'true'" in cleanup["if"]
    assert "steps.phase_applicable.outputs.phase_skipped != 'true'" in cleanup["if"]


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
    assert "dispatchRecordedProgression({ github, context, inputs })" in PROGRESSION
    assert "dispatchRecordedProgression({ github, context, inputs })" in TRIGGER
    assert "format('issue #{0}', inputs.issue_number)" in PROGRESSION


def test_task_trigger_routes_to_phase_three_only_with_parent_context() -> None:
    assert "resolveInitialProgressionPhase" in TRIGGER
    assert "process.env.ENGINE, hierarchyLevel, process.env.SPEC_CONTEXT" in TRIGGER
    assert "resolveInitialProgressionPhase" in TRIGGER
    assert "buildPhaseProgressionInputs" in TRIGGER
    assert "specContext: process.env.SPEC_CONTEXT || ''" in TRIGGER
    assert "agdt-speckit-cloud-agent-guard" in TRIGGER
    assert "--phase 0" in TRIGGER
    assert "steps.cloud-inflight.outputs.already != 'true'" in PROGRESSION


def test_issue_trigger_uses_tested_resolver_instead_of_inline_hierarchy_javascript() -> None:
    steps = yaml.safe_load(TRIGGER)["jobs"]["dispatch-phase-1"]["steps"]
    resolver_step = next(step for step in steps if step["name"] == "Resolve Parent and Hierarchy")
    assert "agdt-speckit-resolve-hierarchy" in resolver_step["run"]
    assert "const authoritativeLevel" not in TRIGGER
    assert "search.code" not in TRIGGER
    assert "def find_parent_spec(" in HIERARCHY_RESOLVER


def test_issue_trigger_sets_up_python_before_any_legacy_package_install() -> None:
    steps = yaml.safe_load(TRIGGER)["jobs"]["dispatch-phase-1"]["steps"]
    setup = next(step for step in steps if step["name"] == "Set up Python")
    install_indexes = [index for index, step in enumerate(steps) if "python -m pip install ." in step.get("run", "")]
    assert setup["with"]["python-version"] == "3.14"
    assert install_indexes
    assert steps.index(setup) < min(install_indexes)


def test_progression_sets_up_python_before_hierarchy_resolution_for_all_engines() -> None:
    workflow = yaml.load(PROGRESSION, Loader=yaml.BaseLoader)
    steps = workflow["jobs"]["progress-phase"]["steps"]
    setup = next(step for step in steps if step["name"] == "Set up Python (Shared)")
    hierarchy = next(step for step in steps if step["name"] == "Resolve Hierarchy Level")
    assert setup["with"]["python-version"] == "3.14"
    assert setup["if"] == "steps.extract.outcome == 'success'"
    assert "SPECKIT_ENGINE" not in setup["if"]
    assert "next_phase" not in setup["if"]
    assert steps.index(setup) < steps.index(hierarchy)


def test_spec_context_flows_through_dispatch_and_task_fail_fast_precedes_phase_applicability() -> None:
    trigger_workflow = yaml.safe_load(TRIGGER)
    trigger_steps = trigger_workflow["jobs"]["dispatch-phase-1"]["steps"]
    dispatch = next(step for step in trigger_steps if step["name"] == "Dispatch Phase Progression")
    assert dispatch["env"]["SPEC_CONTEXT"] == "${{ steps.hierarchy.outputs.spec_context }}"
    assert "specContext: process.env.SPEC_CONTEXT || ''" in dispatch["with"]["script"]

    workflow = yaml.load(PROGRESSION, Loader=yaml.BaseLoader)
    dispatch_inputs = workflow["on"]["workflow_dispatch"]["inputs"]
    assert dispatch_inputs["spec_context"]["type"] == "string"
    assert "parent spec.md" in dispatch_inputs["spec_context"]["description"]
    steps = workflow["jobs"]["progress-phase"]["steps"]
    names = [step["name"] for step in steps]
    assert names.index("Require Task Spec Context") < names.index("Check Phase Applicability")
    skipped = next(step for step in steps if step["name"] == "Handle Skipped Phase (Already Complete or Level-Skipped)")
    assert skipped["env"]["SPEC_DIR"] == "${{ steps.hierarchy.outputs.spec_dir }}"
    assert skipped["env"]["SPEC_CONTEXT"] == "${{ steps.hierarchy.outputs.spec_context }}"
    assert "specContext: process.env.SPEC_CONTEXT || ''" in skipped["with"]["script"]
    assert 'ASSIGN_ARGS+=(--spec-context "$SPEC_CONTEXT")' in PROGRESSION
    gate = next(step for step in steps if step["name"] == "Require Task Spec Context")
    assert "requireTaskContext" in gate["with"]["script"]
    assert gate["env"]["SPECKIT_COMMENT_ON_ISSUE"] == "${{ vars.SPECKIT_COMMENT_ON_ISSUE || '' }}"
    hierarchy = next(step for step in steps if step["name"] == "Resolve Hierarchy Level")
    assert hierarchy["env"]["SPECKIT_TRIGGER_LABEL"] == "${{ vars.SPECKIT_TRIGGER_LABEL || 'speckit' }}"
    assert hierarchy["env"]["SPECKIT_COMMENT_ON_ISSUE"] == gate["env"]["SPECKIT_COMMENT_ON_ISSUE"]
    assert hierarchy["env"]["INPUT_SPEC_CONTEXT"] == "${{ inputs.spec_context || '' }}"
    assert 'if [[ "$LEVEL" == "task" ]]; then' in hierarchy["run"]
    assert 'if [[ "$LEVEL" == "task" && -z "$SPEC_CONTEXT" ]]' not in hierarchy["run"]
    assert "${{" not in hierarchy["run"]
    assert hierarchy["run"].count("tr -d '\\r\\n'") == 4
    downgrade_guard = next(step for step in steps if step["name"] == "Require Phase 1 for Downgraded Task")
    assert "steps.extract.outputs.next_phase != '1'" in downgrade_guard["if"]
    assert "task-without-parent" in downgrade_guard["if"]
    assert "task-cross-repo-parent" in downgrade_guard["if"]
    assert "exit 1" in downgrade_guard["run"]
    assert names.index("Require Phase 1 for Downgraded Task") < names.index("Require Task Spec Context")
    failure_handler = next(step for step in steps if step["name"] == "Post Failure Comment")
    assert failure_handler["env"]["HIERARCHY_REASON"] == "${{ steps.hierarchy.outputs.reason || '' }}"
    assert failure_handler["env"]["TASK_RESTART_GUARD_FAILED"] == "${{ steps.restart-guard.outcome == 'failure' }}"
    assert failure_handler["run"] == "python -S agentic_devtools/cli/speckit/progression_failure.py"
    assert "speckit:failed" in PROGRESSION


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


def test_verified_task_resolution_signals_reach_cascade_and_generation() -> None:
    assert "core.setOutput('task_downgraded', taskDowngraded ? 'true' : 'false')" in EXTRACT_PHASE_INFO
    assert "core.setOutput('task_resolution_failed', taskResolutionFailed ? 'true' : 'false')" in EXTRACT_PHASE_INFO
    assert "steps.extract.outputs.task_resolution_failed == 'true'" in PROGRESSION
    assert 'CASCADE_ARGS+=(--level "$TERMINAL_LEVEL" --task-downgraded)' in PROGRESSION
    assert "CASCADE_ARGS+=(--task-downgraded)" in PROGRESSION
    assert 'SPEC_DIR="$RESOLVED_SPEC_DIR"' in PROGRESSION
    steps = yaml.safe_load(PROGRESSION)["jobs"]["progress-phase"]["steps"]
    generate_step = next(step for step in steps if step.get("id") == "generate")
    assert "RESOLVED_SPEC_DIR" not in generate_step.get("env", {})
    assert '"$HIERARCHY_LEVEL" "${SPEC_CONTEXT:-}"' in (
        REPO_ROOT / ".github/scripts/speckit-trigger/generate-spec-from-issue.sh"
    ).read_text(encoding="utf-8")


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
    assert "- name: Check out repository (Progression Dispatch + Cloud Agent Guard)" in TRIGGER
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
