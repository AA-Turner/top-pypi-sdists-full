# Copyright © 2026 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
from enum import Enum, auto


class Mode(Enum):
    OFF = auto()
    MONITOR = auto()
    BLOCK = auto()
    BLOCK_AT_PERIMETER = auto()
