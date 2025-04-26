from enum import Enum
from functools import lru_cache
from typing import cast

from ..extensions import Enums


class StringSelectFormFieldFormFactor(Enums.KnownString):
    CLOUD_SELECT = "CLOUD_SELECT"
    SELECT_MENU = "SELECT_MENU"

    def __str__(self) -> str:
        return str(self.value)

    @staticmethod
    @lru_cache(maxsize=None)
    def of_unknown(val: str) -> "StringSelectFormFieldFormFactor":
        if not isinstance(val, str):
            raise ValueError(
                f"Value of StringSelectFormFieldFormFactor must be a string (encountered: {val})"
            )
        newcls = Enum("StringSelectFormFieldFormFactor", {"_UNKNOWN": val}, type=Enums.UnknownString)  # type: ignore
        return cast(StringSelectFormFieldFormFactor, getattr(newcls, "_UNKNOWN"))
