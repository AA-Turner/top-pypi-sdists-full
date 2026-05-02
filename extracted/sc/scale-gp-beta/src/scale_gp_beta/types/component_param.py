# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Required, TypedDict

from .item_locator import ItemLocator

__all__ = ["ComponentParam"]


class ComponentParam(TypedDict, total=False):
    data: Required[ItemLocator]
    """
    A pointer to the data in each evaluation item to be displayed within the
    component
    """

    label: str
