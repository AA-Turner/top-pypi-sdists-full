"""Tests for build_conflict_repair_marker() in guards."""

from agentic_devtools.cli.ci.guards import (
    CONFLICT_REPAIR_MARKER_PREFIX,
    build_conflict_repair_marker,
)


class TestBuildConflictRepairMarker:
    """Tests for build_conflict_repair_marker()."""

    def test_starts_with_marker_prefix(self) -> None:
        """Result must begin with CONFLICT_REPAIR_MARKER_PREFIX."""
        result = build_conflict_repair_marker(base_sha="b" * 40, head_sha="a" * 40)
        assert result.startswith(CONFLICT_REPAIR_MARKER_PREFIX)

    def test_embeds_base_and_head_sha(self) -> None:
        """Result must embed both the base_sha and head_sha."""
        base = "b" * 40
        head = "a" * 40
        result = build_conflict_repair_marker(base_sha=base, head_sha=head)
        assert base in result
        assert head in result

    def test_result_is_html_comment(self) -> None:
        """Result must be a well-formed HTML comment."""
        result = build_conflict_repair_marker(base_sha="1" * 40, head_sha="2" * 40)
        assert result.startswith("<!--")
        assert result.endswith("-->")
