"""Device provenance on a write — `origin_device_id` and `client_modified_at`.

SPEC-SERVER §2.2. Two values ride EVERY write route as headers:

    X-Matrx-Device-Id:           <uuid of a public.app_instances row>
    X-Matrx-Client-Modified-At:  <RFC3339>

Headers, not body fields, for three reasons: the buffered upload is
``multipart/form-data`` (so a header matches the existing X-Request-Id /
X-Idempotency-Key convention), TUS has no body at all, and a header applies
unchanged to PATCH, to soft-delete, and to any future write route. TUS
additionally accepts the same two values as ``Upload-Metadata`` keys
``deviceid`` / ``clientmodifiedat``, because a TUS client library may not let a
caller add headers to every PATCH; when both are present the HEADER WINS and a
mismatch is a 400 -- never a silent pick.

Why the validation is not optional: a device id naming another user's device
would let one account's row claim another account's machine, and the daemon
uses exactly that field to decide "this change is my own echo, skip it". A
skewed client clock is a NAMED STATE on the client, never a poisoned row.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, datetime, timedelta
from uuid import UUID

#: A client clock further ahead than this is refused rather than stored.
MAX_CLIENT_CLOCK_SKEW = timedelta(hours=24)


class DeviceWriteError(ValueError):
    """A write carried device provenance the server will not store.

    ``code`` is the wire error code; the REST layer maps every instance to 400.
    """

    def __init__(self, code: str, message: str) -> None:
        super().__init__(message)
        self.code = code
        self.message = message


@dataclass(frozen=True)
class WriteOrigin:
    """Validated device provenance for one write. Both halves may be None."""

    device_id: str | None = None
    client_modified_at: datetime | None = None

    @property
    def is_empty(self) -> bool:
        return self.device_id is None and self.client_modified_at is None


def reconcile_header_and_metadata(
    *,
    name: str,
    header_value: str | None,
    metadata_value: str | None,
) -> str | None:
    """TUS carries these twice. The header wins; a mismatch is refused.

    Silently picking one of two disagreeing values is how a file ends up
    attributed to the wrong machine with nothing in any log to say why.
    """
    if header_value is None:
        return metadata_value
    if metadata_value is None:
        return header_value
    if header_value.strip() == metadata_value.strip():
        return header_value
    raise DeviceWriteError(
        "conflicting_origin_metadata",
        f"{name} was sent twice with different values: header {header_value!r} and "
        f"Upload-Metadata {metadata_value!r}. The header wins, but a disagreement is "
        "refused rather than silently resolved -- send one value, or the same value twice.",
    )


def parse_client_modified_at(raw: str | None, *, now: datetime | None = None) -> datetime | None:
    """Parse and sanity-check the client's observed filesystem mtime."""
    if raw is None or not raw.strip():
        return None
    text = raw.strip()
    try:
        parsed = datetime.fromisoformat(text.replace("Z", "+00:00"))
    except ValueError as exc:
        raise DeviceWriteError(
            "invalid_client_time",
            f"X-Matrx-Client-Modified-At must be RFC3339; got {raw!r} ({exc}).",
        ) from exc
    if parsed.tzinfo is None:
        # A naive timestamp is ambiguous, and guessing UTC would silently shift
        # every conflict decision by the client's offset.
        raise DeviceWriteError(
            "invalid_client_time",
            f"X-Matrx-Client-Modified-At must carry a UTC offset; got {raw!r}.",
        )
    parsed = parsed.astimezone(UTC)
    reference = now or datetime.now(UTC)
    if parsed > reference + MAX_CLIENT_CLOCK_SKEW:
        raise DeviceWriteError(
            "implausible_client_time",
            f"X-Matrx-Client-Modified-At is {parsed.isoformat()}, more than "
            f"{int(MAX_CLIENT_CLOCK_SKEW.total_seconds() // 3600)}h in the future. The "
            "device's clock is wrong; fix the clock (the client shows this as a named "
            "state) -- the server will not store a poisoned timestamp.",
        )
    return parsed


def parse_device_id(raw: str | None) -> str | None:
    """Shape check only; ownership is checked against the database."""
    if raw is None or not raw.strip():
        return None
    try:
        return str(UUID(raw.strip()))
    except ValueError as exc:
        raise DeviceWriteError(
            "invalid_device",
            f"X-Matrx-Device-Id must be the uuid of a public.app_instances row "
            f"(app_instances.id, never instance_id); got {raw!r}.",
        ) from exc


async def resolve_write_origin(
    *,
    user_id: str,
    device_id: str | None,
    client_modified_at: str | None,
    now: datetime | None = None,
) -> WriteOrigin:
    """Validate both halves, including that the device belongs to this caller.

    A device id naming another user's device is refused (``invalid_device``) and
    NEVER stored: ``(user_id, instance_id)`` is the only other unique key on
    app_instances, so the id is the one identity that cannot be guessed into
    someone else's account.
    """
    parsed_device = parse_device_id(device_id)
    parsed_mtime = parse_client_modified_at(client_modified_at, now=now)
    if parsed_device is None:
        return WriteOrigin(None, parsed_mtime)

    from matrx_files.db import ensure_bound  # noqa: F401  (pool must be registered)
    from matrx_files.db.models import AppInstances

    rows = await AppInstances.filter(id=parsed_device).values("id", "user_id")
    if not rows:
        raise DeviceWriteError(
            "invalid_device",
            f"No registered device {parsed_device}. Register the device "
            "(public.app_instances) before attributing a write to it.",
        )
    if str(rows[0]["user_id"]) != str(user_id):
        raise DeviceWriteError(
            "invalid_device",
            f"Device {parsed_device} belongs to a different user. A write is never "
            "attributed to another account's machine.",
        )
    return WriteOrigin(parsed_device, parsed_mtime)
