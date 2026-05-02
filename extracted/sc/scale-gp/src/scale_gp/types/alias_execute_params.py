# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import TypedDict

__all__ = ["AliasExecuteParams"]


class AliasExecuteParams(TypedDict, total=False):
    stream: bool
    """Flag indicating whether to stream the completion response"""
