# Generated - do not edit. Regenerate with: pnpm generate
"""Generated namespace module for the pexels platform."""

from __future__ import annotations

from typing import Literal, TYPE_CHECKING

from pydantic import BaseModel, ConfigDict, Field
from typing_extensions import NotRequired, Required, TypedDict, Unpack

from ..types import RequestOptions, RunResult

if TYPE_CHECKING:
    from .._async_client import AsyncAnyAPI
    from .._client import AnyAPI


class PexelsSearchPhotosInput(TypedDict, total=False):
    """Input for Pexels Photo Search."""

    allowFallbacks: NotRequired[bool]
    """Optional, default true. When false, only the sources listed in `source` may serve; the request is refused with no charge if none of them can. When true, the listed sources are tried first and any other source may serve after them, at the normal price. Default: true."""
    ignoreSources: NotRequired[list[str]]
    """Optional. Source ids to skip for this request, taken from this endpoint's `lanes[].source.id`. The cheapest remaining source serves and the price is that of the dearest remaining source. An id that does not serve this endpoint, or that is also in `source`, is rejected as invalid input with no charge; skipping every source is rejected the same way."""
    limit: NotRequired[int]
    """Maximum number of photos to return (1-20, default 20). You are billed per photo returned, so a lower limit costs less. Range: 1 to 20."""
    minHeight: NotRequired[int]
    """Only return photos at least this many pixels tall. Minimum: 1."""
    minWidth: NotRequired[int]
    """Only return photos at least this many pixels wide. Minimum: 1."""
    orientation: NotRequired[Literal["landscape", "portrait", "square"]]
    """Only return photos with this orientation. Omit for any orientation."""
    peopleCount: NotRequired[Literal["0", "1", "2"]]
    """Only return photos showing this many people: "0" for none, "1" or "2". Omit for any number."""
    preferLatencyUnderMs: NotRequired[int]
    """Optional; omit it and routing is unchanged, with the cheapest source serving. Prefer sources whose typical response time (median over the trailing 30 days, as published on this endpoint's lane health) is under this many milliseconds; among those, the cheapest serves. This can raise your price: when the cheapest source misses the target, a faster and dearer one serves, and you are quoted and charged its price. If no source is that fast the request is still served, by whichever source offers the best speed for its price - it is never refused for being slow. Sources we have not timed are tried last. This is a preference, not a guarantee: the median describes past requests and is not a ceiling on this one, and it excludes any wait this request itself asks for. On a paginated walk it applies to the first page only: later pages stay with the source that page chose, at the price it was quoted. Minimum: 1."""
    query: Required[str]
    """Keyword or phrase to search Pexels photos for, e.g. "coffee" or "city skyline"."""
    requireFields: NotRequired[list[Literal["tags"]]]
    """Optional; omit it and routing is unchanged, with the cheapest source serving. Name the output fields this request must be able to return, for example `tags`, and it is served only by a source that returns every one of them. Fields you do not name are still returned whenever the serving source has them. This can raise your price: when the cheapest source cannot return a named field, a dearer source serves, and you are quoted and charged its price. A named field can still be absent on a photo that genuinely lacks it. Naming a combination that no single source returns together is refused as invalid input, with no charge."""
    source: NotRequired[list[str]]
    """Optional. Source ids to prefer, in order, taken from this endpoint's `lanes[].source.id` in /catalog or /apis. Omit it and the cheapest source serves, with automatic failover. Listed sources are tried first in the order given, then the others, unless `allowFallbacks` is false. A single source with `allowFallbacks` false is served only by that source at its price, quoted and charged exactly, with no failover. The price is that of the dearest source that may serve. An id that does not serve this endpoint is rejected as invalid input with no charge; a listed source that is not serving right now is refused with no charge, so omit `source` to be served by another. On a paginated walk, later pages must include the source that served page one, or omit `source`."""


class PexelsSearchPhotosData(BaseModel):
    photos: list[PexelsSearchPhotosPhoto] = Field(
        description="Free Pexels photos matching the keyword, in Pexels' relevance order."
    )


class PexelsSearchPhotosPhoto(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    alt: str | None = Field(
        default=None,
        description="Alt text describing the photo. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    color: str | None = Field(
        default=None, description='Dominant color as a hex code, e.g. "#918c79".'
    )
    colors: list[str] | None = Field(
        default=None, description="Palette of the photo's main colors as hex codes."
    )
    created_utc: float | None = Field(
        default=None,
        alias="createdUtc",
        description="When the photo was uploaded. UTC epoch timestamp in seconds (Unix time). Multiply by 1000 for a JS Date in milliseconds.",
    )
    download_url: str | None = Field(
        default=None,
        alias="downloadUrl",
        description="Direct download URL for the full-quality file.",
    )
    height: int | None = Field(
        default=None,
        description="Original height in pixels. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    id: str = Field(
        description="Photo id on the source site. Populated whenever the provider has data for the entity."
    )
    image: str = Field(
        description="Display-size image URL, 1440 px wide. The query parameters set the size, so keep the URL intact. Populated whenever the provider has data for the entity."
    )
    image_medium: str | None = Field(
        default=None, alias="imageMedium", description="Medium image URL, 750 px wide."
    )
    image_original: str | None = Field(
        default=None,
        alias="imageOriginal",
        description="Full-resolution original image URL. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    license: str | None = Field(
        default=None,
        description='License the photo is published under. "Pexels" means the Pexels License: free to use, attribution appreciated but not required. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.',
    )
    orientation: str | None = Field(
        default=None, description="landscape, portrait, or square."
    )
    photographer: str | None = Field(
        default=None,
        description="Photographer's display name, for attribution. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    photographer_avatar_url: str | None = Field(
        default=None,
        alias="photographerAvatarUrl",
        description="Photographer's profile picture URL.",
    )
    photographer_instagram_username: str | None = Field(
        default=None,
        alias="photographerInstagramUsername",
        description="Photographer's Instagram username, when they list one on Pexels.",
    )
    photographer_location: str | None = Field(
        default=None,
        alias="photographerLocation",
        description="Photographer's location as they state it on Pexels, when they list one.",
    )
    photographer_url: str | None = Field(
        default=None,
        alias="photographerUrl",
        description="Photographer's Pexels profile page, for attribution. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    photographer_username: str | None = Field(
        default=None,
        alias="photographerUsername",
        description="Photographer's Pexels handle, without the leading @.",
    )
    published_utc: float | None = Field(
        default=None,
        alias="publishedUtc",
        description="When Pexels published the photo. UTC epoch timestamp in seconds (Unix time). Multiply by 1000 for a JS Date in milliseconds.",
    )
    tags: list[str] | None = Field(
        default=None,
        description="Pexels' tags for the photo. One source returns at most 25 tags; name tags in requireFields to be served the full list.",
    )
    thumbnail: str | None = Field(
        default=None, description="Thumbnail image URL, 130 px tall."
    )
    title: str | None = Field(
        default=None, description="Photo title set by the photographer."
    )
    url: str = Field(
        description="The photo's page on pexels.com. Populated whenever the provider has data for the entity."
    )
    width: int | None = Field(
        default=None,
        description="Original width in pixels. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )


class PexelsNamespace:
    """Typed methods for this platform. Attached lazily to the client."""

    def __init__(self, client: "AnyAPI") -> None:
        self._client = client

    def search_photos(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[PexelsSearchPhotosInput],
    ) -> RunResult[PexelsSearchPhotosData]:
        """Pexels Photo Search

        Search Pexels for free stock photos by keyword. Returns image URLs in
        several sizes, dimensions, alt text, the photographer's name and profile,
        and the photo's Pexels page.

        Price: $0.00055 per request plus $0.0033 per result (maximum $0.0666).

        Example:
            res = client.pexels.search_photos(limit=2, query="coffee")
        """
        raw = self._client._run_raw(  # pyright: ignore[reportPrivateUsage]
            "pexels.search_photos", dict(input), options
        )
        return RunResult[PexelsSearchPhotosData].model_validate(raw)


class AsyncPexelsNamespace:
    """Typed methods for this platform. Attached lazily to the client."""

    def __init__(self, client: "AsyncAnyAPI") -> None:
        self._client = client

    async def search_photos(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[PexelsSearchPhotosInput],
    ) -> RunResult[PexelsSearchPhotosData]:
        """Pexels Photo Search

        Search Pexels for free stock photos by keyword. Returns image URLs in
        several sizes, dimensions, alt text, the photographer's name and profile,
        and the photo's Pexels page.

        Price: $0.00055 per request plus $0.0033 per result (maximum $0.0666).

        Example:
            res = client.pexels.search_photos(limit=2, query="coffee")
        """
        raw = await self._client._arun_raw(  # pyright: ignore[reportPrivateUsage]
            "pexels.search_photos", dict(input), options
        )
        return RunResult[PexelsSearchPhotosData].model_validate(raw)
