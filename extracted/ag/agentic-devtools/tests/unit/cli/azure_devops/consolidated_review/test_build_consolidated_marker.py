"""Tests for build_consolidated_marker."""

from agentic_devtools.cli.azure_devops.consolidated_review import (
    CONSOLIDATED_MARKER_TYPE,
    CONSOLIDATED_MARKER_VERSION,
    build_consolidated_marker,
)


class TestBuildConsolidatedMarker:
    """Tests for the v2 consolidated-review marker builder."""

    def test_includes_version_type_and_pr(self):
        """Marker carries the v2 version, consolidated type, and PR id."""
        marker = build_consolidated_marker(42, "abc123def456")
        assert f"agdt-review:v{CONSOLIDATED_MARKER_VERSION}" in marker
        assert f"type:{CONSOLIDATED_MARKER_TYPE}" in marker
        assert "pr:42" in marker

    def test_includes_full_commit_sha(self):
        """The full commit SHA is embedded for self-describing recovery."""
        sha = "4a8685bda246f3bf826efabaf990fe9c3d1da125"
        marker = build_consolidated_marker(28838, sha)
        assert f"commit:{sha}" in marker

    def test_omits_commit_when_none(self):
        """No commit key is emitted when the SHA is None."""
        marker = build_consolidated_marker(7, None)
        assert "commit:" not in marker
        assert "pr:7" in marker

    def test_omits_commit_when_empty(self):
        """No commit key is emitted when the SHA is an empty string."""
        marker = build_consolidated_marker(7, "")
        assert "commit:" not in marker

    def test_is_html_comment(self):
        """Marker is wrapped as an HTML comment so it is invisible in rendered markdown."""
        marker = build_consolidated_marker(1, "deadbeef")
        assert marker.startswith("<!--")
        assert marker.endswith("-->")

    def test_version_is_two(self):
        """The consolidated marker version is 2 (distinct from legacy v1)."""
        assert CONSOLIDATED_MARKER_VERSION == 2
        assert CONSOLIDATED_MARKER_TYPE == "consolidated"
