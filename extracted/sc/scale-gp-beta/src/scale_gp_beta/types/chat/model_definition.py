# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional

from pydantic import Field as FieldInfo

from ..._models import BaseModel
from ..inference_model_type import InferenceModelType
from .inference_model_vendor import InferenceModelVendor
from ..inference_model_availability import InferenceModelAvailability

__all__ = ["ModelDefinition"]


class ModelDefinition(BaseModel):
    name: str = FieldInfo(alias="model_name")
    """model name, for example `gpt-4o`"""

    api_model_type: InferenceModelType = FieldInfo(alias="model_type")
    """model type, for example `chat_completion`"""

    api_model_vendor: InferenceModelVendor = FieldInfo(alias="model_vendor")
    """model vendor, for example `openai`"""

    api_model_availability: Optional[InferenceModelAvailability] = FieldInfo(alias="model_availability", default=None)
    """model availability indicating availability status, for example `available`"""
