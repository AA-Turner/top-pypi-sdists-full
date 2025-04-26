from enum import Enum
from functools import lru_cache
from typing import cast

from ..extensions import Enums


class V2WorkflowTaskUpdatedScheduledOnEventEventType(Enums.KnownString):
    V2_WORKFLOWTASKUPDATEDSCHEDULEDON = "v2.workflowTask.updated.scheduledOn"

    def __str__(self) -> str:
        return str(self.value)

    @staticmethod
    @lru_cache(maxsize=None)
    def of_unknown(val: str) -> "V2WorkflowTaskUpdatedScheduledOnEventEventType":
        if not isinstance(val, str):
            raise ValueError(
                f"Value of V2WorkflowTaskUpdatedScheduledOnEventEventType must be a string (encountered: {val})"
            )
        newcls = Enum("V2WorkflowTaskUpdatedScheduledOnEventEventType", {"_UNKNOWN": val}, type=Enums.UnknownString)  # type: ignore
        return cast(V2WorkflowTaskUpdatedScheduledOnEventEventType, getattr(newcls, "_UNKNOWN"))
