"""Tests for _normalize_jira_comment."""

from __future__ import annotations

from agentic_devtools.orchestration.nodes._issue_retrieval import _normalize_jira_comment


class TestNormalizeJiraComment:
    def test_string_body_preserved(self) -> None:
        result = _normalize_jira_comment({"id": "7", "body": "Plain text", "created": "2024-01-01"})
        assert result == {"comment_id": "7", "body": "Plain text", "created_at": "2024-01-01"}

    def test_adf_body_converted_to_text(self) -> None:
        adf = {
            "type": "doc",
            "content": [{"type": "paragraph", "content": [{"type": "text", "text": "Hello ADF"}]}],
        }
        result = _normalize_jira_comment({"id": "8", "body": adf, "created": "2024-02-02"})
        assert result["comment_id"] == "8"
        assert "Hello ADF" in result["body"]

    def test_missing_fields_default_to_empty_strings(self) -> None:
        result = _normalize_jira_comment({})
        assert result == {"comment_id": "", "body": "", "created_at": ""}

    def test_none_id_and_created_produce_empty_strings(self) -> None:
        result = _normalize_jira_comment({"id": None, "body": "text", "created": None})
        assert result == {"comment_id": "", "body": "text", "created_at": ""}
