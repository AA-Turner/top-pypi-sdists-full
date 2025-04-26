from enum import Enum
from functools import lru_cache
from typing import cast

from ..extensions import Enums


class AppCanvasNotePartType(Enums.KnownString):
    APP_CANVAS = "app_canvas"

    def __str__(self) -> str:
        return str(self.value)

    @staticmethod
    @lru_cache(maxsize=None)
    def of_unknown(val: str) -> "AppCanvasNotePartType":
        if not isinstance(val, str):
            raise ValueError(f"Value of AppCanvasNotePartType must be a string (encountered: {val})")
        newcls = Enum("AppCanvasNotePartType", {"_UNKNOWN": val}, type=Enums.UnknownString)  # type: ignore
        return cast(AppCanvasNotePartType, getattr(newcls, "_UNKNOWN"))
