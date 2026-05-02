# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Dict, List, Union, Optional
from typing_extensions import Literal

from .._models import BaseModel

__all__ = ["InferenceResponse"]


class InferenceResponse(BaseModel):
    response: Union[Dict[str, object], List[object], str, float, bool]

    object: Optional[Literal["generic_inference"]] = None
