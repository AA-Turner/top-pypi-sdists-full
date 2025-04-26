from enum import Enum
from functools import lru_cache
from typing import cast

from ..extensions import Enums


class TableUiBlockType(Enums.KnownString):
    TABLE = "TABLE"

    def __str__(self) -> str:
        return str(self.value)

    @staticmethod
    @lru_cache(maxsize=None)
    def of_unknown(val: str) -> "TableUiBlockType":
        if not isinstance(val, str):
            raise ValueError(f"Value of TableUiBlockType must be a string (encountered: {val})")
        newcls = Enum("TableUiBlockType", {"_UNKNOWN": val}, type=Enums.UnknownString)  # type: ignore
        return cast(TableUiBlockType, getattr(newcls, "_UNKNOWN"))
