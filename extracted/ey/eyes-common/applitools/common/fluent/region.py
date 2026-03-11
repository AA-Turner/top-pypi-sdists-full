from __future__ import absolute_import, division, print_function

from typing import TYPE_CHECKING

import attr

from applitools.common._dynamic_regions import DynamicSettings

from ..accessibility import AccessibilityRegionType
from ..geometry import AccessibilityRegion, DynamicRegion, Rectangle, Region
from ..match import FloatingBounds

if TYPE_CHECKING:
    from typing import Optional, Text, Union

    from ..utils.custom_types import CodedRegionPadding
    from .target_path import RegionLocator

__all__ = (
    "AccessibilityRegionByRectangle",
    "AccessibilityRegionBySelector",
    "FloatingRegionByRectangle",
    "FloatingRegionBySelector",
    "GetAccessibilityRegion",
    "GetFloatingRegion",
    "GetRegion",
    "RegionByRectangle",
    "RegionBySelector",
    "GetDynamicRegion",
    "DynamicRegionBySelector",
    "DynamicRegionByRectangle",
)


class GetRegion(object):
    pass


@attr.s
class RegionByRectangle(GetRegion):
    _region = attr.ib()  # type: Union[Region, Rectangle]


@attr.s
class RegionBySelector(GetRegion):
    _target_path = attr.ib()  # type: RegionLocator
    padding = attr.ib(default=None)  # type: Optional[CodedRegionPadding]
    region_id = attr.ib(default=None)  # type: Optional[Text]


class GetFloatingRegion(GetRegion):
    pass


@attr.s
class FloatingRegionByRectangle(GetFloatingRegion):
    _rect = attr.ib()  # type: Union[Region, Rectangle]
    _bounds = attr.ib()  # type: FloatingBounds

    @property
    def floating_bounds(self):
        return self._bounds


@attr.s
class FloatingRegionBySelector(GetFloatingRegion):
    _target_path = attr.ib()  # type: RegionLocator
    _bounds = attr.ib()  # type: FloatingBounds


class GetAccessibilityRegion(GetRegion):
    pass


@attr.s
class AccessibilityRegionByRectangle(GetAccessibilityRegion):
    _rect = attr.ib()  # type: Union[Region, Rectangle, AccessibilityRegion]
    _type = attr.ib(default=None)  # type: Optional[AccessibilityRegionType]

    @property
    def accessibility_type(self):
        # type: () -> AccessibilityRegionType
        if self._type:
            return self._type
        return self._rect.type


@attr.s
class AccessibilityRegionBySelector(GetAccessibilityRegion):
    _target_path = attr.ib()  # type: RegionLocator
    _type = attr.ib()  # type: AccessibilityRegionType


class GetDynamicRegion(GetRegion):
    pass


@attr.s
class DynamicRegionByRectangle(GetDynamicRegion):
    _rect = attr.ib()  # type: Union[Region, Rectangle, DynamicRegion]
    _dynamic_settings = attr.ib(default=None)  # type: Optional[DynamicSettings]
    padding = attr.ib(default=None)  # type: Optional[CodedRegionPadding]


@attr.s
class DynamicRegionBySelector(GetDynamicRegion):
    _target_path = attr.ib()  # type: RegionLocator
    _dynamic_settings = attr.ib(default=None)  # type: Optional[DynamicSettings]
    padding = attr.ib(default=None)  # type: Optional[CodedRegionPadding]
