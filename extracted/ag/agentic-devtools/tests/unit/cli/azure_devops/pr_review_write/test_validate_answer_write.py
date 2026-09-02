"""Tests for validate_answer_write."""

from agentic_devtools.cli.azure_devops.pr_review_answers import ANSWER_SCHEMA_VERSION
from agentic_devtools.cli.azure_devops.pr_review_write import validate_answer_write


def _scaffold():
    return {
        "fileKey": "src-a-ts-deadbeef",
        "filePath": "/src/a.ts",
        "prId": 123,
        "promptHash": "p" * 64,
        "commitHash": "a" * 40,
        "attemptId": "abc123",
        "reviewMode": "diff",
        "reviewDepth": None,
    }


def _valid_answer(**overrides):
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
        "summary": "ok",
        "suggestions": [],
        "reviewer": {"model": "claude-opus-4.6"},
    }
    answer.update(overrides)
    return answer


class TestValidateAnswerWrite:
    def test_valid(self):
        assert validate_answer_write(_valid_answer(), "src-a-ts-deadbeef", _scaffold()) == []

    def test_schema_error_surfaces(self):
        errors = validate_answer_write(_valid_answer(prId="x"), "src-a-ts-deadbeef", _scaffold())
        assert any("prId" in e for e in errors)

    def test_scope_error_surfaces(self):
        errors = validate_answer_write(_valid_answer(fileKey="other"), "src-a-ts-deadbeef", _scaffold())
        assert any("fileKey" in e for e in errors)

    def test_freshness_error_surfaces(self):
        errors = validate_answer_write(_valid_answer(commitHash="b" * 40), "src-a-ts-deadbeef", _scaffold())
        assert any("stale answer" in e for e in errors)

    def test_line_anchoring_error_surfaces(self):
        answer = _valid_answer(
            reviewMode="binary",
            suggestions=[{"line": 5, "severity": "low", "content": "x"}],
        )
        errors = validate_answer_write(answer, "src-a-ts-deadbeef", _scaffold())
        assert any("not allowed for reviewMode" in e for e in errors)
