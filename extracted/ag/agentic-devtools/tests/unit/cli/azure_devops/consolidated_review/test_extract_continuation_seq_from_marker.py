"""Tests for extract_continuation_seq_from_marker."""

from agentic_devtools.cli.azure_devops.consolidated_review import (
    build_continuation_marker,
    extract_continuation_seq_from_marker,
)


class TestExtractContinuationSeqFromMarker:
    """Tests for extract_continuation_seq_from_marker."""

    def test_extracts_seq_from_continuation_marker(self):
        content = build_continuation_marker(pr_id=42, commit_hash="a" * 40, sequence=1)
        assert extract_continuation_seq_from_marker(content) == 1

    def test_extracts_seq_3(self):
        content = build_continuation_marker(pr_id=99, commit_hash="b" * 40, sequence=3)
        assert extract_continuation_seq_from_marker(content) == 3

    def test_extracts_seq_from_content_with_surrounding_text(self):
        marker = build_continuation_marker(pr_id=42, commit_hash="c" * 40, sequence=2)
        content = f"{marker}\n### 🔁 Review (continued)\n\nSome body."
        assert extract_continuation_seq_from_marker(content) == 2

    def test_returns_none_for_none_input(self):
        assert extract_continuation_seq_from_marker(None) is None

    def test_returns_none_for_empty_string(self):
        assert extract_continuation_seq_from_marker("") is None

    def test_returns_none_for_plain_comment(self):
        assert extract_continuation_seq_from_marker("Just a regular comment") is None

    def test_returns_none_for_unclosed_marker(self):
        content = "<!-- agdt-review:v2 type:continuation pr:42 seq:1 (unclosed"
        assert extract_continuation_seq_from_marker(content) is None

    def test_returns_none_for_non_integer_seq(self):
        content = "<!-- agdt-review:v2 type:continuation pr:42 seq:abc -->"
        assert extract_continuation_seq_from_marker(content) is None

    def test_returns_none_when_no_seq_field(self):
        """Consolidated markers have no seq: field."""
        content = "<!-- agdt-review:v2 type:consolidated pr:42 commit:abc123 -->"
        assert extract_continuation_seq_from_marker(content) is None

    def test_returns_none_for_v1_marker(self):
        content = "<!-- agdt-review:v1 type:continuation pr:42 seq:1 -->"
        assert extract_continuation_seq_from_marker(content) is None
