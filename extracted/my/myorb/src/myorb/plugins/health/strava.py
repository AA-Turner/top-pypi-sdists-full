"""Strava over OAuth with the user's own Strava API application."""

import math
import time
from dataclasses import dataclass
from datetime import UTC, datetime
from typing import Any
from urllib.parse import quote, urlencode

import httpx2

from myorb.connections.providers import ProviderError, request_json

AUTHORIZE_URL = "https://www.strava.com/oauth/authorize"
TOKEN_URL = "https://www.strava.com/oauth/token"
DEAUTHORIZE_URL = "https://www.strava.com/oauth/deauthorize"
API = "https://www.strava.com/api/v3"
SCOPE = "read,activity:read_all"
PROVIDER = "strava"


@dataclass(frozen=True)
class Activity:
    name: str
    sport: str
    start: datetime
    distance_km: float
    moving_minutes: int
    url: str
    # The route as Strava draws it on its map (an encoded polyline); empty without GPS.
    route: str = ""


def authorization_url(client_id: str, redirect_uri: str, state: str) -> str:
    params = {
        "client_id": client_id,
        "redirect_uri": redirect_uri,
        "response_type": "code",
        "approval_prompt": "auto",
        "scope": SCOPE,
        "state": state,
    }
    return f"{AUTHORIZE_URL}?{urlencode(params)}"


async def exchange_code(
    http: httpx2.AsyncClient, client: dict[str, str], code: str
) -> dict[str, Any]:
    return await request_json(
        http,
        "POST",
        TOKEN_URL,
        "Strava",
        data={**client, "code": code, "grant_type": "authorization_code"},
    )


async def access_token(
    http: httpx2.AsyncClient, client: dict[str, str], credentials: dict[str, Any]
) -> tuple[str, dict[str, Any] | None]:
    """A valid access token, and new credentials to store if Strava rotated the tokens."""
    if credentials.get("expires_at", 0) > time.time() + 60:
        return credentials["access_token"], None
    tokens = await request_json(
        http,
        "POST",
        TOKEN_URL,
        "Strava",
        data={
            **client,
            "refresh_token": credentials["refresh_token"],
            "grant_type": "refresh_token",
        },
    )
    updated = {
        **credentials,
        "access_token": tokens["access_token"],
        # Strava may issue a new refresh token; the old one then stops working.
        "refresh_token": tokens.get("refresh_token", credentials["refresh_token"]),
        "expires_at": tokens.get("expires_at", 0),
    }
    return updated["access_token"], updated


async def activities(http: httpx2.AsyncClient, token: str, since: datetime) -> list[Activity]:
    data = await request_json(
        http,
        "GET",
        f"{API}/athlete/activities",
        "Strava",
        headers={"Authorization": f"Bearer {token}"},
        params={"after": int(since.timestamp()), "per_page": 50},
    )
    if not isinstance(data, list):
        raise ProviderError("Strava returned an unexpected answer.")
    return [
        Activity(
            name=item.get("name", "Activity"),
            sport=item.get("sport_type") or item.get("type", ""),
            start=datetime.fromisoformat(item["start_date"].replace("Z", "+00:00")).astimezone(UTC),
            distance_km=round(item.get("distance", 0) / 1000, 1),
            moving_minutes=round(item.get("moving_time", 0) / 60),
            url=f"https://www.strava.com/activities/{item['id']}",
            route=(item.get("map") or {}).get("summary_polyline") or "",
        )
        for item in data
    ]


async def deauthorize(http: httpx2.AsyncClient, token: str) -> None:
    try:
        await http.post(DEAUTHORIZE_URL, data={"access_token": token})
    except httpx2.HTTPError:
        pass


def decode_polyline(encoded: str) -> list[tuple[float, float]]:
    """Google's encoded polyline, as Strava gives a route: (latitude, longitude) pairs."""
    values, number, shift = [], 0, 0
    for char in encoded:
        byte = ord(char) - 63
        number |= (byte & 0x1F) << shift
        shift += 5
        if byte < 0x20:
            values.append(~(number >> 1) if number & 1 else number >> 1)
            number, shift = 0, 0
    points, lat, lng = [], 0, 0
    for dlat, dlng in zip(values[::2], values[1::2], strict=False):
        lat, lng = lat + dlat, lng + dlng
        points.append((lat / 1e5, lng / 1e5))
    return points


def route_image(encoded: str, width: int = 160, height: int = 90) -> str:
    """The route drawn as a small picture (an SVG data URL), north up; empty without one."""
    points = decode_polyline(encoded)
    if len(points) < 2:
        return ""
    # Longitude shrinks towards the poles: scaled by the cosine of the route's latitude.
    scale = math.cos(math.radians(sum(lat for lat, _ in points) / len(points)))
    xs = [lng * scale for _, lng in points]
    ys = [-lat for lat, _ in points]
    x0, y0 = min(xs), min(ys)
    span = max(max(xs) - x0, max(ys) - y0) or 1
    pad = 10
    fit = min(width - 2 * pad, height - 2 * pad) / span
    left = (width - (max(xs) - x0) * fit) / 2
    top = (height - (max(ys) - y0) * fit) / 2
    path = " ".join(
        f"{left + (x - x0) * fit:.1f},{top + (y - y0) * fit:.1f}"
        for x, y in zip(xs, ys, strict=True)
    )
    svg = (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}">'
        f'<polyline points="{path}" fill="none" stroke="#4fd1e8" stroke-width="2.5" '
        'stroke-linecap="round" stroke-linejoin="round"/></svg>'
    )
    return "data:image/svg+xml," + quote(svg)
