"""Tests for extract_commit_hash_from_marker."""

from agentic_devtools.cli.azure_devops.consolidated_review import (
    build_consolidated_marker,
    build_continuation_marker,
    build_model_reply_marker,
    extract_commit_hash_from_marker,
)


class TestExtractCommitHashFromMarker:
    """Tests for extract_commit_hash_from_marker."""

    def test_extracts_sha_from_consolidated_marker(self):
        content = build_consolidated_marker(pr_id=42, commit_hash="abc1234567890")
        assert extract_commit_hash_from_marker(content) == "abc1234567890"

    def test_extracts_sha_from_continuation_marker(self):
        content = build_continuation_marker(pr_id=42, commit_hash="def9876543210", sequence=1)
        assert extract_commit_hash_from_marker(content) == "def9876543210"

    def test_extracts_sha_from_model_reply_marker(self):
        content = build_model_reply_marker(pr_id=42, commit_hash="feedcafe1234", model_id="gpt-5")
        assert extract_commit_hash_from_marker(content) == "feedcafe1234"

    def test_extracts_sha_from_content_with_surrounding_text(self):
        marker = build_consolidated_marker(pr_id=42, commit_hash="aabbcc112233")
        content = f"{marker}\n# PR Review\n\nSome body text."
        assert extract_commit_hash_from_marker(content) == "aabbcc112233"

    def test_returns_none_when_no_commit_field(self):
        """Markers omit commit: when commit_hash is None."""
        content = build_consolidated_marker(pr_id=42, commit_hash=None)
        assert extract_commit_hash_from_marker(content) is None

    def test_returns_none_for_none_input(self):
        assert extract_commit_hash_from_marker(None) is None

    def test_returns_none_for_empty_string(self):
        assert extract_commit_hash_from_marker("") is None

    def test_returns_none_for_plain_comment(self):
        assert extract_commit_hash_from_marker("Just a regular comment") is None

    def test_returns_none_for_v1_marker(self):
        content = "<!-- agdt-review:v1 type:overall-summary pr:42 -->"
        assert extract_commit_hash_from_marker(content) is None

    def test_returns_none_for_unclosed_marker(self):
        """Marker prefix present but missing the closing --> sentinel."""
        content = "<!-- agdt-review:v2 type:consolidated pr:42 commit:abc1234 (unclosed"
        assert extract_commit_hash_from_marker(content) is None
