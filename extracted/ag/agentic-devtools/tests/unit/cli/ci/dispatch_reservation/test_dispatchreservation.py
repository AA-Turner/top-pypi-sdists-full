from dataclasses import fields

import pytest

from agentic_devtools.cli.ci.dispatch_reservation import DispatchReservation


def _reservation(**changes: object) -> DispatchReservation:
    values: dict[str, object] = {
        "repo": "owner/repo",
        "pull_request_id": 123,
        "sha": "a" * 40,
        "ordinal": 1,
        "owner": "456-1-a1b2c3d4",
        "state": "reserved",
        "created_at": "2026-08-19T12:34:56.123456Z",
        "schema_version": 1,
    }
    values.update(changes)
    return DispatchReservation(**values)  # type: ignore[arg-type]


def test_round_trips_closed_schema() -> None:
    reservation = _reservation()

    assert len(fields(reservation)) == 8
    assert DispatchReservation.from_dict(reservation.to_dict()) == reservation


@pytest.mark.parametrize(
    "changes",
    [
        {"repo": "repo"},
        {"pull_request_id": True},
        {"pull_request_id": 1.0},
        {"pull_request_id": 0},
        {"sha": "A" * 40},
        {"ordinal": 4},
        {"ordinal": 1.0},
        {"ordinal": True},
        {"owner": "run-attempt-a1b2c3d4"},
        {"state": "created"},
        {"created_at": "2026-08-19T12:34:56Z"},
        {"created_at": "2026-13-19T12:34:56.123456Z"},
        {"schema_version": 2},
        {"schema_version": 1.0},
        {"schema_version": True},
    ],
)
def test_rejects_invalid_fields(changes: dict[str, object]) -> None:
    with pytest.raises(ValueError):
        _reservation(**changes)


def test_rejects_unknown_or_missing_serialized_fields() -> None:
    payload = _reservation().to_dict()
    payload.pop("owner")
    with pytest.raises(ValueError):
        DispatchReservation.from_dict(payload)

    payload = _reservation().to_dict()
    payload["extra"] = "not allowed"
    with pytest.raises(ValueError):
        DispatchReservation.from_dict(payload)
