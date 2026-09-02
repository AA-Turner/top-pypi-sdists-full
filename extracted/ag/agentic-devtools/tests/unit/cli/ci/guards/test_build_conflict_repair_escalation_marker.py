"""Tests for build_conflict_repair_escalation_marker() guard helper."""

from agentic_devtools.cli.ci.guards import (
    CONFLICT_REPAIR_ESCALATION_MARKER_PREFIX,
    CONFLICT_REPAIR_MARKER_PREFIX,
    build_conflict_repair_escalation_marker,
)

_HEAD = "abc" * 13 + "a"  # 40-char hex-like head SHA


class TestBuildConflictRepairEscalationMarker:
    """Tests for the human-escalation marker builder."""

    def test_embeds_head_sha(self) -> None:
        """The marker embeds the HEAD SHA it escalates for."""
        marker = build_conflict_repair_escalation_marker(head_sha=_HEAD)

        assert marker == f"{CONFLICT_REPAIR_ESCALATION_MARKER_PREFIX}{_HEAD} -->"

    def test_does_not_match_dispatch_marker_prefix(self) -> None:
        """The escalation marker never matches the dispatch-marker prefix search."""
        marker = build_conflict_repair_escalation_marker(head_sha=_HEAD)

        assert CONFLICT_REPAIR_MARKER_PREFIX not in marker
