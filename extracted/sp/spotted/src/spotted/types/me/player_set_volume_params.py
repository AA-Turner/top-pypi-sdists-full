# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Required, TypedDict

__all__ = ["PlayerSetVolumeParams"]


class PlayerSetVolumeParams(TypedDict, total=False):
    volume_percent: Required[int]
    """The volume to set. Must be a value from 0 to 100 inclusive."""

    device_id: str
    """The id of the device this command is targeting.

    If not supplied, the user's currently active device is the target.
    """
