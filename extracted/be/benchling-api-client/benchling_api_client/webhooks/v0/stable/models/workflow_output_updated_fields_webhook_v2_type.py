from enum import Enum
from functools import lru_cache
from typing import cast

from ..extensions import Enums


class WorkflowOutputUpdatedFieldsWebhookV2Type(Enums.KnownString):
    V2_WORKFLOWOUTPUTUPDATEDFIELDS = "v2.workflowOutput.updated.fields"

    def __str__(self) -> str:
        return str(self.value)

    @staticmethod
    @lru_cache(maxsize=None)
    def of_unknown(val: str) -> "WorkflowOutputUpdatedFieldsWebhookV2Type":
        if not isinstance(val, str):
            raise ValueError(
                f"Value of WorkflowOutputUpdatedFieldsWebhookV2Type must be a string (encountered: {val})"
            )
        newcls = Enum("WorkflowOutputUpdatedFieldsWebhookV2Type", {"_UNKNOWN": val}, type=Enums.UnknownString)  # type: ignore
        return cast(WorkflowOutputUpdatedFieldsWebhookV2Type, getattr(newcls, "_UNKNOWN"))
