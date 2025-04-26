from enum import Enum
from functools import lru_cache
from typing import cast

from ..extensions import Enums


class ChartNotePartType(Enums.KnownString):
    NOTE_LINKED_CHART = "note_linked_chart"

    def __str__(self) -> str:
        return str(self.value)

    @staticmethod
    @lru_cache(maxsize=None)
    def of_unknown(val: str) -> "ChartNotePartType":
        if not isinstance(val, str):
            raise ValueError(f"Value of ChartNotePartType must be a string (encountered: {val})")
        newcls = Enum("ChartNotePartType", {"_UNKNOWN": val}, type=Enums.UnknownString)  # type: ignore
        return cast(ChartNotePartType, getattr(newcls, "_UNKNOWN"))
