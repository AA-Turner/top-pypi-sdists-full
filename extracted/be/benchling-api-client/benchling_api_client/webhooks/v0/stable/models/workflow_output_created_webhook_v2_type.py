from enum import Enum
from functools import lru_cache
from typing import cast

from ..extensions import Enums


class WorkflowOutputCreatedWebhookV2Type(Enums.KnownString):
    V2_WORKFLOWOUTPUTCREATED = "v2.workflowOutput.created"

    def __str__(self) -> str:
        return str(self.value)

    @staticmethod
    @lru_cache(maxsize=None)
    def of_unknown(val: str) -> "WorkflowOutputCreatedWebhookV2Type":
        if not isinstance(val, str):
            raise ValueError(
                f"Value of WorkflowOutputCreatedWebhookV2Type must be a string (encountered: {val})"
            )
        newcls = Enum("WorkflowOutputCreatedWebhookV2Type", {"_UNKNOWN": val}, type=Enums.UnknownString)  # type: ignore
        return cast(WorkflowOutputCreatedWebhookV2Type, getattr(newcls, "_UNKNOWN"))
