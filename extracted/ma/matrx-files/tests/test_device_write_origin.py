"""Device provenance on a write is VALIDATED, never taken on trust (§2.2).

`origin_device_id` is the field a daemon uses to decide "this change is my own
echo, skip it". If the server stored whatever a client sent, one account's row
could claim another account's machine and that other machine would then skip a
change it had never made. And a skewed client clock is a named state ON THE
CLIENT -- never a poisoned timestamp in the database.

Bare-venv friendly: the DB-backed ownership check has its own live test in
test_sync_feed_v2_shape.py; everything here is pure parsing.
"""

from __future__ import annotations

from datetime import UTC, datetime, timedelta

import pytest

from matrx_files.cloud_sync.device_writes import (
    MAX_CLIENT_CLOCK_SKEW,
    DeviceWriteError,
    parse_client_modified_at,
    parse_device_id,
    reconcile_header_and_metadata,
)

NOW = datetime(2026, 9, 13, 12, 0, 0, tzinfo=UTC)
DEVICE = "22222222-2222-2222-2222-222222222222"


def test_absent_values_are_absent_not_errors():
    assert parse_device_id(None) is None
    assert parse_device_id("  ") is None
    assert parse_client_modified_at(None) is None


def test_a_device_id_must_be_the_app_instances_uuid():
    assert parse_device_id(f" {DEVICE} ") == DEVICE
    with pytest.raises(DeviceWriteError) as exc:
        parse_device_id("my-laptop")
    assert exc.value.code == "invalid_device"
    assert "app_instances.id" in exc.value.message, "the error must name the right identity"


def test_client_time_must_carry_an_offset():
    """A naive timestamp is ambiguous and guessing UTC silently shifts conflicts."""
    with pytest.raises(DeviceWriteError) as exc:
        parse_client_modified_at("2026-09-13T10:00:00")
    assert exc.value.code == "invalid_client_time"


def test_client_time_is_normalised_to_utc():
    got = parse_client_modified_at("2026-09-13T05:00:00-07:00", now=NOW)
    assert got == datetime(2026, 9, 13, 12, 0, 0, tzinfo=UTC)


def test_a_far_future_clock_is_refused_not_stored():
    ahead = (NOW + MAX_CLIENT_CLOCK_SKEW + timedelta(minutes=1)).isoformat()
    with pytest.raises(DeviceWriteError) as exc:
        parse_client_modified_at(ahead, now=NOW)
    assert exc.value.code == "implausible_client_time"
    assert "clock" in exc.value.message


def test_a_slightly_ahead_clock_is_accepted():
    """Ordinary skew is normal; the feed orders by the server clock anyway."""
    ok = (NOW + timedelta(hours=23)).isoformat()
    assert parse_client_modified_at(ok, now=NOW) is not None


def test_the_header_wins_over_tus_metadata_and_a_mismatch_is_refused():
    assert reconcile_header_and_metadata(name="d", header_value=DEVICE, metadata_value=None) == DEVICE
    assert reconcile_header_and_metadata(name="d", header_value=None, metadata_value=DEVICE) == DEVICE
    assert (
        reconcile_header_and_metadata(name="d", header_value=DEVICE, metadata_value=DEVICE) == DEVICE
    )
    with pytest.raises(DeviceWriteError) as exc:
        reconcile_header_and_metadata(name="d", header_value=DEVICE, metadata_value="other")
    assert exc.value.code == "conflicting_origin_metadata", (
        "silently picking one of two disagreeing values attributes a file to the "
        "wrong machine with nothing in any log to say why"
    )
