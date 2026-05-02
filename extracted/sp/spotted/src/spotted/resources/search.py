# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import List
from typing_extensions import Literal

import httpx

from ..types import search_query_params
from .._types import Body, Omit, Query, Headers, NotGiven, omit, not_given
from .._utils import maybe_transform, async_maybe_transform
from .._compat import cached_property
from .._resource import SyncAPIResource, AsyncAPIResource
from .._response import (
    to_raw_response_wrapper,
    to_streamed_response_wrapper,
    async_to_raw_response_wrapper,
    async_to_streamed_response_wrapper,
)
from .._base_client import make_request_options
from ..types.search_query_response import SearchQueryResponse

__all__ = ["SearchResource", "AsyncSearchResource"]


class SearchResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> SearchResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/cjavdev/spotted-py#accessing-raw-response-data-eg-headers
        """
        return SearchResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> SearchResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/cjavdev/spotted-py#with_streaming_response
        """
        return SearchResourceWithStreamingResponse(self)

    def query(
        self,
        *,
        q: str,
        type: List[Literal["album", "artist", "playlist", "track", "show", "episode", "audiobook"]],
        include_external: Literal["audio"] | Omit = omit,
        limit: int | Omit = omit,
        market: str | Omit = omit,
        offset: int | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> SearchQueryResponse:
        """
        Get Spotify catalog information about albums, artists, playlists, tracks, shows,
        episodes or audiobooks that match a keyword string. Audiobooks are only
        available within the US, UK, Canada, Ireland, New Zealand and Australia markets.

        Args:
          q: Your search query.

              You can narrow down your search using field filters. The available filters are
              `album`, `artist`, `track`, `year`, `upc`, `tag:hipster`, `tag:new`, `isrc`, and
              `genre`. Each field filter only applies to certain result types.

              The `artist` and `year` filters can be used while searching albums, artists and
              tracks. You can filter on a single `year` or a range (e.g. 1955-1960).<br /> The
              `album` filter can be used while searching albums and tracks.<br /> The `genre`
              filter can be used while searching artists and tracks.<br /> The `isrc` and
              `track` filters can be used while searching tracks.<br /> The `upc`, `tag:new`
              and `tag:hipster` filters can only be used while searching albums. The `tag:new`
              filter will return albums released in the past two weeks and `tag:hipster` can
              be used to return only albums with the lowest 10% popularity.<br />

          type: A comma-separated list of item types to search across. Search results include
              hits from all the specified item types. For example: `q=abacab&type=album,track`
              returns both albums and tracks matching "abacab".

          include_external: If `include_external=audio` is specified it signals that the client can play
              externally hosted audio content, and marks the content as playable in the
              response. By default externally hosted audio content is marked as unplayable in
              the response.

          limit: The maximum number of results to return in each item type.

          market: An
              [ISO 3166-1 alpha-2 country code](https://en.wikipedia.org/wiki/ISO_3166-1_alpha-2).
              If a country code is specified, only content that is available in that market
              will be returned.<br/> If a valid user access token is specified in the request
              header, the country associated with the user account will take priority over
              this parameter.<br/> _**Note**: If neither market or user country are provided,
              the content is considered unavailable for the client._<br/> Users can view the
              country that is associated with their account in the
              [account settings](https://www.spotify.com/account/overview/).

          offset: The index of the first result to return. Use with limit to get the next page of
              search results.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._get(
            "/search",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "q": q,
                        "type": type,
                        "include_external": include_external,
                        "limit": limit,
                        "market": market,
                        "offset": offset,
                    },
                    search_query_params.SearchQueryParams,
                ),
            ),
            cast_to=SearchQueryResponse,
        )


class AsyncSearchResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncSearchResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/cjavdev/spotted-py#accessing-raw-response-data-eg-headers
        """
        return AsyncSearchResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncSearchResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/cjavdev/spotted-py#with_streaming_response
        """
        return AsyncSearchResourceWithStreamingResponse(self)

    async def query(
        self,
        *,
        q: str,
        type: List[Literal["album", "artist", "playlist", "track", "show", "episode", "audiobook"]],
        include_external: Literal["audio"] | Omit = omit,
        limit: int | Omit = omit,
        market: str | Omit = omit,
        offset: int | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> SearchQueryResponse:
        """
        Get Spotify catalog information about albums, artists, playlists, tracks, shows,
        episodes or audiobooks that match a keyword string. Audiobooks are only
        available within the US, UK, Canada, Ireland, New Zealand and Australia markets.

        Args:
          q: Your search query.

              You can narrow down your search using field filters. The available filters are
              `album`, `artist`, `track`, `year`, `upc`, `tag:hipster`, `tag:new`, `isrc`, and
              `genre`. Each field filter only applies to certain result types.

              The `artist` and `year` filters can be used while searching albums, artists and
              tracks. You can filter on a single `year` or a range (e.g. 1955-1960).<br /> The
              `album` filter can be used while searching albums and tracks.<br /> The `genre`
              filter can be used while searching artists and tracks.<br /> The `isrc` and
              `track` filters can be used while searching tracks.<br /> The `upc`, `tag:new`
              and `tag:hipster` filters can only be used while searching albums. The `tag:new`
              filter will return albums released in the past two weeks and `tag:hipster` can
              be used to return only albums with the lowest 10% popularity.<br />

          type: A comma-separated list of item types to search across. Search results include
              hits from all the specified item types. For example: `q=abacab&type=album,track`
              returns both albums and tracks matching "abacab".

          include_external: If `include_external=audio` is specified it signals that the client can play
              externally hosted audio content, and marks the content as playable in the
              response. By default externally hosted audio content is marked as unplayable in
              the response.

          limit: The maximum number of results to return in each item type.

          market: An
              [ISO 3166-1 alpha-2 country code](https://en.wikipedia.org/wiki/ISO_3166-1_alpha-2).
              If a country code is specified, only content that is available in that market
              will be returned.<br/> If a valid user access token is specified in the request
              header, the country associated with the user account will take priority over
              this parameter.<br/> _**Note**: If neither market or user country are provided,
              the content is considered unavailable for the client._<br/> Users can view the
              country that is associated with their account in the
              [account settings](https://www.spotify.com/account/overview/).

          offset: The index of the first result to return. Use with limit to get the next page of
              search results.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._get(
            "/search",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=await async_maybe_transform(
                    {
                        "q": q,
                        "type": type,
                        "include_external": include_external,
                        "limit": limit,
                        "market": market,
                        "offset": offset,
                    },
                    search_query_params.SearchQueryParams,
                ),
            ),
            cast_to=SearchQueryResponse,
        )


class SearchResourceWithRawResponse:
    def __init__(self, search: SearchResource) -> None:
        self._search = search

        self.query = to_raw_response_wrapper(
            search.query,
        )


class AsyncSearchResourceWithRawResponse:
    def __init__(self, search: AsyncSearchResource) -> None:
        self._search = search

        self.query = async_to_raw_response_wrapper(
            search.query,
        )


class SearchResourceWithStreamingResponse:
    def __init__(self, search: SearchResource) -> None:
        self._search = search

        self.query = to_streamed_response_wrapper(
            search.query,
        )


class AsyncSearchResourceWithStreamingResponse:
    def __init__(self, search: AsyncSearchResource) -> None:
        self._search = search

        self.query = async_to_streamed_response_wrapper(
            search.query,
        )
