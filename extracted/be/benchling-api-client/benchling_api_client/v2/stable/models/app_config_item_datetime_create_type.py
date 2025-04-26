from enum import Enum
from functools import lru_cache
from typing import cast

from ..extensions import Enums


class AppConfigItemDatetimeCreateType(Enums.KnownString):
    DATETIME = "datetime"

    def __str__(self) -> str:
        return str(self.value)

    @staticmethod
    @lru_cache(maxsize=None)
    def of_unknown(val: str) -> "AppConfigItemDatetimeCreateType":
        if not isinstance(val, str):
            raise ValueError(
                f"Value of AppConfigItemDatetimeCreateType must be a string (encountered: {val})"
            )
        newcls = Enum("AppConfigItemDatetimeCreateType", {"_UNKNOWN": val}, type=Enums.UnknownString)  # type: ignore
        return cast(AppConfigItemDatetimeCreateType, getattr(newcls, "_UNKNOWN"))
