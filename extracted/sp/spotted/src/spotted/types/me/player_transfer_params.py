# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Required, TypedDict

from ..._types import SequenceNotStr

__all__ = ["PlayerTransferParams"]


class PlayerTransferParams(TypedDict, total=False):
    device_ids: Required[SequenceNotStr[str]]
    """
    A JSON array containing the ID of the device on which playback should be
    started/transferred.<br/>For
    example:`{device_ids:["74ASZWbe4lXaubB36ztrGX"]}`<br/>_**Note**: Although an
    array is accepted, only a single device_id is currently supported. Supplying
    more than one will return `400 Bad Request`_
    """

    play: bool
    """
    **true**: ensure playback happens on new device.<br/>**false** or not provided:
    keep the current playback state.
    """

    published: bool
    """
    The playlist's public/private status (if it should be added to the user's
    profile or not): `true` the playlist will be public, `false` the playlist will
    be private, `null` the playlist status is not relevant. For more about
    public/private status, see
    [Working with Playlists](/documentation/web-api/concepts/playlists)
    """
