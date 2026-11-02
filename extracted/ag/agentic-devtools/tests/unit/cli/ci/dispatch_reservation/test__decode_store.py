import json

import pytest

from agentic_devtools.cli.ci.dispatch_reservation import DispatchReservation, _decode_store, _encode_store, _request_key


def _reservation() -> DispatchReservation:
    return DispatchReservation(
        "owner/repo", 123, "a" * 40, 1, "456-1-a1b2c3d4", "reserved", "2026-08-19T12:34:56.123456Z", 1
    )


def test_empty_store_is_empty() -> None:
    assert _decode_store(" \n") == {}


def test_decodes_valid_store() -> None:
    reservation = _reservation()
    key = _request_key(reservation.repo, reservation.pull_request_id, reservation.sha, reservation.ordinal)
    assert _decode_store(_encode_store({key: reservation})) == {key: reservation}


@pytest.mark.parametrize(
    "content",
    [
        "not json",
        "[]",
        '{"schema_version": 2, "reservations": {}}',
        '{"schema_version": true, "reservations": {}}',
        '{"schema_version": 1.0, "reservations": {}}',
    ],
)
def test_rejects_invalid_store_schema(content: str) -> None:
    with pytest.raises(ValueError):
        _decode_store(content)


def test_rejects_non_object_reservations() -> None:
    with pytest.raises(ValueError, match="reservations"):
        _decode_store(json.dumps({"schema_version": 1, "reservations": []}))


def test_rejects_invalid_record() -> None:
    with pytest.raises(ValueError, match="invalid record"):
        _decode_store(json.dumps({"schema_version": 1, "reservations": {"key": []}}))
