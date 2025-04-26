from enum import Enum
from functools import lru_cache
from typing import cast

from ..extensions import Enums


class WorkflowTaskCreatedWebhookV2Type(Enums.KnownString):
    V2_WORKFLOWTASKCREATED = "v2.workflowTask.created"

    def __str__(self) -> str:
        return str(self.value)

    @staticmethod
    @lru_cache(maxsize=None)
    def of_unknown(val: str) -> "WorkflowTaskCreatedWebhookV2Type":
        if not isinstance(val, str):
            raise ValueError(
                f"Value of WorkflowTaskCreatedWebhookV2Type must be a string (encountered: {val})"
            )
        newcls = Enum("WorkflowTaskCreatedWebhookV2Type", {"_UNKNOWN": val}, type=Enums.UnknownString)  # type: ignore
        return cast(WorkflowTaskCreatedWebhookV2Type, getattr(newcls, "_UNKNOWN"))
