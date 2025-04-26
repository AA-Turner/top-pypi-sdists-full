from enum import Enum
from functools import lru_cache
from typing import cast

from ..extensions import Enums


class AppConfigItemBooleanUpdateType(Enums.KnownString):
    BOOLEAN = "boolean"

    def __str__(self) -> str:
        return str(self.value)

    @staticmethod
    @lru_cache(maxsize=None)
    def of_unknown(val: str) -> "AppConfigItemBooleanUpdateType":
        if not isinstance(val, str):
            raise ValueError(f"Value of AppConfigItemBooleanUpdateType must be a string (encountered: {val})")
        newcls = Enum("AppConfigItemBooleanUpdateType", {"_UNKNOWN": val}, type=Enums.UnknownString)  # type: ignore
        return cast(AppConfigItemBooleanUpdateType, getattr(newcls, "_UNKNOWN"))
