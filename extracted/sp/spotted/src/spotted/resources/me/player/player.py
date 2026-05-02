# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Dict

import httpx

from .queue import (
    QueueResource,
    AsyncQueueResource,
    QueueResourceWithRawResponse,
    AsyncQueueResourceWithRawResponse,
    QueueResourceWithStreamingResponse,
    AsyncQueueResourceWithStreamingResponse,
)
from ...._types import Body, Omit, Query, Headers, NoneType, NotGiven, SequenceNotStr, omit, not_given
from ...._utils import maybe_transform, async_maybe_transform
from ...._compat import cached_property
from ....types.me import (
    player_transfer_params,
    player_get_state_params,
    player_skip_next_params,
    player_set_volume_params,
    player_skip_previous_params,
    player_pause_playback_params,
    player_start_playback_params,
    player_toggle_shuffle_params,
    player_set_repeat_mode_params,
    player_seek_to_position_params,
    player_list_recently_played_params,
    player_get_currently_playing_params,
)
from ...._resource import SyncAPIResource, AsyncAPIResource
from ...._response import (
    to_raw_response_wrapper,
    to_streamed_response_wrapper,
    async_to_raw_response_wrapper,
    async_to_streamed_response_wrapper,
)
from ....pagination import SyncCursorURLPage, AsyncCursorURLPage
from ...._base_client import AsyncPaginator, make_request_options
from ....types.me.player_get_state_response import PlayerGetStateResponse
from ....types.me.player_get_devices_response import PlayerGetDevicesResponse
from ....types.me.player_list_recently_played_response import PlayerListRecentlyPlayedResponse
from ....types.me.player_get_currently_playing_response import PlayerGetCurrentlyPlayingResponse

__all__ = ["PlayerResource", "AsyncPlayerResource"]


class PlayerResource(SyncAPIResource):
    @cached_property
    def queue(self) -> QueueResource:
        return QueueResource(self._client)

    @cached_property
    def with_raw_response(self) -> PlayerResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/cjavdev/spotted-py#accessing-raw-response-data-eg-headers
        """
        return PlayerResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> PlayerResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/cjavdev/spotted-py#with_streaming_response
        """
        return PlayerResourceWithStreamingResponse(self)

    def get_currently_playing(
        self,
        *,
        additional_types: str | Omit = omit,
        market: str | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> PlayerGetCurrentlyPlayingResponse:
        """
        Get the object currently being played on the user's Spotify account.

        Args:
          additional_types: A comma-separated list of item types that your client supports besides the
              default `track` type. Valid types are: `track` and `episode`.<br/> _**Note**:
              This parameter was introduced to allow existing clients to maintain their
              current behaviour and might be deprecated in the future._<br/> In addition to
              providing this parameter, make sure that your client properly handles cases of
              new types in the future by checking against the `type` field of each object.

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
        return self._get(
            "/me/player/currently-playing",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "additional_types": additional_types,
                        "market": market,
                    },
                    player_get_currently_playing_params.PlayerGetCurrentlyPlayingParams,
                ),
            ),
            cast_to=PlayerGetCurrentlyPlayingResponse,
        )

    def get_devices(
        self,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> PlayerGetDevicesResponse:
        """Get information about a user’s available Spotify Connect devices.

        Some device
        models are not supported and will not be listed in the API response.
        """
        return self._get(
            "/me/player/devices",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=PlayerGetDevicesResponse,
        )

    def get_state(
        self,
        *,
        additional_types: str | Omit = omit,
        market: str | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> PlayerGetStateResponse:
        """
        Get information about the user’s current playback state, including track or
        episode, progress, and active device.

        Args:
          additional_types: A comma-separated list of item types that your client supports besides the
              default `track` type. Valid types are: `track` and `episode`.<br/> _**Note**:
              This parameter was introduced to allow existing clients to maintain their
              current behaviour and might be deprecated in the future._<br/> In addition to
              providing this parameter, make sure that your client properly handles cases of
              new types in the future by checking against the `type` field of each object.

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
        return self._get(
            "/me/player",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "additional_types": additional_types,
                        "market": market,
                    },
                    player_get_state_params.PlayerGetStateParams,
                ),
            ),
            cast_to=PlayerGetStateResponse,
        )

    def list_recently_played(
        self,
        *,
        after: int | Omit = omit,
        before: int | Omit = omit,
        limit: int | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> SyncCursorURLPage[PlayerListRecentlyPlayedResponse]:
        """Get tracks from the current user's recently played tracks.

        _**Note**: Currently
        doesn't support podcast episodes._

        Args:
          after: A Unix timestamp in milliseconds. Returns all items after (but not including)
              this cursor position. If `after` is specified, `before` must not be specified.

          before: A Unix timestamp in milliseconds. Returns all items before (but not including)
              this cursor position. If `before` is specified, `after` must not be specified.

          limit: The maximum number of items to return. Default: 20. Minimum: 1. Maximum: 50.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._get_api_list(
            "/me/player/recently-played",
            page=SyncCursorURLPage[PlayerListRecentlyPlayedResponse],
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "after": after,
                        "before": before,
                        "limit": limit,
                    },
                    player_list_recently_played_params.PlayerListRecentlyPlayedParams,
                ),
            ),
            model=PlayerListRecentlyPlayedResponse,
        )

    def pause_playback(
        self,
        *,
        device_id: str | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> None:
        """Pause playback on the user's account.

        This API only works for users who have
        Spotify Premium. The order of execution is not guaranteed when you use this API
        with other Player API endpoints.

        Args:
          device_id: The id of the device this command is targeting. If not supplied, the user's
              currently active device is the target.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return self._put(
            "/me/player/pause",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform({"device_id": device_id}, player_pause_playback_params.PlayerPausePlaybackParams),
            ),
            cast_to=NoneType,
        )

    def seek_to_position(
        self,
        *,
        position_ms: int,
        device_id: str | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> None:
        """Seeks to the given position in the user’s currently playing track.

        This API only
        works for users who have Spotify Premium. The order of execution is not
        guaranteed when you use this API with other Player API endpoints.

        Args:
          position_ms: The position in milliseconds to seek to. Must be a positive number. Passing in a
              position that is greater than the length of the track will cause the player to
              start playing the next song.

          device_id: The id of the device this command is targeting. If not supplied, the user's
              currently active device is the target.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return self._put(
            "/me/player/seek",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "position_ms": position_ms,
                        "device_id": device_id,
                    },
                    player_seek_to_position_params.PlayerSeekToPositionParams,
                ),
            ),
            cast_to=NoneType,
        )

    def set_repeat_mode(
        self,
        *,
        state: str,
        device_id: str | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> None:
        """Set the repeat mode for the user's playback.

        This API only works for users who
        have Spotify Premium. The order of execution is not guaranteed when you use this
        API with other Player API endpoints.

        Args:
          state: **track**, **context** or **off**.<br/> **track** will repeat the current
              track.<br/> **context** will repeat the current context.<br/> **off** will turn
              repeat off.

          device_id: The id of the device this command is targeting. If not supplied, the user's
              currently active device is the target.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return self._put(
            "/me/player/repeat",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "state": state,
                        "device_id": device_id,
                    },
                    player_set_repeat_mode_params.PlayerSetRepeatModeParams,
                ),
            ),
            cast_to=NoneType,
        )

    def set_volume(
        self,
        *,
        volume_percent: int,
        device_id: str | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> None:
        """Set the volume for the user’s current playback device.

        This API only works for
        users who have Spotify Premium. The order of execution is not guaranteed when
        you use this API with other Player API endpoints.

        Args:
          volume_percent: The volume to set. Must be a value from 0 to 100 inclusive.

          device_id: The id of the device this command is targeting. If not supplied, the user's
              currently active device is the target.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return self._put(
            "/me/player/volume",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "volume_percent": volume_percent,
                        "device_id": device_id,
                    },
                    player_set_volume_params.PlayerSetVolumeParams,
                ),
            ),
            cast_to=NoneType,
        )

    def skip_next(
        self,
        *,
        device_id: str | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> None:
        """Skips to next track in the user’s queue.

        This API only works for users who have
        Spotify Premium. The order of execution is not guaranteed when you use this API
        with other Player API endpoints.

        Args:
          device_id: The id of the device this command is targeting. If not supplied, the user's
              currently active device is the target.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return self._post(
            "/me/player/next",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform({"device_id": device_id}, player_skip_next_params.PlayerSkipNextParams),
            ),
            cast_to=NoneType,
        )

    def skip_previous(
        self,
        *,
        device_id: str | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> None:
        """Skips to previous track in the user’s queue.

        This API only works for users who
        have Spotify Premium. The order of execution is not guaranteed when you use this
        API with other Player API endpoints.

        Args:
          device_id: The id of the device this command is targeting. If not supplied, the user's
              currently active device is the target.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return self._post(
            "/me/player/previous",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform({"device_id": device_id}, player_skip_previous_params.PlayerSkipPreviousParams),
            ),
            cast_to=NoneType,
        )

    def start_playback(
        self,
        *,
        device_id: str | Omit = omit,
        context_uri: str | Omit = omit,
        offset: Dict[str, object] | Omit = omit,
        position_ms: int | Omit = omit,
        published: bool | Omit = omit,
        uris: SequenceNotStr[str] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> None:
        """Start a new context or resume current playback on the user's active device.

        This
        API only works for users who have Spotify Premium. The order of execution is not
        guaranteed when you use this API with other Player API endpoints.

        Args:
          device_id: The id of the device this command is targeting. If not supplied, the user's
              currently active device is the target.

          context_uri: Optional. Spotify URI of the context to play. Valid contexts are albums, artists
              & playlists. `{context_uri:"spotify:album:1Je1IMUlBXcx1Fz0WE7oPT"}`

          offset: Optional. Indicates from where in the context playback should start. Only
              available when context_uri corresponds to an album or playlist object "position"
              is zero based and can’t be negative. Example: `"offset": {"position": 5}` "uri"
              is a string representing the uri of the item to start at. Example:
              `"offset": {"uri": "spotify:track:1301WleyT98MSxVHPZCA6M"}`

          position_ms: Indicates from what position to start playback. Must be a positive number.
              Passing in a position that is greater than the length of the track will cause
              the player to start playing the next song.

          published: The playlist's public/private status (if it should be added to the user's
              profile or not): `true` the playlist will be public, `false` the playlist will
              be private, `null` the playlist status is not relevant. For more about
              public/private status, see
              [Working with Playlists](/documentation/web-api/concepts/playlists)

          uris:
              Optional. A JSON array of the Spotify track URIs to play. For example:
              `{"uris": ["spotify:track:4iV5W9uYEdYUVa79Axb7Rh", "spotify:track:1301WleyT98MSxVHPZCA6M"]}`

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return self._put(
            "/me/player/play",
            body=maybe_transform(
                {
                    "context_uri": context_uri,
                    "offset": offset,
                    "position_ms": position_ms,
                    "published": published,
                    "uris": uris,
                },
                player_start_playback_params.PlayerStartPlaybackParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform({"device_id": device_id}, player_start_playback_params.PlayerStartPlaybackParams),
            ),
            cast_to=NoneType,
        )

    def toggle_shuffle(
        self,
        *,
        state: bool,
        device_id: str | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> None:
        """Toggle shuffle on or off for user’s playback.

        This API only works for users who
        have Spotify Premium. The order of execution is not guaranteed when you use this
        API with other Player API endpoints.

        Args:
          state: **true** : Shuffle user's playback.<br/> **false** : Do not shuffle user's
              playback.

          device_id: The id of the device this command is targeting. If not supplied, the user's
              currently active device is the target.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return self._put(
            "/me/player/shuffle",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "state": state,
                        "device_id": device_id,
                    },
                    player_toggle_shuffle_params.PlayerToggleShuffleParams,
                ),
            ),
            cast_to=NoneType,
        )

    def transfer(
        self,
        *,
        device_ids: SequenceNotStr[str],
        play: bool | Omit = omit,
        published: bool | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> None:
        """Transfer playback to a new device and optionally begin playback.

        This API only
        works for users who have Spotify Premium. The order of execution is not
        guaranteed when you use this API with other Player API endpoints.

        Args:
          device_ids: A JSON array containing the ID of the device on which playback should be
              started/transferred.<br/>For
              example:`{device_ids:["74ASZWbe4lXaubB36ztrGX"]}`<br/>_**Note**: Although an
              array is accepted, only a single device_id is currently supported. Supplying
              more than one will return `400 Bad Request`_

          play:
              **true**: ensure playback happens on new device.<br/>**false** or not provided:
              keep the current playback state.

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
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return self._put(
            "/me/player",
            body=maybe_transform(
                {
                    "device_ids": device_ids,
                    "play": play,
                    "published": published,
                },
                player_transfer_params.PlayerTransferParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=NoneType,
        )


class AsyncPlayerResource(AsyncAPIResource):
    @cached_property
    def queue(self) -> AsyncQueueResource:
        return AsyncQueueResource(self._client)

    @cached_property
    def with_raw_response(self) -> AsyncPlayerResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/cjavdev/spotted-py#accessing-raw-response-data-eg-headers
        """
        return AsyncPlayerResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncPlayerResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/cjavdev/spotted-py#with_streaming_response
        """
        return AsyncPlayerResourceWithStreamingResponse(self)

    async def get_currently_playing(
        self,
        *,
        additional_types: str | Omit = omit,
        market: str | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> PlayerGetCurrentlyPlayingResponse:
        """
        Get the object currently being played on the user's Spotify account.

        Args:
          additional_types: A comma-separated list of item types that your client supports besides the
              default `track` type. Valid types are: `track` and `episode`.<br/> _**Note**:
              This parameter was introduced to allow existing clients to maintain their
              current behaviour and might be deprecated in the future._<br/> In addition to
              providing this parameter, make sure that your client properly handles cases of
              new types in the future by checking against the `type` field of each object.

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
        return await self._get(
            "/me/player/currently-playing",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=await async_maybe_transform(
                    {
                        "additional_types": additional_types,
                        "market": market,
                    },
                    player_get_currently_playing_params.PlayerGetCurrentlyPlayingParams,
                ),
            ),
            cast_to=PlayerGetCurrentlyPlayingResponse,
        )

    async def get_devices(
        self,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> PlayerGetDevicesResponse:
        """Get information about a user’s available Spotify Connect devices.

        Some device
        models are not supported and will not be listed in the API response.
        """
        return await self._get(
            "/me/player/devices",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=PlayerGetDevicesResponse,
        )

    async def get_state(
        self,
        *,
        additional_types: str | Omit = omit,
        market: str | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> PlayerGetStateResponse:
        """
        Get information about the user’s current playback state, including track or
        episode, progress, and active device.

        Args:
          additional_types: A comma-separated list of item types that your client supports besides the
              default `track` type. Valid types are: `track` and `episode`.<br/> _**Note**:
              This parameter was introduced to allow existing clients to maintain their
              current behaviour and might be deprecated in the future._<br/> In addition to
              providing this parameter, make sure that your client properly handles cases of
              new types in the future by checking against the `type` field of each object.

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
        return await self._get(
            "/me/player",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=await async_maybe_transform(
                    {
                        "additional_types": additional_types,
                        "market": market,
                    },
                    player_get_state_params.PlayerGetStateParams,
                ),
            ),
            cast_to=PlayerGetStateResponse,
        )

    def list_recently_played(
        self,
        *,
        after: int | Omit = omit,
        before: int | Omit = omit,
        limit: int | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> AsyncPaginator[PlayerListRecentlyPlayedResponse, AsyncCursorURLPage[PlayerListRecentlyPlayedResponse]]:
        """Get tracks from the current user's recently played tracks.

        _**Note**: Currently
        doesn't support podcast episodes._

        Args:
          after: A Unix timestamp in milliseconds. Returns all items after (but not including)
              this cursor position. If `after` is specified, `before` must not be specified.

          before: A Unix timestamp in milliseconds. Returns all items before (but not including)
              this cursor position. If `before` is specified, `after` must not be specified.

          limit: The maximum number of items to return. Default: 20. Minimum: 1. Maximum: 50.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._get_api_list(
            "/me/player/recently-played",
            page=AsyncCursorURLPage[PlayerListRecentlyPlayedResponse],
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "after": after,
                        "before": before,
                        "limit": limit,
                    },
                    player_list_recently_played_params.PlayerListRecentlyPlayedParams,
                ),
            ),
            model=PlayerListRecentlyPlayedResponse,
        )

    async def pause_playback(
        self,
        *,
        device_id: str | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> None:
        """Pause playback on the user's account.

        This API only works for users who have
        Spotify Premium. The order of execution is not guaranteed when you use this API
        with other Player API endpoints.

        Args:
          device_id: The id of the device this command is targeting. If not supplied, the user's
              currently active device is the target.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return await self._put(
            "/me/player/pause",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=await async_maybe_transform(
                    {"device_id": device_id}, player_pause_playback_params.PlayerPausePlaybackParams
                ),
            ),
            cast_to=NoneType,
        )

    async def seek_to_position(
        self,
        *,
        position_ms: int,
        device_id: str | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> None:
        """Seeks to the given position in the user’s currently playing track.

        This API only
        works for users who have Spotify Premium. The order of execution is not
        guaranteed when you use this API with other Player API endpoints.

        Args:
          position_ms: The position in milliseconds to seek to. Must be a positive number. Passing in a
              position that is greater than the length of the track will cause the player to
              start playing the next song.

          device_id: The id of the device this command is targeting. If not supplied, the user's
              currently active device is the target.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return await self._put(
            "/me/player/seek",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=await async_maybe_transform(
                    {
                        "position_ms": position_ms,
                        "device_id": device_id,
                    },
                    player_seek_to_position_params.PlayerSeekToPositionParams,
                ),
            ),
            cast_to=NoneType,
        )

    async def set_repeat_mode(
        self,
        *,
        state: str,
        device_id: str | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> None:
        """Set the repeat mode for the user's playback.

        This API only works for users who
        have Spotify Premium. The order of execution is not guaranteed when you use this
        API with other Player API endpoints.

        Args:
          state: **track**, **context** or **off**.<br/> **track** will repeat the current
              track.<br/> **context** will repeat the current context.<br/> **off** will turn
              repeat off.

          device_id: The id of the device this command is targeting. If not supplied, the user's
              currently active device is the target.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return await self._put(
            "/me/player/repeat",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=await async_maybe_transform(
                    {
                        "state": state,
                        "device_id": device_id,
                    },
                    player_set_repeat_mode_params.PlayerSetRepeatModeParams,
                ),
            ),
            cast_to=NoneType,
        )

    async def set_volume(
        self,
        *,
        volume_percent: int,
        device_id: str | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> None:
        """Set the volume for the user’s current playback device.

        This API only works for
        users who have Spotify Premium. The order of execution is not guaranteed when
        you use this API with other Player API endpoints.

        Args:
          volume_percent: The volume to set. Must be a value from 0 to 100 inclusive.

          device_id: The id of the device this command is targeting. If not supplied, the user's
              currently active device is the target.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return await self._put(
            "/me/player/volume",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=await async_maybe_transform(
                    {
                        "volume_percent": volume_percent,
                        "device_id": device_id,
                    },
                    player_set_volume_params.PlayerSetVolumeParams,
                ),
            ),
            cast_to=NoneType,
        )

    async def skip_next(
        self,
        *,
        device_id: str | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> None:
        """Skips to next track in the user’s queue.

        This API only works for users who have
        Spotify Premium. The order of execution is not guaranteed when you use this API
        with other Player API endpoints.

        Args:
          device_id: The id of the device this command is targeting. If not supplied, the user's
              currently active device is the target.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return await self._post(
            "/me/player/next",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=await async_maybe_transform(
                    {"device_id": device_id}, player_skip_next_params.PlayerSkipNextParams
                ),
            ),
            cast_to=NoneType,
        )

    async def skip_previous(
        self,
        *,
        device_id: str | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> None:
        """Skips to previous track in the user’s queue.

        This API only works for users who
        have Spotify Premium. The order of execution is not guaranteed when you use this
        API with other Player API endpoints.

        Args:
          device_id: The id of the device this command is targeting. If not supplied, the user's
              currently active device is the target.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return await self._post(
            "/me/player/previous",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=await async_maybe_transform(
                    {"device_id": device_id}, player_skip_previous_params.PlayerSkipPreviousParams
                ),
            ),
            cast_to=NoneType,
        )

    async def start_playback(
        self,
        *,
        device_id: str | Omit = omit,
        context_uri: str | Omit = omit,
        offset: Dict[str, object] | Omit = omit,
        position_ms: int | Omit = omit,
        published: bool | Omit = omit,
        uris: SequenceNotStr[str] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> None:
        """Start a new context or resume current playback on the user's active device.

        This
        API only works for users who have Spotify Premium. The order of execution is not
        guaranteed when you use this API with other Player API endpoints.

        Args:
          device_id: The id of the device this command is targeting. If not supplied, the user's
              currently active device is the target.

          context_uri: Optional. Spotify URI of the context to play. Valid contexts are albums, artists
              & playlists. `{context_uri:"spotify:album:1Je1IMUlBXcx1Fz0WE7oPT"}`

          offset: Optional. Indicates from where in the context playback should start. Only
              available when context_uri corresponds to an album or playlist object "position"
              is zero based and can’t be negative. Example: `"offset": {"position": 5}` "uri"
              is a string representing the uri of the item to start at. Example:
              `"offset": {"uri": "spotify:track:1301WleyT98MSxVHPZCA6M"}`

          position_ms: Indicates from what position to start playback. Must be a positive number.
              Passing in a position that is greater than the length of the track will cause
              the player to start playing the next song.

          published: The playlist's public/private status (if it should be added to the user's
              profile or not): `true` the playlist will be public, `false` the playlist will
              be private, `null` the playlist status is not relevant. For more about
              public/private status, see
              [Working with Playlists](/documentation/web-api/concepts/playlists)

          uris:
              Optional. A JSON array of the Spotify track URIs to play. For example:
              `{"uris": ["spotify:track:4iV5W9uYEdYUVa79Axb7Rh", "spotify:track:1301WleyT98MSxVHPZCA6M"]}`

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return await self._put(
            "/me/player/play",
            body=await async_maybe_transform(
                {
                    "context_uri": context_uri,
                    "offset": offset,
                    "position_ms": position_ms,
                    "published": published,
                    "uris": uris,
                },
                player_start_playback_params.PlayerStartPlaybackParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=await async_maybe_transform(
                    {"device_id": device_id}, player_start_playback_params.PlayerStartPlaybackParams
                ),
            ),
            cast_to=NoneType,
        )

    async def toggle_shuffle(
        self,
        *,
        state: bool,
        device_id: str | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> None:
        """Toggle shuffle on or off for user’s playback.

        This API only works for users who
        have Spotify Premium. The order of execution is not guaranteed when you use this
        API with other Player API endpoints.

        Args:
          state: **true** : Shuffle user's playback.<br/> **false** : Do not shuffle user's
              playback.

          device_id: The id of the device this command is targeting. If not supplied, the user's
              currently active device is the target.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return await self._put(
            "/me/player/shuffle",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=await async_maybe_transform(
                    {
                        "state": state,
                        "device_id": device_id,
                    },
                    player_toggle_shuffle_params.PlayerToggleShuffleParams,
                ),
            ),
            cast_to=NoneType,
        )

    async def transfer(
        self,
        *,
        device_ids: SequenceNotStr[str],
        play: bool | Omit = omit,
        published: bool | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> None:
        """Transfer playback to a new device and optionally begin playback.

        This API only
        works for users who have Spotify Premium. The order of execution is not
        guaranteed when you use this API with other Player API endpoints.

        Args:
          device_ids: A JSON array containing the ID of the device on which playback should be
              started/transferred.<br/>For
              example:`{device_ids:["74ASZWbe4lXaubB36ztrGX"]}`<br/>_**Note**: Although an
              array is accepted, only a single device_id is currently supported. Supplying
              more than one will return `400 Bad Request`_

          play:
              **true**: ensure playback happens on new device.<br/>**false** or not provided:
              keep the current playback state.

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
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return await self._put(
            "/me/player",
            body=await async_maybe_transform(
                {
                    "device_ids": device_ids,
                    "play": play,
                    "published": published,
                },
                player_transfer_params.PlayerTransferParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=NoneType,
        )


class PlayerResourceWithRawResponse:
    def __init__(self, player: PlayerResource) -> None:
        self._player = player

        self.get_currently_playing = to_raw_response_wrapper(
            player.get_currently_playing,
        )
        self.get_devices = to_raw_response_wrapper(
            player.get_devices,
        )
        self.get_state = to_raw_response_wrapper(
            player.get_state,
        )
        self.list_recently_played = to_raw_response_wrapper(
            player.list_recently_played,
        )
        self.pause_playback = to_raw_response_wrapper(
            player.pause_playback,
        )
        self.seek_to_position = to_raw_response_wrapper(
            player.seek_to_position,
        )
        self.set_repeat_mode = to_raw_response_wrapper(
            player.set_repeat_mode,
        )
        self.set_volume = to_raw_response_wrapper(
            player.set_volume,
        )
        self.skip_next = to_raw_response_wrapper(
            player.skip_next,
        )
        self.skip_previous = to_raw_response_wrapper(
            player.skip_previous,
        )
        self.start_playback = to_raw_response_wrapper(
            player.start_playback,
        )
        self.toggle_shuffle = to_raw_response_wrapper(
            player.toggle_shuffle,
        )
        self.transfer = to_raw_response_wrapper(
            player.transfer,
        )

    @cached_property
    def queue(self) -> QueueResourceWithRawResponse:
        return QueueResourceWithRawResponse(self._player.queue)


class AsyncPlayerResourceWithRawResponse:
    def __init__(self, player: AsyncPlayerResource) -> None:
        self._player = player

        self.get_currently_playing = async_to_raw_response_wrapper(
            player.get_currently_playing,
        )
        self.get_devices = async_to_raw_response_wrapper(
            player.get_devices,
        )
        self.get_state = async_to_raw_response_wrapper(
            player.get_state,
        )
        self.list_recently_played = async_to_raw_response_wrapper(
            player.list_recently_played,
        )
        self.pause_playback = async_to_raw_response_wrapper(
            player.pause_playback,
        )
        self.seek_to_position = async_to_raw_response_wrapper(
            player.seek_to_position,
        )
        self.set_repeat_mode = async_to_raw_response_wrapper(
            player.set_repeat_mode,
        )
        self.set_volume = async_to_raw_response_wrapper(
            player.set_volume,
        )
        self.skip_next = async_to_raw_response_wrapper(
            player.skip_next,
        )
        self.skip_previous = async_to_raw_response_wrapper(
            player.skip_previous,
        )
        self.start_playback = async_to_raw_response_wrapper(
            player.start_playback,
        )
        self.toggle_shuffle = async_to_raw_response_wrapper(
            player.toggle_shuffle,
        )
        self.transfer = async_to_raw_response_wrapper(
            player.transfer,
        )

    @cached_property
    def queue(self) -> AsyncQueueResourceWithRawResponse:
        return AsyncQueueResourceWithRawResponse(self._player.queue)


class PlayerResourceWithStreamingResponse:
    def __init__(self, player: PlayerResource) -> None:
        self._player = player

        self.get_currently_playing = to_streamed_response_wrapper(
            player.get_currently_playing,
        )
        self.get_devices = to_streamed_response_wrapper(
            player.get_devices,
        )
        self.get_state = to_streamed_response_wrapper(
            player.get_state,
        )
        self.list_recently_played = to_streamed_response_wrapper(
            player.list_recently_played,
        )
        self.pause_playback = to_streamed_response_wrapper(
            player.pause_playback,
        )
        self.seek_to_position = to_streamed_response_wrapper(
            player.seek_to_position,
        )
        self.set_repeat_mode = to_streamed_response_wrapper(
            player.set_repeat_mode,
        )
        self.set_volume = to_streamed_response_wrapper(
            player.set_volume,
        )
        self.skip_next = to_streamed_response_wrapper(
            player.skip_next,
        )
        self.skip_previous = to_streamed_response_wrapper(
            player.skip_previous,
        )
        self.start_playback = to_streamed_response_wrapper(
            player.start_playback,
        )
        self.toggle_shuffle = to_streamed_response_wrapper(
            player.toggle_shuffle,
        )
        self.transfer = to_streamed_response_wrapper(
            player.transfer,
        )

    @cached_property
    def queue(self) -> QueueResourceWithStreamingResponse:
        return QueueResourceWithStreamingResponse(self._player.queue)


class AsyncPlayerResourceWithStreamingResponse:
    def __init__(self, player: AsyncPlayerResource) -> None:
        self._player = player

        self.get_currently_playing = async_to_streamed_response_wrapper(
            player.get_currently_playing,
        )
        self.get_devices = async_to_streamed_response_wrapper(
            player.get_devices,
        )
        self.get_state = async_to_streamed_response_wrapper(
            player.get_state,
        )
        self.list_recently_played = async_to_streamed_response_wrapper(
            player.list_recently_played,
        )
        self.pause_playback = async_to_streamed_response_wrapper(
            player.pause_playback,
        )
        self.seek_to_position = async_to_streamed_response_wrapper(
            player.seek_to_position,
        )
        self.set_repeat_mode = async_to_streamed_response_wrapper(
            player.set_repeat_mode,
        )
        self.set_volume = async_to_streamed_response_wrapper(
            player.set_volume,
        )
        self.skip_next = async_to_streamed_response_wrapper(
            player.skip_next,
        )
        self.skip_previous = async_to_streamed_response_wrapper(
            player.skip_previous,
        )
        self.start_playback = async_to_streamed_response_wrapper(
            player.start_playback,
        )
        self.toggle_shuffle = async_to_streamed_response_wrapper(
            player.toggle_shuffle,
        )
        self.transfer = async_to_streamed_response_wrapper(
            player.transfer,
        )

    @cached_property
    def queue(self) -> AsyncQueueResourceWithStreamingResponse:
        return AsyncQueueResourceWithStreamingResponse(self._player.queue)
