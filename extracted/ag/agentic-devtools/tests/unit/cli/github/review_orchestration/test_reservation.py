import pytest
from pydantic import ValidationError

from agentic_devtools.cli.github.review_orchestration import Reservation


def test_reservation_is_immutable(reserve):
    reservation = Reservation.model_validate(reserve()["reservations"][0])
    with pytest.raises(ValidationError):
        reservation.attempt_id = "replacement"


def test_requires_complete_reservation_identity():
    with pytest.raises(ValidationError):
        Reservation.model_validate({"finding_id": "f" * 64})
