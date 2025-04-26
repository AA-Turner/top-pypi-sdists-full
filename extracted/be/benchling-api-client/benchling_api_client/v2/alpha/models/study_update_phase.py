from enum import Enum
from functools import lru_cache
from typing import cast

from ..extensions import Enums


class StudyUpdatePhase(Enums.KnownString):
    DESIGN = "DESIGN"
    EXECUTION = "EXECUTION"
    COMPLETE = "COMPLETE"

    def __str__(self) -> str:
        return str(self.value)

    @staticmethod
    @lru_cache(maxsize=None)
    def of_unknown(val: str) -> "StudyUpdatePhase":
        if not isinstance(val, str):
            raise ValueError(f"Value of StudyUpdatePhase must be a string (encountered: {val})")
        newcls = Enum("StudyUpdatePhase", {"_UNKNOWN": val}, type=Enums.UnknownString)  # type: ignore
        return cast(StudyUpdatePhase, getattr(newcls, "_UNKNOWN"))
