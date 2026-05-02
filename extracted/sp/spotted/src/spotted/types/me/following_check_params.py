# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Literal, Required, TypedDict

__all__ = ["FollowingCheckParams"]


class FollowingCheckParams(TypedDict, total=False):
    ids: Required[str]
    """
    A comma-separated list of the artist or the user
    [Spotify IDs](/documentation/web-api/concepts/spotify-uris-ids) to check. For
    example: `ids=74ASZWbe4lXaubB36ztrGX,08td7MxkoHQkXnWAYD8d6Q`. A maximum of 50
    IDs can be sent in one request.
    """

    type: Required[Literal["artist", "user"]]
    """The ID type: either `artist` or `user`."""
