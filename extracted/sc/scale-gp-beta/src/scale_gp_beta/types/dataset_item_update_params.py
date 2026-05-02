# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Dict
from typing_extensions import Required, TypedDict

__all__ = ["DatasetItemUpdateParams"]


class DatasetItemUpdateParams(TypedDict, total=False):
    data: Required[Dict[str, object]]
    """Updated dataset item data"""

    files: Dict[str, str]
    """Files to be associated to the dataset"""
