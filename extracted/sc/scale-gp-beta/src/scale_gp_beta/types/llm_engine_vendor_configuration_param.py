# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Dict
from typing_extensions import Required, TypedDict

from .._types import SequenceNotStr

__all__ = ["LlmEngineVendorConfigurationParam"]


class LlmEngineVendorConfigurationParam(TypedDict, total=False, extra_items=object):  # type: ignore[call-arg]
    model: Required[str]

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

    nodes_per_worker: int

    num_shards: int

    per_worker: int

    post_inference_hooks: SequenceNotStr[str]

    public_inference: bool

    quantize: str

    source: str

    storage: str
