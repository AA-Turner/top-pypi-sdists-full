# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Literal, Required, TypedDict

__all__ = ["DesignListCuratedSpecificationsParams"]


class DesignListCuratedSpecificationsParams(TypedDict, total=False):
    type: Required[Literal["nanobody", "antibody"]]
    """Curated binder library to retrieve."""
