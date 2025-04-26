from enum import Enum
from functools import lru_cache
from typing import cast

from ..extensions import Enums


class WorkflowTaskUpdatedAssigneeWebhookV2Type(Enums.KnownString):
    V2_WORKFLOWTASKUPDATEDASSIGNEE = "v2.workflowTask.updated.assignee"

    def __str__(self) -> str:
        return str(self.value)

    @staticmethod
    @lru_cache(maxsize=None)
    def of_unknown(val: str) -> "WorkflowTaskUpdatedAssigneeWebhookV2Type":
        if not isinstance(val, str):
            raise ValueError(
                f"Value of WorkflowTaskUpdatedAssigneeWebhookV2Type must be a string (encountered: {val})"
            )
        newcls = Enum("WorkflowTaskUpdatedAssigneeWebhookV2Type", {"_UNKNOWN": val}, type=Enums.UnknownString)  # type: ignore
        return cast(WorkflowTaskUpdatedAssigneeWebhookV2Type, getattr(newcls, "_UNKNOWN"))
