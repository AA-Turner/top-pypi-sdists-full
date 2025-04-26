from enum import Enum
from functools import lru_cache
from typing import cast

from ..extensions import Enums


class WorkflowTaskUpdatedFieldsWebhookV2BetaType(Enums.KnownString):
    V2_BETAWORKFLOWTASKUPDATEDFIELDS = "v2-beta.workflowTask.updated.fields"

    def __str__(self) -> str:
        return str(self.value)

    @staticmethod
    @lru_cache(maxsize=None)
    def of_unknown(val: str) -> "WorkflowTaskUpdatedFieldsWebhookV2BetaType":
        if not isinstance(val, str):
            raise ValueError(
                f"Value of WorkflowTaskUpdatedFieldsWebhookV2BetaType must be a string (encountered: {val})"
            )
        newcls = Enum("WorkflowTaskUpdatedFieldsWebhookV2BetaType", {"_UNKNOWN": val}, type=Enums.UnknownString)  # type: ignore
        return cast(WorkflowTaskUpdatedFieldsWebhookV2BetaType, getattr(newcls, "_UNKNOWN"))
