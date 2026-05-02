# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Required, TypedDict

__all__ = ["LastKMemoryStrategyParams"]


class LastKMemoryStrategyParams(TypedDict, total=False):
    k: Required[int]
    """The maximum number of previous messages to remember."""
