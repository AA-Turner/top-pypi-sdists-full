from enum import Enum


class LPRDirectionEnum(str, Enum):
    IN = "in"
    OUT = "out"
    UNKNOWN = "unknown"
