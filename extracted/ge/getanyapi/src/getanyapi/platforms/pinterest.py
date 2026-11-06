# Generated - do not edit. Regenerate with: pnpm generate
"""Generated namespace module for the pinterest platform."""

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


class PinterestPinInput(TypedDict, total=False):
    """Input for Pinterest Pin."""

    allowFallbacks: NotRequired[bool]
    """Optional, default true. When false, only the sources listed in `source` may serve; the request is refused with no charge if none of them can. When true, the listed sources are tried first and any other source may serve after them, at the normal price. Default: true."""
    ignoreSources: NotRequired[list[str]]
    """Optional. Source ids to skip for this request, taken from this endpoint's `lanes[].source.id`. The cheapest remaining source serves and the price is that of the dearest remaining source. An id that does not serve this endpoint, or that is also in `source`, is rejected as invalid input with no charge; skipping every source is rejected the same way."""
    pinId: NotRequired[str]
    """Numeric Pinterest pin id, the number in the pin URL (https://www.pinterest.com/pin/<id>/), e.g. 101049585382283341. Pinterest Search returns it as id. Send this or url."""
    preferLatencyUnderMs: NotRequired[int]
    """Optional; omit it and routing is unchanged, with the cheapest source serving. Prefer sources whose typical response time (median over the trailing 30 days, as published on this endpoint's lane health) is under this many milliseconds; among those, the cheapest serves. This can raise your price: when the cheapest source misses the target, a faster and dearer one serves, and you are quoted and charged its price. If no source is that fast the request is still served, by whichever source offers the best speed for its price - it is never refused for being slow. Sources we have not timed are tried last. This is a preference, not a guarantee: the median describes past requests and is not a ceiling on this one, and it excludes any wait this request itself asks for. On a paginated walk it applies to the first page only: later pages stay with the source that page chose, at the price it was quoted. Minimum: 1."""
    source: NotRequired[list[str]]
    """Optional. Source ids to prefer, in order, taken from this endpoint's `lanes[].source.id` in /catalog or /apis. Omit it and the cheapest source serves, with automatic failover. Listed sources are tried first in the order given, then the others, unless `allowFallbacks` is false. A single source with `allowFallbacks` false is served only by that source at its price, quoted and charged exactly, with no failover. The price is that of the dearest source that may serve. An id that does not serve this endpoint is rejected as invalid input with no charge; a listed source that is not serving right now is refused with no charge, so omit `source` to be served by another. On a paginated walk, later pages must include the source that served page one, or omit `source`."""
    url: NotRequired[str]
    """Full Pinterest pin URL carrying the numeric pin id, e.g. https://www.pinterest.com/pin/101049585382283341/. Country sites such as uk.pinterest.com or pinterest.de work too. pin.it short links are not accepted: open the link in a browser and send the pinterest.com/pin/... address it lands on. Send this or pinId."""


class PinterestSearchInput(TypedDict, total=False):
    """Input for Pinterest Search."""

    allowFallbacks: NotRequired[bool]
    """Optional, default true. When false, only the sources listed in `source` may serve; the request is refused with no charge if none of them can. When true, the listed sources are tried first and any other source may serve after them, at the normal price. Default: true."""
    cursor: NotRequired[str]
    """Opaque pagination cursor from a previous response's nextCursor. Omit for the first page."""
    ignoreSources: NotRequired[list[str]]
    """Optional. Source ids to skip for this request, taken from this endpoint's `lanes[].source.id`. The cheapest remaining source serves and the price is that of the dearest remaining source. An id that does not serve this endpoint, or that is also in `source`, is rejected as invalid input with no charge; skipping every source is rejected the same way."""
    limit: NotRequired[int]
    """Page size to ask for (1-20). Some sources return their whole page of about 20 pins whatever limit says: a page is never trimmed after the call, so nextCursor continues exactly where this response ended. Range: 1 to 20."""
    preferLatencyUnderMs: NotRequired[int]
    """Optional; omit it and routing is unchanged, with the cheapest source serving. Prefer sources whose typical response time (median over the trailing 30 days, as published on this endpoint's lane health) is under this many milliseconds; among those, the cheapest serves. This can raise your price: when the cheapest source misses the target, a faster and dearer one serves, and you are quoted and charged its price. If no source is that fast the request is still served, by whichever source offers the best speed for its price - it is never refused for being slow. Sources we have not timed are tried last. This is a preference, not a guarantee: the median describes past requests and is not a ceiling on this one, and it excludes any wait this request itself asks for. On a paginated walk it applies to the first page only: later pages stay with the source that page chose, at the price it was quoted. Minimum: 1."""
    query: Required[str]
    """Keyword, topic, brand, or theme to search Pinterest for (e.g. mid-century living room)."""
    requireFields: NotRequired[list[Literal["description", "videoUrl"]]]
    """Optional; omit it and routing is unchanged, with the cheapest source serving. Name the output fields this request must be able to return, for example `description` or `videoUrl`, and it is served only by a source that returns every one of them. Fields you do not name are still returned whenever the serving source has them. This can raise your price: when the cheapest source cannot return a named field, a dearer source serves, and you are quoted and charged its price. A named field can still be null on a pin that genuinely lacks it. Naming a combination that no single source returns together is refused as invalid input, with no charge."""
    source: NotRequired[list[str]]
    """Optional. Source ids to prefer, in order, taken from this endpoint's `lanes[].source.id` in /catalog or /apis. Omit it and the cheapest source serves, with automatic failover. Listed sources are tried first in the order given, then the others, unless `allowFallbacks` is false. A single source with `allowFallbacks` false is served only by that source at its price, quoted and charged exactly, with no failover. The price is that of the dearest source that may serve. An id that does not serve this endpoint is rejected as invalid input with no charge; a listed source that is not serving right now is refused with no charge, so omit `source` to be served by another. On a paginated walk, later pages must include the source that served page one, or omit `source`."""
    type: NotRequired[Literal["all-pins", "videos", "boards", "profiles"]]
    """Kind of results to return: all pins, only video pins, boards, or profiles (e.g. videos). Default: all-pins."""


class PinterestPinData(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    author: str | None = Field(
        default=None,
        description="Username (handle) of the account that saved the pin. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    author_followers: int | None = Field(
        default=None,
        alias="authorFollowers",
        description="Follower count of the account that saved the pin. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    author_id: str | None = Field(
        default=None,
        alias="authorId",
        description="Numeric Pinterest user id of the account that saved the pin.",
    )
    author_name: str | None = Field(
        default=None,
        alias="authorName",
        description="Display name of the account that saved the pin.",
    )
    board_id: str | None = Field(
        default=None,
        alias="boardId",
        description="Numeric id of the board the pin was saved to.",
    )
    board_name: str | None = Field(
        default=None,
        alias="boardName",
        description="Name of the board the pin was saved to. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    board_url: str | None = Field(
        default=None,
        alias="boardUrl",
        description="URL of the board the pin was saved to.",
    )
    comments: int | None = Field(
        default=None,
        description="Comment count, or null when the source does not report it.",
    )
    created_utc: float | None = Field(
        default=None,
        alias="createdUtc",
        description="UTC epoch timestamp in seconds (Unix time). Multiply by 1000 for a JS Date in milliseconds.",
    )
    description: str | None = Field(
        default=None, description="Pin description text, or null when the pin has none."
    )
    domain: str | None = Field(
        default=None,
        description="Domain of the outbound link (e.g. tilebar.com), or null when the pin has no link.",
    )
    hashtags: list[str] | None = Field(default=None, description="Hashtags on the pin.")
    id: str = Field(description="Numeric Pinterest pin id, as a string.")
    image: str | None = Field(
        default=None,
        description="URL of the pin's original-size image; for a video pin, its cover image. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    is_video: bool | None = Field(
        default=None, alias="isVideo", description="True when the pin is a video."
    )
    likes: int | None = Field(
        default=None,
        description="Reaction count, or null when the source does not report it.",
    )
    link: str | None = Field(
        default=None,
        description="The outbound website link the pin points to, or null when it has none.",
    )
    saves: int | None = Field(
        default=None,
        description="Number of times the pin has been saved (repinned). Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    title: str | None = Field(
        default=None, description="Pin title, or null when the pin has none."
    )
    url: str = Field(
        description="Canonical pin URL (https://www.pinterest.com/pin/<id>/)."
    )
    video_url: str | None = Field(
        default=None,
        alias="videoUrl",
        description="URL of the pin's video, or null when the pin is not a video.",
    )


class PinterestSearchData(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    items: list[PinterestSearchItem] = Field(
        description="Matching Pinterest records: pin or board title, description, image/video URL, creator, and link. Populated whenever the provider has data for the entity."
    )
    next_cursor: str | None = Field(
        default=None,
        alias="nextCursor",
        description="Opaque cursor for the next page of results, or null/empty when there are no more. Pass it back as cursor to continue.",
    )


class PinterestSearchItem(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    author: str | None = Field(
        default=None, description="Username (handle) of the account that saved the pin."
    )
    author_name: str | None = Field(
        default=None,
        alias="authorName",
        description="Display name of the account that saved the pin.",
    )
    description: str | None = Field(
        default=None,
        description="The pin's full description text, or null when the source does not provide it.",
    )
    id: str
    image: str | None = Field(
        default=None,
        description="URL of the pin's full-size image; for a video pin, its cover image.",
    )
    title: str = Field(
        description="Pin title, or the pin's description when the pin has no title."
    )
    url: str = Field(
        description="Populated whenever the provider has data for the entity."
    )
    video_url: str | None = Field(
        default=None,
        alias="videoUrl",
        description="Streaming (HLS) URL of the pin's video, or null when the pin is not a video or the source does not provide it.",
    )


class PinterestNamespace:
    """Typed methods for this platform. Attached lazily to the client."""

    def __init__(self, client: "AnyAPI") -> None:
        self._client = client

    def pin(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[PinterestPinInput],
    ) -> RunResult[PinterestPinData]:
        """Pinterest Pin

        Fetch one public Pinterest pin by URL or numeric pin id: title, description,
        image, video, outbound link and site, save count, hashtags, the pinner with
        their follower count, and the board it was saved to, as normalized JSON. A
        pin that does not exist is not charged.

        Price: $0.00085 per request.

        Example:
            res = client.pinterest.pin(url="https://www.pinterest.com/pin/101049585382283341/")
        """
        raw = self._client._run_raw(  # pyright: ignore[reportPrivateUsage]
            "pinterest.pin", dict(input), options
        )
        return RunResult[PinterestPinData].model_validate(raw)

    def search(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[PinterestSearchInput],
    ) -> RunResult[PinterestSearchData]:
        """Pinterest Search

        Search Pinterest by keyword and get pin, video, board, or profile results
        with titles, images, and links.

        Price: $0.0008 per request.

        Example:
            res = client.pinterest.search(limit=3, query="home decor")
        """
        raw = self._client._run_raw(  # pyright: ignore[reportPrivateUsage]
            "pinterest.search", dict(input), options
        )
        return RunResult[PinterestSearchData].model_validate(raw)

    def iter_search(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[PinterestSearchInput],
    ) -> Paginator[PinterestSearchItem, PinterestSearchData]:
        """Iterate Pinterest Search results, following pagination cursors.

        Yields validated `PinterestSearchItem` items from the `items` field of
        each page. Use `.pages()` on the returned paginator to walk whole
        `RunResult` pages.
        """
        return paginate(
            self._client,
            "pinterest.search",
            dict(input),
            "items",
            item_model=PinterestSearchItem,
            data_model=PinterestSearchData,
            bare=False,
            options=options,
        )


class AsyncPinterestNamespace:
    """Typed methods for this platform. Attached lazily to the client."""

    def __init__(self, client: "AsyncAnyAPI") -> None:
        self._client = client

    async def pin(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[PinterestPinInput],
    ) -> RunResult[PinterestPinData]:
        """Pinterest Pin

        Fetch one public Pinterest pin by URL or numeric pin id: title, description,
        image, video, outbound link and site, save count, hashtags, the pinner with
        their follower count, and the board it was saved to, as normalized JSON. A
        pin that does not exist is not charged.

        Price: $0.00085 per request.

        Example:
            res = client.pinterest.pin(url="https://www.pinterest.com/pin/101049585382283341/")
        """
        raw = await self._client._arun_raw(  # pyright: ignore[reportPrivateUsage]
            "pinterest.pin", dict(input), options
        )
        return RunResult[PinterestPinData].model_validate(raw)

    async def search(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[PinterestSearchInput],
    ) -> RunResult[PinterestSearchData]:
        """Pinterest Search

        Search Pinterest by keyword and get pin, video, board, or profile results
        with titles, images, and links.

        Price: $0.0008 per request.

        Example:
            res = client.pinterest.search(limit=3, query="home decor")
        """
        raw = await self._client._arun_raw(  # pyright: ignore[reportPrivateUsage]
            "pinterest.search", dict(input), options
        )
        return RunResult[PinterestSearchData].model_validate(raw)

    def iter_search(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[PinterestSearchInput],
    ) -> AsyncPaginator[PinterestSearchItem, PinterestSearchData]:
        """Iterate Pinterest Search results, following pagination cursors.

        Yields validated `PinterestSearchItem` items from the `items` field of
        each page. Use `.pages()` on the returned paginator to walk whole
        `RunResult` pages.
        """
        return apaginate(
            self._client,
            "pinterest.search",
            dict(input),
            "items",
            item_model=PinterestSearchItem,
            data_model=PinterestSearchData,
            bare=False,
            options=options,
        )
