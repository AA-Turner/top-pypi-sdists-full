# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Dict, Union, Optional
from datetime import datetime
from typing_extensions import Literal, TypeAlias

from pydantic import Field as FieldInfo

from .._models import BaseModel
from .launch_vendor_configuration import LaunchVendorConfiguration
from .llm_engine_vendor_configuration import LlmEngineVendorConfiguration

__all__ = ["InferenceModel", "VendorConfiguration"]

VendorConfiguration: TypeAlias = Union[LaunchVendorConfiguration, LlmEngineVendorConfiguration]


class InferenceModel(BaseModel):
    id: str

    created_at: datetime

    created_by_identity_type: Literal["user", "service_account"]

    created_by_user_id: str

    type: Literal["generic", "completion", "chat_completion"] = FieldInfo(alias="model_type")

    vendor: Literal[
        "openai",
        "cohere",
        "vertex_ai",
        "anthropic",
        "azure",
        "gemini",
        "launch",
        "llmengine",
        "model_zoo",
        "bedrock",
        "xai",
        "fireworks_ai",
    ] = FieldInfo(alias="model_vendor")

    name: str

    status: Literal["failed", "ready", "deploying", "deployment_timeout"]

    availability: Optional[Literal["unknown", "available", "unavailable"]] = FieldInfo(
        alias="model_availability", default=None
    )

    metadata: Optional[Dict[str, object]] = FieldInfo(alias="model_metadata", default=None)

    object: Optional[Literal["model"]] = None

    vendor_configuration: Optional[VendorConfiguration] = None
