# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import TypedDict

__all__ = ["FollowerCheckParams"]


class FollowerCheckParams(TypedDict, total=False):
    ids: str
    """
    **Deprecated** A single item list containing current user's
    [Spotify Username](/documentation/web-api/concepts/spotify-uris-ids). Maximum: 1
    id.
    """
