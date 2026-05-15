# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Dict, Union
from typing_extensions import Literal, Required, TypeAlias, TypedDict

__all__ = [
    "DeploymentCreateParams",
    "VendorConfiguration",
    "VendorConfigurationLaunchDeploymentVendorConfiguration",
    "VendorConfigurationLlmEngineDeploymentVendorConfiguration",
]


class DeploymentCreateParams(TypedDict, total=False):
    name: Required[str]

    account_id: str
    """The ID of the account that owns the given entity."""

    deployment_metadata: Dict[str, object]

    model_creation_parameters: Dict[str, object]

    vendor_configuration: VendorConfiguration

    wait_for_ready: bool
    """If true, the request will block until the Launch endpoint is READY.

    Defaults to true.
    """


class VendorConfigurationLaunchDeploymentVendorConfiguration(TypedDict, total=False):
    max_workers: int

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

    vendor: Literal["LAUNCH"]


class VendorConfigurationLlmEngineDeploymentVendorConfiguration(TypedDict, total=False):
    base_model_name: str

    checkpoint_path: str

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

    high_priority: bool

    inference_framework_image_tag: str

    max_workers: int

    memory: str

    min_workers: int

    model_name: str

    num_shards: int

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

    vendor: Literal["LLMENGINE"]


VendorConfiguration: TypeAlias = Union[
    VendorConfigurationLaunchDeploymentVendorConfiguration, VendorConfigurationLlmEngineDeploymentVendorConfiguration
]
