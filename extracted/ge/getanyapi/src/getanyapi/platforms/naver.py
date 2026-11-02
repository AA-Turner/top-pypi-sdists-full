# Generated - do not edit. Regenerate with: pnpm generate
"""Generated namespace module for the naver platform."""

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


class NaverBlogSearchInput(TypedDict, total=False):
    """Input for Naver Blog Search."""

    allowFallbacks: NotRequired[bool]
    """Optional, default true. When false, only the sources listed in `source` may serve; the request is refused with no charge if none of them can. When true, the listed sources are tried first and any other source may serve after them, at the normal price. Default: true."""
    cursor: NotRequired[str]
    """Opaque pagination cursor from a previous response's nextCursor."""
    ignoreSources: NotRequired[list[str]]
    """Optional. Source ids to skip for this request, taken from this endpoint's `lanes[].source.id`. The cheapest remaining source serves and the price is that of the dearest remaining source. An id that does not serve this endpoint, or that is also in `source`, is rejected as invalid input with no charge; skipping every source is rejected the same way."""
    limit: NotRequired[int]
    """Maximum number of title-enriched posts to return, from 1 to 5 (default 5). Range: 1 to 5."""
    preferLatencyUnderMs: NotRequired[int]
    """Optional; omit it and routing is unchanged, with the cheapest source serving. Prefer sources whose typical response time (median over the trailing 30 days, as published on this endpoint's lane health) is under this many milliseconds; among those, the cheapest serves. This can raise your price: when the cheapest source misses the target, a faster and dearer one serves, and you are quoted and charged its price. If no source is that fast the request is still served, by whichever source offers the best speed for its price - it is never refused for being slow. Sources we have not timed are tried last. This is a preference, not a guarantee: the median describes past requests and is not a ceiling on this one, and it excludes any wait this request itself asks for. On a paginated walk it applies to the first page only: later pages stay with the source that page chose, at the price it was quoted. Minimum: 1."""
    query: Required[str]
    """Keyword phrase to search across Naver blogs."""
    sort: NotRequired[Literal["relevance", "recent"]]
    """Order posts by Naver relevance or newest publication date (default relevance)."""
    source: NotRequired[list[str]]
    """Optional. Source ids to prefer, in order, taken from this endpoint's `lanes[].source.id` in /catalog or /apis. Omit it and the cheapest source serves, with automatic failover. Listed sources are tried first in the order given, then the others, unless `allowFallbacks` is false. A single source with `allowFallbacks` false is served only by that source at its price, quoted and charged exactly, with no failover. The price is that of the dearest source that may serve. An id that does not serve this endpoint is rejected as invalid input with no charge; a listed source that is not serving right now is refused with no charge, so omit `source` to be served by another. On a paginated walk, later pages must include the source that served page one, or omit `source`."""


class NaverBlogSearchData(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    items: list[NaverBlogSearchItem] = Field(
        description="Blog posts in Naver's requested search order. Populated whenever the provider has data for the entity."
    )
    next_cursor: str | None = Field(
        alias="nextCursor",
        description="Opaque cursor for the next page, or an empty string when no next page is available.",
    )
    total: int = Field(
        description="Naver's reported number of matching blog posts. Minimum: 0."
    )


class NaverBlogSearchItem(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    blogger_name: str = Field(alias="bloggerName", description="Blogger display name.")
    blogger_url: str = Field(
        alias="bloggerUrl",
        description="Public root URL for the blog that published the post.",
    )
    created_utc: float = Field(
        alias="createdUtc",
        description="Publication date as a UTC epoch timestamp in seconds.",
    )
    description: str = Field(description="Search-result excerpt from the post.")
    language: str | None = Field(
        default=None,
        description="Two-letter language code Naver detected for the post text.",
    )
    rank: int = Field(description="One-based rank within this result page. Minimum: 1.")
    title: str = Field(description="Blog post title.")
    url: str = Field(description="Public blog post URL.")


class NaverNamespace:
    """Typed methods for this platform. Attached lazily to the client."""

    def __init__(self, client: "AnyAPI") -> None:
        self._client = client

    def blog_search(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[NaverBlogSearchInput],
    ) -> RunResult[NaverBlogSearchData]:
        """Naver Blog Search

        Search up to five enriched Naver blog results by keyword with stable cursor
        pagination: result rank, title, excerpt, post and blogger URLs, blogger
        name, publish time, and Naver's total match count.

        Price: $0.036 per request.

        Example:
            res = client.naver.blog_search(limit=5, query="제주도 맛집", sort="relevance")
        """
        raw = self._client._run_raw(  # pyright: ignore[reportPrivateUsage]
            "naver.blog_search", dict(input), options
        )
        return RunResult[NaverBlogSearchData].model_validate(raw)

    def iter_blog_search(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[NaverBlogSearchInput],
    ) -> Paginator[NaverBlogSearchItem, NaverBlogSearchData]:
        """Iterate Naver Blog Search results, following pagination cursors.

        Yields validated `NaverBlogSearchItem` items from the `items` field of
        each page. Use `.pages()` on the returned paginator to walk whole
        `RunResult` pages.
        """
        return paginate(
            self._client,
            "naver.blog_search",
            dict(input),
            "items",
            item_model=NaverBlogSearchItem,
            data_model=NaverBlogSearchData,
            bare=False,
            options=options,
        )


class AsyncNaverNamespace:
    """Typed methods for this platform. Attached lazily to the client."""

    def __init__(self, client: "AsyncAnyAPI") -> None:
        self._client = client

    async def blog_search(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[NaverBlogSearchInput],
    ) -> RunResult[NaverBlogSearchData]:
        """Naver Blog Search

        Search up to five enriched Naver blog results by keyword with stable cursor
        pagination: result rank, title, excerpt, post and blogger URLs, blogger
        name, publish time, and Naver's total match count.

        Price: $0.036 per request.

        Example:
            res = client.naver.blog_search(limit=5, query="제주도 맛집", sort="relevance")
        """
        raw = await self._client._arun_raw(  # pyright: ignore[reportPrivateUsage]
            "naver.blog_search", dict(input), options
        )
        return RunResult[NaverBlogSearchData].model_validate(raw)

    def iter_blog_search(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[NaverBlogSearchInput],
    ) -> AsyncPaginator[NaverBlogSearchItem, NaverBlogSearchData]:
        """Iterate Naver Blog Search results, following pagination cursors.

        Yields validated `NaverBlogSearchItem` items from the `items` field of
        each page. Use `.pages()` on the returned paginator to walk whole
        `RunResult` pages.
        """
        return apaginate(
            self._client,
            "naver.blog_search",
            dict(input),
            "items",
            item_model=NaverBlogSearchItem,
            data_model=NaverBlogSearchData,
            bare=False,
            options=options,
        )
