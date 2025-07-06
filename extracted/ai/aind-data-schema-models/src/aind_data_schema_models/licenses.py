"""Module for definition of software and data licenses"""

from enum import Enum


class License(str, Enum):
    """Licenses"""

    MIT = "MIT"
    CC_BY_40 = "CC-BY-4.0"
