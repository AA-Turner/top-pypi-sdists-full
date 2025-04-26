from enum import Enum
from functools import lru_cache
from typing import cast

from ..extensions import Enums


class FloatAppConfigItemType(Enums.KnownString):
    FLOAT = "float"

    def __str__(self) -> str:
        return str(self.value)

    @staticmethod
    @lru_cache(maxsize=None)
    def of_unknown(val: str) -> "FloatAppConfigItemType":
        if not isinstance(val, str):
            raise ValueError(f"Value of FloatAppConfigItemType must be a string (encountered: {val})")
        newcls = Enum("FloatAppConfigItemType", {"_UNKNOWN": val}, type=Enums.UnknownString)  # type: ignore
        return cast(FloatAppConfigItemType, getattr(newcls, "_UNKNOWN"))
