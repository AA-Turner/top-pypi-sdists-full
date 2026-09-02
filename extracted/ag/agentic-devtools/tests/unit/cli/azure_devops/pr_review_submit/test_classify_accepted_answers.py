"""Tests for classify_accepted_answers."""

from unittest.mock import patch

from agentic_devtools.cli.azure_devops.pr_review_submit import classify_accepted_answers
from agentic_devtools.cli.azure_devops.pr_review_submit_mapper import MapperError

_MODULE = "agentic_devtools.cli.azure_devops.pr_review_submit"
_FILE_KEY = "src-a-ts-deadbeef"


def _complete(**overrides):
    answer = {
        "schemaVersion": 1,
        "prId": 123,
        "commitHash": "a" * 40,
        "fileKey": _FILE_KEY,
        "filePath": "/src/a.ts",
        "reviewMode": "diff",
        "reviewDepth": "deep",
        "promptHash": "p" * 64,
        "attemptId": "abc123",
        "status": "complete",
        "outcome": "request-changes",
        "summary": "Issues.",
        "suggestions": [{"line": 1, "severity": "high", "content": "fix"}],
        "needsInfo": None,
        "reviewer": {"model": "m"},
        "confidence": "high",
    }
    answer.update(overrides)
    return answer


class TestClassifyAcceptedAnswers:
    def test_non_complete_is_skipped(self):
        latest = {_FILE_KEY: _complete(status="needs-info")}
        submittable, skipped, stale = classify_accepted_answers(latest, lambda k: None)
        assert submittable == []
        assert skipped[0]["fileKey"] == _FILE_KEY
        assert "status:needs-info" in skipped[0]["reason"]
        assert stale == []

    def test_missing_scaffold_is_stale(self):
        latest = {_FILE_KEY: _complete()}
        submittable, skipped, stale = classify_accepted_answers(latest, lambda k: None)
        assert submittable == []
        assert stale[0]["fileKey"] == _FILE_KEY
        assert "no scaffold baseline found" in stale[0]["errors"]

    def test_validation_errors_are_stale(self):
        answer = _complete()
        latest = {_FILE_KEY: answer}
        with patch(f"{_MODULE}.validate_answer_write", return_value=["stale: commitHash mismatch"]):
            submittable, skipped, stale = classify_accepted_answers(latest, lambda k: answer)
        assert submittable == []
        assert stale[0]["errors"] == ["stale: commitHash mismatch"]

    def test_unmappable_is_skipped(self):
        answer = _complete()
        latest = {_FILE_KEY: answer}
        with (
            patch(f"{_MODULE}.validate_answer_write", return_value=[]),
            patch(f"{_MODULE}.map_answer_to_submission_item", side_effect=MapperError("boom")),
        ):
            submittable, skipped, stale = classify_accepted_answers(latest, lambda k: answer)
        assert submittable == []
        assert "unmappable: boom" in skipped[0]["reason"]

    def test_valid_answer_is_submittable(self):
        answer = _complete()
        latest = {_FILE_KEY: answer}
        submittable, skipped, stale = classify_accepted_answers(latest, lambda k: answer)
        assert skipped == []
        assert stale == []
        assert submittable[0]["fileKey"] == _FILE_KEY
        assert submittable[0]["filePath"] == "/src/a.ts"
        assert submittable[0]["item"]["outcome"] == "request-changes"
