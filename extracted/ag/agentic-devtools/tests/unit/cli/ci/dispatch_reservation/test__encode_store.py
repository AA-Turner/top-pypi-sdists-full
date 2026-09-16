from agentic_devtools.cli.ci.dispatch_reservation import DispatchReservation, _encode_store


def test_encodes_one_json_document() -> None:
    reservation = DispatchReservation(
        "owner/repo", 123, "a" * 40, 1, "456-1-a1b2c3d4", "reserved", "2026-08-19T12:34:56.123456Z", 1
    )
    encoded = _encode_store({"key": reservation})
    assert encoded.endswith("\n")
    assert encoded.count("{") == 3
