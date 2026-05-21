from enum import Enum
from functools import lru_cache
from typing import cast

from ..extensions import Enums


class EntryReviewProcessStagesItemActionLabel(Enums.KnownString):
    APPROVE = "APPROVE"
    COMPLETE = "COMPLETE"
    ACCEPT = "ACCEPT"
    REVIEW = "REVIEW"
    WITNESS = "WITNESS"
    SELF_REVIEW = "SELF_REVIEW"

    def __str__(self) -> str:
        return str(self.value)

    @staticmethod
    @lru_cache(maxsize=None)
    def of_unknown(val: str) -> "EntryReviewProcessStagesItemActionLabel":
        if not isinstance(val, str):
            raise ValueError(
                f"Value of EntryReviewProcessStagesItemActionLabel must be a string (encountered: {val})"
            )
        newcls = Enum("EntryReviewProcessStagesItemActionLabel", {"_UNKNOWN": val}, type=Enums.UnknownString)  # type: ignore
        return cast(EntryReviewProcessStagesItemActionLabel, getattr(newcls, "_UNKNOWN"))
