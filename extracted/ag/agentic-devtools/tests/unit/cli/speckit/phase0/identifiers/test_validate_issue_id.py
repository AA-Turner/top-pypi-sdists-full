"""Tests for validate_issue_id in speckit/phase0/identifiers.py (FR-001)."""

from __future__ import annotations

from agentic_devtools.cli.speckit.phase0.identifiers import encode_issue_id, validate_issue_id


class TestValidateIssueId:
    """Tests for the validate_issue_id function."""

    def test_accepts_encoded_github_reference(self) -> None:
        assert validate_issue_id(encode_issue_id("owner/repo#123")) is True

    def test_accepts_well_formed_percent_escape(self) -> None:
        assert validate_issue_id("issue%20with%20space") is True

    def test_rejects_empty_string(self) -> None:
        assert validate_issue_id("") is False

    def test_rejects_raw_space(self) -> None:
        assert validate_issue_id("has space") is False

    def test_rejects_malformed_percent_escape(self) -> None:
        assert validate_issue_id("bad%2") is False

    def test_rejects_invalid_utf8_percent_escape(self) -> None:
        assert validate_issue_id("%FF") is False

    def test_rejects_disallowed_character(self) -> None:
        assert validate_issue_id('has"quote') is False

    def test_rejects_trailing_newline(self) -> None:
        assert validate_issue_id("owner/repo#1\n") is False
