from enum import Enum
from functools import lru_cache
from typing import cast

from ..extensions import Enums


class WorksheetUpdatedReviewSnapshotEventEventType(Enums.KnownString):
    V2_WORKSHEETUPDATEDREVIEWSNAPSHOT = "v2.worksheet.updated.reviewSnapshot"

    def __str__(self) -> str:
        return str(self.value)

    @staticmethod
    @lru_cache(maxsize=None)
    def of_unknown(val: str) -> "WorksheetUpdatedReviewSnapshotEventEventType":
        if not isinstance(val, str):
            raise ValueError(
                f"Value of WorksheetUpdatedReviewSnapshotEventEventType must be a string (encountered: {val})"
            )
        newcls = Enum("WorksheetUpdatedReviewSnapshotEventEventType", {"_UNKNOWN": val}, type=Enums.UnknownString)  # type: ignore
        return cast(WorksheetUpdatedReviewSnapshotEventEventType, getattr(newcls, "_UNKNOWN"))
