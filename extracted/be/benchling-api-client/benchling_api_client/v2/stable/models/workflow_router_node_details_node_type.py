from enum import Enum
from functools import lru_cache
from typing import cast

from ..extensions import Enums


class WorkflowRouterNodeDetailsNodeType(Enums.KnownString):
    ROUTER = "ROUTER"

    def __str__(self) -> str:
        return str(self.value)

    @staticmethod
    @lru_cache(maxsize=None)
    def of_unknown(val: str) -> "WorkflowRouterNodeDetailsNodeType":
        if not isinstance(val, str):
            raise ValueError(
                f"Value of WorkflowRouterNodeDetailsNodeType must be a string (encountered: {val})"
            )
        newcls = Enum("WorkflowRouterNodeDetailsNodeType", {"_UNKNOWN": val}, type=Enums.UnknownString)  # type: ignore
        return cast(WorkflowRouterNodeDetailsNodeType, getattr(newcls, "_UNKNOWN"))
