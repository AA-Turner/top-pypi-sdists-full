from enum import Enum
from functools import lru_cache
from typing import cast

from ..extensions import Enums


class MatchBasesRequestArchiveReason(Enums.KnownString):
    NOT_ARCHIVED = "NOT_ARCHIVED"
    OTHER = "Other"
    ARCHIVED = "Archived"

    def __str__(self) -> str:
        return str(self.value)

    @staticmethod
    @lru_cache(maxsize=None)
    def of_unknown(val: str) -> "MatchBasesRequestArchiveReason":
        if not isinstance(val, str):
            raise ValueError(f"Value of MatchBasesRequestArchiveReason must be a string (encountered: {val})")
        newcls = Enum("MatchBasesRequestArchiveReason", {"_UNKNOWN": val}, type=Enums.UnknownString)  # type: ignore
        return cast(MatchBasesRequestArchiveReason, getattr(newcls, "_UNKNOWN"))
