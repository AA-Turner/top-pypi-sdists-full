from typing import Optional, Text

import attr

from .config import AndroidVersion, IosVersion, ScreenOrientation


@attr.s
class DeviceTarget(object):
    device_name = attr.ib()  # type: Text
    screen_orientation = attr.ib(default=None)  # type: Optional[ScreenOrientation]

    def landscape(self):
        self.screen_orientation = ScreenOrientation.LANDSCAPE
        return self

    def portrait(self):
        self.screen_orientation = ScreenOrientation.PORTRAIT
        return self


@attr.s
class IosDeviceTarget(DeviceTarget):
    device_name = attr.ib()  # type: Text
    screen_orientation = attr.ib(
        default=ScreenOrientation.PORTRAIT, converter=ScreenOrientation
    )  # type: Optional[ScreenOrientation]
    version = attr.ib(
        default=None, converter=attr.converters.optional(IosVersion)
    )  # type: Optional[IosVersion]


@attr.s
class AndroidDeviceTarget(DeviceTarget):
    device_name = attr.ib()  # type: Text
    screen_orientation = attr.ib(
        default=ScreenOrientation.PORTRAIT, converter=ScreenOrientation
    )  # type: Optional[ScreenOrientation]
    version = attr.ib(
        default=None, converter=attr.converters.optional(AndroidVersion)
    )  # type: Optional[AndroidVersion]
