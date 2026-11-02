# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Dict
from typing_extensions import Literal, Required, TypedDict

from .wandb_image_mask_v1_param import WandbImageMaskV1Param
from .wandb_image_boxes_v1_param import WandbImageBoxesV1Param

__all__ = ["WandbImageV1Param"]


class WandbImageV1Param(TypedDict, total=False, extra_items=object):  # type: ignore[call-arg]
    """A V1 W&B image value in an evaluation input or output field.

    Row comparison across EvaluationVersions matches this value by every property except `uri`. An empty optional property matches a missing one.
    """

    extension_type: Required[Literal["wandb-image"]]

    format: Required[str]

    schema_version: Required[Literal[1]]

    sha256: Required[str]

    size: Required[int]

    uri: Required[str]
    """Row comparison across EvaluationVersions ignores this property."""

    wb_media_type: Required[Literal["image-file"]]

    boxes: Dict[str, WandbImageBoxesV1Param]

    caption: str

    height: int

    masks: Dict[str, WandbImageMaskV1Param]

    width: int
