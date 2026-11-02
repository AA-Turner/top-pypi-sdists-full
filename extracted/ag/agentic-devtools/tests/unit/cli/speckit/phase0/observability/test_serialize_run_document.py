"""Tests for serialize_run_document in speckit/phase0/observability.py (FR-001)."""

from __future__ import annotations

import pytest

from agentic_devtools.cli.speckit.phase0.observability import (
    RunRecord,
    StageEvent,
    serialize_run_document,
)


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
        final_outcome="succeeded",
    )
    defaults.update(overrides)
    return RunRecord(**defaults)  # type: ignore[arg-type]


def _make_event(**overrides: object) -> StageEvent:
    defaults = dict(
        sequence=1,
        stage="validation",
        status="succeeded",
        timestamp="2026-01-01T00:00:00Z",
        message="ok",
    )
    defaults.update(overrides)
    return StageEvent(**defaults)  # type: ignore[arg-type]


class TestSerializeRunDocument:
    """Tests for the serialize_run_document function."""

    def test_top_level_shape_matches_fr001(self) -> None:
        run = _make_run(last_stage="validation")
        event = _make_event()
        document = serialize_run_document(run, [event])

        assert set(document.keys()) == {"schemaVersion", "terminationCode", "run", "events"}
        assert document["schemaVersion"] == "1.0"
        assert document["terminationCode"] is None
        assert document["events"] == [event.to_dict()]

    def test_empty_events_list_when_no_stage_attempted(self) -> None:
        run = _make_run(
            configuration_decision="disabled",
            configuration_reason="Phase 0 is disabled; Phase 1 will proceed as normal",
            final_outcome="skipped",
        )
        document = serialize_run_document(run, [])
        assert document["events"] == []
        assert document["run"]["lastStage"] is None

    def test_rejects_mismatched_run_id_coordinates(self) -> None:
        run = _make_run(run_id="gh:owner/repo:2:1")
        with pytest.raises(ValueError, match="run_id must match"):
            serialize_run_document(run, [])

    def test_rejects_non_contiguous_event_sequence(self) -> None:
        run = _make_run(last_stage="validation")
        events = [
            _make_event(sequence=1, stage="validation"),
            _make_event(sequence=3, stage="cleanup", timestamp="2026-01-01T00:00:01Z", message="done"),
        ]
        with pytest.raises(ValueError, match="contiguous sequence"):
            serialize_run_document(run, events)

    @pytest.mark.parametrize("sequence", [True, 1.0])
    def test_rejects_non_integer_event_sequence(self, sequence: object) -> None:
        run = _make_run(last_stage="validation")
        with pytest.raises(ValueError, match="event.sequence must be a positive integer"):
            serialize_run_document(run, [_make_event(sequence=sequence)])  # type: ignore[arg-type]

    def test_rejects_invalid_operation_id(self) -> None:
        with pytest.raises(ValueError, match="Invalid operation_id"):
            serialize_run_document(_make_run(operation_id="gh/event:abc"), [])

    def test_rejects_invalid_issue_id(self) -> None:
        with pytest.raises(ValueError, match="Invalid issue_id"):
            serialize_run_document(_make_run(issue_id="%ZZ"), [])

    def test_rejects_invalid_final_outcome(self) -> None:
        with pytest.raises(ValueError, match="Unknown final_outcome"):
            serialize_run_document(_make_run(final_outcome="unknown"), [])

    def test_rejects_invalid_source(self) -> None:
        with pytest.raises(ValueError, match="Unknown source"):
            serialize_run_document(_make_run(source="bogus"), [])

    def test_rejects_invalid_configuration_decision(self) -> None:
        with pytest.raises(ValueError, match="Unknown configuration_decision"):
            serialize_run_document(_make_run(configuration_decision="bogus"), [])

    def test_accepts_blocked_configuration_decision(self) -> None:
        document = serialize_run_document(
            _make_run(configuration_decision="blocked", final_outcome="blocked", last_stage="validation"),
            [_make_event()],
        )
        assert document["run"]["configurationDecision"] == "blocked"

    def test_rejects_blocked_with_successful_outcome(self) -> None:
        with pytest.raises(ValueError, match="final_outcome must be 'blocked' or 'failed'.*blocked"):
            serialize_run_document(
                _make_run(configuration_decision="blocked", final_outcome="succeeded"),
                [],
            )

    def test_rejects_blocked_failed_without_termination_code(self) -> None:
        with pytest.raises(ValueError, match="termination_code must be set for a 'blocked' run"):
            serialize_run_document(
                _make_run(configuration_decision="blocked", final_outcome="failed", termination_code=None),
                [],
            )

    def test_accepts_not_evaluated_configuration_decision(self) -> None:
        # not-evaluated requires failed + termination_code set (pre-evaluation cancellation).
        document = serialize_run_document(
            _make_run(
                configuration_decision="not-evaluated",
                final_outcome="failed",
                termination_code="workflow-cancelled",
                freshness="not-evaluated",
            ),
            [],
        )
        assert document["run"]["configurationDecision"] == "not-evaluated"

    def test_rejects_not_evaluated_with_successful_outcome(self) -> None:
        with pytest.raises(ValueError, match="final_outcome must be 'failed'.*not-evaluated"):
            serialize_run_document(
                _make_run(
                    configuration_decision="not-evaluated",
                    final_outcome="succeeded",
                    freshness="not-evaluated",
                    termination_code=None,
                ),
                [],
            )

    def test_rejects_not_evaluated_without_termination_code(self) -> None:
        with pytest.raises(ValueError, match="termination_code must be set.*not-evaluated"):
            serialize_run_document(
                _make_run(
                    configuration_decision="not-evaluated",
                    final_outcome="failed",
                    freshness="not-evaluated",
                    termination_code=None,
                ),
                [],
            )

    def test_rejects_disabled_with_non_skipped_outcome(self) -> None:
        with pytest.raises(ValueError, match="final_outcome must be 'skipped' or 'failed'.*disabled"):
            serialize_run_document(
                _make_run(configuration_decision="disabled", final_outcome="succeeded"),
                [],
            )

    def test_rejects_disabled_failed_without_termination_code(self) -> None:
        with pytest.raises(ValueError, match="termination_code must be set for a 'disabled' run"):
            serialize_run_document(
                _make_run(configuration_decision="disabled", final_outcome="failed", termination_code=None),
                [],
            )

    def test_rejects_not_evaluated_with_non_not_evaluated_freshness(self) -> None:
        with pytest.raises(ValueError, match="freshness must be 'not-evaluated'.*not-evaluated"):
            serialize_run_document(
                _make_run(
                    configuration_decision="not-evaluated",
                    final_outcome="failed",
                    freshness="fresh",
                    termination_code="workflow-cancelled",
                ),
                [],
            )

    def test_rejects_invalid_provider(self) -> None:
        with pytest.raises(ValueError, match="Unknown provider"):
            serialize_run_document(_make_run(provider="bogus"), [])

    def test_rejects_invalid_last_stage(self) -> None:
        with pytest.raises(ValueError, match="Unknown last_stage"):
            serialize_run_document(_make_run(last_stage="unknown-stage"), [])

    def test_rejects_invalid_freshness(self) -> None:
        with pytest.raises(ValueError, match="Unknown freshness"):
            serialize_run_document(_make_run(freshness="mystery"), [])

    def test_rejects_non_not_evaluated_freshness_for_disabled_run(self) -> None:
        with pytest.raises(ValueError, match="freshness must be 'not-evaluated'"):
            serialize_run_document(
                _make_run(configuration_decision="disabled", final_outcome="skipped", freshness="fresh"),
                [],
            )

    def test_rejects_invalid_started_at_timestamp_shape(self) -> None:
        with pytest.raises(ValueError, match="Invalid started_at"):
            serialize_run_document(_make_run(started_at="not-a-timestamp"), [])

    def test_rejects_invalid_updated_at_calendar_timestamp(self) -> None:
        with pytest.raises(ValueError, match="Invalid updated_at"):
            serialize_run_document(_make_run(updated_at="2026-02-30T00:00:00Z"), [])

    def test_rejects_invalid_run_coordinates(self) -> None:
        with pytest.raises(ValueError, match="Invalid run coordinate fields"):
            serialize_run_document(_make_run(workflow_run_id=True), [])

    def test_rejects_invalid_event_stage(self) -> None:
        with pytest.raises(ValueError, match="Unknown event stage"):
            serialize_run_document(_make_run(last_stage="validation"), [_make_event(stage="invalid-stage")])

    def test_rejects_invalid_event_status(self) -> None:
        with pytest.raises(ValueError, match="Unknown event status"):
            serialize_run_document(_make_run(last_stage="validation"), [_make_event(status="invalid-status")])

    def test_rejects_invalid_event_timestamp(self) -> None:
        with pytest.raises(ValueError, match="Invalid event timestamp"):
            serialize_run_document(_make_run(last_stage="validation"), [_make_event(timestamp="bad-ts")])

    def test_rejects_last_stage_mismatch_with_last_event(self) -> None:
        with pytest.raises(ValueError, match="run.last_stage must equal"):
            serialize_run_document(_make_run(last_stage="cleanup"), [_make_event(stage="validation")])

    def test_rejects_non_null_last_stage_when_events_are_empty(self) -> None:
        with pytest.raises(ValueError, match="run.last_stage must be null when no events are recorded"):
            serialize_run_document(_make_run(last_stage="validation"), [])

    def test_rejects_empty_events_for_non_disabled_non_terminated_runs(self) -> None:
        with pytest.raises(ValueError, match="events may be empty only for disabled/skipped runs"):
            serialize_run_document(
                _make_run(
                    configuration_decision="enabled",
                    final_outcome="succeeded",
                    last_stage=None,
                ),
                [],
            )

    def test_accepts_empty_events_for_pre_stage_timeout_failure(self) -> None:
        document = serialize_run_document(
            _make_run(
                final_outcome="failed",
                termination_code="workflow-timeout",
                last_stage=None,
            ),
            [],
        )
        assert document["events"] == []

    def test_accepts_empty_events_for_pre_stage_cancelled_failure(self) -> None:
        document = serialize_run_document(
            _make_run(
                final_outcome="failed",
                termination_code="workflow-cancelled",
                last_stage=None,
            ),
            [],
        )
        assert document["events"] == []

    def test_accepts_empty_events_for_disabled_timeout_failure(self) -> None:
        document = serialize_run_document(
            _make_run(
                configuration_decision="disabled",
                final_outcome="failed",
                termination_code="workflow-timeout",
                last_stage=None,
            ),
            [],
        )
        assert document["events"] == []

    def test_accepts_empty_events_for_disabled_cancelled_failure(self) -> None:
        document = serialize_run_document(
            _make_run(
                configuration_decision="disabled",
                final_outcome="failed",
                termination_code="workflow-cancelled",
                last_stage=None,
            ),
            [],
        )
        assert document["events"] == []

    def test_rejects_unknown_termination_code(self) -> None:
        with pytest.raises(ValueError, match="Unknown termination code"):
            serialize_run_document(_make_run(termination_code="bad-code"), [])

    def test_rejects_termination_code_when_outcome_is_not_failed(self) -> None:
        with pytest.raises(ValueError, match="termination_code may only be set"):
            serialize_run_document(_make_run(termination_code="workflow-timeout", final_outcome="succeeded"), [])

    def test_rejects_retry_operation_without_retry_of_run_id(self) -> None:
        with pytest.raises(ValueError, match="retry_of_run_id must be a canonical runId"):
            serialize_run_document(
                _make_run(
                    operation_id="gh-retry:gh-event:delivery:20260101T000000Z:1:1",
                    retry_of_run_id=None,
                ),
                [],
            )

    def test_rejects_retry_of_run_id_for_non_retry_operation(self) -> None:
        with pytest.raises(ValueError, match="retry_of_run_id must be null for non-retry"):
            serialize_run_document(_make_run(retry_of_run_id="gh:owner/repo:1:1"), [])

    def test_rejects_invalid_retry_mode_for_retry_operation(self) -> None:
        with pytest.raises(ValueError, match="retry_mode must be one of"):
            serialize_run_document(
                _make_run(
                    operation_id="gh-retry:gh-event:delivery:20260101T000000Z:1:1",
                    retry_of_run_id="gh:owner/repo:99:1",
                    retry_mode="bad-mode",
                ),
                [],
            )

    def test_rejects_non_null_retry_mode_for_non_retry_operation(self) -> None:
        with pytest.raises(ValueError, match="retry_mode must be null for non-retry"):
            serialize_run_document(_make_run(retry_mode="resumed"), [])

    def test_rejects_source_mismatch_for_retry_operation(self) -> None:
        with pytest.raises(ValueError, match="source must match derived source"):
            serialize_run_document(
                _make_run(
                    operation_id="gh-retry:gh-event:delivery:20260101T000000Z:1:1",
                    retry_of_run_id="gh:owner/repo:99:1",
                    retry_mode="resumed",
                    source="provider-event",
                ),
                [],
            )

    def test_accepts_retry_operation_with_canonical_retry_of_run_id(self) -> None:
        run = _make_run(
            operation_id="gh-retry:gh-event:delivery:20260101T000000Z:1:1",
            retry_of_run_id="gh:owner/repo:99:1",
            retry_mode="restarted",
            source="retry",
            last_stage="validation",
        )
        document = serialize_run_document(run, [_make_event()])
        assert document["run"]["retryOfRunId"] == "gh:owner/repo:99:1"

    def test_sanitizes_event_message_for_directly_constructed_event(self) -> None:
        run = _make_run(last_stage="validation")
        event = _make_event(message="Authorization: ApiKey abc123\nnext\u0000")

        document = serialize_run_document(run, [event])

        assert document["events"][0]["message"] == "Authorization: [REDACTED]\ufffdnext\ufffd"

    def test_rejects_invalid_diagnostic_code_in_directly_constructed_event(self) -> None:
        run = _make_run(last_stage="validation")
        event = _make_event(diagnostic_code="E001\n")
        with pytest.raises(ValueError, match="diagnostic_code must be printable"):
            serialize_run_document(run, [event])

    def test_rejects_invalid_diagnostic_url_in_directly_constructed_event(self) -> None:
        run = _make_run(last_stage="validation")
        event = _make_event(diagnostic_url="not-a-url")
        with pytest.raises(ValueError):
            serialize_run_document(run, [event])

    def test_normalizes_captured_properties_in_directly_constructed_event(self) -> None:
        _FAKE = "".join(["fake", "secret", "val123"])
        run = _make_run(last_stage="validation")
        event = _make_event(
            captured_properties=[
                {"name": "b", "templateSection": "s2"},
                {"name": "a", "templateSection": f"secret={_FAKE}"},
            ]
        )
        document = serialize_run_document(run, [event])
        serialized = document["events"][0]["capturedProperties"]
        assert serialized[0]["name"] == "a"
        assert _FAKE not in serialized[0]["templateSection"]
        assert "[REDACTED]" in serialized[0]["templateSection"]

    def test_normalizes_missing_properties_in_directly_constructed_event(self) -> None:
        _FAKE = "".join(["fake", "secret", "val123"])
        run = _make_run(last_stage="validation")
        event = _make_event(missing_properties=[f"token={_FAKE}", "alpha"])
        document = serialize_run_document(run, [event])
        serialized = document["events"][0]["missingProperties"]
        assert "alpha" in serialized
        assert not any(_FAKE in name for name in serialized)

    def test_rejects_null_trigger(self) -> None:
        with pytest.raises(ValueError, match="trigger must be a non-empty string"):
            serialize_run_document(_make_run(trigger=None), [])  # type: ignore[arg-type]

    def test_rejects_empty_trigger(self) -> None:
        with pytest.raises(ValueError, match="trigger must be a non-empty string"):
            serialize_run_document(_make_run(trigger=""), [])

    def test_rejects_null_configuration_reason(self) -> None:
        with pytest.raises(ValueError, match="configuration_reason must be a non-empty string"):
            serialize_run_document(_make_run(configuration_reason=None), [])  # type: ignore[arg-type]

    def test_rejects_empty_configuration_reason(self) -> None:
        with pytest.raises(ValueError, match="configuration_reason must be a non-empty string"):
            serialize_run_document(_make_run(configuration_reason=""), [])

    def test_rejects_null_workflow_run_url(self) -> None:
        with pytest.raises(ValueError, match="workflow_run_url must be a non-empty string"):
            serialize_run_document(_make_run(workflow_run_url=None), [])  # type: ignore[arg-type]

    def test_rejects_empty_workflow_run_url(self) -> None:
        with pytest.raises(ValueError, match="workflow_run_url must be a non-empty string"):
            serialize_run_document(_make_run(workflow_run_url=""), [])

    def test_rejects_non_https_workflow_run_url(self) -> None:
        with pytest.raises(ValueError, match="workflow_run_url must be an absolute HTTPS URL"):
            serialize_run_document(_make_run(workflow_run_url="http://example.invalid/run/1"), [])

    def test_rejects_non_https_pull_request_url(self) -> None:
        run = _make_run(last_stage="validation", pull_request_url="http://example.invalid/pr/1")
        with pytest.raises(ValueError, match="pull_request_url must be an absolute HTTPS URL"):
            serialize_run_document(run, [_make_event()])

    def test_rejects_workflow_run_url_with_whitespace(self) -> None:
        with pytest.raises(ValueError, match="workflow_run_url must not contain whitespace"):
            serialize_run_document(_make_run(workflow_run_url="https://example.invalid/run /1"), [])

    def test_rejects_workflow_run_url_with_invalid_port(self) -> None:
        with pytest.raises(ValueError, match="workflow_run_url must be a valid absolute HTTPS URL"):
            serialize_run_document(_make_run(workflow_run_url="https://example.invalid:bad/run"), [])

    def test_rejects_workflow_run_url_with_userinfo(self) -> None:
        _userinfo_run_url = "https://" + "user:pass@" + "example.invalid/run"
        with pytest.raises(ValueError, match="workflow_run_url must not contain userinfo"):
            serialize_run_document(_make_run(workflow_run_url=_userinfo_run_url), [])

    def test_rejects_pull_request_url_with_userinfo(self) -> None:
        _userinfo_pr_url = "https://" + "user:pass@" + "example.invalid/pr/1"
        run = _make_run(last_stage="validation", pull_request_url=_userinfo_pr_url)
        with pytest.raises(ValueError, match="pull_request_url must not contain userinfo"):
            serialize_run_document(run, [_make_event()])

    def test_accepts_https_pull_request_url(self) -> None:
        run = _make_run(last_stage="validation", pull_request_url="https://example.invalid/pr/1")
        document = serialize_run_document(run, [_make_event()])
        assert document["run"]["pullRequestUrl"] == "https://example.invalid/pr/1"

    def test_rejects_retry_operation_id_with_mismatched_run_coordinates(self) -> None:
        with pytest.raises(ValueError, match="retry operation_id run/attempt coordinates"):
            serialize_run_document(
                _make_run(
                    operation_id="gh-retry:gh-event:delivery:20260101T000000Z:99:2",
                    retry_of_run_id="gh:owner/repo:2:1",
                    retry_mode="resumed",
                    source="retry",
                ),
                [],
            )

    def test_rejects_retry_of_run_id_self_reference(self) -> None:
        # retry_of_run_id must reference a prior run, not the current run.
        with pytest.raises(ValueError, match="retry_of_run_id must reference a prior run"):
            serialize_run_document(
                _make_run(
                    operation_id="gh-retry:gh-event:abc:20260101T000000Z:1:1",
                    retry_of_run_id="gh:owner/repo:1:1",  # same as default run_id
                    retry_mode="restarted",
                    source="retry",
                ),
                [],
            )

    def test_rejects_non_string_selected_template(self) -> None:
        with pytest.raises(ValueError, match="selected_template must be a non-empty string or null"):
            serialize_run_document(
                _make_run(selected_template=123),  # type: ignore[arg-type]
                [],
            )

    def test_rejects_empty_string_artifact_branch(self) -> None:
        with pytest.raises(ValueError, match="artifact_branch must be a non-empty string or null"):
            serialize_run_document(
                _make_run(artifact_branch=""),
                [],
            )

    def test_rejects_non_string_artifact_path(self) -> None:
        with pytest.raises(ValueError, match="artifact_path must be a non-empty string or null"):
            serialize_run_document(
                _make_run(artifact_path=[]),  # type: ignore[arg-type]
                [],
            )

    def test_selected_template_is_sanitized_in_structured_log(self) -> None:
        """selectedTemplate with control characters must be sanitized in the FR-001 document."""
        _FAKE_TMPL = "template.md\x00\x01"
        doc = serialize_run_document(
            _make_run(selected_template=_FAKE_TMPL, last_stage="validation"),
            [_make_event()],
        )
        assert "\x00" not in doc["run"]["selectedTemplate"]
        assert "\x01" not in doc["run"]["selectedTemplate"]
        assert doc["run"]["selectedTemplate"] is not None

    def test_artifact_fields_are_sanitized_in_structured_log(self) -> None:
        """Artifact fields with embedded credentials or control chars must be sanitized (FR-011)."""
        _FAKE_BRANCH = "feature/branch\x00"
        _FAKE_PATH = "artifacts/file.json?access_token=topdummy123"
        _FAKE_SHA = "abc123\x01def"
        doc = serialize_run_document(
            _make_run(
                artifact_branch=_FAKE_BRANCH,
                artifact_path=_FAKE_PATH,
                commit_sha=_FAKE_SHA,
                last_stage="validation",
            ),
            [_make_event()],
        )
        # Control characters must be stripped from branch and sha
        assert "\x00" not in doc["run"]["artifactBranch"]
        assert "\x01" not in doc["run"]["commitSha"]
        # Embedded token in artifact path must be redacted
        assert "topdummy123" not in doc["run"]["artifactPath"]
        assert "[REDACTED]" in doc["run"]["artifactPath"]

    def test_artifact_fields_none_preserved_in_structured_log(self) -> None:
        """Null artifact fields must remain null in the FR-001 document."""
        doc = serialize_run_document(_make_run(last_stage="validation"), [_make_event()])
        assert doc["run"]["artifactBranch"] is None
        assert doc["run"]["artifactPath"] is None
        assert doc["run"]["commitSha"] is None
