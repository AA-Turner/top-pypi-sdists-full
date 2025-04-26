from enum import Enum
from functools import lru_cache
from typing import cast

from ..extensions import Enums


class BooleanAppConfigItemType(Enums.KnownString):
    BOOLEAN = "boolean"

    def __str__(self) -> str:
        return str(self.value)

    @staticmethod
    @lru_cache(maxsize=None)
    def of_unknown(val: str) -> "BooleanAppConfigItemType":
        if not isinstance(val, str):
            raise ValueError(f"Value of BooleanAppConfigItemType must be a string (encountered: {val})")
        newcls = Enum("BooleanAppConfigItemType", {"_UNKNOWN": val}, type=Enums.UnknownString)  # type: ignore
        return cast(BooleanAppConfigItemType, getattr(newcls, "_UNKNOWN"))
