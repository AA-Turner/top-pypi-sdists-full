from enum import Enum
from functools import lru_cache
from typing import cast

from ..extensions import Enums


class DropdownMultiValueUiBlockType(Enums.KnownString):
    DROPDOWN_MULTIVALUE = "DROPDOWN_MULTIVALUE"

    def __str__(self) -> str:
        return str(self.value)

    @staticmethod
    @lru_cache(maxsize=None)
    def of_unknown(val: str) -> "DropdownMultiValueUiBlockType":
        if not isinstance(val, str):
            raise ValueError(f"Value of DropdownMultiValueUiBlockType must be a string (encountered: {val})")
        newcls = Enum("DropdownMultiValueUiBlockType", {"_UNKNOWN": val}, type=Enums.UnknownString)  # type: ignore
        return cast(DropdownMultiValueUiBlockType, getattr(newcls, "_UNKNOWN"))
