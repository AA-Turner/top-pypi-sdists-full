"""Tests for the PRObservation symbol."""

from __future__ import annotations

import pytest

from agentic_devtools.cli.ci.supervision_control import PRObservation


def test_pr_observation_requires_positive_number_and_head_sha() -> None:
    with pytest.raises(ValueError, match="positive number"):
        PRObservation(0, "head", frozenset())
    with pytest.raises(ValueError, match="positive number"):
        PRObservation(1, "", frozenset())
