"""Tests for map_answer_to_submission_item."""

import pytest

from agentic_devtools.cli.azure_devops.pr_review_submit_mapper import (
    MapperError,
    map_answer_to_submission_item,
)


class TestMapAnswerToSubmissionItem:
    def test_approve_has_no_suggestions(self):
        item = map_answer_to_submission_item({"filePath": "/src/a.ts", "outcome": "approve", "summary": "LGTM"})
        assert item == {"file_path": "/src/a.ts", "outcome": "approve", "summary": "LGTM", "suggestions": None}

    def test_request_changes_maps_suggestions(self):
        item = map_answer_to_submission_item(
            {
                "filePath": "/src/a.ts",
                "outcome": "request-changes",
                "summary": "Issues",
                "reviewMode": "diff",
                "suggestions": [{"line": 1, "severity": "high", "content": "fix"}],
            }
        )
        assert item["suggestions"][0]["line"] == 1
        assert item["file_path"] == "/src/a.ts"

    def test_skipped_out_of_scope_suggestion_drops_to_none(self):
        item = map_answer_to_submission_item(
            {
                "filePath": "/src/a.ts",
                "outcome": "request-changes",
                "summary": "Issues",
                "reviewMode": "diff",
                "suggestions": [{"out_of_scope": True, "severity": "low", "content": "arch note"}],
            }
        )
        assert item["suggestions"] is None

    def test_missing_summary_defaults_to_empty(self):
        item = map_answer_to_submission_item({"filePath": "/x", "outcome": "approve"})
        assert item["summary"] == ""

    def test_missing_file_path_raises(self):
        with pytest.raises(MapperError):
            map_answer_to_submission_item({"outcome": "approve"})

    def test_blank_file_path_raises(self):
        with pytest.raises(MapperError):
            map_answer_to_submission_item({"filePath": "   ", "outcome": "approve"})

    def test_invalid_outcome_raises(self):
        with pytest.raises(MapperError):
            map_answer_to_submission_item({"filePath": "/x", "outcome": "nope"})
