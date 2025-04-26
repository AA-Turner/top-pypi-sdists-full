from enum import Enum
from functools import lru_cache
from typing import cast

from ..extensions import Enums


class WorkflowTaskGroupCreatedWebhookV2BetaType(Enums.KnownString):
    V2_BETAWORKFLOWTASKGROUPCREATED = "v2-beta.workflowTaskGroup.created"

    def __str__(self) -> str:
        return str(self.value)

    @staticmethod
    @lru_cache(maxsize=None)
    def of_unknown(val: str) -> "WorkflowTaskGroupCreatedWebhookV2BetaType":
        if not isinstance(val, str):
            raise ValueError(
                f"Value of WorkflowTaskGroupCreatedWebhookV2BetaType must be a string (encountered: {val})"
            )
        newcls = Enum("WorkflowTaskGroupCreatedWebhookV2BetaType", {"_UNKNOWN": val}, type=Enums.UnknownString)  # type: ignore
        return cast(WorkflowTaskGroupCreatedWebhookV2BetaType, getattr(newcls, "_UNKNOWN"))
