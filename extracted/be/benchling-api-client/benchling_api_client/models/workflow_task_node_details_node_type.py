from enum import Enum
from functools import lru_cache
from typing import cast

from ..extensions import Enums


class WorkflowTaskNodeDetailsNodeType(Enums.KnownString):
    TASK = "TASK"

    def __str__(self) -> str:
        return str(self.value)

    @staticmethod
    @lru_cache(maxsize=None)
    def of_unknown(val: str) -> "WorkflowTaskNodeDetailsNodeType":
        if not isinstance(val, str):
            raise ValueError(
                f"Value of WorkflowTaskNodeDetailsNodeType must be a string (encountered: {val})"
            )
        newcls = Enum("WorkflowTaskNodeDetailsNodeType", {"_UNKNOWN": val}, type=Enums.UnknownString)  # type: ignore
        return cast(WorkflowTaskNodeDetailsNodeType, getattr(newcls, "_UNKNOWN"))
