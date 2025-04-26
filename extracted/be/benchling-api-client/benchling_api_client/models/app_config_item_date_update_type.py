from enum import Enum
from functools import lru_cache
from typing import cast

from ..extensions import Enums


class AppConfigItemDateUpdateType(Enums.KnownString):
    DATE = "date"

    def __str__(self) -> str:
        return str(self.value)

    @staticmethod
    @lru_cache(maxsize=None)
    def of_unknown(val: str) -> "AppConfigItemDateUpdateType":
        if not isinstance(val, str):
            raise ValueError(f"Value of AppConfigItemDateUpdateType must be a string (encountered: {val})")
        newcls = Enum("AppConfigItemDateUpdateType", {"_UNKNOWN": val}, type=Enums.UnknownString)  # type: ignore
        return cast(AppConfigItemDateUpdateType, getattr(newcls, "_UNKNOWN"))
