from enum import Enum
from functools import lru_cache
from typing import cast

from ..extensions import Enums


class ArrayElementAppConfigItemType(Enums.KnownString):
    ARRAY_ELEMENT = "array_element"

    def __str__(self) -> str:
        return str(self.value)

    @staticmethod
    @lru_cache(maxsize=None)
    def of_unknown(val: str) -> "ArrayElementAppConfigItemType":
        if not isinstance(val, str):
            raise ValueError(f"Value of ArrayElementAppConfigItemType must be a string (encountered: {val})")
        newcls = Enum("ArrayElementAppConfigItemType", {"_UNKNOWN": val}, type=Enums.UnknownString)  # type: ignore
        return cast(ArrayElementAppConfigItemType, getattr(newcls, "_UNKNOWN"))
