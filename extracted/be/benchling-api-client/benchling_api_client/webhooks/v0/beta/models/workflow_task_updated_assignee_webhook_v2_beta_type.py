from enum import Enum
from functools import lru_cache
from typing import cast

from ..extensions import Enums


class WorkflowTaskUpdatedAssigneeWebhookV2BetaType(Enums.KnownString):
    V2_BETAWORKFLOWTASKUPDATEDASSIGNEE = "v2-beta.workflowTask.updated.assignee"

    def __str__(self) -> str:
        return str(self.value)

    @staticmethod
    @lru_cache(maxsize=None)
    def of_unknown(val: str) -> "WorkflowTaskUpdatedAssigneeWebhookV2BetaType":
        if not isinstance(val, str):
            raise ValueError(
                f"Value of WorkflowTaskUpdatedAssigneeWebhookV2BetaType must be a string (encountered: {val})"
            )
        newcls = Enum("WorkflowTaskUpdatedAssigneeWebhookV2BetaType", {"_UNKNOWN": val}, type=Enums.UnknownString)  # type: ignore
        return cast(WorkflowTaskUpdatedAssigneeWebhookV2BetaType, getattr(newcls, "_UNKNOWN"))
