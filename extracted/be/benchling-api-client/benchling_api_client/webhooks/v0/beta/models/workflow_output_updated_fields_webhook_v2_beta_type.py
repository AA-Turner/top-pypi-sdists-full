from enum import Enum
from functools import lru_cache
from typing import cast

from ..extensions import Enums


class WorkflowOutputUpdatedFieldsWebhookV2BetaType(Enums.KnownString):
    V2_BETAWORKFLOWOUTPUTUPDATEDFIELDS = "v2-beta.workflowOutput.updated.fields"

    def __str__(self) -> str:
        return str(self.value)

    @staticmethod
    @lru_cache(maxsize=None)
    def of_unknown(val: str) -> "WorkflowOutputUpdatedFieldsWebhookV2BetaType":
        if not isinstance(val, str):
            raise ValueError(
                f"Value of WorkflowOutputUpdatedFieldsWebhookV2BetaType must be a string (encountered: {val})"
            )
        newcls = Enum("WorkflowOutputUpdatedFieldsWebhookV2BetaType", {"_UNKNOWN": val}, type=Enums.UnknownString)  # type: ignore
        return cast(WorkflowOutputUpdatedFieldsWebhookV2BetaType, getattr(newcls, "_UNKNOWN"))
