"""Tests for the verify_repo_labels symbol."""

from __future__ import annotations

import pytest

from agentic_devtools.cli.ci.supervision_control_command import verify_repo_labels


def test_verify_repo_labels_raises_when_missing() -> None:
    with pytest.raises(RuntimeError, match="labels missing"):
        verify_repo_labels(frozenset({"a", "b"}), frozenset({"a"}))


def test_verify_repo_labels_passes_when_all_present() -> None:
    verify_repo_labels(frozenset({"a", "b"}), frozenset({"a", "b", "c"}))
