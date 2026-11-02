"""Push devices of a company's users («dispositivos de push»): one row per installation of the web or the app, per user
and company, that notifications-lambda sends pushes to. The port every device store implements, and the rule of which
installation receives pushes.

The entity is `letschatty.models.push_notifications.UserDevice`, unchanged. A row is found by its natural key — company,
user and installation — never by id alone: the key only identifies a row inside one company and one user, so the
company is part of the lookup (ADR-007 of api-chatty, «clave natural»).
"""
from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Any, Optional, Protocol

from ...models.push_notifications import DeviceStatus, TokenStatus, UserDevice


@dataclass(frozen=True)
class DeviceKey:
    """Which installation: the company of the session, the user it is registered for, the id the client generated."""

    company_id: str
    user_id: str
    installation_id: str


@dataclass(frozen=True)
class RegisteredDevice:
    """What registering leaves: the device, and its `_id` exactly as stored (an `ObjectId` for every row the app
    creates), which the token retirement excludes as is."""

    device: UserDevice
    stored_id: Any


class UserDeviceRepository(Protocol):
    async def register(self, key: DeviceKey, *, platform: str, fcm_token: str, app_version: Optional[str],
                       now: datetime) -> RegisteredDevice:
        """Creates the row of `key`, or revives it with everything that says "this installation is live"; its identity,
        `created_at`, `last_seen_at` and `last_push_sent_at` stay. One row per key, also under concurrent calls."""
        ...

    async def retire_others_with_token(self, fcm_token: str, keep: RegisteredDevice, now: datetime) -> int:
        """Logs out every live row but `keep` (`is_active` and `status` active) carrying `fcm_token`, in any company and for
        any user, and says how many."""
        ...

    async def touch(self, key: DeviceKey, now: datetime) -> Optional[UserDevice]:
        """Marks it online, seen `now`; None if `key` has no row."""
        ...

    async def log_out(self, key: DeviceKey, now: datetime) -> Optional[UserDevice]:
        """Logs it out (the row stays); None if `key` has no row."""
        ...

    async def find(self, key: DeviceKey) -> Optional[UserDevice]:
        """The row of `key` whatever its state; None if there is none."""
        ...


def is_eligible_for_push(device: UserDevice) -> bool:
    """Whether this installation would actually receive a push right now.

    Deliberately a MIRROR of the query notifications-lambda runs to pick devices
    (`services/notifications-lambda/src/repositories/user_device_repository.py`). The two must agree: this is the
    predicate behind the frontend's "am I registered?" check, and a check that is stricter than the sender makes the
    client re-register devices that were about to receive pushes just fine.

    `online` is NOT part of it, and that is the point. It is a presence flag — only registering and the heartbeat set it
    True and only logging out sets it False, nothing expires it, and a backgrounded tab receives push regardless. Gating
    registration on presence is what made the check fail permanently after a single logout.
    """
    return (
        device.deleted_at is None
        and device.is_active
        and device.status == DeviceStatus.ACTIVE
        and device.token_status == TokenStatus.VALID
        and bool(device.fcm_token)
    )
