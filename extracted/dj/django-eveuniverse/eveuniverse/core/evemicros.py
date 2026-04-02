"""Wrapper to access evemicros API."""

from dataclasses import dataclass
from typing import Optional
from urllib.parse import urlencode

import requests
from django.core.cache import cache

from eveuniverse.app_settings import EVEUNIVERSE_REQUESTS_DEFAULT_TIMEOUT

_CACHE_TIMEOUT = 3_600 * 12
_BASE_URL = "https://www.kalkoken.org/apps/evemicros/eveUniverse.php"


@dataclass
class EveItem:
    """A celestial item."""

    id: int
    name: str
    type_id: int
    distance: float


def nearest_celestial(
    solar_system_id: int, x: int, y: int, z: int, group_id: Optional[int] = None
) -> Optional[EveItem]:
    """Fetch nearest celestial to given coordinates from API. Results are cached.

    Args:
        solar_system_id: Eve ID of solar system
        x, y, z: Start point in space to look from
        group_id: Eve ID of group to filter results by

    Raises:
        HTTPError: If an HTTP error is encountered

    Returns:
        Found Eve item or None if nothing found nearby.
    """
    result = _fetch_result_from_api_cached(
        solar_system_id=solar_system_id, x=x, y=y, z=z
    )
    return _get_item_from_result(result, group_id)


def _fetch_result_from_api_cached(
    solar_system_id: int, x: int, y: int, z: int
) -> Optional[dict]:
    """Fetches result from API or cache.
    Returns None if data from API does not have expected structure.
    """
    params = map(str, map(int, [solar_system_id, x, y, z]))
    query = urlencode({"nearestCelestials": ",".join(params)})
    cache_key = f"EVEUNIVERSE_NEAREST_CELESTIAL_{query}"
    result = cache.get(key=cache_key)
    if not result:
        response = requests.get(
            f"{_BASE_URL}?{query}", timeout=EVEUNIVERSE_REQUESTS_DEFAULT_TIMEOUT
        )
        response.raise_for_status()
        data = response.json()
        if "ok" not in data or not data["ok"] or "result" not in data:
            return None
        result = data["result"]
        cache.set(key=cache_key, value=result, timeout=_CACHE_TIMEOUT)
    return result


def _get_item_from_result(result, group_id) -> Optional[EveItem]:
    """Tries to find item in result. Returns None if item can not be found."""
    if not result:
        return None
    if not group_id:
        return _create_item(result[0])
    for item in result:
        if item["groupID"] == group_id:
            return _create_item(item)
    return None


def _create_item(record: dict) -> EveItem:
    return EveItem(
        id=int(record["itemID"]),
        name=str(record["itemName"]),
        type_id=int(record["typeID"]),
        distance=float(record["distanceKm"]),
    )
