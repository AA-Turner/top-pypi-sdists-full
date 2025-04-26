from enum import Enum
from functools import lru_cache
from typing import cast

from ..extensions import Enums


class WorkflowEndNodeDetailsNodeType(Enums.KnownString):
    END = "END"

    def __str__(self) -> str:
        return str(self.value)

    @staticmethod
    @lru_cache(maxsize=None)
    def of_unknown(val: str) -> "WorkflowEndNodeDetailsNodeType":
        if not isinstance(val, str):
            raise ValueError(f"Value of WorkflowEndNodeDetailsNodeType must be a string (encountered: {val})")
        newcls = Enum("WorkflowEndNodeDetailsNodeType", {"_UNKNOWN": val}, type=Enums.UnknownString)  # type: ignore
        return cast(WorkflowEndNodeDetailsNodeType, getattr(newcls, "_UNKNOWN"))
