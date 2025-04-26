from enum import Enum
from functools import lru_cache
from typing import cast

from ..extensions import Enums


class ChipUiBlockType(Enums.KnownString):
    CHIP = "CHIP"

    def __str__(self) -> str:
        return str(self.value)

    @staticmethod
    @lru_cache(maxsize=None)
    def of_unknown(val: str) -> "ChipUiBlockType":
        if not isinstance(val, str):
            raise ValueError(f"Value of ChipUiBlockType must be a string (encountered: {val})")
        newcls = Enum("ChipUiBlockType", {"_UNKNOWN": val}, type=Enums.UnknownString)  # type: ignore
        return cast(ChipUiBlockType, getattr(newcls, "_UNKNOWN"))
