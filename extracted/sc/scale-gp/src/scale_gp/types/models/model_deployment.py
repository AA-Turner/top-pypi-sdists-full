# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Dict, Union, Optional
from datetime import datetime
from typing_extensions import Literal, Annotated, TypeAlias

from ..._utils import PropertyInfo
from ..._compat import PYDANTIC_V1, ConfigDict
from ..._models import BaseModel

__all__ = [
    "ModelDeployment",
    "VendorConfiguration",
    "VendorConfigurationLaunchDeploymentVendorConfiguration",
    "VendorConfigurationLlmEngineDeploymentVendorConfiguration",
]


class VendorConfigurationLaunchDeploymentVendorConfiguration(BaseModel):
    max_workers: Optional[int] = None

    min_workers: Optional[int] = None

    per_worker: Optional[int] = None
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

    vendor: Optional[Literal["LAUNCH"]] = None


class VendorConfigurationLlmEngineDeploymentVendorConfiguration(BaseModel):
    base_model_name: Optional[str] = None

    checkpoint_path: Optional[str] = None

    cpus: Optional[int] = None

    gpu_type: Optional[
        Literal[
            "nvidia-tesla-t4",
            "nvidia-ampere-a10",
            "nvidia-ampere-a100",
            "nvidia-ampere-a100e",
            "nvidia-hopper-h100",
            "nvidia-hopper-h100-1g20gb",
            "nvidia-hopper-h100-3g40gb",
        ]
    ] = None

    gpus: Optional[int] = None

    high_priority: Optional[bool] = None

    inference_framework_image_tag: Optional[str] = None

    max_workers: Optional[int] = None

    memory: Optional[str] = None

    min_workers: Optional[int] = None

    model_name: Optional[str] = None

    num_shards: Optional[int] = None

    per_worker: Optional[int] = None
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

    storage: Optional[str] = None

    vendor: Optional[Literal["LLMENGINE"]] = None

    if not PYDANTIC_V1:
        # allow fields with a `model_` prefix
        model_config = ConfigDict(protected_namespaces=tuple())


VendorConfiguration: TypeAlias = Annotated[
    Union[
        VendorConfigurationLaunchDeploymentVendorConfiguration,
        VendorConfigurationLlmEngineDeploymentVendorConfiguration,
    ],
    PropertyInfo(discriminator="vendor"),
]


class ModelDeployment(BaseModel):
    id: str
    """The unique identifier of the entity."""

    account_id: str
    """The ID of the account that owns the given entity."""

    created_at: datetime
    """The date and time when the entity was created in ISO format."""

    created_by_identity_type: Literal["user", "service_account"]
    """The type of identity that created the entity."""

    created_by_user_id: str
    """The user who originally created the entity."""

    name: str

    status: str
    """Status of the model's deployment."""

    deployment_metadata: Optional[Dict[str, object]] = None

    model_creation_parameters: Optional[Dict[str, object]] = None

    model_endpoint_id: Optional[str] = None

    model_instance_id: Optional[str] = None

    vendor_configuration: Optional[VendorConfiguration] = None

    if not PYDANTIC_V1:
        # allow fields with a `model_` prefix
        model_config = ConfigDict(protected_namespaces=tuple())
