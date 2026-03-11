from __future__ import absolute_import, division, print_function, unicode_literals

from applitools.common import deprecated
from applitools.common.fluent.check_settings import CheckSettings, CheckSettingsValues
from applitools.common.fluent.region import (
    AccessibilityRegionByRectangle,
    FloatingRegionByRectangle,
    GetAccessibilityRegion,
    GetFloatingRegion,
    GetRegion,
    RegionByRectangle,
)

deprecated.module(__name__)
__all__ = (
    "AccessibilityRegionByRectangle",
    "CheckSettings",
    "CheckSettingsValues",
    "FloatingRegionByRectangle",
    "GetAccessibilityRegion",
    "GetFloatingRegion",
    "GetRegion",
    "RegionByRectangle",
)
