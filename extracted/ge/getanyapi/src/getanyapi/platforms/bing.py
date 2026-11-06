# Generated - do not edit. Regenerate with: pnpm generate
"""Generated namespace module for the bing platform."""

from __future__ import annotations

from typing import Literal, TYPE_CHECKING

from pydantic import BaseModel, ConfigDict, Field
from typing_extensions import NotRequired, Required, TypedDict, Unpack

from ..types import RequestOptions, RunResult

if TYPE_CHECKING:
    from .._async_client import AsyncAnyAPI
    from .._client import AnyAPI


class BingCopilotInput(TypedDict, total=False):
    """Input for Microsoft Copilot Search."""

    allowFallbacks: NotRequired[bool]
    """Optional, default true. When false, only the sources listed in `source` may serve; the request is refused with no charge if none of them can. When true, the listed sources are tried first and any other source may serve after them, at the normal price. Default: true."""
    ignoreSources: NotRequired[list[str]]
    """Optional. Source ids to skip for this request, taken from this endpoint's `lanes[].source.id`. The cheapest remaining source serves and the price is that of the dearest remaining source. An id that does not serve this endpoint, or that is also in `source`, is rejected as invalid input with no charge; skipping every source is rejected the same way."""
    preferLatencyUnderMs: NotRequired[int]
    """Optional; omit it and routing is unchanged, with the cheapest source serving. Prefer sources whose typical response time (median over the trailing 30 days, as published on this endpoint's lane health) is under this many milliseconds; among those, the cheapest serves. This can raise your price: when the cheapest source misses the target, a faster and dearer one serves, and you are quoted and charged its price. If no source is that fast the request is still served, by whichever source offers the best speed for its price - it is never refused for being slow. Sources we have not timed are tried last. This is a preference, not a guarantee: the median describes past requests and is not a ceiling on this one, and it excludes any wait this request itself asks for. On a paginated walk it applies to the first page only: later pages stay with the source that page chose, at the price it was quoted. Minimum: 1."""
    prompt: Required[str]
    """The question or prompt for Microsoft Copilot to answer using Bing web search."""
    requireFields: NotRequired[
        list[
            Literal[
                "additionalSections",
                "answerMarkdown",
                "caption",
                "complete",
                "domain",
                "headers",
                "inlineCitations",
                "name",
                "recommendations",
                "researchSources",
                "rows",
                "tables",
                "text",
            ]
        ]
    ]
    """Optional; omit it and routing is unchanged, with the cheapest source serving. Name the output fields this request must be able to return, for example `answerMarkdown`, `inlineCitations` or `tables`, and it is served only by a source that returns every one of them. Fields you do not name are still returned whenever the serving source has them. This can raise your price: when the cheapest source cannot return a named field, a dearer source serves, and you are quoted and charged its price. A named field can still be absent on an answer that genuinely lacks it. Naming a combination that no single source returns together is refused as invalid input, with no charge."""
    source: NotRequired[list[str]]
    """Optional. Source ids to prefer, in order, taken from this endpoint's `lanes[].source.id` in /catalog or /apis. Omit it and the cheapest source serves, with automatic failover. Listed sources are tried first in the order given, then the others, unless `allowFallbacks` is false. A single source with `allowFallbacks` false is served only by that source at its price, quoted and charged exactly, with no failover. The price is that of the dearest source that may serve. An id that does not serve this endpoint is rejected as invalid input with no charge; a listed source that is not serving right now is refused with no charge, so omit `source` to be served by another. On a paginated walk, later pages must include the source that served page one, or omit `source`."""


class BingSearchInput(TypedDict, total=False):
    """Input for Bing Search."""

    allowFallbacks: NotRequired[bool]
    """Optional, default true. When false, only the sources listed in `source` may serve; the request is refused with no charge if none of them can. When true, the listed sources are tried first and any other source may serve after them, at the normal price. Default: true."""
    country: NotRequired[str]
    """ISO-3166 alpha-2 country Bing searches from, e.g. US, GB, DE. Bing ranks and localizes results for that country and its main language. Common countries are served by every source; a country only some sources cover is served by those, and one no source covers is refused with no charge. Default: US."""
    ignoreSources: NotRequired[list[str]]
    """Optional. Source ids to skip for this request, taken from this endpoint's `lanes[].source.id`. The cheapest remaining source serves and the price is that of the dearest remaining source. An id that does not serve this endpoint, or that is also in `source`, is rejected as invalid input with no charge; skipping every source is rejected the same way."""
    limit: NotRequired[int]
    """Maximum number of organic results to return (1-10, default 10). Bing serves about 10 organic results per page, and some queries carry fewer. Range: 1 to 10. Default: 10."""
    preferLatencyUnderMs: NotRequired[int]
    """Optional; omit it and routing is unchanged, with the cheapest source serving. Prefer sources whose typical response time (median over the trailing 30 days, as published on this endpoint's lane health) is under this many milliseconds; among those, the cheapest serves. This can raise your price: when the cheapest source misses the target, a faster and dearer one serves, and you are quoted and charged its price. If no source is that fast the request is still served, by whichever source offers the best speed for its price - it is never refused for being slow. Sources we have not timed are tried last. This is a preference, not a guarantee: the median describes past requests and is not a ceiling on this one, and it excludes any wait this request itself asks for. On a paginated walk it applies to the first page only: later pages stay with the source that page chose, at the price it was quoted. Minimum: 1."""
    query: Required[str]
    """The Bing search query."""
    requireFields: NotRequired[
        list[Literal["answer", "peopleAlsoAsk", "publishedUtc", "question", "siteName"]]
    ]
    """Optional; omit it and routing is unchanged, with the cheapest source serving. Name the output fields this request must be able to return, for example `siteName` or `publishedUtc`, and it is served only by a source that returns every one of them. Fields you do not name are still returned whenever the serving source has them. This can raise your price: when the cheapest source cannot return a named field, a dearer source serves, and you are quoted and charged its price. A named field can still be absent on a result that genuinely lacks it. Naming a combination that no single source returns together is refused as invalid input, with no charge."""
    source: NotRequired[list[str]]
    """Optional. Source ids to prefer, in order, taken from this endpoint's `lanes[].source.id` in /catalog or /apis. Omit it and the cheapest source serves, with automatic failover. Listed sources are tried first in the order given, then the others, unless `allowFallbacks` is false. A single source with `allowFallbacks` false is served only by that source at its price, quoted and charged exactly, with no failover. The price is that of the dearest source that may serve. An id that does not serve this endpoint is rejected as invalid input with no charge; a listed source that is not serving right now is refused with no charge, so omit `source` to be served by another. On a paginated walk, later pages must include the source that served page one, or omit `source`."""


class BingCopilotData(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    additional_sections: list[str] | None = Field(
        alias="additionalSections",
        description="Text of answer sections Copilot rendered outside the main answer, such as a section heading or a card, kept so nothing it showed is lost. null means the source that answered cannot report them.",
    )
    answer: str = Field(
        description="Copilot's answer as text. Citation markers Copilot places inline can appear as numbers or source names next to the words they support. Populated whenever the provider has data for the entity."
    )
    answer_markdown: str | None = Field(
        alias="answerMarkdown",
        description="Copilot's answer in Markdown, keeping its bold text, lists and tables. null means the source that answered returns plain text only; name answerMarkdown in requireFields to be served only by a source that returns it.",
    )
    citations: list[BingCopilotCitation] = Field(
        description="Sources Copilot cites for the answer, in the order it lists them. Populated whenever the provider has data for the entity."
    )
    complete: bool | None = Field(
        description="Whether Copilot finished the answer. false means the answer may be cut short. null means the source that answered cannot report it, which is not the same as true."
    )
    inline_citations: list[BingCopilotInlineCitation] | None = Field(
        alias="inlineCitations",
        description="Each claim in the answer that Copilot ties to a source, with the source it cites. null means the source that answered cannot report them.",
    )
    prompt: str = Field(description="The prompt Copilot answered.")
    recommendations: list[BingCopilotRecommendation] | None = Field(
        description="Products, brands or options Copilot recommends in the answer, each with the sentence that recommends it. null means the source that answered cannot report them."
    )
    research_sources: list[BingCopilotResearchSource] | None = Field(
        alias="researchSources",
        description="Pages Copilot searched while researching the answer. A different list from citations: a page here was read but is not necessarily cited. null means the source that answered cannot report them.",
    )
    tables: list[BingCopilotTable] | None = Field(
        description="Tables in the answer, e.g. a comparison table. null means the source that answered cannot report them."
    )


class BingCopilotCitation(BaseModel):
    model_config = ConfigDict(extra="allow")

    domain: str | None = Field(
        description="Host of the source page as Copilot shows it, e.g. blog.salesflare.com. null means the source that answered cannot report it."
    )
    snippet: str | None = Field(
        description="Excerpt of the source page Copilot shows. null when Copilot shows none or the source that answered cannot report it."
    )
    title: str = Field(description="Source page title, empty when Copilot shows none.")
    url: str = Field(
        description="Source page URL. Populated whenever the provider has data for the entity."
    )


class BingCopilotInlineCitation(BaseModel):
    model_config = ConfigDict(extra="allow")

    text: str | None = Field(
        default=None, description="The sentence of the answer the citation supports."
    )
    title: str | None = Field(
        default=None,
        description="Title of the cited source, empty when Copilot shows none.",
    )
    url: str = Field(description="URL of the cited source.")


class BingCopilotRecommendation(BaseModel):
    model_config = ConfigDict(extra="allow")

    name: str = Field(description="Name of the recommended product, brand or option.")
    text: str | None = Field(
        default=None, description="The sentence of the answer that recommends it."
    )


class BingCopilotResearchSource(BaseModel):
    model_config = ConfigDict(extra="allow")

    snippet: str | None = Field(
        default=None,
        description="Excerpt of the page Copilot shows, null when it shows none.",
    )
    title: str | None = Field(
        default=None, description="Title of the page, empty when Copilot shows none."
    )
    url: str = Field(description="URL of the page.")


class BingCopilotTable(BaseModel):
    model_config = ConfigDict(extra="allow")

    caption: str | None = Field(
        default=None, description="Table caption, null when the table has none."
    )
    headers: list[str] | None = Field(default=None, description="Column headers.")
    rows: list[list[str]] | None = Field(
        default=None,
        description="Table rows, each a list of cell texts in column order.",
    )


class BingSearchData(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    items: list[BingSearchItem] = Field(
        description="Organic results in Bing's ranked order. Ads are not included. Populated whenever the provider has data for the entity."
    )
    people_also_ask: list[BingSearchPeopleAlsoAsk] | None = Field(
        alias="peopleAlsoAsk",
        description="Bing's People also ask questions with the answer it shows. An empty array means Bing showed none; null means the source that answered cannot report them.",
    )
    query: str = Field(description="The query Bing searched.")
    related_searches: list[str] | None = Field(
        alias="relatedSearches",
        description="Bing's related searches for the query. An empty array means Bing showed none; null means the source that answered cannot report them.",
    )


class BingSearchItem(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    display_url: str | None = Field(
        alias="displayUrl",
        description="The URL as Bing displays it under the title, e.g. a host or a breadcrumb path. Its format differs by source. null when the source did not send one.",
    )
    domain: str | None = Field(
        description="Host of the result URL without a leading www., e.g. seriouseats.com."
    )
    position: int = Field(
        description="1-based rank of the result on the page. Populated whenever the provider has data for the entity."
    )
    published_utc: int | None = Field(
        alias="publishedUtc",
        description="Page date Bing shows for the result. UTC epoch timestamp in seconds (Unix time). Multiply by 1000 for a JS Date in milliseconds. null when Bing shows no date or the source that answered cannot report it.",
    )
    site_name: str | None = Field(
        alias="siteName",
        description="Site name Bing shows beside the result, e.g. Serious Eats. null means the source that answered cannot report it.",
    )
    snippet: str | None = Field(
        default=None,
        description="Text excerpt Bing shows under the result, often led by the page date. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    title: str = Field(
        description="Result title as Bing shows it. Populated whenever the provider has data for the entity."
    )
    url: str = Field(
        description="Destination URL of the result. Populated whenever the provider has data for the entity."
    )


class BingSearchPeopleAlsoAsk(BaseModel):
    model_config = ConfigDict(extra="allow")

    answer: str | None = Field(
        default=None,
        description="The answer Bing shows under the question, null when it shows none.",
    )
    question: str = Field(description="The question.")
    title: str | None = Field(
        default=None,
        description="Title of the page the answer is taken from, null when Bing names none.",
    )
    url: str | None = Field(
        default=None,
        description="URL of the page the answer is taken from, null when Bing links none.",
    )


class BingNamespace:
    """Typed methods for this platform. Attached lazily to the client."""

    def __init__(self, client: "AnyAPI") -> None:
        self._client = client

    def copilot(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[BingCopilotInput],
    ) -> RunResult[BingCopilotData]:
        """Microsoft Copilot Search

        Ask Microsoft Copilot (the AI answer in Bing) a question and get its
        web-grounded answer with the sources it cites as clean JSON - for tracking
        how Copilot answers and which sites it cites.

        Price: $0.00085 per request.

        Example:
            res = client.bing.copilot(prompt="what is the capital of australia and why")
        """
        raw = self._client._run_raw(  # pyright: ignore[reportPrivateUsage]
            "bing.copilot", dict(input), options
        )
        return RunResult[BingCopilotData].model_validate(raw)

    def search(
        self, *, options: RequestOptions | None = None, **input: Unpack[BingSearchInput]
    ) -> RunResult[BingSearchData]:
        """Bing Search

        Run a Bing web search and get the ranked organic results (title, URL,
        snippet, position, display URL, domain) plus Bing's related searches as
        clean JSON. Returns up to 10 results per call; pick the country Bing
        searches from.

        Price: $0.00085 per request.

        Example:
            res = client.bing.search(country="US", limit=10, query="best espresso machines")
        """
        raw = self._client._run_raw(  # pyright: ignore[reportPrivateUsage]
            "bing.search", dict(input), options
        )
        return RunResult[BingSearchData].model_validate(raw)


class AsyncBingNamespace:
    """Typed methods for this platform. Attached lazily to the client."""

    def __init__(self, client: "AsyncAnyAPI") -> None:
        self._client = client

    async def copilot(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[BingCopilotInput],
    ) -> RunResult[BingCopilotData]:
        """Microsoft Copilot Search

        Ask Microsoft Copilot (the AI answer in Bing) a question and get its
        web-grounded answer with the sources it cites as clean JSON - for tracking
        how Copilot answers and which sites it cites.

        Price: $0.00085 per request.

        Example:
            res = client.bing.copilot(prompt="what is the capital of australia and why")
        """
        raw = await self._client._arun_raw(  # pyright: ignore[reportPrivateUsage]
            "bing.copilot", dict(input), options
        )
        return RunResult[BingCopilotData].model_validate(raw)

    async def search(
        self, *, options: RequestOptions | None = None, **input: Unpack[BingSearchInput]
    ) -> RunResult[BingSearchData]:
        """Bing Search

        Run a Bing web search and get the ranked organic results (title, URL,
        snippet, position, display URL, domain) plus Bing's related searches as
        clean JSON. Returns up to 10 results per call; pick the country Bing
        searches from.

        Price: $0.00085 per request.

        Example:
            res = client.bing.search(country="US", limit=10, query="best espresso machines")
        """
        raw = await self._client._arun_raw(  # pyright: ignore[reportPrivateUsage]
            "bing.search", dict(input), options
        )
        return RunResult[BingSearchData].model_validate(raw)
