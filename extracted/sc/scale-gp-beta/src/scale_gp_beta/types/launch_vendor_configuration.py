# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Dict, List, Union, Optional
from typing_extensions import Literal

from pydantic import Field as FieldInfo

from .._models import BaseModel

__all__ = ["LaunchVendorConfiguration", "ModelImage", "ModelInfra"]


class ModelImage(BaseModel):
    command: List[str]

    registry: str

    repository: str

    tag: str

    env_vars: Optional[Dict[str, object]] = None

    healthcheck_route: Optional[str] = None

    predict_route: Optional[str] = None

    readiness_delay: Optional[int] = None

    request_schema: Optional[Dict[str, object]] = None

    response_schema: Optional[Dict[str, object]] = None

    streaming_command: Optional[List[str]] = None

    streaming_predict_route: Optional[str] = None


class ModelInfra(BaseModel):
    cpus: Union[str, int, None] = None

    endpoint_type: Optional[Literal["async", "sync", "streaming"]] = None

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

    labels: Optional[Dict[str, str]] = None

    max_workers: Optional[int] = None

    memory: Optional[str] = None

    min_workers: Optional[int] = None

    per_worker: Optional[int] = None

    public_inference: Optional[bool] = None

    storage: Optional[str] = None


class LaunchVendorConfiguration(BaseModel):
    image: ModelImage = FieldInfo(alias="model_image")

    infra: ModelInfra = FieldInfo(alias="model_infra")
