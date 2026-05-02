# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List

from ..._models import BaseModel
from .device_object import DeviceObject

__all__ = ["PlayerGetDevicesResponse"]


class PlayerGetDevicesResponse(BaseModel):
    devices: List[DeviceObject]
