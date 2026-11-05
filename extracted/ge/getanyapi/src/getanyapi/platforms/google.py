# Generated - do not edit. Regenerate with: pnpm generate
"""Generated namespace module for the google platform."""

from __future__ import annotations

from typing import Literal, TYPE_CHECKING

from pydantic import BaseModel, ConfigDict, Field
from typing_extensions import NotRequired, Required, TypedDict, Unpack

from ..types import RequestOptions, RunResult
from .._pagination import (
    AsyncPaginator,
    Paginator,
    apaginate,
    paginate,
)

if TYPE_CHECKING:
    from .._async_client import AsyncAnyAPI
    from .._client import AnyAPI


class GoogleAiModeInput(TypedDict, total=False):
    """Input for Google AI Mode."""

    allowFallbacks: NotRequired[bool]
    """Optional, default true. When false, only the sources listed in `source` may serve; the request is refused with no charge if none of them can. When true, the listed sources are tried first and any other source may serve after them, at the normal price. Default: true."""
    ignoreSources: NotRequired[list[str]]
    """Optional. Source ids to skip for this request, taken from this endpoint's `lanes[].source.id`. The cheapest remaining source serves and the price is that of the dearest remaining source. An id that does not serve this endpoint, or that is also in `source`, is rejected as invalid input with no charge; skipping every source is rejected the same way."""
    preferLatencyUnderMs: NotRequired[int]
    """Optional; omit it and routing is unchanged, with the cheapest source serving. Prefer sources whose typical response time (median over the trailing 30 days, as published on this endpoint's lane health) is under this many milliseconds; among those, the cheapest serves. This can raise your price: when the cheapest source misses the target, a faster and dearer one serves, and you are quoted and charged its price. If no source is that fast the request is still served, by whichever source offers the best speed for its price - it is never refused for being slow. Sources we have not timed are tried last. This is a preference, not a guarantee: the median describes past requests and is not a ceiling on this one, and it excludes any wait this request itself asks for. On a paginated walk it applies to the first page only: later pages stay with the source that page chose, at the price it was quoted. Minimum: 1."""
    prompt: Required[str]
    """The question or prompt to answer with Google AI Mode."""
    source: NotRequired[list[str]]
    """Optional. Source ids to prefer, in order, taken from this endpoint's `lanes[].source.id` in /catalog or /apis. Omit it and the cheapest source serves, with automatic failover. Listed sources are tried first in the order given, then the others, unless `allowFallbacks` is false. A single source with `allowFallbacks` false is served only by that source at its price, quoted and charged exactly, with no failover. The price is that of the dearest source that may serve. An id that does not serve this endpoint is rejected as invalid input with no charge; a listed source that is not serving right now is refused with no charge, so omit `source` to be served by another. On a paginated walk, later pages must include the source that served page one, or omit `source`."""


class GoogleAiOverviewInput(TypedDict, total=False):
    """Input for Google AI Overview."""

    allowFallbacks: NotRequired[bool]
    """Optional, default true. When false, only the sources listed in `source` may serve; the request is refused with no charge if none of them can. When true, the listed sources are tried first and any other source may serve after them, at the normal price. Default: true."""
    ignoreSources: NotRequired[list[str]]
    """Optional. Source ids to skip for this request, taken from this endpoint's `lanes[].source.id`. The cheapest remaining source serves and the price is that of the dearest remaining source. An id that does not serve this endpoint, or that is also in `source`, is rejected as invalid input with no charge; skipping every source is rejected the same way."""
    preferLatencyUnderMs: NotRequired[int]
    """Optional; omit it and routing is unchanged, with the cheapest source serving. Prefer sources whose typical response time (median over the trailing 30 days, as published on this endpoint's lane health) is under this many milliseconds; among those, the cheapest serves. This can raise your price: when the cheapest source misses the target, a faster and dearer one serves, and you are quoted and charged its price. If no source is that fast the request is still served, by whichever source offers the best speed for its price - it is never refused for being slow. Sources we have not timed are tried last. This is a preference, not a guarantee: the median describes past requests and is not a ceiling on this one, and it excludes any wait this request itself asks for. On a paginated walk it applies to the first page only: later pages stay with the source that page chose, at the price it was quoted. Minimum: 1."""
    prompt: Required[str]
    """The question or prompt to answer with a Google AI Overview."""
    requireFields: NotRequired[list[Literal["scrapedAt"]]]
    """Optional; omit it and routing is unchanged, with the cheapest source serving. Name the output fields this request must be able to return, for example `scrapedAt`, and it is served only by a source that returns every one of them. Fields you do not name are still returned whenever the serving source has them. This can raise your price: when the cheapest source cannot return a named field, a dearer source serves, and you are quoted and charged its price. Naming a combination that no single source returns together is refused as invalid input, with no charge."""
    source: NotRequired[list[str]]
    """Optional. Source ids to prefer, in order, taken from this endpoint's `lanes[].source.id` in /catalog or /apis. Omit it and the cheapest source serves, with automatic failover. Listed sources are tried first in the order given, then the others, unless `allowFallbacks` is false. A single source with `allowFallbacks` false is served only by that source at its price, quoted and charged exactly, with no failover. The price is that of the dearest source that may serve. An id that does not serve this endpoint is rejected as invalid input with no charge; a listed source that is not serving right now is refused with no charge, so omit `source` to be served by another. On a paginated walk, later pages must include the source that served page one, or omit `source`."""


class GoogleAiOverviewPreviewInput(TypedDict, total=False):
    """Input for Google AI Overview Preview."""

    allowFallbacks: NotRequired[bool]
    """Optional, default true. When false, only the sources listed in `source` may serve; the request is refused with no charge if none of them can. When true, the listed sources are tried first and any other source may serve after them, at the normal price. Default: true."""
    ignoreSources: NotRequired[list[str]]
    """Optional. Source ids to skip for this request, taken from this endpoint's `lanes[].source.id`. The cheapest remaining source serves and the price is that of the dearest remaining source. An id that does not serve this endpoint, or that is also in `source`, is rejected as invalid input with no charge; skipping every source is rejected the same way."""
    preferLatencyUnderMs: NotRequired[int]
    """Optional; omit it and routing is unchanged, with the cheapest source serving. Prefer sources whose typical response time (median over the trailing 30 days, as published on this endpoint's lane health) is under this many milliseconds; among those, the cheapest serves. This can raise your price: when the cheapest source misses the target, a faster and dearer one serves, and you are quoted and charged its price. If no source is that fast the request is still served, by whichever source offers the best speed for its price - it is never refused for being slow. Sources we have not timed are tried last. This is a preference, not a guarantee: the median describes past requests and is not a ceiling on this one, and it excludes any wait this request itself asks for. On a paginated walk it applies to the first page only: later pages stay with the source that page chose, at the price it was quoted. Minimum: 1."""
    prompt: Required[str]
    """The question or prompt to search Google for."""
    source: NotRequired[list[str]]
    """Optional. Source ids to prefer, in order, taken from this endpoint's `lanes[].source.id` in /catalog or /apis. Omit it and the cheapest source serves, with automatic failover. Listed sources are tried first in the order given, then the others, unless `allowFallbacks` is false. A single source with `allowFallbacks` false is served only by that source at its price, quoted and charged exactly, with no failover. The price is that of the dearest source that may serve. An id that does not serve this endpoint is rejected as invalid input with no charge; a listed source that is not serving right now is refused with no charge, so omit `source` to be served by another. On a paginated walk, later pages must include the source that served page one, or omit `source`."""


class GoogleAutocompleteInput(TypedDict, total=False):
    """Input for Google Autocomplete."""

    allowFallbacks: NotRequired[bool]
    """Optional, default true. When false, only the sources listed in `source` may serve; the request is refused with no charge if none of them can. When true, the listed sources are tried first and any other source may serve after them, at the normal price. Default: true."""
    gl: NotRequired[str]
    """Two-letter country code for result localization (e.g. us, gb, de). Default: us."""
    hl: NotRequired[str]
    """Two-letter interface and results language code for the suggestions (e.g. en, es, de). Default: en."""
    ignoreSources: NotRequired[list[str]]
    """Optional. Source ids to skip for this request, taken from this endpoint's `lanes[].source.id`. The cheapest remaining source serves and the price is that of the dearest remaining source. An id that does not serve this endpoint, or that is also in `source`, is rejected as invalid input with no charge; skipping every source is rejected the same way."""
    preferLatencyUnderMs: NotRequired[int]
    """Optional; omit it and routing is unchanged, with the cheapest source serving. Prefer sources whose typical response time (median over the trailing 30 days, as published on this endpoint's lane health) is under this many milliseconds; among those, the cheapest serves. This can raise your price: when the cheapest source misses the target, a faster and dearer one serves, and you are quoted and charged its price. If no source is that fast the request is still served, by whichever source offers the best speed for its price - it is never refused for being slow. Sources we have not timed are tried last. This is a preference, not a guarantee: the median describes past requests and is not a ceiling on this one, and it excludes any wait this request itself asks for. On a paginated walk it applies to the first page only: later pages stay with the source that page chose, at the price it was quoted. Minimum: 1."""
    query: Required[str]
    """The partial Google search query."""
    source: NotRequired[list[str]]
    """Optional. Source ids to prefer, in order, taken from this endpoint's `lanes[].source.id` in /catalog or /apis. Omit it and the cheapest source serves, with automatic failover. Listed sources are tried first in the order given, then the others, unless `allowFallbacks` is false. A single source with `allowFallbacks` false is served only by that source at its price, quoted and charged exactly, with no failover. The price is that of the dearest source that may serve. An id that does not serve this endpoint is rejected as invalid input with no charge; a listed source that is not serving right now is refused with no charge, so omit `source` to be served by another. On a paginated walk, later pages must include the source that served page one, or omit `source`."""


class GoogleImagesInput(TypedDict, total=False):
    """Input for Google Images."""

    allowFallbacks: NotRequired[bool]
    """Optional, default true. When false, only the sources listed in `source` may serve; the request is refused with no charge if none of them can. When true, the listed sources are tried first and any other source may serve after them, at the normal price. Default: true."""
    autocorrect: NotRequired[bool]
    """Toggle Google spelling autocorrect (default true). Set false to search the exact query without correction."""
    gl: NotRequired[str]
    """Two-letter country code for result localization (e.g. us, gb, de). Default: us."""
    hl: NotRequired[str]
    """Two-letter interface and results language code (e.g. en, es, de). Default: en."""
    ignoreSources: NotRequired[list[str]]
    """Optional. Source ids to skip for this request, taken from this endpoint's `lanes[].source.id`. The cheapest remaining source serves and the price is that of the dearest remaining source. An id that does not serve this endpoint, or that is also in `source`, is rejected as invalid input with no charge; skipping every source is rejected the same way."""
    limit: NotRequired[int]
    """Maximum number of images to return (1-100, default 20). Requests for 10 results or fewer are billed at a lower rate than larger requests. Range: 1 to 100. Default: 20."""
    location: NotRequired[str]
    """Fine-grained location for result localization, given as a canonical Google location string (e.g. 'New York, United States', 'London, United Kingdom'). More specific than the country-level gl."""
    preferLatencyUnderMs: NotRequired[int]
    """Optional; omit it and routing is unchanged, with the cheapest source serving. Prefer sources whose typical response time (median over the trailing 30 days, as published on this endpoint's lane health) is under this many milliseconds; among those, the cheapest serves. This can raise your price: when the cheapest source misses the target, a faster and dearer one serves, and you are quoted and charged its price. If no source is that fast the request is still served, by whichever source offers the best speed for its price - it is never refused for being slow. Sources we have not timed are tried last. This is a preference, not a guarantee: the median describes past requests and is not a ceiling on this one, and it excludes any wait this request itself asks for. On a paginated walk it applies to the first page only: later pages stay with the source that page chose, at the price it was quoted. Minimum: 1."""
    query: Required[str]
    """Image search query (e.g. golden gate bridge at sunset)."""
    source: NotRequired[list[str]]
    """Optional. Source ids to prefer, in order, taken from this endpoint's `lanes[].source.id` in /catalog or /apis. Omit it and the cheapest source serves, with automatic failover. Listed sources are tried first in the order given, then the others, unless `allowFallbacks` is false. A single source with `allowFallbacks` false is served only by that source at its price, quoted and charged exactly, with no failover. The price is that of the dearest source that may serve. An id that does not serve this endpoint is rejected as invalid input with no charge; a listed source that is not serving right now is refused with no charge, so omit `source` to be served by another. On a paginated walk, later pages must include the source that served page one, or omit `source`."""
    timeframe: NotRequired[Literal["1h", "1d", "7d", "1y", "all"]]
    """Restrict results to a recent time window: 1h, 1d, 7d, 1y, or all. Default all (no time restriction)."""


class GoogleJobInput(TypedDict, total=False):
    """Input for Google Job."""

    allowFallbacks: NotRequired[bool]
    """Optional, default true. When false, only the sources listed in `source` may serve; the request is refused with no charge if none of them can. When true, the listed sources are tried first and any other source may serve after them, at the normal price. Default: true."""
    ignoreSources: NotRequired[list[str]]
    """Optional. Source ids to skip for this request, taken from this endpoint's `lanes[].source.id`. The cheapest remaining source serves and the price is that of the dearest remaining source. An id that does not serve this endpoint, or that is also in `source`, is rejected as invalid input with no charge; skipping every source is rejected the same way."""
    listingToken: Required[str]
    """The listingToken of one listing in a google.jobs response."""
    preferLatencyUnderMs: NotRequired[int]
    """Optional; omit it and routing is unchanged, with the cheapest source serving. Prefer sources whose typical response time (median over the trailing 30 days, as published on this endpoint's lane health) is under this many milliseconds; among those, the cheapest serves. This can raise your price: when the cheapest source misses the target, a faster and dearer one serves, and you are quoted and charged its price. If no source is that fast the request is still served, by whichever source offers the best speed for its price - it is never refused for being slow. Sources we have not timed are tried last. This is a preference, not a guarantee: the median describes past requests and is not a ceiling on this one, and it excludes any wait this request itself asks for. On a paginated walk it applies to the first page only: later pages stay with the source that page chose, at the price it was quoted. Minimum: 1."""
    source: NotRequired[list[str]]
    """Optional. Source ids to prefer, in order, taken from this endpoint's `lanes[].source.id` in /catalog or /apis. Omit it and the cheapest source serves, with automatic failover. Listed sources are tried first in the order given, then the others, unless `allowFallbacks` is false. A single source with `allowFallbacks` false is served only by that source at its price, quoted and charged exactly, with no failover. The price is that of the dearest source that may serve. An id that does not serve this endpoint is rejected as invalid input with no charge; a listed source that is not serving right now is refused with no charge, so omit `source` to be served by another. On a paginated walk, later pages must include the source that served page one, or omit `source`."""


class GoogleJobsInput(TypedDict, total=False):
    """Input for Google Jobs."""

    allowFallbacks: NotRequired[bool]
    """Optional, default true. When false, only the sources listed in `source` may serve; the request is refused with no charge if none of them can. When true, the listed sources are tried first and any other source may serve after them, at the normal price. Default: true."""
    cursor: NotRequired[str]
    """Opaque cursor from a previous response's nextCursor. Send it with the same query, location, gl and hl to get the next page of about 10 listings; it expires about an hour after it was issued, after which you start again from page 1."""
    gl: NotRequired[str]
    """Two-letter country code to search in (e.g. us, gb, de). Default: us."""
    hl: NotRequired[str]
    """Language code for the listings and their details (e.g. en, de, es). Default: en."""
    ignoreSources: NotRequired[list[str]]
    """Optional. Source ids to skip for this request, taken from this endpoint's `lanes[].source.id`. The cheapest remaining source serves and the price is that of the dearest remaining source. An id that does not serve this endpoint, or that is also in `source`, is rejected as invalid input with no charge; skipping every source is rejected the same way."""
    location: NotRequired[str]
    """City, region or country to search around, e.g. Chicago, IL or London. Google may include nearby places."""
    preferLatencyUnderMs: NotRequired[int]
    """Optional; omit it and routing is unchanged, with the cheapest source serving. Prefer sources whose typical response time (median over the trailing 30 days, as published on this endpoint's lane health) is under this many milliseconds; among those, the cheapest serves. This can raise your price: when the cheapest source misses the target, a faster and dearer one serves, and you are quoted and charged its price. If no source is that fast the request is still served, by whichever source offers the best speed for its price - it is never refused for being slow. Sources we have not timed are tried last. This is a preference, not a guarantee: the median describes past requests and is not a ceiling on this one, and it excludes any wait this request itself asks for. On a paginated walk it applies to the first page only: later pages stay with the source that page chose, at the price it was quoted. Minimum: 1."""
    query: Required[str]
    """Job title or keywords to search, e.g. registered nurse. A place written into the query ("barista in Austin, TX") also localizes the search."""
    source: NotRequired[list[str]]
    """Optional. Source ids to prefer, in order, taken from this endpoint's `lanes[].source.id` in /catalog or /apis. Omit it and the cheapest source serves, with automatic failover. Listed sources are tried first in the order given, then the others, unless `allowFallbacks` is false. A single source with `allowFallbacks` false is served only by that source at its price, quoted and charged exactly, with no failover. The price is that of the dearest source that may serve. An id that does not serve this endpoint is rejected as invalid input with no charge; a listed source that is not serving right now is refused with no charge, so omit `source` to be served by another. On a paginated walk, later pages must include the source that served page one, or omit `source`."""


class GoogleLensInput(TypedDict, total=False):
    """Input for Google Lens."""

    allowFallbacks: NotRequired[bool]
    """Optional, default true. When false, only the sources listed in `source` may serve; the request is refused with no charge if none of them can. When true, the listed sources are tried first and any other source may serve after them, at the normal price. Default: true."""
    ignoreSources: NotRequired[list[str]]
    """Optional. Source ids to skip for this request, taken from this endpoint's `lanes[].source.id`. The cheapest remaining source serves and the price is that of the dearest remaining source. An id that does not serve this endpoint, or that is also in `source`, is rejected as invalid input with no charge; skipping every source is rejected the same way."""
    preferLatencyUnderMs: NotRequired[int]
    """Optional; omit it and routing is unchanged, with the cheapest source serving. Prefer sources whose typical response time (median over the trailing 30 days, as published on this endpoint's lane health) is under this many milliseconds; among those, the cheapest serves. This can raise your price: when the cheapest source misses the target, a faster and dearer one serves, and you are quoted and charged its price. If no source is that fast the request is still served, by whichever source offers the best speed for its price - it is never refused for being slow. Sources we have not timed are tried last. This is a preference, not a guarantee: the median describes past requests and is not a ceiling on this one, and it excludes any wait this request itself asks for. On a paginated walk it applies to the first page only: later pages stay with the source that page chose, at the price it was quoted. Minimum: 1."""
    source: NotRequired[list[str]]
    """Optional. Source ids to prefer, in order, taken from this endpoint's `lanes[].source.id` in /catalog or /apis. Omit it and the cheapest source serves, with automatic failover. Listed sources are tried first in the order given, then the others, unless `allowFallbacks` is false. A single source with `allowFallbacks` false is served only by that source at its price, quoted and charged exactly, with no failover. The price is that of the dearest source that may serve. An id that does not serve this endpoint is rejected as invalid input with no charge; a listed source that is not serving right now is refused with no charge, so omit `source` to be served by another. On a paginated walk, later pages must include the source that served page one, or omit `source`."""
    url: Required[str]
    """Public URL of the image to search with."""


class GoogleLocalServicesInput(TypedDict, total=False):
    """Input for Google Local Services."""

    allowFallbacks: NotRequired[bool]
    """Optional, default true. When false, only the sources listed in `source` may serve; the request is refused with no charge if none of them can. When true, the listed sources are tried first and any other source may serve after them, at the normal price. Default: true."""
    ignoreSources: NotRequired[list[str]]
    """Optional. Source ids to skip for this request, taken from this endpoint's `lanes[].source.id`. The cheapest remaining source serves and the price is that of the dearest remaining source. An id that does not serve this endpoint, or that is also in `source`, is rejected as invalid input with no charge; skipping every source is rejected the same way."""
    limit: NotRequired[int]
    """Maximum number of businesses to return (1-20, default 20). Google lists at most 20 businesses for one service in one city, so there are no further pages. Range: 1 to 20."""
    location: Required[str]
    """The US city to search, with its state (e.g. Denver, CO or Austin, TX)."""
    preferLatencyUnderMs: NotRequired[int]
    """Optional; omit it and routing is unchanged, with the cheapest source serving. Prefer sources whose typical response time (median over the trailing 30 days, as published on this endpoint's lane health) is under this many milliseconds; among those, the cheapest serves. This can raise your price: when the cheapest source misses the target, a faster and dearer one serves, and you are quoted and charged its price. If no source is that fast the request is still served, by whichever source offers the best speed for its price - it is never refused for being slow. Sources we have not timed are tried last. This is a preference, not a guarantee: the median describes past requests and is not a ceiling on this one, and it excludes any wait this request itself asks for. On a paginated walk it applies to the first page only: later pages stay with the source that page chose, at the price it was quoted. Minimum: 1."""
    query: Required[str]
    """The service to find businesses for, in everyday words (e.g. plumber, electrician, house cleaning, roofer)."""
    requireFields: NotRequired[
        list[
            Literal[
                "highlights",
                "hours",
                "image",
                "isOpenNow",
                "responseTime",
                "yearsInBusiness",
            ]
        ]
    ]
    """Optional; omit it and routing is unchanged, with the cheapest source serving. Name the output fields this request must be able to return, for example `yearsInBusiness` or `hours`, and it is served only by a source that returns every one of them. Fields you do not name are still returned whenever the serving source has them. This can raise your price: when the cheapest source cannot return a named field, a dearer source serves, and you are quoted and charged its price. A named field can still be null on a business that genuinely lacks it. Naming a combination that no single source returns together is refused as invalid input, with no charge."""
    source: NotRequired[list[str]]
    """Optional. Source ids to prefer, in order, taken from this endpoint's `lanes[].source.id` in /catalog or /apis. Omit it and the cheapest source serves, with automatic failover. Listed sources are tried first in the order given, then the others, unless `allowFallbacks` is false. A single source with `allowFallbacks` false is served only by that source at its price, quoted and charged exactly, with no failover. The price is that of the dearest source that may serve. An id that does not serve this endpoint is rejected as invalid input with no charge; a listed source that is not serving right now is refused with no charge, so omit `source` to be served by another. On a paginated walk, later pages must include the source that served page one, or omit `source`."""


class GoogleNewsInput(TypedDict, total=False):
    """Input for Google News."""

    allowFallbacks: NotRequired[bool]
    """Optional, default true. When false, only the sources listed in `source` may serve; the request is refused with no charge if none of them can. When true, the listed sources are tried first and any other source may serve after them, at the normal price. Default: true."""
    gl: NotRequired[str]
    """Two-letter country code for result localization (e.g. us, gb, de). Default: us."""
    hl: NotRequired[str]
    """Two-letter interface and results language code (e.g. en, es, de). Default: en."""
    ignoreSources: NotRequired[list[str]]
    """Optional. Source ids to skip for this request, taken from this endpoint's `lanes[].source.id`. The cheapest remaining source serves and the price is that of the dearest remaining source. An id that does not serve this endpoint, or that is also in `source`, is rejected as invalid input with no charge; skipping every source is rejected the same way."""
    limit: NotRequired[int]
    """Requested article count (1-20, default 20). Google News returns its latest matching articles and may return more or fewer than requested. Price is flat per request. Range: 1 to 20."""
    location: NotRequired[str]
    """Fine-grained location for result localization, given as a canonical Google location string (e.g. 'New York, United States', 'London, United Kingdom'). More specific than the country-level gl."""
    preferLatencyUnderMs: NotRequired[int]
    """Optional; omit it and routing is unchanged, with the cheapest source serving. Prefer sources whose typical response time (median over the trailing 30 days, as published on this endpoint's lane health) is under this many milliseconds; among those, the cheapest serves. This can raise your price: when the cheapest source misses the target, a faster and dearer one serves, and you are quoted and charged its price. If no source is that fast the request is still served, by whichever source offers the best speed for its price - it is never refused for being slow. Sources we have not timed are tried last. This is a preference, not a guarantee: the median describes past requests and is not a ceiling on this one, and it excludes any wait this request itself asks for. On a paginated walk it applies to the first page only: later pages stay with the source that page chose, at the price it was quoted. Minimum: 1."""
    query: Required[str]
    """News search query; supports operators like '-', 'OR', and 'site:' (e.g. bitcoin site:cnn.com)."""
    source: NotRequired[list[str]]
    """Optional. Source ids to prefer, in order, taken from this endpoint's `lanes[].source.id` in /catalog or /apis. Omit it and the cheapest source serves, with automatic failover. Listed sources are tried first in the order given, then the others, unless `allowFallbacks` is false. A single source with `allowFallbacks` false is served only by that source at its price, quoted and charged exactly, with no failover. The price is that of the dearest source that may serve. An id that does not serve this endpoint is rejected as invalid input with no charge; a listed source that is not serving right now is refused with no charge, so omit `source` to be served by another. On a paginated walk, later pages must include the source that served page one, or omit `source`."""
    timeframe: NotRequired[str]
    """How far back to search, written as a count plus a unit: h hours, d days, w weeks, m months, y years. So 2h is the last two hours, 30d the last thirty days, 6m the last six months. Omit this field, or send 'all', to search without a time limit."""


class GooglePatentsInput(TypedDict, total=False):
    """Input for Google Patents."""

    allowFallbacks: NotRequired[bool]
    """Optional, default true. When false, only the sources listed in `source` may serve; the request is refused with no charge if none of them can. When true, the listed sources are tried first and any other source may serve after them, at the normal price. Default: true."""
    ignoreSources: NotRequired[list[str]]
    """Optional. Source ids to skip for this request, taken from this endpoint's `lanes[].source.id`. The cheapest remaining source serves and the price is that of the dearest remaining source. An id that does not serve this endpoint, or that is also in `source`, is rejected as invalid input with no charge; skipping every source is rejected the same way."""
    preferLatencyUnderMs: NotRequired[int]
    """Optional; omit it and routing is unchanged, with the cheapest source serving. Prefer sources whose typical response time (median over the trailing 30 days, as published on this endpoint's lane health) is under this many milliseconds; among those, the cheapest serves. This can raise your price: when the cheapest source misses the target, a faster and dearer one serves, and you are quoted and charged its price. If no source is that fast the request is still served, by whichever source offers the best speed for its price - it is never refused for being slow. Sources we have not timed are tried last. This is a preference, not a guarantee: the median describes past requests and is not a ceiling on this one, and it excludes any wait this request itself asks for. On a paginated walk it applies to the first page only: later pages stay with the source that page chose, at the price it was quoted. Minimum: 1."""
    query: Required[str]
    """The Google Patents search query."""
    source: NotRequired[list[str]]
    """Optional. Source ids to prefer, in order, taken from this endpoint's `lanes[].source.id` in /catalog or /apis. Omit it and the cheapest source serves, with automatic failover. Listed sources are tried first in the order given, then the others, unless `allowFallbacks` is false. A single source with `allowFallbacks` false is served only by that source at its price, quoted and charged exactly, with no failover. The price is that of the dearest source that may serve. An id that does not serve this endpoint is rejected as invalid input with no charge; a listed source that is not serving right now is refused with no charge, so omit `source` to be served by another. On a paginated walk, later pages must include the source that served page one, or omit `source`."""


class GoogleScholarInput(TypedDict, total=False):
    """Input for Google Scholar."""

    allowFallbacks: NotRequired[bool]
    """Optional, default true. When false, only the sources listed in `source` may serve; the request is refused with no charge if none of them can. When true, the listed sources are tried first and any other source may serve after them, at the normal price. Default: true."""
    ignoreSources: NotRequired[list[str]]
    """Optional. Source ids to skip for this request, taken from this endpoint's `lanes[].source.id`. The cheapest remaining source serves and the price is that of the dearest remaining source. An id that does not serve this endpoint, or that is also in `source`, is rejected as invalid input with no charge; skipping every source is rejected the same way."""
    preferLatencyUnderMs: NotRequired[int]
    """Optional; omit it and routing is unchanged, with the cheapest source serving. Prefer sources whose typical response time (median over the trailing 30 days, as published on this endpoint's lane health) is under this many milliseconds; among those, the cheapest serves. This can raise your price: when the cheapest source misses the target, a faster and dearer one serves, and you are quoted and charged its price. If no source is that fast the request is still served, by whichever source offers the best speed for its price - it is never refused for being slow. Sources we have not timed are tried last. This is a preference, not a guarantee: the median describes past requests and is not a ceiling on this one, and it excludes any wait this request itself asks for. On a paginated walk it applies to the first page only: later pages stay with the source that page chose, at the price it was quoted. Minimum: 1."""
    query: Required[str]
    """The Google Scholar search query."""
    requireFields: NotRequired[list[Literal["year"]]]
    """Optional; omit it and routing is unchanged, with the cheapest source serving. Name the output fields this request must be able to return, for example `year`, and it is served only by a source that returns every one of them. Fields you do not name are still returned whenever the serving source has them. This can raise your price: when the cheapest source cannot return a named field, a dearer source serves, and you are quoted and charged its price. A named field can still be absent on a record that genuinely lacks it. Naming a combination that no single source returns together is refused as invalid input, with no charge."""
    source: NotRequired[list[str]]
    """Optional. Source ids to prefer, in order, taken from this endpoint's `lanes[].source.id` in /catalog or /apis. Omit it and the cheapest source serves, with automatic failover. Listed sources are tried first in the order given, then the others, unless `allowFallbacks` is false. A single source with `allowFallbacks` false is served only by that source at its price, quoted and charged exactly, with no failover. The price is that of the dearest source that may serve. An id that does not serve this endpoint is rejected as invalid input with no charge; a listed source that is not serving right now is refused with no charge, so omit `source` to be served by another. On a paginated walk, later pages must include the source that served page one, or omit `source`."""


class GoogleSearchInput(TypedDict, total=False):
    """Input for Google Search."""

    allowFallbacks: NotRequired[bool]
    """Optional, default true. When false, only the sources listed in `source` may serve; the request is refused with no charge if none of them can. When true, the listed sources are tried first and any other source may serve after them, at the normal price. Default: true."""
    autocorrect: NotRequired[bool]
    """Toggle Google spelling autocorrect (default true). Set false to search the exact query without correction."""
    cursor: NotRequired[str]
    """Deprecated: send page instead. A continuation token from an earlier response's nextCursor is still accepted and still continues on the source that issued it; page is ignored when cursor is sent alongside it."""
    gl: NotRequired[str]
    """Two-letter country code for result localization (e.g. us, gb, de). Default: us."""
    hl: NotRequired[str]
    """Two-letter interface and results language code (e.g. en, es, de). Default: en."""
    ignoreSources: NotRequired[list[str]]
    """Optional. Source ids to skip for this request, taken from this endpoint's `lanes[].source.id`. The cheapest remaining source serves and the price is that of the dearest remaining source. An id that does not serve this endpoint, or that is also in `source`, is rejected as invalid input with no charge; skipping every source is rejected the same way."""
    limit: NotRequired[int]
    """Page size to ask for. Google returns about 10 organic results per page and stopped honoring larger counts in September 2025, so a limit above 10 still returns about 10. Some sources return their whole page of about 10 whatever limit says: a page is never trimmed after the call, so nextCursor always continues exactly where this response ended. To go deeper, send page (about 10 results per page, each billed as a request) or use google.search_100, which returns up to 100 ranked results in a single call for one flat charge and is cheaper past roughly 20 results. Price is flat per request. Range: 1 to 100. Default: 10."""
    location: NotRequired[str]
    """Fine-grained location to localize results to, more specific than the country-level gl. Send it as an Active Canonical Name from Google's geo-target list: place, then each parent region, then country, with no space after each comma, e.g. 'New York,New York,United States', 'Austin,Texas,United States', 'London,England,United Kingdom'. Common variations are translated to that name when they point to exactly one place: spaces after commas, missing accents, a US state abbreviation ('Orlando, FL, United States'), or a skipped region ('Sydney, Australia'). A value that names no place, or more than one, is rejected rather than quietly searched from somewhere else."""
    page: NotRequired[int]
    """Which page of about 10 organic results to return, starting at 1. Send page 2, 3, ... to walk deeper; each page is billed as one request and any source can serve any page. Replaces cursor. Minimum: 1. Default: 1."""
    preferLatencyUnderMs: NotRequired[int]
    """Optional; omit it and routing is unchanged, with the cheapest source serving. Prefer sources whose typical response time (median over the trailing 30 days, as published on this endpoint's lane health) is under this many milliseconds; among those, the cheapest serves. This can raise your price: when the cheapest source misses the target, a faster and dearer one serves, and you are quoted and charged its price. If no source is that fast the request is still served, by whichever source offers the best speed for its price - it is never refused for being slow. Sources we have not timed are tried last. This is a preference, not a guarantee: the median describes past requests and is not a ceiling on this one, and it excludes any wait this request itself asks for. On a paginated walk it applies to the first page only: later pages stay with the source that page chose, at the price it was quoted. Minimum: 1."""
    query: Required[str]
    """The Google search query."""
    requireCursor: NotRequired[bool]
    """Deprecated. Every source for this search returns a nextCursor, so this changes nothing about the price or which source serves you; it stays accepted so callers that already send it keep working."""
    source: NotRequired[list[str]]
    """Optional. Source ids to prefer, in order, taken from this endpoint's `lanes[].source.id` in /catalog or /apis. Omit it and the cheapest source serves, with automatic failover. Listed sources are tried first in the order given, then the others, unless `allowFallbacks` is false. A single source with `allowFallbacks` false is served only by that source at its price, quoted and charged exactly, with no failover. The price is that of the dearest source that may serve. An id that does not serve this endpoint is rejected as invalid input with no charge; a listed source that is not serving right now is refused with no charge, so omit `source` to be served by another. On a paginated walk, later pages must include the source that served page one, or omit `source`."""
    timeframe: NotRequired[Literal["1h", "1d", "7d", "1y", "all"]]
    """Restrict results to a recent time window: 1h, 1d, 7d, 1y, or all. Default all (no time restriction)."""


class GoogleSearch100Input(TypedDict, total=False):
    """Input for Google Search Top 100."""

    allowFallbacks: NotRequired[bool]
    """Optional, default true. When false, only the sources listed in `source` may serve; the request is refused with no charge if none of them can. When true, the listed sources are tried first and any other source may serve after them, at the normal price. Default: true."""
    autocorrect: NotRequired[bool]
    """Toggle Google spelling autocorrect (default true). Set false to search the exact query without correction."""
    gl: NotRequired[str]
    """Two-letter country code for result localization (e.g. us, gb, de). Default: us."""
    hl: NotRequired[str]
    """Two-letter interface and results language code (e.g. en, es, de). Default: en."""
    ignoreSources: NotRequired[list[str]]
    """Optional. Source ids to skip for this request, taken from this endpoint's `lanes[].source.id`. The cheapest remaining source serves and the price is that of the dearest remaining source. An id that does not serve this endpoint, or that is also in `source`, is rejected as invalid input with no charge; skipping every source is rejected the same way."""
    preferLatencyUnderMs: NotRequired[int]
    """Optional; omit it and routing is unchanged, with the cheapest source serving. Prefer sources whose typical response time (median over the trailing 30 days, as published on this endpoint's lane health) is under this many milliseconds; among those, the cheapest serves. This can raise your price: when the cheapest source misses the target, a faster and dearer one serves, and you are quoted and charged its price. If no source is that fast the request is still served, by whichever source offers the best speed for its price - it is never refused for being slow. Sources we have not timed are tried last. This is a preference, not a guarantee: the median describes past requests and is not a ceiling on this one, and it excludes any wait this request itself asks for. On a paginated walk it applies to the first page only: later pages stay with the source that page chose, at the price it was quoted. Minimum: 1."""
    query: Required[str]
    """The Google search query."""
    source: NotRequired[list[str]]
    """Optional. Source ids to prefer, in order, taken from this endpoint's `lanes[].source.id` in /catalog or /apis. Omit it and the cheapest source serves, with automatic failover. Listed sources are tried first in the order given, then the others, unless `allowFallbacks` is false. A single source with `allowFallbacks` false is served only by that source at its price, quoted and charged exactly, with no failover. The price is that of the dearest source that may serve. An id that does not serve this endpoint is rejected as invalid input with no charge; a listed source that is not serving right now is refused with no charge, so omit `source` to be served by another. On a paginated walk, later pages must include the source that served page one, or omit `source`."""
    timeframe: NotRequired[Literal["1h", "1d", "7d", "1y", "all"]]
    """Restrict results to a recent time window: 1h, 1d, 7d, 1y, or all. Default all (no time restriction)."""


class GoogleTrendsInput(TypedDict, total=False):
    """Input for Google Trends."""

    allowFallbacks: NotRequired[bool]
    """Optional, default true. When false, only the sources listed in `source` may serve; the request is refused with no charge if none of them can. When true, the listed sources are tried first and any other source may serve after them, at the normal price. Default: true."""
    geo: NotRequired[str]
    """Where the searches came from: an uppercase ISO country code (US, GB, DE) or a country subdivision (US-CA, GB-ENG). Omit it, or send worldwide, for worldwide interest. Default: worldwide."""
    ignoreSources: NotRequired[list[str]]
    """Optional. Source ids to skip for this request, taken from this endpoint's `lanes[].source.id`. The cheapest remaining source serves and the price is that of the dearest remaining source. An id that does not serve this endpoint, or that is also in `source`, is rejected as invalid input with no charge; skipping every source is rejected the same way."""
    keywords: Required[list[str]]
    """Search terms to compare, 1 to 5, each 2 to 100 characters and without commas (e.g. ["coffee", "tea"]). Values are relative across the whole set, so the same term scores differently next to different terms."""
    preferLatencyUnderMs: NotRequired[int]
    """Optional; omit it and routing is unchanged, with the cheapest source serving. Prefer sources whose typical response time (median over the trailing 30 days, as published on this endpoint's lane health) is under this many milliseconds; among those, the cheapest serves. This can raise your price: when the cheapest source misses the target, a faster and dearer one serves, and you are quoted and charged its price. If no source is that fast the request is still served, by whichever source offers the best speed for its price - it is never refused for being slow. Sources we have not timed are tried last. This is a preference, not a guarantee: the median describes past requests and is not a ceiling on this one, and it excludes any wait this request itself asks for. On a paginated walk it applies to the first page only: later pages stay with the source that page chose, at the price it was quoted. Minimum: 1."""
    source: NotRequired[list[str]]
    """Optional. Source ids to prefer, in order, taken from this endpoint's `lanes[].source.id` in /catalog or /apis. Omit it and the cheapest source serves, with automatic failover. Listed sources are tried first in the order given, then the others, unless `allowFallbacks` is false. A single source with `allowFallbacks` false is served only by that source at its price, quoted and charged exactly, with no failover. The price is that of the dearest source that may serve. An id that does not serve this endpoint is rejected as invalid input with no charge; a listed source that is not serving right now is refused with no charge, so omit `source` to be served by another. On a paginated walk, later pages must include the source that served page one, or omit `source`."""
    timeframe: NotRequired[
        Literal["1h", "4h", "1d", "7d", "1m", "3m", "12m", "5y", "all"]
    ]
    """The window to chart, ending now: 1h, 4h, 1d or 7d (hours and days), 1m or 3m (months), 12m, 5y, or all (back to January 2004). Buckets grow with the window: minutes up to 1d, hours for 7d, days for 1m and 3m, weeks for 12m and 5y, months for all. Default: 12m."""


class GoogleVideosInput(TypedDict, total=False):
    """Input for Google Videos."""

    allowFallbacks: NotRequired[bool]
    """Optional, default true. When false, only the sources listed in `source` may serve; the request is refused with no charge if none of them can. When true, the listed sources are tried first and any other source may serve after them, at the normal price. Default: true."""
    autocorrect: NotRequired[bool]
    """Toggle Google spelling autocorrect (default true). Set false to search the exact query without correction."""
    gl: NotRequired[str]
    """Two-letter country code for result localization (e.g. us, gb, de). Default: us."""
    hl: NotRequired[str]
    """Two-letter interface and results language code (e.g. en, es, de). Default: en."""
    ignoreSources: NotRequired[list[str]]
    """Optional. Source ids to skip for this request, taken from this endpoint's `lanes[].source.id`. The cheapest remaining source serves and the price is that of the dearest remaining source. An id that does not serve this endpoint, or that is also in `source`, is rejected as invalid input with no charge; skipping every source is rejected the same way."""
    location: NotRequired[str]
    """Fine-grained location for result localization, given as a canonical Google location string (e.g. 'New York, United States', 'London, United Kingdom'). More specific than the country-level gl."""
    preferLatencyUnderMs: NotRequired[int]
    """Optional; omit it and routing is unchanged, with the cheapest source serving. Prefer sources whose typical response time (median over the trailing 30 days, as published on this endpoint's lane health) is under this many milliseconds; among those, the cheapest serves. This can raise your price: when the cheapest source misses the target, a faster and dearer one serves, and you are quoted and charged its price. If no source is that fast the request is still served, by whichever source offers the best speed for its price - it is never refused for being slow. Sources we have not timed are tried last. This is a preference, not a guarantee: the median describes past requests and is not a ceiling on this one, and it excludes any wait this request itself asks for. On a paginated walk it applies to the first page only: later pages stay with the source that page chose, at the price it was quoted. Minimum: 1."""
    query: Required[str]
    """The video search query."""
    requireFields: NotRequired[list[Literal["source"]]]
    """Optional; omit it and routing is unchanged, with the cheapest source serving. Name the output fields this request must be able to return, for example `source`, and it is served only by a source that returns every one of them. Fields you do not name are still returned whenever the serving source has them. This can raise your price: when the cheapest source cannot return a named field, a dearer source serves, and you are quoted and charged its price. A named field can still be absent on a record that genuinely lacks it. Naming a combination that no single source returns together is refused as invalid input, with no charge."""
    source: NotRequired[list[str]]
    """Optional. Source ids to prefer, in order, taken from this endpoint's `lanes[].source.id` in /catalog or /apis. Omit it and the cheapest source serves, with automatic failover. Listed sources are tried first in the order given, then the others, unless `allowFallbacks` is false. A single source with `allowFallbacks` false is served only by that source at its price, quoted and charged exactly, with no failover. The price is that of the dearest source that may serve. An id that does not serve this endpoint is rejected as invalid input with no charge; a listed source that is not serving right now is refused with no charge, so omit `source` to be served by another. On a paginated walk, later pages must include the source that served page one, or omit `source`."""
    timeframe: NotRequired[Literal["1h", "1d", "7d", "1y", "all"]]
    """Restrict results to a recent time window: 1h, 1d, 7d, 1y, or all. Default all (no time restriction)."""


class GoogleAiModeData(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    answer: str = Field(
        description="The answer as plain text, as Google generated it for this search. Length and coverage vary between searches on the same prompt. Populated whenever the provider has data for the entity."
    )
    answer_markdown: str = Field(
        alias="answerMarkdown",
        description="The answer in Markdown when Google returns a Markdown rendering, otherwise the same text as answer. Populated whenever the provider has data for the entity.",
    )
    citations: list[GoogleAiModeCitation] = Field(
        description="The sources Google cited for this search, in the order it returned them. Google recomputes the set per search, so counts and membership vary between calls on the same prompt."
    )
    prompt: str = Field(
        description="The prompt answered by the upstream search experience. Populated whenever the provider has data for the entity."
    )


class GoogleAiModeCitation(BaseModel):
    model_config = ConfigDict(extra="allow")

    title: str = Field(description="The cited source title.")
    url: str = Field(description="The cited source URL.")


class GoogleAiOverviewData(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    answer: str = Field(
        description="The AI Overview answer as plain text, as generated for this scrape. Populated whenever the provider has data for the entity."
    )
    answer_markdown: str = Field(
        alias="answerMarkdown",
        description="The same answer in Markdown, preserving the headings and lists Google rendered. Populated whenever the provider has data for the entity.",
    )
    citations: list[GoogleAiOverviewCitation] = Field(
        description="Every source Google listed with a usable URL for this overview, in Google's own order. References without a URL are omitted. This is the full list behind the overview, not only the few sources Google renders inline before the list is expanded, so it is routinely longer than what a reader sees at a glance."
    )
    language: str | None = Field(
        default=None,
        description="Two-letter language code the overview was generated in.",
    )
    prompt: str = Field(
        description="The prompt Google answered. Populated whenever the provider has data for the entity."
    )
    scraped_at: str | None = Field(
        default=None,
        alias="scrapedAt",
        description="When this overview was captured, ISO 8601 UTC. Because Google regenerates the overview per search, this identifies which generation the other fields describe.",
    )


class GoogleAiOverviewCitation(BaseModel):
    model_config = ConfigDict(extra="allow")

    index: int | None = Field(
        default=None,
        description="Google's position for this source within the overview, starting at 1.",
    )
    title: str = Field(
        description="The cited source title as Google presented it, which may carry a trailing date and snippet."
    )
    url: str = Field(description="The cited source URL.")


class GoogleAiOverviewPreviewData(BaseModel):
    answer: str = Field(
        description="The overview text visible before Show more, as plain text. Google cuts the preview where the fold falls, so it often ends mid-sentence. When Google shows the whole overview with no Show more button, this is the whole overview. Populated whenever the provider has data for the entity."
    )
    citations: list[GoogleAiOverviewPreviewCitation] = Field(
        description="The sources linked in the visible part of the overview, in page order. This is only what shows before Show more, so it is usually shorter than the full source list google.ai_overview returns. Populated whenever the provider has data for the entity."
    )
    prompt: str = Field(
        description="The prompt Google answered. Populated whenever the provider has data for the entity."
    )


class GoogleAiOverviewPreviewCitation(BaseModel):
    model_config = ConfigDict(extra="allow")

    index: int | None = Field(
        default=None,
        description="The link's position in the visible overview, starting at 1.",
    )
    title: str = Field(
        description="The link text or source name Google showed. Empty when Google showed the link without text."
    )
    url: str = Field(description="The linked source URL.")


class GoogleAutocompleteData(BaseModel):
    query: str = Field(description="The partial query that was searched.")
    suggestions: list[GoogleAutocompleteSuggestion] = Field(
        description="Autocomplete suggestion records. Populated whenever the provider has data for the entity."
    )


class GoogleAutocompleteSuggestion(BaseModel):
    model_config = ConfigDict(extra="allow")

    value: str = Field(
        description="Suggested query text. Populated whenever the provider has data for the entity."
    )


class GoogleImagesData(BaseModel):
    items: list[GoogleImagesItem] = Field(
        description="Image result records: image URL, dimensions, title, and the source page it appears on. Populated whenever the provider has data for the entity."
    )


class GoogleImagesItem(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    height: int | None = Field(default=None, description="Full image height in pixels.")
    position: int | None = Field(
        default=None,
        description="One-based position of this image in Google's result order.",
    )
    source: str | None = Field(
        default=None,
        description="Host domain of the page the image appears on. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    source_url: str | None = Field(
        default=None,
        alias="sourceUrl",
        description="URL of the page the image appears on. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    thumbnail_url: str | None = Field(
        default=None,
        alias="thumbnailUrl",
        description="URL to a thumbnail of the image.",
    )
    title: str = Field(
        description="Image result title. Populated whenever the provider has data for the entity."
    )
    url: str = Field(
        description="Direct URL to the full-size image. Populated whenever the provider has data for the entity."
    )
    width: int | None = Field(default=None, description="Full image width in pixels.")


class GoogleJobData(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    apply_options: list[GoogleJobApplyOption] | None = Field(
        default=None,
        alias="applyOptions",
        description="Where the job can be applied for. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    company_name: str | None = Field(
        default=None,
        alias="companyName",
        description="Hiring company. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    company_ratings: list[GoogleJobCompanyRating] | None = Field(
        default=None,
        alias="companyRatings",
        description="The employer's ratings on review sites, as Google shows them; empty when Google shows none.",
    )
    description: str | None = Field(
        default=None,
        description="The whole job description Google holds, as plain text. A few postings reach Google already shortened by the job board and end in [...]. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    extensions: list[str] | None = Field(
        default=None,
        description='The posting details Google shows, in its order and wording, e.g. ["7 days ago", "Full-time", "Health insurance"]: when it was posted, pay, job type and benefits, each only when Google shows it.',
    )
    job_id: str | None = Field(
        default=None, alias="jobId", description="Google's id for the listing."
    )
    location: str | None = Field(
        default=None, description="Job location as Google shows it, e.g. Chicago, IL."
    )
    title: str = Field(
        description="Job title. Populated whenever the provider has data for the entity."
    )
    via: str | None = Field(
        default=None,
        description="The site Google found the listing on, e.g. LinkedIn or Indeed.",
    )


class GoogleJobApplyOption(BaseModel):
    model_config = ConfigDict(extra="allow")

    title: str | None = Field(
        default=None, description="Label, e.g. Apply on LinkedIn."
    )
    url: str | None = Field(
        default=None,
        description="Apply link with Google's tracking parameters removed.",
    )


class GoogleJobCompanyRating(BaseModel):
    model_config = ConfigDict(extra="allow")

    rating: float | None = Field(
        default=None, description="Employer star rating on that site."
    )
    reviews: int | None = Field(
        default=None,
        description="Number of reviews on that site. Rounded when Google shows an abbreviated count: 8.9K becomes 8900.",
    )
    source: str | None = Field(
        default=None, description="Review site, e.g. Glassdoor or Indeed."
    )
    url: str | None = Field(
        default=None,
        description="The employer's page on that site, with Google's tracking parameters removed.",
    )


class GoogleJobsData(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    items: list[GoogleJobsItem] = Field(
        description="Job listings in Google's order. Populated whenever the provider has data for the entity."
    )
    next_cursor: str | None = Field(
        default=None,
        alias="nextCursor",
        description="Opaque cursor for the next page of listings, or null when there are no more. Pass it back as cursor with the same query, location, gl and hl.",
    )


class GoogleJobsItem(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    apply_options: list[GoogleJobsApplyOption] | None = Field(
        default=None,
        alias="applyOptions",
        description="Where the job can be applied for. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    company_name: str | None = Field(
        default=None,
        alias="companyName",
        description="Hiring company. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    description: str | None = Field(
        default=None,
        description="Job description as plain text. Usually the full text, but for some listings (seen on German searches) Google shows only an excerpt of about 400 characters that can stop mid-word; google.job with this listing's listingToken returns the whole description Google holds. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    extensions: list[str] | None = Field(
        default=None,
        description='The posting details Google shows, in its order and wording, e.g. ["2 days ago", "36.50-58.40 an hour", "Full-time", "Health insurance"]: when it was posted, pay, job type and benefits, each only when Google shows it. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.',
    )
    job_id: str | None = Field(
        default=None,
        alias="jobId",
        description="Google's id for the listing. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    listing_token: str | None = Field(
        default=None,
        alias="listingToken",
        description="Token for this listing; pass it to google.job as listingToken for the listing with employer ratings. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    location: str | None = Field(
        default=None,
        description="Job location as Google shows it, e.g. Chicago, IL. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    position: int | None = Field(
        default=None,
        description="1-based rank of the listing across pages (page 2 starts at 11).",
    )
    title: str = Field(
        description="Job title. Populated whenever the provider has data for the entity."
    )
    via: str | None = Field(
        default=None,
        description="The site Google found the listing on, e.g. LinkedIn or Indeed. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )


class GoogleJobsApplyOption(BaseModel):
    model_config = ConfigDict(extra="allow")

    title: str | None = Field(
        default=None, description="Label, e.g. Apply on LinkedIn."
    )
    url: str | None = Field(
        default=None,
        description="Apply link with Google's tracking parameters removed.",
    )


class GoogleLensData(BaseModel):
    results: list[GoogleLensResult] = Field(
        description="Visual match result records. Populated whenever the provider has data for the entity."
    )
    url: str = Field(description="The input image URL that was searched.")


class GoogleLensResult(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    image: str | None = Field(default=None, description="Matched image URL.")
    link: str = Field(
        description="URL to the matching web page. Populated whenever the provider has data for the entity."
    )
    source: str | None = Field(default=None, description="Source site name.")
    thumbnail_url: str | None = Field(
        default=None,
        alias="thumbnailUrl",
        description="Thumbnail image URL for the match.",
    )
    title: str = Field(
        description="Title of the matching web page. Populated whenever the provider has data for the entity."
    )


class GoogleLocalServicesData(BaseModel):
    items: list[GoogleLocalServicesItem] = Field(
        description="Businesses Google lists in Local Services ads for the service and location, in Google's order. Populated whenever the provider has data for the entity."
    )


class GoogleLocalServicesItem(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    bid: str | None = Field(
        default=None,
        description="Google Local Services business id (bid). Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    category: str | None = Field(
        default=None,
        description="Google's service category for the business (e.g. Plumbers, Electricians). Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    cid: str | None = Field(
        default=None,
        description="Google customer id (cid) of the business. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    highlights: list[str] | None = Field(
        default=None,
        description="Selling points the business lists, such as Flat rate pricing or Free in-home estimate. Null when this source does not report them.",
    )
    hours: str | None = Field(
        default=None,
        description="Opening status as Google shows it at request time (e.g. Open 24 hours). Null when this source does not report it.",
    )
    image: str | None = Field(
        default=None,
        description="Business logo or photo URL. Null when the business has none or this source does not report it.",
    )
    is_open_now: bool | None = Field(
        default=None,
        alias="isOpenNow",
        description="Whether the business was open when the request ran, as Google shows it. Null when this source does not report it.",
    )
    name: str = Field(
        description="Business name. Populated whenever the provider has data for the entity."
    )
    phone: str | None = Field(
        default=None,
        description="Business phone number in E.164 format (e.g. +17205550123). Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    pid: str | None = Field(
        default=None,
        description="Google Local Services provider id (pid). Null when Google assigns none, which is common.",
    )
    position: int | None = Field(
        default=None,
        description="1-based position of the business in Google's list. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    profile_url: str | None = Field(
        default=None,
        alias="profileUrl",
        description="The business's Google Local Services profile page. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    rating: float | None = Field(
        default=None,
        description="Average Google star rating out of 5. Null for a business with no reviews yet. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    response_time: str | None = Field(
        default=None,
        alias="responseTime",
        description="How quickly the business usually replies, as Google shows it (e.g. Typically replies in 15 min). Null when Google shows none or this source does not report it.",
    )
    review_count: int | None = Field(
        default=None,
        alias="reviewCount",
        description="Number of Google reviews behind the rating. Null for a business with no reviews yet. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    service_area: str | None = Field(
        default=None,
        alias="serviceArea",
        description="The area Google says the business serves (e.g. Denver). Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    years_in_business: int | None = Field(
        default=None,
        alias="yearsInBusiness",
        description='Years in business as Google shows it ("8+ years in business" reads 8). Null when Google shows none or this source does not report it.',
    )


class GoogleNewsData(BaseModel):
    items: list[GoogleNewsItem] = Field(
        description="Article records: headline, source name, article link, and publish time. Populated whenever the provider has data for the entity."
    )


class GoogleNewsItem(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    created_utc: float | None = Field(
        default=None,
        alias="createdUtc",
        description="UTC epoch timestamp in seconds (Unix time). Multiply by 1000 for a JS Date in milliseconds. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    image: str | None = Field(
        default=None,
        description="Thumbnail image URL for the article. The query string carries the image identity, so it is kept.",
    )
    snippet: str | None = Field(
        default=None, description="Article snippet when available."
    )
    source: str | None = Field(
        default=None,
        description="Publisher name. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    title: str = Field(
        description="Article headline. Populated whenever the provider has data for the entity."
    )
    url: str = Field(
        description="Article link. Populated whenever the provider has data for the entity."
    )


class GooglePatentsData(BaseModel):
    query: str = Field(description="The query that was searched.")
    results: list[GooglePatentsResult] = Field(description="Patent result records.")


class GooglePatentsResult(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    assignee: str | None = Field(default=None, description="Patent assignee.")
    filed_utc: float | None = Field(
        default=None,
        alias="filedUtc",
        description="UTC epoch timestamp in seconds (Unix time). Multiply by 1000 for a JS Date in milliseconds.",
    )
    granted_utc: float | None = Field(
        default=None,
        alias="grantedUtc",
        description="UTC epoch timestamp in seconds (Unix time). Multiply by 1000 for a JS Date in milliseconds.",
    )
    image: str | None = Field(
        default=None, description="First patent figure thumbnail image URL."
    )
    inventor: str | None = Field(
        default=None, description="Named inventor or inventors."
    )
    language: str | None = Field(
        default=None, description="Two-letter language code of the patent document."
    )
    link: str = Field(
        description="URL to the patent. Populated whenever the provider has data for the entity."
    )
    pdf_url: str | None = Field(
        default=None, alias="pdfUrl", description="URL to an available patent PDF."
    )
    priority_utc: float | None = Field(
        default=None,
        alias="priorityUtc",
        description="UTC epoch timestamp in seconds (Unix time). Multiply by 1000 for a JS Date in milliseconds.",
    )
    publication_number: str = Field(
        alias="publicationNumber",
        description="Patent publication number (e.g. US11303135B2). Populated whenever the provider has data for the entity.",
    )
    published_utc: float | None = Field(
        default=None,
        alias="publishedUtc",
        description="UTC epoch timestamp in seconds (Unix time). Multiply by 1000 for a JS Date in milliseconds.",
    )
    snippet: str | None = Field(
        default=None, description="Short patent description snippet."
    )
    title: str = Field(
        description="Patent title. Populated whenever the provider has data for the entity."
    )


class GoogleScholarData(BaseModel):
    query: str = Field(description="The query that was searched.")
    results: list[GoogleScholarResult] = Field(
        description="Academic paper result records."
    )


class GoogleScholarResult(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    cited_by: int | None = Field(
        default=None,
        alias="citedBy",
        description="Number of citations reported by Google Scholar.",
    )
    id: str | None = Field(default=None, description="Result identifier.")
    link: str = Field(
        description="URL to the paper. Populated whenever the provider has data for the entity."
    )
    pdf_url: str | None = Field(
        default=None, alias="pdfUrl", description="URL to an available PDF."
    )
    publication_info: str | None = Field(
        default=None,
        alias="publicationInfo",
        description="Authors, venue, and publication year.",
    )
    snippet: str | None = Field(
        default=None, description="Short paper description snippet."
    )
    title: str = Field(
        description="Paper title. Populated whenever the provider has data for the entity."
    )
    year: int | None = Field(default=None, description="Publication year.")


class GoogleSearchData(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    next_cursor: str | None = Field(
        default=None,
        alias="nextCursor",
        description="Opaque cursor for the next page of results, or null when this lane has no more. Pass it back as cursor to continue.",
    )
    query: str
    results: list[GoogleSearchResult] = Field(
        description="Populated whenever the provider has data for the entity."
    )


class GoogleSearchResult(BaseModel):
    model_config = ConfigDict(extra="allow")

    link: str = Field(
        description="Populated whenever the provider has data for the entity."
    )
    position: int
    snippet: str = Field(
        description="Populated whenever the provider has data for the entity."
    )
    title: str = Field(
        description="Populated whenever the provider has data for the entity."
    )


class GoogleSearch100Data(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    ai_overview: str | None = Field(
        default=None,
        alias="aiOverview",
        description="Google's AI Overview text for this query, when Google showed one. Absent when it did not.",
    )
    query: str = Field(description="The search query these results answer.")
    results: list[GoogleSearch100Result] = Field(
        description="Organic results in Google's own order, position 1 first. Populated whenever the provider has data for the entity."
    )


class GoogleSearch100Result(BaseModel):
    model_config = ConfigDict(extra="allow")

    link: str = Field(
        description="The destination URL. Populated whenever the provider has data for the entity."
    )
    position: int = Field(
        description="Absolute rank across the whole result set, counting from 1 - not restarted per page. Populated whenever the provider has data for the entity."
    )
    snippet: str = Field(description="Google's summary text for the result.")
    title: str = Field(
        description="The result's headline as Google renders it. Populated whenever the provider has data for the entity."
    )


class GoogleTrendsData(BaseModel):
    geo: str = Field(
        description="The place the series cover: the country or subdivision code you sent, or worldwide."
    )
    series: list[GoogleTrendsSerie] = Field(
        description="One series per search term, in the order you sent the terms. All series share one 0-100 scale. Populated whenever the provider has data for the entity."
    )
    timeframe: str = Field(
        description="The window the series cover: the timeframe you sent, or 12m when you sent none."
    )


class GoogleTrendsSerie(BaseModel):
    model_config = ConfigDict(extra="allow")

    keyword: str = Field(
        description="The search term this series charts. Populated whenever the provider has data for the entity."
    )
    points: list[GoogleTrendsPoint] = Field(
        description="One point per time bucket, oldest first. Populated whenever the provider has data for the entity."
    )


class GoogleTrendsPoint(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    partial: bool | None = Field(
        default=None,
        description="True when Google is still counting this bucket, normally the newest one, so it reads lower than it will end. Present only when the source reports it.",
    )
    start_utc: float = Field(
        alias="startUtc",
        description="Start of the time bucket. UTC epoch timestamp in seconds (Unix time). Multiply by 1000 for a JS Date in milliseconds. Populated whenever the provider has data for the entity.",
    )
    value: int = Field(
        description="Search interest in this bucket on Google's 0-100 scale, where 100 is the peak of any term in the response and 0 means there was not enough data. Populated whenever the provider has data for the entity. Range: 0 to 100."
    )


class GoogleVideosData(BaseModel):
    query: str = Field(description="The query that was searched.")
    results: list[GoogleVideosResult] = Field(
        description="Video result records. Populated whenever the provider has data for the entity."
    )


class GoogleVideosResult(BaseModel):
    model_config = ConfigDict(extra="allow")

    image: str | None = Field(
        default=None, description="Thumbnail image URL for the video."
    )
    link: str = Field(
        description="URL to the video. Populated whenever the provider has data for the entity."
    )
    position: int | None = Field(
        default=None, description="1-based rank in the result list."
    )
    snippet: str | None = Field(default=None, description="Short description snippet.")
    source: str | None = Field(
        default=None, description="Host platform (e.g. YouTube, Vimeo)."
    )
    title: str = Field(
        description="Video title. Populated whenever the provider has data for the entity."
    )


class GoogleNamespace:
    """Typed methods for this platform. Attached lazily to the client."""

    def __init__(self, client: "AnyAPI") -> None:
        self._client = client

    def ai_mode(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[GoogleAiModeInput],
    ) -> RunResult[GoogleAiModeData]:
        """Google AI Mode

        Ask Google AI Mode a prompt and receive the cited answer it generates. AI
        Mode composes the answer at search time, so repeat calls on one prompt can
        differ in wording and in which sources are cited.

        Price: $0.002 per request.

        Example:
            res = client.google.ai_mode(prompt="What is AnyAPI at getanyapi.com, and what does it offer?")
        """
        raw = self._client._run_raw(  # pyright: ignore[reportPrivateUsage]
            "google.ai_mode", dict(input), options
        )
        return RunResult[GoogleAiModeData].model_validate(raw)

    def ai_overview(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[GoogleAiOverviewInput],
    ) -> RunResult[GoogleAiOverviewData]:
        """Google AI Overview

        Ask Google Search a prompt and receive the AI Overview it generated for that
        scrape, with every source Google listed. Google regenerates the overview per
        search, so the same prompt can return different wording and a different
        source list.

        Price: $0.0018 per request.

        Example:
            res = client.google.ai_overview(prompt="How does photosynthesis work?")
        """
        raw = self._client._run_raw(  # pyright: ignore[reportPrivateUsage]
            "google.ai_overview", dict(input), options
        )
        return RunResult[GoogleAiOverviewData].model_validate(raw)

    def ai_overview_preview(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[GoogleAiOverviewPreviewInput],
    ) -> RunResult[GoogleAiOverviewPreviewData]:
        """Google AI Overview Preview

        Ask Google Search a prompt and receive the AI Overview as a searcher first
        sees it, before selecting Show more: the opening text and the sources linked
        inside it. When Google shows the whole overview without a Show more button,
        that is what you receive. For the complete expanded overview with every
        source Google listed, use google.ai_overview.

        Price: $0.0007 per request.

        Example:
            res = client.google.ai_overview_preview(prompt="How does photosynthesis work?")
        """
        raw = self._client._run_raw(  # pyright: ignore[reportPrivateUsage]
            "google.ai_overview_preview", dict(input), options
        )
        return RunResult[GoogleAiOverviewPreviewData].model_validate(raw)

    def autocomplete(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[GoogleAutocompleteInput],
    ) -> RunResult[GoogleAutocompleteData]:
        """Google Autocomplete

        Get Google search autocomplete suggestions for a partial query (keyword
        ideas).

        Price: $0.00085 per request.

        Example:
            res = client.google.autocomplete(query="best coff")
        """
        raw = self._client._run_raw(  # pyright: ignore[reportPrivateUsage]
            "google.autocomplete", dict(input), options
        )
        return RunResult[GoogleAutocompleteData].model_validate(raw)

    def images(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[GoogleImagesInput],
    ) -> RunResult[GoogleImagesData]:
        """Google Images

        Run a Google Images search and get structured results: image URLs,
        dimensions, titles, and source pages.

        Price: $0.00085 per request.

        Example:
            res = client.google.images(gl="us", hl="en", limit=5, query="golden retriever")
        """
        raw = self._client._run_raw(  # pyright: ignore[reportPrivateUsage]
            "google.images", dict(input), options
        )
        return RunResult[GoogleImagesData].model_validate(raw)

    def job(
        self, *, options: RequestOptions | None = None, **input: Unpack[GoogleJobInput]
    ) -> RunResult[GoogleJobData]:
        """Google Job

        Fetch one Google Jobs listing by the listingToken that google.jobs returns:
        title, company, location, the site it was found on, the full description,
        apply links on every board that carries it, the posting details Google shows
        (posted, pay, job type, benefits), and the employer's ratings on review
        sites such as Glassdoor and Indeed when Google shows them.

        Price: $0.00085 per request.

        Example:
            res = client.google.job(listingToken="gcb1.eyJ2IjoxLCJvcCI6Imdvb2dsZV9qb2JzX2xpc3RpbmciLCJzY29wZSI6InctN2lTM2lzV09LSUhqZTMwaVR5NkEiLCJxIjoicmVnaXN0ZXJlZCBudXJzZSIsImZjIjoiRXN3QkNvd0JRVXBwVkRSMFRGVnBlamxoVFdaQ2FVZHpiMWh4Y0cxVE1TMDBlV2c1UWxWSFZpMWpjelpYVmtOaFpUSjBXbmRQT0ZCQ01VWXlURFl5TWs0NFgyOVFTM1pEVjFSaU5VRkZhR1JzYTBGTU1IUnRPR0Z2V1ZaemFGUk5XRlJRVTFSU2JETkZSaTFOVUV4eVkwcDJTbGd0YkZWUlZXTktjMHhMYjBWdWFHWjFPRFpZUldoUFFtVnlaRk5tYlhVU0YzbHNYMU5oZEdvM1FYRmhjbWt0WjFBME9UTlJMVkZ6R2lKQlJITnlPV1pVV2pGS05XbENSMnRyUTJkelNqbGhkelpIVnkxT1RscE1NbU5CIiwiZWkiOiJ5bF9TYXRqN0FxYXJpLWdQNDkzUS1RcyIsImlkIjoiMFRHZ0p6WW1XT0drWFZCR0FBQUFBQT09IiwidmVkIjoiMmFoVUtFd2pZaUlQeGlMLVhBeFdtMVFJSEhlTXVOTDhRcDR3Q2VnUUlKUkFCIn0")
        """
        raw = self._client._run_raw(  # pyright: ignore[reportPrivateUsage]
            "google.job", dict(input), options
        )
        return RunResult[GoogleJobData].model_validate(raw)

    def jobs(
        self, *, options: RequestOptions | None = None, **input: Unpack[GoogleJobsInput]
    ) -> RunResult[GoogleJobsData]:
        """Google Jobs

        Search Google Jobs, the job listings Google gathers from LinkedIn, Indeed,
        ZipRecruiter, company career sites and other boards, and get about 10
        listings per call: title, company, location, the site it was found on, the
        full description, apply links on every board that carries it, and the
        posting details Google shows (posted, pay, job type, benefits). Each listing
        carries a listingToken you can pass to google.job for employer ratings. Send
        nextCursor back as cursor to walk further pages.

        Price: $0.00085 per request.

        Example:
            res = client.google.jobs(gl="us", hl="en", location="Chicago, IL", query="registered nurse")
        """
        raw = self._client._run_raw(  # pyright: ignore[reportPrivateUsage]
            "google.jobs", dict(input), options
        )
        return RunResult[GoogleJobsData].model_validate(raw)

    def iter_jobs(
        self, *, options: RequestOptions | None = None, **input: Unpack[GoogleJobsInput]
    ) -> Paginator[GoogleJobsItem, GoogleJobsData]:
        """Iterate Google Jobs results, following pagination cursors.

        Yields validated `GoogleJobsItem` items from the `items` field of
        each page. Use `.pages()` on the returned paginator to walk whole
        `RunResult` pages.
        """
        return paginate(
            self._client,
            "google.jobs",
            dict(input),
            "items",
            item_model=GoogleJobsItem,
            data_model=GoogleJobsData,
            bare=False,
            options=options,
        )

    def lens(
        self, *, options: RequestOptions | None = None, **input: Unpack[GoogleLensInput]
    ) -> RunResult[GoogleLensData]:
        """Google Lens

        Reverse image search: find web pages and visual matches for an image URL.

        Price: $0.00085 per request.

        Example:
            res = client.google.lens(url="https://i.imgur.com/HBrB8p0.png")
        """
        raw = self._client._run_raw(  # pyright: ignore[reportPrivateUsage]
            "google.lens", dict(input), options
        )
        return RunResult[GoogleLensData].model_validate(raw)

    def local_services(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[GoogleLocalServicesInput],
    ) -> RunResult[GoogleLocalServicesData]:
        """Google Local Services

        Find the businesses Google lists in Local Services ads for a service in a US
        city (plumbers, electricians, cleaners...): up to 20 per request, each with
        phone, star rating, review count, category, service area and Google profile
        link.

        Price: $0.00085 per request.

        Example:
            res = client.google.local_services(limit=5, location="Denver, CO", query="plumber")
        """
        raw = self._client._run_raw(  # pyright: ignore[reportPrivateUsage]
            "google.local_services", dict(input), options
        )
        return RunResult[GoogleLocalServicesData].model_validate(raw)

    def news(
        self, *, options: RequestOptions | None = None, **input: Unpack[GoogleNewsInput]
    ) -> RunResult[GoogleNewsData]:
        """Google News

        Search Google News by keyword and get fresh articles (headlines, sources,
        links, and publish times) as clean JSON.

        Price: $0.00099 per request.

        Example:
            res = client.google.news(gl="us", hl="en", query="openai")
        """
        raw = self._client._run_raw(  # pyright: ignore[reportPrivateUsage]
            "google.news", dict(input), options
        )
        return RunResult[GoogleNewsData].model_validate(raw)

    def patents(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[GooglePatentsInput],
    ) -> RunResult[GooglePatentsData]:
        """Google Patents

        Search Google Patents with title, patent number, inventor, assignee, key
        dates, and PDF link.

        Price: $0.00085 per request.

        Example:
            res = client.google.patents(query="wireless charging")
        """
        raw = self._client._run_raw(  # pyright: ignore[reportPrivateUsage]
            "google.patents", dict(input), options
        )
        return RunResult[GooglePatentsData].model_validate(raw)

    def scholar(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[GoogleScholarInput],
    ) -> RunResult[GoogleScholarData]:
        """Google Scholar

        Search Google Scholar for academic papers with title, authors, citation
        count, and PDF link.

        Price: $0.00085 per request.

        Example:
            res = client.google.scholar(query="attention is all you need")
        """
        raw = self._client._run_raw(  # pyright: ignore[reportPrivateUsage]
            "google.scholar", dict(input), options
        )
        return RunResult[GoogleScholarData].model_validate(raw)

    def search(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[GoogleSearchInput],
    ) -> RunResult[GoogleSearchData]:
        """Google Search

        Run a Google web search and get the organic results (title, link, snippet,
        position) as clean JSON. Returns about 10 results per call - Google stopped
        honoring bulk result counts in September 2025, so a limit above 10 is
        accepted but returns no more than a page. Send page 2, 3, ... to walk
        further, or use google.search_100 for up to 100 ranked results in one call,
        which is normally cheaper past roughly 20 results.

        Price: $0.0005 per request.

        Example:
            res = client.google.search(gl="us", hl="en", limit=10, query="best coffee maker")
        """
        raw = self._client._run_raw(  # pyright: ignore[reportPrivateUsage]
            "google.search", dict(input), options
        )
        return RunResult[GoogleSearchData].model_validate(raw)

    def iter_search(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[GoogleSearchInput],
    ) -> Paginator[GoogleSearchResult, GoogleSearchData]:
        """Iterate Google Search results, following pagination cursors.

        Yields validated `GoogleSearchResult` items from the `results` field of
        each page. Use `.pages()` on the returned paginator to walk whole
        `RunResult` pages.
        """
        return paginate(
            self._client,
            "google.search",
            dict(input),
            "results",
            item_model=GoogleSearchResult,
            data_model=GoogleSearchData,
            bare=False,
            options=options,
        )

    def search_100(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[GoogleSearch100Input],
    ) -> RunResult[GoogleSearch100Data]:
        """Google Search Top 100

        Run a Google web search and get up to 100 ranked organic results in one
        call, with true absolute positions rather than per-page numbering. One
        charge per call whatever the depth, which normally makes it cheaper than
        paging google.search past roughly 20 results; when the backup source has to
        answer, the call costs more, up to $0.024. It reads ten pages of Google to
        build the list, so a call can take up to about five minutes - use
        google.search when you want the first page back in a second.

        Price: $0.024 per request.

        Example:
            res = client.google.search_100(gl="us", hl="en", query="best crm software")
        """
        raw = self._client._run_raw(  # pyright: ignore[reportPrivateUsage]
            "google.search_100", dict(input), options
        )
        return RunResult[GoogleSearch100Data].model_validate(raw)

    def trends(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[GoogleTrendsInput],
    ) -> RunResult[GoogleTrendsData]:
        """Google Trends

        Google Trends interest over time for up to 5 search terms compared on one
        0-100 scale, where 100 is the peak search interest of any term in the
        window. Returns one series per term, in the order you sent them, with a
        value for every time bucket. Choose the country or region with geo
        (worldwide when omitted) and the window with timeframe (the past 12 months
        when omitted); both are echoed in the response. Interest over time only, not
        related queries or regions.

        Price: $0.002 per request.

        Example:
            res = client.google.trends(geo="US", keywords=["coffee", "tea"], timeframe="12m")
        """
        raw = self._client._run_raw(  # pyright: ignore[reportPrivateUsage]
            "google.trends", dict(input), options
        )
        return RunResult[GoogleTrendsData].model_validate(raw)

    def videos(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[GoogleVideosInput],
    ) -> RunResult[GoogleVideosData]:
        """Google Videos

        Search Google for video results (YouTube and others) with title, link,
        thumbnail, and source.

        Price: $0.00085 per request.

        Example:
            res = client.google.videos(gl="us", hl="en", query="lofi hip hop")
        """
        raw = self._client._run_raw(  # pyright: ignore[reportPrivateUsage]
            "google.videos", dict(input), options
        )
        return RunResult[GoogleVideosData].model_validate(raw)


class AsyncGoogleNamespace:
    """Typed methods for this platform. Attached lazily to the client."""

    def __init__(self, client: "AsyncAnyAPI") -> None:
        self._client = client

    async def ai_mode(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[GoogleAiModeInput],
    ) -> RunResult[GoogleAiModeData]:
        """Google AI Mode

        Ask Google AI Mode a prompt and receive the cited answer it generates. AI
        Mode composes the answer at search time, so repeat calls on one prompt can
        differ in wording and in which sources are cited.

        Price: $0.002 per request.

        Example:
            res = client.google.ai_mode(prompt="What is AnyAPI at getanyapi.com, and what does it offer?")
        """
        raw = await self._client._arun_raw(  # pyright: ignore[reportPrivateUsage]
            "google.ai_mode", dict(input), options
        )
        return RunResult[GoogleAiModeData].model_validate(raw)

    async def ai_overview(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[GoogleAiOverviewInput],
    ) -> RunResult[GoogleAiOverviewData]:
        """Google AI Overview

        Ask Google Search a prompt and receive the AI Overview it generated for that
        scrape, with every source Google listed. Google regenerates the overview per
        search, so the same prompt can return different wording and a different
        source list.

        Price: $0.0018 per request.

        Example:
            res = client.google.ai_overview(prompt="How does photosynthesis work?")
        """
        raw = await self._client._arun_raw(  # pyright: ignore[reportPrivateUsage]
            "google.ai_overview", dict(input), options
        )
        return RunResult[GoogleAiOverviewData].model_validate(raw)

    async def ai_overview_preview(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[GoogleAiOverviewPreviewInput],
    ) -> RunResult[GoogleAiOverviewPreviewData]:
        """Google AI Overview Preview

        Ask Google Search a prompt and receive the AI Overview as a searcher first
        sees it, before selecting Show more: the opening text and the sources linked
        inside it. When Google shows the whole overview without a Show more button,
        that is what you receive. For the complete expanded overview with every
        source Google listed, use google.ai_overview.

        Price: $0.0007 per request.

        Example:
            res = client.google.ai_overview_preview(prompt="How does photosynthesis work?")
        """
        raw = await self._client._arun_raw(  # pyright: ignore[reportPrivateUsage]
            "google.ai_overview_preview", dict(input), options
        )
        return RunResult[GoogleAiOverviewPreviewData].model_validate(raw)

    async def autocomplete(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[GoogleAutocompleteInput],
    ) -> RunResult[GoogleAutocompleteData]:
        """Google Autocomplete

        Get Google search autocomplete suggestions for a partial query (keyword
        ideas).

        Price: $0.00085 per request.

        Example:
            res = client.google.autocomplete(query="best coff")
        """
        raw = await self._client._arun_raw(  # pyright: ignore[reportPrivateUsage]
            "google.autocomplete", dict(input), options
        )
        return RunResult[GoogleAutocompleteData].model_validate(raw)

    async def images(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[GoogleImagesInput],
    ) -> RunResult[GoogleImagesData]:
        """Google Images

        Run a Google Images search and get structured results: image URLs,
        dimensions, titles, and source pages.

        Price: $0.00085 per request.

        Example:
            res = client.google.images(gl="us", hl="en", limit=5, query="golden retriever")
        """
        raw = await self._client._arun_raw(  # pyright: ignore[reportPrivateUsage]
            "google.images", dict(input), options
        )
        return RunResult[GoogleImagesData].model_validate(raw)

    async def job(
        self, *, options: RequestOptions | None = None, **input: Unpack[GoogleJobInput]
    ) -> RunResult[GoogleJobData]:
        """Google Job

        Fetch one Google Jobs listing by the listingToken that google.jobs returns:
        title, company, location, the site it was found on, the full description,
        apply links on every board that carries it, the posting details Google shows
        (posted, pay, job type, benefits), and the employer's ratings on review
        sites such as Glassdoor and Indeed when Google shows them.

        Price: $0.00085 per request.

        Example:
            res = client.google.job(listingToken="gcb1.eyJ2IjoxLCJvcCI6Imdvb2dsZV9qb2JzX2xpc3RpbmciLCJzY29wZSI6InctN2lTM2lzV09LSUhqZTMwaVR5NkEiLCJxIjoicmVnaXN0ZXJlZCBudXJzZSIsImZjIjoiRXN3QkNvd0JRVXBwVkRSMFRGVnBlamxoVFdaQ2FVZHpiMWh4Y0cxVE1TMDBlV2c1UWxWSFZpMWpjelpYVmtOaFpUSjBXbmRQT0ZCQ01VWXlURFl5TWs0NFgyOVFTM1pEVjFSaU5VRkZhR1JzYTBGTU1IUnRPR0Z2V1ZaemFGUk5XRlJRVTFSU2JETkZSaTFOVUV4eVkwcDJTbGd0YkZWUlZXTktjMHhMYjBWdWFHWjFPRFpZUldoUFFtVnlaRk5tYlhVU0YzbHNYMU5oZEdvM1FYRmhjbWt0WjFBME9UTlJMVkZ6R2lKQlJITnlPV1pVV2pGS05XbENSMnRyUTJkelNqbGhkelpIVnkxT1RscE1NbU5CIiwiZWkiOiJ5bF9TYXRqN0FxYXJpLWdQNDkzUS1RcyIsImlkIjoiMFRHZ0p6WW1XT0drWFZCR0FBQUFBQT09IiwidmVkIjoiMmFoVUtFd2pZaUlQeGlMLVhBeFdtMVFJSEhlTXVOTDhRcDR3Q2VnUUlKUkFCIn0")
        """
        raw = await self._client._arun_raw(  # pyright: ignore[reportPrivateUsage]
            "google.job", dict(input), options
        )
        return RunResult[GoogleJobData].model_validate(raw)

    async def jobs(
        self, *, options: RequestOptions | None = None, **input: Unpack[GoogleJobsInput]
    ) -> RunResult[GoogleJobsData]:
        """Google Jobs

        Search Google Jobs, the job listings Google gathers from LinkedIn, Indeed,
        ZipRecruiter, company career sites and other boards, and get about 10
        listings per call: title, company, location, the site it was found on, the
        full description, apply links on every board that carries it, and the
        posting details Google shows (posted, pay, job type, benefits). Each listing
        carries a listingToken you can pass to google.job for employer ratings. Send
        nextCursor back as cursor to walk further pages.

        Price: $0.00085 per request.

        Example:
            res = client.google.jobs(gl="us", hl="en", location="Chicago, IL", query="registered nurse")
        """
        raw = await self._client._arun_raw(  # pyright: ignore[reportPrivateUsage]
            "google.jobs", dict(input), options
        )
        return RunResult[GoogleJobsData].model_validate(raw)

    def iter_jobs(
        self, *, options: RequestOptions | None = None, **input: Unpack[GoogleJobsInput]
    ) -> AsyncPaginator[GoogleJobsItem, GoogleJobsData]:
        """Iterate Google Jobs results, following pagination cursors.

        Yields validated `GoogleJobsItem` items from the `items` field of
        each page. Use `.pages()` on the returned paginator to walk whole
        `RunResult` pages.
        """
        return apaginate(
            self._client,
            "google.jobs",
            dict(input),
            "items",
            item_model=GoogleJobsItem,
            data_model=GoogleJobsData,
            bare=False,
            options=options,
        )

    async def lens(
        self, *, options: RequestOptions | None = None, **input: Unpack[GoogleLensInput]
    ) -> RunResult[GoogleLensData]:
        """Google Lens

        Reverse image search: find web pages and visual matches for an image URL.

        Price: $0.00085 per request.

        Example:
            res = client.google.lens(url="https://i.imgur.com/HBrB8p0.png")
        """
        raw = await self._client._arun_raw(  # pyright: ignore[reportPrivateUsage]
            "google.lens", dict(input), options
        )
        return RunResult[GoogleLensData].model_validate(raw)

    async def local_services(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[GoogleLocalServicesInput],
    ) -> RunResult[GoogleLocalServicesData]:
        """Google Local Services

        Find the businesses Google lists in Local Services ads for a service in a US
        city (plumbers, electricians, cleaners...): up to 20 per request, each with
        phone, star rating, review count, category, service area and Google profile
        link.

        Price: $0.00085 per request.

        Example:
            res = client.google.local_services(limit=5, location="Denver, CO", query="plumber")
        """
        raw = await self._client._arun_raw(  # pyright: ignore[reportPrivateUsage]
            "google.local_services", dict(input), options
        )
        return RunResult[GoogleLocalServicesData].model_validate(raw)

    async def news(
        self, *, options: RequestOptions | None = None, **input: Unpack[GoogleNewsInput]
    ) -> RunResult[GoogleNewsData]:
        """Google News

        Search Google News by keyword and get fresh articles (headlines, sources,
        links, and publish times) as clean JSON.

        Price: $0.00099 per request.

        Example:
            res = client.google.news(gl="us", hl="en", query="openai")
        """
        raw = await self._client._arun_raw(  # pyright: ignore[reportPrivateUsage]
            "google.news", dict(input), options
        )
        return RunResult[GoogleNewsData].model_validate(raw)

    async def patents(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[GooglePatentsInput],
    ) -> RunResult[GooglePatentsData]:
        """Google Patents

        Search Google Patents with title, patent number, inventor, assignee, key
        dates, and PDF link.

        Price: $0.00085 per request.

        Example:
            res = client.google.patents(query="wireless charging")
        """
        raw = await self._client._arun_raw(  # pyright: ignore[reportPrivateUsage]
            "google.patents", dict(input), options
        )
        return RunResult[GooglePatentsData].model_validate(raw)

    async def scholar(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[GoogleScholarInput],
    ) -> RunResult[GoogleScholarData]:
        """Google Scholar

        Search Google Scholar for academic papers with title, authors, citation
        count, and PDF link.

        Price: $0.00085 per request.

        Example:
            res = client.google.scholar(query="attention is all you need")
        """
        raw = await self._client._arun_raw(  # pyright: ignore[reportPrivateUsage]
            "google.scholar", dict(input), options
        )
        return RunResult[GoogleScholarData].model_validate(raw)

    async def search(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[GoogleSearchInput],
    ) -> RunResult[GoogleSearchData]:
        """Google Search

        Run a Google web search and get the organic results (title, link, snippet,
        position) as clean JSON. Returns about 10 results per call - Google stopped
        honoring bulk result counts in September 2025, so a limit above 10 is
        accepted but returns no more than a page. Send page 2, 3, ... to walk
        further, or use google.search_100 for up to 100 ranked results in one call,
        which is normally cheaper past roughly 20 results.

        Price: $0.0005 per request.

        Example:
            res = client.google.search(gl="us", hl="en", limit=10, query="best coffee maker")
        """
        raw = await self._client._arun_raw(  # pyright: ignore[reportPrivateUsage]
            "google.search", dict(input), options
        )
        return RunResult[GoogleSearchData].model_validate(raw)

    def iter_search(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[GoogleSearchInput],
    ) -> AsyncPaginator[GoogleSearchResult, GoogleSearchData]:
        """Iterate Google Search results, following pagination cursors.

        Yields validated `GoogleSearchResult` items from the `results` field of
        each page. Use `.pages()` on the returned paginator to walk whole
        `RunResult` pages.
        """
        return apaginate(
            self._client,
            "google.search",
            dict(input),
            "results",
            item_model=GoogleSearchResult,
            data_model=GoogleSearchData,
            bare=False,
            options=options,
        )

    async def search_100(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[GoogleSearch100Input],
    ) -> RunResult[GoogleSearch100Data]:
        """Google Search Top 100

        Run a Google web search and get up to 100 ranked organic results in one
        call, with true absolute positions rather than per-page numbering. One
        charge per call whatever the depth, which normally makes it cheaper than
        paging google.search past roughly 20 results; when the backup source has to
        answer, the call costs more, up to $0.024. It reads ten pages of Google to
        build the list, so a call can take up to about five minutes - use
        google.search when you want the first page back in a second.

        Price: $0.024 per request.

        Example:
            res = client.google.search_100(gl="us", hl="en", query="best crm software")
        """
        raw = await self._client._arun_raw(  # pyright: ignore[reportPrivateUsage]
            "google.search_100", dict(input), options
        )
        return RunResult[GoogleSearch100Data].model_validate(raw)

    async def trends(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[GoogleTrendsInput],
    ) -> RunResult[GoogleTrendsData]:
        """Google Trends

        Google Trends interest over time for up to 5 search terms compared on one
        0-100 scale, where 100 is the peak search interest of any term in the
        window. Returns one series per term, in the order you sent them, with a
        value for every time bucket. Choose the country or region with geo
        (worldwide when omitted) and the window with timeframe (the past 12 months
        when omitted); both are echoed in the response. Interest over time only, not
        related queries or regions.

        Price: $0.002 per request.

        Example:
            res = client.google.trends(geo="US", keywords=["coffee", "tea"], timeframe="12m")
        """
        raw = await self._client._arun_raw(  # pyright: ignore[reportPrivateUsage]
            "google.trends", dict(input), options
        )
        return RunResult[GoogleTrendsData].model_validate(raw)

    async def videos(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[GoogleVideosInput],
    ) -> RunResult[GoogleVideosData]:
        """Google Videos

        Search Google for video results (YouTube and others) with title, link,
        thumbnail, and source.

        Price: $0.00085 per request.

        Example:
            res = client.google.videos(gl="us", hl="en", query="lofi hip hop")
        """
        raw = await self._client._arun_raw(  # pyright: ignore[reportPrivateUsage]
            "google.videos", dict(input), options
        )
        return RunResult[GoogleVideosData].model_validate(raw)
