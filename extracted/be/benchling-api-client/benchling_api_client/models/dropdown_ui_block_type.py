from enum import Enum
from functools import lru_cache
from typing import cast

from ..extensions import Enums


class DropdownUiBlockType(Enums.KnownString):
    DROPDOWN = "DROPDOWN"

    def __str__(self) -> str:
        return str(self.value)

    @staticmethod
    @lru_cache(maxsize=None)
    def of_unknown(val: str) -> "DropdownUiBlockType":
        if not isinstance(val, str):
            raise ValueError(f"Value of DropdownUiBlockType must be a string (encountered: {val})")
        newcls = Enum("DropdownUiBlockType", {"_UNKNOWN": val}, type=Enums.UnknownString)  # type: ignore
        return cast(DropdownUiBlockType, getattr(newcls, "_UNKNOWN"))
