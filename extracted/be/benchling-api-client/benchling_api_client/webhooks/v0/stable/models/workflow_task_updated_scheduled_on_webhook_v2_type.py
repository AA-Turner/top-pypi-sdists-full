from enum import Enum
from functools import lru_cache
from typing import cast

from ..extensions import Enums


class WorkflowTaskUpdatedScheduledOnWebhookV2Type(Enums.KnownString):
    V2_WORKFLOWTASKUPDATEDSCHEDULEDON = "v2.workflowTask.updated.scheduledOn"

    def __str__(self) -> str:
        return str(self.value)

    @staticmethod
    @lru_cache(maxsize=None)
    def of_unknown(val: str) -> "WorkflowTaskUpdatedScheduledOnWebhookV2Type":
        if not isinstance(val, str):
            raise ValueError(
                f"Value of WorkflowTaskUpdatedScheduledOnWebhookV2Type must be a string (encountered: {val})"
            )
        newcls = Enum("WorkflowTaskUpdatedScheduledOnWebhookV2Type", {"_UNKNOWN": val}, type=Enums.UnknownString)  # type: ignore
        return cast(WorkflowTaskUpdatedScheduledOnWebhookV2Type, getattr(newcls, "_UNKNOWN"))
