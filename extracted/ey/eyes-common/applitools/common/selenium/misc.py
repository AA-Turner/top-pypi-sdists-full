from __future__ import absolute_import, division, print_function

from enum import Enum
from typing import Optional

import attr

from ..utils.general_utils import DeprecatedEnumVariant


class BrowserType(Enum):
    CHROME = "chrome"
    CHROME_ONE_VERSION_BACK = "chrome-one-version-back"
    CHROME_TWO_VERSIONS_BACK = "chrome-two-versions-back"
    FIREFOX = "firefox"
    FIREFOX_ONE_VERSION_BACK = "firefox-one-version-back"
    FIREFOX_TWO_VERSIONS_BACK = "firefox-two-versions-back"
    SAFARI = "safari"
    SAFARI_ONE_VERSION_BACK = "safari-one-version-back"
    SAFARI_TWO_VERSIONS_BACK = "safari-two-versions-back"
    IE_10 = "ie10"
    IE_11 = "ie11"
    EDGE_LEGACY = "edgelegacy"
    EDGE_CHROMIUM = "edgechromium"
    EDGE_CHROMIUM_ONE_VERSION_BACK = "edgechromium-one-version-back"
    EDGE_CHROMIUM_TWO_VERSIONS_BACK = "edgechromium-two-versions-back"

    @DeprecatedEnumVariant
    def EDGE(self):
        # type: () -> BrowserType
        """
        The `EDGE` option that is being used in your browsers configuration
        will soon be deprecated. Please change it to either `EDGE_LEGACY`
        for the legacy version or to `EDGE_CHROMIUM` for the
        new Chromium-based version.
        """
        return self.EDGE_LEGACY


class StitchMode(Enum):
    """
    The type of methods for stitching full-page screenshots.
    """

    Scroll = "Scroll"
    CSS = "CSS"


@attr.s
class MobileOptions(object):
    keep_navigation_bar = attr.ib(default=None)  # type: Optional[bool]
