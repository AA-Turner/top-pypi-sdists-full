from enum import Enum
from functools import lru_cache
from typing import cast

from ..extensions import Enums


class DatetimeAppConfigItemType(Enums.KnownString):
    DATETIME = "datetime"

    def __str__(self) -> str:
        return str(self.value)

    @staticmethod
    @lru_cache(maxsize=None)
    def of_unknown(val: str) -> "DatetimeAppConfigItemType":
        if not isinstance(val, str):
            raise ValueError(f"Value of DatetimeAppConfigItemType must be a string (encountered: {val})")
        newcls = Enum("DatetimeAppConfigItemType", {"_UNKNOWN": val}, type=Enums.UnknownString)  # type: ignore
        return cast(DatetimeAppConfigItemType, getattr(newcls, "_UNKNOWN"))
