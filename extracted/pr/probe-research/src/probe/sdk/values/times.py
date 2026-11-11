"""A run's real start or end time as the ISO 8601 text the server takes, with its UTC offset kept."""

from __future__ import annotations

from datetime import datetime

from .. import errors


def to_iso_time(value: str | datetime, *, label: str) -> str:
    """``value`` as ISO 8601 with an offset; anything else is refused before a request is sent.

    A time with no offset is refused, not read as UTC: a re-logged run's clock is often not UTC,
    and a silent guess shifts the run by hours. ``label`` names the argument in the error."""
    if isinstance(value, datetime):
        moment = value
    else:
        text = str(value).strip()
        try:
            # A trailing `Z` is UTC; Python 3.10's `fromisoformat` refuses it.
            moment = datetime.fromisoformat(text[:-1] + "+00:00" if text.endswith(("Z", "z")) else text)
        except ValueError:
            raise errors.ValidationError(
                f"{label} {value!r} is not an ISO 8601 time. Use one with its offset, "
                "like 2026-11-08T12:00:00+00:00 or 2026-11-08T12:00:00Z."
            ) from None
    if moment.tzinfo is None or moment.utcoffset() is None:
        raise errors.ValidationError(
            f"{label} {value!s} has no UTC offset. Add one, like 2026-11-08T12:00:00+00:00 "
            "or 2026-11-08T12:00:00Z."
        )
    return moment.isoformat()
