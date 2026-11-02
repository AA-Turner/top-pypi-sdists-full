"""Tests for agentic_devtools.adapters.exceptions.AdapterError."""

from __future__ import annotations

from agentic_devtools.adapters.exceptions import AdapterError


class TestAdapterError:
    """Tests for the AdapterError base exception class."""

    def test_inherits_from_exception(self) -> None:
        """AdapterError is a subclass of Exception."""
        assert issubclass(AdapterError, Exception)

    def test_message_propagation(self) -> None:
        """AdapterError propagates message through args."""
        err = AdapterError("something went wrong")
        assert str(err) == "something went wrong"
        assert err.args == ("something went wrong",)

    def test_can_be_raised_and_caught(self) -> None:
        """AdapterError can be raised and caught as Exception."""
        try:
            raise AdapterError("test")
        except Exception as exc:
            assert isinstance(exc, AdapterError)
