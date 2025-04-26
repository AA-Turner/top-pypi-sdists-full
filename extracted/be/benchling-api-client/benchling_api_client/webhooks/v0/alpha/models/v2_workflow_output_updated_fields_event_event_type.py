from enum import Enum
from functools import lru_cache
from typing import cast

from ..extensions import Enums


class V2WorkflowOutputUpdatedFieldsEventEventType(Enums.KnownString):
    V2_WORKFLOWOUTPUTUPDATEDFIELDS = "v2.workflowOutput.updated.fields"

    def __str__(self) -> str:
        return str(self.value)

    @staticmethod
    @lru_cache(maxsize=None)
    def of_unknown(val: str) -> "V2WorkflowOutputUpdatedFieldsEventEventType":
        if not isinstance(val, str):
            raise ValueError(
                f"Value of V2WorkflowOutputUpdatedFieldsEventEventType must be a string (encountered: {val})"
            )
        newcls = Enum("V2WorkflowOutputUpdatedFieldsEventEventType", {"_UNKNOWN": val}, type=Enums.UnknownString)  # type: ignore
        return cast(V2WorkflowOutputUpdatedFieldsEventEventType, getattr(newcls, "_UNKNOWN"))
