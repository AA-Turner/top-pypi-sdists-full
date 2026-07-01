# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Dict, Iterable
from typing_extensions import Required, TypedDict

__all__ = ["DatasetItemBatchCreateParams"]


class DatasetItemBatchCreateParams(TypedDict, total=False):
    data: Required[Iterable[Dict[str, object]]]
    """Items to be added to the dataset"""

    dataset_id: Required[str]
    """Identifier of the target dataset"""

    files: Iterable[Dict[str, str]]
    """Files to be associated to the dataset"""
