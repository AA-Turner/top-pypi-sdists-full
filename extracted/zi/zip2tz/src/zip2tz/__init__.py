from typing import Optional

from zip2tz._data import TIMEZONES, ZIP_TZ


def timezone(zipcode: str | int) -> Optional[str]:
    """
    Returns the timezone string for a given zipcode.

    Args:
        zipcode: The zipcode as a string or integer.

    Returns:
        The timezone string (e.g., 'America/New_York') or None if not found.
    """
    try:
        zip_int = int(zipcode)
    except (ValueError, TypeError):
        return None

    tz_idx = ZIP_TZ.get(zip_int)
    if tz_idx is None:
        return None
    return TIMEZONES[tz_idx]
