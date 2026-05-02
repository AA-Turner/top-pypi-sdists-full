# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import typing_extensions

import httpx

from ..types import artist_top_tracks_params, artist_list_albums_params, artist_bulk_retrieve_params
from .._types import Body, Omit, Query, Headers, NotGiven, omit, not_given
from .._utils import path_template, maybe_transform, async_maybe_transform
from .._compat import cached_property
from .._resource import SyncAPIResource, AsyncAPIResource
from .._response import (
    to_raw_response_wrapper,
    to_streamed_response_wrapper,
    async_to_raw_response_wrapper,
    async_to_streamed_response_wrapper,
)
from ..pagination import SyncCursorURLPage, AsyncCursorURLPage
from .._base_client import AsyncPaginator, make_request_options
from ..types.shared.artist_object import ArtistObject
from ..types.artist_top_tracks_response import ArtistTopTracksResponse
from ..types.artist_list_albums_response import ArtistListAlbumsResponse
from ..types.artist_bulk_retrieve_response import ArtistBulkRetrieveResponse
from ..types.artist_list_related_artists_response import ArtistListRelatedArtistsResponse

__all__ = ["ArtistsResource", "AsyncArtistsResource"]


class ArtistsResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> ArtistsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/cjavdev/spotted-py#accessing-raw-response-data-eg-headers
        """
        return ArtistsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> ArtistsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/cjavdev/spotted-py#with_streaming_response
        """
        return ArtistsResourceWithStreamingResponse(self)

    def retrieve(
        self,
        id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> ArtistObject:
        """
        Get Spotify catalog information for a single artist identified by their unique
        Spotify ID.

        Args:
          id: The [Spotify ID](/documentation/web-api/concepts/spotify-uris-ids) of the
              artist.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        return self._get(
            path_template("/artists/{id}", id=id),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=ArtistObject,
        )

    @typing_extensions.deprecated("deprecated")
    def bulk_retrieve(
        self,
        *,
        ids: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> ArtistBulkRetrieveResponse:
        """
        Get Spotify catalog information for several artists based on their Spotify IDs.

        Args:
          ids: A comma-separated list of the
              [Spotify IDs](/documentation/web-api/concepts/spotify-uris-ids) for the artists.
              Maximum: 50 IDs.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._get(
            "/artists",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform({"ids": ids}, artist_bulk_retrieve_params.ArtistBulkRetrieveParams),
            ),
            cast_to=ArtistBulkRetrieveResponse,
        )

    def list_albums(
        self,
        id: str,
        *,
        include_groups: str | Omit = omit,
        limit: int | Omit = omit,
        market: str | Omit = omit,
        offset: int | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> SyncCursorURLPage[ArtistListAlbumsResponse]:
        """
        Get Spotify catalog information about an artist's albums.

        Args:
          id: The [Spotify ID](/documentation/web-api/concepts/spotify-uris-ids) of the
              artist.

          include_groups: A comma-separated list of keywords that will be used to filter the response. If
              not supplied, all album types will be returned. <br/> Valid values are:<br/>-
              `album`<br/>- `single`<br/>- `appears_on`<br/>- `compilation`<br/>For example:
              `include_groups=album,single`.

          limit: The maximum number of items to return. Default: 5. Minimum: 1. Maximum: 10.

          market: An
              [ISO 3166-1 alpha-2 country code](https://en.wikipedia.org/wiki/ISO_3166-1_alpha-2).
              If a country code is specified, only content that is available in that market
              will be returned.<br/> If a valid user access token is specified in the request
              header, the country associated with the user account will take priority over
              this parameter.<br/> _**Note**: If neither market or user country are provided,
              the content is considered unavailable for the client._<br/> Users can view the
              country that is associated with their account in the
              [account settings](https://www.spotify.com/account/overview/).

          offset: The index of the first item to return. Default: 0 (the first item). Use with
              limit to get the next set of items.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        return self._get_api_list(
            path_template("/artists/{id}/albums", id=id),
            page=SyncCursorURLPage[ArtistListAlbumsResponse],
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "include_groups": include_groups,
                        "limit": limit,
                        "market": market,
                        "offset": offset,
                    },
                    artist_list_albums_params.ArtistListAlbumsParams,
                ),
            ),
            model=ArtistListAlbumsResponse,
        )

    @typing_extensions.deprecated("deprecated")
    def list_related_artists(
        self,
        id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> ArtistListRelatedArtistsResponse:
        """
        Get Spotify catalog information about artists similar to a given artist.
        Similarity is based on analysis of the Spotify community's listening history.

        Args:
          id: The [Spotify ID](/documentation/web-api/concepts/spotify-uris-ids) of the
              artist.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        return self._get(
            path_template("/artists/{id}/related-artists", id=id),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=ArtistListRelatedArtistsResponse,
        )

    @typing_extensions.deprecated("deprecated")
    def top_tracks(
        self,
        id: str,
        *,
        market: str | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> ArtistTopTracksResponse:
        """
        Get Spotify catalog information about an artist's top tracks by country.

        Args:
          id: The [Spotify ID](/documentation/web-api/concepts/spotify-uris-ids) of the
              artist.

          market: An
              [ISO 3166-1 alpha-2 country code](https://en.wikipedia.org/wiki/ISO_3166-1_alpha-2).
              If a country code is specified, only content that is available in that market
              will be returned.<br/> If a valid user access token is specified in the request
              header, the country associated with the user account will take priority over
              this parameter.<br/> _**Note**: If neither market or user country are provided,
              the content is considered unavailable for the client._<br/> Users can view the
              country that is associated with their account in the
              [account settings](https://www.spotify.com/account/overview/).

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        return self._get(
            path_template("/artists/{id}/top-tracks", id=id),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform({"market": market}, artist_top_tracks_params.ArtistTopTracksParams),
            ),
            cast_to=ArtistTopTracksResponse,
        )


class AsyncArtistsResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncArtistsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/cjavdev/spotted-py#accessing-raw-response-data-eg-headers
        """
        return AsyncArtistsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncArtistsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/cjavdev/spotted-py#with_streaming_response
        """
        return AsyncArtistsResourceWithStreamingResponse(self)

    async def retrieve(
        self,
        id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> ArtistObject:
        """
        Get Spotify catalog information for a single artist identified by their unique
        Spotify ID.

        Args:
          id: The [Spotify ID](/documentation/web-api/concepts/spotify-uris-ids) of the
              artist.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        return await self._get(
            path_template("/artists/{id}", id=id),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=ArtistObject,
        )

    @typing_extensions.deprecated("deprecated")
    async def bulk_retrieve(
        self,
        *,
        ids: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> ArtistBulkRetrieveResponse:
        """
        Get Spotify catalog information for several artists based on their Spotify IDs.

        Args:
          ids: A comma-separated list of the
              [Spotify IDs](/documentation/web-api/concepts/spotify-uris-ids) for the artists.
              Maximum: 50 IDs.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._get(
            "/artists",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=await async_maybe_transform({"ids": ids}, artist_bulk_retrieve_params.ArtistBulkRetrieveParams),
            ),
            cast_to=ArtistBulkRetrieveResponse,
        )

    def list_albums(
        self,
        id: str,
        *,
        include_groups: str | Omit = omit,
        limit: int | Omit = omit,
        market: str | Omit = omit,
        offset: int | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> AsyncPaginator[ArtistListAlbumsResponse, AsyncCursorURLPage[ArtistListAlbumsResponse]]:
        """
        Get Spotify catalog information about an artist's albums.

        Args:
          id: The [Spotify ID](/documentation/web-api/concepts/spotify-uris-ids) of the
              artist.

          include_groups: A comma-separated list of keywords that will be used to filter the response. If
              not supplied, all album types will be returned. <br/> Valid values are:<br/>-
              `album`<br/>- `single`<br/>- `appears_on`<br/>- `compilation`<br/>For example:
              `include_groups=album,single`.

          limit: The maximum number of items to return. Default: 5. Minimum: 1. Maximum: 10.

          market: An
              [ISO 3166-1 alpha-2 country code](https://en.wikipedia.org/wiki/ISO_3166-1_alpha-2).
              If a country code is specified, only content that is available in that market
              will be returned.<br/> If a valid user access token is specified in the request
              header, the country associated with the user account will take priority over
              this parameter.<br/> _**Note**: If neither market or user country are provided,
              the content is considered unavailable for the client._<br/> Users can view the
              country that is associated with their account in the
              [account settings](https://www.spotify.com/account/overview/).

          offset: The index of the first item to return. Default: 0 (the first item). Use with
              limit to get the next set of items.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        return self._get_api_list(
            path_template("/artists/{id}/albums", id=id),
            page=AsyncCursorURLPage[ArtistListAlbumsResponse],
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "include_groups": include_groups,
                        "limit": limit,
                        "market": market,
                        "offset": offset,
                    },
                    artist_list_albums_params.ArtistListAlbumsParams,
                ),
            ),
            model=ArtistListAlbumsResponse,
        )

    @typing_extensions.deprecated("deprecated")
    async def list_related_artists(
        self,
        id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> ArtistListRelatedArtistsResponse:
        """
        Get Spotify catalog information about artists similar to a given artist.
        Similarity is based on analysis of the Spotify community's listening history.

        Args:
          id: The [Spotify ID](/documentation/web-api/concepts/spotify-uris-ids) of the
              artist.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        return await self._get(
            path_template("/artists/{id}/related-artists", id=id),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=ArtistListRelatedArtistsResponse,
        )

    @typing_extensions.deprecated("deprecated")
    async def top_tracks(
        self,
        id: str,
        *,
        market: str | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> ArtistTopTracksResponse:
        """
        Get Spotify catalog information about an artist's top tracks by country.

        Args:
          id: The [Spotify ID](/documentation/web-api/concepts/spotify-uris-ids) of the
              artist.

          market: An
              [ISO 3166-1 alpha-2 country code](https://en.wikipedia.org/wiki/ISO_3166-1_alpha-2).
              If a country code is specified, only content that is available in that market
              will be returned.<br/> If a valid user access token is specified in the request
              header, the country associated with the user account will take priority over
              this parameter.<br/> _**Note**: If neither market or user country are provided,
              the content is considered unavailable for the client._<br/> Users can view the
              country that is associated with their account in the
              [account settings](https://www.spotify.com/account/overview/).

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        return await self._get(
            path_template("/artists/{id}/top-tracks", id=id),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=await async_maybe_transform({"market": market}, artist_top_tracks_params.ArtistTopTracksParams),
            ),
            cast_to=ArtistTopTracksResponse,
        )


class ArtistsResourceWithRawResponse:
    def __init__(self, artists: ArtistsResource) -> None:
        self._artists = artists

        self.retrieve = to_raw_response_wrapper(
            artists.retrieve,
        )
        self.bulk_retrieve = (  # pyright: ignore[reportDeprecated]
            to_raw_response_wrapper(
                artists.bulk_retrieve,  # pyright: ignore[reportDeprecated],
            )
        )
        self.list_albums = to_raw_response_wrapper(
            artists.list_albums,
        )
        self.list_related_artists = (  # pyright: ignore[reportDeprecated]
            to_raw_response_wrapper(
                artists.list_related_artists,  # pyright: ignore[reportDeprecated],
            )
        )
        self.top_tracks = (  # pyright: ignore[reportDeprecated]
            to_raw_response_wrapper(
                artists.top_tracks,  # pyright: ignore[reportDeprecated],
            )
        )


class AsyncArtistsResourceWithRawResponse:
    def __init__(self, artists: AsyncArtistsResource) -> None:
        self._artists = artists

        self.retrieve = async_to_raw_response_wrapper(
            artists.retrieve,
        )
        self.bulk_retrieve = (  # pyright: ignore[reportDeprecated]
            async_to_raw_response_wrapper(
                artists.bulk_retrieve,  # pyright: ignore[reportDeprecated],
            )
        )
        self.list_albums = async_to_raw_response_wrapper(
            artists.list_albums,
        )
        self.list_related_artists = (  # pyright: ignore[reportDeprecated]
            async_to_raw_response_wrapper(
                artists.list_related_artists,  # pyright: ignore[reportDeprecated],
            )
        )
        self.top_tracks = (  # pyright: ignore[reportDeprecated]
            async_to_raw_response_wrapper(
                artists.top_tracks,  # pyright: ignore[reportDeprecated],
            )
        )


class ArtistsResourceWithStreamingResponse:
    def __init__(self, artists: ArtistsResource) -> None:
        self._artists = artists

        self.retrieve = to_streamed_response_wrapper(
            artists.retrieve,
        )
        self.bulk_retrieve = (  # pyright: ignore[reportDeprecated]
            to_streamed_response_wrapper(
                artists.bulk_retrieve,  # pyright: ignore[reportDeprecated],
            )
        )
        self.list_albums = to_streamed_response_wrapper(
            artists.list_albums,
        )
        self.list_related_artists = (  # pyright: ignore[reportDeprecated]
            to_streamed_response_wrapper(
                artists.list_related_artists,  # pyright: ignore[reportDeprecated],
            )
        )
        self.top_tracks = (  # pyright: ignore[reportDeprecated]
            to_streamed_response_wrapper(
                artists.top_tracks,  # pyright: ignore[reportDeprecated],
            )
        )


class AsyncArtistsResourceWithStreamingResponse:
    def __init__(self, artists: AsyncArtistsResource) -> None:
        self._artists = artists

        self.retrieve = async_to_streamed_response_wrapper(
            artists.retrieve,
        )
        self.bulk_retrieve = (  # pyright: ignore[reportDeprecated]
            async_to_streamed_response_wrapper(
                artists.bulk_retrieve,  # pyright: ignore[reportDeprecated],
            )
        )
        self.list_albums = async_to_streamed_response_wrapper(
            artists.list_albums,
        )
        self.list_related_artists = (  # pyright: ignore[reportDeprecated]
            async_to_streamed_response_wrapper(
                artists.list_related_artists,  # pyright: ignore[reportDeprecated],
            )
        )
        self.top_tracks = (  # pyright: ignore[reportDeprecated]
            async_to_streamed_response_wrapper(
                artists.top_tracks,  # pyright: ignore[reportDeprecated],
            )
        )
