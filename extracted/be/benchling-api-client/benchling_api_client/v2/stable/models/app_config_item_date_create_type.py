from enum import Enum
from functools import lru_cache
from typing import cast

from ..extensions import Enums


class AppConfigItemDateCreateType(Enums.KnownString):
    DATE = "date"

    def __str__(self) -> str:
        return str(self.value)

    @staticmethod
    @lru_cache(maxsize=None)
    def of_unknown(val: str) -> "AppConfigItemDateCreateType":
        if not isinstance(val, str):
            raise ValueError(f"Value of AppConfigItemDateCreateType must be a string (encountered: {val})")
        newcls = Enum("AppConfigItemDateCreateType", {"_UNKNOWN": val}, type=Enums.UnknownString)  # type: ignore
        return cast(AppConfigItemDateCreateType, getattr(newcls, "_UNKNOWN"))
