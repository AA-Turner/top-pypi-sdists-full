"""Tests for render_stdout_projection in speckit/phase0/projections.py (FR-001)."""

from __future__ import annotations

import json

from agentic_devtools.cli.speckit.phase0.observability import Recorder, RunRecord
from agentic_devtools.cli.speckit.phase0.projections import render_stdout_projection


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


class TestRenderStdoutProjection:
    """Tests for the render_stdout_projection function."""

    def test_header_line_uses_exact_field_order_and_labels(self) -> None:
        recorder = Recorder(
            _make_run(
                configuration_decision="disabled",
                configuration_reason="Phase 0 is disabled; Phase 1 will proceed as normal",
            )
        )
        recorder.finalize(final_outcome="skipped", updated_at="2026-01-01T00:00:00Z")
        document = recorder.to_document()

        rendered = render_stdout_projection(document)
        header = rendered.splitlines()[0]
        assert header == (
            "PHASE0_RUN run_id=gh:owner/repo:1:1 operation_id=gh-event:abc issue=owner/repo#1 "
            "outcome=skipped last_stage=none updated_at=2026-01-01T00:00:00Z retry_of=none "
            "retry_mode=none freshness=not-evaluated"
        )

    def test_stage_line_serializes_message_as_json_string(self) -> None:
        recorder = Recorder(_make_run())
        recorder.record(
            stage="validation", status="succeeded", message='has "quotes"', timestamp="2026-01-01T00:00:01Z"
        )
        document = recorder.to_document()

        rendered = render_stdout_projection(document)
        stage_line = rendered.splitlines()[1]
        expected_message = json.dumps('has "quotes"')
        expected_line = (
            "PHASE0_STAGE seq=1 stage=validation status=succeeded "
            f"at=2026-01-01T00:00:01Z code=none message={expected_message}"
        )
        assert stage_line == (expected_line)

    def test_no_events_produces_only_header(self) -> None:
        recorder = Recorder(
            _make_run(
                configuration_decision="disabled",
                configuration_reason="Phase 0 is disabled; Phase 1 will proceed as normal",
            )
        )
        recorder.finalize(final_outcome="skipped")
        rendered = render_stdout_projection(recorder.to_document())
        assert len(rendered.splitlines()) == 1
