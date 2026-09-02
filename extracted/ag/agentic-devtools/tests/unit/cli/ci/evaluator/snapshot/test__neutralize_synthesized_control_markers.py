"""Tests for _neutralize_synthesized_control_markers()."""

from agentic_devtools.cli.ci.evaluator.snapshot import _neutralize_synthesized_control_markers


class TestNeutralizeSynthesizedControlMarkers:
    """Escape synthesized trusted markers while leaving other text unchanged."""

    def test_returns_original_body_when_inserted_position_has_no_opener(self):
        """A stray insertion offset with no preceding opener is ignored safely."""
        body = "plain text"

        assert _neutralize_synthesized_control_markers(body, (0,)) == body
