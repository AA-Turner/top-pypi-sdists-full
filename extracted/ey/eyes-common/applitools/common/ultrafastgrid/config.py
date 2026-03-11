from __future__ import absolute_import, division, print_function

from enum import Enum
from typing import Any, Text

from ..utils.general_utils import DeprecatedEnumVariant
from .device_name import DeviceName
from .ios_device_name import IosDeviceName


class ScreenOrientation(Enum):
    PORTRAIT = "portrait"
    LANDSCAPE = "landscape"


class IosVersion(Enum):
    LATEST = "latest"
    ONE_VERSION_BACK = "latest-1"


class AndroidVersion(Enum):
    LATEST = "latest"
    ONE_VERSION_BACK = "latest-1"


class VisualGridOption(object):
    def __init__(self, key, value):
        # type: (Text, Any) -> None
        self.key = key
        self.value = value

    def __eq__(self, other):
        # type: (VisualGridOption) -> bool
        return other and self.key == other.key and self.value == other.value
