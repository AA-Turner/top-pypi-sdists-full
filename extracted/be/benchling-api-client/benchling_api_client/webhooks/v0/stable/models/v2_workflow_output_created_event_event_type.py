from enum import Enum
from functools import lru_cache
from typing import cast

from ..extensions import Enums


class V2WorkflowOutputCreatedEventEventType(Enums.KnownString):
    V2_WORKFLOWOUTPUTCREATED = "v2.workflowOutput.created"

    def __str__(self) -> str:
        return str(self.value)

    @staticmethod
    @lru_cache(maxsize=None)
    def of_unknown(val: str) -> "V2WorkflowOutputCreatedEventEventType":
        if not isinstance(val, str):
            raise ValueError(
                f"Value of V2WorkflowOutputCreatedEventEventType must be a string (encountered: {val})"
            )
        newcls = Enum("V2WorkflowOutputCreatedEventEventType", {"_UNKNOWN": val}, type=Enums.UnknownString)  # type: ignore
        return cast(V2WorkflowOutputCreatedEventEventType, getattr(newcls, "_UNKNOWN"))
