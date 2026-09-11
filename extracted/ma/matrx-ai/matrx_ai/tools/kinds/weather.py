"""Historical weather kinds — what the weather WAS at one place on one date.

Why a kind and not a dict: the whole point of a historical weather reading is
that something downstream acts on it. A verification desk compares it against
what a photo shows; a report renders it; an agent quotes it back in a sentence.
An anonymous dict can be none of those — nothing can route, filter, trigger on
or render a shape with no identity.

ONE kind per capability, shared by the workflow node and the agent tool — the
precedent ``media_forensics`` set for the image-verification pair, rather than a
node kind and a near-identical twin tool kind (the near-duplicate the kind
doctrine forbids). ``aidream/graph_actions/web/weather.py`` imports
``WeatherHistoryReading`` as its node ``output_schema``,
``aidream/services/weather_history/service.py`` builds it, and the
``weather_history`` agent tool returns it, so node, tool and published registry
row cannot drift apart.

It lives in the package, not in ``aidream/kinds/``, because the TOOL
implementation imports it and a package never imports aidream
(``scripts/check_package_boundaries.py``).

The three nested shapes (place, day, hour) are ``KindSubModel`` and NOT kinds of
their own: none has independent meaning outside a reading, and minting a slug
for every nested object is how a family ends up with a hundred kinds, which is
the same as none.

Publish with::

    uv run python scripts/publish_kind_catalog.py matrx_ai.tools.kinds.weather --apply
"""

from __future__ import annotations

from typing import Literal

from matrx_graph.content_ir.model import KindModel, KindSubModel
from matrx_graph.content_ir.sdk import kind
from pydantic import Field


class WeatherPlace(KindSubModel):
    """The place the reading is actually FOR — never assumed to be the place the
    caller typed. A desk that cannot see WHICH "Springfield" answered has
    learned nothing, so the resolved identity travels with every reading."""

    name: str = Field(
        description="Resolved place name, or the coordinate pair when the caller supplied one."
    )
    country: str | None = Field(
        default=None, description="Country name as the geocoder resolved it."
    )
    country_code: str | None = Field(default=None, description="ISO-3166 alpha-2 country code.")
    admin1: str | None = Field(
        default=None, description="First-level administrative area (state, region, county)."
    )
    latitude: float = Field(description="Latitude of the grid cell the reading came from.")
    longitude: float = Field(description="Longitude of the grid cell the reading came from.")
    timezone: str = Field(description="IANA timezone the returned local times are expressed in.")
    elevation_m: float | None = Field(
        default=None, description="Elevation of the grid cell, in metres."
    )
    resolved_by: Literal["place_name", "coordinates"] = Field(
        description=(
            "'place_name' when a name was geocoded to get here, 'coordinates' when the "
            "caller supplied lat/lon directly."
        )
    )


class WeatherDaySummary(KindSubModel):
    """The whole-day summary for the requested date, in local time."""

    date: str = Field(
        description="The date this summary covers, ISO-8601 (YYYY-MM-DD), local to the place."
    )
    weather_code: int | None = Field(
        default=None, description="WMO 4677 present-weather code for the day."
    )
    description: str = Field(
        description="Plain-English rendering of the weather code, e.g. 'Heavy rain'."
    )
    temperature_max_c: float | None = Field(
        default=None, description="Highest 2m air temperature, Celsius."
    )
    temperature_min_c: float | None = Field(
        default=None, description="Lowest 2m air temperature, Celsius."
    )
    apparent_temperature_max_c: float | None = Field(
        default=None, description="Highest apparent (feels-like) temperature, Celsius."
    )
    apparent_temperature_min_c: float | None = Field(
        default=None, description="Lowest apparent (feels-like) temperature, Celsius."
    )
    precipitation_mm: float | None = Field(
        default=None, description="Total precipitation for the day, millimetres."
    )
    rain_mm: float | None = Field(
        default=None, description="Rain component of the day's precipitation, millimetres."
    )
    snowfall_cm: float | None = Field(
        default=None, description="Snowfall for the day, centimetres."
    )
    precipitation_hours: float | None = Field(
        default=None, description="Number of hours of the day with measurable precipitation."
    )
    wind_speed_max_kmh: float | None = Field(
        default=None, description="Maximum 10m wind speed, km/h."
    )
    wind_gusts_max_kmh: float | None = Field(
        default=None, description="Maximum 10m wind gust, km/h."
    )
    sunrise: str | None = Field(default=None, description="Local sunrise time, ISO-8601.")
    sunset: str | None = Field(default=None, description="Local sunset time, ISO-8601.")


class WeatherHourReading(KindSubModel):
    """One hour inside the requested window, in the place's local time."""

    time: str = Field(description="Local time of this reading, ISO-8601 (YYYY-MM-DDTHH:MM).")
    hour: int = Field(ge=0, le=23, description="Local hour of day, 0-23.")
    temperature_c: float | None = Field(default=None, description="2m air temperature, Celsius.")
    apparent_temperature_c: float | None = Field(
        default=None, description="Apparent (feels-like) temperature, Celsius."
    )
    precipitation_mm: float | None = Field(
        default=None, description="Precipitation during this hour, millimetres."
    )
    rain_mm: float | None = Field(default=None, description="Rain during this hour, millimetres.")
    snowfall_cm: float | None = Field(
        default=None, description="Snowfall during this hour, centimetres."
    )
    cloud_cover_pct: float | None = Field(default=None, description="Total cloud cover, percent.")
    wind_speed_kmh: float | None = Field(default=None, description="10m wind speed, km/h.")
    wind_direction_deg: float | None = Field(
        default=None, description="10m wind direction, degrees clockwise from north."
    )
    relative_humidity_pct: float | None = Field(
        default=None, description="2m relative humidity, percent."
    )
    weather_code: int | None = Field(
        default=None, description="WMO 4677 present-weather code for this hour."
    )
    description: str = Field(description="Plain-English rendering of this hour's weather code.")


@kind(
    "weather_history_reading",
    label="Historical Weather Reading",
    family="weather",
    # A REAL measured payload: Open-Meteo's ERA5 archive for London on
    # 2014-01-20, fetched 2026-09-10. An invented example is a lie about what
    # this kind looks like.
    example={
        "__kind": "weather_history_reading",
        "provider": "open_meteo",
        "place": {
            "name": "London",
            "country": "United Kingdom",
            "country_code": "GB",
            "admin1": "England",
            "latitude": 51.493847,
            "longitude": -0.1630249,
            "timezone": "Europe/London",
            "elevation_m": 23.0,
            "resolved_by": "place_name",
        },
        "date": "2014-01-20",
        "daily": {
            "date": "2014-01-20",
            "weather_code": 3,
            "description": "Overcast",
            "temperature_max_c": 8.3,
            "temperature_min_c": 0.3,
            "apparent_temperature_max_c": 6.6,
            "apparent_temperature_min_c": -3.0,
            "precipitation_mm": 0.0,
            "rain_mm": 0.0,
            "snowfall_cm": 0.0,
            "precipitation_hours": 0.0,
            "wind_speed_max_kmh": 8.4,
            "wind_gusts_max_kmh": 13.0,
            "sunrise": "2014-01-20T08:54",
            "sunset": "2014-01-20T17:29",
        },
        "hourly": [
            {
                "time": "2014-01-20T12:00",
                "hour": 12,
                "temperature_c": 6.0,
                "apparent_temperature_c": 4.2,
                "precipitation_mm": 0.0,
                "rain_mm": 0.0,
                "snowfall_cm": 0.0,
                "cloud_cover_pct": 100.0,
                "wind_speed_kmh": 3.1,
                "wind_direction_deg": 216.0,
                "relative_humidity_pct": 89.0,
                "weather_code": 3,
                "description": "Overcast",
            }
        ],
        "hour_window": "12:00-12:00",
        "summary": (
            "Overcast in London on 2014-01-20; 0.3\u00b0C to 8.3\u00b0C; no precipitation; "
            "sunrise 08:54, sunset 17:29."
        ),
    },
    # DISTILLED — the load-bearing fields are `place` (WHICH place answered) and
    # `daily.description` + `daily.precipitation_mm` (what a photo of that day
    # should and should not show). `summary` exists so the reading is never mute:
    # one sentence anybody can read without decoding a WMO code.
    maturity="distilled",
)
class WeatherHistoryReading(KindModel):
    """What the weather actually was at one place on one past date."""

    provider: Literal["open_meteo"] = Field(
        default="open_meteo",
        description="The archive this reading came from. Open-Meteo serves ERA5 reanalysis.",
    )
    place: WeatherPlace = Field(
        description="The place the reading is for, as resolved — not as typed."
    )
    date: str = Field(description="The date the reading covers, ISO-8601 (YYYY-MM-DD).")
    daily: WeatherDaySummary = Field(description="Whole-day summary for that date.")
    hourly: list[WeatherHourReading] = Field(
        default_factory=list,
        description="Hour-by-hour readings for the requested local window, in time order.",
    )
    hour_window: str = Field(
        description="The local hour window the hourly rows cover, e.g. '09:00-17:00'."
    )
    summary: str = Field(
        description="One plain-English sentence stating what the weather was that day at that place."
    )


WEATHER_TOOL_RESULT_KINDS: dict[str, type[KindModel]] = {
    "weather_history": WeatherHistoryReading,
}


__all__ = [
    "WEATHER_TOOL_RESULT_KINDS",
    "WeatherDaySummary",
    "WeatherHistoryReading",
    "WeatherHourReading",
    "WeatherPlace",
]
