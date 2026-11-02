"""Cross-component contracts for SpecKit progression dispatch inputs."""

import json
import subprocess
from pathlib import Path

import pytest
import yaml

REPO_ROOT = Path(__file__).resolve().parents[2]
HELPER = REPO_ROOT / ".github" / "scripts" / "speckit-trigger" / "progression-dispatch.js"
ISSUE_TRIGGER = REPO_ROOT / ".github" / "workflows" / "speckit-issue-trigger.yml"
PHASE_PROGRESSION = REPO_ROOT / ".github" / "workflows" / "speckit-phase-progression.yml"


def _load_workflow(path: Path) -> dict:
    return yaml.load(path.read_text(encoding="utf-8"), Loader=yaml.BaseLoader)


def _load_helper_contract() -> dict:
    result = subprocess.run(  # noqa: S603
        [
            "node",
            "-e",
            "const helper = require(process.argv[1]); "
            "process.stdout.write(JSON.stringify({ choices: helper.DISPATCH_HIERARCHY_LEVELS }));",
            str(HELPER),
        ],
        check=True,
        capture_output=True,
        text=True,
        shell=False,
    )
    return json.loads(result.stdout)


def _assert_choice_contract(helper_choices: list[str], receiver_choices: list[str], default: str) -> None:
    assert set(helper_choices) == set(receiver_choices)
    assert default == "auto"


def test_helper_choices_match_receiver_choices_and_auto_default() -> None:
    helper_contract = _load_helper_contract()
    dispatch_inputs = _load_workflow(PHASE_PROGRESSION)["on"]["workflow_dispatch"]["inputs"]
    receiver_choices = dispatch_inputs["hierarchy_level"]["options"]

    _assert_choice_contract(
        helper_choices=helper_contract["choices"],
        receiver_choices=receiver_choices,
        default=dispatch_inputs["hierarchy_level"]["default"],
    )


def test_choice_contract_rejects_receiver_option_drift() -> None:
    helper_choices = _load_helper_contract()["choices"]
    receiver_choices = _load_workflow(PHASE_PROGRESSION)["on"]["workflow_dispatch"]["inputs"]["hierarchy_level"][
        "options"
    ]

    with pytest.raises(AssertionError):
        _assert_choice_contract(helper_choices, [*receiver_choices, "unknown"], "auto")


def test_both_progression_callers_use_the_shared_payload_builder() -> None:
    initial_steps = _load_workflow(ISSUE_TRIGGER)["jobs"]["dispatch-phase-1"]["steps"]
    initial_step = next(step for step in initial_steps if step.get("name") == "Dispatch Phase Progression")
    self_dispatch_steps = _load_workflow(PHASE_PROGRESSION)["jobs"]["progress-phase"]["steps"]
    self_dispatch_step = next(
        step
        for step in self_dispatch_steps
        if step.get("name") == "Handle Skipped Phase (Already Complete or Level-Skipped)"
    )

    initial_script = initial_step["with"]["script"]
    self_dispatch_script = self_dispatch_step["with"]["script"]
    for script in (initial_script, self_dispatch_script):
        assert "progression-dispatch.js" in script
        assert "buildPhaseProgressionInputs" in script
        assert "dispatchRecordedProgression({ github, context, inputs })" in script
        assert "hierarchy_level: hierarchyLevel" not in script
    assert "resolveInitialProgressionPhase" in initial_script
    assert "specDir: process.env.SPEC_DIR || ''" in initial_script
    assert "hierarchyLevel = process.env.HIERARCHY_LEVEL" in self_dispatch_script
    helper = HELPER.read_text(encoding="utf-8")
    assert "github.rest.actions.createWorkflowDispatch" in helper
    assert helper.index("github.rest.issues.createComment") < helper.index("github.rest.actions.createWorkflowDispatch")


def test_initial_dispatch_checks_out_the_shared_helper_for_both_engines() -> None:
    steps = _load_workflow(ISSUE_TRIGGER)["jobs"]["dispatch-phase-1"]["steps"]
    checkout_step = next(
        step for step in steps if step.get("name") == "Check out repository (Progression Dispatch + Cloud Agent Guard)"
    )
    cloud_guard = next(step for step in steps if step.get("name") == "Cloud Agent In-Flight Guard")

    assert "if" not in checkout_step
    assert cloud_guard["if"] == "steps.engine.outputs.value == 'cloud-agent'"


def test_initial_progression_dispatch_uses_repository_workflow_credential() -> None:
    steps = _load_workflow(ISSUE_TRIGGER)["jobs"]["dispatch-phase-1"]["steps"]
    dispatch_step = next(step for step in steps if step.get("name") == "Dispatch Phase Progression")
    assert dispatch_step["with"]["github-token"] == "${{ secrets.DEFAULT_CLASSIC_REPO_WORKFLOW_PAT }}"
    assert dispatch_step["env"]["HIERARCHY_LEVEL"] == "${{ steps.hierarchy.outputs.hierarchy_level }}"


def test_downgraded_task_continuation_requires_preceding_phase_completion_evidence() -> None:
    steps = _load_workflow(PHASE_PROGRESSION)["jobs"]["progress-phase"]["steps"]
    guard = next(step for step in steps if step.get("name") == "Require Phase 1 for Downgraded Task")
    issue_details = next(step for step in steps if step.get("name") == "Get Issue Details")

    assert guard["id"] == "restart-guard"
    assert "steps.extract.outputs.completed_phase != '1'" in guard["if"]
    assert "steps.extract.outputs.next_phase != '0'" in guard["if"]
    assert "github.event_name != 'pull_request'" in guard["if"]
    assert "github.event_name == 'workflow_dispatch'" in guard["if"]
    assert "steps.extract.outputs.task_downgraded == 'true'" in guard["if"]
    assert (
        "!contains( fromJSON(steps.issue.outputs.labels), "
        "format('speckit:phase-{0}-complete', steps.extract.outputs.completed_phase) )"
    ) in " ".join(guard["if"].split())
    assert issue_details["if"] == "steps.extract.outcome == 'success' && steps.extract.outputs.next_phase != '0'"
    assert "verified as a standalone Feature" in guard["run"]

    failure = next(step for step in steps if step.get("name") == "Post Failure Comment")
    assert failure["env"]["TASK_RESTART_GUARD_FAILED"] == "${{ steps.restart-guard.outcome == 'failure' }}"
    assert failure["env"]["HIERARCHY_REASON"] == "${{ steps.hierarchy.outputs.reason || '' }}"
    assert failure["run"] == "python -S agentic_devtools/cli/speckit/progression_failure.py"
    assert "steps.cloud-inflight.outputs.already != 'true'" in failure["if"]
    assert "steps['task-context'].outputs.handled != 'true'" in failure["if"]
    assert "steps.hierarchy.outputs.reason != 'parent-spec-missing'" in failure["if"]


def test_standalone_task_phase_one_uses_the_verified_hierarchy_for_scaffolding() -> None:
    skill = (REPO_ROOT / ".agents" / "skills" / "speckit-specify" / "SKILL.md").read_text(encoding="utf-8")

    assert "agdt-speckit-resolve-hierarchy" in skill
    assert "--verified-hierarchy-level" in skill
    assert "agdt-detect-parent --issue" not in skill


def test_missing_standalone_prerequisites_restart_phase_three_downgrade() -> None:
    steps = _load_workflow(PHASE_PROGRESSION)["jobs"]["progress-phase"]["steps"]
    guard = next(step for step in steps if step.get("name") == "Require Phase 1 for Downgraded Task")

    assert "steps.extract.outputs.standalone_prerequisites_missing == 'true'" in guard["if"]


def test_task_validation_stops_before_reresolution_when_cloud_assignment_is_in_flight() -> None:
    steps = _load_workflow(PHASE_PROGRESSION)["jobs"]["progress-phase"]["steps"]
    hierarchy = next(step for step in steps if step.get("name") == "Resolve Hierarchy Level")
    task_context = next(step for step in steps if step.get("name") == "Require Task Spec Context")
    failure = next(step for step in steps if step.get("name") == "Post Failure Comment")
    idempotency = next(step for step in steps if step.get("name") == "Check Phase Idempotency")
    resolution_failure = next(step for step in steps if step.get("name") == "Fail on Task Parent Resolution Error")

    assert "steps.cloud-inflight.outputs.already != 'true'" in hierarchy["if"]
    assert "steps.cloud-inflight.outputs.already != 'true'" in task_context["if"]
    assert "steps.cloud-inflight.outputs.already != 'true'" in idempotency["if"]
    assert "steps.cloud-inflight.outputs.already != 'true'" in failure["if"]
    assert "steps.extract.outputs.task_resolution_failed == 'true'" in resolution_failure["if"]
    assert "steps.cloud-inflight.outputs.already != 'true'" in resolution_failure["if"]


def test_phase_three_idempotency_receives_resolved_task_context() -> None:
    steps = _load_workflow(PHASE_PROGRESSION)["jobs"]["progress-phase"]["steps"]
    idempotency = next(step for step in steps if step.get("name") == "Check Phase Idempotency")

    assert idempotency["env"]["SPEC_CONTEXT"] == "${{ steps.hierarchy.outputs.spec_context }}"
    assert '--spec-context "$SPEC_CONTEXT"' in idempotency["run"]


def test_skipped_phase_and_recovery_handoffs_preserve_completion_evidence() -> None:
    steps = _load_workflow(PHASE_PROGRESSION)["jobs"]["progress-phase"]["steps"]
    skipped_phase = next(
        step for step in steps if step.get("name") == "Handle Skipped Phase (Already Complete or Level-Skipped)"
    )
    successful_phase = next(step for step in steps if step.get("name") == "Add Phase Complete Label to Issue")

    assert "labels: [`speckit:phase-${nextPhase}-complete`]" in skipped_phase["with"]["script"]
    assert skipped_phase["with"]["script"].index("issues.addLabels") < skipped_phase["with"]["script"].index(
        "dispatchRecordedProgression"
    )
    assert "labels: [`speckit:phase-${completedPhase}-complete`]" in successful_phase["with"]["script"]
    assert (
        "github.event_name != 'workflow_dispatch' && steps.cloud-inflight.outputs.already != 'true'"
        in successful_phase["if"]
    )
    assert (
        "format('speckit:phase-{0}-complete', steps.extract.outputs.completed_phase)"
        in next(step for step in steps if step.get("name") == "Require Phase 1 for Downgraded Task")["if"]
    )


def test_task_reresolution_preserves_supplied_spec_dir_when_no_directory_is_found() -> None:
    steps = _load_workflow(PHASE_PROGRESSION)["jobs"]["progress-phase"]["steps"]
    hierarchy_step = next(step for step in steps if step.get("name") == "Resolve Hierarchy Level")
    script = hierarchy_step["run"]

    assert 'SPEC_DIR="$INPUT_SPEC_DIR"' in script
    assert 'RESOLVED_SPEC_DIR="$INPUT_SPEC_DIR"' not in script
    assert "RESOLVED_SPEC_DIR" in script
    assert 'if [[ -n "$RESOLVED_SPEC_DIR" ]]; then' in script
    assert 'SPEC_DIR="$RESOLVED_SPEC_DIR"' in script
    assert 'SPEC_CONTEXT="$RESOLVED_SPEC_CONTEXT"' in script


def test_relocated_spec_source_deletions_are_staged_with_generated_artifacts() -> None:
    generator = (REPO_ROOT / ".github" / "scripts" / "speckit-trigger" / "generate-spec-from-issue.sh").read_text(
        encoding="utf-8"
    )
    workflow = PHASE_PROGRESSION.read_text(encoding="utf-8")

    assert "moved_from_spec_dir=" in generator
    assert "steps.generate.outputs.moved_from_spec_dir" in workflow
    assert 'git add -A -- "$MOVED_FROM_SPEC_DIR" "$SPEC_DIR"' in workflow


def test_create_pr_passes_issue_title_through_environment_in_every_branch() -> None:
    steps = _load_workflow(PHASE_PROGRESSION)["jobs"]["progress-phase"]["steps"]
    create_pr = next(step for step in steps if step.get("name") == "Create Pull Request")
    script = create_pr["run"]
    invocations = script.split(".github/scripts/speckit-trigger/create-spec-pr.sh \\")[1:]

    assert create_pr["env"]["ISSUE_TITLE"] == "${{ steps.issue.outputs.title }}"
    assert len(invocations) == 3
    assert all('"$ISSUE_TITLE"' in invocation for invocation in invocations)
    assert all("${{ steps.issue.outputs.title }}" not in invocation for invocation in invocations)


def test_sanitize_branch_name_passes_issue_title_through_environment() -> None:
    steps = _load_workflow(PHASE_PROGRESSION)["jobs"]["progress-phase"]["steps"]
    sanitize = next(step for step in steps if step.get("name") == "Sanitize Branch Name")

    assert sanitize["env"]["ISSUE_TITLE"] == "${{ steps.issue.outputs.title }}"
    assert '.github/scripts/speckit-trigger/sanitize-branch-name.sh "$ISSUE_TITLE"' in sanitize["run"]
    assert "${{ steps.issue.outputs.title }}" not in sanitize["run"]
