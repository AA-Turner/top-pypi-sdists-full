"""Tests for the Checkpoint symbol."""

from __future__ import annotations

from agentic_devtools.cli.ci.supervision_control import Checkpoint


def test_checkpoint_retains_its_serialized_fields() -> None:
    checkpoint = Checkpoint("run-1", {"selected": [7]}, "owner/repo")

    assert checkpoint == Checkpoint("run-1", {"selected": [7]}, "owner/repo")
