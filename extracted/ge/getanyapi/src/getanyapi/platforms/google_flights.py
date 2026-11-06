# Generated - do not edit. Regenerate with: pnpm generate
"""Generated namespace module for the google_flights platform."""

from __future__ import annotations

from typing import Literal, TYPE_CHECKING

from pydantic import BaseModel, ConfigDict, Field
from typing_extensions import NotRequired, Required, TypedDict, Unpack

from ..types import RequestOptions, RunResult

if TYPE_CHECKING:
    from .._async_client import AsyncAnyAPI
    from .._client import AnyAPI


class GoogleFlightsSearchInput(TypedDict, total=False):
    """Input for Google Flights Search."""

    adults: NotRequired[int]
    """Number of adult passengers (1-9, default 1). Prices are for all passengers together. Range: 1 to 9. Default: 1."""
    airlines: NotRequired[list[str]]
    """Only itineraries flown by these airlines, as two-character IATA codes (e.g. ["BA", "AA"])."""
    allowFallbacks: NotRequired[bool]
    """Optional, default true. When false, only the sources listed in `source` may serve; the request is refused with no charge if none of them can. When true, the listed sources are tried first and any other source may serve after them, at the normal price. Default: true."""
    cabinClass: NotRequired[Literal["economy", "premium_economy", "business", "first"]]
    """Cabin class (default economy). Default: economy."""
    children: NotRequired[int]
    """Number of child passengers aged 2-11 (e.g. 1). Range: 0 to 8."""
    currency: NotRequired[str]
    """ISO 4217 currency code for prices (e.g. USD, EUR, GBP; default USD). Default: USD."""
    departureDate: Required[str]
    """Departure date in YYYY-MM-DD format (e.g. 2027-01-12). Today or later."""
    destination: Required[str]
    """Arrival airport as a three-letter IATA code in capitals (e.g. LHR)."""
    ignoreSources: NotRequired[list[str]]
    """Optional. Source ids to skip for this request, taken from this endpoint's `lanes[].source.id`. The cheapest remaining source serves and the price is that of the dearest remaining source. An id that does not serve this endpoint, or that is also in `source`, is rejected as invalid input with no charge; skipping every source is rejected the same way."""
    maxPrice: NotRequired[int]
    """Highest total price to return, in currency (e.g. 600). Minimum: 1."""
    maxStops: NotRequired[Literal["any", "nonstop", "one_or_fewer", "two_or_fewer"]]
    """Most stops an itinerary may have (default any). Default: any."""
    origin: Required[str]
    """Departure airport as a three-letter IATA code in capitals (e.g. JFK)."""
    preferLatencyUnderMs: NotRequired[int]
    """Optional; omit it and routing is unchanged, with the cheapest source serving. Prefer sources whose typical response time (median over the trailing 30 days, as published on this endpoint's lane health) is under this many milliseconds; among those, the cheapest serves. This can raise your price: when the cheapest source misses the target, a faster and dearer one serves, and you are quoted and charged its price. If no source is that fast the request is still served, by whichever source offers the best speed for its price - it is never refused for being slow. Sources we have not timed are tried last. This is a preference, not a guarantee: the median describes past requests and is not a ceiling on this one, and it excludes any wait this request itself asks for. On a paginated walk it applies to the first page only: later pages stay with the source that page chose, at the price it was quoted. Minimum: 1."""
    requireFields: NotRequired[list[Literal["typicalCo2Kg"]]]
    """Optional; omit it and routing is unchanged, with the cheapest source serving. Name the output fields this request must be able to return, for example `typicalCo2Kg`, and it is served only by a source that returns every one of them. Fields you do not name are still returned whenever the serving source has them. This can raise your price: when the cheapest source cannot return a named field, a dearer source serves, and you are quoted and charged its price. A named field can still be absent on an itinerary that genuinely lacks it. Naming a combination that no single source returns together is refused as invalid input, with no charge."""
    returnDate: NotRequired[str]
    """Return date in YYYY-MM-DD format for a round trip (e.g. 2027-01-19). Omit it for one way. With it, each result is an outbound option priced at the cheapest round trip that starts with it, and the return flights are not included."""
    sortBy: NotRequired[
        Literal[
            "top_flights",
            "cheapest",
            "departure_time",
            "arrival_time",
            "duration",
            "emissions",
        ]
    ]
    """Result order: top_flights (Google's best flights first, the default), cheapest, departure_time, arrival_time, duration or emissions. Default: top_flights."""
    source: NotRequired[list[str]]
    """Optional. Source ids to prefer, in order, taken from this endpoint's `lanes[].source.id` in /catalog or /apis. Omit it and the cheapest source serves, with automatic failover. Listed sources are tried first in the order given, then the others, unless `allowFallbacks` is false. A single source with `allowFallbacks` false is served only by that source at its price, quoted and charged exactly, with no failover. The price is that of the dearest source that may serve. An id that does not serve this endpoint is rejected as invalid input with no charge; a listed source that is not serving right now is refused with no charge, so omit `source` to be served by another. On a paginated walk, later pages must include the source that served page one, or omit `source`."""


class GoogleFlightsSearchData(BaseModel):
    itineraries: list[GoogleFlightsSearchItinerarie] = Field(
        description="Itineraries in Google Flights' order for the chosen sort. On a round trip each one is an outbound option. Populated whenever the provider has data for the entity."
    )


class GoogleFlightsSearchItinerarie(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    airline: str | None = Field(
        default=None,
        description="Name of the airline Google Flights shows for the itinerary (e.g. British Airways). The airline of each leg is in legs. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    booking_token: str | None = Field(
        default=None,
        alias="bookingToken",
        description="Google Flights' token for this itinerary's fare, or null when not given.",
    )
    co2_kg: float | None = Field(
        default=None,
        alias="co2Kg",
        description="Estimated CO2 emissions of the itinerary in kilograms, or null when not shown (usually on round trips).",
    )
    currency: str | None = Field(
        default=None,
        description="ISO 4217 currency code of price. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    departure_token: str | None = Field(
        default=None,
        alias="departureToken",
        description="On a round trip, the source's token for this outbound option; null on a one-way search.",
    )
    legs: list[GoogleFlightsSearchLeg] = Field(
        description="Flights of the itinerary in order (the outbound journey on a round trip)."
    )
    price: float | None = Field(
        default=None,
        description="Price for all passengers together, in currency, or null when Google shows no price. What it covers is in priceType. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    price_type: Literal["total", "round_trip_starting"] = Field(
        alias="priceType",
        description="total: the one-way fare for all passengers. round_trip_starting: the cheapest round-trip fare that starts with this outbound option; the return flights are not included.",
    )
    stops: int | None = Field(
        default=None,
        description="Number of stops (0 for nonstop); on a round trip, of the outbound journey. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    total_duration_minutes: int | None = Field(
        default=None,
        alias="totalDurationMinutes",
        description="Total travel time in minutes, layovers included; on a round trip, of the outbound journey. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    typical_co2_kg: float | None = Field(
        default=None,
        alias="typicalCo2Kg",
        description="Typical CO2 emissions in kilograms for this route, to compare co2Kg against, or null when not shown.",
    )


class GoogleFlightsSearchLeg(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    airline_code: str | None = Field(
        default=None,
        alias="airlineCode",
        description="IATA code of the airline flying this leg (e.g. BA).",
    )
    arrival_airport: str = Field(
        alias="arrivalAirport", description="IATA code of the arrival airport."
    )
    arrival_date: str | None = Field(
        default=None,
        alias="arrivalDate",
        description="Arrival date in YYYY-MM-DD, local time at the arrival airport.",
    )
    arrival_time: str | None = Field(
        default=None,
        alias="arrivalTime",
        description="Arrival time as 24-hour HH:MM, local time at the arrival airport.",
    )
    departure_airport: str = Field(
        alias="departureAirport", description="IATA code of the departure airport."
    )
    departure_date: str | None = Field(
        default=None,
        alias="departureDate",
        description="Departure date in YYYY-MM-DD, local time at the departure airport.",
    )
    departure_time: str | None = Field(
        default=None,
        alias="departureTime",
        description="Departure time as 24-hour HH:MM, local time at the departure airport.",
    )
    duration_minutes: int | None = Field(
        default=None,
        alias="durationMinutes",
        description="Flight time of this leg in minutes.",
    )
    flight_number: str | None = Field(
        default=None,
        alias="flightNumber",
        description="Flight number without the airline code (e.g. 112).",
    )


class GoogleFlightsNamespace:
    """Typed methods for this platform. Attached lazily to the client."""

    def __init__(self, client: "AnyAPI") -> None:
        self._client = client

    def search(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[GoogleFlightsSearchInput],
    ) -> RunResult[GoogleFlightsSearchData]:
        """Google Flights Search

        Search Google Flights between two airports on a date and get about 20
        itineraries: price, airline, stops, total duration, CO2 emissions against
        the typical figure for the route, and every leg's airline code, flight
        number, airports, local departure and arrival times and duration, as
        normalized JSON. Filter by cabin class, stops, airlines and maximum price.
        One-way searches return the total fare for all passengers. With a
        returnDate, each result is an outbound option priced at the cheapest round
        trip that starts with it (priceType round_trip_starting); the return flights
        are not included.

        Price: $0.001 per request.

        Example:
            res = client.google_flights.search(departureDate="2026-12-06", destination="LHR", origin="JFK")
        """
        raw = self._client._run_raw(  # pyright: ignore[reportPrivateUsage]
            "google_flights.search", dict(input), options
        )
        return RunResult[GoogleFlightsSearchData].model_validate(raw)


class AsyncGoogleFlightsNamespace:
    """Typed methods for this platform. Attached lazily to the client."""

    def __init__(self, client: "AsyncAnyAPI") -> None:
        self._client = client

    async def search(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[GoogleFlightsSearchInput],
    ) -> RunResult[GoogleFlightsSearchData]:
        """Google Flights Search

        Search Google Flights between two airports on a date and get about 20
        itineraries: price, airline, stops, total duration, CO2 emissions against
        the typical figure for the route, and every leg's airline code, flight
        number, airports, local departure and arrival times and duration, as
        normalized JSON. Filter by cabin class, stops, airlines and maximum price.
        One-way searches return the total fare for all passengers. With a
        returnDate, each result is an outbound option priced at the cheapest round
        trip that starts with it (priceType round_trip_starting); the return flights
        are not included.

        Price: $0.001 per request.

        Example:
            res = client.google_flights.search(departureDate="2026-12-06", destination="LHR", origin="JFK")
        """
        raw = await self._client._arun_raw(  # pyright: ignore[reportPrivateUsage]
            "google_flights.search", dict(input), options
        )
        return RunResult[GoogleFlightsSearchData].model_validate(raw)
