"""Tests for _parse_canonical_validated_marker."""

from agentic_devtools.cli.ci.pipeline.runner import _parse_canonical_validated_marker


class TestParseCanonicalValidatedMarker:
    """Tests for canonical conflict-repair validation marker parsing."""

    def test_returns_match_for_full_body_marker(self) -> None:
        """A validated marker is accepted only when it is the whole body."""
        match = _parse_canonical_validated_marker("<!-- agdt:conflict-repair-validated:feedbeef -->")

        assert match is not None
        assert match.group(1) == "feedbeef"

    def test_returns_none_for_empty_body(self) -> None:
        """An empty body does not contain a canonical validated marker."""
        assert _parse_canonical_validated_marker("") is None

    def test_returns_none_when_body_contains_surrounding_text(self) -> None:
        """A validated marker embedded in other text is rejected."""
        body = "\n".join(
            [
                "@copilot context",
                "<!-- agdt:conflict-repair-validated:feedbeef -->",
            ]
        )

        assert _parse_canonical_validated_marker(body) is None
