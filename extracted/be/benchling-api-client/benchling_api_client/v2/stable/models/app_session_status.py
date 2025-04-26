from enum import Enum
from functools import lru_cache
from typing import cast

from ..extensions import Enums


class AppSessionStatus(Enums.KnownString):
    COMPLETED_WITH_WARNINGS = "COMPLETED_WITH_WARNINGS"
    FAILED = "FAILED"
    RUNNING = "RUNNING"
    SUCCEEDED = "SUCCEEDED"
    TIMEOUT = "TIMEOUT"

    def __str__(self) -> str:
        return str(self.value)

    @staticmethod
    @lru_cache(maxsize=None)
    def of_unknown(val: str) -> "AppSessionStatus":
        if not isinstance(val, str):
            raise ValueError(f"Value of AppSessionStatus must be a string (encountered: {val})")
        newcls = Enum("AppSessionStatus", {"_UNKNOWN": val}, type=Enums.UnknownString)  # type: ignore
        return cast(AppSessionStatus, getattr(newcls, "_UNKNOWN"))
