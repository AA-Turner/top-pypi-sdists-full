from enum import Enum
from functools import lru_cache
from typing import cast

from ..extensions import Enums


class WorksheetUpdatedReviewSnapshotBetaEventEventType(Enums.KnownString):
    V2_BETAWORKSHEETUPDATEDREVIEWSNAPSHOT = "v2-beta.worksheet.updated.reviewSnapshot"

    def __str__(self) -> str:
        return str(self.value)

    @staticmethod
    @lru_cache(maxsize=None)
    def of_unknown(val: str) -> "WorksheetUpdatedReviewSnapshotBetaEventEventType":
        if not isinstance(val, str):
            raise ValueError(
                f"Value of WorksheetUpdatedReviewSnapshotBetaEventEventType must be a string (encountered: {val})"
            )
        newcls = Enum("WorksheetUpdatedReviewSnapshotBetaEventEventType", {"_UNKNOWN": val}, type=Enums.UnknownString)  # type: ignore
        return cast(WorksheetUpdatedReviewSnapshotBetaEventEventType, getattr(newcls, "_UNKNOWN"))
