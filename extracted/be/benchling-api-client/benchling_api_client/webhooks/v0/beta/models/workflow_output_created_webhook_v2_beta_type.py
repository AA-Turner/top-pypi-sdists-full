from enum import Enum
from functools import lru_cache
from typing import cast

from ..extensions import Enums


class WorkflowOutputCreatedWebhookV2BetaType(Enums.KnownString):
    V2_BETAWORKFLOWOUTPUTCREATED = "v2-beta.workflowOutput.created"

    def __str__(self) -> str:
        return str(self.value)

    @staticmethod
    @lru_cache(maxsize=None)
    def of_unknown(val: str) -> "WorkflowOutputCreatedWebhookV2BetaType":
        if not isinstance(val, str):
            raise ValueError(
                f"Value of WorkflowOutputCreatedWebhookV2BetaType must be a string (encountered: {val})"
            )
        newcls = Enum("WorkflowOutputCreatedWebhookV2BetaType", {"_UNKNOWN": val}, type=Enums.UnknownString)  # type: ignore
        return cast(WorkflowOutputCreatedWebhookV2BetaType, getattr(newcls, "_UNKNOWN"))
