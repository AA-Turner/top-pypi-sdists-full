from enum import Enum
from functools import lru_cache
from typing import cast

from ..extensions import Enums


class WorkflowTaskUpdatedStatusWebhookV2Type(Enums.KnownString):
    V2_WORKFLOWTASKUPDATEDSTATUS = "v2.workflowTask.updated.status"

    def __str__(self) -> str:
        return str(self.value)

    @staticmethod
    @lru_cache(maxsize=None)
    def of_unknown(val: str) -> "WorkflowTaskUpdatedStatusWebhookV2Type":
        if not isinstance(val, str):
            raise ValueError(
                f"Value of WorkflowTaskUpdatedStatusWebhookV2Type must be a string (encountered: {val})"
            )
        newcls = Enum("WorkflowTaskUpdatedStatusWebhookV2Type", {"_UNKNOWN": val}, type=Enums.UnknownString)  # type: ignore
        return cast(WorkflowTaskUpdatedStatusWebhookV2Type, getattr(newcls, "_UNKNOWN"))
