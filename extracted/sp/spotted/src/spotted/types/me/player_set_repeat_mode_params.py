# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Required, TypedDict

__all__ = ["PlayerSetRepeatModeParams"]


class PlayerSetRepeatModeParams(TypedDict, total=False):
    state: Required[str]
    """
    **track**, **context** or **off**.<br/> **track** will repeat the current
    track.<br/> **context** will repeat the current context.<br/> **off** will turn
    repeat off.
    """

    device_id: str
    """The id of the device this command is targeting.

    If not supplied, the user's currently active device is the target.
    """
