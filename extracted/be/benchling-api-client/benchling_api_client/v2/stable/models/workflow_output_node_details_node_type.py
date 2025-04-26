from enum import Enum
from functools import lru_cache
from typing import cast

from ..extensions import Enums


class WorkflowOutputNodeDetailsNodeType(Enums.KnownString):
    OUTPUT = "OUTPUT"

    def __str__(self) -> str:
        return str(self.value)

    @staticmethod
    @lru_cache(maxsize=None)
    def of_unknown(val: str) -> "WorkflowOutputNodeDetailsNodeType":
        if not isinstance(val, str):
            raise ValueError(
                f"Value of WorkflowOutputNodeDetailsNodeType must be a string (encountered: {val})"
            )
        newcls = Enum("WorkflowOutputNodeDetailsNodeType", {"_UNKNOWN": val}, type=Enums.UnknownString)  # type: ignore
        return cast(WorkflowOutputNodeDetailsNodeType, getattr(newcls, "_UNKNOWN"))
