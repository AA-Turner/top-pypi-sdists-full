"""Tests for RunRecord in speckit/phase0/observability.py (FR-001)."""

from __future__ import annotations

from agentic_devtools.cli.speckit.phase0.observability import RunRecord


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


class TestRunRecord:
    """Tests for the RunRecord dataclass."""

    def test_defaults_use_null_for_optional_fields(self) -> None:
        run = _make_run()
        document = run.to_dict()
        assert document["retryOfRunId"] is None
        assert document["retryMode"] is None
        assert document["issueType"] is None
        assert document["selectedTemplate"] is None
        assert document["artifactBranch"] is None
        assert document["artifactPath"] is None
        assert document["commitSha"] is None
        assert document["pullRequestUrl"] is None

    def test_defaults_in_progress_and_not_evaluated(self) -> None:
        run = _make_run()
        assert run.final_outcome == "in_progress"
        assert run.freshness == "not-evaluated"

    def test_to_dict_uses_exact_fr001_key_names(self) -> None:
        run = _make_run()
        document = run.to_dict()
        expected_keys = {
            "repository",
            "workflowRunId",
            "workflowRunAttempt",
            "runId",
            "operationId",
            "issueId",
            "retryOfRunId",
            "retryMode",
            "trigger",
            "source",
            "provider",
            "issueType",
            "configurationDecision",
            "configurationReason",
            "selectedTemplate",
            "finalOutcome",
            "lastStage",
            "startedAt",
            "updatedAt",
            "freshness",
            "artifactBranch",
            "artifactPath",
            "commitSha",
            "workflowRunUrl",
            "pullRequestUrl",
        }
        assert set(document.keys()) == expected_keys

    def test_to_dict_redacts_secrets_in_configuration_reason(self) -> None:
        run = _make_run(configuration_reason="failed: token=s3cr3tvalue123")
        document = run.to_dict()
        assert "s3cr3tvalue123" not in document["configurationReason"]
        assert "[REDACTED]" in document["configurationReason"]

    def test_to_dict_sanitizes_control_chars_in_configuration_reason(self) -> None:
        run = _make_run(configuration_reason="reason\x00with\nnull")
        document = run.to_dict()
        assert "\x00" not in document["configurationReason"]
        assert "\n" not in document["configurationReason"]

    def test_to_dict_sanitizes_issue_type(self) -> None:
        run = _make_run(issue_type="token=fake-secret\x00")
        document = run.to_dict()
        assert document["issueType"] is not None
        assert "fake-secret" not in document["issueType"]
        assert "\x00" not in document["issueType"]
        assert "[REDACTED]" in document["issueType"]
