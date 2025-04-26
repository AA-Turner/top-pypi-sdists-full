from enum import Enum
from functools import lru_cache
from typing import cast

from ..extensions import Enums


class UnitTypeTermValue(Enums.KnownString):
    TIME = "TIME"
    LENGTH = "LENGTH"
    MASS = "MASS"
    CURRENT = "CURRENT"
    TEMPERATURE = "TEMPERATURE"
    AMOUNT = "AMOUNT"
    LUMINOUS_INTENSITY = "LUMINOUS_INTENSITY"

    def __str__(self) -> str:
        return str(self.value)

    @staticmethod
    @lru_cache(maxsize=None)
    def of_unknown(val: str) -> "UnitTypeTermValue":
        if not isinstance(val, str):
            raise ValueError(f"Value of UnitTypeTermValue must be a string (encountered: {val})")
        newcls = Enum("UnitTypeTermValue", {"_UNKNOWN": val}, type=Enums.UnknownString)  # type: ignore
        return cast(UnitTypeTermValue, getattr(newcls, "_UNKNOWN"))
