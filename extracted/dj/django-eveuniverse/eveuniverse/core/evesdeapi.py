"""Wrapper to access evesdeapi website."""

import logging
from dataclasses import dataclass
from typing import Optional

import requests
from django.core.cache import cache

from eveuniverse.app_settings import EVEUNIVERSE_REQUESTS_DEFAULT_TIMEOUT
from eveuniverse.helpers import dict_hash

_CACHE_TIMEOUT = 3_600 * 12
_BASE_URL = "https://evesdeapi.kalkoken.net/latest"

logger = logging.getLogger(__name__)


@dataclass
class EveItem:
    """A celestial item."""

    id: int
    name: str
    type_id: int
    distance: float

    @classmethod
    def from_dict(cls, record: dict) -> "EveItem":
        """Create new obj from a record."""
        return cls(
            id=int(record["item_id"]),
            name=str(record["name"]),
            type_id=int(record["type_id"]),
            distance=float(record["distance"]),
        )


def nearest_celestial(
    solar_system_id: float, x: float, y: float, z: float, group_id: Optional[int] = None
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
    result = _fetch_items_from_endpoint_cached(
        solar_system_id=solar_system_id, x=x, y=y, z=z, group_id=group_id
    )
    if not result:
        return None
    return EveItem.from_dict(result[0])


def _fetch_items_from_endpoint_cached(
    solar_system_id: float, x: float, y: float, z: float, group_id: Optional[int] = None
) -> Optional[dict]:
    """Fetch items from endpoint with caching.

    Returns None if data from API does not have expected structure.
    """
    params = {"x": x, "y": y, "z": z}
    if group_id is not None:
        params["group_id"] = int(group_id)
    cache_key = f"eveuniverse_nearest_celestial_{dict_hash(params)}"
    result = cache.get(key=cache_key)
    if not result:
        url = f"{_BASE_URL}/universe/systems/{solar_system_id}/nearest_celestials"
        response = requests.get(
            url, params=params, timeout=EVEUNIVERSE_REQUESTS_DEFAULT_TIMEOUT
        )
        logger.debug(
            "Response from evesdeapi: url %s, status %s, headers %s, content %s",
            response.url,
            response.status_code,
            response.headers,
            response.text,
        )
        response.raise_for_status()
        result = response.json()
        cache.set(key=cache_key, value=result, timeout=_CACHE_TIMEOUT)
    return result
