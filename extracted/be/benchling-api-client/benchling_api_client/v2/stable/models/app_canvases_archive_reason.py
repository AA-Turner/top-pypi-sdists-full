from enum import Enum
from functools import lru_cache
from typing import cast

from ..extensions import Enums


class AppCanvasesArchiveReason(Enums.KnownString):
    OTHER = "Other"

    def __str__(self) -> str:
        return str(self.value)

    @staticmethod
    @lru_cache(maxsize=None)
    def of_unknown(val: str) -> "AppCanvasesArchiveReason":
        if not isinstance(val, str):
            raise ValueError(f"Value of AppCanvasesArchiveReason must be a string (encountered: {val})")
        newcls = Enum("AppCanvasesArchiveReason", {"_UNKNOWN": val}, type=Enums.UnknownString)  # type: ignore
        return cast(AppCanvasesArchiveReason, getattr(newcls, "_UNKNOWN"))
