from enum import Enum
from functools import lru_cache
from typing import cast

from ..extensions import Enums


class StudyPhase(Enums.KnownString):
    DESIGN = "DESIGN"
    EXECUTION = "EXECUTION"
    COMPLETE = "COMPLETE"

    def __str__(self) -> str:
        return str(self.value)

    @staticmethod
    @lru_cache(maxsize=None)
    def of_unknown(val: str) -> "StudyPhase":
        if not isinstance(val, str):
            raise ValueError(f"Value of StudyPhase must be a string (encountered: {val})")
        newcls = Enum("StudyPhase", {"_UNKNOWN": val}, type=Enums.UnknownString)  # type: ignore
        return cast(StudyPhase, getattr(newcls, "_UNKNOWN"))
