# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import typing_extensions
from typing import Iterable

import httpx

from ..._types import Body, Omit, Query, Headers, NotGiven, SequenceNotStr, omit, not_given
from ..._utils import path_template, maybe_transform, async_maybe_transform
from ..._compat import cached_property
from ..._resource import SyncAPIResource, AsyncAPIResource
from ..._response import (
    to_raw_response_wrapper,
    to_streamed_response_wrapper,
    async_to_raw_response_wrapper,
    async_to_streamed_response_wrapper,
)
from ...pagination import SyncCursorURLPage, AsyncCursorURLPage
from ..._base_client import AsyncPaginator, make_request_options
from ...types.playlists import track_add_params, track_list_params, track_remove_params, track_update_params
from ...types.playlists.track_add_response import TrackAddResponse
from ...types.shared.playlist_track_object import PlaylistTrackObject
from ...types.playlists.track_remove_response import TrackRemoveResponse
from ...types.playlists.track_update_response import TrackUpdateResponse

__all__ = ["TracksResource", "AsyncTracksResource"]


class TracksResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> TracksResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/cjavdev/spotted-py#accessing-raw-response-data-eg-headers
        """
        return TracksResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> TracksResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/cjavdev/spotted-py#with_streaming_response
        """
        return TracksResourceWithStreamingResponse(self)

    @typing_extensions.deprecated("deprecated")
    def update(
        self,
        playlist_id: str,
        *,
        insert_before: int | Omit = omit,
        published: bool | Omit = omit,
        range_length: int | Omit = omit,
        range_start: int | Omit = omit,
        snapshot_id: str | Omit = omit,
        uris: SequenceNotStr[str] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> TrackUpdateResponse:
        """
        **Deprecated:** Use
        [Update Playlist Items](/documentation/web-api/reference/reorder-or-replace-playlists-items)
        instead.

        Either reorder or replace items in a playlist depending on the request's
        parameters. To reorder items, include `range_start`, `insert_before`,
        `range_length` and `snapshot_id` in the request's body. To replace items,
        include `uris` as either a query parameter or in the request's body. Replacing
        items in a playlist will overwrite its existing items. This operation can be
        used for replacing or clearing items in a playlist. <br/> **Note**: Replace and
        reorder are mutually exclusive operations which share the same endpoint, but
        have different parameters. These operations can't be applied together in a
        single request.

        Args:
          playlist_id: The [Spotify ID](/documentation/web-api/concepts/spotify-uris-ids) of the
              playlist.

          insert_before: The position where the items should be inserted.<br/>To reorder the items to the
              end of the playlist, simply set _insert_before_ to the position after the last
              item.<br/>Examples:<br/>To reorder the first item to the last position in a
              playlist with 10 items, set _range_start_ to 0, and _insert_before_
              to 10.<br/>To reorder the last item in a playlist with 10 items to the start of
              the playlist, set _range_start_ to 9, and _insert_before_ to 0.

          published: The playlist's public/private status (if it should be added to the user's
              profile or not): `true` the playlist will be public, `false` the playlist will
              be private, `null` the playlist status is not relevant. For more about
              public/private status, see
              [Working with Playlists](/documentation/web-api/concepts/playlists)

          range_length: The amount of items to be reordered. Defaults to 1 if not set.<br/>The range of
              items to be reordered begins from the _range_start_ position, and includes the
              _range_length_ subsequent items.<br/>Example:<br/>To move the items at index
              9-10 to the start of the playlist, _range_start_ is set to 9, and _range_length_
              is set to 2.

          range_start: The position of the first item to be reordered.

          snapshot_id: The playlist's snapshot ID against which you want to make the changes.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not playlist_id:
            raise ValueError(f"Expected a non-empty value for `playlist_id` but received {playlist_id!r}")
        return self._put(
            path_template("/playlists/{playlist_id}/tracks", playlist_id=playlist_id),
            body=maybe_transform(
                {
                    "insert_before": insert_before,
                    "published": published,
                    "range_length": range_length,
                    "range_start": range_start,
                    "snapshot_id": snapshot_id,
                    "uris": uris,
                },
                track_update_params.TrackUpdateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=TrackUpdateResponse,
        )

    @typing_extensions.deprecated("deprecated")
    def list(
        self,
        playlist_id: str,
        *,
        additional_types: str | Omit = omit,
        fields: str | Omit = omit,
        limit: int | Omit = omit,
        market: str | Omit = omit,
        offset: int | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> SyncCursorURLPage[PlaylistTrackObject]:
        """
        **Deprecated:** Use
        [Get Playlist Items](/documentation/web-api/reference/get-playlists-items)
        instead.

        Get full details of the items of a playlist owned by a Spotify user.

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
              omitted, all fields are returned. For example, to get just the total number of
              items and the request limit:<br/>`fields=total,limit`<br/>A dot separator can be
              used to specify non-reoccurring fields, while parentheses can be used to specify
              reoccurring fields within objects. For example, to get just the added date and
              user ID of the adder:<br/>`fields=items(added_at,added_by.id)`<br/>Use multiple
              parentheses to drill down into nested objects, for
              example:<br/>`fields=items(track(name,href,album(name,href)))`<br/>Fields can be
              excluded by prefixing them with an exclamation mark, for
              example:<br/>`fields=items.track.album(!external_urls,images)`

          limit: The maximum number of items to return. Default: 20. Minimum: 1. Maximum: 100.

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
        if not playlist_id:
            raise ValueError(f"Expected a non-empty value for `playlist_id` but received {playlist_id!r}")
        return self._get_api_list(
            path_template("/playlists/{playlist_id}/tracks", playlist_id=playlist_id),
            page=SyncCursorURLPage[PlaylistTrackObject],
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "additional_types": additional_types,
                        "fields": fields,
                        "limit": limit,
                        "market": market,
                        "offset": offset,
                    },
                    track_list_params.TrackListParams,
                ),
            ),
            model=PlaylistTrackObject,
        )

    @typing_extensions.deprecated("deprecated")
    def add(
        self,
        playlist_id: str,
        *,
        position: int | Omit = omit,
        published: bool | Omit = omit,
        uris: SequenceNotStr[str] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> TrackAddResponse:
        """
        **Deprecated:** Use
        [Add Items to Playlist](/documentation/web-api/reference/add-items-to-playlist)
        instead.

        Add one or more items to a user's playlist.

        Args:
          playlist_id: The [Spotify ID](/documentation/web-api/concepts/spotify-uris-ids) of the
              playlist.

          position: The position to insert the items, a zero-based index. For example, to insert the
              items in the first position: `position=0` ; to insert the items in the third
              position: `position=2`. If omitted, the items will be appended to the playlist.
              Items are added in the order they appear in the uris array. For example:
              `{"uris": ["spotify:track:4iV5W9uYEdYUVa79Axb7Rh","spotify:track:1301WleyT98MSxVHPZCA6M"], "position": 3}`

          published: The playlist's public/private status (if it should be added to the user's
              profile or not): `true` the playlist will be public, `false` the playlist will
              be private, `null` the playlist status is not relevant. For more about
              public/private status, see
              [Working with Playlists](/documentation/web-api/concepts/playlists)

          uris: A JSON array of the
              [Spotify URIs](/documentation/web-api/concepts/spotify-uris-ids) to add. For
              example:
              `{"uris": ["spotify:track:4iV5W9uYEdYUVa79Axb7Rh","spotify:track:1301WleyT98MSxVHPZCA6M", "spotify:episode:512ojhOuo1ktJprKbVcKyQ"]}`<br/>A
              maximum of 100 items can be added in one request. _**Note**: if the `uris`
              parameter is present in the query string, any URIs listed here in the body will
              be ignored._

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not playlist_id:
            raise ValueError(f"Expected a non-empty value for `playlist_id` but received {playlist_id!r}")
        return self._post(
            path_template("/playlists/{playlist_id}/tracks", playlist_id=playlist_id),
            body=maybe_transform(
                {
                    "position": position,
                    "published": published,
                    "uris": uris,
                },
                track_add_params.TrackAddParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=TrackAddResponse,
        )

    @typing_extensions.deprecated("deprecated")
    def remove(
        self,
        playlist_id: str,
        *,
        tracks: Iterable[track_remove_params.Track],
        published: bool | Omit = omit,
        snapshot_id: str | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> TrackRemoveResponse:
        """
        **Deprecated:** Use
        [Remove Playlist Items](/documentation/web-api/reference/remove-items-playlist)
        instead.

        Remove one or more items from a user's playlist.

        Args:
          playlist_id: The [Spotify ID](/documentation/web-api/concepts/spotify-uris-ids) of the
              playlist.

          tracks: An array of objects containing
              [Spotify URIs](/documentation/web-api/concepts/spotify-uris-ids) of the tracks
              or episodes to remove. For example:
              `{ "tracks": [{ "uri": "spotify:track:4iV5W9uYEdYUVa79Axb7Rh" },{ "uri": "spotify:track:1301WleyT98MSxVHPZCA6M" }] }`.
              A maximum of 100 objects can be sent at once.

          published: The playlist's public/private status (if it should be added to the user's
              profile or not): `true` the playlist will be public, `false` the playlist will
              be private, `null` the playlist status is not relevant. For more about
              public/private status, see
              [Working with Playlists](/documentation/web-api/concepts/playlists)

          snapshot_id: The playlist's snapshot ID against which you want to make the changes. The API
              will validate that the specified items exist and in the specified positions and
              make the changes, even if more recent changes have been made to the playlist.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not playlist_id:
            raise ValueError(f"Expected a non-empty value for `playlist_id` but received {playlist_id!r}")
        return self._delete(
            path_template("/playlists/{playlist_id}/tracks", playlist_id=playlist_id),
            body=maybe_transform(
                {
                    "tracks": tracks,
                    "published": published,
                    "snapshot_id": snapshot_id,
                },
                track_remove_params.TrackRemoveParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=TrackRemoveResponse,
        )


class AsyncTracksResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncTracksResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/cjavdev/spotted-py#accessing-raw-response-data-eg-headers
        """
        return AsyncTracksResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncTracksResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/cjavdev/spotted-py#with_streaming_response
        """
        return AsyncTracksResourceWithStreamingResponse(self)

    @typing_extensions.deprecated("deprecated")
    async def update(
        self,
        playlist_id: str,
        *,
        insert_before: int | Omit = omit,
        published: bool | Omit = omit,
        range_length: int | Omit = omit,
        range_start: int | Omit = omit,
        snapshot_id: str | Omit = omit,
        uris: SequenceNotStr[str] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> TrackUpdateResponse:
        """
        **Deprecated:** Use
        [Update Playlist Items](/documentation/web-api/reference/reorder-or-replace-playlists-items)
        instead.

        Either reorder or replace items in a playlist depending on the request's
        parameters. To reorder items, include `range_start`, `insert_before`,
        `range_length` and `snapshot_id` in the request's body. To replace items,
        include `uris` as either a query parameter or in the request's body. Replacing
        items in a playlist will overwrite its existing items. This operation can be
        used for replacing or clearing items in a playlist. <br/> **Note**: Replace and
        reorder are mutually exclusive operations which share the same endpoint, but
        have different parameters. These operations can't be applied together in a
        single request.

        Args:
          playlist_id: The [Spotify ID](/documentation/web-api/concepts/spotify-uris-ids) of the
              playlist.

          insert_before: The position where the items should be inserted.<br/>To reorder the items to the
              end of the playlist, simply set _insert_before_ to the position after the last
              item.<br/>Examples:<br/>To reorder the first item to the last position in a
              playlist with 10 items, set _range_start_ to 0, and _insert_before_
              to 10.<br/>To reorder the last item in a playlist with 10 items to the start of
              the playlist, set _range_start_ to 9, and _insert_before_ to 0.

          published: The playlist's public/private status (if it should be added to the user's
              profile or not): `true` the playlist will be public, `false` the playlist will
              be private, `null` the playlist status is not relevant. For more about
              public/private status, see
              [Working with Playlists](/documentation/web-api/concepts/playlists)

          range_length: The amount of items to be reordered. Defaults to 1 if not set.<br/>The range of
              items to be reordered begins from the _range_start_ position, and includes the
              _range_length_ subsequent items.<br/>Example:<br/>To move the items at index
              9-10 to the start of the playlist, _range_start_ is set to 9, and _range_length_
              is set to 2.

          range_start: The position of the first item to be reordered.

          snapshot_id: The playlist's snapshot ID against which you want to make the changes.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not playlist_id:
            raise ValueError(f"Expected a non-empty value for `playlist_id` but received {playlist_id!r}")
        return await self._put(
            path_template("/playlists/{playlist_id}/tracks", playlist_id=playlist_id),
            body=await async_maybe_transform(
                {
                    "insert_before": insert_before,
                    "published": published,
                    "range_length": range_length,
                    "range_start": range_start,
                    "snapshot_id": snapshot_id,
                    "uris": uris,
                },
                track_update_params.TrackUpdateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=TrackUpdateResponse,
        )

    @typing_extensions.deprecated("deprecated")
    def list(
        self,
        playlist_id: str,
        *,
        additional_types: str | Omit = omit,
        fields: str | Omit = omit,
        limit: int | Omit = omit,
        market: str | Omit = omit,
        offset: int | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> AsyncPaginator[PlaylistTrackObject, AsyncCursorURLPage[PlaylistTrackObject]]:
        """
        **Deprecated:** Use
        [Get Playlist Items](/documentation/web-api/reference/get-playlists-items)
        instead.

        Get full details of the items of a playlist owned by a Spotify user.

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
              omitted, all fields are returned. For example, to get just the total number of
              items and the request limit:<br/>`fields=total,limit`<br/>A dot separator can be
              used to specify non-reoccurring fields, while parentheses can be used to specify
              reoccurring fields within objects. For example, to get just the added date and
              user ID of the adder:<br/>`fields=items(added_at,added_by.id)`<br/>Use multiple
              parentheses to drill down into nested objects, for
              example:<br/>`fields=items(track(name,href,album(name,href)))`<br/>Fields can be
              excluded by prefixing them with an exclamation mark, for
              example:<br/>`fields=items.track.album(!external_urls,images)`

          limit: The maximum number of items to return. Default: 20. Minimum: 1. Maximum: 100.

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
        if not playlist_id:
            raise ValueError(f"Expected a non-empty value for `playlist_id` but received {playlist_id!r}")
        return self._get_api_list(
            path_template("/playlists/{playlist_id}/tracks", playlist_id=playlist_id),
            page=AsyncCursorURLPage[PlaylistTrackObject],
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "additional_types": additional_types,
                        "fields": fields,
                        "limit": limit,
                        "market": market,
                        "offset": offset,
                    },
                    track_list_params.TrackListParams,
                ),
            ),
            model=PlaylistTrackObject,
        )

    @typing_extensions.deprecated("deprecated")
    async def add(
        self,
        playlist_id: str,
        *,
        position: int | Omit = omit,
        published: bool | Omit = omit,
        uris: SequenceNotStr[str] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> TrackAddResponse:
        """
        **Deprecated:** Use
        [Add Items to Playlist](/documentation/web-api/reference/add-items-to-playlist)
        instead.

        Add one or more items to a user's playlist.

        Args:
          playlist_id: The [Spotify ID](/documentation/web-api/concepts/spotify-uris-ids) of the
              playlist.

          position: The position to insert the items, a zero-based index. For example, to insert the
              items in the first position: `position=0` ; to insert the items in the third
              position: `position=2`. If omitted, the items will be appended to the playlist.
              Items are added in the order they appear in the uris array. For example:
              `{"uris": ["spotify:track:4iV5W9uYEdYUVa79Axb7Rh","spotify:track:1301WleyT98MSxVHPZCA6M"], "position": 3}`

          published: The playlist's public/private status (if it should be added to the user's
              profile or not): `true` the playlist will be public, `false` the playlist will
              be private, `null` the playlist status is not relevant. For more about
              public/private status, see
              [Working with Playlists](/documentation/web-api/concepts/playlists)

          uris: A JSON array of the
              [Spotify URIs](/documentation/web-api/concepts/spotify-uris-ids) to add. For
              example:
              `{"uris": ["spotify:track:4iV5W9uYEdYUVa79Axb7Rh","spotify:track:1301WleyT98MSxVHPZCA6M", "spotify:episode:512ojhOuo1ktJprKbVcKyQ"]}`<br/>A
              maximum of 100 items can be added in one request. _**Note**: if the `uris`
              parameter is present in the query string, any URIs listed here in the body will
              be ignored._

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not playlist_id:
            raise ValueError(f"Expected a non-empty value for `playlist_id` but received {playlist_id!r}")
        return await self._post(
            path_template("/playlists/{playlist_id}/tracks", playlist_id=playlist_id),
            body=await async_maybe_transform(
                {
                    "position": position,
                    "published": published,
                    "uris": uris,
                },
                track_add_params.TrackAddParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=TrackAddResponse,
        )

    @typing_extensions.deprecated("deprecated")
    async def remove(
        self,
        playlist_id: str,
        *,
        tracks: Iterable[track_remove_params.Track],
        published: bool | Omit = omit,
        snapshot_id: str | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> TrackRemoveResponse:
        """
        **Deprecated:** Use
        [Remove Playlist Items](/documentation/web-api/reference/remove-items-playlist)
        instead.

        Remove one or more items from a user's playlist.

        Args:
          playlist_id: The [Spotify ID](/documentation/web-api/concepts/spotify-uris-ids) of the
              playlist.

          tracks: An array of objects containing
              [Spotify URIs](/documentation/web-api/concepts/spotify-uris-ids) of the tracks
              or episodes to remove. For example:
              `{ "tracks": [{ "uri": "spotify:track:4iV5W9uYEdYUVa79Axb7Rh" },{ "uri": "spotify:track:1301WleyT98MSxVHPZCA6M" }] }`.
              A maximum of 100 objects can be sent at once.

          published: The playlist's public/private status (if it should be added to the user's
              profile or not): `true` the playlist will be public, `false` the playlist will
              be private, `null` the playlist status is not relevant. For more about
              public/private status, see
              [Working with Playlists](/documentation/web-api/concepts/playlists)

          snapshot_id: The playlist's snapshot ID against which you want to make the changes. The API
              will validate that the specified items exist and in the specified positions and
              make the changes, even if more recent changes have been made to the playlist.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not playlist_id:
            raise ValueError(f"Expected a non-empty value for `playlist_id` but received {playlist_id!r}")
        return await self._delete(
            path_template("/playlists/{playlist_id}/tracks", playlist_id=playlist_id),
            body=await async_maybe_transform(
                {
                    "tracks": tracks,
                    "published": published,
                    "snapshot_id": snapshot_id,
                },
                track_remove_params.TrackRemoveParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=TrackRemoveResponse,
        )


class TracksResourceWithRawResponse:
    def __init__(self, tracks: TracksResource) -> None:
        self._tracks = tracks

        self.update = (  # pyright: ignore[reportDeprecated]
            to_raw_response_wrapper(
                tracks.update,  # pyright: ignore[reportDeprecated],
            )
        )
        self.list = (  # pyright: ignore[reportDeprecated]
            to_raw_response_wrapper(
                tracks.list,  # pyright: ignore[reportDeprecated],
            )
        )
        self.add = (  # pyright: ignore[reportDeprecated]
            to_raw_response_wrapper(
                tracks.add,  # pyright: ignore[reportDeprecated],
            )
        )
        self.remove = (  # pyright: ignore[reportDeprecated]
            to_raw_response_wrapper(
                tracks.remove,  # pyright: ignore[reportDeprecated],
            )
        )


class AsyncTracksResourceWithRawResponse:
    def __init__(self, tracks: AsyncTracksResource) -> None:
        self._tracks = tracks

        self.update = (  # pyright: ignore[reportDeprecated]
            async_to_raw_response_wrapper(
                tracks.update,  # pyright: ignore[reportDeprecated],
            )
        )
        self.list = (  # pyright: ignore[reportDeprecated]
            async_to_raw_response_wrapper(
                tracks.list,  # pyright: ignore[reportDeprecated],
            )
        )
        self.add = (  # pyright: ignore[reportDeprecated]
            async_to_raw_response_wrapper(
                tracks.add,  # pyright: ignore[reportDeprecated],
            )
        )
        self.remove = (  # pyright: ignore[reportDeprecated]
            async_to_raw_response_wrapper(
                tracks.remove,  # pyright: ignore[reportDeprecated],
            )
        )


class TracksResourceWithStreamingResponse:
    def __init__(self, tracks: TracksResource) -> None:
        self._tracks = tracks

        self.update = (  # pyright: ignore[reportDeprecated]
            to_streamed_response_wrapper(
                tracks.update,  # pyright: ignore[reportDeprecated],
            )
        )
        self.list = (  # pyright: ignore[reportDeprecated]
            to_streamed_response_wrapper(
                tracks.list,  # pyright: ignore[reportDeprecated],
            )
        )
        self.add = (  # pyright: ignore[reportDeprecated]
            to_streamed_response_wrapper(
                tracks.add,  # pyright: ignore[reportDeprecated],
            )
        )
        self.remove = (  # pyright: ignore[reportDeprecated]
            to_streamed_response_wrapper(
                tracks.remove,  # pyright: ignore[reportDeprecated],
            )
        )


class AsyncTracksResourceWithStreamingResponse:
    def __init__(self, tracks: AsyncTracksResource) -> None:
        self._tracks = tracks

        self.update = (  # pyright: ignore[reportDeprecated]
            async_to_streamed_response_wrapper(
                tracks.update,  # pyright: ignore[reportDeprecated],
            )
        )
        self.list = (  # pyright: ignore[reportDeprecated]
            async_to_streamed_response_wrapper(
                tracks.list,  # pyright: ignore[reportDeprecated],
            )
        )
        self.add = (  # pyright: ignore[reportDeprecated]
            async_to_streamed_response_wrapper(
                tracks.add,  # pyright: ignore[reportDeprecated],
            )
        )
        self.remove = (  # pyright: ignore[reportDeprecated]
            async_to_streamed_response_wrapper(
                tracks.remove,  # pyright: ignore[reportDeprecated],
            )
        )
