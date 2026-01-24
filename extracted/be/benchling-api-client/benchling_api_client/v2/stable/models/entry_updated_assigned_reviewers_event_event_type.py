from enum import Enum
from functools import lru_cache
from typing import cast

from ..extensions import Enums


class EntryUpdatedAssignedReviewersEventEventType(Enums.KnownString):
    V2_ENTRYUPDATEDASSIGNEDREVIEWERS = "v2.entry.updated.assignedReviewers"

    def __str__(self) -> str:
        return str(self.value)

    @staticmethod
    @lru_cache(maxsize=None)
    def of_unknown(val: str) -> "EntryUpdatedAssignedReviewersEventEventType":
        if not isinstance(val, str):
            raise ValueError(
                f"Value of EntryUpdatedAssignedReviewersEventEventType must be a string (encountered: {val})"
            )
        newcls = Enum("EntryUpdatedAssignedReviewersEventEventType", {"_UNKNOWN": val}, type=Enums.UnknownString)  # type: ignore
        return cast(EntryUpdatedAssignedReviewersEventEventType, getattr(newcls, "_UNKNOWN"))
