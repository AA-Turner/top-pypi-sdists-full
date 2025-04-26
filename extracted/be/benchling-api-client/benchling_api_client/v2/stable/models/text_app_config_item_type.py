from enum import Enum
from functools import lru_cache
from typing import cast

from ..extensions import Enums


class TextAppConfigItemType(Enums.KnownString):
    TEXT = "text"

    def __str__(self) -> str:
        return str(self.value)

    @staticmethod
    @lru_cache(maxsize=None)
    def of_unknown(val: str) -> "TextAppConfigItemType":
        if not isinstance(val, str):
            raise ValueError(f"Value of TextAppConfigItemType must be a string (encountered: {val})")
        newcls = Enum("TextAppConfigItemType", {"_UNKNOWN": val}, type=Enums.UnknownString)  # type: ignore
        return cast(TextAppConfigItemType, getattr(newcls, "_UNKNOWN"))
