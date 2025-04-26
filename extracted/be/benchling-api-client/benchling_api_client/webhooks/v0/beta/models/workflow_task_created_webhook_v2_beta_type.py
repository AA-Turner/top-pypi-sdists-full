from enum import Enum
from functools import lru_cache
from typing import cast

from ..extensions import Enums


class WorkflowTaskCreatedWebhookV2BetaType(Enums.KnownString):
    V2_BETAWORKFLOWTASKCREATED = "v2-beta.workflowTask.created"

    def __str__(self) -> str:
        return str(self.value)

    @staticmethod
    @lru_cache(maxsize=None)
    def of_unknown(val: str) -> "WorkflowTaskCreatedWebhookV2BetaType":
        if not isinstance(val, str):
            raise ValueError(
                f"Value of WorkflowTaskCreatedWebhookV2BetaType must be a string (encountered: {val})"
            )
        newcls = Enum("WorkflowTaskCreatedWebhookV2BetaType", {"_UNKNOWN": val}, type=Enums.UnknownString)  # type: ignore
        return cast(WorkflowTaskCreatedWebhookV2BetaType, getattr(newcls, "_UNKNOWN"))
