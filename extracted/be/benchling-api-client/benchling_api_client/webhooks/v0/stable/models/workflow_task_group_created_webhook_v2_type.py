from enum import Enum
from functools import lru_cache
from typing import cast

from ..extensions import Enums


class WorkflowTaskGroupCreatedWebhookV2Type(Enums.KnownString):
    V2_WORKFLOWTASKGROUPCREATED = "v2.workflowTaskGroup.created"

    def __str__(self) -> str:
        return str(self.value)

    @staticmethod
    @lru_cache(maxsize=None)
    def of_unknown(val: str) -> "WorkflowTaskGroupCreatedWebhookV2Type":
        if not isinstance(val, str):
            raise ValueError(
                f"Value of WorkflowTaskGroupCreatedWebhookV2Type must be a string (encountered: {val})"
            )
        newcls = Enum("WorkflowTaskGroupCreatedWebhookV2Type", {"_UNKNOWN": val}, type=Enums.UnknownString)  # type: ignore
        return cast(WorkflowTaskGroupCreatedWebhookV2Type, getattr(newcls, "_UNKNOWN"))
