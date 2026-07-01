# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Dict, Union
from typing_extensions import Literal, Required, TypedDict

from .._types import SequenceNotStr

__all__ = ["LaunchVendorConfigurationParam", "ModelImage", "ModelInfra"]


class ModelImage(TypedDict, total=False):
    command: Required[SequenceNotStr[str]]

    registry: Required[str]

    repository: Required[str]

    tag: Required[str]

    env_vars: Dict[str, object]

    healthcheck_route: str

    predict_route: str

    readiness_delay: int

    request_schema: Dict[str, object]

    response_schema: Dict[str, object]

    streaming_command: SequenceNotStr[str]

    streaming_predict_route: str


class ModelInfra(TypedDict, total=False):
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


class LaunchVendorConfigurationParam(TypedDict, total=False):
    model_image: Required[ModelImage]

    model_infra: Required[ModelInfra]
