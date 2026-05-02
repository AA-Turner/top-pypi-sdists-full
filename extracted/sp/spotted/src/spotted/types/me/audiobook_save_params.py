# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Required, TypedDict

__all__ = ["AudiobookSaveParams"]


class AudiobookSaveParams(TypedDict, total=False):
    ids: Required[str]
    """
    A comma-separated list of the
    [Spotify IDs](/documentation/web-api/concepts/spotify-uris-ids). For example:
    `ids=18yVqkdbdRvS24c0Ilj2ci,1HGw3J3NxZO1TP1BTtVhpZ`. Maximum: 50 IDs.
    """
