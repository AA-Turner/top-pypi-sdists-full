"""Tests for DispatchEvent dataclass."""

from agentic_devtools.cli.ci.scheduler import DispatchEvent


class TestDispatchEvent:
    """Tests for the DispatchEvent frozen dataclass."""

    def test_create_instance(self) -> None:
        event = DispatchEvent(pr_number=2020, created_at="2024-01-01T00:00:00Z")
        assert event.pr_number == 2020
        assert event.created_at == "2024-01-01T00:00:00Z"

    def test_frozen(self) -> None:
        event = DispatchEvent(pr_number=2020, created_at="2024-01-01T00:00:00Z")
        import pytest

        with pytest.raises(AttributeError):
            event.pr_number = 2021  # type: ignore[misc]
