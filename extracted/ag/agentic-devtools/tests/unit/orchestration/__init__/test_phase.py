"""Tests for ``Phase`` re-export from ``agentic_devtools.orchestration``."""

from typing import get_args

from agentic_devtools.orchestration import Phase


def test_phase_is_reexported_from_orchestration() -> None:
    assert set(get_args(Phase)) == {"standard", "heavyweight_checkpoint"}
