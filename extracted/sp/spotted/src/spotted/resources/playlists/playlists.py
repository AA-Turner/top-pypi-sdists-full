# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import httpx

from .images import (
    ImagesResource,
    AsyncImagesResource,
    ImagesResourceWithRawResponse,
    AsyncImagesResourceWithRawResponse,
    ImagesResourceWithStreamingResponse,
    AsyncImagesResourceWithStreamingResponse,
)
from .tracks import (
    TracksResource,
    AsyncTracksResource,
    TracksResourceWithRawResponse,
    AsyncTracksResourceWithRawResponse,
    TracksResourceWithStreamingResponse,
    AsyncTracksResourceWithStreamingResponse,
)
from ...types import playlist_update_params, playlist_retrieve_params
from ..._types import Body, Omit, Query, Headers, NoneType, NotGiven, omit, not_given
from ..._utils import path_template, maybe_transform, async_maybe_transform
from ..._compat import cached_property
from .followers import (
    FollowersResource,
    AsyncFollowersResource,
    FollowersResourceWithRawResponse,
    AsyncFollowersResourceWithRawResponse,
    FollowersResourceWithStreamingResponse,
    AsyncFollowersResourceWithStreamingResponse,
)
from ..._resource import SyncAPIResource, AsyncAPIResource
from ..._response import (
    to_raw_response_wrapper,
    to_streamed_response_wrapper,
    async_to_raw_response_wrapper,
    async_to_streamed_response_wrapper,
)
from ..._base_client import make_request_options
from ...types.playlist_retrieve_response import PlaylistRetrieveResponse

__all__ = ["PlaylistsResource", "AsyncPlaylistsResource"]


class PlaylistsResource(SyncAPIResource):
    @cached_property
    def tracks(self) -> TracksResource:
        return TracksResource(self._client)

    @cached_property
    def followers(self) -> FollowersResource:
        return FollowersResource(self._client)

    @cached_property
    def images(self) -> ImagesResource:
        return ImagesResource(self._client)

    @cached_property
    def with_raw_response(self) -> PlaylistsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/cjavdev/spotted-py#accessing-raw-response-data-eg-headers
        """
        return PlaylistsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> PlaylistsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/cjavdev/spotted-py#with_streaming_response
        """
        return PlaylistsResourceWithStreamingResponse(self)

    def retrieve(
        self,
        playlist_id: str,
        *,
        additional_types: str | Omit = omit,
        fields: str | Omit = omit,
        market: str | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> PlaylistRetrieveResponse:
        """
        Get a playlist owned by a Spotify user.

        Args:
          playlist_id: The [Spotify ID](/documentation/web-api/concepts/spotify-uris-ids) of the
              playlist.

          additional_types: A comma-separated list of item types that your client supports besides the
              default `track` type. Valid types are: `track` and `episode`.<br/> _**Note**:
              This parameter was introduced to allow existing clients to maintain their
              current behaviour and might be deprecated in the future._<br/> In addition to
              providing this parameter, make sure that your client properly handles cases of
              new types in the future by checking against the `type` field of each object.

          fields: Filters for the query: a comma-separated list of the fields to return. If
              omitted, all fields are returned. For example, to get just the playlist''s
              description and URI: `fields=description,uri`. A dot separator can be used to
              specify non-reoccurring fields, while parentheses can be used to specify
              reoccurring fields within objects. For example, to get just the added date and
              user ID of the adder: `fields=tracks.items(added_at,added_by.id)`. Use multiple
              parentheses to drill down into nested objects, for example:
              `fields=tracks.items(track(name,href,album(name,href)))`. Fields can be excluded
              by prefixing them with an exclamation mark, for example:
              `fields=tracks.items(track(name,href,album(!name,href)))`

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
        if not playlist_id:
            raise ValueError(f"Expected a non-empty value for `playlist_id` but received {playlist_id!r}")
        return self._get(
            path_template("/playlists/{playlist_id}", playlist_id=playlist_id),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "additional_types": additional_types,
                        "fields": fields,
                        "market": market,
                    },
                    playlist_retrieve_params.PlaylistRetrieveParams,
                ),
            ),
            cast_to=PlaylistRetrieveResponse,
        )

    def update(
        self,
        playlist_id: str,
        *,
        collaborative: bool | Omit = omit,
        description: str | Omit = omit,
        name: str | Omit = omit,
        published: bool | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> None:
        """Change a playlist's name and public/private state.

        (The user must, of course,
        own the playlist.)

        Args:
          playlist_id: The [Spotify ID](/documentation/web-api/concepts/spotify-uris-ids) of the
              playlist.

          collaborative: If `true`, the playlist will become collaborative and other users will be able
              to modify the playlist in their Spotify client. <br/> _**Note**: You can only
              set `collaborative` to `true` on non-public playlists._

          description: Value for playlist description as displayed in Spotify Clients and in the Web
              API.

          name: The new name for the playlist, for example `"My New Playlist Title"`

          published: The playlist's public/private status (if it should be added to the user's
              profile or not): `true` the playlist will be public, `false` the playlist will
              be private, `null` the playlist status is not relevant. For more about
              public/private status, see
              [Working with Playlists](/documentation/web-api/concepts/playlists)

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not playlist_id:
            raise ValueError(f"Expected a non-empty value for `playlist_id` but received {playlist_id!r}")
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return self._put(
            path_template("/playlists/{playlist_id}", playlist_id=playlist_id),
            body=maybe_transform(
                {
                    "collaborative": collaborative,
                    "description": description,
                    "name": name,
                    "published": published,
                },
                playlist_update_params.PlaylistUpdateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=NoneType,
        )


class AsyncPlaylistsResource(AsyncAPIResource):
    @cached_property
    def tracks(self) -> AsyncTracksResource:
        return AsyncTracksResource(self._client)

    @cached_property
    def followers(self) -> AsyncFollowersResource:
        return AsyncFollowersResource(self._client)

    @cached_property
    def images(self) -> AsyncImagesResource:
        return AsyncImagesResource(self._client)

    @cached_property
    def with_raw_response(self) -> AsyncPlaylistsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/cjavdev/spotted-py#accessing-raw-response-data-eg-headers
        """
        return AsyncPlaylistsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncPlaylistsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/cjavdev/spotted-py#with_streaming_response
        """
        return AsyncPlaylistsResourceWithStreamingResponse(self)

    async def retrieve(
        self,
        playlist_id: str,
        *,
        additional_types: str | Omit = omit,
        fields: str | Omit = omit,
        market: str | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> PlaylistRetrieveResponse:
        """
        Get a playlist owned by a Spotify user.

        Args:
          playlist_id: The [Spotify ID](/documentation/web-api/concepts/spotify-uris-ids) of the
              playlist.

          additional_types: A comma-separated list of item types that your client supports besides the
              default `track` type. Valid types are: `track` and `episode`.<br/> _**Note**:
              This parameter was introduced to allow existing clients to maintain their
              current behaviour and might be deprecated in the future._<br/> In addition to
              providing this parameter, make sure that your client properly handles cases of
              new types in the future by checking against the `type` field of each object.

          fields: Filters for the query: a comma-separated list of the fields to return. If
              omitted, all fields are returned. For example, to get just the playlist''s
              description and URI: `fields=description,uri`. A dot separator can be used to
              specify non-reoccurring fields, while parentheses can be used to specify
              reoccurring fields within objects. For example, to get just the added date and
              user ID of the adder: `fields=tracks.items(added_at,added_by.id)`. Use multiple
              parentheses to drill down into nested objects, for example:
              `fields=tracks.items(track(name,href,album(name,href)))`. Fields can be excluded
              by prefixing them with an exclamation mark, for example:
              `fields=tracks.items(track(name,href,album(!name,href)))`

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
        if not playlist_id:
            raise ValueError(f"Expected a non-empty value for `playlist_id` but received {playlist_id!r}")
        return await self._get(
            path_template("/playlists/{playlist_id}", playlist_id=playlist_id),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=await async_maybe_transform(
                    {
                        "additional_types": additional_types,
                        "fields": fields,
                        "market": market,
                    },
                    playlist_retrieve_params.PlaylistRetrieveParams,
                ),
            ),
            cast_to=PlaylistRetrieveResponse,
        )

    async def update(
        self,
        playlist_id: str,
        *,
        collaborative: bool | Omit = omit,
        description: str | Omit = omit,
        name: str | Omit = omit,
        published: bool | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> None:
        """Change a playlist's name and public/private state.

        (The user must, of course,
        own the playlist.)

        Args:
          playlist_id: The [Spotify ID](/documentation/web-api/concepts/spotify-uris-ids) of the
              playlist.

          collaborative: If `true`, the playlist will become collaborative and other users will be able
              to modify the playlist in their Spotify client. <br/> _**Note**: You can only
              set `collaborative` to `true` on non-public playlists._

          description: Value for playlist description as displayed in Spotify Clients and in the Web
              API.

          name: The new name for the playlist, for example `"My New Playlist Title"`

          published: The playlist's public/private status (if it should be added to the user's
              profile or not): `true` the playlist will be public, `false` the playlist will
              be private, `null` the playlist status is not relevant. For more about
              public/private status, see
              [Working with Playlists](/documentation/web-api/concepts/playlists)

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not playlist_id:
            raise ValueError(f"Expected a non-empty value for `playlist_id` but received {playlist_id!r}")
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return await self._put(
            path_template("/playlists/{playlist_id}", playlist_id=playlist_id),
            body=await async_maybe_transform(
                {
                    "collaborative": collaborative,
                    "description": description,
                    "name": name,
                    "published": published,
                },
                playlist_update_params.PlaylistUpdateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=NoneType,
        )


class PlaylistsResourceWithRawResponse:
    def __init__(self, playlists: PlaylistsResource) -> None:
        self._playlists = playlists

        self.retrieve = to_raw_response_wrapper(
            playlists.retrieve,
        )
        self.update = to_raw_response_wrapper(
            playlists.update,
        )

    @cached_property
    def tracks(self) -> TracksResourceWithRawResponse:
        return TracksResourceWithRawResponse(self._playlists.tracks)

    @cached_property
    def followers(self) -> FollowersResourceWithRawResponse:
        return FollowersResourceWithRawResponse(self._playlists.followers)

    @cached_property
    def images(self) -> ImagesResourceWithRawResponse:
        return ImagesResourceWithRawResponse(self._playlists.images)


class AsyncPlaylistsResourceWithRawResponse:
    def __init__(self, playlists: AsyncPlaylistsResource) -> None:
        self._playlists = playlists

        self.retrieve = async_to_raw_response_wrapper(
            playlists.retrieve,
        )
        self.update = async_to_raw_response_wrapper(
            playlists.update,
        )

    @cached_property
    def tracks(self) -> AsyncTracksResourceWithRawResponse:
        return AsyncTracksResourceWithRawResponse(self._playlists.tracks)

    @cached_property
    def followers(self) -> AsyncFollowersResourceWithRawResponse:
        return AsyncFollowersResourceWithRawResponse(self._playlists.followers)

    @cached_property
    def images(self) -> AsyncImagesResourceWithRawResponse:
        return AsyncImagesResourceWithRawResponse(self._playlists.images)


class PlaylistsResourceWithStreamingResponse:
    def __init__(self, playlists: PlaylistsResource) -> None:
        self._playlists = playlists

        self.retrieve = to_streamed_response_wrapper(
            playlists.retrieve,
        )
        self.update = to_streamed_response_wrapper(
            playlists.update,
        )

    @cached_property
    def tracks(self) -> TracksResourceWithStreamingResponse:
        return TracksResourceWithStreamingResponse(self._playlists.tracks)

    @cached_property
    def followers(self) -> FollowersResourceWithStreamingResponse:
        return FollowersResourceWithStreamingResponse(self._playlists.followers)

    @cached_property
    def images(self) -> ImagesResourceWithStreamingResponse:
        return ImagesResourceWithStreamingResponse(self._playlists.images)


class AsyncPlaylistsResourceWithStreamingResponse:
    def __init__(self, playlists: AsyncPlaylistsResource) -> None:
        self._playlists = playlists

        self.retrieve = async_to_streamed_response_wrapper(
            playlists.retrieve,
        )
        self.update = async_to_streamed_response_wrapper(
            playlists.update,
        )

    @cached_property
    def tracks(self) -> AsyncTracksResourceWithStreamingResponse:
        return AsyncTracksResourceWithStreamingResponse(self._playlists.tracks)

    @cached_property
    def followers(self) -> AsyncFollowersResourceWithStreamingResponse:
        return AsyncFollowersResourceWithStreamingResponse(self._playlists.followers)

    @cached_property
    def images(self) -> AsyncImagesResourceWithStreamingResponse:
        return AsyncImagesResourceWithStreamingResponse(self._playlists.images)
