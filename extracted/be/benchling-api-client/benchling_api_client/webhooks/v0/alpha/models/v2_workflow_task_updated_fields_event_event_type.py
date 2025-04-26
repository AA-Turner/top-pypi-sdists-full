from enum import Enum
from functools import lru_cache
from typing import cast

from ..extensions import Enums


class V2WorkflowTaskUpdatedFieldsEventEventType(Enums.KnownString):
    V2_WORKFLOWTASKUPDATEDFIELDS = "v2.workflowTask.updated.fields"

    def __str__(self) -> str:
        return str(self.value)

    @staticmethod
    @lru_cache(maxsize=None)
    def of_unknown(val: str) -> "V2WorkflowTaskUpdatedFieldsEventEventType":
        if not isinstance(val, str):
            raise ValueError(
                f"Value of V2WorkflowTaskUpdatedFieldsEventEventType must be a string (encountered: {val})"
            )
        newcls = Enum("V2WorkflowTaskUpdatedFieldsEventEventType", {"_UNKNOWN": val}, type=Enums.UnknownString)  # type: ignore
        return cast(V2WorkflowTaskUpdatedFieldsEventEventType, getattr(newcls, "_UNKNOWN"))
