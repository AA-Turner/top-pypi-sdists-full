"""Feed v2's device provenance, checked against the live device registry (§2.2).

`origin_device_id` is the field a daemon uses to decide "this change is my own
echo, skip it". If the server stored whatever a client sent, one account's row
could claim another account's machine -- and that machine would then skip a
change it had never made. So ownership is checked against
``public.app_instances`` on every write, and the checks here run against the
real table rather than a double.

Marked ``integration``: SELECT only, no row is written.
"""

from __future__ import annotations

import os
from datetime import UTC, datetime, timedelta

import pytest

from matrx_files.cloud_sync.device_writes import DeviceWriteError, resolve_write_origin

pytestmark = [pytest.mark.integration, pytest.mark.asyncio]

_REQUIRED_ENV = ("SUPABASE_MATRIX_HOST", "SUPABASE_MATRIX_PASSWORD")
_NOBODY = "00000000-0000-0000-0000-0000000000ff"


def _skip_without_db() -> None:
    missing = [n for n in _REQUIRED_ENV if not os.environ.get(n)]
    if missing:
        pytest.skip(f"live platform database unavailable: {', '.join(missing)} unset")


async def _a_real_device() -> tuple[str, str]:
    """(device_id, its owner) from the live registry."""
    from matrx_orm import acquire_connection

    from matrx_files.db import bootstrap_db

    async with acquire_connection(bootstrap_db()) as conn:
        row = await conn.fetchrow(
            "SELECT id::text AS id, user_id::text AS user_id FROM public.app_instances "
            "WHERE deleted_at IS NULL LIMIT 1"
        )
    if row is None:
        pytest.skip("no registered devices on this database")
    return row["id"], row["user_id"]


async def test_a_device_owned_by_the_caller_is_accepted():
    _skip_without_db()
    device_id, owner = await _a_real_device()
    origin = await resolve_write_origin(
        user_id=owner, device_id=device_id, client_modified_at=None
    )
    assert origin.device_id == device_id


async def test_another_users_device_is_never_stored():
    _skip_without_db()
    device_id, _owner = await _a_real_device()
    with pytest.raises(DeviceWriteError) as exc:
        await resolve_write_origin(
            user_id=_NOBODY, device_id=device_id, client_modified_at=None
        )
    assert exc.value.code == "invalid_device"
    assert "different user" in exc.value.message


async def test_an_unregistered_device_is_refused_with_the_remedy():
    _skip_without_db()
    with pytest.raises(DeviceWriteError) as exc:
        await resolve_write_origin(
            user_id=_NOBODY,
            device_id="11111111-2222-3333-4444-555555555555",
            client_modified_at=None,
        )
    assert exc.value.code == "invalid_device"
    assert "Register the device" in exc.value.message


async def test_a_future_client_clock_is_refused_before_any_device_lookup():
    _skip_without_db()
    device_id, owner = await _a_real_device()
    ahead = (datetime.now(UTC) + timedelta(days=3)).isoformat()
    with pytest.raises(DeviceWriteError) as exc:
        await resolve_write_origin(
            user_id=owner, device_id=device_id, client_modified_at=ahead
        )
    assert exc.value.code == "implausible_client_time"


async def test_an_empty_origin_is_simply_empty():
    """A browser upload declares nothing and is not an error."""
    _skip_without_db()
    origin = await resolve_write_origin(
        user_id=_NOBODY, device_id=None, client_modified_at=None
    )
    assert origin.is_empty
