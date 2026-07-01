# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional

from .._models import BaseModel
from .item_locator import ItemLocator

__all__ = ["Component"]


class Component(BaseModel):
    data: ItemLocator
    """
    A pointer to the data in each evaluation item to be displayed within the
    component
    """

    label: Optional[str] = None
