from enum import Enum
from functools import lru_cache
from typing import cast

from ..extensions import Enums


class WorkflowTaskUpdatedStatusWebhookV2BetaType(Enums.KnownString):
    V2_BETAWORKFLOWTASKUPDATEDSTATUS = "v2-beta.workflowTask.updated.status"

    def __str__(self) -> str:
        return str(self.value)

    @staticmethod
    @lru_cache(maxsize=None)
    def of_unknown(val: str) -> "WorkflowTaskUpdatedStatusWebhookV2BetaType":
        if not isinstance(val, str):
            raise ValueError(
                f"Value of WorkflowTaskUpdatedStatusWebhookV2BetaType must be a string (encountered: {val})"
            )
        newcls = Enum("WorkflowTaskUpdatedStatusWebhookV2BetaType", {"_UNKNOWN": val}, type=Enums.UnknownString)  # type: ignore
        return cast(WorkflowTaskUpdatedStatusWebhookV2BetaType, getattr(newcls, "_UNKNOWN"))
