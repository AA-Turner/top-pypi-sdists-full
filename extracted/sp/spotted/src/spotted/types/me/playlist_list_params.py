# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import TypedDict

__all__ = ["PlaylistListParams"]


class PlaylistListParams(TypedDict, total=False):
    limit: int
    """The maximum number of items to return. Default: 20. Minimum: 1. Maximum: 50."""

    offset: int
    """'The index of the first playlist to return.

    Default: 0 (the first object). Maximum offset: 100.000\\.. Use with `limit` to get
    the next set of playlists.'
    """
