"""Tests for ChildInfo dataclass including order field (FR-010)."""

from agentic_devtools.hierarchy.models import ChildInfo


class TestChildInfo:
    """Tests for ChildInfo serialization and order field."""

    def test_to_dict_without_order(self) -> None:
        """ChildInfo without order serializes without order key."""
        child = ChildInfo(number=42, title="My Issue")
        result = child.to_dict()
        assert result == {"number": 42, "title": "My Issue"}
        assert "order" not in result

    def test_to_dict_with_order(self) -> None:
        """ChildInfo with order includes it in serialization."""
        child = ChildInfo(number=42, title="My Issue", order=3)
        result = child.to_dict()
        assert result == {"number": 42, "title": "My Issue", "order": 3}

    def test_order_defaults_to_none(self) -> None:
        """Order field defaults to None."""
        child = ChildInfo(number=1, title="Test")
        assert child.order is None

    def test_order_zero_is_valid(self) -> None:
        """Order of 0 is a valid value."""
        child = ChildInfo(number=1, title="Test", order=0)
        assert child.order == 0
        assert child.to_dict()["order"] == 0
