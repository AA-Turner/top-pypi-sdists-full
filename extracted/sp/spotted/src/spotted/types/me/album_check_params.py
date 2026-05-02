# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Required, TypedDict

__all__ = ["AlbumCheckParams"]


class AlbumCheckParams(TypedDict, total=False):
    ids: Required[str]
    """
    A comma-separated list of the
    [Spotify IDs](/documentation/web-api/concepts/spotify-uris-ids) for the albums.
    Maximum: 20 IDs.
    """
