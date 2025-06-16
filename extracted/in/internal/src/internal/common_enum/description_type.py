from enum import Enum


class DescriptionTypeEnum(str, Enum):
    ALERT = "alert"
    TEXT = "text"
    LINE = "line"
