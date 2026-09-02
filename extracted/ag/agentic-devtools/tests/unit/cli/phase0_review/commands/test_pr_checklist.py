"""Tests for Phase 0 PR checklist injection."""

from agentic_devtools.cli.phase0_review.commands import inject_phase0_checklist


def test_checklist_is_phase0_only_complete_and_idempotent():
    phase0 = inject_phase0_checklist("Body", 0)
    for word in ("Title", "Description", "Labels", "Type", "Properties", "Template compliance"):
        assert word in phase0
    assert "out of scope" in phase0
    assert inject_phase0_checklist(phase0, "phase 0") == phase0
    assert inject_phase0_checklist("", "0").startswith("## Phase 0")
    for phase in range(1, 6):
        assert inject_phase0_checklist("Body", phase) == "Body"
