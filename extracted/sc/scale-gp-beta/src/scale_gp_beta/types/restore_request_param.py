# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Literal, Required, TypedDict

__all__ = ["RestoreRequestParam"]


class RestoreRequestParam(TypedDict, total=False):
    restore: Required[Literal[True]]
    """Set to true to restore the entity from the database."""
