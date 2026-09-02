"""Tests for validate_answer_schema."""

from agentic_devtools.cli.azure_devops.pr_review_answers import ANSWER_SCHEMA_VERSION
from agentic_devtools.cli.azure_devops.pr_review_write import validate_answer_schema


def _base(**overrides):
    answer = {
        "schemaVersion": ANSWER_SCHEMA_VERSION,
        "prId": 123,
        "commitHash": "a" * 40,
        "fileKey": "src-a-ts-deadbeef",
        "filePath": "/src/a.ts",
        "promptHash": "p" * 64,
        "attemptId": "abc123",
        "reviewMode": "diff",
        "status": "complete",
        "outcome": "approve",
        "summary": "Looks good.",
        "suggestions": [],
        "reviewer": {"model": "claude-opus-4.6"},
    }
    answer.update(overrides)
    return answer


class TestValidateAnswerSchema:
    def test_valid_complete(self):
        assert validate_answer_schema(_base()) == []

    def test_non_dict(self):
        assert validate_answer_schema("nope") == ["answer must be a JSON object"]

    def test_bad_schema_version(self):
        errors = validate_answer_schema(_base(schemaVersion=999))
        assert any("schemaVersion" in e for e in errors)

    def test_pr_id_not_int(self):
        errors = validate_answer_schema(_base(prId="123"))
        assert any("prId" in e for e in errors)

    def test_pr_id_bool_rejected(self):
        errors = validate_answer_schema(_base(prId=True))
        assert any("prId" in e for e in errors)

    def test_missing_string_field(self):
        errors = validate_answer_schema(_base(commitHash=""))
        assert any("commitHash" in e for e in errors)

    def test_invalid_review_mode(self):
        errors = validate_answer_schema(_base(reviewMode="weird"))
        assert any("reviewMode" in e for e in errors)

    def test_review_depth_invalid_type_rejected(self):
        errors = validate_answer_schema(_base(reviewDepth={}))
        assert any("reviewDepth" in e for e in errors)

    def test_review_depth_invalid_value_rejected(self):
        errors = validate_answer_schema(_base(reviewDepth="weird"))
        assert any("reviewDepth" in e for e in errors)

    def test_review_depth_empty_string_rejected(self):
        errors = validate_answer_schema(_base(reviewDepth=""))
        assert any("reviewDepth" in e for e in errors)

    def test_invalid_status(self):
        errors = validate_answer_schema(_base(status="weird"))
        assert any("status" in e for e in errors)

    def test_confidence_invalid_type_rejected(self):
        errors = validate_answer_schema(_base(confidence={}))
        assert any("confidence" in e for e in errors)

    def test_confidence_invalid_value_rejected(self):
        errors = validate_answer_schema(_base(confidence="certain"))
        assert any("confidence" in e for e in errors)

    def test_confidence_empty_string_rejected(self):
        errors = validate_answer_schema(_base(confidence=""))
        assert any("confidence" in e for e in errors)

    def test_suggestions_not_list(self):
        errors = validate_answer_schema(_base(status="failed", suggestions="nope"))
        assert any("suggestions must be a list" in e for e in errors)

    def test_complete_requires_outcome(self):
        errors = validate_answer_schema(_base(outcome="weird"))
        assert any("outcome" in e for e in errors)

    def test_complete_requires_summary(self):
        errors = validate_answer_schema(_base(summary=""))
        assert any("summary" in e for e in errors)

    def test_complete_requires_reviewer(self):
        answer = _base()
        del answer["reviewer"]
        errors = validate_answer_schema(answer)
        assert any("reviewer" in e for e in errors)

    def test_request_changes_with_suggestion_needs_suggestion(self):
        errors = validate_answer_schema(_base(outcome="request-changes-with-suggestion", suggestions=[]))
        assert any("at least one suggestion" in e for e in errors)

    def test_request_changes_with_suggestion_ok(self):
        answer = _base(
            outcome="request-changes-with-suggestion",
            suggestions=[{"line": 1, "severity": "high", "content": "x", "replacement_code": "y"}],
        )
        assert validate_answer_schema(answer) == []

    def test_request_changes_with_suggestion_missing_replacement(self):
        answer = _base(
            outcome="request-changes-with-suggestion",
            suggestions=[{"line": 1, "severity": "high", "content": "x"}],
        )
        errors = validate_answer_schema(answer)
        assert any("replacement_code is required" in e for e in errors)

    def test_request_changes_with_suggestion_non_dict_suggestion(self):
        answer = _base(outcome="request-changes-with-suggestion", suggestions=["nope"])
        errors = validate_answer_schema(answer)
        assert any("suggestions[0]" in e for e in errors)

    def test_invalid_suggestion_reported(self):
        errors = validate_answer_schema(_base(suggestions=[{"severity": "nope", "content": ""}]))
        assert any("suggestions[0]" in e for e in errors)

    def test_needs_info_requires_blocked_on(self):
        answer = _base(status="needs-info", outcome=None, summary=None, reviewer=None)
        errors = validate_answer_schema(answer)
        assert any("blockedOn" in e for e in errors)

    def test_needs_info_valid(self):
        answer = _base(
            status="needs-info",
            outcome=None,
            summary=None,
            reviewer=None,
            blockedOn="Need the schema for the related migration.",
            partialSummary="Reviewed the happy path.",
            partialFindings=[],
        )
        assert validate_answer_schema(answer) == []

    def test_needs_info_blank_partial_summary_rejected(self):
        answer = _base(
            status="needs-info",
            outcome=None,
            summary=None,
            reviewer=None,
            blockedOn="Need more context.",
            partialSummary="   ",
        )
        errors = validate_answer_schema(answer)
        assert any("partialSummary" in e for e in errors)

    def test_needs_info_partial_findings_non_list_rejected(self):
        answer = _base(
            status="needs-info",
            outcome=None,
            summary=None,
            reviewer=None,
            blockedOn="Need more context.",
            partialFindings="not a list",
        )
        errors = validate_answer_schema(answer)
        assert any("partialFindings" in e for e in errors)

    def test_needs_info_optional_fields_absent_is_ok(self):
        # partialSummary and partialFindings are optional; omitting them is valid.
        answer = _base(status="needs-info", outcome=None, summary=None, reviewer=None, blockedOn="x")
        assert validate_answer_schema(answer) == []

    def test_failed_status_minimal(self):
        answer = _base(status="failed", outcome=None, summary=None, reviewer=None)
        assert validate_answer_schema(answer) == []
