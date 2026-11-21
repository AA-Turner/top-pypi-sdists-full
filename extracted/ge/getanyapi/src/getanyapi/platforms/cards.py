# Generated - do not edit. Regenerate with: pnpm generate
"""Generated namespace module for the cards platform."""

from __future__ import annotations

from typing import Literal, TYPE_CHECKING

from pydantic import BaseModel, ConfigDict, Field
from typing_extensions import NotRequired, Required, TypedDict, Unpack

from ..types import RequestOptions, RunResult

if TYPE_CHECKING:
    from .._async_client import AsyncAnyAPI
    from .._client import AnyAPI


class CardsGradedCertInput(TypedDict, total=False):
    """Input for Graded Card Cert Lookup."""

    allowFallbacks: NotRequired[bool]
    """Optional, default true. We recommend leaving it out. Setting it to false is experimental (its behavior may change) and ties the request to the sources listed in `source`: only they may serve, the request is refused with no charge if none of them can, and no other source rescues it when they fail. To control cost, set `max_cost_usd` instead: the REST query parameter or MCP `run_api` argument, on requests paid from your AnyAPI wallet. When true, the listed sources are tried first and any other source may serve after them, at the normal price. Default: true."""
    certNumber: Required[str]
    """Certificate number printed on the slab label, digits only, e.g. 171634124. Keep any leading zeros: BGS numbers start with 00 (0011562845)."""
    gradingCompany: Required[Literal["PSA", "BGS", "SGC", "CGC"]]
    """The company that graded the slab. Required because the same number can exist at two graders (4272318 is both a PSA and an SGC cert)."""
    ignoreSources: NotRequired[list[str]]
    """Optional. Source ids to skip for this request, taken from this endpoint's `lanes[].source.id`. The cheapest remaining source serves. You are charged for the source that serves, plus any source tried before it that charged for its attempt, and never more than the most this endpoint can cost with the remaining sources. An id that does not serve this endpoint, or that is also in `source`, is rejected as invalid input with no charge; skipping every source is rejected the same way."""
    preferLatencyUnderMs: NotRequired[int]
    """Optional; omit it and routing is unchanged, with the cheapest source serving. Prefer sources whose typical response time (median over the trailing 30 days, as published on this endpoint's lane health) is under this many milliseconds; among those, the cheapest serves. This can raise your price: when the cheapest source misses the target, a faster and dearer one serves, and you are quoted and charged its price. If no source is that fast the request is still served, by whichever source offers the best speed for its price - it is never refused for being slow. Sources we have not timed are tried last. This is a preference, not a guarantee: the median describes past requests and is not a ceiling on this one, and it excludes any wait this request itself asks for. On a paginated walk it applies to the first page only: later pages stay with the source that page chose, at the price it was quoted. Minimum: 1."""
    source: NotRequired[list[str]]
    """Optional and experimental: its behavior may change. We recommend leaving it out and letting automatic routing choose: routing serves the cheapest source, uses cheaper sources as they are added, and fails over to another source when one fails, so your requests are not tied to the uptime of one source. To control cost, set a price ceiling instead: on requests paid from your AnyAPI wallet, the `max_cost_usd` REST query parameter or MCP `run_api` argument skips any source that would charge more, and refuses the request with no charge if none is left. Avoid pinning a single source, especially with `allowFallbacks` false: when that source has an outage your requests fail while others are served. If you send it, list source ids from this endpoint's `lanes[].source.id` in /catalog or /apis; they are tried first in the order given, then the others, unless `allowFallbacks` is false. You are charged for the source that serves, plus any source tried before it that charged for its attempt, and never more than the most this endpoint can cost with the sources that may serve. An id that does not serve this endpoint is rejected as invalid input with no charge; a listed source that is not serving right now is refused with no charge, so omit `source` to be served by another. On a paginated walk, later pages must include the source that served page one, or omit `source`."""


class CardsPopulationInput(TypedDict, total=False):
    """Input for Graded Card Population."""

    allowFallbacks: NotRequired[bool]
    """Optional, default true. We recommend leaving it out. Setting it to false is experimental (its behavior may change) and ties the request to the sources listed in `source`: only they may serve, the request is refused with no charge if none of them can, and no other source rescues it when they fail. To control cost, set `max_cost_usd` instead: the REST query parameter or MCP `run_api` argument, on requests paid from your AnyAPI wallet. When true, the listed sources are tried first and any other source may serve after them, at the normal price. Default: true."""
    cardId: Required[str]
    """Card ID from Graded Card Population Search (cards.population_search), 40 hex characters, e.g. ffb8699bb7f435eff4e9761f8e29358e351d777e. Each variant (base, 1st edition, shadowless, refractor...) has its own ID."""
    ignoreSources: NotRequired[list[str]]
    """Optional. Source ids to skip for this request, taken from this endpoint's `lanes[].source.id`. The cheapest remaining source serves. You are charged for the source that serves, plus any source tried before it that charged for its attempt, and never more than the most this endpoint can cost with the remaining sources. An id that does not serve this endpoint, or that is also in `source`, is rejected as invalid input with no charge; skipping every source is rejected the same way."""
    preferLatencyUnderMs: NotRequired[int]
    """Optional; omit it and routing is unchanged, with the cheapest source serving. Prefer sources whose typical response time (median over the trailing 30 days, as published on this endpoint's lane health) is under this many milliseconds; among those, the cheapest serves. This can raise your price: when the cheapest source misses the target, a faster and dearer one serves, and you are quoted and charged its price. If no source is that fast the request is still served, by whichever source offers the best speed for its price - it is never refused for being slow. Sources we have not timed are tried last. This is a preference, not a guarantee: the median describes past requests and is not a ceiling on this one, and it excludes any wait this request itself asks for. On a paginated walk it applies to the first page only: later pages stay with the source that page chose, at the price it was quoted. Minimum: 1."""
    source: NotRequired[list[str]]
    """Optional and experimental: its behavior may change. We recommend leaving it out and letting automatic routing choose: routing serves the cheapest source, uses cheaper sources as they are added, and fails over to another source when one fails, so your requests are not tied to the uptime of one source. To control cost, set a price ceiling instead: on requests paid from your AnyAPI wallet, the `max_cost_usd` REST query parameter or MCP `run_api` argument skips any source that would charge more, and refuses the request with no charge if none is left. Avoid pinning a single source, especially with `allowFallbacks` false: when that source has an outage your requests fail while others are served. If you send it, list source ids from this endpoint's `lanes[].source.id` in /catalog or /apis; they are tried first in the order given, then the others, unless `allowFallbacks` is false. You are charged for the source that serves, plus any source tried before it that charged for its attempt, and never more than the most this endpoint can cost with the sources that may serve. An id that does not serve this endpoint is rejected as invalid input with no charge; a listed source that is not serving right now is refused with no charge, so omit `source` to be served by another. On a paginated walk, later pages must include the source that served page one, or omit `source`."""


class CardsPopulationSearchInput(TypedDict, total=False):
    """Input for Graded Card Population Search."""

    allowFallbacks: NotRequired[bool]
    """Optional, default true. We recommend leaving it out. Setting it to false is experimental (its behavior may change) and ties the request to the sources listed in `source`: only they may serve, the request is refused with no charge if none of them can, and no other source rescues it when they fail. To control cost, set `max_cost_usd` instead: the REST query parameter or MCP `run_api` argument, on requests paid from your AnyAPI wallet. When true, the listed sources are tried first and any other source may serve after them, at the normal price. Default: true."""
    ignoreSources: NotRequired[list[str]]
    """Optional. Source ids to skip for this request, taken from this endpoint's `lanes[].source.id`. The cheapest remaining source serves. You are charged for the source that serves, plus any source tried before it that charged for its attempt, and never more than the most this endpoint can cost with the remaining sources. An id that does not serve this endpoint, or that is also in `source`, is rejected as invalid input with no charge; skipping every source is rejected the same way."""
    page: NotRequired[int]
    """1-based results page of 10 cards, up to 5 pages. Each page is billed as one request. Range: 1 to 5. Default: 1."""
    preferLatencyUnderMs: NotRequired[int]
    """Optional; omit it and routing is unchanged, with the cheapest source serving. Prefer sources whose typical response time (median over the trailing 30 days, as published on this endpoint's lane health) is under this many milliseconds; among those, the cheapest serves. This can raise your price: when the cheapest source misses the target, a faster and dearer one serves, and you are quoted and charged its price. If no source is that fast the request is still served, by whichever source offers the best speed for its price - it is never refused for being slow. Sources we have not timed are tried last. This is a preference, not a guarantee: the median describes past requests and is not a ceiling on this one, and it excludes any wait this request itself asks for. On a paginated walk it applies to the first page only: later pages stay with the source that page chose, at the price it was quoted. Minimum: 1."""
    query: Required[str]
    """Free text describing the card: year, set, player or character, card number and parallel, e.g. "2018 Topps Chrome Update Shohei Ohtani Refractor"."""
    source: NotRequired[list[str]]
    """Optional and experimental: its behavior may change. We recommend leaving it out and letting automatic routing choose: routing serves the cheapest source, uses cheaper sources as they are added, and fails over to another source when one fails, so your requests are not tied to the uptime of one source. To control cost, set a price ceiling instead: on requests paid from your AnyAPI wallet, the `max_cost_usd` REST query parameter or MCP `run_api` argument skips any source that would charge more, and refuses the request with no charge if none is left. Avoid pinning a single source, especially with `allowFallbacks` false: when that source has an outage your requests fail while others are served. If you send it, list source ids from this endpoint's `lanes[].source.id` in /catalog or /apis; they are tried first in the order given, then the others, unless `allowFallbacks` is false. You are charged for the source that serves, plus any source tried before it that charged for its attempt, and never more than the most this endpoint can cost with the sources that may serve. An id that does not serve this endpoint is rejected as invalid input with no charge; a listed source that is not serving right now is refused with no charge, so omit `source` to be served by another. On a paginated walk, later pages must include the source that served page one, or omit `source`."""


class CardsGradedCertData(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    card_name: str | None = Field(
        default=None,
        alias="cardName",
        description='Full card name, e.g. "1999 Pokemon Game Holo Charizard #4". Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.',
    )
    card_number: str | None = Field(
        default=None, alias="cardNumber", description="Card number within the set."
    )
    category: str | None = Field(
        default=None, description="Card category, e.g. pokemon, basketball or football."
    )
    cert_number: str = Field(
        alias="certNumber",
        description="Certificate number of the slab. Populated whenever the provider has data for the entity.",
    )
    cert_url: str | None = Field(
        default=None,
        alias="certUrl",
        description="The grading company's own certificate verification page, when it has one (PSA).",
    )
    grade: float | None = Field(
        default=None,
        description="Numeric grade, e.g. 9.5. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    grade_label: str | None = Field(
        default=None,
        alias="gradeLabel",
        description='Grade as printed with its grader, e.g. "PSA 9" or "BGS 9.5".',
    )
    grading_company: str = Field(
        alias="gradingCompany",
        description="Grading company of the slab: PSA, BGS, SGC or CGC. Populated whenever the provider has data for the entity.",
    )
    image: str | None = Field(
        default=None, description="Card image URL, when one is known."
    )
    last_sale_in_grade: CardsGradedCertLastSaleInGrade | None = Field(
        default=None,
        alias="lastSaleInGrade",
        description="The most recent sale of any copy of this card at this grade. Every member is null when none is recorded.",
    )
    population_in_grade: int | None = Field(
        default=None,
        alias="populationInGrade",
        description="Approximate number of copies of this card graded at this grade by this grader. It tracks the grader's own population report closely (within about 2% for PSA) but is not the official count.",
    )
    qualifier: str | None = Field(
        default=None,
        description="Grade qualifier such as OC (off center) or MK (marks), or null when the grade has none.",
    )
    sales: list[CardsGradedCertSale] | None = Field(
        default=None,
        description="Sales of this exact slab that carry its certificate number, newest first. Sales recorded with the number itself are kept whatever their age; eBay and Fanatics Collect sales are found only from about the last 90 days and only when the seller wrote the number in the title. Empty when no such sale is found, which does not mean the slab never sold.",
    )
    sales_in_grade: int | None = Field(
        default=None,
        alias="salesInGrade",
        description="Number of recorded sales of any copy of this card at this grade.",
    )
    set: str | None = Field(
        default=None, description='Set name, e.g. "Pokemon Game" or "Fleer".'
    )
    subgrades: CardsGradedCertSubgrade | None = Field(
        default=None,
        description="BGS subgrades. Every member is null for graders that do not issue subgrades.",
    )
    subject: str | None = Field(
        default=None, description="Player or character on the card."
    )
    value: float | None = Field(
        default=None,
        description="Estimated market value in USD of this card at this grade, modeled from recent sales.",
    )
    value_confidence: float | None = Field(
        default=None,
        alias="valueConfidence",
        description="Confidence in the estimated value, 0 to 100. Higher means more recent comparable sales.",
    )
    value_high: float | None = Field(
        default=None,
        alias="valueHigh",
        description="High end of the estimated value range in USD.",
    )
    value_low: float | None = Field(
        default=None,
        alias="valueLow",
        description="Low end of the estimated value range in USD.",
    )
    variety: str | None = Field(
        default=None,
        description='Variety or parallel, e.g. "1st Edition Holo" or "Refractor", or null for the base card.',
    )
    year: int | None = Field(default=None, description="Year of the card's set.")


class CardsGradedCertLastSaleInGrade(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    marketplace: str | None = Field(
        default=None,
        description="Where it sold, as a lowercase marketplace id, e.g. ebay, fanatics (Fanatics Collect, including former PWCC venues), goldin or heritage.",
    )
    price: float | None = Field(default=None, description="Sale price in USD.")
    sale_type: str | None = Field(
        default=None,
        alias="saleType",
        description="How it sold: AUCTION, BUY_IT_NOW or BEST_OFFER.",
    )
    sold_utc: float | None = Field(
        default=None,
        alias="soldUtc",
        description="UTC epoch timestamp in seconds (Unix time). Multiply by 1000 for a JS Date in milliseconds.",
    )
    url: str | None = Field(default=None, description="Link to the sold listing.")


class CardsGradedCertSale(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    grade: str | None = Field(
        default=None, description='Grade as listed, e.g. "PSA 6".'
    )
    image: str | None = Field(default=None, description="Listing photo URL.")
    marketplace: str | None = Field(
        default=None,
        description="Where it sold, as a lowercase marketplace id, e.g. ebay, fanatics (Fanatics Collect, including former PWCC venues), goldin or heritage.",
    )
    matched_by: str | None = Field(
        default=None,
        alias="matchedBy",
        description="How the sale was tied to this slab: cert_field (the sale record carries the certificate number) or title (the seller wrote the number in the listing title).",
    )
    price: float | None = Field(default=None, description="Sale price in USD.")
    sale_id: str = Field(alias="saleId", description="Identifier of the sale record.")
    sale_type: str | None = Field(
        default=None,
        alias="saleType",
        description="How it sold: AUCTION, BUY_IT_NOW or BEST_OFFER.",
    )
    shipping_price: float | None = Field(
        default=None,
        alias="shippingPrice",
        description="Shipping charged in USD, when known.",
    )
    sold_utc: float | None = Field(
        default=None,
        alias="soldUtc",
        description="UTC epoch timestamp in seconds (Unix time). Multiply by 1000 for a JS Date in milliseconds.",
    )
    title: str | None = Field(default=None, description="Listing title.")
    url: str | None = Field(default=None, description="Link to the sold listing.")


class CardsGradedCertSubgrade(BaseModel):
    model_config = ConfigDict(extra="allow")

    centering: float | None = Field(default=None, description="Centering subgrade.")
    corners: float | None = Field(default=None, description="Corners subgrade.")
    edges: float | None = Field(default=None, description="Edges subgrade.")
    surfaces: float | None = Field(default=None, description="Surface subgrade.")


class CardsPopulationData(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    by_grader: list[CardsPopulationByGrader] | None = Field(
        default=None,
        alias="byGrader",
        description="Population per grading company. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    card_id: str = Field(
        alias="cardId",
        description="Card ID. Populated whenever the provider has data for the entity.",
    )
    card_number: str | None = Field(
        default=None, alias="cardNumber", description="Card number within the set."
    )
    category: str | None = Field(
        default=None, description="Card category, e.g. tcg-cards or baseball-cards."
    )
    description: str | None = Field(
        default=None,
        description='Full card description, e.g. "1999 Pokemon Game Charizard-Holo Base 4". Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.',
    )
    gem_rate_percent: float | None = Field(
        default=None,
        alias="gemRatePercent",
        description="Share of graded copies that are gem mint or better, in percent.",
    )
    gems: int | None = Field(
        default=None,
        description="Copies graded gem mint or better across all included graders.",
    )
    graders: list[str] | None = Field(
        default=None,
        description='Graders whose counts are included, e.g. ["psa", "bgs", "sgc", "cgc"].',
    )
    image: str | None = Field(default=None, description="Front image URL.")
    image_back: str | None = Field(
        default=None, alias="imageBack", description="Back image URL."
    )
    name: str | None = Field(
        default=None, description="Card name: player or character."
    )
    parallel: str | None = Field(
        default=None,
        description='Variant or parallel name, e.g. "1st Edition" or "Refractor".',
    )
    population_changed_utc: float | None = Field(
        default=None,
        alias="populationChangedUtc",
        description="UTC epoch timestamp in seconds (Unix time). Multiply by 1000 for a JS Date in milliseconds.",
    )
    qualified_grades: list[CardsPopulationQualifiedGrade] | None = Field(
        default=None,
        alias="qualifiedGrades",
        description="PSA copies with a qualified grade (OC, MK, ST and the like) at each numeric grade, counted apart from the plain grades.",
    )
    set: str | None = Field(default=None, description="Set name.")
    total_population: int | None = Field(
        default=None,
        alias="totalPopulation",
        description="Total copies graded across all included graders. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    universal_grades: list[CardsPopulationUniversalGrade] | None = Field(
        default=None,
        alias="universalGrades",
        description="Count at every grade on a common scale that lines up the graders (Perfect, Pristine, Gem Mint, Mint+, 9 down to 1, Authentic), highest first.",
    )
    updated_utc: float | None = Field(
        default=None,
        alias="updatedUtc",
        description="UTC epoch timestamp in seconds (Unix time). Multiply by 1000 for a JS Date in milliseconds.",
    )
    year: int | None = Field(default=None, description="Year of the card's set.")


class CardsPopulationByGrader(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    gem_rate_percent: float | None = Field(
        default=None,
        alias="gemRatePercent",
        description="Share of this grader's copies that are gem mint or better, in percent.",
    )
    gems: int | None = Field(
        default=None, description="Copies this grader graded gem mint or better."
    )
    grader: str = Field(description="Grader code: psa, bgs, sgc or cgc.")
    grader_card_name: str | None = Field(
        default=None,
        alias="graderCardName",
        description="The card as this grader lists it, which can differ from the combined description.",
    )
    grader_name: str | None = Field(
        default=None,
        alias="graderName",
        description='Grader display name, e.g. "Beckett (BGS)".',
    )
    grades: list[CardsPopulationGrade] | None = Field(
        default=None,
        description='Count at each of this grader\'s grades, highest first, including half grades and labels such as "10 Pristine", "10 Black Label" and "Auth". Qualified copies are not in these counts.',
    )
    pop_report_url: str | None = Field(
        default=None,
        alias="popReportUrl",
        description="The grader's own population report page for this card or set.",
    )
    population_changed_utc: float | None = Field(
        default=None,
        alias="populationChangedUtc",
        description="UTC epoch timestamp in seconds (Unix time). Multiply by 1000 for a JS Date in milliseconds.",
    )
    qualified_grades: list[CardsPopulationQualifiedGrade] | None = Field(
        default=None,
        alias="qualifiedGrades",
        description="Copies with a qualified grade (OC, MK and the like) at each numeric grade. To count copies graded higher than a grade the way the grader's own report does, add the qualified copies above it to the plain counts above it. Empty for graders that do not issue qualifiers.",
    )
    qualified_total: int | None = Field(
        default=None,
        alias="qualifiedTotal",
        description="Total qualified copies, or null when the grader issues none.",
    )
    total_graded: int | None = Field(
        default=None,
        alias="totalGraded",
        description="Copies this grader has graded, qualified grades included.",
    )


class CardsPopulationGrade(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    count: int | None = Field(default=None, description="Copies at this grade.")
    grade: str = Field(
        description='Grade as the grader names it, e.g. "10", "9.5" or "10 Pristine".'
    )
    is_gem: bool | None = Field(
        default=None,
        alias="isGem",
        description="True when this grade counts as gem mint or better.",
    )


class CardsPopulationQualifiedGrade(BaseModel):
    model_config = ConfigDict(extra="allow")

    count: int | None = Field(
        default=None, description="Qualified copies at this grade."
    )
    grade: str = Field(description="Numeric grade the qualifier applies to.")


class CardsPopulationUniversalGrade(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    count: int | None = Field(
        default=None, description="Copies at this grade across all included graders."
    )
    grade: str = Field(
        description='Grade on the common scale, e.g. "Gem Mint" or "8.5".'
    )
    percent_graded_higher: float | None = Field(
        default=None,
        alias="percentGradedHigher",
        description="Share of all graded copies graded above this grade, in percent.",
    )
    percent_of_total: float | None = Field(
        default=None,
        alias="percentOfTotal",
        description="Share of all graded copies at this grade, in percent.",
    )


class CardsPopulationSearchData(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    has_more: bool | None = Field(
        default=None,
        alias="hasMore",
        description="True when another page of matches exists.",
    )
    items: list[CardsPopulationSearchItem] = Field(
        description="Matching card variants, best match first. Each variant (base, 1st edition, shadowless, refractor...) is its own row. Populated whenever the provider has data for the entity."
    )


class CardsPopulationSearchItem(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    card_id: str = Field(
        alias="cardId",
        description="Card ID. Pass it as cardId to Graded Card Population (cards.population) for the count at every grade. Populated whenever the provider has data for the entity.",
    )
    card_number: str | None = Field(
        default=None, alias="cardNumber", description="Card number within the set."
    )
    category: str | None = Field(
        default=None, description="Card category, e.g. tcg-cards or baseball-cards."
    )
    description: str | None = Field(
        default=None,
        description='Full card description, e.g. "1999 Pokemon Game Charizard-Holo Base 4". Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.',
    )
    gem_rate_percent: float | None = Field(
        default=None,
        alias="gemRatePercent",
        description="Share of graded copies that are gem mint or better, in percent.",
    )
    gems: int | None = Field(
        default=None, description="Copies graded gem mint or better."
    )
    graders: list[str] | None = Field(
        default=None,
        description='Graders whose counts are included, e.g. ["psa", "bgs", "sgc", "cgc"].',
    )
    image: str | None = Field(default=None, description="Card image URL.")
    name: str | None = Field(
        default=None, description="Card name: player or character."
    )
    parallel: str | None = Field(
        default=None,
        description='Variant or parallel name, e.g. "1st Edition", "Shadowless" or "Refractor".',
    )
    set: str | None = Field(default=None, description="Set name.")
    total_population: int | None = Field(
        default=None,
        alias="totalPopulation",
        description="Total copies graded across the graders listed in graders.",
    )
    year: int | None = Field(default=None, description="Year of the card's set.")


class CardsNamespace:
    """Typed methods for this platform. Attached lazily to the client."""

    def __init__(self, client: "AnyAPI") -> None:
        self._client = client

    def graded_cert(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[CardsGradedCertInput],
    ) -> RunResult[CardsGradedCertData]:
        """Graded Card Cert Lookup

        Look up one graded trading card slab by its PSA, BGS, SGC or CGC certificate
        number and get the card (year, set, number, player or character, variety),
        its grade with BGS subgrades, the approximate population in that grade, the
        estimated market value with its low and high range, the last sale of any
        copy in that grade, and the sales of this exact slab that carry its
        certificate number (eBay and Fanatics Collect sales only from about the last
        90 days, when the seller put the number in the title), in one normalized
        response. Sports cards, Pokemon and other trading card games.

        Price: $0.00338 per request.

        Example:
            res = client.cards.graded_cert(certNumber="0011562845", gradingCompany="BGS")
        """
        raw = self._client._run_raw(  # pyright: ignore[reportPrivateUsage]
            "cards.graded_cert", dict(input), options
        )
        return RunResult[CardsGradedCertData].model_validate(raw)

    def population(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[CardsPopulationInput],
    ) -> RunResult[CardsPopulationData]:
        """Graded Card Population

        Get one graded trading card's population report across PSA, BGS, SGC and CGC
        by card ID (from Graded Card Population Search): total graded, gem count and
        gem rate, the count at every grade on a common scale with the share graded
        higher, and per grader the count at every grade including half grades and
        qualified grades (OC, MK and the like), with the date the population last
        changed. Sports cards, Pokemon and other trading card games.

        Price: $0.00338 per request.

        Example:
            res = client.cards.population(cardId="ffb8699bb7f435eff4e9761f8e29358e351d777e")
        """
        raw = self._client._run_raw(  # pyright: ignore[reportPrivateUsage]
            "cards.population", dict(input), options
        )
        return RunResult[CardsPopulationData].model_validate(raw)

    def population_search(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[CardsPopulationSearchInput],
    ) -> RunResult[CardsPopulationSearchData]:
        """Graded Card Population Search

        Search graded trading cards across PSA, BGS, SGC and CGC by free text (year,
        set, player or character, card number, parallel) and get each matching card
        variant with its card ID, year, set, number, parallel, total graded
        population, gem count and gem rate. Pass the card ID to Graded Card
        Population for the count at every grade.

        Price: $0.00225 per request.

        Example:
            res = client.cards.population_search(query="1999 Pokemon Base Charizard")
        """
        raw = self._client._run_raw(  # pyright: ignore[reportPrivateUsage]
            "cards.population_search", dict(input), options
        )
        return RunResult[CardsPopulationSearchData].model_validate(raw)


class AsyncCardsNamespace:
    """Typed methods for this platform. Attached lazily to the client."""

    def __init__(self, client: "AsyncAnyAPI") -> None:
        self._client = client

    async def graded_cert(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[CardsGradedCertInput],
    ) -> RunResult[CardsGradedCertData]:
        """Graded Card Cert Lookup

        Look up one graded trading card slab by its PSA, BGS, SGC or CGC certificate
        number and get the card (year, set, number, player or character, variety),
        its grade with BGS subgrades, the approximate population in that grade, the
        estimated market value with its low and high range, the last sale of any
        copy in that grade, and the sales of this exact slab that carry its
        certificate number (eBay and Fanatics Collect sales only from about the last
        90 days, when the seller put the number in the title), in one normalized
        response. Sports cards, Pokemon and other trading card games.

        Price: $0.00338 per request.

        Example:
            res = client.cards.graded_cert(certNumber="0011562845", gradingCompany="BGS")
        """
        raw = await self._client._arun_raw(  # pyright: ignore[reportPrivateUsage]
            "cards.graded_cert", dict(input), options
        )
        return RunResult[CardsGradedCertData].model_validate(raw)

    async def population(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[CardsPopulationInput],
    ) -> RunResult[CardsPopulationData]:
        """Graded Card Population

        Get one graded trading card's population report across PSA, BGS, SGC and CGC
        by card ID (from Graded Card Population Search): total graded, gem count and
        gem rate, the count at every grade on a common scale with the share graded
        higher, and per grader the count at every grade including half grades and
        qualified grades (OC, MK and the like), with the date the population last
        changed. Sports cards, Pokemon and other trading card games.

        Price: $0.00338 per request.

        Example:
            res = client.cards.population(cardId="ffb8699bb7f435eff4e9761f8e29358e351d777e")
        """
        raw = await self._client._arun_raw(  # pyright: ignore[reportPrivateUsage]
            "cards.population", dict(input), options
        )
        return RunResult[CardsPopulationData].model_validate(raw)

    async def population_search(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[CardsPopulationSearchInput],
    ) -> RunResult[CardsPopulationSearchData]:
        """Graded Card Population Search

        Search graded trading cards across PSA, BGS, SGC and CGC by free text (year,
        set, player or character, card number, parallel) and get each matching card
        variant with its card ID, year, set, number, parallel, total graded
        population, gem count and gem rate. Pass the card ID to Graded Card
        Population for the count at every grade.

        Price: $0.00225 per request.

        Example:
            res = client.cards.population_search(query="1999 Pokemon Base Charizard")
        """
        raw = await self._client._arun_raw(  # pyright: ignore[reportPrivateUsage]
            "cards.population_search", dict(input), options
        )
        return RunResult[CardsPopulationSearchData].model_validate(raw)
