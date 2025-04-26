from enum import Enum
from functools import lru_cache
from typing import cast

from ..extensions import Enums


class WorkflowTaskUpdatedScheduledOnWebhookV2BetaType(Enums.KnownString):
    V2_BETAWORKFLOWTASKUPDATEDSCHEDULEDON = "v2-beta.workflowTask.updated.scheduledOn"

    def __str__(self) -> str:
        return str(self.value)

    @staticmethod
    @lru_cache(maxsize=None)
    def of_unknown(val: str) -> "WorkflowTaskUpdatedScheduledOnWebhookV2BetaType":
        if not isinstance(val, str):
            raise ValueError(
                f"Value of WorkflowTaskUpdatedScheduledOnWebhookV2BetaType must be a string (encountered: {val})"
            )
        newcls = Enum("WorkflowTaskUpdatedScheduledOnWebhookV2BetaType", {"_UNKNOWN": val}, type=Enums.UnknownString)  # type: ignore
        return cast(WorkflowTaskUpdatedScheduledOnWebhookV2BetaType, getattr(newcls, "_UNKNOWN"))
