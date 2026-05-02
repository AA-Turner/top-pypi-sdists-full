# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import httpx

from .top import (
    TopResource,
    AsyncTopResource,
    TopResourceWithRawResponse,
    AsyncTopResourceWithRawResponse,
    TopResourceWithStreamingResponse,
    AsyncTopResourceWithStreamingResponse,
)
from .shows import (
    ShowsResource,
    AsyncShowsResource,
    ShowsResourceWithRawResponse,
    AsyncShowsResourceWithRawResponse,
    ShowsResourceWithStreamingResponse,
    AsyncShowsResourceWithStreamingResponse,
)
from .albums import (
    AlbumsResource,
    AsyncAlbumsResource,
    AlbumsResourceWithRawResponse,
    AsyncAlbumsResourceWithRawResponse,
    AlbumsResourceWithStreamingResponse,
    AsyncAlbumsResourceWithStreamingResponse,
)
from .tracks import (
    TracksResource,
    AsyncTracksResource,
    TracksResourceWithRawResponse,
    AsyncTracksResourceWithRawResponse,
    TracksResourceWithStreamingResponse,
    AsyncTracksResourceWithStreamingResponse,
)
from ..._types import Body, Query, Headers, NotGiven, not_given
from .episodes import (
    EpisodesResource,
    AsyncEpisodesResource,
    EpisodesResourceWithRawResponse,
    AsyncEpisodesResourceWithRawResponse,
    EpisodesResourceWithStreamingResponse,
    AsyncEpisodesResourceWithStreamingResponse,
)
from ..._compat import cached_property
from .following import (
    FollowingResource,
    AsyncFollowingResource,
    FollowingResourceWithRawResponse,
    AsyncFollowingResourceWithRawResponse,
    FollowingResourceWithStreamingResponse,
    AsyncFollowingResourceWithStreamingResponse,
)
from .playlists import (
    PlaylistsResource,
    AsyncPlaylistsResource,
    PlaylistsResourceWithRawResponse,
    AsyncPlaylistsResourceWithRawResponse,
    PlaylistsResourceWithStreamingResponse,
    AsyncPlaylistsResourceWithStreamingResponse,
)
from .audiobooks import (
    AudiobooksResource,
    AsyncAudiobooksResource,
    AudiobooksResourceWithRawResponse,
    AsyncAudiobooksResourceWithRawResponse,
    AudiobooksResourceWithStreamingResponse,
    AsyncAudiobooksResourceWithStreamingResponse,
)
from ..._resource import SyncAPIResource, AsyncAPIResource
from ..._response import (
    to_raw_response_wrapper,
    to_streamed_response_wrapper,
    async_to_raw_response_wrapper,
    async_to_streamed_response_wrapper,
)
from .player.player import (
    PlayerResource,
    AsyncPlayerResource,
    PlayerResourceWithRawResponse,
    AsyncPlayerResourceWithRawResponse,
    PlayerResourceWithStreamingResponse,
    AsyncPlayerResourceWithStreamingResponse,
)
from ..._base_client import make_request_options
from ...types.me_retrieve_response import MeRetrieveResponse

__all__ = ["MeResource", "AsyncMeResource"]


class MeResource(SyncAPIResource):
    @cached_property
    def audiobooks(self) -> AudiobooksResource:
        return AudiobooksResource(self._client)

    @cached_property
    def playlists(self) -> PlaylistsResource:
        return PlaylistsResource(self._client)

    @cached_property
    def top(self) -> TopResource:
        return TopResource(self._client)

    @cached_property
    def albums(self) -> AlbumsResource:
        return AlbumsResource(self._client)

    @cached_property
    def tracks(self) -> TracksResource:
        return TracksResource(self._client)

    @cached_property
    def episodes(self) -> EpisodesResource:
        return EpisodesResource(self._client)

    @cached_property
    def shows(self) -> ShowsResource:
        return ShowsResource(self._client)

    @cached_property
    def following(self) -> FollowingResource:
        return FollowingResource(self._client)

    @cached_property
    def player(self) -> PlayerResource:
        return PlayerResource(self._client)

    @cached_property
    def with_raw_response(self) -> MeResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/cjavdev/spotted-py#accessing-raw-response-data-eg-headers
        """
        return MeResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> MeResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/cjavdev/spotted-py#with_streaming_response
        """
        return MeResourceWithStreamingResponse(self)

    def retrieve(
        self,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> MeRetrieveResponse:
        """
        Get detailed profile information about the current user (including the current
        user's username).
        """
        return self._get(
            "/me",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=MeRetrieveResponse,
        )


class AsyncMeResource(AsyncAPIResource):
    @cached_property
    def audiobooks(self) -> AsyncAudiobooksResource:
        return AsyncAudiobooksResource(self._client)

    @cached_property
    def playlists(self) -> AsyncPlaylistsResource:
        return AsyncPlaylistsResource(self._client)

    @cached_property
    def top(self) -> AsyncTopResource:
        return AsyncTopResource(self._client)

    @cached_property
    def albums(self) -> AsyncAlbumsResource:
        return AsyncAlbumsResource(self._client)

    @cached_property
    def tracks(self) -> AsyncTracksResource:
        return AsyncTracksResource(self._client)

    @cached_property
    def episodes(self) -> AsyncEpisodesResource:
        return AsyncEpisodesResource(self._client)

    @cached_property
    def shows(self) -> AsyncShowsResource:
        return AsyncShowsResource(self._client)

    @cached_property
    def following(self) -> AsyncFollowingResource:
        return AsyncFollowingResource(self._client)

    @cached_property
    def player(self) -> AsyncPlayerResource:
        return AsyncPlayerResource(self._client)

    @cached_property
    def with_raw_response(self) -> AsyncMeResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/cjavdev/spotted-py#accessing-raw-response-data-eg-headers
        """
        return AsyncMeResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncMeResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/cjavdev/spotted-py#with_streaming_response
        """
        return AsyncMeResourceWithStreamingResponse(self)

    async def retrieve(
        self,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> MeRetrieveResponse:
        """
        Get detailed profile information about the current user (including the current
        user's username).
        """
        return await self._get(
            "/me",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=MeRetrieveResponse,
        )


class MeResourceWithRawResponse:
    def __init__(self, me: MeResource) -> None:
        self._me = me

        self.retrieve = to_raw_response_wrapper(
            me.retrieve,
        )

    @cached_property
    def audiobooks(self) -> AudiobooksResourceWithRawResponse:
        return AudiobooksResourceWithRawResponse(self._me.audiobooks)

    @cached_property
    def playlists(self) -> PlaylistsResourceWithRawResponse:
        return PlaylistsResourceWithRawResponse(self._me.playlists)

    @cached_property
    def top(self) -> TopResourceWithRawResponse:
        return TopResourceWithRawResponse(self._me.top)

    @cached_property
    def albums(self) -> AlbumsResourceWithRawResponse:
        return AlbumsResourceWithRawResponse(self._me.albums)

    @cached_property
    def tracks(self) -> TracksResourceWithRawResponse:
        return TracksResourceWithRawResponse(self._me.tracks)

    @cached_property
    def episodes(self) -> EpisodesResourceWithRawResponse:
        return EpisodesResourceWithRawResponse(self._me.episodes)

    @cached_property
    def shows(self) -> ShowsResourceWithRawResponse:
        return ShowsResourceWithRawResponse(self._me.shows)

    @cached_property
    def following(self) -> FollowingResourceWithRawResponse:
        return FollowingResourceWithRawResponse(self._me.following)

    @cached_property
    def player(self) -> PlayerResourceWithRawResponse:
        return PlayerResourceWithRawResponse(self._me.player)


class AsyncMeResourceWithRawResponse:
    def __init__(self, me: AsyncMeResource) -> None:
        self._me = me

        self.retrieve = async_to_raw_response_wrapper(
            me.retrieve,
        )

    @cached_property
    def audiobooks(self) -> AsyncAudiobooksResourceWithRawResponse:
        return AsyncAudiobooksResourceWithRawResponse(self._me.audiobooks)

    @cached_property
    def playlists(self) -> AsyncPlaylistsResourceWithRawResponse:
        return AsyncPlaylistsResourceWithRawResponse(self._me.playlists)

    @cached_property
    def top(self) -> AsyncTopResourceWithRawResponse:
        return AsyncTopResourceWithRawResponse(self._me.top)

    @cached_property
    def albums(self) -> AsyncAlbumsResourceWithRawResponse:
        return AsyncAlbumsResourceWithRawResponse(self._me.albums)

    @cached_property
    def tracks(self) -> AsyncTracksResourceWithRawResponse:
        return AsyncTracksResourceWithRawResponse(self._me.tracks)

    @cached_property
    def episodes(self) -> AsyncEpisodesResourceWithRawResponse:
        return AsyncEpisodesResourceWithRawResponse(self._me.episodes)

    @cached_property
    def shows(self) -> AsyncShowsResourceWithRawResponse:
        return AsyncShowsResourceWithRawResponse(self._me.shows)

    @cached_property
    def following(self) -> AsyncFollowingResourceWithRawResponse:
        return AsyncFollowingResourceWithRawResponse(self._me.following)

    @cached_property
    def player(self) -> AsyncPlayerResourceWithRawResponse:
        return AsyncPlayerResourceWithRawResponse(self._me.player)


class MeResourceWithStreamingResponse:
    def __init__(self, me: MeResource) -> None:
        self._me = me

        self.retrieve = to_streamed_response_wrapper(
            me.retrieve,
        )

    @cached_property
    def audiobooks(self) -> AudiobooksResourceWithStreamingResponse:
        return AudiobooksResourceWithStreamingResponse(self._me.audiobooks)

    @cached_property
    def playlists(self) -> PlaylistsResourceWithStreamingResponse:
        return PlaylistsResourceWithStreamingResponse(self._me.playlists)

    @cached_property
    def top(self) -> TopResourceWithStreamingResponse:
        return TopResourceWithStreamingResponse(self._me.top)

    @cached_property
    def albums(self) -> AlbumsResourceWithStreamingResponse:
        return AlbumsResourceWithStreamingResponse(self._me.albums)

    @cached_property
    def tracks(self) -> TracksResourceWithStreamingResponse:
        return TracksResourceWithStreamingResponse(self._me.tracks)

    @cached_property
    def episodes(self) -> EpisodesResourceWithStreamingResponse:
        return EpisodesResourceWithStreamingResponse(self._me.episodes)

    @cached_property
    def shows(self) -> ShowsResourceWithStreamingResponse:
        return ShowsResourceWithStreamingResponse(self._me.shows)

    @cached_property
    def following(self) -> FollowingResourceWithStreamingResponse:
        return FollowingResourceWithStreamingResponse(self._me.following)

    @cached_property
    def player(self) -> PlayerResourceWithStreamingResponse:
        return PlayerResourceWithStreamingResponse(self._me.player)


class AsyncMeResourceWithStreamingResponse:
    def __init__(self, me: AsyncMeResource) -> None:
        self._me = me

        self.retrieve = async_to_streamed_response_wrapper(
            me.retrieve,
        )

    @cached_property
    def audiobooks(self) -> AsyncAudiobooksResourceWithStreamingResponse:
        return AsyncAudiobooksResourceWithStreamingResponse(self._me.audiobooks)

    @cached_property
    def playlists(self) -> AsyncPlaylistsResourceWithStreamingResponse:
        return AsyncPlaylistsResourceWithStreamingResponse(self._me.playlists)

    @cached_property
    def top(self) -> AsyncTopResourceWithStreamingResponse:
        return AsyncTopResourceWithStreamingResponse(self._me.top)

    @cached_property
    def albums(self) -> AsyncAlbumsResourceWithStreamingResponse:
        return AsyncAlbumsResourceWithStreamingResponse(self._me.albums)

    @cached_property
    def tracks(self) -> AsyncTracksResourceWithStreamingResponse:
        return AsyncTracksResourceWithStreamingResponse(self._me.tracks)

    @cached_property
    def episodes(self) -> AsyncEpisodesResourceWithStreamingResponse:
        return AsyncEpisodesResourceWithStreamingResponse(self._me.episodes)

    @cached_property
    def shows(self) -> AsyncShowsResourceWithStreamingResponse:
        return AsyncShowsResourceWithStreamingResponse(self._me.shows)

    @cached_property
    def following(self) -> AsyncFollowingResourceWithStreamingResponse:
        return AsyncFollowingResourceWithStreamingResponse(self._me.following)

    @cached_property
    def player(self) -> AsyncPlayerResourceWithStreamingResponse:
        return AsyncPlayerResourceWithStreamingResponse(self._me.player)
