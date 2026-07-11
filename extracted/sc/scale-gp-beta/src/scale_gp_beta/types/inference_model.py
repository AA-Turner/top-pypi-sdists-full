# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Dict, Union, Optional
from datetime import datetime
from typing_extensions import Literal, TypeAlias

from pydantic import Field as FieldInfo

from .._models import BaseModel
from .inference_model_type import InferenceModelType
from .chat.inference_model_vendor import InferenceModelVendor
from .launch_vendor_configuration import LaunchVendorConfiguration
from .inference_model_availability import InferenceModelAvailability
from .llm_engine_vendor_configuration import LlmEngineVendorConfiguration

__all__ = ["InferenceModel", "VendorConfiguration"]

VendorConfiguration: TypeAlias = Union[LaunchVendorConfiguration, LlmEngineVendorConfiguration]


class InferenceModel(BaseModel):
    id: str

    created_at: datetime

    created_by_identity_type: Literal["user", "service_account"]

    created_by_user_id: str

    api_model_type: InferenceModelType = FieldInfo(alias="model_type")

    api_model_vendor: InferenceModelVendor = FieldInfo(alias="model_vendor")

    name: str

    status: Literal["failed", "ready", "deploying", "deployment_timeout"]

    api_model_availability: Optional[InferenceModelAvailability] = FieldInfo(alias="model_availability", default=None)

    metadata: Optional[Dict[str, object]] = FieldInfo(alias="model_metadata", default=None)

    object: Optional[Literal["model"]] = None

    status_reason: Optional[str] = None

    vendor_configuration: Optional[VendorConfiguration] = None
