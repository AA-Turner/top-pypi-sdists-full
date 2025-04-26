from enum import Enum
from functools import lru_cache
from typing import cast

from ..extensions import Enums


class AppConfigItemIntegerUpdateType(Enums.KnownString):
    INTEGER = "integer"

    def __str__(self) -> str:
        return str(self.value)

    @staticmethod
    @lru_cache(maxsize=None)
    def of_unknown(val: str) -> "AppConfigItemIntegerUpdateType":
        if not isinstance(val, str):
            raise ValueError(f"Value of AppConfigItemIntegerUpdateType must be a string (encountered: {val})")
        newcls = Enum("AppConfigItemIntegerUpdateType", {"_UNKNOWN": val}, type=Enums.UnknownString)  # type: ignore
        return cast(AppConfigItemIntegerUpdateType, getattr(newcls, "_UNKNOWN"))
