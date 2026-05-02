# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Dict
from typing_extensions import Literal, Required, TypedDict

from .._types import SequenceNotStr
from .parameter_schema_param import ParameterSchemaParam

__all__ = [
    "ModelTemplateCreateParams",
    "VendorConfiguration",
    "VendorConfigurationBundleConfig",
    "VendorConfigurationEndpointConfig",
    "VendorConfigurationFineTuningJobBundleConfig",
    "VendorConfigurationFineTuningJobBundleConfigResources",
]


class ModelTemplateCreateParams(TypedDict, total=False):
    account_id: Required[str]
    """The ID of the account that owns the given entity."""

    endpoint_type: Required[Literal["SYNC", "ASYNC", "STREAMING", "BATCH"]]
    """An enum representing the different types of model endpoint types supported.

    Attributes: SYNC: Denotes that the model endpoint type is sync. ASYNC: Denotes
    that the model endpoint type is async. STREAMING: Denotes that the model
    endpoint type is streaming. BATCH: Denotes that the model endpoint type is
    batch.
    """

    model_type: Required[
        Literal["COMPLETION", "CHAT_COMPLETION", "AGENT", "EMBEDDING", "RERANKING", "GENERIC", "BUNDLE"]
    ]
    """An enum representing the different types of models supported.

    Attributes: COMPLETION: Denotes that the model type is completion.
    CHAT_COMPLETION: Denotes that the model type is chat completion. AGENT: Denotes
    that the model type is agent. EMBEDDING: Denotes that the model type is
    embedding. RERANKING: Denotes that the model type is reranking. GENERIC: Denotes
    that the model type is generic. BUNDLE: "Not to be used directly - type to
    surface a model bundle in the UI - TODO: Explicitly type a bundle
    """

    name: Required[str]

    vendor_configuration: Required[VendorConfiguration]
    """
    Configuration for launching a model using the Launch service which is an
    internal and self-hosted service developed by Scale that deploys models on
    Kubernetes.

    Attributes: vendor: The vendor of the model template bundle_config: The bundle
    configuration of the model template endpoint_config: The endpoint configuration
    of the model template
    """

    endpoint_protocol: Literal["SGP", "COHERE", "VLLM"]
    """The name of the calling convention expected by the Launch model endpoint"""

    model_creation_parameters_schema: ParameterSchemaParam
    """
    The field names and types of available parameter fields which may be specified
    during model creation
    """

    model_request_parameters_schema: ParameterSchemaParam
    """
    The field names and types of available parameter fields which may be specified
    in a model execution API's `model_request_parameters` field.
    """


class VendorConfigurationBundleConfig(TypedDict, total=False):
    image: Required[str]

    registry: Required[str]

    tag: Required[str]

    command: SequenceNotStr[str]

    env: Dict[str, str]

    healthcheck_route: str

    predict_route: str

    readiness_initial_delay_seconds: int

    streaming_command: SequenceNotStr[str]

    streaming_predict_route: str


class VendorConfigurationEndpointConfig(TypedDict, total=False):
    cpus: int

    endpoint_type: Literal["SYNC", "ASYNC", "STREAMING", "BATCH"]
    """An enum representing the different types of model endpoint types supported.

    Attributes: SYNC: Denotes that the model endpoint type is sync. ASYNC: Denotes
    that the model endpoint type is async. STREAMING: Denotes that the model
    endpoint type is streaming. BATCH: Denotes that the model endpoint type is
    batch.
    """

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

    max_workers: int

    memory: str

    min_workers: int

    per_worker: int
    """The maximum number of concurrent requests that an individual worker can service.

    Launch automatically scales the number of workers for the endpoint so that each
    worker is processing `per_worker` requests, subject to the limits defined by
    `min_workers` and `max_workers`.

    - If the average number of concurrent requests per worker is lower than
      `per_worker`, then the number of workers will be reduced. - Otherwise, if the
      average number of concurrent requests per worker is higher than `per_worker`,
      then the number of workers will be increased to meet the elevated traffic.

    Here is our recommendation for computing `per_worker`:

    1. Compute `min_workers` and `max_workers` per your minimum and maximum
       throughput requirements. 2. Determine a value for the maximum number of
       concurrent requests in the workload. Divide this number by `max_workers`.
       Doing this ensures that the number of workers will "climb" to `max_workers`.
    """

    storage: str


class VendorConfigurationFineTuningJobBundleConfigResources(TypedDict, total=False):
    cpus: int

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

    memory: str

    storage: str


class VendorConfigurationFineTuningJobBundleConfig(TypedDict, total=False):
    image: Required[str]

    registry: Required[str]

    tag: Required[str]

    command: SequenceNotStr[str]

    env: Dict[str, str]

    mount_location: str
    """
    The filesystem location where the fine tuning job's configuration will be
    available when it is started.
    """

    resources: VendorConfigurationFineTuningJobBundleConfigResources

    training_dataset_schema_type: Literal["GENERATION", "RERANKING_QUESTIONS"]
    """Optionally set required training and validation dataset schema"""


class VendorConfiguration(TypedDict, total=False):
    """
    Configuration for launching a model using the Launch service which is an internal and
    self-hosted service developed by Scale that deploys models on Kubernetes.

    Attributes:
        vendor: The vendor of the model template
        bundle_config: The bundle configuration of the model template
        endpoint_config: The endpoint configuration of the model template
    """

    bundle_config: Required[VendorConfigurationBundleConfig]

    endpoint_config: VendorConfigurationEndpointConfig

    fine_tuning_job_bundle_config: VendorConfigurationFineTuningJobBundleConfig

    vendor: Literal["LAUNCH"]
