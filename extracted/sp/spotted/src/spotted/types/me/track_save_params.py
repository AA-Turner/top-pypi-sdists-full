# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Union, Iterable
from datetime import datetime
from typing_extensions import Required, Annotated, TypedDict

from ..._types import SequenceNotStr
from ..._utils import PropertyInfo

__all__ = ["TrackSaveParams", "TimestampedID"]


class TrackSaveParams(TypedDict, total=False):
    ids: Required[SequenceNotStr[str]]
    """
    A JSON array of the
    [Spotify IDs](/documentation/web-api/concepts/spotify-uris-ids). For example:
    `["4iV5W9uYEdYUVa79Axb7Rh", "1301WleyT98MSxVHPZCA6M"]`<br/>A maximum of 50 items
    can be specified in one request. _**Note**: if the `timestamped_ids` is present
    in the body, any IDs listed in the query parameters (deprecated) or the `ids`
    field in the body will be ignored._
    """

    published: bool
    """
    The playlist's public/private status (if it should be added to the user's
    profile or not): `true` the playlist will be public, `false` the playlist will
    be private, `null` the playlist status is not relevant. For more about
    public/private status, see
    [Working with Playlists](/documentation/web-api/concepts/playlists)
    """

    timestamped_ids: Iterable[TimestampedID]
    """A JSON array of objects containing track IDs with their corresponding
    timestamps.

    Each object must include a track ID and an `added_at` timestamp. This allows you
    to specify when tracks were added to maintain a specific chronological order in
    the user's library.<br/>A maximum of 50 items can be specified in one request.
    _**Note**: if the `timestamped_ids` is present in the body, any IDs listed in
    the query parameters (deprecated) or the `ids` field in the body will be
    ignored._
    """


class TimestampedID(TypedDict, total=False):
    id: Required[str]
    """
    The [Spotify ID](/documentation/web-api/concepts/spotify-uris-ids) for the
    track.
    """

    added_at: Required[Annotated[Union[str, datetime], PropertyInfo(format="iso8601")]]
    """The timestamp when the track was added to the library.

    Use ISO 8601 format with UTC timezone (e.g., `2023-01-15T14:30:00Z`). You can
    specify past timestamps to insert tracks at specific positions in the library's
    chronological order. The API uses minute-level granularity for ordering, though
    the timestamp supports millisecond precision.
    """
