from enum import Enum
from functools import lru_cache
from typing import cast

from ..extensions import Enums


class IntegerAppConfigItemType(Enums.KnownString):
    INTEGER = "integer"

    def __str__(self) -> str:
        return str(self.value)

    @staticmethod
    @lru_cache(maxsize=None)
    def of_unknown(val: str) -> "IntegerAppConfigItemType":
        if not isinstance(val, str):
            raise ValueError(f"Value of IntegerAppConfigItemType must be a string (encountered: {val})")
        newcls = Enum("IntegerAppConfigItemType", {"_UNKNOWN": val}, type=Enums.UnknownString)  # type: ignore
        return cast(IntegerAppConfigItemType, getattr(newcls, "_UNKNOWN"))
