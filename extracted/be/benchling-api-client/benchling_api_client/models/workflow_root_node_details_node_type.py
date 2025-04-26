from enum import Enum
from functools import lru_cache
from typing import cast

from ..extensions import Enums


class WorkflowRootNodeDetailsNodeType(Enums.KnownString):
    ROOT = "ROOT"

    def __str__(self) -> str:
        return str(self.value)

    @staticmethod
    @lru_cache(maxsize=None)
    def of_unknown(val: str) -> "WorkflowRootNodeDetailsNodeType":
        if not isinstance(val, str):
            raise ValueError(
                f"Value of WorkflowRootNodeDetailsNodeType must be a string (encountered: {val})"
            )
        newcls = Enum("WorkflowRootNodeDetailsNodeType", {"_UNKNOWN": val}, type=Enums.UnknownString)  # type: ignore
        return cast(WorkflowRootNodeDetailsNodeType, getattr(newcls, "_UNKNOWN"))
