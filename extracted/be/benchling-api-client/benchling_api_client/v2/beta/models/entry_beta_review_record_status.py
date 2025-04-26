from enum import Enum
from functools import lru_cache
from typing import cast

from ..extensions import Enums


class EntryBetaReviewRecordStatus(Enums.KnownString):
    ACCEPTED = "ACCEPTED"
    NEEDS_REVIEW = "NEEDS_REVIEW"
    REJECTED = "REJECTED"
    RETRACTED = "RETRACTED"
    ACCEPTANCE_SNAPSHOT_IN_PROGRESS = "ACCEPTANCE_SNAPSHOT_IN_PROGRESS"
    REVIEW_SNAPSHOT_IN_PROGRESS = "REVIEW_SNAPSHOT_IN_PROGRESS"
    IN_PROGRESS = "IN_PROGRESS"
    ACTION_REQUIRED = "ACTION_REQUIRED"

    def __str__(self) -> str:
        return str(self.value)

    @staticmethod
    @lru_cache(maxsize=None)
    def of_unknown(val: str) -> "EntryBetaReviewRecordStatus":
        if not isinstance(val, str):
            raise ValueError(f"Value of EntryBetaReviewRecordStatus must be a string (encountered: {val})")
        newcls = Enum("EntryBetaReviewRecordStatus", {"_UNKNOWN": val}, type=Enums.UnknownString)  # type: ignore
        return cast(EntryBetaReviewRecordStatus, getattr(newcls, "_UNKNOWN"))
