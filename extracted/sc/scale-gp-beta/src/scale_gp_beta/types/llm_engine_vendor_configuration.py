# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import TYPE_CHECKING, Dict, List, Optional

from pydantic import Field as FieldInfo

from .._models import BaseModel

__all__ = ["LlmEngineVendorConfiguration"]


class LlmEngineVendorConfiguration(BaseModel):
    model: str

    checkpoint_path: Optional[str] = None

    cpus: Optional[int] = None

    default_callback_url: Optional[str] = None

    endpoint_type: Optional[str] = None

    gpu_type: Optional[str] = None

    gpus: Optional[int] = None

    high_priority: Optional[bool] = None

    inference_framework: Optional[str] = None

    inference_framework_image_tag: Optional[str] = None

    labels: Optional[Dict[str, str]] = None

    max_workers: Optional[int] = None

    memory: Optional[str] = None

    min_workers: Optional[int] = None

    nodes_per_worker: Optional[int] = None

    num_shards: Optional[int] = None

    per_worker: Optional[int] = None

    post_inference_hooks: Optional[List[str]] = None

    public_inference: Optional[bool] = None

    quantize: Optional[str] = None

    source: Optional[str] = None

    storage: Optional[str] = None

    if TYPE_CHECKING:
        # Some versions of Pydantic <2.8.0 have a bug and don’t allow assigning a
        # value to this field, so for compatibility we avoid doing it at runtime.
        __pydantic_extra__: Dict[str, object] = FieldInfo(init=False)  # pyright: ignore[reportIncompatibleVariableOverride]

        # Stub to indicate that arbitrary properties are accepted.
        # To access properties that are not valid identifiers you can use `getattr`, e.g.
        # `getattr(obj, '$type')`
        def __getattr__(self, attr: str) -> object: ...
    else:
        __pydantic_extra__: Dict[str, object]
