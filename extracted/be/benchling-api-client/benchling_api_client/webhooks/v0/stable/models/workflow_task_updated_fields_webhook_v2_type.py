from enum import Enum
from functools import lru_cache
from typing import cast

from ..extensions import Enums


class WorkflowTaskUpdatedFieldsWebhookV2Type(Enums.KnownString):
    V2_WORKFLOWTASKUPDATEDFIELDS = "v2.workflowTask.updated.fields"

    def __str__(self) -> str:
        return str(self.value)

    @staticmethod
    @lru_cache(maxsize=None)
    def of_unknown(val: str) -> "WorkflowTaskUpdatedFieldsWebhookV2Type":
        if not isinstance(val, str):
            raise ValueError(
                f"Value of WorkflowTaskUpdatedFieldsWebhookV2Type must be a string (encountered: {val})"
            )
        newcls = Enum("WorkflowTaskUpdatedFieldsWebhookV2Type", {"_UNKNOWN": val}, type=Enums.UnknownString)  # type: ignore
        return cast(WorkflowTaskUpdatedFieldsWebhookV2Type, getattr(newcls, "_UNKNOWN"))
