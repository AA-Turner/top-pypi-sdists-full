from enum import Enum
from functools import lru_cache
from typing import cast

from ..extensions import Enums


class DateSelectionFormFieldType(Enums.KnownString):
    DATE_SELECTION = "DATE_SELECTION"

    def __str__(self) -> str:
        return str(self.value)

    @staticmethod
    @lru_cache(maxsize=None)
    def of_unknown(val: str) -> "DateSelectionFormFieldType":
        if not isinstance(val, str):
            raise ValueError(f"Value of DateSelectionFormFieldType must be a string (encountered: {val})")
        newcls = Enum("DateSelectionFormFieldType", {"_UNKNOWN": val}, type=Enums.UnknownString)  # type: ignore
        return cast(DateSelectionFormFieldType, getattr(newcls, "_UNKNOWN"))
