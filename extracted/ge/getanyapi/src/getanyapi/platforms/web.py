# Generated - do not edit. Regenerate with: pnpm generate
"""Generated namespace module for the web platform."""

from __future__ import annotations

from typing import Any, Literal, TYPE_CHECKING

from pydantic import BaseModel, ConfigDict, Field
from typing_extensions import NotRequired, Required, TypedDict, Unpack

from ..types import RequestOptions, RunResult

if TYPE_CHECKING:
    from .._async_client import AsyncAnyAPI
    from .._client import AnyAPI


class WebCrawlInput(TypedDict, total=False):
    """Input for Website Crawl."""

    allowFallbacks: NotRequired[bool]
    """Optional, default true. When false, only the sources listed in `source` may serve; the request is refused with no charge if none of them can. When true, the listed sources are tried first and any other source may serve after them, at the normal price. Default: true."""
    ignoreSources: NotRequired[list[str]]
    """Optional. Source ids to skip for this request, taken from this endpoint's `lanes[].source.id`. The cheapest remaining source serves and the price is that of the dearest remaining source. An id that does not serve this endpoint, or that is also in `source`, is rejected as invalid input with no charge; skipping every source is rejected the same way."""
    limit: NotRequired[int]
    """Maximum number of pages to crawl and return (1-10, default 10). You are billed per page returned, so a lower limit costs less. Range: 1 to 10."""
    preferLatencyUnderMs: NotRequired[int]
    """Optional; omit it and routing is unchanged, with the cheapest source serving. Prefer sources whose typical response time (median over the trailing 30 days, as published on this endpoint's lane health) is under this many milliseconds; among those, the cheapest serves. This can raise your price: when the cheapest source misses the target, a faster and dearer one serves, and you are quoted and charged its price. If no source is that fast the request is still served, by whichever source offers the best speed for its price - it is never refused for being slow. Sources we have not timed are tried last. This is a preference, not a guarantee: the median describes past requests and is not a ceiling on this one, and it excludes any wait this request itself asks for. On a paginated walk it applies to the first page only: later pages stay with the source that page chose, at the price it was quoted. Minimum: 1."""
    requireFields: NotRequired[
        list[
            Literal[
                "author",
                "canonicalUrl",
                "contentType",
                "headings",
                "jsonLd",
                "language",
                "modifiedUtc",
                "publishedUtc",
                "robots",
                "siteName",
            ]
        ]
    ]
    """Optional; omit it and routing is unchanged. Name the output fields this request must be able to return, for example `language`, and it is served only by a source that returns every one of them. Fields you do not name are still returned whenever the serving source has them. Every source charges the same per page, so this never changes your price. A named field can still be empty on a page that genuinely lacks it."""
    source: NotRequired[list[str]]
    """Optional. Source ids to prefer, in order, taken from this endpoint's `lanes[].source.id` in /catalog or /apis. Omit it and the cheapest source serves, with automatic failover. Listed sources are tried first in the order given, then the others, unless `allowFallbacks` is false. A single source with `allowFallbacks` false is served only by that source at its price, quoted and charged exactly, with no failover. The price is that of the dearest source that may serve. An id that does not serve this endpoint is rejected as invalid input with no charge; a listed source that is not serving right now is refused with no charge, so omit `source` to be served by another. On a paginated walk, later pages must include the source that served page one, or omit `source`."""
    url: Required[str]
    """The website URL or domain to crawl. Pages linked from it on the same site are crawled too."""


class WebMapInput(TypedDict, total=False):
    """Input for Web Map."""

    allowFallbacks: NotRequired[bool]
    """Optional, default true. When false, only the sources listed in `source` may serve; the request is refused with no charge if none of them can. When true, the listed sources are tried first and any other source may serve after them, at the normal price. Default: true."""
    ignoreSources: NotRequired[list[str]]
    """Optional. Source ids to skip for this request, taken from this endpoint's `lanes[].source.id`. The cheapest remaining source serves and the price is that of the dearest remaining source. An id that does not serve this endpoint, or that is also in `source`, is rejected as invalid input with no charge; skipping every source is rejected the same way."""
    includeSubdomains: NotRequired[bool]
    """When true (upstream default), include URLs on subdomains of the target (for example docs.example.com when mapping example.com). Set false to return only URLs on the exact host."""
    limit: NotRequired[int]
    """Maximum number of links to return. Default: 100."""
    preferLatencyUnderMs: NotRequired[int]
    """Optional; omit it and routing is unchanged, with the cheapest source serving. Prefer sources whose typical response time (median over the trailing 30 days, as published on this endpoint's lane health) is under this many milliseconds; among those, the cheapest serves. This can raise your price: when the cheapest source misses the target, a faster and dearer one serves, and you are quoted and charged its price. If no source is that fast the request is still served, by whichever source offers the best speed for its price - it is never refused for being slow. Sources we have not timed are tried last. This is a preference, not a guarantee: the median describes past requests and is not a ceiling on this one, and it excludes any wait this request itself asks for. On a paginated walk it applies to the first page only: later pages stay with the source that page chose, at the price it was quoted. Minimum: 1."""
    search: NotRequired[str]
    """Optional term that orders the returned links by relevance."""
    sitemap: NotRequired[Literal["include", "skip", "only"]]
    """How to use the site's sitemap.xml when discovering URLs. 'include' (upstream default) merges sitemap URLs with links found by crawling; 'only' returns just the URLs listed in the sitemap (fastest and most authoritative); 'skip' ignores the sitemap and discovers URLs by crawling links. Omit to use 'include'."""
    source: NotRequired[list[str]]
    """Optional. Source ids to prefer, in order, taken from this endpoint's `lanes[].source.id` in /catalog or /apis. Omit it and the cheapest source serves, with automatic failover. Listed sources are tried first in the order given, then the others, unless `allowFallbacks` is false. A single source with `allowFallbacks` false is served only by that source at its price, quoted and charged exactly, with no failover. The price is that of the dearest source that may serve. An id that does not serve this endpoint is rejected as invalid input with no charge; a listed source that is not serving right now is refused with no charge, so omit `source` to be served by another. On a paginated walk, later pages must include the source that served page one, or omit `source`."""
    url: Required[str]
    """The base URL of the site to map into a list of links."""


class WebScrapeInput(TypedDict, total=False):
    """Input for Web Scrape."""

    allowFallbacks: NotRequired[bool]
    """Optional, default true. When false, only the sources listed in `source` may serve; the request is refused with no charge if none of them can. When true, the listed sources are tried first and any other source may serve after them, at the normal price. Default: true."""
    blockAds: NotRequired[bool]
    """When true (upstream default), strip ad and cookie-consent elements before capture. Set false to keep them."""
    excludeTags: NotRequired[list[str]]
    """CSS selectors to drop before capture (for example ["nav", "footer", ".ads"]). Applied after includeTags."""
    formats: NotRequired[list[Literal["markdown", "html", "rawHtml"]]]
    """Which representations of the page to return. Any combination of: markdown (page content as Markdown), html (the page HTML exactly as the browser received it, including head and script tags). Each requested format is returned under the matching output field. Defaults to both. rawHtml is a deprecated alias of html, returned under a rawHtml field for callers that predate the rename; send html instead."""
    ignoreSources: NotRequired[list[str]]
    """Optional. Source ids to skip for this request, taken from this endpoint's `lanes[].source.id`. The cheapest remaining source serves and the price is that of the dearest remaining source. An id that does not serve this endpoint, or that is also in `source`, is rejected as invalid input with no charge; skipping every source is rejected the same way."""
    includeTags: NotRequired[list[str]]
    """CSS selectors to keep. When set, only content matching these selectors is captured (for example ["article", "main"] or ["#content"])."""
    mobile: NotRequired[bool]
    """When true, render the page with a mobile viewport and user agent instead of desktop. Some sites serve materially different content to mobile."""
    onlyMainContent: NotRequired[bool]
    """When true, return only the main article content, stripping navigation, headers, footers, and other boilerplate. Defaults to false to capture the full page. Default: false."""
    preferLatencyUnderMs: NotRequired[int]
    """Optional; omit it and routing is unchanged, with the cheapest source serving. Prefer sources whose typical response time (median over the trailing 30 days, as published on this endpoint's lane health) is under this many milliseconds; among those, the cheapest serves. This can raise your price: when the cheapest source misses the target, a faster and dearer one serves, and you are quoted and charged its price. If no source is that fast the request is still served, by whichever source offers the best speed for its price - it is never refused for being slow. Sources we have not timed are tried last. This is a preference, not a guarantee: the median describes past requests and is not a ceiling on this one, and it excludes any wait this request itself asks for. On a paginated walk it applies to the first page only: later pages stay with the source that page chose, at the price it was quoted. Minimum: 1."""
    requireFields: NotRequired[list[Literal["statusCode"]]]
    """Optional; omit it and routing is unchanged, with the cheapest source serving. Name the output fields this request must be able to return, for example `statusCode`, and it is served only by a source that returns every one of them. Fields you do not name are still returned whenever the serving source has them. This can raise your price: when the cheapest source cannot return a named field, a dearer source serves, and you are quoted and charged its price. A named field can still be absent on a record that genuinely lacks it. Naming a combination that no single source returns together is refused as invalid input, with no charge. A source that reports a field only in some cases, such as only when the website answered with an error, does not count as returning it."""
    source: NotRequired[list[str]]
    """Optional. Source ids to prefer, in order, taken from this endpoint's `lanes[].source.id` in /catalog or /apis. Omit it and the cheapest source serves, with automatic failover. Listed sources are tried first in the order given, then the others, unless `allowFallbacks` is false. A single source with `allowFallbacks` false is served only by that source at its price, quoted and charged exactly, with no failover. The price is that of the dearest source that may serve. An id that does not serve this endpoint is rejected as invalid input with no charge; a listed source that is not serving right now is refused with no charge, so omit `source` to be served by another. On a paginated walk, later pages must include the source that served page one, or omit `source`."""
    url: Required[str]
    """The full web address of the page to scrape, including its domain, for example https://example.com. The https:// prefix is optional."""
    waitFor: NotRequired[int]
    """Milliseconds to wait for the page to finish rendering before capture. Use this for JavaScript-heavy pages or single-page apps whose content loads after the initial paint. Capped at 15000 to stay within the request timeout. This wait is time you asked us to spend, so your response takes this much longer, and it is excluded from the latency published for this endpoint. If every provider that can wait fails, the page may still be returned, captured without the wait. Range: 0 to 15000."""


class WebScreenshotInput(TypedDict, total=False):
    """Input for Website Screenshot."""

    allowFallbacks: NotRequired[bool]
    """Optional, default true. When false, only the sources listed in `source` may serve; the request is refused with no charge if none of them can. When true, the listed sources are tried first and any other source may serve after them, at the normal price. Default: true."""
    ignoreSources: NotRequired[list[str]]
    """Optional. Source ids to skip for this request, taken from this endpoint's `lanes[].source.id`. The cheapest remaining source serves and the price is that of the dearest remaining source. An id that does not serve this endpoint, or that is also in `source`, is rejected as invalid input with no charge; skipping every source is rejected the same way."""
    preferLatencyUnderMs: NotRequired[int]
    """Optional; omit it and routing is unchanged, with the cheapest source serving. Prefer sources whose typical response time (median over the trailing 30 days, as published on this endpoint's lane health) is under this many milliseconds; among those, the cheapest serves. This can raise your price: when the cheapest source misses the target, a faster and dearer one serves, and you are quoted and charged its price. If no source is that fast the request is still served, by whichever source offers the best speed for its price - it is never refused for being slow. Sources we have not timed are tried last. This is a preference, not a guarantee: the median describes past requests and is not a ceiling on this one, and it excludes any wait this request itself asks for. On a paginated walk it applies to the first page only: later pages stay with the source that page chose, at the price it was quoted. Minimum: 1."""
    source: NotRequired[list[str]]
    """Optional. Source ids to prefer, in order, taken from this endpoint's `lanes[].source.id` in /catalog or /apis. Omit it and the cheapest source serves, with automatic failover. Listed sources are tried first in the order given, then the others, unless `allowFallbacks` is false. A single source with `allowFallbacks` false is served only by that source at its price, quoted and charged exactly, with no failover. The price is that of the dearest source that may serve. An id that does not serve this endpoint is rejected as invalid input with no charge; a listed source that is not serving right now is refused with no charge, so omit `source` to be served by another. On a paginated walk, later pages must include the source that served page one, or omit `source`."""
    url: Required[str]
    """The full URL of the page to capture."""
    viewportWidth: NotRequired[int]
    """Browser viewport width in pixels (e.g. 1280). Default: 1280."""


class WebCrawlData(BaseModel):
    issues: list[WebCrawlIssue] | None = Field(
        default=None,
        description="Pages the crawl reported as failed or skipped. They are never in items and never billed. The list holds what the crawl reported, not every page of the site.",
    )
    items: list[WebCrawlItem] = Field(
        description="One record per crawled page: its URL and domain, page title, meta description, language, HTTP status, the page content as Markdown text, and the page metadata the source reports. You are billed for these pages only. Populated whenever the provider has data for the entity."
    )
    summary: WebCrawlSummary | None = Field(
        default=None,
        description="Counts for this crawl. They describe the pages this crawl visited and reported, not the whole website, and are not added together into a total.",
    )


class WebCrawlIssue(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    outcome: Literal["failed", "robots_disallowed", "skipped"] = Field(
        description="failed: the page could not be fetched or answered with an HTTP error. robots_disallowed: the site's robots.txt does not allow crawling it. skipped: the crawl did not fetch it, for example because it is outside the crawled site."
    )
    status_code: int | None = Field(
        default=None,
        alias="statusCode",
        description="The HTTP status code the page answered with, or null when unknown.",
    )
    url: str = Field(description="The page's URL.")


class WebCrawlItem(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    author: str | None = Field(
        default=None, description="The author the page declares, or null when unknown."
    )
    canonical_url: str | None = Field(
        default=None,
        alias="canonicalUrl",
        description="The canonical URL the page declares in its own markup, or null when it declares none or the source does not report it.",
    )
    content_type: str | None = Field(
        default=None,
        alias="contentType",
        description="The content type the page was served with (for example text/html;charset=utf-8), or null when unknown.",
    )
    description: str | None = Field(
        default=None,
        description="The page's meta description, empty when the page has none.",
    )
    domain: str = Field(
        description="The page's host name, without a leading www. Populated whenever the provider has data for the entity."
    )
    headings: list[WebCrawlHeading] | None = Field(
        default=None,
        description="The page's headings in document order, each with its level (1 for an h1) and text, or null when the source does not report them.",
    )
    json_ld: list[Any] | None = Field(
        default=None,
        alias="jsonLd",
        description="The JSON-LD structured data blocks the page publishes (schema.org Organization, LocalBusiness, BreadcrumbList and so on), as parsed JSON, or null when the source does not report them. They are the publisher's own claims, not verified facts.",
    )
    language: str | None = Field(
        default=None,
        description="The page's declared language code (for example en-US), or null when unknown.",
    )
    modified_utc: int | None = Field(
        default=None,
        alias="modifiedUtc",
        description="When the page says it was last modified, as a UTC epoch timestamp in seconds (Unix time), or null when unknown. Multiply by 1000 for a JS Date in milliseconds.",
    )
    published_utc: int | None = Field(
        default=None,
        alias="publishedUtc",
        description="When the page says it was published, as a UTC epoch timestamp in seconds (Unix time), or null when unknown. Multiply by 1000 for a JS Date in milliseconds.",
    )
    robots: str | None = Field(
        default=None,
        description="The page's robots meta directives (for example noindex, nofollow), or null when it declares none or the source does not report them.",
    )
    site_name: str | None = Field(
        default=None,
        alias="siteName",
        description="The site name the page declares (its og:site_name), or null when unknown.",
    )
    source_url: str | None = Field(
        default=None,
        alias="sourceUrl",
        description="The URL the crawler requested for this page, before any redirect, or null when unknown.",
    )
    status_code: int | None = Field(
        default=None,
        alias="statusCode",
        description="The HTTP status code the page answered with, or null when unknown.",
    )
    text: str = Field(
        description="The page content as Markdown. Populated whenever the provider has data for the entity."
    )
    title: str | None = Field(
        default=None,
        description="The page title, empty when the page has none (a PDF, for example).",
    )
    url: str | None = Field(
        default=None,
        description="The crawled page's URL, after any redirect. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )


class WebCrawlHeading(BaseModel):
    model_config = ConfigDict(extra="allow")

    level: int | None = Field(default=None, description="The heading level, 1 to 6.")
    text: str | None = Field(default=None, description="The heading text.")


class WebCrawlSummary(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    pages_returned: int = Field(
        alias="pagesReturned",
        description="The number of pages in items, which is the number you are billed for.",
    )
    reported_failed: int | None = Field(
        alias="reportedFailed",
        description="The number of pages the crawl reported as failed, or null when the source does not report a complete count.",
    )
    reported_skipped: int | None = Field(
        alias="reportedSkipped",
        description="The number of pages the crawl reported as skipped, including those robots.txt disallows, or null when the source does not report a complete count.",
    )


class WebMapData(BaseModel):
    results: list[WebMapResult] = Field(
        description="Populated whenever the provider has data for the entity."
    )


class WebMapResult(BaseModel):
    model_config = ConfigDict(extra="allow")

    description: str
    title: str
    url: str = Field(
        description="Populated whenever the provider has data for the entity."
    )


class WebScrapeData(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    description: str = Field(description="The page meta description.")
    html: str | None = Field(
        default=None,
        description="The page HTML exactly as the browser received it, head and script tags included. Present when 'html' is among the requested formats (the default).",
    )
    language: str | None = Field(
        default=None,
        description="Two-letter language code the page declares (its html lang attribute or the equivalent metadata).",
    )
    markdown: str | None = Field(
        default=None,
        description="The page content as clean Markdown. Present when 'markdown' is among the requested formats (the default). Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    raw_html: str | None = Field(
        default=None,
        alias="rawHtml",
        description="The same bytes as 'html'. Deprecated alias returned only when 'rawHtml' is among the requested formats; use 'html'.",
    )
    status_code: int | None = Field(
        default=None,
        alias="statusCode",
        description="HTTP status code the website answered with, such as 200, 404 or 500. Absent when it could not be determined. Some sources report it only when the website answered with an error; name `statusCode` in requireFields to be served only by a source that always reports it.",
    )
    title: str = Field(description="The page title from its metadata.")
    url: str = Field(
        description="The canonical source URL of the scraped page. Populated whenever the provider has data for the entity."
    )


class WebScreenshotData(BaseModel):
    items: list[WebScreenshotItem] = Field(
        description="Screenshot records: the requested page URL and a link to the captured image. Populated whenever the provider has data for the entity."
    )


class WebScreenshotItem(BaseModel):
    model_config = ConfigDict(extra="allow")

    image: str | None = Field(
        default=None,
        description="Link to the captured screenshot image. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    url: str = Field(
        description="The final page URL that was captured. Populated whenever the provider has data for the entity."
    )


class WebNamespace:
    """Typed methods for this platform. Attached lazily to the client."""

    def __init__(self, client: "AnyAPI") -> None:
        self._client = client

    def crawl(
        self, *, options: RequestOptions | None = None, **input: Unpack[WebCrawlInput]
    ) -> RunResult[WebCrawlData]:
        """Website Crawl

        Crawl a website and get up to 10 of its pages as separate items, each with
        its URL, title, description, language, HTTP status, clean Markdown text and
        page metadata such as headings and structured data, ideal for feeding sites
        into LLMs and search indexes. Pages that failed or were skipped are listed
        separately and never billed.

        Price: $0 per request plus $0.00125 per result (maximum $0.0125).

        Example:
            res = client.web.crawl(limit=3, url="https://example.com")
        """
        raw = self._client._run_raw(  # pyright: ignore[reportPrivateUsage]
            "web.crawl", dict(input), options
        )
        return RunResult[WebCrawlData].model_validate(raw)

    def map(
        self, *, options: RequestOptions | None = None, **input: Unpack[WebMapInput]
    ) -> RunResult[WebMapData]:
        """Web Map

        Map an entire website into a clean list of its URLs (with titles and
        descriptions) in a single call.

        Price: $0.001 per request.

        Example:
            res = client.web.map(search="domain", url="https://www.iana.org")
        """
        raw = self._client._run_raw(  # pyright: ignore[reportPrivateUsage]
            "web.map", dict(input), options
        )
        return RunResult[WebMapData].model_validate(raw)

    def scrape(
        self, *, options: RequestOptions | None = None, **input: Unpack[WebScrapeInput]
    ) -> RunResult[WebScrapeData]:
        """Web Scrape

        Scrape any web page and get its content back as clean Markdown (or HTML, or
        raw HTML) plus title and metadata.

        Price: $0.0007 per request.

        Example:
            res = client.web.scrape(formats=["markdown", "html"], onlyMainContent=False, url="https://example.com")
        """
        raw = self._client._run_raw(  # pyright: ignore[reportPrivateUsage]
            "web.scrape", dict(input), options
        )
        return RunResult[WebScrapeData].model_validate(raw)

    def screenshot(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[WebScreenshotInput],
    ) -> RunResult[WebScreenshotData]:
        """Website Screenshot

        Capture a real-browser screenshot of any web page URL.

        Price: $0.0013 per request.

        Example:
            res = client.web.screenshot(url="https://example.com")
        """
        raw = self._client._run_raw(  # pyright: ignore[reportPrivateUsage]
            "web.screenshot", dict(input), options
        )
        return RunResult[WebScreenshotData].model_validate(raw)


class AsyncWebNamespace:
    """Typed methods for this platform. Attached lazily to the client."""

    def __init__(self, client: "AsyncAnyAPI") -> None:
        self._client = client

    async def crawl(
        self, *, options: RequestOptions | None = None, **input: Unpack[WebCrawlInput]
    ) -> RunResult[WebCrawlData]:
        """Website Crawl

        Crawl a website and get up to 10 of its pages as separate items, each with
        its URL, title, description, language, HTTP status, clean Markdown text and
        page metadata such as headings and structured data, ideal for feeding sites
        into LLMs and search indexes. Pages that failed or were skipped are listed
        separately and never billed.

        Price: $0 per request plus $0.00125 per result (maximum $0.0125).

        Example:
            res = client.web.crawl(limit=3, url="https://example.com")
        """
        raw = await self._client._arun_raw(  # pyright: ignore[reportPrivateUsage]
            "web.crawl", dict(input), options
        )
        return RunResult[WebCrawlData].model_validate(raw)

    async def map(
        self, *, options: RequestOptions | None = None, **input: Unpack[WebMapInput]
    ) -> RunResult[WebMapData]:
        """Web Map

        Map an entire website into a clean list of its URLs (with titles and
        descriptions) in a single call.

        Price: $0.001 per request.

        Example:
            res = client.web.map(search="domain", url="https://www.iana.org")
        """
        raw = await self._client._arun_raw(  # pyright: ignore[reportPrivateUsage]
            "web.map", dict(input), options
        )
        return RunResult[WebMapData].model_validate(raw)

    async def scrape(
        self, *, options: RequestOptions | None = None, **input: Unpack[WebScrapeInput]
    ) -> RunResult[WebScrapeData]:
        """Web Scrape

        Scrape any web page and get its content back as clean Markdown (or HTML, or
        raw HTML) plus title and metadata.

        Price: $0.0007 per request.

        Example:
            res = client.web.scrape(formats=["markdown", "html"], onlyMainContent=False, url="https://example.com")
        """
        raw = await self._client._arun_raw(  # pyright: ignore[reportPrivateUsage]
            "web.scrape", dict(input), options
        )
        return RunResult[WebScrapeData].model_validate(raw)

    async def screenshot(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[WebScreenshotInput],
    ) -> RunResult[WebScreenshotData]:
        """Website Screenshot

        Capture a real-browser screenshot of any web page URL.

        Price: $0.0013 per request.

        Example:
            res = client.web.screenshot(url="https://example.com")
        """
        raw = await self._client._arun_raw(  # pyright: ignore[reportPrivateUsage]
            "web.screenshot", dict(input), options
        )
        return RunResult[WebScreenshotData].model_validate(raw)
