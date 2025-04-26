from enum import Enum
from functools import lru_cache
from typing import cast

from ..extensions import Enums


class WorkflowTaskGroupMappingCompletedEventEventType(Enums.KnownString):
    V2_WORKFLOWTASKGROUPMAPPINGCOMPLETED = "v2.workflowTaskGroup.mappingCompleted"

    def __str__(self) -> str:
        return str(self.value)

    @staticmethod
    @lru_cache(maxsize=None)
    def of_unknown(val: str) -> "WorkflowTaskGroupMappingCompletedEventEventType":
        if not isinstance(val, str):
            raise ValueError(
                f"Value of WorkflowTaskGroupMappingCompletedEventEventType must be a string (encountered: {val})"
            )
        newcls = Enum("WorkflowTaskGroupMappingCompletedEventEventType", {"_UNKNOWN": val}, type=Enums.UnknownString)  # type: ignore
        return cast(WorkflowTaskGroupMappingCompletedEventEventType, getattr(newcls, "_UNKNOWN"))
