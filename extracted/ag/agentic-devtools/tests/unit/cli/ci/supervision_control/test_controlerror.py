"""Tests for the ControlError symbol."""

from __future__ import annotations

from agentic_devtools.cli.ci.supervision_control import ControlError


def test_control_error_is_a_value_error() -> None:
    assert issubclass(ControlError, ValueError)
