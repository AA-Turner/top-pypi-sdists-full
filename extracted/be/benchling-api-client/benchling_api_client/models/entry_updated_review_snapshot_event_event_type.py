from enum import Enum
from functools import lru_cache
from typing import cast

from ..extensions import Enums


class EntryUpdatedReviewSnapshotEventEventType(Enums.KnownString):
    V2_ENTRYUPDATEDREVIEWSNAPSHOT = "v2.entry.updated.reviewSnapshot"

    def __str__(self) -> str:
        return str(self.value)

    @staticmethod
    @lru_cache(maxsize=None)
    def of_unknown(val: str) -> "EntryUpdatedReviewSnapshotEventEventType":
        if not isinstance(val, str):
            raise ValueError(
                f"Value of EntryUpdatedReviewSnapshotEventEventType must be a string (encountered: {val})"
            )
        newcls = Enum("EntryUpdatedReviewSnapshotEventEventType", {"_UNKNOWN": val}, type=Enums.UnknownString)  # type: ignore
        return cast(EntryUpdatedReviewSnapshotEventEventType, getattr(newcls, "_UNKNOWN"))
