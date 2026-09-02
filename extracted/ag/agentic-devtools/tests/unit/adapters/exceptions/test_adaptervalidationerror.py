"""Tests for agentic_devtools.adapters.exceptions.AdapterValidationError."""

from __future__ import annotations

from agentic_devtools.adapters.exceptions import AdapterError, AdapterValidationError


class TestAdapterValidationError:
    """Tests for the AdapterValidationError exception class."""

    def test_inherits_from_adapter_error(self) -> None:
        """AdapterValidationError is a subclass of AdapterError."""
        assert issubclass(AdapterValidationError, AdapterError)

    def test_inherits_from_exception(self) -> None:
        """AdapterValidationError is also a subclass of Exception."""
        assert issubclass(AdapterValidationError, Exception)

    def test_message_propagation(self) -> None:
        """AdapterValidationError propagates message through args."""
        err = AdapterValidationError("field is empty")
        assert str(err) == "field is empty"
        assert err.args == ("field is empty",)

    def test_can_be_caught_as_adapter_error(self) -> None:
        """AdapterValidationError can be caught as AdapterError."""
        try:
            raise AdapterValidationError("validation failed")
        except AdapterError as exc:
            assert isinstance(exc, AdapterValidationError)
