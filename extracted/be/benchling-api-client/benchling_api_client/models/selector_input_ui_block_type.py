from enum import Enum
from functools import lru_cache
from typing import cast

from ..extensions import Enums


class SelectorInputUiBlockType(Enums.KnownString):
    SELECTOR_INPUT = "SELECTOR_INPUT"

    def __str__(self) -> str:
        return str(self.value)

    @staticmethod
    @lru_cache(maxsize=None)
    def of_unknown(val: str) -> "SelectorInputUiBlockType":
        if not isinstance(val, str):
            raise ValueError(f"Value of SelectorInputUiBlockType must be a string (encountered: {val})")
        newcls = Enum("SelectorInputUiBlockType", {"_UNKNOWN": val}, type=Enums.UnknownString)  # type: ignore
        return cast(SelectorInputUiBlockType, getattr(newcls, "_UNKNOWN"))
