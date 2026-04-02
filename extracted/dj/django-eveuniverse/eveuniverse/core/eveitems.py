"""URLs for profile pages on eveitems webpage."""

from urllib.parse import urlencode

_PROFILE_BASE_URL = "https://www.kalkoken.org/apps/eveitems/"


def type_url(type_id: int) -> str:
    """URL to display any type on the default third party webpage."""
    query = urlencode({"typeId": int(type_id)}, doseq=True)
    return f"{_PROFILE_BASE_URL}?{query}"
