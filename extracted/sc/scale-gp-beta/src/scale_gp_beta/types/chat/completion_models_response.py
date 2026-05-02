# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional
from typing_extensions import Literal

from ..._models import BaseModel
from .model_definition import ModelDefinition

__all__ = ["CompletionModelsResponse"]


class CompletionModelsResponse(BaseModel):
    items: List[ModelDefinition]

    object: Optional[Literal["list"]] = None
