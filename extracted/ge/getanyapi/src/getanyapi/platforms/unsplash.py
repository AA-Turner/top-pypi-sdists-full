# Generated - do not edit. Regenerate with: pnpm generate
"""Generated namespace module for the unsplash platform."""

from __future__ import annotations

from typing import Literal, TYPE_CHECKING

from pydantic import BaseModel, ConfigDict, Field
from typing_extensions import NotRequired, Required, TypedDict, Unpack

from ..types import RequestOptions, RunResult

if TYPE_CHECKING:
    from .._async_client import AsyncAnyAPI
    from .._client import AnyAPI


class UnsplashSearchPhotosInput(TypedDict, total=False):
    """Input for Unsplash Photo Search."""

    allowFallbacks: NotRequired[bool]
    """Optional, default true. When false, only the sources listed in `source` may serve; the request is refused with no charge if none of them can. When true, the listed sources are tried first and any other source may serve after them, at the normal price. Default: true."""
    color: NotRequired[
        Literal[
            "black_and_white",
            "black",
            "white",
            "yellow",
            "orange",
            "red",
            "purple",
            "magenta",
            "green",
            "teal",
            "blue",
        ]
    ]
    """Only return photos with this dominant color tone. Omit for any color."""
    ignoreSources: NotRequired[list[str]]
    """Optional. Source ids to skip for this request, taken from this endpoint's `lanes[].source.id`. The cheapest remaining source serves and the price is that of the dearest remaining source. An id that does not serve this endpoint, or that is also in `source`, is rejected as invalid input with no charge; skipping every source is rejected the same way."""
    limit: NotRequired[int]
    """Maximum number of photos to return (1-20, default 20). You are billed per photo returned, so a lower limit costs less. Range: 1 to 20."""
    orientation: NotRequired[Literal["landscape", "portrait", "square"]]
    """Only return photos with this orientation. Omit for any orientation."""
    preferLatencyUnderMs: NotRequired[int]
    """Optional; omit it and routing is unchanged, with the cheapest source serving. Prefer sources whose typical response time (median over the trailing 30 days, as published on this endpoint's lane health) is under this many milliseconds; among those, the cheapest serves. This can raise your price: when the cheapest source misses the target, a faster and dearer one serves, and you are quoted and charged its price. If no source is that fast the request is still served, by whichever source offers the best speed for its price - it is never refused for being slow. Sources we have not timed are tried last. This is a preference, not a guarantee: the median describes past requests and is not a ceiling on this one, and it excludes any wait this request itself asks for. On a paginated walk it applies to the first page only: later pages stay with the source that page chose, at the price it was quoted. Minimum: 1."""
    query: Required[str]
    """Keyword or phrase to search Unsplash photos for, e.g. "coffee" or "minimal workspace"."""
    sortBy: NotRequired[Literal["relevant", "recent"]]
    """Order results by best match (relevant, the default) or newest first (recent). Default: relevant."""
    source: NotRequired[list[str]]
    """Optional. Source ids to prefer, in order, taken from this endpoint's `lanes[].source.id` in /catalog or /apis. Omit it and the cheapest source serves, with automatic failover. Listed sources are tried first in the order given, then the others, unless `allowFallbacks` is false. A single source with `allowFallbacks` false is served only by that source at its price, quoted and charged exactly, with no failover. The price is that of the dearest source that may serve. An id that does not serve this endpoint is rejected as invalid input with no charge; a listed source that is not serving right now is refused with no charge, so omit `source` to be served by another. On a paginated walk, later pages must include the source that served page one, or omit `source`."""


class UnsplashSearchPhotosData(BaseModel):
    photos: list[UnsplashSearchPhotosPhoto] = Field(
        description="Free Unsplash photos matching the keyword. Unsplash+ premium photos are excluded, so every photo is under the Unsplash License. Unsplash places sponsored photos among the results, flagged by sponsored."
    )


class UnsplashSearchPhotosPhoto(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    alt: str | None = Field(
        default=None,
        description="Alt text describing the photo. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    blur_hash: str | None = Field(
        default=None,
        alias="blurHash",
        description="BlurHash string for rendering a blurred placeholder while the image loads.",
    )
    color: str | None = Field(
        default=None, description='Dominant color as a hex code, e.g. "#918c79".'
    )
    created_utc: float | None = Field(
        default=None,
        alias="createdUtc",
        description="UTC epoch timestamp in seconds (Unix time). Multiply by 1000 for a JS Date in milliseconds.",
    )
    description: str | None = Field(
        default=None,
        description="Photographer's own description. Absent when they wrote none.",
    )
    download_url: str | None = Field(
        default=None,
        alias="downloadUrl",
        description="Unsplash download link for the photo.",
    )
    height: int | None = Field(
        default=None,
        description="Original height in pixels. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    id: str = Field(
        description="Photo id on the source site. Populated whenever the provider has data for the entity."
    )
    image: str = Field(
        description="Display-size image URL, 1080 px wide. The query parameters set the size, so keep the URL intact. Populated whenever the provider has data for the entity."
    )
    image_full: str | None = Field(
        default=None, alias="imageFull", description="Full-resolution JPEG URL."
    )
    image_original: str | None = Field(
        default=None,
        alias="imageOriginal",
        description="Original image URL at full resolution, unprocessed. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    image_small: str | None = Field(
        default=None, alias="imageSmall", description="Small image URL, 400 px wide."
    )
    likes: int | None = Field(default=None, description="Number of likes on Unsplash.")
    photographer: str | None = Field(
        default=None,
        description="Photographer's display name, for attribution. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    photographer_avatar_url: str | None = Field(
        default=None,
        alias="photographerAvatarUrl",
        description="Photographer's profile picture URL.",
    )
    photographer_bio: str | None = Field(
        default=None,
        alias="photographerBio",
        description="Photographer's Unsplash bio, when they wrote one.",
    )
    photographer_for_hire: bool | None = Field(
        default=None,
        alias="photographerForHire",
        description="True when the photographer marks themselves available for hire on Unsplash.",
    )
    photographer_instagram_username: str | None = Field(
        default=None,
        alias="photographerInstagramUsername",
        description="Photographer's Instagram username, when they list one on Unsplash.",
    )
    photographer_location: str | None = Field(
        default=None,
        alias="photographerLocation",
        description="Photographer's location as they state it on Unsplash, when they list one.",
    )
    photographer_total_likes: int | None = Field(
        default=None,
        alias="photographerTotalLikes",
        description="Number of photos the photographer has liked on Unsplash.",
    )
    photographer_total_photos: int | None = Field(
        default=None,
        alias="photographerTotalPhotos",
        description="Number of photos the photographer has published on Unsplash.",
    )
    photographer_twitter_username: str | None = Field(
        default=None,
        alias="photographerTwitterUsername",
        description="Photographer's X (Twitter) username, when they list one on Unsplash.",
    )
    photographer_url: str | None = Field(
        default=None,
        alias="photographerUrl",
        description="Photographer's Unsplash profile page, for attribution. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    photographer_username: str | None = Field(
        default=None,
        alias="photographerUsername",
        description="Photographer's Unsplash username, without the leading @.",
    )
    photographer_website: str | None = Field(
        default=None,
        alias="photographerWebsite",
        description="Photographer's portfolio or personal website, when they list one.",
    )
    sponsored: bool | None = Field(
        default=None,
        description="True when Unsplash placed this photo in the results as a sponsored listing.",
    )
    thumbnail: str | None = Field(
        default=None, description="Thumbnail image URL, 200 px wide."
    )
    updated_utc: float | None = Field(
        default=None,
        alias="updatedUtc",
        description="When the photo's record last changed on Unsplash. UTC epoch timestamp in seconds (Unix time). Multiply by 1000 for a JS Date in milliseconds.",
    )
    url: str = Field(
        description="The photo's page on unsplash.com. Populated whenever the provider has data for the entity."
    )
    width: int | None = Field(
        default=None,
        description="Original width in pixels. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )


class UnsplashNamespace:
    """Typed methods for this platform. Attached lazily to the client."""

    def __init__(self, client: "AnyAPI") -> None:
        self._client = client

    def search_photos(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[UnsplashSearchPhotosInput],
    ) -> RunResult[UnsplashSearchPhotosData]:
        """Unsplash Photo Search

        Search Unsplash for free stock photos by keyword. Returns image URLs in
        several sizes, dimensions, alt text, the photographer's name and profile,
        and the photo's Unsplash page.

        Price: $0.00055 per request plus $0.00165 per result (maximum $0.0336).

        Example:
            res = client.unsplash.search_photos(limit=2, query="coffee")
        """
        raw = self._client._run_raw(  # pyright: ignore[reportPrivateUsage]
            "unsplash.search_photos", dict(input), options
        )
        return RunResult[UnsplashSearchPhotosData].model_validate(raw)


class AsyncUnsplashNamespace:
    """Typed methods for this platform. Attached lazily to the client."""

    def __init__(self, client: "AsyncAnyAPI") -> None:
        self._client = client

    async def search_photos(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[UnsplashSearchPhotosInput],
    ) -> RunResult[UnsplashSearchPhotosData]:
        """Unsplash Photo Search

        Search Unsplash for free stock photos by keyword. Returns image URLs in
        several sizes, dimensions, alt text, the photographer's name and profile,
        and the photo's Unsplash page.

        Price: $0.00055 per request plus $0.00165 per result (maximum $0.0336).

        Example:
            res = client.unsplash.search_photos(limit=2, query="coffee")
        """
        raw = await self._client._arun_raw(  # pyright: ignore[reportPrivateUsage]
            "unsplash.search_photos", dict(input), options
        )
        return RunResult[UnsplashSearchPhotosData].model_validate(raw)
