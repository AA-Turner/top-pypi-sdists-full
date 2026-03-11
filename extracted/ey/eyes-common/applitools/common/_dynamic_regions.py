from enum import Enum
from typing import Text, Union

import attr

from applitools.common.utils.general_utils import CustomEnumMethod

__all__ = ("DynamicTextType", "DynamicSettings")


@attr.s(slots=True)
class DynamicSettings:
    ignore_patterns = attr.ib(type=str, factory=list)

    @classmethod
    def from_(cls, dynamic_text_or_patterns):
        obj = cls()
        for pattern in dynamic_text_or_patterns:
            if isinstance(pattern, str):
                obj.ignore_patterns.append(pattern)
            elif isinstance(pattern, DynamicTextType):
                obj.ignore_patterns.append(pattern.value)
        return obj

    def to_dict(self):
        return attr.asdict(self)


class DynamicTextType(Enum):
    TextField = "TextField"
    Number = "Number"
    Date = "Date"
    Link = "Link"
    Email = "Email"
    Currency = "Currency"

    @CustomEnumMethod
    def Custom(cls, pattern):
        # type: (Text) -> Text
        """Set desired pattern"""
        return pattern


DynamicTextTypeOrPattern = Union[DynamicTextType, str]
