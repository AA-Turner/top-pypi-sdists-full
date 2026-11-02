# Generated - do not edit. Regenerate with: pnpm generate
"""Generated namespace module for the playstore platform."""

from __future__ import annotations

from typing import Literal, TYPE_CHECKING

from pydantic import BaseModel, ConfigDict, Field
from typing_extensions import NotRequired, Required, TypedDict, Unpack

from ..types import RequestOptions, RunResult

if TYPE_CHECKING:
    from .._async_client import AsyncAnyAPI
    from .._client import AnyAPI


class PlaystoreAppInput(TypedDict, total=False):
    """Input for Google Play App Details."""

    allowFallbacks: NotRequired[bool]
    """Optional, default true. When false, only the sources listed in `source` may serve; the request is refused with no charge if none of them can. When true, the listed sources are tried first and any other source may serve after them, at the normal price. Default: true."""
    appId: Required[str]
    """Android app package name, the id parameter of the app's Google Play URL (e.g. com.supercell.brawlstars)."""
    country: NotRequired[str]
    """Two-letter Google Play store country code to read the listing from (e.g. gb); price and currency follow that country. Text is returned in English. Default: us."""
    ignoreSources: NotRequired[list[str]]
    """Optional. Source ids to skip for this request, taken from this endpoint's `lanes[].source.id`. The cheapest remaining source serves and the price is that of the dearest remaining source. An id that does not serve this endpoint, or that is also in `source`, is rejected as invalid input with no charge; skipping every source is rejected the same way."""
    preferLatencyUnderMs: NotRequired[int]
    """Optional; omit it and routing is unchanged, with the cheapest source serving. Prefer sources whose typical response time (median over the trailing 30 days, as published on this endpoint's lane health) is under this many milliseconds; among those, the cheapest serves. This can raise your price: when the cheapest source misses the target, a faster and dearer one serves, and you are quoted and charged its price. If no source is that fast the request is still served, by whichever source offers the best speed for its price - it is never refused for being slow. Sources we have not timed are tried last. This is a preference, not a guarantee: the median describes past requests and is not a ceiling on this one, and it excludes any wait this request itself asks for. On a paginated walk it applies to the first page only: later pages stay with the source that page chose, at the price it was quoted. Minimum: 1."""
    requireFields: NotRequired[
        list[
            Literal[
                "author",
                "containsAds",
                "createdUtc",
                "dataSafety",
                "developerAddress",
                "developerEmail",
                "developerId",
                "developerPhone",
                "editorsChoice",
                "group",
                "headerImage",
                "helpfulVotes",
                "id",
                "installCount",
                "minAndroidVersion",
                "moreByDeveloper",
                "permissions",
                "ratingHistogram",
                "recentChanges",
                "reviewCount",
                "reviewSamples",
                "similarApps",
                "text",
                "version",
            ]
        ]
    ]
    """Optional; omit it and routing is unchanged, with the cheapest source serving. Name the output fields this request must be able to return, for example `reviewCount` or `developerEmail`, and it is served only by a source that returns every one of them. Fields you do not name are still returned whenever the serving source has them. This can raise your price: when the cheapest source cannot return a named field, a dearer source serves, and you are quoted and charged its price. A named field can still be absent on an app that genuinely lacks it. Naming a combination that no single source returns together is refused as invalid input, with no charge."""
    source: NotRequired[list[str]]
    """Optional. Source ids to prefer, in order, taken from this endpoint's `lanes[].source.id` in /catalog or /apis. Omit it and the cheapest source serves, with automatic failover. Listed sources are tried first in the order given, then the others, unless `allowFallbacks` is false. A single source with `allowFallbacks` false is served only by that source at its price, quoted and charged exactly, with no failover. The price is that of the dearest source that may serve. An id that does not serve this endpoint is rejected as invalid input with no charge; a listed source that is not serving right now is refused with no charge, so omit `source` to be served by another. On a paginated walk, later pages must include the source that served page one, or omit `source`."""


class PlaystoreReviewsInput(TypedDict, total=False):
    """Input for Google Play Reviews."""

    allowFallbacks: NotRequired[bool]
    """Optional, default true. When false, only the sources listed in `source` may serve; the request is refused with no charge if none of them can. When true, the listed sources are tried first and any other source may serve after them, at the normal price. Default: true."""
    appId: Required[str]
    """Android app package name or full Google Play store URL (e.g. com.supercell.brawlstars)."""
    appVersion: NotRequired[list[str]]
    """Only return reviews left on these app versions (e.g. ["2.24.1", "2.24.2"])."""
    deviceType: NotRequired[Literal["mobile", "tablet", "chromebook"]]
    """Only return reviews from this device type (e.g. "tablet"); omit for the provider default."""
    endDate: NotRequired[str]
    """Only return reviews on or before this date, inclusive, in YYYY-MM-DD format (e.g. 2026-06-30)."""
    ignoreSources: NotRequired[list[str]]
    """Optional. Source ids to skip for this request, taken from this endpoint's `lanes[].source.id`. The cheapest remaining source serves and the price is that of the dearest remaining source. An id that does not serve this endpoint, or that is also in `source`, is rejected as invalid input with no charge; skipping every source is rejected the same way."""
    keywords: NotRequired[list[str]]
    """Only return reviews whose text contains one of these keywords (e.g. ["crash", "login"])."""
    languages: NotRequired[list[str]]
    """Only return reviews in these ISO 639-1 languages (e.g. ["en", "es"])."""
    limit: NotRequired[int]
    """Maximum number of results to return (1-100, default 100). Range: 1 to 100."""
    preferLatencyUnderMs: NotRequired[int]
    """Optional; omit it and routing is unchanged, with the cheapest source serving. Prefer sources whose typical response time (median over the trailing 30 days, as published on this endpoint's lane health) is under this many milliseconds; among those, the cheapest serves. This can raise your price: when the cheapest source misses the target, a faster and dearer one serves, and you are quoted and charged its price. If no source is that fast the request is still served, by whichever source offers the best speed for its price - it is never refused for being slow. Sources we have not timed are tried last. This is a preference, not a guarantee: the median describes past requests and is not a ceiling on this one, and it excludes any wait this request itself asks for. On a paginated walk it applies to the first page only: later pages stay with the source that page chose, at the price it was quoted. Minimum: 1."""
    rating: NotRequired[int]
    """Only return reviews with this exact star rating from 1 to 5 (e.g. 1); omit for all ratings."""
    recentDays: NotRequired[int]
    """Only return reviews from the last N days (e.g. 30); omit for no time limit. Minimum: 1."""
    requireFields: NotRequired[list[Literal["appId", "title"]]]
    """Optional; omit it and routing is unchanged, with the cheapest source serving. Name the output fields this request must be able to return, for example `title` or `appId`, and it is served only by a source that returns every one of them. Fields you do not name are still returned whenever the serving source has them. This can raise your price: when the cheapest source cannot return a named field, a dearer source serves, and you are quoted and charged its price. A named field can still be absent on a review that genuinely lacks it. Naming a combination that no single source returns together is refused as invalid input, with no charge."""
    sortBy: NotRequired[str]
    """Review ordering: mostRelevant, newest, or rating (e.g. newest)."""
    source: NotRequired[list[str]]
    """Optional. Source ids to prefer, in order, taken from this endpoint's `lanes[].source.id` in /catalog or /apis. Omit it and the cheapest source serves, with automatic failover. Listed sources are tried first in the order given, then the others, unless `allowFallbacks` is false. A single source with `allowFallbacks` false is served only by that source at its price, quoted and charged exactly, with no failover. The price is that of the dearest source that may serve. An id that does not serve this endpoint is rejected as invalid input with no charge; a listed source that is not serving right now is refused with no charge, so omit `source` to be served by another. On a paginated walk, later pages must include the source that served page one, or omit `source`."""


class PlaystoreSearchInput(TypedDict, total=False):
    """Input for Google Play Search."""

    allowFallbacks: NotRequired[bool]
    """Optional, default true. When false, only the sources listed in `source` may serve; the request is refused with no charge if none of them can. When true, the listed sources are tried first and any other source may serve after them, at the normal price. Default: true."""
    country: NotRequired[str]
    """Two-letter Google Play store country code to search (e.g. gb); results, prices, and currency follow that country. Text is returned in English. Default: us."""
    ignoreSources: NotRequired[list[str]]
    """Optional. Source ids to skip for this request, taken from this endpoint's `lanes[].source.id`. The cheapest remaining source serves and the price is that of the dearest remaining source. An id that does not serve this endpoint, or that is also in `source`, is rejected as invalid input with no charge; skipping every source is rejected the same way."""
    limit: NotRequired[int]
    """Maximum number of apps to return in items (1-30, default 20). Google Play shows about 30 apps per search, so fewer may come back. The app Google Play features above the results comes back separately in featuredApps and does not count toward this limit. Range: 1 to 30. Default: 20."""
    preferLatencyUnderMs: NotRequired[int]
    """Optional; omit it and routing is unchanged, with the cheapest source serving. Prefer sources whose typical response time (median over the trailing 30 days, as published on this endpoint's lane health) is under this many milliseconds; among those, the cheapest serves. This can raise your price: when the cheapest source misses the target, a faster and dearer one serves, and you are quoted and charged its price. If no source is that fast the request is still served, by whichever source offers the best speed for its price - it is never refused for being slow. Sources we have not timed are tried last. This is a preference, not a guarantee: the median describes past requests and is not a ceiling on this one, and it excludes any wait this request itself asks for. On a paginated walk it applies to the first page only: later pages stay with the source that page chose, at the price it was quoted. Minimum: 1."""
    query: Required[str]
    """Search keywords, as typed into the Google Play search box (e.g. budget tracker)."""
    source: NotRequired[list[str]]
    """Optional. Source ids to prefer, in order, taken from this endpoint's `lanes[].source.id` in /catalog or /apis. Omit it and the cheapest source serves, with automatic failover. Listed sources are tried first in the order given, then the others, unless `allowFallbacks` is false. A single source with `allowFallbacks` false is served only by that source at its price, quoted and charged exactly, with no failover. The price is that of the dearest source that may serve. An id that does not serve this endpoint is rejected as invalid input with no charge; a listed source that is not serving right now is refused with no charge, so omit `source` to be served by another. On a paginated walk, later pages must include the source that served page one, or omit `source`."""


class PlaystoreAppData(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    app_id: str = Field(
        alias="appId",
        description="Android package name. Populated whenever the provider has data for the entity.",
    )
    category: str | None = Field(
        default=None,
        description="Google Play category name (e.g. Music & Audio). Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    category_id: str | None = Field(
        default=None,
        alias="categoryId",
        description="Google Play category ID (e.g. MUSIC_AND_AUDIO). Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    contains_ads: bool | None = Field(
        default=None,
        alias="containsAds",
        description="True when the listing says the app contains ads.",
    )
    content_rating: str | None = Field(
        default=None,
        alias="contentRating",
        description="Content rating as shown (e.g. Teen). Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    currency: str | None = Field(
        default=None, description="ISO 4217 currency code of the price (e.g. USD)."
    )
    data_safety: list[PlaystoreAppDataSafety] | None = Field(
        default=None,
        alias="dataSafety",
        description="The Data safety section: what the developer says the app shares and collects.",
    )
    description: str | None = Field(
        default=None,
        description="Full app description as plain text. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    developer: str | None = Field(
        default=None,
        description="Developer name as listed. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    developer_address: str | None = Field(
        default=None, alias="developerAddress", description="Developer postal address."
    )
    developer_email: str | None = Field(
        default=None,
        alias="developerEmail",
        description="Developer support email address.",
    )
    developer_id: str | None = Field(
        default=None, alias="developerId", description="Google Play developer ID."
    )
    developer_phone: str | None = Field(
        default=None, alias="developerPhone", description="Developer phone number."
    )
    developer_website: str | None = Field(
        default=None, alias="developerWebsite", description="Developer website URL."
    )
    editors_choice: bool | None = Field(
        default=None,
        alias="editorsChoice",
        description="True when the app carries the Editors' Choice badge.",
    )
    header_image: str | None = Field(
        default=None, alias="headerImage", description="Feature graphic image URL."
    )
    image: str | None = Field(
        default=None,
        description="App icon image URL. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    in_app_purchase_range: str | None = Field(
        default=None,
        alias="inAppPurchaseRange",
        description="Price range of in-app purchases as shown (e.g. $4.99 - $203.88 per item); null when the app has none.",
    )
    install_count: int | None = Field(
        default=None,
        alias="installCount",
        description="Install count Google Play holds behind the bracket.",
    )
    installs: str | None = Field(
        default=None,
        description="Install count bracket as Google Play shows it (e.g. 1,000,000,000+). Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    min_android_version: str | None = Field(
        default=None,
        alias="minAndroidVersion",
        description="Minimum Android version required; null when it varies with device.",
    )
    min_installs: int | None = Field(
        default=None,
        alias="minInstalls",
        description="Lower bound of the install bracket (e.g. 1000000000). Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    more_by_developer: list[PlaystoreAppMoreByDeveloper] | None = Field(
        default=None,
        alias="moreByDeveloper",
        description="Other apps by the same developer, from the listing's More by section.",
    )
    permissions: list[PlaystoreAppPermission] | None = Field(
        default=None, description="Android permissions the app requests, grouped."
    )
    price: float | None = Field(
        default=None,
        description="Price to install in the country's currency; 0 for a free app. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    privacy_policy_url: str | None = Field(
        default=None, alias="privacyPolicyUrl", description="Privacy policy URL."
    )
    rating: float | None = Field(
        default=None,
        description="Average star rating, 0 to 5. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    rating_count: int | None = Field(
        default=None,
        alias="ratingCount",
        description="Number of star ratings the app has (ratings, not written reviews). Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    rating_histogram: PlaystoreAppRatingHistogram | None = Field(
        default=None,
        alias="ratingHistogram",
        description="Number of ratings at each star level.",
    )
    recent_changes: str | None = Field(
        default=None,
        alias="recentChanges",
        description="What's new in the latest update.",
    )
    released_utc: float | None = Field(
        default=None,
        alias="releasedUtc",
        description="UTC epoch timestamp in seconds (Unix time). Multiply by 1000 for a JS Date in milliseconds. When the app was first released. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    review_count: int | None = Field(
        default=None,
        alias="reviewCount",
        description="Number of written reviews, a subset of the ratings.",
    )
    review_samples: list[PlaystoreAppReviewSample] | None = Field(
        default=None,
        alias="reviewSamples",
        description="A few reviews shown on the listing page; use playstore.reviews for the full list.",
    )
    screenshots: list[str] | None = Field(
        default=None,
        description="Screenshot image URLs. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    similar_apps: list[PlaystoreAppSimilarApp] | None = Field(
        default=None,
        alias="similarApps",
        description="Apps from the listing's Similar apps (or Similar games) section.",
    )
    summary: str | None = Field(
        default=None, description="Short description shown under the app name."
    )
    title: str = Field(
        description="App name as listed. Populated whenever the provider has data for the entity."
    )
    updated_utc: float | None = Field(
        default=None,
        alias="updatedUtc",
        description="UTC epoch timestamp in seconds (Unix time). Multiply by 1000 for a JS Date in milliseconds. When the app was last updated. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    url: str | None = Field(
        default=None,
        description="Google Play page URL for the app. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    version: str | None = Field(
        default=None,
        description="Current version number; null when the listing says it varies with device.",
    )


class PlaystoreAppDataSafety(BaseModel):
    model_config = ConfigDict(extra="allow")

    description: str | None = Field(default=None, description="Data types it covers.")
    title: str = Field(
        description="Statement (e.g. This app may collect these data types)."
    )


class PlaystoreAppMoreByDeveloper(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    app_id: str = Field(alias="appId", description="Android package name.")
    developer: str | None = Field(default=None, description="Developer name.")
    image: str | None = Field(default=None, description="App icon image URL.")
    rating: float | None = Field(
        default=None, description="Average star rating, 0 to 5."
    )
    title: str | None = Field(default=None, description="App name.")
    url: str | None = Field(default=None, description="Google Play page URL.")


class PlaystoreAppPermission(BaseModel):
    model_config = ConfigDict(extra="allow")

    group: str = Field(description="Permission group (e.g. Location).")
    permissions: list[str] | None = Field(
        default=None, description="Individual permissions in the group."
    )


class PlaystoreAppRatingHistogram(BaseModel):
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


class PlaystoreAppReviewSample(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    author: str | None = Field(default=None, description="Reviewer name.")
    created_utc: float | None = Field(
        default=None,
        alias="createdUtc",
        description="UTC epoch timestamp in seconds (Unix time). Multiply by 1000 for a JS Date in milliseconds. When the review was posted.",
    )
    helpful_votes: int | None = Field(
        default=None,
        alias="helpfulVotes",
        description="Number of people who found the review helpful.",
    )
    id: str | None = Field(default=None, description="Review identifier.")
    rating: float = Field(description="Star rating, 1 to 5.")
    text: str | None = Field(default=None, description="Review text.")
    version: str | None = Field(
        default=None, description="App version the review was left on."
    )


class PlaystoreAppSimilarApp(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    app_id: str = Field(alias="appId", description="Android package name.")
    developer: str | None = Field(default=None, description="Developer name.")
    image: str | None = Field(default=None, description="App icon image URL.")
    rating: float | None = Field(
        default=None, description="Average star rating, 0 to 5."
    )
    title: str | None = Field(default=None, description="App name.")
    url: str | None = Field(default=None, description="Google Play page URL.")


class PlaystoreReviewsData(BaseModel):
    items: list[PlaystoreReviewsItem] = Field(
        description="Review records: star rating, review text, reviewer name, app version, helpfulness votes, and review date. Populated whenever the provider has data for the entity."
    )


class PlaystoreReviewsItem(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    app_id: str | None = Field(
        default=None,
        alias="appId",
        description="Google Play package name the review belongs to.",
    )
    author: str | None = Field(
        default=None,
        description="Reviewer display name. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    author_avatar_url: str | None = Field(
        default=None, alias="authorAvatarUrl", description="Reviewer profile photo URL."
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
    title: str | None = Field(
        default=None, description="Review title, when the store provides one."
    )
    version: str | None = Field(
        default=None, description="App version the review was left on."
    )


class PlaystoreSearchData(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    featured_apps: list[PlaystoreSearchFeaturedApp] | None = Field(
        default=None,
        alias="featuredApps",
        description="The app Google Play features above the results, usually the exact app the query names (e.g. Minecraft for minecraft); empty when the search shows none.",
    )
    items: list[PlaystoreSearchItem] = Field(
        description="Matching apps in Google Play search order, including the Similar apps shelf Google Play shows under a search for one app. Populated whenever the provider has data for the entity."
    )


class PlaystoreSearchFeaturedApp(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    app_id: str = Field(alias="appId", description="Android package name.")
    currency: str | None = Field(
        default=None, description="ISO 4217 currency code of the price."
    )
    description: str | None = Field(default=None, description="Short app description.")
    developer: str | None = Field(default=None, description="Developer name.")
    image: str | None = Field(default=None, description="App icon image URL.")
    installs: str | None = Field(
        default=None,
        description="Install bracket as the featured card shows it (e.g. 50M+).",
    )
    price: float | None = Field(
        default=None,
        description="Price to install in the country's currency; 0 for a free app.",
    )
    rating: float | None = Field(
        default=None, description="Average star rating, 0 to 5."
    )
    rating_count: int | None = Field(
        default=None,
        alias="ratingCount",
        description="Number of star ratings (ratings, not written reviews).",
    )
    title: str = Field(description="App name.")
    url: str | None = Field(default=None, description="Google Play page URL.")


class PlaystoreSearchItem(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    app_id: str = Field(
        alias="appId",
        description="Android package name; pass it to playstore.app for the full listing. Populated whenever the provider has data for the entity.",
    )
    category: str | None = Field(
        default=None,
        description="Google Play category name. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    currency: str | None = Field(
        default=None, description="ISO 4217 currency code of the price (e.g. USD)."
    )
    description: str | None = Field(default=None, description="App description.")
    developer: str | None = Field(
        default=None,
        description="Developer name. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    image: str | None = Field(
        default=None,
        description="App icon image URL. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    installs: str | None = Field(
        default=None,
        description="Install count bracket as Google Play shows it (e.g. 1,000,000+). Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    price: float = Field(
        description="Price to install in the country's currency; 0 for a free app."
    )
    rating: float | None = Field(
        default=None,
        description="Average star rating, 0 to 5; absent for an app with too few ratings. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    screenshots: list[str] | None = Field(
        default=None, description="Screenshot image URLs."
    )
    title: str = Field(
        description="App name. Populated whenever the provider has data for the entity."
    )
    url: str | None = Field(
        default=None,
        description="Google Play page URL. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )


class PlaystoreNamespace:
    """Typed methods for this platform. Attached lazily to the client."""

    def __init__(self, client: "AnyAPI") -> None:
        self._client = client

    def app(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[PlaystoreAppInput],
    ) -> RunResult[PlaystoreAppData]:
        """Google Play App Details

        Get an Android app's Google Play listing by package name, in any store
        country: title, developer and contact details, rating, ratings count,
        installs, price, description, screenshots, and more.

        Price: $0.00085 per request.

        Example:
            res = client.playstore.app(appId="com.playdigious.deadcells.mobile", country="us")
        """
        raw = self._client._run_raw(  # pyright: ignore[reportPrivateUsage]
            "playstore.app", dict(input), options
        )
        return RunResult[PlaystoreAppData].model_validate(raw)

    def reviews(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[PlaystoreReviewsInput],
    ) -> RunResult[PlaystoreReviewsData]:
        """Google Play Reviews

        Fetch Google Play reviews for any Android app by package name or store URL:
        ratings, review text, dates, and helpfulness votes.

        Price: $0.0009 per request.

        Example:
            res = client.playstore.reviews(appId="com.whatsapp", limit=3)
        """
        raw = self._client._run_raw(  # pyright: ignore[reportPrivateUsage]
            "playstore.reviews", dict(input), options
        )
        return RunResult[PlaystoreReviewsData].model_validate(raw)

    def search(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[PlaystoreSearchInput],
    ) -> RunResult[PlaystoreSearchData]:
        """Google Play Search

        Search Google Play for Android apps by keyword, in any store country:
        package name, title, developer, rating, installs, price, and category for
        each result.

        Price: $0.00085 per request.

        Example:
            res = client.playstore.search(country="us", limit=10, query="budget tracker")
        """
        raw = self._client._run_raw(  # pyright: ignore[reportPrivateUsage]
            "playstore.search", dict(input), options
        )
        return RunResult[PlaystoreSearchData].model_validate(raw)


class AsyncPlaystoreNamespace:
    """Typed methods for this platform. Attached lazily to the client."""

    def __init__(self, client: "AsyncAnyAPI") -> None:
        self._client = client

    async def app(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[PlaystoreAppInput],
    ) -> RunResult[PlaystoreAppData]:
        """Google Play App Details

        Get an Android app's Google Play listing by package name, in any store
        country: title, developer and contact details, rating, ratings count,
        installs, price, description, screenshots, and more.

        Price: $0.00085 per request.

        Example:
            res = client.playstore.app(appId="com.playdigious.deadcells.mobile", country="us")
        """
        raw = await self._client._arun_raw(  # pyright: ignore[reportPrivateUsage]
            "playstore.app", dict(input), options
        )
        return RunResult[PlaystoreAppData].model_validate(raw)

    async def reviews(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[PlaystoreReviewsInput],
    ) -> RunResult[PlaystoreReviewsData]:
        """Google Play Reviews

        Fetch Google Play reviews for any Android app by package name or store URL:
        ratings, review text, dates, and helpfulness votes.

        Price: $0.0009 per request.

        Example:
            res = client.playstore.reviews(appId="com.whatsapp", limit=3)
        """
        raw = await self._client._arun_raw(  # pyright: ignore[reportPrivateUsage]
            "playstore.reviews", dict(input), options
        )
        return RunResult[PlaystoreReviewsData].model_validate(raw)

    async def search(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[PlaystoreSearchInput],
    ) -> RunResult[PlaystoreSearchData]:
        """Google Play Search

        Search Google Play for Android apps by keyword, in any store country:
        package name, title, developer, rating, installs, price, and category for
        each result.

        Price: $0.00085 per request.

        Example:
            res = client.playstore.search(country="us", limit=10, query="budget tracker")
        """
        raw = await self._client._arun_raw(  # pyright: ignore[reportPrivateUsage]
            "playstore.search", dict(input), options
        )
        return RunResult[PlaystoreSearchData].model_validate(raw)
