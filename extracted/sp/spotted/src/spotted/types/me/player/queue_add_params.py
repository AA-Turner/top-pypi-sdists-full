# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Required, TypedDict

__all__ = ["QueueAddParams"]


class QueueAddParams(TypedDict, total=False):
    uri: Required[str]
    """The uri of the item to add to the queue. Must be a track or an episode uri."""

    device_id: str
    """The id of the device this command is targeting.

    If not supplied, the user's currently active device is the target.
    """
