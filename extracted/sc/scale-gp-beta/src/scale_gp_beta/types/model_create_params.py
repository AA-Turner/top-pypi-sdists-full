# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Dict, Union
from typing_extensions import Literal, Required, TypeAlias, TypedDict

from .inference_model_type import InferenceModelType
from .launch_vendor_configuration_param import LaunchVendorConfigurationParam
from .llm_engine_vendor_configuration_param import LlmEngineVendorConfigurationParam

__all__ = [
    "ModelCreateParams",
    "Model",
    "ModelLaunchModelCreateRequest",
    "ModelLlmEngineModelCreateRequest",
    "ModelHostedModelCreateRequest",
]


class ModelCreateParams(TypedDict, total=False):
    model: Required[Model]
    """Register a model already served by an external / proxy-served vendor (e.g.

    an OpenAI-compatible self-hosted model behind the inference proxy).

    Unlike launch/llmengine, no Scale-side deployment is performed: the record is
    created READY and is immediately callable via /v5/chat/completions. Accepted
    only when NATIVE_OPENAI_INFERENCE_GATEWAY is enabled. The discriminator
    (model_vendor) covers every vendor except launch/llmengine, and no
    vendor_configuration applies.
    """


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


class ModelHostedModelCreateRequest(TypedDict, total=False):
    """Register a model already served by an external / proxy-served vendor
    (e.g.

    an OpenAI-compatible self-hosted model behind the inference proxy).

    Unlike launch/llmengine, no Scale-side deployment is performed: the record is
    created READY and is immediately callable via /v5/chat/completions. Accepted only
    when NATIVE_OPENAI_INFERENCE_GATEWAY is enabled. The discriminator (model_vendor)
    covers every vendor except launch/llmengine, and no vendor_configuration applies.
    """

    model_type: Required[InferenceModelType]
    """Type of model, for example `chat_completion`"""

    model_vendor: Required[
        Literal[
            "openai",
            "cohere",
            "vertex_ai",
            "anthropic",
            "azure",
            "gemini",
            "model_zoo",
            "bedrock",
            "xai",
            "fireworks_ai",
        ]
    ]
    """Vendor to serve/create model"""

    name: Required[str]
    """Unique name to reference your model"""

    model_metadata: Dict[str, object]

    on_conflict: Literal["error", "update"]


Model: TypeAlias = Union[ModelLaunchModelCreateRequest, ModelLlmEngineModelCreateRequest, ModelHostedModelCreateRequest]
