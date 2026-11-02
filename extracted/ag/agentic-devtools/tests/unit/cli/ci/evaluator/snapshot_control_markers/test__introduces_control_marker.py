"""Tests for _introduces_control_marker()."""

import pytest

from agentic_devtools.cli.ci.evaluator.snapshot_control_markers import _introduces_control_marker


class TestIntroducesControlMarker:
    """Detect synthesized trusted markers added by balancing."""

    @pytest.mark.parametrize("kind", ["v2", "work", "exhausted"])
    def test_repair_accounting_markers_cannot_be_synthesized_by_balancing(self, kind):
        original = f"> <!-- repair-dispatch:{kind}:head:10:work"
        assert _introduces_control_marker(original, original + " -->")
        complete = original + " -->"
        assert not _introduces_control_marker(complete, complete)

    def test_returns_true_when_fixed_marker_count_increases(self):
        """A newly completed fixed marker is reported as introduced."""
        original = "<!-- copilot-agent-result\nHEAD: `abc12345`"
        sanitized = "<!-- copilot-agent-result -->\nHEAD: `abc12345`"

        assert _introduces_control_marker(original, sanitized) is True

    def test_returns_true_when_regex_marker_list_changes(self):
        """A newly completed variable-content marker is reported as introduced."""
        original = "> <!-- copilot-trigger:777:2026-08-10T00:00:00+00:00"
        sanitized = "> <!-- copilot-trigger:777:2026-08-10T00:00:00+00:00 -->"

        assert _introduces_control_marker(original, sanitized) is True

    def test_returns_false_when_marker_set_is_unchanged(self):
        """Unchanged trusted markers do not trigger a false positive."""
        body = "<!-- review-id:123 -->\n<!-- copilot-agent-result -->"

        assert _introduces_control_marker(body, body) is False
