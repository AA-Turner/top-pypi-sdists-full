"""Tests for the find_published_checkpoint symbol."""

from __future__ import annotations

import pytest

from agentic_devtools.cli.ci.supervision_control import CONTROL_MARKER, Checkpoint, ControlError, SupervisionControl
from agentic_devtools.cli.ci.supervision_control_command import find_published_checkpoint


def test_find_published_checkpoint_returns_matching_run() -> None:
    control = SupervisionControl()
    encoded = control.encode_checkpoint(Checkpoint("run-1", {"step": 1}, "repo"))

    result = find_published_checkpoint(control, encoded, ["unrelated", encoded], "repo")

    assert result == Checkpoint("run-1", {"step": 1}, "repo")


def test_find_published_checkpoint_rejects_a_matching_run_id_from_a_different_repository() -> None:
    control = SupervisionControl()
    cross_repo = control.encode_checkpoint(Checkpoint("run-1", {"step": 1}, "other/repo"))

    with pytest.raises(RuntimeError, match="did not find"):
        find_published_checkpoint(
            control,
            control.encode_checkpoint(Checkpoint("run-1", {}, "requested/repo")),
            [cross_repo],
            "requested/repo",
        )


def test_find_published_checkpoint_rejects_repository_mismatch() -> None:
    control = SupervisionControl()
    encoded = control.encode_checkpoint(Checkpoint("run-1", {}, "other/repo"))

    with pytest.raises(RuntimeError, match="repository does not match"):
        find_published_checkpoint(control, encoded, [encoded], "requested/repo")


@pytest.mark.parametrize("decoded_matches", [False, "invalid"])
def test_find_published_checkpoint_rejects_a_nonmatching_exact_read_back(decoded_matches: bool | str) -> None:
    encoded = SupervisionControl().encode_checkpoint(Checkpoint("run-1", {}, "repo"))

    class ChangingControl:
        calls = 0

        def decode_checkpoint(self, _body: str) -> Checkpoint:
            self.calls += 1
            if self.calls == 1:
                return Checkpoint("run-1", {}, "repo")
            if decoded_matches == "invalid":
                raise ControlError("malformed checkpoint")
            return Checkpoint("run-1", {"different": True}, "repo")

    with pytest.raises(RuntimeError, match="exact published payload"):
        find_published_checkpoint(ChangingControl(), encoded, [encoded], "repo")  # type: ignore[arg-type]


def test_find_published_checkpoint_skips_malformed_and_mismatched_entries() -> None:
    control = SupervisionControl()
    other_run = control.encode_checkpoint(Checkpoint("run-2", {"step": 1}, "repo"))
    malformed = f"{CONTROL_MARKER}\nnot-json"

    with pytest.raises(RuntimeError, match="did not find"):
        find_published_checkpoint(
            control,
            control.encode_checkpoint(Checkpoint("run-1", {}, "repo")),
            [malformed, other_run, "unrelated"],
            "repo",
        )


def test_find_published_checkpoint_rejects_malformed_terminal_label() -> None:
    control = SupervisionControl()
    encoded = control.encode_checkpoint(Checkpoint("run-1", {}, "repo"))

    with pytest.raises(RuntimeError, match="payload has a malformed terminal label"):
        find_published_checkpoint(control, f"{encoded}\n🤖 AI PR Loop ·", [encoded], "repo")
