from enum import Enum
from functools import lru_cache
from typing import cast

from ..extensions import Enums


class EntryReviewProcessCompletionStatus(Enums.KnownString):
    APPROVED = "APPROVED"
    COMPLETED = "COMPLETED"
    ACCEPTED = "ACCEPTED"
    REVIEWED = "REVIEWED"
    WITNESSED = "WITNESSED"
    SELF_REVIEWED = "SELF_REVIEWED"

    def __str__(self) -> str:
        return str(self.value)

    @staticmethod
    @lru_cache(maxsize=None)
    def of_unknown(val: str) -> "EntryReviewProcessCompletionStatus":
        if not isinstance(val, str):
            raise ValueError(
                f"Value of EntryReviewProcessCompletionStatus must be a string (encountered: {val})"
            )
        newcls = Enum("EntryReviewProcessCompletionStatus", {"_UNKNOWN": val}, type=Enums.UnknownString)  # type: ignore
        return cast(EntryReviewProcessCompletionStatus, getattr(newcls, "_UNKNOWN"))
