"""Contract tests for the Phase 3 skill and its IDE bridges."""

from pathlib import Path

import yaml

REPO_ROOT = Path(__file__).resolve().parents[2]
PLAN_AGENT = REPO_ROOT / ".github" / "agents" / "speckit.plan.agent.md"
PLAN_PROMPT = REPO_ROOT / ".github" / "prompts" / "speckit.plan.prompt.md"
PLAN_SKILL = REPO_ROOT / ".agents" / "skills" / "speckit-plan" / "SKILL.md"
CLI_REFERENCE = REPO_ROOT / "docs" / "agdt-cli-reference.md"
PYPROJECT = REPO_ROOT / "pyproject.toml"
CLI_RUNNER = REPO_ROOT / "agentic_devtools" / "cli" / "runner.py"
SPECKIT_INIT = REPO_ROOT / "agentic_devtools" / "cli" / "speckit" / "__init__.py"


def test_plan_and_tasks_authoring_matches_each_hierarchy() -> None:
    skill = PLAN_SKILL.read_text(encoding="utf-8")

    assert 'agdt-speckit-scaffold-tasks --hierarchy-level task --spec-context "$PARENT_SPEC_DIR" --json' in skill
    assert '`agdt-task-wait --id "$TASK_ID"` until the task completes' in skill
    assert 'agdt-task-log --id "$TASK_ID"' in skill
    assert "Confirm the task completed successfully and the logged JSON" in skill
    assert "`HIERARCHY_LEVEL`, `SPEC_CONTEXT`, and `PARENT_PLAN_CONTEXT`" in skill
    assert skill.count("after the scaffold result is verified") == 2
    assert "Task:** inherit the parent plan; do not create a local `plan.md`" in skill
    assert "**Feature:** run `agdt-speckit-scaffold-plan --json`" in skill
    assert "author `plan.md`;" in skill
    assert "**Epic:** run `agdt-speckit-scaffold-plan --json`" in skill
    assert "Do not create `tasks.md`" in skill
    assert "parent directory must contain" in skill


def test_gate_remediation_uses_independent_three_attempt_limits() -> None:
    skill = " ".join(PLAN_SKILL.read_text(encoding="utf-8").split())

    assert (
        "Track remediation attempts independently for FR validation, E.2 test coverage, artifact-path verification, "
        "and Pass G." in skill
    )
    assert "at most three remediation attempts" in skill
    assert "a passing gate consumes no further attempts" in skill
    assert "Rerun the full gate command after each repair" in skill
    assert "Exit `2` is an operational/configuration error" in skill


def test_phase_three_pull_request_metadata_and_bases_are_preserved() -> None:
    skill = PLAN_SKILL.read_text(encoding="utf-8")

    assert "Task-level pull requests target `main`." in skill
    assert "active Phase 2 branch, or the Phase 1 branch when clarification was" in skill
    assert (
        "<!-- speckit:agent-assigned schema_version=1 engine=cloud-agent issue=<num> "
        "phase=3 hierarchy=<level> correlation_id=<uuid> -->"
    ) in skill
    assert "`gate_status: failed`" in skill
    assert "docs(#<num>): add phase 3 planning artifacts" in skill


def test_skill_has_portable_metadata_and_preserves_assignment_inputs() -> None:
    _, frontmatter, body = PLAN_SKILL.read_text(encoding="utf-8").split("---", 2)
    metadata = yaml.safe_load(frontmatter)

    assert metadata["name"] == PLAN_SKILL.parent.name == "speckit-plan"
    assert "Use when" in metadata["description"]
    assert metadata["agdt"]["requires"] == {"code_hosting": "github"}
    for required_input in (
        "issue number",
        "hierarchy level",
        "feature directory",
        "parent spec directory",
        "active Phase 2 or Phase 1 branch",
        "correlation ID",
    ):
        assert required_input in body
    assert "generated/phase3-gates.json" in body
    assert "generated/analysis-report.md" in body
    assert "wait for the background task to complete" in body
    assert "plain fast-forward `git push`" in body


def test_ide_bridges_link_to_the_skill_without_duplicating_the_procedure() -> None:
    for bridge in (PLAN_AGENT, PLAN_PROMPT):
        _, _, body = bridge.read_text(encoding="utf-8").split("---", 2)
        target = "../../.agents/skills/speckit-plan/SKILL.md"

        assert f"]({target})" in body
        assert (bridge.parent / target).resolve() == PLAN_SKILL
        assert len(body.strip().splitlines()) <= 15
        assert "## Procedure" not in body
        assert "agdt-speckit-run-phase3-gates" not in body

    _, frontmatter, _ = PLAN_PROMPT.read_text(encoding="utf-8").split("---", 2)
    assert yaml.safe_load(frontmatter)["agent"] == "speckit.plan"


def test_plan_agent_preserves_ide_handoffs() -> None:
    _, frontmatter, _ = PLAN_AGENT.read_text(encoding="utf-8").split("---", 2)
    metadata = yaml.safe_load(frontmatter)

    assert metadata["name"] == "speckit.plan"
    assert metadata["handoffs"] == [
        {"label": "Create Tasks", "agent": "speckit.tasks", "prompt": "Break the plan into tasks", "send": True},
        {
            "label": "Create Checklist",
            "agent": "speckit.checklist",
            "prompt": "Create a checklist for the following domain...",
        },
    ]


def test_phase_three_gate_runner_is_registered_and_documented() -> None:
    pyproject = PYPROJECT.read_text(encoding="utf-8")
    runner = CLI_RUNNER.read_text(encoding="utf-8")
    speckit_init = SPECKIT_INIT.read_text(encoding="utf-8")
    docs = CLI_REFERENCE.read_text(encoding="utf-8")

    assert 'agdt-speckit-run-phase3-gates = "agentic_devtools.cli.runner:run_as_script"' in pyproject
    assert '"agdt-speckit-run-phase3-gates": (' in runner
    assert '"speckit_run_phase3_gates",' in runner
    assert "run_phase3_gates_command as speckit_run_phase3_gates" in speckit_init
    assert '"speckit_run_phase3_gates"' in speckit_init
    assert "#### Phase 3 gate runner" in docs
    assert "generated/phase3-gates.json" in docs
