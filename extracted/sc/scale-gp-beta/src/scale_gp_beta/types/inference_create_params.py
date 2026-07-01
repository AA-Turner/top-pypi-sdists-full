# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Dict
from typing_extensions import Required, TypedDict

from .launch_inference_configuration_param import LaunchInferenceConfigurationParam

__all__ = ["InferenceCreateParams"]


class InferenceCreateParams(TypedDict, total=False):
    model: Required[str]
    """model specified as `vendor/name` (ex. openai/gpt-5)"""

    args: Dict[str, object]
    """Arguments passed into model"""

    inference_configuration: LaunchInferenceConfigurationParam
    """Vendor specific configuration"""
