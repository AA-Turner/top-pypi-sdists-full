from enum import Enum
from functools import lru_cache
from typing import cast

from ..extensions import Enums


class FieldAppConfigItemType(Enums.KnownString):
    FIELD = "field"

    def __str__(self) -> str:
        return str(self.value)

    @staticmethod
    @lru_cache(maxsize=None)
    def of_unknown(val: str) -> "FieldAppConfigItemType":
        if not isinstance(val, str):
            raise ValueError(f"Value of FieldAppConfigItemType must be a string (encountered: {val})")
        newcls = Enum("FieldAppConfigItemType", {"_UNKNOWN": val}, type=Enums.UnknownString)  # type: ignore
        return cast(FieldAppConfigItemType, getattr(newcls, "_UNKNOWN"))
