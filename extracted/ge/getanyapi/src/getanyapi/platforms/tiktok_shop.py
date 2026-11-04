# Generated - do not edit. Regenerate with: pnpm generate
"""Generated namespace module for the tiktok_shop platform."""

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


class TiktokShopCategoriesInput(TypedDict, total=False):
    """Input for TikTok Shop Categories."""

    allowFallbacks: NotRequired[bool]
    """Optional, default true. When false, only the sources listed in `source` may serve; the request is refused with no charge if none of them can. When true, the listed sources are tried first and any other source may serve after them, at the normal price. Default: true."""
    ignoreSources: NotRequired[list[str]]
    """Optional. Source ids to skip for this request, taken from this endpoint's `lanes[].source.id`. The cheapest remaining source serves and the price is that of the dearest remaining source. An id that does not serve this endpoint, or that is also in `source`, is rejected as invalid input with no charge; skipping every source is rejected the same way."""
    preferLatencyUnderMs: NotRequired[int]
    """Optional; omit it and routing is unchanged, with the cheapest source serving. Prefer sources whose typical response time (median over the trailing 30 days, as published on this endpoint's lane health) is under this many milliseconds; among those, the cheapest serves. This can raise your price: when the cheapest source misses the target, a faster and dearer one serves, and you are quoted and charged its price. If no source is that fast the request is still served, by whichever source offers the best speed for its price - it is never refused for being slow. Sources we have not timed are tried last. This is a preference, not a guarantee: the median describes past requests and is not a ceiling on this one, and it excludes any wait this request itself asks for. On a paginated walk it applies to the first page only: later pages stay with the source that page chose, at the price it was quoted. Minimum: 1."""
    region: NotRequired[Literal["US", "VN"]]
    """Country code of the TikTok Shop market whose category tree to list. Only US and VN publish a category tree. Default: US."""
    source: NotRequired[list[str]]
    """Optional. Source ids to prefer, in order, taken from this endpoint's `lanes[].source.id` in /catalog or /apis. Omit it and the cheapest source serves, with automatic failover. Listed sources are tried first in the order given, then the others, unless `allowFallbacks` is false. A single source with `allowFallbacks` false is served only by that source at its price, quoted and charged exactly, with no failover. The price is that of the dearest source that may serve. An id that does not serve this endpoint is rejected as invalid input with no charge; a listed source that is not serving right now is refused with no charge, so omit `source` to be served by another. On a paginated walk, later pages must include the source that served page one, or omit `source`."""


class TiktokShopCreatorInput(TypedDict, total=False):
    """Input for TikTok Shop Creator."""

    allowFallbacks: NotRequired[bool]
    """Optional, default true. When false, only the sources listed in `source` may serve; the request is refused with no charge if none of them can. When true, the listed sources are tried first and any other source may serve after them, at the normal price. Default: true."""
    handle: Required[str]
    """TikTok handle of the creator or shop account, without the @ (e.g. golinutrition)."""
    ignoreSources: NotRequired[list[str]]
    """Optional. Source ids to skip for this request, taken from this endpoint's `lanes[].source.id`. The cheapest remaining source serves and the price is that of the dearest remaining source. An id that does not serve this endpoint, or that is also in `source`, is rejected as invalid input with no charge; skipping every source is rejected the same way."""
    preferLatencyUnderMs: NotRequired[int]
    """Optional; omit it and routing is unchanged, with the cheapest source serving. Prefer sources whose typical response time (median over the trailing 30 days, as published on this endpoint's lane health) is under this many milliseconds; among those, the cheapest serves. This can raise your price: when the cheapest source misses the target, a faster and dearer one serves, and you are quoted and charged its price. If no source is that fast the request is still served, by whichever source offers the best speed for its price - it is never refused for being slow. Sources we have not timed are tried last. This is a preference, not a guarantee: the median describes past requests and is not a ceiling on this one, and it excludes any wait this request itself asks for. On a paginated walk it applies to the first page only: later pages stay with the source that page chose, at the price it was quoted. Minimum: 1."""
    region: NotRequired[Literal["us", "US"]]
    """Country code of the TikTok Shop market. Only the US market is served; creators in other markets are not available. Default: us."""
    source: NotRequired[list[str]]
    """Optional. Source ids to prefer, in order, taken from this endpoint's `lanes[].source.id` in /catalog or /apis. Omit it and the cheapest source serves, with automatic failover. Listed sources are tried first in the order given, then the others, unless `allowFallbacks` is false. A single source with `allowFallbacks` false is served only by that source at its price, quoted and charged exactly, with no failover. The price is that of the dearest source that may serve. An id that does not serve this endpoint is rejected as invalid input with no charge; a listed source that is not serving right now is refused with no charge, so omit `source` to be served by another. On a paginated walk, later pages must include the source that served page one, or omit `source`."""


class TiktokShopProductInput(TypedDict, total=False):
    """Input for TikTok Shop Product."""

    allowFallbacks: NotRequired[bool]
    """Optional, default true. When false, only the sources listed in `source` may serve; the request is refused with no charge if none of them can. When true, the listed sources are tried first and any other source may serve after them, at the normal price. Default: true."""
    ignoreSources: NotRequired[list[str]]
    """Optional. Source ids to skip for this request, taken from this endpoint's `lanes[].source.id`. The cheapest remaining source serves and the price is that of the dearest remaining source. An id that does not serve this endpoint, or that is also in `source`, is rejected as invalid input with no charge; skipping every source is rejected the same way."""
    preferLatencyUnderMs: NotRequired[int]
    """Optional; omit it and routing is unchanged, with the cheapest source serving. Prefer sources whose typical response time (median over the trailing 30 days, as published on this endpoint's lane health) is under this many milliseconds; among those, the cheapest serves. This can raise your price: when the cheapest source misses the target, a faster and dearer one serves, and you are quoted and charged its price. If no source is that fast the request is still served, by whichever source offers the best speed for its price - it is never refused for being slow. Sources we have not timed are tried last. This is a preference, not a guarantee: the median describes past requests and is not a ceiling on this one, and it excludes any wait this request itself asks for. On a paginated walk it applies to the first page only: later pages stay with the source that page chose, at the price it was quoted. Minimum: 1."""
    region: NotRequired[str]
    """Two-letter country code for the proxy location used to access region-specific products (e.g. US, GB, FR). Defaults to US."""
    requireFields: NotRequired[
        list[
            Literal[
                "brand", "category", "name", "sellerLocation", "specifications", "value"
            ]
        ]
    ]
    """Optional; omit it and routing is unchanged, with the cheapest source serving. Name the output fields this request must be able to return, for example `sellerLocation`, and it is served only by a source that returns every one of them. Fields you do not name are still returned whenever the serving source has them. This can raise your price: when the cheapest source cannot return a named field, a dearer source serves, and you are quoted and charged its price. A named field can still be absent on a product that genuinely lacks it. Naming a combination that no single source returns together is refused as invalid input, with no charge."""
    source: NotRequired[list[str]]
    """Optional. Source ids to prefer, in order, taken from this endpoint's `lanes[].source.id` in /catalog or /apis. Omit it and the cheapest source serves, with automatic failover. Listed sources are tried first in the order given, then the others, unless `allowFallbacks` is false. A single source with `allowFallbacks` false is served only by that source at its price, quoted and charged exactly, with no failover. The price is that of the dearest source that may serve. An id that does not serve this endpoint is rejected as invalid input with no charge; a listed source that is not serving right now is refused with no charge, so omit `source` to be served by another. On a paginated walk, later pages must include the source that served page one, or omit `source`."""
    url: Required[str]
    """TikTok Shop product detail page URL (e.g. https://www.tiktok.com/shop/pdp/.../1729587769570529799)."""


class TiktokShopProductReviewsInput(TypedDict, total=False):
    """Input for TikTok Shop Product Reviews."""

    allowFallbacks: NotRequired[bool]
    """Optional, default true. When false, only the sources listed in `source` may serve; the request is refused with no charge if none of them can. When true, the listed sources are tried first and any other source may serve after them, at the normal price. Default: true."""
    ignoreSources: NotRequired[list[str]]
    """Optional. Source ids to skip for this request, taken from this endpoint's `lanes[].source.id`. The cheapest remaining source serves and the price is that of the dearest remaining source. An id that does not serve this endpoint, or that is also in `source`, is rejected as invalid input with no charge; skipping every source is rejected the same way."""
    page: NotRequired[int]
    """1-based results page. Use with hasMore in the output to paginate. Minimum: 1. Default: 1."""
    preferLatencyUnderMs: NotRequired[int]
    """Optional; omit it and routing is unchanged, with the cheapest source serving. Prefer sources whose typical response time (median over the trailing 30 days, as published on this endpoint's lane health) is under this many milliseconds; among those, the cheapest serves. This can raise your price: when the cheapest source misses the target, a faster and dearer one serves, and you are quoted and charged its price. If no source is that fast the request is still served, by whichever source offers the best speed for its price - it is never refused for being slow. Sources we have not timed are tried last. This is a preference, not a guarantee: the median describes past requests and is not a ceiling on this one, and it excludes any wait this request itself asks for. On a paginated walk it applies to the first page only: later pages stay with the source that page chose, at the price it was quoted. Minimum: 1."""
    region: NotRequired[str]
    """Two-letter country code of the product's shop region (e.g. US). Strongly recommended for correct results."""
    requireFields: NotRequired[list[Literal["images", "rating"]]]
    """Optional; omit it and routing is unchanged, with the cheapest source serving. Name the output fields this request must be able to return, for example `images`, and it is served only by a source that returns every one of them. Fields you do not name are still returned whenever the serving source has them. This can raise your price: when the cheapest source cannot return a named field, a dearer source serves, and you are quoted and charged its price. A named field can still be empty on a review that genuinely lacks it. Naming a combination that no single source returns together is refused as invalid input, with no charge."""
    source: NotRequired[list[str]]
    """Optional. Source ids to prefer, in order, taken from this endpoint's `lanes[].source.id` in /catalog or /apis. Omit it and the cheapest source serves, with automatic failover. Listed sources are tried first in the order given, then the others, unless `allowFallbacks` is false. A single source with `allowFallbacks` false is served only by that source at its price, quoted and charged exactly, with no failover. The price is that of the dearest source that may serve. An id that does not serve this endpoint is rejected as invalid input with no charge; a listed source that is not serving right now is refused with no charge, so omit `source` to be served by another. On a paginated walk, later pages must include the source that served page one, or omit `source`."""
    url: Required[str]
    """TikTok Shop product URL (e.g. https://www.tiktok.com/shop/pdp/.../1729385633899532161)."""


class TiktokShopSearchInput(TypedDict, total=False):
    """Input for TikTok Shop Search."""

    allowFallbacks: NotRequired[bool]
    """Optional, default true. When false, only the sources listed in `source` may serve; the request is refused with no charge if none of them can. When true, the listed sources are tried first and any other source may serve after them, at the normal price. Default: true."""
    country: NotRequired[
        Literal[
            "US",
            "VN",
            "TH",
            "PH",
            "MY",
            "ID",
            "GB",
            "SG",
            "ES",
            "MX",
            "DE",
            "IT",
            "FR",
            "BR",
            "JP",
        ]
    ]
    """Country code of the TikTok Shop market to search (e.g. US). Default: US."""
    ignoreSources: NotRequired[list[str]]
    """Optional. Source ids to skip for this request, taken from this endpoint's `lanes[].source.id`. The cheapest remaining source serves and the price is that of the dearest remaining source. An id that does not serve this endpoint, or that is also in `source`, is rejected as invalid input with no charge; skipping every source is rejected the same way."""
    limit: NotRequired[int]
    """Maximum products to return, honoured on US searches up to 30. Other countries and larger values return every product TikTok Shop gives for the query, typically about 30 and occasionally more than 50. The price per call is the same either way. Minimum: 1."""
    preferLatencyUnderMs: NotRequired[int]
    """Optional; omit it and routing is unchanged, with the cheapest source serving. Prefer sources whose typical response time (median over the trailing 30 days, as published on this endpoint's lane health) is under this many milliseconds; among those, the cheapest serves. This can raise your price: when the cheapest source misses the target, a faster and dearer one serves, and you are quoted and charged its price. If no source is that fast the request is still served, by whichever source offers the best speed for its price - it is never refused for being slow. Sources we have not timed are tried last. This is a preference, not a guarantee: the median describes past requests and is not a ceiling on this one, and it excludes any wait this request itself asks for. On a paginated walk it applies to the first page only: later pages stay with the source that page chose, at the price it was quoted. Minimum: 1."""
    query: Required[str]
    """Search keyword for TikTok Shop products (e.g. wireless earbuds)."""
    requireFields: NotRequired[list[Literal["currency", "reviewCount"]]]
    """Optional; omit it and routing is unchanged, with the cheapest source serving. Name the output fields this request must be able to return, for example `currency`, and it is served only by a source that returns every one of them. Fields you do not name are still returned whenever the serving source has them. This can raise your price: when the cheapest source cannot return a named field, a dearer source serves, and you are quoted and charged its price. A named field can still be absent on a product that genuinely lacks it. Naming a combination that no single source returns together is refused as invalid input, with no charge."""
    source: NotRequired[list[str]]
    """Optional. Source ids to prefer, in order, taken from this endpoint's `lanes[].source.id` in /catalog or /apis. Omit it and the cheapest source serves, with automatic failover. Listed sources are tried first in the order given, then the others, unless `allowFallbacks` is false. A single source with `allowFallbacks` false is served only by that source at its price, quoted and charged exactly, with no failover. The price is that of the dearest source that may serve. An id that does not serve this endpoint is rejected as invalid input with no charge; a listed source that is not serving right now is refused with no charge, so omit `source` to be served by another. On a paginated walk, later pages must include the source that served page one, or omit `source`."""


class TiktokShopSearchSuggestionsInput(TypedDict, total=False):
    """Input for TikTok Shop Search Suggestions."""

    allowFallbacks: NotRequired[bool]
    """Optional, default true. When false, only the sources listed in `source` may serve; the request is refused with no charge if none of them can. When true, the listed sources are tried first and any other source may serve after them, at the normal price. Default: true."""
    country: NotRequired[str]
    """Two-letter country code of the TikTok Shop market (e.g. US). Default: US."""
    ignoreSources: NotRequired[list[str]]
    """Optional. Source ids to skip for this request, taken from this endpoint's `lanes[].source.id`. The cheapest remaining source serves and the price is that of the dearest remaining source. An id that does not serve this endpoint, or that is also in `source`, is rejected as invalid input with no charge; skipping every source is rejected the same way."""
    language: NotRequired[str]
    """Language tag for the suggestions (e.g. en-US). Default: en-US."""
    preferLatencyUnderMs: NotRequired[int]
    """Optional; omit it and routing is unchanged, with the cheapest source serving. Prefer sources whose typical response time (median over the trailing 30 days, as published on this endpoint's lane health) is under this many milliseconds; among those, the cheapest serves. This can raise your price: when the cheapest source misses the target, a faster and dearer one serves, and you are quoted and charged its price. If no source is that fast the request is still served, by whichever source offers the best speed for its price - it is never refused for being slow. Sources we have not timed are tried last. This is a preference, not a guarantee: the median describes past requests and is not a ceiling on this one, and it excludes any wait this request itself asks for. On a paginated walk it applies to the first page only: later pages stay with the source that page chose, at the price it was quoted. Minimum: 1."""
    query: Required[str]
    """Seed keyword to expand (e.g. ashwagandha gummies)."""
    source: NotRequired[list[str]]
    """Optional. Source ids to prefer, in order, taken from this endpoint's `lanes[].source.id` in /catalog or /apis. Omit it and the cheapest source serves, with automatic failover. Listed sources are tried first in the order given, then the others, unless `allowFallbacks` is false. A single source with `allowFallbacks` false is served only by that source at its price, quoted and charged exactly, with no failover. The price is that of the dearest source that may serve. An id that does not serve this endpoint is rejected as invalid input with no charge; a listed source that is not serving right now is refused with no charge, so omit `source` to be served by another. On a paginated walk, later pages must include the source that served page one, or omit `source`."""


class TiktokShopShopProductsInput(TypedDict, total=False):
    """Input for TikTok Shop Store Products."""

    allowFallbacks: NotRequired[bool]
    """Optional, default true. When false, only the sources listed in `source` may serve; the request is refused with no charge if none of them can. When true, the listed sources are tried first and any other source may serve after them, at the normal price. Default: true."""
    cursor: NotRequired[str]
    """Opaque pagination cursor from a previous response's nextCursor."""
    ignoreSources: NotRequired[list[str]]
    """Optional. Source ids to skip for this request, taken from this endpoint's `lanes[].source.id`. The cheapest remaining source serves and the price is that of the dearest remaining source. An id that does not serve this endpoint, or that is also in `source`, is rejected as invalid input with no charge; skipping every source is rejected the same way."""
    preferLatencyUnderMs: NotRequired[int]
    """Optional; omit it and routing is unchanged, with the cheapest source serving. Prefer sources whose typical response time (median over the trailing 30 days, as published on this endpoint's lane health) is under this many milliseconds; among those, the cheapest serves. This can raise your price: when the cheapest source misses the target, a faster and dearer one serves, and you are quoted and charged its price. If no source is that fast the request is still served, by whichever source offers the best speed for its price - it is never refused for being slow. Sources we have not timed are tried last. This is a preference, not a guarantee: the median describes past requests and is not a ceiling on this one, and it excludes any wait this request itself asks for. On a paginated walk it applies to the first page only: later pages stay with the source that page chose, at the price it was quoted. Minimum: 1."""
    region: NotRequired[str]
    """Two-letter country code of the store's market (e.g. US)."""
    requireFields: NotRequired[list[Literal["productCount", "shopRating", "soldCount"]]]
    """Optional; omit it and routing is unchanged, with the cheapest source serving. Name the output fields this request must be able to return, for example `shopRating`, and it is served only by a source that returns every one of them. Fields you do not name are still returned whenever the serving source has them. This can raise your price: when the cheapest source cannot return a named field, a dearer source serves, and you are quoted and charged its price. A named field can still be absent on a store that genuinely lacks it. Naming a combination that no single source returns together is refused as invalid input, with no charge. On a paginated walk it applies to the first page only; later pages stay with the source that page chose, at the price it was quoted."""
    sortBy: NotRequired[Literal["top", "new_releases"]]
    """Product ordering within the store. Default: top."""
    source: NotRequired[list[str]]
    """Optional. Source ids to prefer, in order, taken from this endpoint's `lanes[].source.id` in /catalog or /apis. Omit it and the cheapest source serves, with automatic failover. Listed sources are tried first in the order given, then the others, unless `allowFallbacks` is false. A single source with `allowFallbacks` false is served only by that source at its price, quoted and charged exactly, with no failover. The price is that of the dearest source that may serve. An id that does not serve this endpoint is rejected as invalid input with no charge; a listed source that is not serving right now is refused with no charge, so omit `source` to be served by another. On a paginated walk, later pages must include the source that served page one, or omit `source`."""
    url: Required[str]
    """TikTok Shop store URL (e.g. https://www.tiktok.com/shop/store/<name>/<id> or https://shop.tiktok.com/us/store/<name>/<id>). The link must include the store's numeric id, the long number after the store name: a link with only the name (tiktok.com/shop/store/<name>) does not open a store page on TikTok. A link without the store id, a vt.tiktok.com or vm.tiktok.com share link, or any link that is not a store page, is refused as invalid input, with no charge; send the store page link with its id (tiktok.com/shop/store/<name>/<id>) instead."""


class TiktokShopUserShowcaseInput(TypedDict, total=False):
    """Input for TikTok Shop User Showcase."""

    allowFallbacks: NotRequired[bool]
    """Optional, default true. When false, only the sources listed in `source` may serve; the request is refused with no charge if none of them can. When true, the listed sources are tried first and any other source may serve after them, at the normal price. Default: true."""
    cursor: NotRequired[str]
    """Pagination token for retrieving subsequent product pages."""
    handle: Required[str]
    """The handle of the TikTok user (e.g. mrtiktokreviews)."""
    ignoreSources: NotRequired[list[str]]
    """Optional. Source ids to skip for this request, taken from this endpoint's `lanes[].source.id`. The cheapest remaining source serves and the price is that of the dearest remaining source. An id that does not serve this endpoint, or that is also in `source`, is rejected as invalid input with no charge; skipping every source is rejected the same way."""
    preferLatencyUnderMs: NotRequired[int]
    """Optional; omit it and routing is unchanged, with the cheapest source serving. Prefer sources whose typical response time (median over the trailing 30 days, as published on this endpoint's lane health) is under this many milliseconds; among those, the cheapest serves. This can raise your price: when the cheapest source misses the target, a faster and dearer one serves, and you are quoted and charged its price. If no source is that fast the request is still served, by whichever source offers the best speed for its price - it is never refused for being slow. Sources we have not timed are tried last. This is a preference, not a guarantee: the median describes past requests and is not a ceiling on this one, and it excludes any wait this request itself asks for. On a paginated walk it applies to the first page only: later pages stay with the source that page chose, at the price it was quoted. Minimum: 1."""
    region: NotRequired[str]
    """Geographical region for proxy placement (defaults to US)."""
    source: NotRequired[list[str]]
    """Optional. Source ids to prefer, in order, taken from this endpoint's `lanes[].source.id` in /catalog or /apis. Omit it and the cheapest source serves, with automatic failover. Listed sources are tried first in the order given, then the others, unless `allowFallbacks` is false. A single source with `allowFallbacks` false is served only by that source at its price, quoted and charged exactly, with no failover. The price is that of the dearest source that may serve. An id that does not serve this endpoint is rejected as invalid input with no charge; a listed source that is not serving right now is refused with no charge, so omit `source` to be served by another. On a paginated walk, later pages must include the source that served page one, or omit `source`."""


class TiktokShopCategoriesData(BaseModel):
    categories: list[TiktokShopCategoriesCategorie] = Field(
        description="Top-level TikTok Shop categories for the market, each with its child categories. Populated whenever the provider has data for the entity."
    )


class TiktokShopCategoriesCategorie(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    category_id: str = Field(
        alias="categoryId",
        description="TikTok Shop category id. Populated whenever the provider has data for the entity.",
    )
    children: list[TiktokShopCategoriesChildren] | None = Field(
        default=None, description="Child categories one level down."
    )
    image: str | None = Field(default=None, description="Category tile image URL.")
    is_leaf: bool | None = Field(
        default=None,
        alias="isLeaf",
        description="True when the category has no children.",
    )
    name: str = Field(
        description="Display name of the category. Populated whenever the provider has data for the entity."
    )
    slug: str | None = Field(default=None, description="URL slug of the category.")


class TiktokShopCategoriesChildren(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    category_id: str = Field(alias="categoryId", description="TikTok Shop category id.")
    image: str | None = Field(default=None, description="Category image URL.")
    is_leaf: bool | None = Field(
        default=None,
        alias="isLeaf",
        description="True when the category has no children.",
    )
    name: str = Field(description="Display name of the category.")
    slug: str | None = Field(default=None, description="URL slug of the category.")


class TiktokShopCreatorData(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    audience_age: list[TiktokShopCreatorAudienceAge] | None = Field(
        default=None, alias="audienceAge", description="Follower age distribution."
    )
    audience_gender: list[TiktokShopCreatorAudienceGender] | None = Field(
        default=None,
        alias="audienceGender",
        description="Follower gender distribution.",
    )
    audience_locations: list[TiktokShopCreatorAudienceLocation] | None = Field(
        default=None, alias="audienceLocations", description="Top follower locations."
    )
    avg_commission_range: str | None = Field(
        default=None,
        alias="avgCommissionRange",
        description="Banded average affiliate commission rate the creator earns. Empty when upstream does not publish it.",
    )
    avg_live_likes: float | None = Field(
        default=None, alias="avgLiveLikes", description="Average likes per live stream."
    )
    avg_live_views: float | None = Field(
        default=None,
        alias="avgLiveViews",
        description="Average viewers per live stream.",
    )
    avg_video_comments: float | None = Field(
        default=None,
        alias="avgVideoComments",
        description="Average comments per video.",
    )
    avg_video_likes: float | None = Field(
        default=None, alias="avgVideoLikes", description="Average likes per video."
    )
    avg_video_views: float | None = Field(
        default=None, alias="avgVideoViews", description="Average views per video."
    )
    bio: str | None = Field(default=None, description="Creator bio text.")
    brand_collaborations: int | None = Field(
        default=None,
        alias="brandCollaborations",
        description="Number of distinct brands the creator has collaborated with.",
    )
    categories: list[TiktokShopCreatorCategorie] | None = Field(
        default=None, description="TikTok Shop categories the creator sells in."
    )
    followers: int | None = Field(default=None, description="Follower count.")
    gmv_range: str | None = Field(
        default=None,
        alias="gmvRange",
        description='Banded gross merchandise value the creator has driven, e.g. "$25K-$60K". Upstream publishes a band rather than an exact figure.',
    )
    gpm: float | None = Field(
        default=None,
        description="Gross merchandise value per thousand views. Null when upstream does not publish it.",
    )
    handle: str = Field(
        description="TikTok handle of the creator, without the @. Populated whenever the provider has data for the entity."
    )
    image: str | None = Field(default=None, description="Creator avatar URL.")
    live_count: int | None = Field(
        default=None,
        alias="liveCount",
        description="Number of live streams in the measured window.",
    )
    live_engagement_rate: float | None = Field(
        default=None,
        alias="liveEngagementRate",
        description="Engagement rate on live streams, as a percentage.",
    )
    nickname: str | None = Field(
        default=None,
        description="Display name of the creator. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    post_rate: float | None = Field(
        default=None,
        alias="postRate",
        description="Share of the creator's posts that carry a shop product, as a percentage.",
    )
    promoted_products: int | None = Field(
        default=None,
        alias="promotedProducts",
        description="Number of TikTok Shop products the creator has promoted.",
    )
    rating: float | None = Field(
        default=None,
        description="Creator rating. Null when upstream does not publish it.",
    )
    region: str | None = Field(
        default=None,
        description="Two-letter country code of the creator's TikTok Shop market.",
    )
    video_count: int | None = Field(
        default=None,
        alias="videoCount",
        description="Number of videos posted in the measured window.",
    )
    video_engagement_rate: float | None = Field(
        default=None,
        alias="videoEngagementRate",
        description="Engagement rate on videos, as a percentage.",
    )


class TiktokShopCreatorAudienceAge(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    bucket: str | None = Field(default=None, description="Age bucket, e.g. 25-34.")
    share_pct: float | None = Field(
        default=None,
        alias="sharePct",
        description="Share of followers in this bucket, as a percentage.",
    )


class TiktokShopCreatorAudienceGender(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    gender: str | None = Field(
        default=None, description="Gender label as published upstream."
    )
    share_pct: float | None = Field(
        default=None,
        alias="sharePct",
        description="Share of followers, as a percentage.",
    )


class TiktokShopCreatorAudienceLocation(BaseModel):
    model_config = ConfigDict(extra="allow")

    followers: int | None = Field(
        default=None, description="Followers in this location."
    )
    state: str | None = Field(default=None, description="State or region name.")


class TiktokShopCreatorCategorie(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    category_id: str | None = Field(
        default=None, alias="categoryId", description="TikTok Shop category id."
    )
    name: str | None = Field(default=None, description="Category display name.")


class TiktokShopProductData(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    brand: str | None = Field(
        default=None,
        description="Brand as the seller listed it. Omitted when not listed or when the serving source does not report it.",
    )
    category: str | None = Field(
        default=None,
        description='Top-level TikTok Shop category, e.g. "Health". Omitted when the serving source does not report it.',
    )
    currency: str = Field(
        description="Populated whenever the provider has data for the entity."
    )
    images: list[str] | None = Field(
        default=None,
        description="Product photo URLs, main photo first. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    original_price: str = Field(
        alias="originalPrice",
        description="Populated whenever the provider has data for the entity.",
    )
    price: str = Field(
        description="Populated whenever the provider has data for the entity."
    )
    product_id: str = Field(
        alias="productId",
        description="Populated whenever the provider has data for the entity.",
    )
    rating: float
    review_count: int = Field(alias="reviewCount")
    seller_id: str | None = Field(
        default=None,
        alias="sellerId",
        description="TikTok Shop seller id, for joining to the seller's other products. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    seller_location: str | None = Field(
        alias="sellerLocation",
        description="Where the seller is based, or null when the serving source does not report it.",
    )
    seller_name: str = Field(
        alias="sellerName",
        description="Populated whenever the provider has data for the entity.",
    )
    sold_count: int = Field(alias="soldCount")
    specifications: list[TiktokShopProductSpecification] | None = Field(
        default=None,
        description="The product's attribute table as the seller filled it in (brand, flavor, manufacturer and so on); the set of names varies by category. Omitted when the serving source does not report it.",
    )
    title: str = Field(
        description="Populated whenever the provider has data for the entity."
    )
    url: str | None = Field(
        default=None,
        description="Product detail page URL. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )


class TiktokShopProductSpecification(BaseModel):
    model_config = ConfigDict(extra="allow")

    name: str = Field(description="Attribute name, e.g. Brand.")
    value: str = Field(description="Attribute value as the seller entered it.")


class TiktokShopProductReviewsData(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    has_more: bool = Field(
        alias="hasMore",
        description="True when more reviews are available beyond this page.",
    )
    rating: float | None = Field(
        description="Overall product score (1-5), or null when the serving source does not report it."
    )
    reviews: list[TiktokShopProductReviewsReview] = Field(
        description="Product reviews. Populated whenever the provider has data for the entity."
    )
    total_reviews: int | None = Field(
        alias="totalReviews",
        description="Total number of reviews for the product, or null when the serving source does not report it.",
    )


class TiktokShopProductReviewsReview(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    avatar_url: str | None = Field(
        default=None,
        alias="avatarUrl",
        description="Reviewer's avatar image URL. Signed and short-lived, so the query string is load-bearing and kept intact.",
    )
    country: str = Field(description="Reviewer's country code.")
    created_utc: float = Field(
        alias="createdUtc",
        description="Review time as epoch milliseconds. Populated whenever the provider has data for the entity.",
    )
    id: str = Field(
        description="Review identifier. Populated whenever the provider has data for the entity."
    )
    images: list[str] | None = Field(
        default=None,
        description="Photos the reviewer attached, as image URLs; empty when the review has none. Some are signed and short-lived, so the query string is kept intact. Omitted when the serving source does not report review photos.",
    )
    product_id: str | None = Field(
        default=None,
        alias="productId",
        description="Identifier of the reviewed product.",
    )
    rating: float = Field(description="Star rating for this review (1-5).")
    reviewer_name: str = Field(
        alias="reviewerName",
        description="Display name of the reviewer. Populated whenever the provider has data for the entity.",
    )
    sku: str = Field(
        description='Variant bought, e.g. "Color: Black". Populated whenever the provider has data for the entity.'
    )
    text: str = Field(
        description="Review text content. Populated whenever the provider has data for the entity."
    )
    verified_purchase: bool = Field(
        alias="verifiedPurchase",
        description="True when the review is from a verified purchase.",
    )


class TiktokShopSearchData(BaseModel):
    items: list[TiktokShopSearchItem] = Field(
        description="Product records matching the search query: id, title, price, sales count, rating, seller, and product URL. Populated whenever the provider has data for the entity."
    )


class TiktokShopSearchItem(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    currency: str | None = Field(
        default=None, description="ISO currency name, e.g. USD."
    )
    discount_pct: float | None = Field(
        default=None,
        alias="discountPct",
        description="Discount off the original price as a percentage, e.g. 10 for 10% off. Omitted when the product is not discounted.",
    )
    image: str | None = Field(default=None, description="Product image URL.")
    original_price: float | None = Field(
        default=None,
        alias="originalPrice",
        description="Pre-discount list price. Omitted when the product is not on sale.",
    )
    price: float | None = Field(default=None, description="Current sale price.")
    product_id: str = Field(
        alias="productId",
        description="TikTok Shop product id. Populated whenever the provider has data for the entity.",
    )
    rating: float | None = Field(
        default=None,
        description="Average review score. Omitted when the product has no rating yet.",
    )
    review_count: int | None = Field(
        default=None,
        alias="reviewCount",
        description="Number of reviews. Omitted when the lane that served this request does not report it.",
    )
    seller_id: str | None = Field(
        default=None,
        alias="sellerId",
        description="TikTok Shop seller id, for joining to the seller's other products.",
    )
    shop_name: str | None = Field(
        default=None, alias="shopName", description="Seller shop name."
    )
    sold_count: int | None = Field(
        default=None, alias="soldCount", description="Units sold."
    )
    title: str = Field(
        description="Product title. Populated whenever the provider has data for the entity."
    )
    url: str | None = Field(
        default=None,
        description="Canonical product detail page URL. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )


class TiktokShopSearchSuggestionsData(BaseModel):
    model_config = ConfigDict(extra="allow")

    suggestions: list[str] = Field(
        description="Autocomplete terms TikTok Shop suggests for the seed keyword, most relevant first. Populated whenever the provider has data for the entity."
    )


class TiktokShopShopProductsData(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    has_more: bool = Field(alias="hasMore")
    next_cursor: str | None = Field(
        alias="nextCursor",
        description="Opaque cursor for the next page of products, or null when this lane has no more. Pass it back as cursor to continue.",
    )
    product_count: int | None = Field(
        alias="productCount",
        description="Number of products the store has on sale, or null when the serving source does not report it.",
    )
    products: list[TiktokShopShopProductsProduct] = Field(
        description="Populated whenever the provider has data for the entity."
    )
    shop_name: str = Field(
        alias="shopName",
        description="Populated whenever the provider has data for the entity.",
    )
    shop_rating: float | None = Field(
        alias="shopRating",
        description="The store's rating out of 5, or null when the serving source does not report it.",
    )
    sold_count: int | None = Field(
        alias="soldCount",
        description="Units the store has sold across all its products, or null when the serving source does not report it.",
    )


class TiktokShopShopProductsProduct(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    currency: str
    discount_pct: float | None = Field(
        default=None,
        alias="discountPct",
        description="Discount off the original price as a percentage, e.g. 10 for 10% off. Omitted when the product is not discounted.",
    )
    image: str | None = Field(default=None, description="Product image URL.")
    original_price: float | None = Field(
        alias="originalPrice",
        description="Pre-discount list price, or null when the product is not on sale.",
    )
    price: float
    product_id: str = Field(
        alias="productId",
        description="Populated whenever the provider has data for the entity.",
    )
    rating: float | None = Field(
        description="Average review score out of 5, or null when the product has no rating yet."
    )
    review_count: int = Field(alias="reviewCount")
    seller_id: str | None = Field(
        default=None,
        alias="sellerId",
        description="TikTok Shop seller id, for joining to the seller's other products. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    sold_count: int = Field(alias="soldCount")
    title: str = Field(
        description="Populated whenever the provider has data for the entity."
    )
    url: str = Field(
        description="Populated whenever the provider has data for the entity."
    )


class TiktokShopUserShowcaseData(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    next_cursor: str | None = Field(
        alias="nextCursor",
        description="Opaque cursor for the next page of products, or null when this lane has no more. Pass it back as cursor to continue.",
    )
    products: list[TiktokShopUserShowcaseProduct] = Field(
        description="Populated whenever the provider has data for the entity."
    )


class TiktokShopUserShowcaseProduct(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    currency: str
    discount_pct: float | None = Field(
        default=None,
        alias="discountPct",
        description="Discount off the original price as a percentage, e.g. 10 for 10% off. Omitted when the product is not discounted.",
    )
    image_url: str = Field(
        alias="imageUrl",
        description="Populated whenever the provider has data for the entity.",
    )
    original_price: str | None = Field(
        alias="originalPrice",
        description="Pre-discount list price, or null when the product is not on sale.",
    )
    price: str
    product_id: str = Field(
        alias="productId",
        description="Populated whenever the provider has data for the entity.",
    )
    rating: float | None = Field(
        description="Average review score out of 5, or null when the product has no rating yet."
    )
    review_count: int = Field(alias="reviewCount")
    seller_id: str | None = Field(
        default=None,
        alias="sellerId",
        description="Identifier of the seller listing the product.",
    )
    sold_count: int = Field(alias="soldCount")
    title: str = Field(
        description="Populated whenever the provider has data for the entity."
    )
    url: str = Field(
        description="Populated whenever the provider has data for the entity."
    )


class TiktokShopNamespace:
    """Typed methods for this platform. Attached lazily to the client."""

    def __init__(self, client: "AnyAPI") -> None:
        self._client = client

    def categories(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[TiktokShopCategoriesInput],
    ) -> RunResult[TiktokShopCategoriesData]:
        """TikTok Shop Categories

        List the TikTok Shop category tree for a market: top-level categories with
        ids, slugs, and images, each with its child categories.

        Price: $0.0012 per request.

        Example:
            res = client.tiktok_shop.categories(region="US")
        """
        raw = self._client._run_raw(  # pyright: ignore[reportPrivateUsage]
            "tiktok_shop.categories", dict(input), options
        )
        return RunResult[TiktokShopCategoriesData].model_validate(raw)

    def creator(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[TiktokShopCreatorInput],
    ) -> RunResult[TiktokShopCreatorData]:
        """TikTok Shop Creator

        TikTok Shop creator performance by handle: GMV range, promoted product
        count, brand collaborations, follower age/gender/location demographics,
        category GMV split, and video versus live engagement.

        Price: $0.0055 per request plus $0 per result (maximum $0.0055).

        Example:
            res = client.tiktok_shop.creator(handle="golinutrition")
        """
        raw = self._client._run_raw(  # pyright: ignore[reportPrivateUsage]
            "tiktok_shop.creator", dict(input), options
        )
        return RunResult[TiktokShopCreatorData].model_validate(raw)

    def product(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[TiktokShopProductInput],
    ) -> RunResult[TiktokShopProductData]:
        """TikTok Shop Product

        Fetch TikTok Shop product details (title, price, sales, seller, and ratings)
        from a product URL.

        Price: $0.00095 per request.

        Example:
            res = client.tiktok_shop.product(url="https://www.tiktok.com/shop/pdp/goli-ashwagandha-gummies-with-vitamin-d-ksm-66-vegan-non-gmo/1729587769570529799")
        """
        raw = self._client._run_raw(  # pyright: ignore[reportPrivateUsage]
            "tiktok_shop.product", dict(input), options
        )
        return RunResult[TiktokShopProductData].model_validate(raw)

    def product_reviews(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[TiktokShopProductReviewsInput],
    ) -> RunResult[TiktokShopProductReviewsData]:
        """TikTok Shop Product Reviews

        Fetch customer reviews for a TikTok Shop product by URL (rating, text,
        reviewer, country, and verified-purchase flag).

        Price: $0.00095 per request.

        Example:
            res = client.tiktok_shop.product_reviews(url="https://www.tiktok.com/shop/pdp/cat-nail-clipper-by-potaroma-adjustable-sizes-built-in-file-safe-for-kittens-cats/1731578642912612516")
        """
        raw = self._client._run_raw(  # pyright: ignore[reportPrivateUsage]
            "tiktok_shop.product_reviews", dict(input), options
        )
        return RunResult[TiktokShopProductReviewsData].model_validate(raw)

    def search(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[TiktokShopSearchInput],
    ) -> RunResult[TiktokShopSearchData]:
        """TikTok Shop Search

        Search TikTok Shop products by keyword across 15 countries: price, sales,
        rating, and seller info per product, in one normalized response.

        Price: $0.00095 per request.

        Example:
            res = client.tiktok_shop.search(limit=3, query="phone case")
        """
        raw = self._client._run_raw(  # pyright: ignore[reportPrivateUsage]
            "tiktok_shop.search", dict(input), options
        )
        return RunResult[TiktokShopSearchData].model_validate(raw)

    def search_suggestions(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[TiktokShopSearchSuggestionsInput],
    ) -> RunResult[TiktokShopSearchSuggestionsData]:
        """TikTok Shop Search Suggestions

        Get TikTok Shop search autocomplete terms for a keyword: the long-tail
        queries shoppers actually type, for keyword and demand research.

        Price: $0.00095 per request.

        Example:
            res = client.tiktok_shop.search_suggestions(country="US", query="ashwagandha gummies")
        """
        raw = self._client._run_raw(  # pyright: ignore[reportPrivateUsage]
            "tiktok_shop.search_suggestions", dict(input), options
        )
        return RunResult[TiktokShopSearchSuggestionsData].model_validate(raw)

    def shop_products(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[TiktokShopShopProductsInput],
    ) -> RunResult[TiktokShopShopProductsData]:
        """TikTok Shop Store Products

        List every product of a TikTok Shop store by URL (title, price, sales, and
        rating per product plus shop-level stats) with cursor pagination.

        Price: $0.0012 per request.

        Example:
            res = client.tiktok_shop.shop_products(url="https://www.tiktok.com/shop/store/goli-nutrition/7495794203056835079")
        """
        raw = self._client._run_raw(  # pyright: ignore[reportPrivateUsage]
            "tiktok_shop.shop_products", dict(input), options
        )
        return RunResult[TiktokShopShopProductsData].model_validate(raw)

    def iter_shop_products(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[TiktokShopShopProductsInput],
    ) -> Paginator[TiktokShopShopProductsProduct, TiktokShopShopProductsData]:
        """Iterate TikTok Shop Store Products results, following pagination cursors.

        Yields validated `TiktokShopShopProductsProduct` items from the `products` field of
        each page. Use `.pages()` on the returned paginator to walk whole
        `RunResult` pages.
        """
        return paginate(
            self._client,
            "tiktok_shop.shop_products",
            dict(input),
            "products",
            item_model=TiktokShopShopProductsProduct,
            data_model=TiktokShopShopProductsData,
            bare=False,
            options=options,
        )

    def user_showcase(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[TiktokShopUserShowcaseInput],
    ) -> RunResult[TiktokShopUserShowcaseData]:
        """TikTok Shop User Showcase

        List the TikTok Shop products a creator showcases (title, price, rating, and
        sales per product).

        Price: $0.0012 per request.

        Example:
            res = client.tiktok_shop.user_showcase(handle="mrtiktokreviews")
        """
        raw = self._client._run_raw(  # pyright: ignore[reportPrivateUsage]
            "tiktok_shop.user_showcase", dict(input), options
        )
        return RunResult[TiktokShopUserShowcaseData].model_validate(raw)

    def iter_user_showcase(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[TiktokShopUserShowcaseInput],
    ) -> Paginator[TiktokShopUserShowcaseProduct, TiktokShopUserShowcaseData]:
        """Iterate TikTok Shop User Showcase results, following pagination cursors.

        Yields validated `TiktokShopUserShowcaseProduct` items from the `products` field of
        each page. Use `.pages()` on the returned paginator to walk whole
        `RunResult` pages.
        """
        return paginate(
            self._client,
            "tiktok_shop.user_showcase",
            dict(input),
            "products",
            item_model=TiktokShopUserShowcaseProduct,
            data_model=TiktokShopUserShowcaseData,
            bare=False,
            options=options,
        )


class AsyncTiktokShopNamespace:
    """Typed methods for this platform. Attached lazily to the client."""

    def __init__(self, client: "AsyncAnyAPI") -> None:
        self._client = client

    async def categories(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[TiktokShopCategoriesInput],
    ) -> RunResult[TiktokShopCategoriesData]:
        """TikTok Shop Categories

        List the TikTok Shop category tree for a market: top-level categories with
        ids, slugs, and images, each with its child categories.

        Price: $0.0012 per request.

        Example:
            res = client.tiktok_shop.categories(region="US")
        """
        raw = await self._client._arun_raw(  # pyright: ignore[reportPrivateUsage]
            "tiktok_shop.categories", dict(input), options
        )
        return RunResult[TiktokShopCategoriesData].model_validate(raw)

    async def creator(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[TiktokShopCreatorInput],
    ) -> RunResult[TiktokShopCreatorData]:
        """TikTok Shop Creator

        TikTok Shop creator performance by handle: GMV range, promoted product
        count, brand collaborations, follower age/gender/location demographics,
        category GMV split, and video versus live engagement.

        Price: $0.0055 per request plus $0 per result (maximum $0.0055).

        Example:
            res = client.tiktok_shop.creator(handle="golinutrition")
        """
        raw = await self._client._arun_raw(  # pyright: ignore[reportPrivateUsage]
            "tiktok_shop.creator", dict(input), options
        )
        return RunResult[TiktokShopCreatorData].model_validate(raw)

    async def product(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[TiktokShopProductInput],
    ) -> RunResult[TiktokShopProductData]:
        """TikTok Shop Product

        Fetch TikTok Shop product details (title, price, sales, seller, and ratings)
        from a product URL.

        Price: $0.00095 per request.

        Example:
            res = client.tiktok_shop.product(url="https://www.tiktok.com/shop/pdp/goli-ashwagandha-gummies-with-vitamin-d-ksm-66-vegan-non-gmo/1729587769570529799")
        """
        raw = await self._client._arun_raw(  # pyright: ignore[reportPrivateUsage]
            "tiktok_shop.product", dict(input), options
        )
        return RunResult[TiktokShopProductData].model_validate(raw)

    async def product_reviews(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[TiktokShopProductReviewsInput],
    ) -> RunResult[TiktokShopProductReviewsData]:
        """TikTok Shop Product Reviews

        Fetch customer reviews for a TikTok Shop product by URL (rating, text,
        reviewer, country, and verified-purchase flag).

        Price: $0.00095 per request.

        Example:
            res = client.tiktok_shop.product_reviews(url="https://www.tiktok.com/shop/pdp/cat-nail-clipper-by-potaroma-adjustable-sizes-built-in-file-safe-for-kittens-cats/1731578642912612516")
        """
        raw = await self._client._arun_raw(  # pyright: ignore[reportPrivateUsage]
            "tiktok_shop.product_reviews", dict(input), options
        )
        return RunResult[TiktokShopProductReviewsData].model_validate(raw)

    async def search(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[TiktokShopSearchInput],
    ) -> RunResult[TiktokShopSearchData]:
        """TikTok Shop Search

        Search TikTok Shop products by keyword across 15 countries: price, sales,
        rating, and seller info per product, in one normalized response.

        Price: $0.00095 per request.

        Example:
            res = client.tiktok_shop.search(limit=3, query="phone case")
        """
        raw = await self._client._arun_raw(  # pyright: ignore[reportPrivateUsage]
            "tiktok_shop.search", dict(input), options
        )
        return RunResult[TiktokShopSearchData].model_validate(raw)

    async def search_suggestions(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[TiktokShopSearchSuggestionsInput],
    ) -> RunResult[TiktokShopSearchSuggestionsData]:
        """TikTok Shop Search Suggestions

        Get TikTok Shop search autocomplete terms for a keyword: the long-tail
        queries shoppers actually type, for keyword and demand research.

        Price: $0.00095 per request.

        Example:
            res = client.tiktok_shop.search_suggestions(country="US", query="ashwagandha gummies")
        """
        raw = await self._client._arun_raw(  # pyright: ignore[reportPrivateUsage]
            "tiktok_shop.search_suggestions", dict(input), options
        )
        return RunResult[TiktokShopSearchSuggestionsData].model_validate(raw)

    async def shop_products(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[TiktokShopShopProductsInput],
    ) -> RunResult[TiktokShopShopProductsData]:
        """TikTok Shop Store Products

        List every product of a TikTok Shop store by URL (title, price, sales, and
        rating per product plus shop-level stats) with cursor pagination.

        Price: $0.0012 per request.

        Example:
            res = client.tiktok_shop.shop_products(url="https://www.tiktok.com/shop/store/goli-nutrition/7495794203056835079")
        """
        raw = await self._client._arun_raw(  # pyright: ignore[reportPrivateUsage]
            "tiktok_shop.shop_products", dict(input), options
        )
        return RunResult[TiktokShopShopProductsData].model_validate(raw)

    def iter_shop_products(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[TiktokShopShopProductsInput],
    ) -> AsyncPaginator[TiktokShopShopProductsProduct, TiktokShopShopProductsData]:
        """Iterate TikTok Shop Store Products results, following pagination cursors.

        Yields validated `TiktokShopShopProductsProduct` items from the `products` field of
        each page. Use `.pages()` on the returned paginator to walk whole
        `RunResult` pages.
        """
        return apaginate(
            self._client,
            "tiktok_shop.shop_products",
            dict(input),
            "products",
            item_model=TiktokShopShopProductsProduct,
            data_model=TiktokShopShopProductsData,
            bare=False,
            options=options,
        )

    async def user_showcase(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[TiktokShopUserShowcaseInput],
    ) -> RunResult[TiktokShopUserShowcaseData]:
        """TikTok Shop User Showcase

        List the TikTok Shop products a creator showcases (title, price, rating, and
        sales per product).

        Price: $0.0012 per request.

        Example:
            res = client.tiktok_shop.user_showcase(handle="mrtiktokreviews")
        """
        raw = await self._client._arun_raw(  # pyright: ignore[reportPrivateUsage]
            "tiktok_shop.user_showcase", dict(input), options
        )
        return RunResult[TiktokShopUserShowcaseData].model_validate(raw)

    def iter_user_showcase(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[TiktokShopUserShowcaseInput],
    ) -> AsyncPaginator[TiktokShopUserShowcaseProduct, TiktokShopUserShowcaseData]:
        """Iterate TikTok Shop User Showcase results, following pagination cursors.

        Yields validated `TiktokShopUserShowcaseProduct` items from the `products` field of
        each page. Use `.pages()` on the returned paginator to walk whole
        `RunResult` pages.
        """
        return apaginate(
            self._client,
            "tiktok_shop.user_showcase",
            dict(input),
            "products",
            item_model=TiktokShopUserShowcaseProduct,
            data_model=TiktokShopUserShowcaseData,
            bare=False,
            options=options,
        )
