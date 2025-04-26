from enum import Enum
from functools import lru_cache
from typing import cast

from ..extensions import Enums


class DateAppConfigItemType(Enums.KnownString):
    DATE = "date"

    def __str__(self) -> str:
        return str(self.value)

    @staticmethod
    @lru_cache(maxsize=None)
    def of_unknown(val: str) -> "DateAppConfigItemType":
        if not isinstance(val, str):
            raise ValueError(f"Value of DateAppConfigItemType must be a string (encountered: {val})")
        newcls = Enum("DateAppConfigItemType", {"_UNKNOWN": val}, type=Enums.UnknownString)  # type: ignore
        return cast(DateAppConfigItemType, getattr(newcls, "_UNKNOWN"))
