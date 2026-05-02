# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Dict, Union
from typing_extensions import Literal, Required, TypeAlias, TypedDict

from .launch_vendor_configuration_param import LaunchVendorConfigurationParam
from .llm_engine_vendor_configuration_param import LlmEngineVendorConfigurationParam

__all__ = ["ModelCreateParams", "Model", "ModelLaunchModelCreateRequest", "ModelLlmEngineModelCreateRequest"]


class ModelCreateParams(TypedDict, total=False):
    model: Required[Model]


class ModelLaunchModelCreateRequest(TypedDict, total=False):
    name: Required[str]
    """Unique name to reference your model"""

    vendor_configuration: Required[LaunchVendorConfigurationParam]

    model_metadata: Dict[str, object]

    model_type: Literal["generic"]

    model_vendor: Literal["launch"]

    on_conflict: Literal["error", "update"]


class ModelLlmEngineModelCreateRequest(TypedDict, total=False):
    name: Required[str]
    """Unique name to reference your model"""

    vendor_configuration: Required[LlmEngineVendorConfigurationParam]

    model_metadata: Dict[str, object]

    model_type: Literal["chat_completion"]

    model_vendor: Literal["llmengine"]

    on_conflict: Literal["error", "update"]


Model: TypeAlias = Union[ModelLaunchModelCreateRequest, ModelLlmEngineModelCreateRequest]
