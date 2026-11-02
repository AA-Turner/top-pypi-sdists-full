"""Tests for BlockedState."""

from agentic_devtools.models.git_results import BlockedState


class TestBlockedState:
    """Tests for BlockedState dataclass."""

    def test_stores_category_message_and_default_details(self):
        """BlockedState stores required fields and defaults details to None."""
        result = BlockedState(category="transient", message="Network unavailable")

        assert result.category == "transient"
        assert result.message == "Network unavailable"
        assert result.details is None

    def test_stores_optional_details(self):
        """BlockedState stores optional detail strings."""
        result = BlockedState(category="conflict", message="Merge conflict", details=["src/app.py"])

        assert result.details == ["src/app.py"]
