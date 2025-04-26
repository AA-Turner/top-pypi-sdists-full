from enum import Enum
from functools import lru_cache
from typing import cast

from ..extensions import Enums


class AppSessionMessageStyle(Enums.KnownString):
    ERROR = "ERROR"
    INFO = "INFO"
    NONE = "NONE"
    SUCCESS = "SUCCESS"
    WARNING = "WARNING"

    def __str__(self) -> str:
        return str(self.value)

    @staticmethod
    @lru_cache(maxsize=None)
    def of_unknown(val: str) -> "AppSessionMessageStyle":
        if not isinstance(val, str):
            raise ValueError(f"Value of AppSessionMessageStyle must be a string (encountered: {val})")
        newcls = Enum("AppSessionMessageStyle", {"_UNKNOWN": val}, type=Enums.UnknownString)  # type: ignore
        return cast(AppSessionMessageStyle, getattr(newcls, "_UNKNOWN"))
