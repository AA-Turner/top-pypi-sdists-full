# GENERATED FILE #
from enum import Enum

from applitools.common.utils.general_utils import DeprecatedEnumVariant

__all__ = ("AndroidMultiDeviceTarget",)


class AndroidMultiDeviceTarget(Enum):
    def __call__(self):
        from ._device_target import AndroidDeviceTarget

        return AndroidDeviceTarget(self.value)

    Galaxy_S25 = "Galaxy S25"
    Galaxy_S25_Ultra = "Galaxy S25 Ultra"
    Pixel_9 = "Pixel 9"
