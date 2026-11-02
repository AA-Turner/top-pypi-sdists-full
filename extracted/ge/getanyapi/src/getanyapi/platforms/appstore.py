# Generated - do not edit. Regenerate with: pnpm generate
"""Generated namespace module for the appstore platform."""

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


class AppstoreAppInput(TypedDict, total=False):
    """Input for App Store App Details."""

    allowFallbacks: NotRequired[bool]
    """Optional, default true. When false, only the sources listed in `source` may serve; the request is refused with no charge if none of them can. When true, the listed sources are tried first and any other source may serve after them, at the normal price. Default: true."""
    appId: Required[str]
    """Numeric App Store app ID, the digits at the end of the app's store URL without the 'id' prefix (e.g. 310633997)."""
    country: NotRequired[str]
    """Two-letter App Store storefront country code to read the listing from (e.g. gb); price and currency follow that storefront. Default: us."""
    ignoreSources: NotRequired[list[str]]
    """Optional. Source ids to skip for this request, taken from this endpoint's `lanes[].source.id`. The cheapest remaining source serves and the price is that of the dearest remaining source. An id that does not serve this endpoint, or that is also in `source`, is rejected as invalid input with no charge; skipping every source is rejected the same way."""
    preferLatencyUnderMs: NotRequired[int]
    """Optional; omit it and routing is unchanged, with the cheapest source serving. Prefer sources whose typical response time (median over the trailing 30 days, as published on this endpoint's lane health) is under this many milliseconds; among those, the cheapest serves. This can raise your price: when the cheapest source misses the target, a faster and dearer one serves, and you are quoted and charged its price. If no source is that fast the request is still served, by whichever source offers the best speed for its price - it is never refused for being slow. Sources we have not timed are tried last. This is a preference, not a guarantee: the median describes past requests and is not a ceiling on this one, and it excludes any wait this request itself asks for. On a paginated walk it applies to the first page only: later pages stay with the source that page chose, at the price it was quoted. Minimum: 1."""
    requireFields: NotRequired[
        list[
            Literal[
                "author",
                "bundleId",
                "categories",
                "category",
                "createdUtc",
                "currency",
                "currentVersionRating",
                "currentVersionRatingCount",
                "genres",
                "hasInAppPurchases",
                "languages",
                "minimumOsVersion",
                "moreByDeveloper",
                "privacyTypes",
                "ratingCount",
                "ratingHistogram",
                "releasedUtc",
                "reviewSamples",
                "screenshots",
                "similarApps",
                "sizeBytes",
                "subtitle",
                "supportedDevices",
                "text",
                "website",
            ]
        ]
    ]
    """Optional; omit it and routing is unchanged, with the cheapest source serving. Name the output fields this request must be able to return, for example `ratingCount` or `screenshots`, and it is served only by a source that returns every one of them. Fields you do not name are still returned whenever the serving source has them. This can raise your price: when the cheapest source cannot return a named field, a dearer source serves, and you are quoted and charged its price. A named field can still be absent on an app that genuinely lacks it. Naming a combination that no single source returns together is refused as invalid input, with no charge."""
    source: NotRequired[list[str]]
    """Optional. Source ids to prefer, in order, taken from this endpoint's `lanes[].source.id` in /catalog or /apis. Omit it and the cheapest source serves, with automatic failover. Listed sources are tried first in the order given, then the others, unless `allowFallbacks` is false. A single source with `allowFallbacks` false is served only by that source at its price, quoted and charged exactly, with no failover. The price is that of the dearest source that may serve. An id that does not serve this endpoint is rejected as invalid input with no charge; a listed source that is not serving right now is refused with no charge, so omit `source` to be served by another. On a paginated walk, later pages must include the source that served page one, or omit `source`."""


class AppstoreReviewsInput(TypedDict, total=False):
    """Input for App Store Reviews."""

    allowFallbacks: NotRequired[bool]
    """Optional, default true. When false, only the sources listed in `source` may serve; the request is refused with no charge if none of them can. When true, the listed sources are tried first and any other source may serve after them, at the normal price. Default: true."""
    appId: Required[str]
    """Numeric App Store app ID, the digits at the end of the app's store URL without the 'id' prefix (e.g. 310633997)."""
    country: NotRequired[str]
    """Two-letter App Store storefront country code to read reviews from. Default: us."""
    cursor: NotRequired[str]
    """Opaque pagination cursor from a previous response's nextCursor. Omit for the first page; pass it to fetch the next page of reviews."""
    ignoreSources: NotRequired[list[str]]
    """Optional. Source ids to skip for this request, taken from this endpoint's `lanes[].source.id`. The cheapest remaining source serves and the price is that of the dearest remaining source. An id that does not serve this endpoint, or that is also in `source`, is rejected as invalid input with no charge; skipping every source is rejected the same way."""
    limit: NotRequired[int]
    """Maximum number of results to return (1-100, default 100). Range: 1 to 100."""
    preferLatencyUnderMs: NotRequired[int]
    """Optional; omit it and routing is unchanged, with the cheapest source serving. Prefer sources whose typical response time (median over the trailing 30 days, as published on this endpoint's lane health) is under this many milliseconds; among those, the cheapest serves. This can raise your price: when the cheapest source misses the target, a faster and dearer one serves, and you are quoted and charged its price. If no source is that fast the request is still served, by whichever source offers the best speed for its price - it is never refused for being slow. Sources we have not timed are tried last. This is a preference, not a guarantee: the median describes past requests and is not a ceiling on this one, and it excludes any wait this request itself asks for. On a paginated walk it applies to the first page only: later pages stay with the source that page chose, at the price it was quoted. Minimum: 1."""
    requireFields: NotRequired[
        list[Literal["appId", "helpfulVotes", "nextCursor", "url", "version"]]
    ]
    """Optional; omit it and routing is unchanged, with the cheapest source serving. Name the output fields this request must be able to return, for example `helpfulVotes` or `version`, and it is served only by a source that returns every one of them. Fields you do not name are still returned whenever the serving source has them. This can raise your price: when the cheapest source cannot return a named field, a dearer source serves, and you are quoted and charged its price. A named field can still be absent on a review that genuinely lacks it. Naming a combination that no single source returns together is refused as invalid input, with no charge. On a paginated walk it applies to the first page only; later pages stay with the source that page chose, at the price it was quoted."""
    source: NotRequired[list[str]]
    """Optional. Source ids to prefer, in order, taken from this endpoint's `lanes[].source.id` in /catalog or /apis. Omit it and the cheapest source serves, with automatic failover. Listed sources are tried first in the order given, then the others, unless `allowFallbacks` is false. A single source with `allowFallbacks` false is served only by that source at its price, quoted and charged exactly, with no failover. The price is that of the dearest source that may serve. An id that does not serve this endpoint is rejected as invalid input with no charge; a listed source that is not serving right now is refused with no charge, so omit `source` to be served by another. On a paginated walk, later pages must include the source that served page one, or omit `source`."""


class AppstoreSearchInput(TypedDict, total=False):
    """Input for App Store Search."""

    allowFallbacks: NotRequired[bool]
    """Optional, default true. When false, only the sources listed in `source` may serve; the request is refused with no charge if none of them can. When true, the listed sources are tried first and any other source may serve after them, at the normal price. Default: true."""
    country: NotRequired[str]
    """Two-letter App Store storefront country code to search (e.g. gb); results, prices, and currency follow that storefront. Default: us."""
    ignoreSources: NotRequired[list[str]]
    """Optional. Source ids to skip for this request, taken from this endpoint's `lanes[].source.id`. The cheapest remaining source serves and the price is that of the dearest remaining source. An id that does not serve this endpoint, or that is also in `source`, is rejected as invalid input with no charge; skipping every source is rejected the same way."""
    limit: NotRequired[int]
    """Maximum number of apps to return (1-50, default 20). Range: 1 to 50. Default: 20."""
    preferLatencyUnderMs: NotRequired[int]
    """Optional; omit it and routing is unchanged, with the cheapest source serving. Prefer sources whose typical response time (median over the trailing 30 days, as published on this endpoint's lane health) is under this many milliseconds; among those, the cheapest serves. This can raise your price: when the cheapest source misses the target, a faster and dearer one serves, and you are quoted and charged its price. If no source is that fast the request is still served, by whichever source offers the best speed for its price - it is never refused for being slow. Sources we have not timed are tried last. This is a preference, not a guarantee: the median describes past requests and is not a ceiling on this one, and it excludes any wait this request itself asks for. On a paginated walk it applies to the first page only: later pages stay with the source that page chose, at the price it was quoted. Minimum: 1."""
    query: Required[str]
    """Search keywords, as typed into the App Store search box (e.g. budget tracker)."""
    requireFields: NotRequired[
        list[Literal["bundleId", "screenshots", "sizeBytes", "updatedUtc"]]
    ]
    """Optional; omit it and routing is unchanged, with the cheapest source serving. Name the output fields this request must be able to return, for example `sizeBytes` or `updatedUtc`, and it is served only by a source that returns every one of them. Fields you do not name are still returned whenever the serving source has them. This can raise your price: when the cheapest source cannot return a named field, a dearer source serves, and you are quoted and charged its price. A named field can still be absent on an app that genuinely lacks it. Naming a combination that no single source returns together is refused as invalid input, with no charge."""
    source: NotRequired[list[str]]
    """Optional. Source ids to prefer, in order, taken from this endpoint's `lanes[].source.id` in /catalog or /apis. Omit it and the cheapest source serves, with automatic failover. Listed sources are tried first in the order given, then the others, unless `allowFallbacks` is false. A single source with `allowFallbacks` false is served only by that source at its price, quoted and charged exactly, with no failover. The price is that of the dearest source that may serve. An id that does not serve this endpoint is rejected as invalid input with no charge; a listed source that is not serving right now is refused with no charge, so omit `source` to be served by another. On a paginated walk, later pages must include the source that served page one, or omit `source`."""


class AppstoreAppData(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    app_id: str = Field(
        alias="appId",
        description="Numeric App Store app ID. Populated whenever the provider has data for the entity.",
    )
    bundle_id: str | None = Field(
        default=None,
        alias="bundleId",
        description="The app's bundle identifier (e.g. com.burbn.instagram).",
    )
    category: str | None = Field(
        default=None, description="Primary App Store category (e.g. Photo & Video)."
    )
    content_rating: str | None = Field(
        default=None,
        alias="contentRating",
        description="Age rating as shown on the listing (e.g. 13+). Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    currency: str | None = Field(
        default=None, description="ISO 4217 currency code of the price (e.g. USD)."
    )
    current_version_rating: float | None = Field(
        default=None,
        alias="currentVersionRating",
        description="Average star rating of the current version.",
    )
    current_version_rating_count: int | None = Field(
        default=None,
        alias="currentVersionRatingCount",
        description="Number of star ratings of the current version.",
    )
    description: str | None = Field(
        default=None,
        description="Full app description. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    developer: str | None = Field(
        default=None,
        description="Developer name as listed. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    developer_id: str | None = Field(
        default=None,
        alias="developerId",
        description="Numeric App Store developer ID. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    developer_url: str | None = Field(
        default=None,
        alias="developerUrl",
        description="The developer's App Store page URL. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    genres: list[str] | None = Field(
        default=None, description="All App Store categories the app is listed in."
    )
    has_in_app_purchases: bool | None = Field(
        default=None,
        alias="hasInAppPurchases",
        description="True when the listing offers in-app purchases; null when the source does not say.",
    )
    image: str | None = Field(
        default=None,
        description="App icon image URL. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    languages: list[str] | None = Field(
        default=None,
        description="Two-letter codes of the languages the app supports (e.g. EN).",
    )
    minimum_os_version: str | None = Field(
        default=None,
        alias="minimumOsVersion",
        description="Minimum iOS version required (e.g. 16.3).",
    )
    more_by_developer: list[AppstoreAppMoreByDeveloper] | None = Field(
        default=None,
        alias="moreByDeveloper",
        description="Other apps by the same developer.",
    )
    price: float | None = Field(
        default=None,
        description="Price to download in the storefront's currency; 0 for a free app. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    privacy_types: list[AppstoreAppPrivacyType] | None = Field(
        default=None,
        alias="privacyTypes",
        description="The App Privacy label: each kind of data use the developer declared, with the data categories it covers.",
    )
    rating: float | None = Field(
        default=None,
        description="Average star rating, 0 to 5. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    rating_count: int | None = Field(
        default=None,
        alias="ratingCount",
        description="Number of star ratings the app has in this storefront (ratings, not written reviews).",
    )
    rating_histogram: AppstoreAppRatingHistogram | None = Field(
        default=None,
        alias="ratingHistogram",
        description="Number of ratings at each star level.",
    )
    release_notes: str | None = Field(
        default=None,
        alias="releaseNotes",
        description="What's new in the current version. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    released_utc: float | None = Field(
        default=None,
        alias="releasedUtc",
        description="UTC epoch timestamp in seconds (Unix time). Multiply by 1000 for a JS Date in milliseconds. When the app was first released.",
    )
    review_samples: list[AppstoreAppReviewSample] | None = Field(
        default=None,
        alias="reviewSamples",
        description="A few reviews shown on the listing page; use appstore.reviews for the full list.",
    )
    screenshots: list[str] | None = Field(
        default=None, description="iPhone screenshot image URLs."
    )
    similar_apps: list[AppstoreAppSimilarApp] | None = Field(
        default=None,
        alias="similarApps",
        description="Apps shown under You Might Also Like.",
    )
    size_bytes: int | None = Field(
        default=None, alias="sizeBytes", description="Download size in bytes."
    )
    subtitle: str | None = Field(
        default=None, description="Short subtitle shown under the app name."
    )
    supported_devices: list[str] | None = Field(
        default=None,
        alias="supportedDevices",
        description="Apple device model codes the app runs on.",
    )
    title: str = Field(
        description="App name as listed. Populated whenever the provider has data for the entity."
    )
    updated_utc: float | None = Field(
        default=None,
        alias="updatedUtc",
        description="UTC epoch timestamp in seconds (Unix time). Multiply by 1000 for a JS Date in milliseconds. When the current version was released. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    url: str | None = Field(
        default=None,
        description="App Store page URL for the app in the requested storefront. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    version: str | None = Field(
        default=None,
        description="Current version number (e.g. 451.0.0). Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    website: str | None = Field(
        default=None, description="The seller's own website, when listed."
    )


class AppstoreAppMoreByDeveloper(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    app_id: str = Field(alias="appId", description="Numeric App Store app ID.")
    image: str | None = Field(default=None, description="App icon image URL.")
    title: str | None = Field(default=None, description="App name.")
    url: str | None = Field(default=None, description="App Store page URL.")


class AppstoreAppPrivacyType(BaseModel):
    model_config = ConfigDict(extra="allow")

    categories: list[str] | None = Field(
        default=None, description="Data categories it covers (e.g. Contact Info)."
    )
    title: str = Field(description="Kind of data use (e.g. Data Linked to You).")


class AppstoreAppRatingHistogram(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    five_star: int | None = Field(
        default=None, alias="fiveStar", description="Number of 5-star ratings."
    )
    four_star: int | None = Field(
        default=None, alias="fourStar", description="Number of 4-star ratings."
    )
    one_star: int | None = Field(
        default=None, alias="oneStar", description="Number of 1-star ratings."
    )
    three_star: int | None = Field(
        default=None, alias="threeStar", description="Number of 3-star ratings."
    )
    two_star: int | None = Field(
        default=None, alias="twoStar", description="Number of 2-star ratings."
    )


class AppstoreAppReviewSample(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    author: str | None = Field(default=None, description="Reviewer nickname.")
    created_utc: float | None = Field(
        default=None,
        alias="createdUtc",
        description="UTC epoch timestamp in seconds (Unix time). Multiply by 1000 for a JS Date in milliseconds. When the review was posted.",
    )
    rating: float = Field(description="Star rating, 1 to 5.")
    text: str | None = Field(default=None, description="Review text.")
    title: str | None = Field(default=None, description="Review title.")


class AppstoreAppSimilarApp(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    app_id: str = Field(alias="appId", description="Numeric App Store app ID.")
    image: str | None = Field(default=None, description="App icon image URL.")
    title: str | None = Field(default=None, description="App name.")
    url: str | None = Field(default=None, description="App Store page URL.")


class AppstoreReviewsData(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    items: list[AppstoreReviewsItem] = Field(
        description="Review records: star rating, review title and text, reviewer nickname, app version, and review date. Populated whenever the provider has data for the entity."
    )
    next_cursor: str | None = Field(
        default=None,
        alias="nextCursor",
        description="Opaque cursor for the next page of reviews, or null when there are no more. Pass it back as cursor to continue.",
    )


class AppstoreReviewsItem(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    app_id: str | None = Field(
        default=None,
        alias="appId",
        description="App Store numeric app identifier the review belongs to.",
    )
    author: str | None = Field(
        default=None,
        description="Reviewer nickname. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    created_utc: float | None = Field(
        default=None,
        alias="createdUtc",
        description="UTC epoch timestamp in seconds (Unix time). Multiply by 1000 for a JS Date in milliseconds. When the review was posted. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    helpful_votes: int | None = Field(
        default=None,
        alias="helpfulVotes",
        description="Number of helpful votes on the review.",
    )
    id: str | None = Field(
        default=None,
        description="Review identifier. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    rating: float = Field(
        description="Star rating, 1 to 5. Populated whenever the provider has data for the entity."
    )
    text: str = Field(
        description="Review body text. Populated whenever the provider has data for the entity."
    )
    title: str | None = Field(default=None, description="Review title.")
    url: str | None = Field(
        default=None,
        description="Public App Store page for this review, when supplied by the serving lane.",
    )
    version: str | None = Field(
        default=None, description="App version the review was left on."
    )


class AppstoreSearchData(BaseModel):
    items: list[AppstoreSearchItem] = Field(
        description="Matching apps in App Store search order. Populated whenever the provider has data for the entity."
    )


class AppstoreSearchItem(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    app_id: str = Field(
        alias="appId",
        description="Numeric App Store app ID; pass it to appstore.app for the full listing. Populated whenever the provider has data for the entity.",
    )
    bundle_id: str | None = Field(
        default=None, alias="bundleId", description="The app's bundle identifier."
    )
    content_rating: str | None = Field(
        default=None,
        alias="contentRating",
        description="Age rating (e.g. 4+). Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    currency: str | None = Field(
        default=None, description="ISO 4217 currency code of the price (e.g. USD)."
    )
    description: str | None = Field(
        default=None,
        description="App description. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    developer: str | None = Field(
        default=None,
        description="Developer name. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    developer_id: str | None = Field(
        default=None,
        alias="developerId",
        description="Numeric App Store developer ID. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    genres: list[str] | None = Field(
        default=None,
        description="App Store categories, primary first. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    image: str | None = Field(
        default=None,
        description="App icon image URL. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    languages: list[str] | None = Field(
        default=None,
        description="Two-letter codes of the languages the app supports. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    minimum_os_version: str | None = Field(
        default=None,
        alias="minimumOsVersion",
        description="Minimum iOS version required. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    price: float = Field(
        description="Price to download in the storefront's currency; 0 for a free app."
    )
    rating: float | None = Field(
        default=None,
        description="Average star rating, 0 to 5. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    rating_count: int | None = Field(
        default=None,
        alias="ratingCount",
        description="Number of star ratings (ratings, not written reviews). Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    released_utc: float | None = Field(
        default=None,
        alias="releasedUtc",
        description="UTC epoch timestamp in seconds (Unix time). Multiply by 1000 for a JS Date in milliseconds. When the app was first released. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    screenshots: list[str] | None = Field(
        default=None, description="iPhone screenshot image URLs."
    )
    size_bytes: int | None = Field(
        default=None, alias="sizeBytes", description="Download size in bytes."
    )
    title: str = Field(
        description="App name. Populated whenever the provider has data for the entity."
    )
    updated_utc: float | None = Field(
        default=None,
        alias="updatedUtc",
        description="UTC epoch timestamp in seconds (Unix time). Multiply by 1000 for a JS Date in milliseconds. When the current version was released.",
    )
    url: str | None = Field(
        default=None,
        description="App Store page URL. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    version: str | None = Field(
        default=None,
        description="Current version number. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )


class AppstoreNamespace:
    """Typed methods for this platform. Attached lazily to the client."""

    def __init__(self, client: "AnyAPI") -> None:
        self._client = client

    def app(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[AppstoreAppInput],
    ) -> RunResult[AppstoreAppData]:
        """App Store App Details

        Get an iOS app's App Store listing by app ID, in any storefront country:
        title, developer, rating, price, version, description, screenshots, and
        more.

        Price: $0.00085 per request.

        Example:
            res = client.appstore.app(appId="479516143", country="us")
        """
        raw = self._client._run_raw(  # pyright: ignore[reportPrivateUsage]
            "appstore.app", dict(input), options
        )
        return RunResult[AppstoreAppData].model_validate(raw)

    def reviews(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[AppstoreReviewsInput],
    ) -> RunResult[AppstoreReviewsData]:
        """App Store Reviews

        Get App Store reviews for any iOS app by app ID, in any storefront country:
        ratings, titles, and review text.

        Price: $0.0009 per request.

        Example:
            res = client.appstore.reviews(appId="389801252", country="us", limit=3)
        """
        raw = self._client._run_raw(  # pyright: ignore[reportPrivateUsage]
            "appstore.reviews", dict(input), options
        )
        return RunResult[AppstoreReviewsData].model_validate(raw)

    def iter_reviews(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[AppstoreReviewsInput],
    ) -> Paginator[AppstoreReviewsItem, AppstoreReviewsData]:
        """Iterate App Store Reviews results, following pagination cursors.

        Yields validated `AppstoreReviewsItem` items from the `items` field of
        each page. Use `.pages()` on the returned paginator to walk whole
        `RunResult` pages.
        """
        return paginate(
            self._client,
            "appstore.reviews",
            dict(input),
            "items",
            item_model=AppstoreReviewsItem,
            data_model=AppstoreReviewsData,
            bare=False,
            options=options,
        )

    def search(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[AppstoreSearchInput],
    ) -> RunResult[AppstoreSearchData]:
        """App Store Search

        Search the App Store for iOS apps by keyword, in any storefront country: app
        ID, title, developer, rating, ratings count, price, version, and more for
        each result.

        Price: $0.00085 per request.

        Example:
            res = client.appstore.search(country="us", limit=10, query="minecraft")
        """
        raw = self._client._run_raw(  # pyright: ignore[reportPrivateUsage]
            "appstore.search", dict(input), options
        )
        return RunResult[AppstoreSearchData].model_validate(raw)


class AsyncAppstoreNamespace:
    """Typed methods for this platform. Attached lazily to the client."""

    def __init__(self, client: "AsyncAnyAPI") -> None:
        self._client = client

    async def app(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[AppstoreAppInput],
    ) -> RunResult[AppstoreAppData]:
        """App Store App Details

        Get an iOS app's App Store listing by app ID, in any storefront country:
        title, developer, rating, price, version, description, screenshots, and
        more.

        Price: $0.00085 per request.

        Example:
            res = client.appstore.app(appId="479516143", country="us")
        """
        raw = await self._client._arun_raw(  # pyright: ignore[reportPrivateUsage]
            "appstore.app", dict(input), options
        )
        return RunResult[AppstoreAppData].model_validate(raw)

    async def reviews(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[AppstoreReviewsInput],
    ) -> RunResult[AppstoreReviewsData]:
        """App Store Reviews

        Get App Store reviews for any iOS app by app ID, in any storefront country:
        ratings, titles, and review text.

        Price: $0.0009 per request.

        Example:
            res = client.appstore.reviews(appId="389801252", country="us", limit=3)
        """
        raw = await self._client._arun_raw(  # pyright: ignore[reportPrivateUsage]
            "appstore.reviews", dict(input), options
        )
        return RunResult[AppstoreReviewsData].model_validate(raw)

    def iter_reviews(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[AppstoreReviewsInput],
    ) -> AsyncPaginator[AppstoreReviewsItem, AppstoreReviewsData]:
        """Iterate App Store Reviews results, following pagination cursors.

        Yields validated `AppstoreReviewsItem` items from the `items` field of
        each page. Use `.pages()` on the returned paginator to walk whole
        `RunResult` pages.
        """
        return apaginate(
            self._client,
            "appstore.reviews",
            dict(input),
            "items",
            item_model=AppstoreReviewsItem,
            data_model=AppstoreReviewsData,
            bare=False,
            options=options,
        )

    async def search(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[AppstoreSearchInput],
    ) -> RunResult[AppstoreSearchData]:
        """App Store Search

        Search the App Store for iOS apps by keyword, in any storefront country: app
        ID, title, developer, rating, ratings count, price, version, and more for
        each result.

        Price: $0.00085 per request.

        Example:
            res = client.appstore.search(country="us", limit=10, query="minecraft")
        """
        raw = await self._client._arun_raw(  # pyright: ignore[reportPrivateUsage]
            "appstore.search", dict(input), options
        )
        return RunResult[AppstoreSearchData].model_validate(raw)
