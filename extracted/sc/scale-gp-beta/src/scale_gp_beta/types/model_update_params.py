# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Dict, Union
from typing_extensions import Literal, Required, TypeAlias, TypedDict

from .._types import SequenceNotStr

__all__ = [
    "ModelUpdateParams",
    "Model",
    "ModelDefaultModelPatchRequest",
    "ModelModelConfigurationPatchRequest",
    "ModelModelConfigurationPatchRequestVendorConfiguration",
    "ModelModelConfigurationPatchRequestVendorConfigurationPartialLaunchVendorConfiguration",
    "ModelModelConfigurationPatchRequestVendorConfigurationPartialLaunchVendorConfigurationModelImage",
    "ModelModelConfigurationPatchRequestVendorConfigurationPartialLaunchVendorConfigurationModelInfra",
    "ModelModelConfigurationPatchRequestVendorConfigurationPartialLlmEngineVendorConfiguration",
    "ModelSwapNamesModelPatchRequest",
]


class ModelUpdateParams(TypedDict, total=False):
    model: Required[Model]


class ModelDefaultModelPatchRequest(TypedDict, total=False):
    model_metadata: Dict[str, object]


class ModelModelConfigurationPatchRequestVendorConfigurationPartialLaunchVendorConfigurationModelImage(
    TypedDict, total=False
):
    command: SequenceNotStr[str]

    env_vars: Dict[str, object]

    healthcheck_route: str

    predict_route: str

    readiness_delay: int

    registry: str

    repository: str

    request_schema: Dict[str, object]

    response_schema: Dict[str, object]

    streaming_command: SequenceNotStr[str]

    streaming_predict_route: str

    tag: str


class ModelModelConfigurationPatchRequestVendorConfigurationPartialLaunchVendorConfigurationModelInfra(
    TypedDict, total=False
):
    cpus: Union[str, int]

    endpoint_type: Literal["async", "sync", "streaming"]

    gpu_type: Literal[
        "nvidia-tesla-t4",
        "nvidia-ampere-a10",
        "nvidia-ampere-a100",
        "nvidia-ampere-a100e",
        "nvidia-hopper-h100",
        "nvidia-hopper-h100-1g20gb",
        "nvidia-hopper-h100-3g40gb",
    ]

    gpus: int

    high_priority: bool

    labels: Dict[str, str]

    max_workers: int

    memory: str

    min_workers: int

    per_worker: int

    public_inference: bool

    storage: str


class ModelModelConfigurationPatchRequestVendorConfigurationPartialLaunchVendorConfiguration(TypedDict, total=False):
    model_image: ModelModelConfigurationPatchRequestVendorConfigurationPartialLaunchVendorConfigurationModelImage

    model_infra: ModelModelConfigurationPatchRequestVendorConfigurationPartialLaunchVendorConfigurationModelInfra


class ModelModelConfigurationPatchRequestVendorConfigurationPartialLlmEngineVendorConfiguration(TypedDict, total=False):
    chat_template_override: str

    checkpoint_path: str

    cpus: int

    default_callback_url: str

    endpoint_type: str

    gpu_type: str

    gpus: int

    high_priority: bool

    inference_framework: str

    inference_framework_image_tag: str

    labels: Dict[str, str]

    max_workers: int

    memory: str

    min_workers: int

    model: str

    nodes_per_worker: int

    num_shards: int

    per_worker: int

    post_inference_hooks: SequenceNotStr[str]

    public_inference: bool

    quantize: str

    source: str

    storage: str


ModelModelConfigurationPatchRequestVendorConfiguration: TypeAlias = Union[
    ModelModelConfigurationPatchRequestVendorConfigurationPartialLaunchVendorConfiguration,
    ModelModelConfigurationPatchRequestVendorConfigurationPartialLlmEngineVendorConfiguration,
]


class ModelModelConfigurationPatchRequest(TypedDict, total=False):
    vendor_configuration: Required[ModelModelConfigurationPatchRequestVendorConfiguration]

    model_metadata: Dict[str, object]


class ModelSwapNamesModelPatchRequest(TypedDict, total=False):
    name: Required[str]

    on_conflict: Literal["error", "swap"]


Model: TypeAlias = Union[
    ModelDefaultModelPatchRequest, ModelModelConfigurationPatchRequest, ModelSwapNamesModelPatchRequest
]
