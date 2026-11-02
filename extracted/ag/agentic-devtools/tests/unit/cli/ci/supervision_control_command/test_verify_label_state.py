"""Tests for the verify_label_state symbol."""

from __future__ import annotations

import pytest

from agentic_devtools.cli.ci.supervision_control import PRObservation
from agentic_devtools.cli.ci.supervision_control_command import verify_label_state


def _observation(number: int, head: str, *labels: str) -> PRObservation:
    return PRObservation(number, head, frozenset(labels))


def test_verify_label_state_raises_on_mismatch() -> None:
    with pytest.raises(RuntimeError, match="label read-back mismatch"):
        verify_label_state({7: frozenset({"a"})}, [_observation(7, "head-7", "b")], {7: "head-7"})


def test_verify_label_state_raises_when_pr_missing_from_observed() -> None:
    with pytest.raises(RuntimeError, match="head read-back mismatch"):
        verify_label_state({7: frozenset({"a"})}, [], {7: "head-7"})


def test_verify_label_state_rejects_a_changed_head_sha() -> None:
    with pytest.raises(RuntimeError, match="head read-back mismatch"):
        verify_label_state({7: frozenset({"a"})}, [_observation(7, "moved", "a")], {7: "head-7"})


def test_verify_label_state_passes_on_exact_match() -> None:
    verify_label_state({7: frozenset({"a"})}, [_observation(7, "head-7", "a")], {7: "head-7"})
