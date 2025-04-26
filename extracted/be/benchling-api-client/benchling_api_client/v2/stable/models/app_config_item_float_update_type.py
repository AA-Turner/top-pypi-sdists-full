from enum import Enum
from functools import lru_cache
from typing import cast

from ..extensions import Enums


class AppConfigItemFloatUpdateType(Enums.KnownString):
    FLOAT = "float"

    def __str__(self) -> str:
        return str(self.value)

    @staticmethod
    @lru_cache(maxsize=None)
    def of_unknown(val: str) -> "AppConfigItemFloatUpdateType":
        if not isinstance(val, str):
            raise ValueError(f"Value of AppConfigItemFloatUpdateType must be a string (encountered: {val})")
        newcls = Enum("AppConfigItemFloatUpdateType", {"_UNKNOWN": val}, type=Enums.UnknownString)  # type: ignore
        return cast(AppConfigItemFloatUpdateType, getattr(newcls, "_UNKNOWN"))
