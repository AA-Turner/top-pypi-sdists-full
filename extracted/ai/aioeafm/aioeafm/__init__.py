"""Thin wrapper around the UK Environment Agent Real-time Flood Monitoring API."""
import enum
from typing import Any, Dict, List

import aiohttp


class Status(enum.Enum):

    """The status of the monitoring station."""

    ACTIVE = "Active"
    CLOSED = "Closed"
    SUSPENDED = "Suspended"


async def get_stations(
    session: aiohttp.ClientSession,
    parameter_name: str = None,
    parameter: str = None,
    qualifier: str = None,
    label: str = None,
    town: str = None,
    river_name: str = None,
    station: str = None,
    status: Status = Status.ACTIVE,
) -> List[Dict[str, Any]]:
    """Returns a list of stations."""
    params = {}

    if parameter_name:
        params["parameterName"] = parameter_name
    if parameter:
        params["parameter"] = parameter
    if qualifier:
        params["qualifier"] = qualifier
    if label:
        params["label"] = label
    if town:
        params["town"] = town
    if river_name:
        params["riverName"] = river_name
    if station:
        params["stationReference"] = station
    if status:
        params["status"] = status.value

    response = await session.get(
        "http://environment.data.gov.uk/flood-monitoring/id/stations",
        raise_for_status=True,
        timeout=aiohttp.ClientTimeout(total=30),
        params=params,
    )
    results = await response.json()

    return results["items"]


async def get_station(session: aiohttp.ClientSession, station: str) -> Dict[str, Any]:
    """Returns all data for a given station."""
    response = await session.get(
        f"http://environment.data.gov.uk/flood-monitoring/id/stations/{station}",
        raise_for_status=True,
        timeout=aiohttp.ClientTimeout(total=15),
    )
    results = await response.json()

    return results["items"]
