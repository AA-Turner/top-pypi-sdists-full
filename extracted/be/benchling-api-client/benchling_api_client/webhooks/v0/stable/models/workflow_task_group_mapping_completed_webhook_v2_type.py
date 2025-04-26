from enum import Enum
from functools import lru_cache
from typing import cast

from ..extensions import Enums


class WorkflowTaskGroupMappingCompletedWebhookV2Type(Enums.KnownString):
    V2_WORKFLOWTASKGROUPMAPPINGCOMPLETED = "v2.workflowTaskGroup.mappingCompleted"

    def __str__(self) -> str:
        return str(self.value)

    @staticmethod
    @lru_cache(maxsize=None)
    def of_unknown(val: str) -> "WorkflowTaskGroupMappingCompletedWebhookV2Type":
        if not isinstance(val, str):
            raise ValueError(
                f"Value of WorkflowTaskGroupMappingCompletedWebhookV2Type must be a string (encountered: {val})"
            )
        newcls = Enum("WorkflowTaskGroupMappingCompletedWebhookV2Type", {"_UNKNOWN": val}, type=Enums.UnknownString)  # type: ignore
        return cast(WorkflowTaskGroupMappingCompletedWebhookV2Type, getattr(newcls, "_UNKNOWN"))
