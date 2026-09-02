"""Tests for ChildRef dataclass in nest/discovery.py."""

from __future__ import annotations

from agentic_devtools.cli.speckit.nest.discovery import ChildRef


class TestChildRef:
    """Tests for the ChildRef dataclass."""

    def test_stores_fields_with_order(self) -> None:
        """Fields including order are accessible."""
        ref = ChildRef(number=10, title="My issue", order=3)
        assert ref.number == 10
        assert ref.title == "My issue"
        assert ref.order == 3

    def test_order_defaults_to_none(self) -> None:
        """order defaults to None when not supplied."""
        ref = ChildRef(number=5, title="No order")
        assert ref.order is None

    def test_frozen_equality(self) -> None:
        """Two identical ChildRef instances are equal (frozen dataclass)."""
        assert ChildRef(number=1, title="t", order=0) == ChildRef(number=1, title="t", order=0)

    def test_hashable(self) -> None:
        """ChildRef instances can be placed in a set."""
        refs = {ChildRef(number=1, title="a"), ChildRef(number=2, title="b")}
        assert len(refs) == 2
