from enum import Enum
from functools import lru_cache
from typing import cast

from ..extensions import Enums


class NestedFormFieldType(Enums.KnownString):
    FORM = "FORM"

    def __str__(self) -> str:
        return str(self.value)

    @staticmethod
    @lru_cache(maxsize=None)
    def of_unknown(val: str) -> "NestedFormFieldType":
        if not isinstance(val, str):
            raise ValueError(f"Value of NestedFormFieldType must be a string (encountered: {val})")
        newcls = Enum("NestedFormFieldType", {"_UNKNOWN": val}, type=Enums.UnknownString)  # type: ignore
        return cast(NestedFormFieldType, getattr(newcls, "_UNKNOWN"))
