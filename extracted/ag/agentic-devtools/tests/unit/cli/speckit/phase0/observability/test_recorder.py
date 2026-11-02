"""Tests for Recorder in speckit/phase0/observability.py (FR-001, FR-011, FR-012)."""

from __future__ import annotations

from typing import cast

import pytest

from agentic_devtools.cli.speckit.phase0.observability import Recorder, RunRecord


def _make_run() -> RunRecord:
    return RunRecord(
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


class TestRecorder:
    """Tests for the Recorder class."""

    def test_assigns_consecutive_sequence_numbers_from_one(self) -> None:
        recorder = Recorder(_make_run())
        first = recorder.record(stage="validation", status="succeeded", message="a", timestamp="t1")
        second = recorder.record(stage="branch_creation", status="succeeded", message="b", timestamp="t2")
        assert first.sequence == 1
        assert second.sequence == 2

    def test_updates_run_last_stage_and_updated_at(self) -> None:
        recorder = Recorder(_make_run())
        recorder.record(stage="validation", status="succeeded", message="a", timestamp="t1")
        assert recorder.run.last_stage == "validation"
        assert recorder.run.updated_at == "t1"

    def test_sanitizes_control_characters_in_message(self) -> None:
        recorder = Recorder(_make_run())
        event = recorder.record(stage="validation", status="succeeded", message="line1\nline2", timestamp="t1")
        assert event.message == "line1\ufffdline2"

    def test_rejects_unknown_stage(self) -> None:
        recorder = Recorder(_make_run())
        with pytest.raises(ValueError):
            recorder.record(stage="not-a-stage", status="succeeded", message="a", timestamp="t1")

    def test_rejects_unknown_status(self) -> None:
        recorder = Recorder(_make_run())
        with pytest.raises(ValueError):
            recorder.record(stage="validation", status="not-a-status", message="a", timestamp="t1")

    def test_normalizes_property_arrays(self) -> None:
        recorder = Recorder(_make_run())
        event = recorder.record(
            stage="property_discovery",
            status="succeeded",
            message="ok",
            timestamp="t1",
            captured_properties=[{"name": "z", "templateSection": "s"}, {"name": "a", "templateSection": "s"}],
            missing_properties=["z", "a"],
        )
        assert [entry["name"] for entry in event.captured_properties] == ["a", "z"]
        assert event.missing_properties == ["a", "z"]

    def test_finalize_sets_outcome_and_termination_code(self) -> None:
        recorder = Recorder(_make_run())
        recorder.finalize(
            final_outcome="failed",
            termination_code="workflow-cancelled",
            updated_at="t2",
        )
        assert recorder.run.final_outcome == "failed"
        assert recorder.run.termination_code == "workflow-cancelled"
        assert recorder.run.updated_at == "t2"

    def test_finalize_rejects_unknown_outcome(self) -> None:
        recorder = Recorder(_make_run())
        with pytest.raises(ValueError):
            recorder.finalize(final_outcome="not-a-status")

    def test_finalize_rejects_unknown_termination_code(self) -> None:
        recorder = Recorder(_make_run())
        with pytest.raises(ValueError):
            recorder.finalize(final_outcome="failed", termination_code="not-a-code")

    def test_finalize_rejects_in_progress_as_terminal_outcome(self) -> None:
        recorder = Recorder(_make_run())
        with pytest.raises(ValueError, match="in_progress"):
            recorder.finalize(final_outcome="in_progress")

    def test_finalize_rejects_termination_code_with_non_failed_outcome(self) -> None:
        recorder = Recorder(_make_run())
        with pytest.raises(ValueError, match="final_outcome.*failed"):
            recorder.finalize(final_outcome="succeeded", termination_code="workflow-cancelled")

    def test_to_document_produces_full_schema(self) -> None:
        recorder = Recorder(_make_run())
        recorder.record(stage="validation", status="succeeded", message="ok", timestamp="2026-01-01T00:00:00Z")
        recorder.finalize(final_outcome="succeeded")
        document = recorder.to_document()
        assert document["schemaVersion"] == "1.0"
        assert document["run"]["finalOutcome"] == "succeeded"
        assert len(document["events"]) == 1

    def test_rejects_diagnostic_code_with_whitespace(self) -> None:
        recorder = Recorder(_make_run())
        with pytest.raises(ValueError, match="diagnostic_code"):
            recorder.record(
                stage="validation",
                status="succeeded",
                message="ok",
                timestamp="t1",
                diagnostic_code="has space",
            )

    def test_rejects_diagnostic_code_with_newline(self) -> None:
        recorder = Recorder(_make_run())
        with pytest.raises(ValueError, match="diagnostic_code"):
            recorder.record(
                stage="validation",
                status="succeeded",
                message="ok",
                timestamp="t1",
                diagnostic_code="code\ninjected",
            )

    def test_rejects_diagnostic_code_with_trailing_newline(self) -> None:
        recorder = Recorder(_make_run())
        with pytest.raises(ValueError, match="diagnostic_code"):
            recorder.record(
                stage="validation",
                status="succeeded",
                message="ok",
                timestamp="t1",
                diagnostic_code="E001\n",
            )

    def test_accepts_valid_diagnostic_code(self) -> None:
        recorder = Recorder(_make_run())
        event = recorder.record(
            stage="validation",
            status="succeeded",
            message="ok",
            timestamp="t1",
            diagnostic_code="E001",
        )
        assert event.diagnostic_code == "E001"

    def test_accepts_none_diagnostic_code(self) -> None:
        recorder = Recorder(_make_run())
        event = recorder.record(stage="validation", status="succeeded", message="ok", timestamp="t1")
        assert event.diagnostic_code is None

    def test_accepts_absolute_https_diagnostic_url(self) -> None:
        recorder = Recorder(_make_run())
        event = recorder.record(
            stage="validation",
            status="succeeded",
            message="ok",
            timestamp="t1",
            diagnostic_url="https://example.invalid/debug",
        )
        assert event.diagnostic_url == "https://example.invalid/debug"

    def test_accepts_absolute_https_diagnostic_url_with_safe_query(self) -> None:
        recorder = Recorder(_make_run())
        event = recorder.record(
            stage="validation",
            status="succeeded",
            message="ok",
            timestamp="t1",
            diagnostic_url="https://example.invalid/debug?error=timeout&code=500",
        )
        assert event.diagnostic_url == "https://example.invalid/debug?error=timeout&code=500"

    @pytest.mark.parametrize(
        "diagnostic_url",
        [
            "http://example.invalid/debug",
            "/debug",
            "******example.invalid/debug",
            "https://example.invalid/debug?token=secret",
            "https://example.invalid/debug?access_token=oauth-cred",
            "https://example.invalid/debug?authorization=somevalue",
            "https://example.invalid/debug?pat=fakepatvalue123",
            "https://example.invalid/debug?accessToken=oauth-cred",
            "https://example.invalid/debug?refreshToken=somevalue",
            "https://example.invalid/debug?apiKey=fakeapikeyval123",
            "https://example.invalid/debug?APIKey=fakeapikeyval123",
            "https://example.invalid/debug?access-token=oauth-cred",
            "https://example.invalid/debug?error=token%3Ds3cr3tvalue123",
            "https://example.invalid/debug?error=token%253Ds3cr3tvalue123",
            "https://example.invalid/debug?error=bearer+abcdefgh",
            "https://example.invalid/token%3Ds3cr3tvalue123",
            "https://example.invalid/token%253Ds3cr3tvalue123",
            "https://example.invalid/debug#access_token=oauth-cred",
            "https://example.invalid:bad/debug",
            f"https://{'user'}:{'pass'}@example.invalid/debug",
            "https://example.invalid/debug\nforged",
            "https://exa mple.invalid/debug",
            "https://example.invalid/a path",
            123,
        ],
    )
    def test_rejects_unsafe_diagnostic_url(self, diagnostic_url: object) -> None:
        recorder = Recorder(_make_run())
        with pytest.raises(ValueError, match="diagnostic_url"):
            recorder.record(
                stage="validation",
                status="succeeded",
                message="ok",
                timestamp="t1",
                diagnostic_url=cast(str, diagnostic_url),
            )
