# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import TypedDict

from ..._types import SequenceNotStr

__all__ = ["TrackUpdateParams"]


class TrackUpdateParams(TypedDict, total=False):
    insert_before: int
    """
    The position where the items should be inserted.<br/>To reorder the items to the
    end of the playlist, simply set _insert_before_ to the position after the last
    item.<br/>Examples:<br/>To reorder the first item to the last position in a
    playlist with 10 items, set _range_start_ to 0, and _insert_before_
    to 10.<br/>To reorder the last item in a playlist with 10 items to the start of
    the playlist, set _range_start_ to 9, and _insert_before_ to 0.
    """

    published: bool
    """
    The playlist's public/private status (if it should be added to the user's
    profile or not): `true` the playlist will be public, `false` the playlist will
    be private, `null` the playlist status is not relevant. For more about
    public/private status, see
    [Working with Playlists](/documentation/web-api/concepts/playlists)
    """

    range_length: int
    """The amount of items to be reordered.

    Defaults to 1 if not set.<br/>The range of items to be reordered begins from the
    _range_start_ position, and includes the _range_length_ subsequent
    items.<br/>Example:<br/>To move the items at index 9-10 to the start of the
    playlist, _range_start_ is set to 9, and _range_length_ is set to 2.
    """

    range_start: int
    """The position of the first item to be reordered."""

    snapshot_id: str
    """The playlist's snapshot ID against which you want to make the changes."""

    uris: SequenceNotStr[str]
