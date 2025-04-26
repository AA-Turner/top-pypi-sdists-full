from enum import Enum
from functools import lru_cache
from typing import cast

from ..extensions import Enums


class EntryReviewProcessType(Enums.KnownString):
    SELF_REVIEW = "SELF_REVIEW"
    SEQUENTIAL = "SEQUENTIAL"
    PARALLEL = "PARALLEL"

    def __str__(self) -> str:
        return str(self.value)

    @staticmethod
    @lru_cache(maxsize=None)
    def of_unknown(val: str) -> "EntryReviewProcessType":
        if not isinstance(val, str):
            raise ValueError(f"Value of EntryReviewProcessType must be a string (encountered: {val})")
        newcls = Enum("EntryReviewProcessType", {"_UNKNOWN": val}, type=Enums.UnknownString)  # type: ignore
        return cast(EntryReviewProcessType, getattr(newcls, "_UNKNOWN"))
