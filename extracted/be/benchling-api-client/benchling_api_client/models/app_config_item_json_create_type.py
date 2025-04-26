from enum import Enum
from functools import lru_cache
from typing import cast

from ..extensions import Enums


class AppConfigItemJsonCreateType(Enums.KnownString):
    JSON = "json"

    def __str__(self) -> str:
        return str(self.value)

    @staticmethod
    @lru_cache(maxsize=None)
    def of_unknown(val: str) -> "AppConfigItemJsonCreateType":
        if not isinstance(val, str):
            raise ValueError(f"Value of AppConfigItemJsonCreateType must be a string (encountered: {val})")
        newcls = Enum("AppConfigItemJsonCreateType", {"_UNKNOWN": val}, type=Enums.UnknownString)  # type: ignore
        return cast(AppConfigItemJsonCreateType, getattr(newcls, "_UNKNOWN"))
