from enum import Enum
from functools import lru_cache
from typing import cast

from ..extensions import Enums


class EntryUpdatedReviewSnapshotBetaEventEventType(Enums.KnownString):
    V2_BETAENTRYUPDATEDREVIEWSNAPSHOT = "v2-beta.entry.updated.reviewSnapshot"

    def __str__(self) -> str:
        return str(self.value)

    @staticmethod
    @lru_cache(maxsize=None)
    def of_unknown(val: str) -> "EntryUpdatedReviewSnapshotBetaEventEventType":
        if not isinstance(val, str):
            raise ValueError(
                f"Value of EntryUpdatedReviewSnapshotBetaEventEventType must be a string (encountered: {val})"
            )
        newcls = Enum("EntryUpdatedReviewSnapshotBetaEventEventType", {"_UNKNOWN": val}, type=Enums.UnknownString)  # type: ignore
        return cast(EntryUpdatedReviewSnapshotBetaEventEventType, getattr(newcls, "_UNKNOWN"))
