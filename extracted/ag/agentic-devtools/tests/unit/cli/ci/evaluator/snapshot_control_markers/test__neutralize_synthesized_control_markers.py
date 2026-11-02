"""Tests for _neutralize_synthesized_control_markers()."""

from agentic_devtools.cli.ci.evaluator.snapshot_control_markers import _neutralize_synthesized_control_markers


class TestNeutralizeSynthesizedControlMarkers:
    """Escape synthesized trusted markers while leaving other text unchanged."""

    def test_returns_original_body_when_inserted_position_has_no_opener(self):
        """A stray insertion offset with no preceding opener is ignored safely."""
        body = "plain text"

        assert _neutralize_synthesized_control_markers(body, (0,)) == body

    def test_escapes_a_synthesized_control_marker(self):
        """Escapes a trusted marker whose closing delimiter was inserted."""
        body = "<!-- copilot-agent-result -->"
        inserted_at = len(body) - 4

        assert _neutralize_synthesized_control_markers(body, (inserted_at,)) == "&lt;!-- copilot-agent-result -->"

    def test_escapes_a_synthesized_regex_marker(self):
        """Escapes a trusted variable-content marker recognized by its regex."""
        body = "<!-- review-id:123 -->"
        inserted_at = len(body) - 4

        assert _neutralize_synthesized_control_markers(body, (inserted_at,)) == "&lt;!-- review-id:123 -->"

    def test_leaves_untrusted_markers_unchanged(self):
        """Does not escape a marker that is not trusted control content."""
        body = "<!-- ordinary text -->"
        inserted_at = len(body) - 4

        assert _neutralize_synthesized_control_markers(body, (inserted_at,)) == body
