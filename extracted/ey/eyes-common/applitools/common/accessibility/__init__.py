from __future__ import absolute_import, division, print_function

import attr

from .. import deprecated
from ._guidelines_version import AccessibilityGuidelinesVersion
from ._level import AccessibilityLevel
from ._region_type import AccessibilityRegionType
from ._status import AccessibilityStatus

__all__ = (
    "AccessibilityGuidelinesVersion",
    "AccessibilityLevel",
    "AccessibilityStatus",
    "AccessibilityRegionType",
    "AccessibilitySettings",
    "SessionAccessibilityStatus",
)


@attr.s(init=False)
class AccessibilitySettings(object):
    level = attr.ib(type=AccessibilityLevel)  # type: AccessibilityLevel
    guidelines_version = attr.ib(
        type=AccessibilityGuidelinesVersion
    )  # type: AccessibilityGuidelinesVersion

    def __init__(
        self,
        level,  # type: AccessibilityLevel
        guidelines_version,  # type: AccessibilityGuidelinesVersion
    ):
        # type: (...) -> None
        self.level = AccessibilityLevel(level)
        self.guidelines_version = AccessibilityGuidelinesVersion(guidelines_version)


@attr.s(init=False)
class SessionAccessibilityStatus(object):
    level = attr.ib(type=AccessibilityLevel)  # type: AccessibilityLevel
    version = attr.ib(
        type=AccessibilityGuidelinesVersion
    )  # type: AccessibilityGuidelinesVersion
    status = attr.ib(type=AccessibilityStatus)  # type: AccessibilityStatus

    def __init__(
        self,
        status,  # type: AccessibilityStatus
        level,  # type: AccessibilityLevel
        version,  # type: AccessibilityGuidelinesVersion
    ):
        self.level = AccessibilityLevel(level)
        self.version = AccessibilityGuidelinesVersion(version)
        self.status = AccessibilityStatus(status)

    @property
    @deprecated.attribute("use `version` instead")
    def guidelines_version(self):
        # type: () -> AccessibilityGuidelinesVersion
        return self.version
