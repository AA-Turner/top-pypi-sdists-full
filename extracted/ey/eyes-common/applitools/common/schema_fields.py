from __future__ import absolute_import, division, print_function

import enum
from typing import TYPE_CHECKING

from . import (
    ChromeEmulationInfo,
    DesktopBrowserInfo,
    DiffsFoundError,
    IosDeviceInfo,
    NewTestError,
    TestFailedError,
)
from .context_vars import get_object_registry
from .errors import USDKFailure
from .extract_text import OCRRegion
from .fluent.region import (
    AccessibilityRegionByRectangle,
    AccessibilityRegionBySelector,
    DynamicRegionByRectangle,
    DynamicRegionBySelector,
    FloatingRegionByRectangle,
    FloatingRegionBySelector,
    RegionByRectangle,
    RegionBySelector,
)
from .fluent.target_path import RegionLocator
from .layout_breakpoints_options import LayoutBreakpointsOptions as LBO
from .mmallow import Dict, Raw
from .optional_deps import StaleElementReferenceException
from .ultrafastgrid import AndroidDeviceInfo

if TYPE_CHECKING:
    import typing as t

    from . import config as cfg
    from . import ultrafastgrid as ufg
    from .fluent import region, target_path
    from .fluent import web_check_settings as cs
    from .selenium import misc as selenium_misc


class Enum(Raw):
    # Customize the error message so that it matches the expected output.
    default_error_messages = {"invalid": "is not a valid {enum_name}"}

    def __init__(self, enum_type, data_key=None, attribute=None):
        # enum_type is the expected enum (e.g. StitchMode)
        super().__init__(data_key=data_key, attribute=attribute)
        self.enum_type = enum_type

    def _serialize(self, value, attr, obj, *args, **kwargs):
        """
        Converts the enum instance (or a raw compatible value) into its underlying value.
        Accepts:
          - None: returns None.
          - An instance of the expected enum type: returns its .value.
          - An instance of a different enum: attempts to convert it using its .value.
          - A raw value: attempts to convert it to the expected enum.
        If conversion fails, self.fail() is called.
        """
        if value is None:
            return None
        try:
            if isinstance(value, self.enum_type):
                # Value is already an instance of the expected enum.
                return value.value
            elif isinstance(value, enum.Enum):
                # Value is an enum of a different type.
                # * robotframework library defines customized enums like RobotStitchMode
                # Try to create an instance of the expected enum using its .value.
                return self.enum_type(value.value).value
            else:
                # Accept raw values.
                return self.enum_type(value).value
        except ValueError:
            raise self.make_error("invalid", enum_name=self.enum_type.__name__)

    def _deserialize(self, value, attr, data, *args, **kwargs):
        if value is None:
            return None
        try:
            return self.enum_type(value)
        except ValueError:
            raise self.make_error("invalid", enum_name=self.enum_type.__name__)


class Error(Raw):
    def _deserialize(self, value, attr, data, *args, **kwargs):
        # type: (dict, t.Any, t.Any, *t.Any) -> Exception
        return demarshal_error(value)


class DebugScreenshots(Raw):
    _CHECK_ATTRIBUTE = False

    def _serialize(self, _, __, config, *args, **kwargs):
        # type: (t.Any, t.Any, cfg.Configuration, *t.Any, **t.Any) -> dict
        from .schema import DebugScreenshotHandler

        if config.save_debug_screenshots:
            return DebugScreenshotHandler().dump(config)


class EnvironmentRaw(Raw):
    _CHECK_ATTRIBUTE = False

    def _serialize(self, _, __, config, *args, **kwargs):
        # type: (t.Any, t.Any, cfg.Configuration, *t.Any, **t.Any) -> dict
        from .schema import Environment

        return Environment().dump(config)


class VisualGridOptions(Raw):
    def _serialize(self, value, *args, **kwargs):
        # type: (t.Optional[t.List[ufg.VisualGridOption]], *t.Any, **t.Any) -> t.Optional[dict]
        if value is not None:
            return {r.key: r.value for r in value}
        else:
            return None


class ElementReference(Dict):
    def _serialize(self, locator, *args, **kwargs):
        # type: (t.Any, target_path.TargetPathLocator, *t.Any, **t.Any) -> t.Optional[dict]
        return None if locator is None else locator.to_dict(get_object_registry())


class MobileOptions(Dict):
    def _serialize(self, obj, *args, **kwargs):
        # type: (t.Any, selenium_misc.MobileOptions, t.Any) -> t.Optional[dict]
        if getattr(obj, "keep_navigation_bar", None) is not None:
            return {"keepNavigationBar": obj.keep_navigation_bar}
        return None


class FrameReference(Raw):
    _CHECK_ATTRIBUTE = False

    def _serialize(self, _, __, frame, *args, **kwargs):
        # type: (t.Any, t.Any, cs.FrameLocator,*t.Any, **t.Any) -> t.Union[int, t.Text, dict]
        if frame.frame_index is not None:
            return frame.frame_index
        elif frame.frame_name_or_id is not None:
            return frame.frame_name_or_id
        else:
            return frame.frame_locator.to_dict(get_object_registry())


class LayoutBreakpoints(Raw):
    """This custom field serializer is needed to provide backward compatibility with
    code that explicitly sets value of layout_breakpoints configuration attribute"""

    def _serialize(self, lbo, *args, **kwargs):
        # type: (t.Union[bool, list, tuple, LBO], *t.Any, **t.Any) -> dict
        if isinstance(lbo, (bool, list)):
            lbo = LBO(lbo)
        elif isinstance(lbo, tuple):
            lbo = LBO(list(lbo))
        from .schema import LayoutBreakpointsOptions

        res = LayoutBreakpointsOptions().dump(lbo)
        return res


class NormalizationRaw(Raw):
    _CHECK_ATTRIBUTE = False

    def _serialize(self, _, __, config, *args, **kwargs):
        from .schema import Normalization

        return Normalization().dump(config)


class StitchOverlap(Raw):
    def _serialize(self, value, *args, **kwargs):
        # type: (t.Any, int, *t.Any, **t.Any) -> dict
        if value is not None:
            return {"bottom": value}


class TargetReference(Raw):
    _CHECK_ATTRIBUTE = False  # it might be target_locator or target_region

    def _serialize(self, _, __, check_settings, *args, **kwargs):
        # type: (t.Any, t.Any, cs.WebCheckSettingsValues, *t.Any, **t.Any) -> t.Optional[dict]
        if check_settings.target_locator:
            return check_settings.target_locator.to_dict(get_object_registry())
        elif check_settings.target_region:
            from .schema import Region

            return Region().dump(check_settings.target_region)
        else:
            return None


class RegionReference(Raw):
    _CHECK_ATTRIBUTE = False

    def _serialize(self, _, __, obj, *args, **kwargs):
        # type: (t.Any, t.Any, t.Union[region.GetRegion, OCRRegion], *t.Any, **t.Any) -> dict
        from .schema import Region

        if isinstance(
            obj,
            (
                RegionBySelector,
                FloatingRegionBySelector,
                AccessibilityRegionBySelector,
                DynamicRegionBySelector,
            ),
        ):
            return obj._target_path.to_dict(get_object_registry())  # noqa
        elif isinstance(obj, RegionByRectangle):
            return Region().dump(obj._region)  # noqa
        elif isinstance(
            obj,
            (
                FloatingRegionByRectangle,
                AccessibilityRegionByRectangle,
                DynamicRegionByRectangle,
            ),
        ):
            return Region().dump(obj._rect)  # noqa
        elif isinstance(obj, OCRRegion):
            if isinstance(obj.target, RegionLocator):
                return obj.target.to_dict(get_object_registry())
            else:
                return Region().dump(obj.target)
        else:
            raise RuntimeError("Unexpected region type", type(obj))


class BrowserInfo(Raw):
    def _serialize(self, value, *args, **kwargs):
        # type: (ufg.IRenderBrowserInfo, *t.Any, **t.Any) -> dict
        if isinstance(value, DesktopBrowserInfo):
            from .schema import DesktopBrowserRenderer

            return DesktopBrowserRenderer().dump(value)
        elif isinstance(value, ChromeEmulationInfo):
            from .schema import ChromeEmulationRenderer

            return {"chromeEmulationInfo": ChromeEmulationRenderer().dump(value)}
        elif isinstance(value, IosDeviceInfo):
            from .schema import IosDeviceRenderer

            return {"iosDeviceInfo": IosDeviceRenderer().dump(value)}
        elif isinstance(value, AndroidDeviceInfo):
            from .schema import AndroidDeviceRenderer

            return {"androidDeviceInfo": AndroidDeviceRenderer().dump(value)}
        else:
            raise RuntimeError("Unexpected BrowserInfo type", type(value))

    def _deserialize(self, value, *args, **kwargs):
        # type: (t.Optional[dict], *t.Any, **t.Any) -> t.Optional[ufg.IRenderBrowserInfo]
        if value is None or "requested" not in value:
            return None
        value = value["requested"]
        if "iosDeviceInfo" in value:
            from .schema import IosDeviceRenderer

            return IosDeviceRenderer().load(value["iosDeviceInfo"])
        elif "chromeEmulationInfo" in value:
            from .schema import ChromeEmulationRenderer

            return ChromeEmulationRenderer().load(value["chromeEmulationInfo"])
        elif "androidDeviceInfo" in value:
            from .schema import AndroidDeviceRenderer

            return AndroidDeviceRenderer().load(value["androidDeviceInfo"])
        elif "environment" in value:
            from .schema import EnvironmentRenderer

            return EnvironmentRenderer().load(value["environment"])
        elif "name" in value and "width" in value and "height" in value:
            from .schema import DesktopBrowserRenderer

            return DesktopBrowserRenderer().load(value)
        else:
            # According to core team unknown types should be ignored
            return None


def demarshal_error(error_dict):
    # type: (dict) -> Exception
    message = error_dict["message"]
    if message.startswith("stale element reference"):
        return StaleElementReferenceException(message)
    elif error_dict.get("reason") in _matching_failures:
        return _matching_failures[error_dict["reason"]](message)
    else:
        stack = error_dict["stack"]
        if message:  # Sometimes when internal error occurs the message is empty
            # There is usually a copy of message in stack trace too, remove it
            stack = stack.split(message)[-1].strip("\n")
        return USDKFailure(message, stack)


_matching_failures = {
    "test different": DiffsFoundError,
    "test failed": TestFailedError,
    "test new": NewTestError,
}
