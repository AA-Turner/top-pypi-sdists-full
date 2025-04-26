from enum import Enum
from functools import lru_cache
from typing import cast

from ..extensions import Enums


class AppConfigItemDatetimeUpdateType(Enums.KnownString):
    DATETIME = "datetime"

    def __str__(self) -> str:
        return str(self.value)

    @staticmethod
    @lru_cache(maxsize=None)
    def of_unknown(val: str) -> "AppConfigItemDatetimeUpdateType":
        if not isinstance(val, str):
            raise ValueError(
                f"Value of AppConfigItemDatetimeUpdateType must be a string (encountered: {val})"
            )
        newcls = Enum("AppConfigItemDatetimeUpdateType", {"_UNKNOWN": val}, type=Enums.UnknownString)  # type: ignore
        return cast(AppConfigItemDatetimeUpdateType, getattr(newcls, "_UNKNOWN"))
