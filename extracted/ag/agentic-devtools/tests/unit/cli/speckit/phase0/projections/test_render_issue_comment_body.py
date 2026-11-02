"""Tests for render_issue_comment_body in speckit/phase0/projections.py (FR-004)."""

from __future__ import annotations

import pytest

from agentic_devtools.cli.speckit.phase0.observability import Recorder, RunRecord
from agentic_devtools.cli.speckit.phase0.projections import render_issue_comment_body


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


class TestRenderIssueCommentBody:
    """Tests for the render_issue_comment_body function."""

    def test_starts_with_marker_then_heading(self) -> None:
        recorder = Recorder(_make_run())
        recorder.record(stage="validation", status="succeeded", message="ok", timestamp="2026-01-01T00:00:01Z")
        recorder.finalize(final_outcome="succeeded")
        rendered = render_issue_comment_body(
            recorder.to_document(), chain_operation_id="gh-event:abc", next_action="none"
        )
        lines = rendered.splitlines()
        assert lines[0].startswith("<!-- agdt:phase0-status")
        assert lines[1] == "## Phase 0 Status"

    def test_excludes_issue_comment_stage_from_stage_list(self) -> None:
        recorder = Recorder(_make_run())
        recorder.record(stage="validation", status="succeeded", message="ok", timestamp="2026-01-01T00:00:01Z")
        recorder.record(stage="issue_comment", status="succeeded", message="posted", timestamp="2026-01-01T00:00:02Z")
        recorder.finalize(final_outcome="succeeded")

        # The pre-publication snapshot (FR-004) captures lastStage before the
        # issue_comment stage was attempted, so it is passed explicitly here.
        rendered = render_issue_comment_body(
            recorder.to_document(),
            chain_operation_id="gh-event:abc",
            next_action="none",
            pre_publication_last_stage="validation",
            pre_publication_updated_at="2026-01-01T00:00:01Z",
        )
        assert "issue_comment" not in rendered
        assert "  - validation: succeeded \u2014 ok" in rendered

    def test_property_guidance_lists_missing_properties(self) -> None:
        recorder = Recorder(_make_run())
        recorder.record(
            stage="property_discovery",
            status="succeeded",
            message="ok",
            timestamp="2026-01-01T00:00:01Z",
            missing_properties=["b", "a"],
        )
        recorder.finalize(final_outcome="succeeded")
        rendered = render_issue_comment_body(
            recorder.to_document(), chain_operation_id="gh-event:abc", next_action="none"
        )
        assert "- Property Guidance: Provide values for: a, b" in rendered

    def test_property_guidance_none_when_no_missing_properties(self) -> None:
        recorder = Recorder(_make_run())
        recorder.record(stage="property_discovery", status="succeeded", message="ok", timestamp="2026-01-01T00:00:01Z")
        recorder.finalize(final_outcome="succeeded")
        rendered = render_issue_comment_body(
            recorder.to_document(), chain_operation_id="gh-event:abc", next_action="none"
        )
        assert "- Property Guidance: none" in rendered

    def test_pre_publication_snapshot_overrides_last_stage_and_updated(self) -> None:
        recorder = Recorder(_make_run())
        recorder.record(stage="validation", status="succeeded", message="ok", timestamp="2026-01-01T00:00:01Z")
        recorder.finalize(final_outcome="succeeded", updated_at="2026-01-01T00:00:02Z")
        rendered = render_issue_comment_body(
            recorder.to_document(),
            chain_operation_id="gh-event:abc",
            next_action="none",
            pre_publication_last_stage="validation",
            pre_publication_updated_at="2026-01-01T00:00:01Z",
        )
        assert "- Updated: 2026-01-01T00:00:01Z" in rendered
        assert "- Last Known Stage: validation" in rendered

    def test_supersession_metadata_defaults_to_none(self) -> None:
        recorder = Recorder(_make_run())
        recorder.record(stage="validation", status="succeeded", message="ok", timestamp="2026-01-01T00:00:01Z")
        recorder.finalize(final_outcome="succeeded")
        rendered = render_issue_comment_body(
            recorder.to_document(), chain_operation_id="gh-event:abc", next_action="none"
        )
        assert "- Supersedes Identity: none" in rendered
        assert "- Superseded By Identity: none" in rendered

    def test_supersession_metadata_rendered_when_provided(self) -> None:
        recorder = Recorder(_make_run())
        recorder.record(stage="validation", status="succeeded", message="ok", timestamp="2026-01-01T00:00:01Z")
        recorder.finalize(final_outcome="succeeded")
        rendered = render_issue_comment_body(
            recorder.to_document(),
            chain_operation_id="gh-event:abc",
            next_action="none",
            supersedes_identity="old-bot",
            superseded_by_identity="new-bot",
        )
        assert "- Supersedes Identity: old-bot" in rendered
        assert "- Superseded By Identity: new-bot" in rendered

    def test_explicit_none_pre_publication_last_stage_renders_as_none(self) -> None:
        # An explicit None means lastStage was legitimately null at snapshot time
        # (pre-stage cancellation). It must NOT fall back to run["lastStage"].
        recorder = Recorder(_make_run())
        recorder.record(stage="validation", status="succeeded", message="ok", timestamp="2026-01-01T00:00:01Z")
        recorder.finalize(final_outcome="failed", updated_at="2026-01-01T00:00:02Z")
        rendered = render_issue_comment_body(
            recorder.to_document(),
            chain_operation_id="gh-event:abc",
            next_action="retry-safe:from-start",
            pre_publication_last_stage=None,
        )
        # Should show "none" (the explicit snapshot), not "validation" (run["lastStage"])
        assert "- Last Known Stage: none" in rendered

    def test_supersession_identity_control_characters_sanitized(self) -> None:
        # FR-012: control characters are replaced with U+FFFD, preventing markdown-
        # structure injection (a \n followed by "- forged bullet" cannot create a new
        # bullet line because the \n is replaced before rendering).
        recorder = Recorder(_make_run())
        recorder.record(stage="validation", status="succeeded", message="ok", timestamp="2026-01-01T00:00:01Z")
        recorder.finalize(final_outcome="succeeded")
        rendered = render_issue_comment_body(
            recorder.to_document(),
            chain_operation_id="gh-event:abc",
            next_action="none",
            supersedes_identity="old-bot\nforged-line",
            superseded_by_identity="new-bot\rforged",
        )
        # The raw control characters must not survive into the output.
        assert "old-bot\nforged-line" not in rendered
        assert "new-bot\rforged" not in rendered
        # The replacement character signals the sanitization happened.
        assert "\ufffd" in rendered

    def test_rejects_supersedes_identity_without_superseded_by_identity(self) -> None:
        """Providing only supersedes_identity without superseded_by_identity must raise (FR-006)."""
        recorder = Recorder(_make_run())
        recorder.record(stage="validation", status="succeeded", message="ok", timestamp="2026-01-01T00:00:01Z")
        recorder.finalize(final_outcome="succeeded")
        with pytest.raises(ValueError, match="both be provided or both be None"):
            render_issue_comment_body(
                recorder.to_document(),
                chain_operation_id="gh-event:abc",
                next_action="none",
                supersedes_identity="old-bot",
                superseded_by_identity=None,
            )

    def test_rejects_superseded_by_identity_without_supersedes_identity(self) -> None:
        """Providing only superseded_by_identity without supersedes_identity must raise (FR-006)."""
        recorder = Recorder(_make_run())
        recorder.record(stage="validation", status="succeeded", message="ok", timestamp="2026-01-01T00:00:01Z")
        recorder.finalize(final_outcome="succeeded")
        with pytest.raises(ValueError, match="both be provided or both be None"):
            render_issue_comment_body(
                recorder.to_document(),
                chain_operation_id="gh-event:abc",
                next_action="none",
                supersedes_identity=None,
                superseded_by_identity="new-bot",
            )

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
        rendered = render_issue_comment_body(
            recorder.to_document(),
            chain_operation_id="gh-event:abc",
            next_action="none",
        )

        assert "- Selected Template: template.md\ufffd- Forged: yes" in rendered
        assert "\n- Forged: yes" not in rendered
        assert "- Artifact Branch: feature/&#42;unsafe&#42;" in rendered
        assert "- Commit: sha\ufffdvalue" in rendered
        assert "- Artifact File: " in rendered
        assert "a" * 2000 not in rendered
        assert "\u2026[T]" in rendered

    def test_rejects_chain_operation_id_mismatch_for_non_retry_runs(self) -> None:
        recorder = Recorder(_make_run(operation_id="gh-event:abc"))
        recorder.record(stage="validation", status="succeeded", message="ok", timestamp="2026-01-01T00:00:01Z")
        recorder.finalize(final_outcome="succeeded")
        with pytest.raises(ValueError, match="chain_operation_id"):
            render_issue_comment_body(
                recorder.to_document(),
                chain_operation_id="gh-event:different",
                next_action="none",
            )

    def test_allows_matching_chain_operation_id_for_retry_runs(self) -> None:
        recorder = Recorder(
            _make_run(
                operation_id="gh-retry:gh-event:chain:20260101T000000Z:1:1",
                retry_of_run_id="gh:owner/repo:99:1",
                retry_mode="restarted",
                source="retry",
            )
        )
        recorder.record(stage="validation", status="succeeded", message="ok", timestamp="2026-01-01T00:00:01Z")
        recorder.finalize(final_outcome="succeeded")
        rendered = render_issue_comment_body(
            recorder.to_document(),
            chain_operation_id="gh-event:chain",
            next_action="none",
        )
        assert rendered.startswith("<!-- agdt:phase0-status")

    def test_rejects_chain_operation_id_mismatch_for_retry_runs(self) -> None:
        recorder = Recorder(
            _make_run(
                operation_id="gh-retry:gh-event:chain:20260101T000000Z:1:1",
                retry_of_run_id="gh:owner/repo:99:1",
                retry_mode="restarted",
                source="retry",
            )
        )
        recorder.record(stage="validation", status="succeeded", message="ok", timestamp="2026-01-01T00:00:01Z")
        recorder.finalize(final_outcome="succeeded")
        with pytest.raises(ValueError, match="chain_operation_id"):
            render_issue_comment_body(
                recorder.to_document(),
                chain_operation_id="gh-event:other",
                next_action="none",
            )

    def test_rejects_prefix_only_match_when_delivery_id_contains_colon(self) -> None:
        # gh-event:abc:def is a valid delivery-ID-with-colon chain; supplying
        # only the shorter gh-event:abc prefix must not be accepted.
        recorder = Recorder(
            _make_run(
                operation_id="gh-retry:gh-event:abc:def:20260101T000000Z:1:1",
                retry_of_run_id="gh:owner/repo:99:1",
                retry_mode="restarted",
                source="retry",
            )
        )
        recorder.record(stage="validation", status="succeeded", message="ok", timestamp="2026-01-01T00:00:01Z")
        recorder.finalize(final_outcome="succeeded")
        with pytest.raises(ValueError, match="chain_operation_id"):
            render_issue_comment_body(
                recorder.to_document(),
                chain_operation_id="gh-event:abc",
                next_action="none",
            )

    def test_rejects_next_action_mismatch(self) -> None:
        recorder = Recorder(_make_run())
        recorder.record(stage="validation", status="failed", message="failed", timestamp="2026-01-01T00:00:01Z")
        recorder.finalize(final_outcome="failed", termination_code="workflow-timeout")
        with pytest.raises(ValueError, match="next_action must equal derived value"):
            render_issue_comment_body(
                recorder.to_document(),
                chain_operation_id="gh-event:abc",
                next_action="none",
            )

    def test_rejects_none_next_action_when_derived_value_is_not_none(self) -> None:
        recorder = Recorder(_make_run())
        recorder.record(stage="validation", status="failed", message="failed", timestamp="2026-01-01T00:00:01Z")
        recorder.finalize(final_outcome="failed", termination_code="workflow-timeout")
        with pytest.raises(ValueError, match="next_action must be"):
            render_issue_comment_body(
                recorder.to_document(),
                chain_operation_id="gh-event:abc",
                next_action=None,
            )

    def test_rejects_invalid_pre_publication_last_stage(self) -> None:
        recorder = Recorder(_make_run())
        recorder.record(stage="validation", status="succeeded", message="ok", timestamp="2026-01-01T00:00:01Z")
        recorder.finalize(final_outcome="succeeded")
        with pytest.raises(ValueError, match="pre_publication_last_stage must be a valid Phase 0 stage name"):
            render_issue_comment_body(
                recorder.to_document(),
                chain_operation_id="gh-event:abc",
                next_action="none",
                pre_publication_last_stage="forged\n- Injected: yes",
            )

    def test_rejects_invalid_pre_publication_updated_at(self) -> None:
        recorder = Recorder(_make_run())
        recorder.record(stage="validation", status="succeeded", message="ok", timestamp="2026-01-01T00:00:01Z")
        recorder.finalize(final_outcome="succeeded")
        with pytest.raises(ValueError, match="pre_publication_updated_at must be a canonical RFC3339 UTC timestamp"):
            render_issue_comment_body(
                recorder.to_document(),
                chain_operation_id="gh-event:abc",
                next_action="none",
                pre_publication_last_stage="validation",
                pre_publication_updated_at="2026-01-01T00:00:00Z\n- Forged: yes",
            )
