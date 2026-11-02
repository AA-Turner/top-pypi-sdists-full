"""Tests for the verify_complete_workflow_set symbol."""

from __future__ import annotations

import pytest

from agentic_devtools.cli.ci.supervision_control_command import LOOP_WORKFLOW_FILES, verify_complete_workflow_set


def test_verify_complete_workflow_set_passes_when_all_required_present() -> None:
    verify_complete_workflow_set(dict.fromkeys(LOOP_WORKFLOW_FILES, True))


def test_verify_complete_workflow_set_raises_on_missing_evidence() -> None:
    incomplete = dict.fromkeys(LOOP_WORKFLOW_FILES, True)
    del incomplete[next(iter(LOOP_WORKFLOW_FILES))]

    with pytest.raises(RuntimeError, match="incomplete workflow evidence"):
        verify_complete_workflow_set(incomplete)
