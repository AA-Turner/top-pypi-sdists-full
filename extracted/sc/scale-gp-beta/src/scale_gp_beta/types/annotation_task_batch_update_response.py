# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional
from typing_extensions import Literal

from .._models import BaseModel
from .annotation_task import AnnotationTask

__all__ = ["AnnotationTaskBatchUpdateResponse"]


class AnnotationTaskBatchUpdateResponse(BaseModel):
    items: List[AnnotationTask]

    object: Optional[Literal["list"]] = None
