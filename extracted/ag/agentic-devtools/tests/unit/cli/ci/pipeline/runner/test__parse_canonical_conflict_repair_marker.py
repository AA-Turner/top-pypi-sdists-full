"""Tests for _parse_canonical_conflict_repair_marker."""

from agentic_devtools.cli.ci.pipeline.runner import _parse_canonical_conflict_repair_marker


class TestParseCanonicalConflictRepairMarker:
    """Tests for canonical conflict-repair dispatch marker parsing."""

    def test_returns_match_for_final_standalone_marker(self) -> None:
        """A final standalone dispatch marker is accepted."""
        body = "\n".join(
            [
                "@copilot repair context",
                "",
                "<!-- agdt:conflict-repair:abc123:def456:2026-09-08T15:17:04+00:00 -->",
            ]
        )

        match = _parse_canonical_conflict_repair_marker(body)

        assert match is not None
        assert match.group(2) == "def456"

    def test_returns_none_for_empty_body(self) -> None:
        """An empty body does not contain a canonical dispatch marker."""
        assert _parse_canonical_conflict_repair_marker("") is None

    def test_returns_none_when_marker_is_not_final_line(self) -> None:
        """A dispatch marker followed by additional text is rejected."""
        body = "\n".join(
            [
                "<!-- agdt:conflict-repair:abc123:def456:2026-09-08T15:17:04+00:00 -->",
                "trailing context",
            ]
        )

        assert _parse_canonical_conflict_repair_marker(body) is None
