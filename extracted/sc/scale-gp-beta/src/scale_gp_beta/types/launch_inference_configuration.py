# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional

from .._models import BaseModel

__all__ = ["LaunchInferenceConfiguration"]


class LaunchInferenceConfiguration(BaseModel):
    num_retries: Optional[int] = None

    timeout_seconds: Optional[int] = None
