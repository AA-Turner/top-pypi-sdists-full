from enum import Enum
from functools import lru_cache
from typing import cast

from ..extensions import Enums


class WorkflowTaskGroupUpdatedWatchersWebhookV2BetaType(Enums.KnownString):
    V2_BETAWORKFLOWTASKGROUPUPDATEDWATCHERS = "v2-beta.workflowTaskGroup.updated.watchers"

    def __str__(self) -> str:
        return str(self.value)

    @staticmethod
    @lru_cache(maxsize=None)
    def of_unknown(val: str) -> "WorkflowTaskGroupUpdatedWatchersWebhookV2BetaType":
        if not isinstance(val, str):
            raise ValueError(
                f"Value of WorkflowTaskGroupUpdatedWatchersWebhookV2BetaType must be a string (encountered: {val})"
            )
        newcls = Enum("WorkflowTaskGroupUpdatedWatchersWebhookV2BetaType", {"_UNKNOWN": val}, type=Enums.UnknownString)  # type: ignore
        return cast(WorkflowTaskGroupUpdatedWatchersWebhookV2BetaType, getattr(newcls, "_UNKNOWN"))
