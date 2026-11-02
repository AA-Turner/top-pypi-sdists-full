"""Tests for RegistryError."""

from agentic_devtools.cli.setup.registry import RegistryError


class TestRegistryError:
    """Tests for the RegistryError exception type."""

    def test_is_a_runtime_error(self) -> None:
        """RegistryError subclasses RuntimeError for broad except compatibility."""
        assert issubclass(RegistryError, RuntimeError)

    def test_preserves_message(self) -> None:
        """The error message is preserved on the instance."""
        err = RegistryError("boom")
        assert str(err) == "boom"
