from enum import Enum
from functools import lru_cache
from typing import cast

from ..extensions import Enums


class WorkflowTaskGroupUpdatedWatchersWebhookV2Type(Enums.KnownString):
    V2_WORKFLOWTASKGROUPUPDATEDWATCHERS = "v2.workflowTaskGroup.updated.watchers"

    def __str__(self) -> str:
        return str(self.value)

    @staticmethod
    @lru_cache(maxsize=None)
    def of_unknown(val: str) -> "WorkflowTaskGroupUpdatedWatchersWebhookV2Type":
        if not isinstance(val, str):
            raise ValueError(
                f"Value of WorkflowTaskGroupUpdatedWatchersWebhookV2Type must be a string (encountered: {val})"
            )
        newcls = Enum("WorkflowTaskGroupUpdatedWatchersWebhookV2Type", {"_UNKNOWN": val}, type=Enums.UnknownString)  # type: ignore
        return cast(WorkflowTaskGroupUpdatedWatchersWebhookV2Type, getattr(newcls, "_UNKNOWN"))
