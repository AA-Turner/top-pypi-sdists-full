# coding=utf-8
# *** WARNING: this file was generated by pulumi-language-python. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import builtins
import builtins
from enum import Enum

__all__ = [
    'ZoneType',
]


class ZoneType(builtins.str, Enum):
    """
    The type of this DNS zone (Public or Private).
    """
    PUBLIC = "Public"
    PRIVATE = "Private"
