# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Required, TypedDict

__all__ = ["PlayerToggleShuffleParams"]


class PlayerToggleShuffleParams(TypedDict, total=False):
    state: Required[bool]
    """
    **true** : Shuffle user's playback.<br/> **false** : Do not shuffle user's
    playback.
    """

    device_id: str
    """The id of the device this command is targeting.

    If not supplied, the user's currently active device is the target.
    """
