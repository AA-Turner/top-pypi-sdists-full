"""Tests for the latest_valid_checkpoint symbol."""

from __future__ import annotations

import pytest

from agentic_devtools.cli.ci.supervision_control import CONTROL_MARKER, Checkpoint, SupervisionControl
from agentic_devtools.cli.ci.supervision_control_command import latest_valid_checkpoint


def test_latest_valid_checkpoint_returns_most_recent_well_formed_entry() -> None:
    control = SupervisionControl()
    older = control.encode_checkpoint(Checkpoint("run-1", {"step": 1}, "repo"))
    newer = control.encode_checkpoint(Checkpoint("run-2", {"step": 2}, "repo"))

    result = latest_valid_checkpoint(control, ["unrelated", older, newer], "repo")

    assert result == Checkpoint("run-2", {"step": 2}, "repo")


def test_latest_valid_checkpoint_returns_none_when_no_checkpoint_present() -> None:
    control = SupervisionControl()
    assert latest_valid_checkpoint(control, ["unrelated", "also unrelated"], "repo") is None


def test_latest_valid_checkpoint_returns_none_when_only_a_different_repository_checkpoint_exists() -> None:
    control = SupervisionControl()
    other_repo = control.encode_checkpoint(Checkpoint("run-1", {"step": 1}, "other/repo"))

    assert latest_valid_checkpoint(control, [other_repo], "requested/repo") is None


def test_latest_valid_checkpoint_ignores_a_validly_signed_checkpoint_for_a_different_repository() -> None:
    control = SupervisionControl()
    other_repo = control.encode_checkpoint(Checkpoint("run-1", {"step": 1}, "other/repo"))
    matching = control.encode_checkpoint(Checkpoint("run-2", {"step": 2}, "requested/repo"))

    result = latest_valid_checkpoint(control, [other_repo, matching], "requested/repo")

    assert result == Checkpoint("run-2", {"step": 2}, "requested/repo")


def test_latest_valid_checkpoint_skips_malformed_entries() -> None:
    control = SupervisionControl()
    valid = control.encode_checkpoint(Checkpoint("run-1", {"step": 1}, "repo"))
    malformed = f"{CONTROL_MARKER}\nnot-json"

    result = latest_valid_checkpoint(control, [valid, malformed], "repo")

    assert result == Checkpoint("run-1", {"step": 1}, "repo")


def test_latest_valid_checkpoint_rejects_malformed_terminal_label() -> None:
    control = SupervisionControl()
    encoded = control.encode_checkpoint(Checkpoint("run-1", {"step": 1}, "repo"))

    with pytest.raises(ValueError, match="malformed terminal label"):
        latest_valid_checkpoint(control, [f"{encoded}\n🤖 AI PR Loop ·"], "repo")
