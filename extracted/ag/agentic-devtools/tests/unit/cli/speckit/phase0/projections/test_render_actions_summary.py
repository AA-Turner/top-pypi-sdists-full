"""Tests for render_actions_summary in speckit/phase0/projections.py (FR-003)."""

from __future__ import annotations

import pytest

from agentic_devtools.cli.speckit.phase0.observability import Recorder, RunRecord
from agentic_devtools.cli.speckit.phase0.projections import render_actions_summary


def _make_run(**overrides: object) -> RunRecord:
    defaults = dict(
        repository="owner/repo",
        workflow_run_id=1,
        workflow_run_attempt=1,
        run_id="gh:owner/repo:1:1",
        operation_id="gh-event:abc",
        issue_id="owner/repo#1",
        trigger="issues",
        source="provider-event",
        provider="github",
        configuration_decision="enabled",
        configuration_reason="Phase 0 is enabled",
        started_at="2026-01-01T00:00:00Z",
        updated_at="2026-01-01T00:00:00Z",
        workflow_run_url="https://example.invalid/run/1",
    )
    defaults.update(overrides)
    return RunRecord(**defaults)  # type: ignore[arg-type]


class TestRenderActionsSummary:
    """Tests for the render_actions_summary function."""

    def test_starts_with_exact_heading(self) -> None:
        recorder = Recorder(
            _make_run(
                configuration_decision="disabled",
                configuration_reason="Phase 0 is disabled; Phase 1 will proceed as normal",
            )
        )
        recorder.finalize(final_outcome="skipped")
        rendered = render_actions_summary(recorder.to_document(), next_action="none")
        assert rendered.startswith("## Phase 0 Status\n\n- Repository: owner/repo\n")

    def test_property_fields_are_not_evaluated_when_no_discovery_event(self) -> None:
        recorder = Recorder(_make_run())
        recorder.record(stage="validation", status="failed", message="failed", timestamp="2026-01-01T00:00:01Z")
        recorder.finalize(final_outcome="blocked")
        rendered = render_actions_summary(recorder.to_document(), next_action="manual-intervention-required")
        assert "- Captured Properties: not evaluated" in rendered
        assert "- Captured Count: not evaluated" in rendered

    def test_property_fields_render_from_property_discovery_snapshot(self) -> None:
        recorder = Recorder(_make_run())
        recorder.record(
            stage="property_discovery",
            status="succeeded",
            message="ok",
            timestamp="2026-01-01T00:00:01Z",
            captured_properties=[{"name": "b", "templateSection": "s"}, {"name": "a", "templateSection": "s"}],
            missing_properties=["z"],
        )
        recorder.finalize(final_outcome="succeeded")
        rendered = render_actions_summary(recorder.to_document(), next_action="none")
        assert "- Captured Properties: a, b" in rendered
        assert "- Captured Count: 2" in rendered
        assert "- Missing Properties: z" in rendered
        assert "- Missing Count: 1" in rendered

    def test_no_stages_still_renders_stages_heading_without_bullets(self) -> None:
        recorder = Recorder(
            _make_run(
                configuration_decision="disabled",
                configuration_reason="Phase 0 is disabled; Phase 1 will proceed as normal",
            )
        )
        recorder.finalize(final_outcome="skipped")
        rendered = render_actions_summary(recorder.to_document(), next_action="none")
        assert "- Stages:\n\n- Final Outcome:" in rendered

    def test_stage_bullets_use_terminal_event_per_stage(self) -> None:
        recorder = Recorder(_make_run())
        recorder.record(stage="validation", status="in_progress", message="starting", timestamp="2026-01-01T00:00:01Z")
        recorder.record(stage="validation", status="succeeded", message="validated", timestamp="2026-01-01T00:00:02Z")
        recorder.finalize(final_outcome="succeeded")
        rendered = render_actions_summary(recorder.to_document(), next_action="none")
        assert "  - validation: succeeded \u2014 validated" in rendered
        assert "starting" not in rendered

    def test_unavailable_values_render_as_none(self) -> None:
        recorder = Recorder(
            _make_run(
                configuration_decision="disabled",
                configuration_reason="Phase 0 is disabled; Phase 1 will proceed as normal",
            )
        )
        recorder.finalize(final_outcome="skipped")
        rendered = render_actions_summary(recorder.to_document(), next_action=None)
        assert "- Issue Type: none" in rendered
        assert "- Last Known Stage: none" in rendered
        assert "- Next Action: none" in rendered
        assert "- Termination Code: none" in rendered

    def test_rejects_next_action_mismatch(self) -> None:
        recorder = Recorder(_make_run())
        recorder.record(stage="validation", status="failed", message="failed", timestamp="2026-01-01T00:00:01Z")
        recorder.finalize(final_outcome="failed", termination_code="workflow-timeout")
        with pytest.raises(ValueError, match="next_action must equal derived value"):
            render_actions_summary(recorder.to_document(), next_action="none")

    def test_rejects_none_next_action_when_derived_value_is_not_none(self) -> None:
        recorder = Recorder(_make_run())
        recorder.record(stage="validation", status="failed", message="failed", timestamp="2026-01-01T00:00:01Z")
        recorder.finalize(final_outcome="failed", termination_code="workflow-timeout")
        with pytest.raises(ValueError, match="next_action must be"):
            render_actions_summary(recorder.to_document(), next_action=None)

    def test_issue_type_is_sanitized_for_markdown_output(self) -> None:
        recorder = Recorder(
            _make_run(
                issue_type="Epic\n- Forged: yes",
                configuration_decision="disabled",
                configuration_reason="Phase 0 is disabled; Phase 1 will proceed as normal",
            )
        )
        recorder.finalize(final_outcome="skipped")
        rendered = render_actions_summary(recorder.to_document(), next_action="none")
        assert "- Issue Type: Epic\ufffd- Forged: yes" in rendered
        assert "\n- Forged: yes" not in rendered
        assert "\ufffd" in rendered

    def test_selected_template_and_artifact_fields_are_sanitized(self) -> None:
        recorder = Recorder(
            _make_run(
                selected_template="template.md\n- Forged: yes",
                artifact_branch="feature/*unsafe*",
                artifact_path="a" * 2000,
                commit_sha="sha\rvalue",
            )
        )
        recorder.record(stage="validation", status="succeeded", message="ok", timestamp="2026-01-01T00:00:01Z")
        recorder.finalize(final_outcome="succeeded")
        rendered = render_actions_summary(recorder.to_document(), next_action="none")

        assert "- Selected Template: template.md\ufffd- Forged: yes" in rendered
        assert "\n- Forged: yes" not in rendered
        assert "- Artifact Branch: feature/&#42;unsafe&#42;" in rendered
        assert "- Commit: sha\ufffdvalue" in rendered
        assert "- Artifact File: " in rendered
        assert "a" * 2000 not in rendered
        assert "\u2026[T]" in rendered
