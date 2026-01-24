from enum import Enum
from functools import lru_cache
from typing import cast

from ..extensions import Enums


class StageEntryUpdatedAssignedReviewersEventEventType(Enums.KnownString):
    V2_ALPHASTAGEENTRYUPDATEDASSIGNEDREVIEWERS = "v2-alpha.stageEntry.updated.assignedReviewers"

    def __str__(self) -> str:
        return str(self.value)

    @staticmethod
    @lru_cache(maxsize=None)
    def of_unknown(val: str) -> "StageEntryUpdatedAssignedReviewersEventEventType":
        if not isinstance(val, str):
            raise ValueError(
                f"Value of StageEntryUpdatedAssignedReviewersEventEventType must be a string (encountered: {val})"
            )
        newcls = Enum("StageEntryUpdatedAssignedReviewersEventEventType", {"_UNKNOWN": val}, type=Enums.UnknownString)  # type: ignore
        return cast(StageEntryUpdatedAssignedReviewersEventEventType, getattr(newcls, "_UNKNOWN"))
