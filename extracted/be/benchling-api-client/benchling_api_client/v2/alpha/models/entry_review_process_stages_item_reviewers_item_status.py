from enum import Enum
from functools import lru_cache
from typing import cast

from ..extensions import Enums


class EntryReviewProcessStagesItemReviewersItemStatus(Enums.KnownString):
    BLOCKED = "BLOCKED"
    PENDING = "PENDING"
    FINISHED = "FINISHED"
    REJECTED = "REJECTED"

    def __str__(self) -> str:
        return str(self.value)

    @staticmethod
    @lru_cache(maxsize=None)
    def of_unknown(val: str) -> "EntryReviewProcessStagesItemReviewersItemStatus":
        if not isinstance(val, str):
            raise ValueError(
                f"Value of EntryReviewProcessStagesItemReviewersItemStatus must be a string (encountered: {val})"
            )
        newcls = Enum("EntryReviewProcessStagesItemReviewersItemStatus", {"_UNKNOWN": val}, type=Enums.UnknownString)  # type: ignore
        return cast(EntryReviewProcessStagesItemReviewersItemStatus, getattr(newcls, "_UNKNOWN"))
