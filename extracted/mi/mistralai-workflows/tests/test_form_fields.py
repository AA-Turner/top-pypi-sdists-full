import pytest
from pydantic import ValidationError

from mistralai.workflows.conversational import FormInput, TextField

PATTERN = r"^00\d{8}$"
MESSAGE = "Booking reference must be 00 followed by 8 digits."


class BookingForm(FormInput):
    booking: str = TextField(
        description="Booking reference",
        pattern=PATTERN,
        error_message=MESSAGE,
    )


class UnannotatedBookingForm(FormInput):
    booking: str = TextField(description="Booking reference", pattern=PATTERN)


def test_error_message_is_exposed_to_the_form_ui() -> None:
    schema = BookingForm.model_json_schema()

    assert schema["properties"]["booking"]["errorMessage"] == MESSAGE


def test_error_message_is_absent_when_not_provided() -> None:
    schema = UnannotatedBookingForm.model_json_schema()

    assert "errorMessage" not in schema["properties"]["booking"]
    assert schema["properties"]["booking"]["pattern"] == PATTERN


def test_error_message_does_not_relax_validation() -> None:
    assert BookingForm(booking="0012345678").booking == "0012345678"

    with pytest.raises(ValidationError):
        BookingForm(booking="nope")
