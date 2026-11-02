"""Unit tests for FR-018 conflict detection and resolution."""

from __future__ import annotations

from agentic_devtools.orchestration.hierarchy.conflicts import (
    ProposedEdit,
    detect_proposed_edit_conflicts,
)


def test_detect_proposed_edit_conflicts_finds_shared_path_edits() -> None:
    edits = [
        ProposedEdit(agent_id="a", path="shared.py", summary="added feature", content="print(1)"),
        ProposedEdit(agent_id="b", path="shared.py", summary="fixed bug", content="print(2)"),
    ]
    detection = detect_proposed_edit_conflicts(edits)
    assert detection is not None
    assert detection.contested_paths == ("shared.py",)
    assert detection.has_proposed_edits
    assert (
        detection.proposed_edit_summaries["shared.py"]["a"]["content_sha256"]
        != detection.proposed_edit_summaries["shared.py"]["b"]["content_sha256"]
    )
    assert detection.proposed_edit_summaries["shared.py"]["a"]["summary"] is None
    assert detection.proposed_edit_summaries["shared.py"]["a"]["summary_sha256"] is not None


def test_detect_proposed_edit_conflicts_none_when_no_overlap() -> None:
    edits = [ProposedEdit(agent_id="a", path="a.py", summary="s", content="x")]
    assert detect_proposed_edit_conflicts(edits) is None
