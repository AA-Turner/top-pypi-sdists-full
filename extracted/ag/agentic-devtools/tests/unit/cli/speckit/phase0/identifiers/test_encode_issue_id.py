"""Tests for encode_issue_id in speckit/phase0/identifiers.py (FR-001)."""

from __future__ import annotations

import pytest

from agentic_devtools.cli.speckit.phase0.identifiers import encode_issue_id


class TestEncodeIssueId:
    """Tests for the encode_issue_id function."""

    def test_github_reference_is_mostly_unescaped(self) -> None:
        assert encode_issue_id("owner/repo#123") == "owner/repo#123"

    def test_jira_reference_is_unescaped(self) -> None:
        assert encode_issue_id("PROJ-123") == "PROJ-123"

    def test_literal_percent_is_escaped_first(self) -> None:
        assert encode_issue_id("100%done") == "100%25done"

    def test_disallowed_characters_are_percent_encoded_uppercase(self) -> None:
        assert encode_issue_id("issue with space") == "issue%20with%20space"

    def test_rejects_empty_reference(self) -> None:
        with pytest.raises(ValueError):
            encode_issue_id("")

    def test_markdown_path_reference(self) -> None:
        assert encode_issue_id("docs/issues/42.md") == "docs/issues/42.md"

    def test_rejects_non_string_type(self) -> None:
        with pytest.raises(ValueError):
            encode_issue_id(123)  # type: ignore[arg-type]
