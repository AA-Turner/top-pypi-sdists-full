from enum import Enum
from functools import lru_cache
from typing import cast

from ..extensions import Enums


class JsonAppConfigItemType(Enums.KnownString):
    JSON = "json"

    def __str__(self) -> str:
        return str(self.value)

    @staticmethod
    @lru_cache(maxsize=None)
    def of_unknown(val: str) -> "JsonAppConfigItemType":
        if not isinstance(val, str):
            raise ValueError(f"Value of JsonAppConfigItemType must be a string (encountered: {val})")
        newcls = Enum("JsonAppConfigItemType", {"_UNKNOWN": val}, type=Enums.UnknownString)  # type: ignore
        return cast(JsonAppConfigItemType, getattr(newcls, "_UNKNOWN"))
