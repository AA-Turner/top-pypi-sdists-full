# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional
from typing_extensions import Literal

from .._models import BaseModel
from .dataset_item import DatasetItem

__all__ = ["DatasetItemBatchCreateResponse"]


class DatasetItemBatchCreateResponse(BaseModel):
    items: List[DatasetItem]

    object: Optional[Literal["list"]] = None
