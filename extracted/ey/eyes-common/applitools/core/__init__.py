from __future__ import absolute_import, division, print_function, unicode_literals

from ..common import deprecated
from ..common.batch_close import BatchClose
from ..common.cut import FixedCutProvider, NullCutProvider, UnscaledFixedCutProvider
from ..common.extract_text import TextRegionSettings
from ..common.feature import Feature
from ..common.fluent import (
    CheckSettings,
    CheckSettingsValues,
    FloatingRegionByRectangle,
    GetFloatingRegion,
    GetRegion,
    RegionByRectangle,
)
from ..common.locators import VisualLocator, VisualLocatorSettings
from ..common.triggers import MouseTrigger, TextTrigger

deprecated.module(__name__)
__all__ = (
    "BatchClose",
    "CheckSettings",
    "CheckSettingsValues",
    "Feature",
    "FixedCutProvider",
    "FloatingRegionByRectangle",
    "GetFloatingRegion",
    "GetRegion",
    "MouseTrigger",
    "NullCutProvider",
    "RegionByRectangle",
    "TextRegionSettings",
    "TextTrigger",
    "UnscaledFixedCutProvider",
    "VisualLocator",
    "VisualLocatorSettings",
    "__version__",
)
