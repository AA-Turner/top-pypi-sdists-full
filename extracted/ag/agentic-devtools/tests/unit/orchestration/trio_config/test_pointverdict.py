"""Tests for ``PointVerdict``."""

import pytest

from agentic_devtools.orchestration.trio_config import PointVerdict


def test_pointverdict_rejects_invalid_values() -> None:
    with pytest.raises(ValueError):
        PointVerdict("", "ACCEPT", "evidence")  # type: ignore[arg-type]
    with pytest.raises(ValueError):
        PointVerdict("p", "UNKNOWN", "evidence")  # type: ignore[arg-type]
    with pytest.raises(ValueError):
        PointVerdict("p", "ACCEPT", "")  # type: ignore[arg-type]


def test_pointverdict_accepted_is_true_for_accepting_verdicts() -> None:
    assert PointVerdict("x", "ACCEPT", "evidence").accepted
