"""Tests for _marker_excerpt_within_limit in retro_spec/synthesis.py."""

from __future__ import annotations

from agentic_devtools.cli.speckit.retro_spec.synthesis import _marker_excerpt_within_limit


class TestMarkerExcerptWithinLimit:
    """Tests for the _marker_excerpt_within_limit helper."""

    def test_returns_compact_marker_excerpt_within_limit(self) -> None:
        """Non-adjacent marker lines are compacted into a bounded excerpt."""
        body = (
            "intro\n"
            + "x\n" * 200
            + "### Functional Requirements\n"
            + "- FR-001\n"
            + "y\n" * 200
            + "### Non-Functional Requirements\n"
            + "- NFR-001\n"
        )

        result = _marker_excerpt_within_limit(
            body,
            ["### Functional Requirements", "### Non-Functional Requirements"],
            120,
        )

        assert len(result) <= 120
        assert "### Functional Requirements" in result
        assert "### Non-Functional Requirements" in result

    def test_returns_empty_when_limit_is_zero(self) -> None:
        """A zero limit yields an empty excerpt."""
        assert _marker_excerpt_within_limit("### Functional Requirements\n", ["### Functional Requirements"], 0) == ""

    def test_falls_back_to_generic_cap_when_no_markers_are_requested(self) -> None:
        """An empty marker list delegates to the generic cap path."""
        body = "abcdefghijklmnopqrstuvwxyz"

        result = _marker_excerpt_within_limit(body, [], 10)

        assert len(result) <= 10
        assert result == body[:10]

    def test_falls_back_to_generic_cap_when_requested_markers_are_absent(self) -> None:
        """A non-empty marker list still falls back when the body contains no matches."""
        body = "abcdefghijklmnopqrstuvwxyz"

        result = _marker_excerpt_within_limit(body, ["### Functional Requirements"], 10)

        assert len(result) <= 10
        assert result == body[:10]

    def test_truncates_first_marker_line_when_it_exceeds_limit(self) -> None:
        """The first marker line is clipped when it alone exceeds the remaining budget."""
        body = "### Functional Requirements with extra detail that will not fit\n"

        result = _marker_excerpt_within_limit(body, ["### Functional Requirements"], 12)

        assert result == body[:12]

    def test_skips_missing_markers_before_collecting_present_ones(self) -> None:
        """Missing markers are ignored without preventing later matches from being used."""
        body = "preamble\n### Functional Requirements\n"

        result = _marker_excerpt_within_limit(
            body,
            ["### Missing Marker", "### Functional Requirements"],
            80,
        )

        assert result == "### Functional Requirements\n"

    def test_stops_before_marker_that_would_overflow_after_prior_excerpt(self) -> None:
        """Once one marker fits, later overflowing markers are omitted instead of exceeding the cap."""
        body = "### Functional Requirements\n### Non-Functional Requirements\n"

        result = _marker_excerpt_within_limit(
            body,
            ["### Functional Requirements", "### Non-Functional Requirements"],
            len("### Functional Requirements\n") + 5,
        )

        assert result == "### Functional Requirements\n"
