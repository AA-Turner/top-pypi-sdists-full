from enum import Enum
from functools import lru_cache
from typing import cast

from ..extensions import Enums


class MafftOptionsAdjustDirection(Enums.KnownString):
    FAST = "fast"
    ACCURATE = "accurate"
    DISABLED = "disabled"

    def __str__(self) -> str:
        return str(self.value)

    @staticmethod
    @lru_cache(maxsize=None)
    def of_unknown(val: str) -> "MafftOptionsAdjustDirection":
        if not isinstance(val, str):
            raise ValueError(f"Value of MafftOptionsAdjustDirection must be a string (encountered: {val})")
        newcls = Enum("MafftOptionsAdjustDirection", {"_UNKNOWN": val}, type=Enums.UnknownString)  # type: ignore
        return cast(MafftOptionsAdjustDirection, getattr(newcls, "_UNKNOWN"))
