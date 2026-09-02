"""Tests for build_continuation_marker."""

from agentic_devtools.cli.azure_devops.consolidated_review import (
    CONSOLIDATED_MARKER_VERSION,
    CONTINUATION_MARKER_TYPE,
    build_continuation_marker,
)


class TestBuildContinuationMarker:
    """Tests for the v2 continuation marker builder."""

    def test_includes_version_type_pr_and_seq(self):
        marker = build_continuation_marker(42, "abc123def456", 1)
        assert f"agdt-review:v{CONSOLIDATED_MARKER_VERSION}" in marker
        assert f"type:{CONTINUATION_MARKER_TYPE}" in marker
        assert "pr:42" in marker
        assert "seq:1" in marker

    def test_includes_commit_when_present(self):
        marker = build_continuation_marker(42, "abc123def456", 2)
        assert "commit:abc123def456" in marker

    def test_omits_commit_when_none(self):
        marker = build_continuation_marker(7, None, 3)
        assert "commit:" not in marker
        assert "seq:3" in marker

    def test_omits_commit_when_empty(self):
        marker = build_continuation_marker(7, "", 1)
        assert "commit:" not in marker

    def test_is_html_comment(self):
        marker = build_continuation_marker(1, "deadbeef", 1)
        assert marker.startswith("<!--")
        assert marker.endswith("-->")
