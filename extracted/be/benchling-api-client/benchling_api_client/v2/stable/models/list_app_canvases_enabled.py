from enum import Enum
from functools import lru_cache
from typing import cast

from ..extensions import Enums


class ListAppCanvasesEnabled(Enums.KnownString):
    TRUE = "true"
    FALSE = "false"

    def __str__(self) -> str:
        return str(self.value)

    @staticmethod
    @lru_cache(maxsize=None)
    def of_unknown(val: str) -> "ListAppCanvasesEnabled":
        if not isinstance(val, str):
            raise ValueError(f"Value of ListAppCanvasesEnabled must be a string (encountered: {val})")
        newcls = Enum("ListAppCanvasesEnabled", {"_UNKNOWN": val}, type=Enums.UnknownString)  # type: ignore
        return cast(ListAppCanvasesEnabled, getattr(newcls, "_UNKNOWN"))
