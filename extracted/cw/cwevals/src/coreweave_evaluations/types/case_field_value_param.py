# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Dict, Union, Iterable, Optional
from typing_extensions import TypeAlias

from .wandb_audio_v1_param import WandbAudioV1Param
from .wandb_image_v1_param import WandbImageV1Param
from .wandb_video_v1_param import WandbVideoV1Param

__all__ = ["CaseFieldValueParam"]

CaseFieldValueParam: TypeAlias = Union[
    WandbImageV1Param,
    WandbAudioV1Param,
    WandbVideoV1Param,
    bool,
    float,
    str,
    Iterable[object],
    Dict[str, object],
    Optional[object],
]
