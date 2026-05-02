# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Required, TypedDict

__all__ = ["TrackCheckParams"]


class TrackCheckParams(TypedDict, total=False):
    ids: Required[str]
    """
    A comma-separated list of the
    [Spotify IDs](/documentation/web-api/concepts/spotify-uris-ids). For example:
    `ids=4iV5W9uYEdYUVa79Axb7Rh,1301WleyT98MSxVHPZCA6M`. Maximum: 50 IDs.
    """
