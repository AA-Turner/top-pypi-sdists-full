"""Tests for FixAction frozen dataclass."""

from __future__ import annotations

import pytest

from agentic_devtools.cli.setup.fixloop import FixAction


class TestFixAction:
    """Verify FixAction is frozen, slotted, and has correct field types."""

    def test_frozen_immutability(self) -> None:
        action = FixAction(give_up=False, remedy="test", re_exec=True)
        with pytest.raises(AttributeError):
            action.give_up = True  # type: ignore[misc]

    def test_slots(self) -> None:
        action = FixAction(give_up=True, remedy=None, re_exec=False)
        assert hasattr(action, "__slots__")
        with pytest.raises(AttributeError):
            object.__setattr__(action, "extra", "nope")

    def test_field_types(self) -> None:
        action = FixAction(give_up=True, remedy="do something", re_exec=False)
        assert isinstance(action.give_up, bool)
        assert isinstance(action.remedy, str)
        assert isinstance(action.re_exec, bool)

    def test_remedy_none(self) -> None:
        action = FixAction(give_up=False, remedy=None, re_exec=False)
        assert action.remedy is None
