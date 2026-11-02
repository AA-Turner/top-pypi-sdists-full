# Generated - do not edit. Regenerate with: pnpm generate
"""Generated namespace module for the chatgpt platform."""

from __future__ import annotations

from typing import Literal, TYPE_CHECKING

from pydantic import BaseModel, ConfigDict, Field
from typing_extensions import NotRequired, Required, TypedDict, Unpack

from ..types import RequestOptions, RunResult

if TYPE_CHECKING:
    from .._async_client import AsyncAnyAPI
    from .._client import AnyAPI


class ChatgptSearchInput(TypedDict, total=False):
    """Input for ChatGPT Search."""

    allowFallbacks: NotRequired[bool]
    """Optional, default true. When false, only the sources listed in `source` may serve; the request is refused with no charge if none of them can. When true, the listed sources are tried first and any other source may serve after them, at the normal price. Default: true."""
    country: NotRequired[str]
    """ISO-3166 alpha-2 country to ask from, e.g. US, GB, DE. ChatGPT localizes both the pages it retrieves and the answer it writes, so this is the difference between what a US buyer and a UK buyer are told. Default: US."""
    ignoreSources: NotRequired[list[str]]
    """Optional. Source ids to skip for this request, taken from this endpoint's `lanes[].source.id`. The cheapest remaining source serves and the price is that of the dearest remaining source. An id that does not serve this endpoint, or that is also in `source`, is rejected as invalid input with no charge; skipping every source is rejected the same way."""
    preferLatencyUnderMs: NotRequired[int]
    """Optional; omit it and routing is unchanged, with the cheapest source serving. Prefer sources whose typical response time (median over the trailing 30 days, as published on this endpoint's lane health) is under this many milliseconds; among those, the cheapest serves. This can raise your price: when the cheapest source misses the target, a faster and dearer one serves, and you are quoted and charged its price. If no source is that fast the request is still served, by whichever source offers the best speed for its price - it is never refused for being slow. Sources we have not timed are tried last. This is a preference, not a guarantee: the median describes past requests and is not a ceiling on this one, and it excludes any wait this request itself asks for. On a paginated walk it applies to the first page only: later pages stay with the source that page chose, at the price it was quoted. Minimum: 1."""
    prompt: Required[str]
    """Question or research prompt for ChatGPT to answer using web search."""
    requireAds: NotRequired[bool]
    """Serve only from a source that can return sponsored placements shown with the answer. One source currently qualifies, so the request cannot fall back when it is unavailable. Default: false."""
    requireEntities: NotRequired[bool]
    """Serve only from a source that can return brands and other named entities recognized in the answer. One source currently qualifies, so the request cannot fall back when it is unavailable. Default: false."""
    requireFields: NotRequired[
        list[
            Literal[
                "address",
                "ads",
                "advertiserName",
                "advertiserUrl",
                "answerPosition",
                "category",
                "cited",
                "createdUtc",
                "currency",
                "description",
                "domain",
                "entities",
                "model",
                "name",
                "phone",
                "places",
                "position",
                "reviewCount",
                "searchQueries",
                "searchResults",
                "snippet",
                "webSearchTriggered",
                "websiteUrl",
            ]
        ]
    ]
    """Optional; omit it and routing is unchanged, with the cheapest source serving. Name the output fields this request must be able to return, for example `cited` or `ads`, and it is served only by a source that returns every one of them. Fields you do not name are still returned whenever the serving source has them. This can raise your price: when the cheapest source cannot return a named field, a dearer source serves, and you are quoted and charged its price. A named field can still be absent on a result that genuinely lacks it. Naming a combination that no single source returns together is refused as invalid input, with no charge."""
    requirePlaces: NotRequired[bool]
    """Serve only from a source that can return places shown with the answer. Leaving this off still returns places whenever the source that answered can. Turning it on selects the single source that guarantees them, which costs more and has nothing to fall back to if it is unavailable. Default: false."""
    requireShoppingCards: NotRequired[bool]
    """Serve only from a source that can return shopping cards shown with the answer. Leaving this off still returns shopping cards whenever the source that answered can. Turning it on selects the single source that guarantees them, which costs more and has nothing to fall back to if it is unavailable. Default: false."""
    source: NotRequired[list[str]]
    """Optional. Source ids to prefer, in order, taken from this endpoint's `lanes[].source.id` in /catalog or /apis. Omit it and the cheapest source serves, with automatic failover. Listed sources are tried first in the order given, then the others, unless `allowFallbacks` is false. A single source with `allowFallbacks` false is served only by that source at its price, quoted and charged exactly, with no failover. The price is that of the dearest source that may serve. An id that does not serve this endpoint is rejected as invalid input with no charge; a listed source that is not serving right now is refused with no charge, so omit `source` to be served by another. On a paginated walk, later pages must include the source that served page one, or omit `source`."""
    webSearch: NotRequired[Literal["force", "auto"]]
    """Whether to insist ChatGPT browses the web. force instructs it to search and is the default; auto lets ChatGPT decide, which is cheaper and answers from memory roughly half the time. Check webSearchTriggered for what actually happened - an answer written without a search is not web-grounded. Default: force."""


class ChatgptSearchData(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    ads: list[ChatgptSearchAd] | None = Field(
        default=None,
        description="Sponsored placements ChatGPT displayed with the answer. null means the source that answered cannot report ads; an empty array means none were shown.",
    )
    answer: str = Field(
        description="The web-grounded answer as text. Populated whenever the provider has data for the entity."
    )
    answer_markdown: str = Field(
        alias="answerMarkdown",
        description="The answer in Markdown when the engine returns a Markdown rendering, otherwise the same text as answer. Populated whenever the provider has data for the entity.",
    )
    citations: list[ChatgptSearchCitation] = Field(
        description="Sources cited by the answer. Populated whenever the provider has data for the entity."
    )
    created_utc: float | None = Field(
        default=None,
        alias="createdUtc",
        description="UTC epoch timestamp in seconds (Unix time). Multiply by 1000 for a JS Date in milliseconds. null means the source that answered does not report when it answered.",
    )
    entities: list[ChatgptSearchEntitie] | None = Field(
        default=None,
        description="Brands and other named entities recognized in the answer. null means the source that answered cannot report them; an empty array means none were identified.",
    )
    model: str | None = Field(
        default=None,
        description="The ChatGPT model that produced the answer. null means the source that answered does not report it, which is not the same as an unknown model.",
    )
    places: list[ChatgptSearchPlace] | None = Field(
        default=None,
        description="Places and local businesses ChatGPT displayed with the answer. null means the source that answered cannot report them; an empty array means none were shown.",
    )
    prompt: str = Field(description="The prompt answered by ChatGPT.")
    search_queries: list[str] | None = Field(
        default=None,
        alias="searchQueries",
        description="The web search queries ChatGPT ran to ground its answer. null means the source that answered cannot report them; an empty array means it searched with none recorded.",
    )
    search_results: list[ChatgptSearchSearchResult] | None = Field(
        default=None,
        alias="searchResults",
        description="Pages ChatGPT retrieved while answering. A SUPERSET of citations: a page can be read and not cited. null means the source that answered cannot report them.",
    )
    shopping_cards: list[ChatgptSearchShoppingCard] | None = Field(
        default=None,
        alias="shoppingCards",
        description="Products ChatGPT displayed with the answer. null means the source that answered cannot report shopping cards; an empty array means none were shown.",
    )
    web_search_triggered: bool | None = Field(
        default=None,
        alias="webSearchTriggered",
        description="Whether ChatGPT actually ran a web search before answering. ChatGPT decides this per session, and an answer written without one is not web-grounded. null means the source that answered cannot report it, which is not the same as false.",
    )


class ChatgptSearchAd(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    advertiser_name: str | None = Field(
        default=None, alias="advertiserName", description="Advertiser name."
    )
    advertiser_url: str | None = Field(
        default=None,
        alias="advertiserUrl",
        description="Advertiser URL, tracking parameters stripped.",
    )
    domain: str | None = Field(default=None, description="Advertised domain.")
    image: str | None = Field(default=None, description="Sponsored image URL.")
    snippet: str | None = Field(default=None, description="Sponsored placement text.")
    title: str = Field(description="Sponsored placement title.")
    url: str | None = Field(
        default=None,
        description="Sponsored destination URL, tracking parameters stripped.",
    )


class ChatgptSearchCitation(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    answer_position: int | None = Field(
        default=None,
        alias="answerPosition",
        description="One-based answer section where ChatGPT cited this source. null means the source that answered cannot report the position.",
    )
    title: str = Field(
        description="Source page title when supplied by the search engine."
    )
    url: str = Field(description="Source page URL.")


class ChatgptSearchEntitie(BaseModel):
    model_config = ConfigDict(extra="allow")

    category: str | None = Field(default=None, description="Entity category.")
    domain: str | None = Field(default=None, description="Entity domain.")
    title: str = Field(description="Entity name.")
    url: str | None = Field(
        default=None, description="Entity URL, tracking parameters stripped."
    )


class ChatgptSearchPlace(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    address: str | None = Field(default=None, description="Place address as displayed.")
    category: str | None = Field(
        default=None, description="Place category shown by ChatGPT."
    )
    description: str | None = Field(
        default=None, description="Place description shown by ChatGPT."
    )
    name: str = Field(description="Place or business name.")
    phone: str | None = Field(
        default=None, description="Place phone number as displayed."
    )
    position: int | None = Field(
        default=None, description="One-based position in the places block."
    )
    rating: float | None = Field(
        default=None, description="Place rating when the source reports one."
    )
    review_count: int | None = Field(
        default=None,
        alias="reviewCount",
        description="Number of reviews behind the displayed rating.",
    )
    website_url: str | None = Field(
        default=None,
        alias="websiteUrl",
        description="Place website URL with tracking parameters stripped; an id parameter is kept, since a page such as Facebook profile.php needs it.",
    )


class ChatgptSearchSearchResult(BaseModel):
    model_config = ConfigDict(extra="allow")

    cited: bool | None = Field(
        default=None,
        description="Whether this retrieved page made it into citations. false means ChatGPT read the page and chose not to cite it, which is a different and more actionable fact than the page being absent.",
    )
    title: str | None = Field(
        default=None,
        description="Title of the retrieved page, empty when the source did not send one.",
    )
    url: str | None = Field(
        default=None,
        description="Canonical URL of the retrieved page, tracking parameters stripped.",
    )


class ChatgptSearchShoppingCard(BaseModel):
    model_config = ConfigDict(extra="allow")

    currency: str | None = Field(
        default=None, description="ISO 4217 currency code when the source reports it."
    )
    description: str | None = Field(
        default=None, description="Product description shown on the shopping card."
    )
    image: str | None = Field(default=None, description="Product image URL.")
    merchants: str | None = Field(
        default=None, description="Merchant name shown on the shopping card."
    )
    price: float | None = Field(
        default=None,
        description="Displayed product price as a number when the source reports one.",
    )
    rating: float | None = Field(
        default=None, description="Product rating when the source reports one."
    )
    title: str = Field(description="Product name shown by ChatGPT.")
    url: str | None = Field(
        default=None,
        description="Product page URL with its query kept, since the query can name the product variant (e.g. color and size).",
    )


class ChatgptNamespace:
    """Typed methods for this platform. Attached lazily to the client."""

    def __init__(self, client: "AnyAPI") -> None:
        self._client = client

    def search(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[ChatgptSearchInput],
    ) -> RunResult[ChatgptSearchData]:
        """ChatGPT Search

        Ask ChatGPT a web-grounded question and receive an answer with source
        citations. ChatGPT composes each answer per request, so the same prompt
        returns different wording and a different source set.

        Price: $0.0018 per request.

        Example:
            res = client.chatgpt.search(prompt="What is AnyAPI at getanyapi.com, and what does it offer?")
        """
        raw = self._client._run_raw(  # pyright: ignore[reportPrivateUsage]
            "chatgpt.search", dict(input), options
        )
        return RunResult[ChatgptSearchData].model_validate(raw)


class AsyncChatgptNamespace:
    """Typed methods for this platform. Attached lazily to the client."""

    def __init__(self, client: "AsyncAnyAPI") -> None:
        self._client = client

    async def search(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[ChatgptSearchInput],
    ) -> RunResult[ChatgptSearchData]:
        """ChatGPT Search

        Ask ChatGPT a web-grounded question and receive an answer with source
        citations. ChatGPT composes each answer per request, so the same prompt
        returns different wording and a different source set.

        Price: $0.0018 per request.

        Example:
            res = client.chatgpt.search(prompt="What is AnyAPI at getanyapi.com, and what does it offer?")
        """
        raw = await self._client._arun_raw(  # pyright: ignore[reportPrivateUsage]
            "chatgpt.search", dict(input), options
        )
        return RunResult[ChatgptSearchData].model_validate(raw)
