"""Tests for decode_issue_id in speckit/phase0/identifiers.py (FR-001)."""

from __future__ import annotations

from agentic_devtools.cli.speckit.phase0.identifiers import decode_issue_id, encode_issue_id


class TestDecodeIssueId:
    """Tests for the decode_issue_id function."""

    def test_round_trips_github_reference(self) -> None:
        original = "owner/repo#123"
        assert decode_issue_id(encode_issue_id(original)) == original

    def test_round_trips_reference_with_space(self) -> None:
        original = "issue with space"
        assert decode_issue_id(encode_issue_id(original)) == original

    def test_round_trips_literal_percent(self) -> None:
        original = "100%done"
        assert decode_issue_id(encode_issue_id(original)) == original

    def test_round_trips_unicode_reference(self) -> None:
        original = "docs/issues/caf\u00e9.md"
        assert decode_issue_id(encode_issue_id(original)) == original

    def test_decodes_uppercase_hex_escape(self) -> None:
        assert decode_issue_id("issue%20with%20space") == "issue with space"
