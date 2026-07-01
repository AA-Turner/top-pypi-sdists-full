# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Literal, Required, TypedDict

__all__ = ["TextContentParam"]


class TextContentParam(TypedDict, total=False):
    """Text content for documents."""

    text: Required[str]
    """Text content to be embedded"""

    type: Literal["text"]
    """Content type identifier"""
