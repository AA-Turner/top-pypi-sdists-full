from enum import Enum
from functools import lru_cache
from typing import cast

from ..extensions import Enums


class WorkflowFlowchartNodeConfigNodeType(Enums.KnownString):
    ROOT = "ROOT"
    OUTPUT = "OUTPUT"
    TASK = "TASK"
    ROUTER = "ROUTER"
    END = "END"

    def __str__(self) -> str:
        return str(self.value)

    @staticmethod
    @lru_cache(maxsize=None)
    def of_unknown(val: str) -> "WorkflowFlowchartNodeConfigNodeType":
        if not isinstance(val, str):
            raise ValueError(
                f"Value of WorkflowFlowchartNodeConfigNodeType must be a string (encountered: {val})"
            )
        newcls = Enum("WorkflowFlowchartNodeConfigNodeType", {"_UNKNOWN": val}, type=Enums.UnknownString)  # type: ignore
        return cast(WorkflowFlowchartNodeConfigNodeType, getattr(newcls, "_UNKNOWN"))
