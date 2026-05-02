# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Required, TypedDict

__all__ = ["PlayerSeekToPositionParams"]


class PlayerSeekToPositionParams(TypedDict, total=False):
    position_ms: Required[int]
    """The position in milliseconds to seek to.

    Must be a positive number. Passing in a position that is greater than the length
    of the track will cause the player to start playing the next song.
    """

    device_id: str
    """The id of the device this command is targeting.

    If not supplied, the user's currently active device is the target.
    """
