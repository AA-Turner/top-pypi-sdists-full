"""Tests for ``build_repair_comment()`` in ``request_artifact_fix``."""

from pathlib import Path

from agentic_devtools.cli.speckit.request_artifact_fix import build_repair_comment


def _build(**overrides: object) -> str:
    kwargs: dict[str, object] = {
        "spec_dir": "specs/1900-task",
        "phase_number": "4",
        "phase_name": "tasks",
        "violations": "tasks.md: missing path pkg/typo.py",
        "spec_context": None,
    }
    kwargs.update(overrides)
    return build_repair_comment(**kwargs)  # type: ignore[arg-type]


class TestBuildRepairComment:
    """Renders the @copilot repair request body."""

    def test_body_starts_with_the_copilot_mention(self) -> None:
        assert _build().startswith("@copilot - the SpecKit artifact verification gate")

    def test_includes_the_violation_detail(self) -> None:
        body = _build()
        assert "tasks.md: missing path pkg/typo.py" in body
        assert "~~~text" in body

    def test_falls_back_when_no_violation_detail_captured(self) -> None:
        assert "(no violation detail captured" in _build(violations="   ")

    def test_includes_the_local_rerun_command(self) -> None:
        body = _build()
        # Phase 4 is an internal phase-3 sub-step; verify command must be unscoped.
        assert "agdt-speckit-verify-artifacts --spec-dir specs/1900-task --repo-root .`" in body
        assert "--phase 4" not in body

    def test_includes_the_report_update_command(self) -> None:
        body = _build()
        assert "--json > specs/1900-task/artifact-verification.json`" in body

    def test_appends_spec_context_argument_when_provided(self) -> None:
        body = _build(spec_context=Path("specs/1859-feature/spec.md"))
        assert "--spec-context specs/1859-feature/spec.md" in body

    def test_mentions_the_phase(self) -> None:
        assert "Phase 4 (tasks) artifacts were generated" in _build()

    def test_feature_level_downstream_note_includes_tasks_and_analysis(self) -> None:
        body = _build(hierarchy_level="feature")
        assert "tasks.md" in body
        assert "coverage diagnostics" in body
        assert "analysis-report.md" in body
        assert "regenerate" in body.lower()

    def test_epic_level_downstream_note_includes_analysis_but_not_tasks(self) -> None:
        body = _build(hierarchy_level="epic")
        assert "analysis-report.md" in body
        assert "regenerate" in body.lower()
        # The downstream note for epic must NOT mention tasks.md; only the violation
        # detail (from the fixture) may mention it.
        what_to_do_section = body.split("### What to do")[1]
        assert "tasks.md" not in what_to_do_section

    def test_task_level_has_no_downstream_note(self) -> None:
        body = _build(hierarchy_level="task")
        assert "regenerate" not in body.lower()
        assert "analysis-report.md" not in body

    def test_default_level_is_feature_for_phase3_internal_steps(self) -> None:
        # Omitting hierarchy_level must behave identically to hierarchy_level="feature"
        body_default = _build()  # phase_number="4"
        body_feature = _build(hierarchy_level="feature")
        assert body_default == body_feature

    def test_includes_downstream_regeneration_note_for_plan_phase(self) -> None:
        body = _build(phase_number="3", phase_name="plan")
        assert "regenerate" in body.lower()
        # Phase 3 (plan) note should mention tasks.md as a downstream artifact.
        assert "tasks.md" in body

    def test_no_downstream_regeneration_note_for_non_phase3_steps(self) -> None:
        body = _build(phase_number="1", phase_name="specify")
        assert "regenerate" not in body.lower()
        assert "--phase 1" in body

    def test_uses_unscoped_verify_command_for_multi_phase_failures(self) -> None:
        body = _build(phase_number="3,4", phase_name="plan,tasks")
        assert "Phases 3,4 (plan,tasks) artifacts were generated" in body
        assert "agdt-speckit-verify-artifacts --spec-dir specs/1900-task --repo-root ." in body
        assert "--phase 3,4" not in body

    def test_omits_phase_argument_when_phase_number_is_blank(self) -> None:
        body = _build(phase_number=" ", phase_name="tasks")
        assert "Phase (tasks) artifacts were generated" in body
        assert "--phase " not in body
