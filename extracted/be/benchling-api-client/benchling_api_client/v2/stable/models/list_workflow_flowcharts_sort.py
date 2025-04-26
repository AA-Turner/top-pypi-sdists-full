from enum import Enum
from functools import lru_cache
from typing import cast

from ..extensions import Enums


class ListWorkflowFlowchartsSort(Enums.KnownString):
    CREATEDAT = "createdAt"
    CREATEDATASC = "createdAt:asc"
    CREATEDATDESC = "createdAt:desc"

    def __str__(self) -> str:
        return str(self.value)

    @staticmethod
    @lru_cache(maxsize=None)
    def of_unknown(val: str) -> "ListWorkflowFlowchartsSort":
        if not isinstance(val, str):
            raise ValueError(f"Value of ListWorkflowFlowchartsSort must be a string (encountered: {val})")
        newcls = Enum("ListWorkflowFlowchartsSort", {"_UNKNOWN": val}, type=Enums.UnknownString)  # type: ignore
        return cast(ListWorkflowFlowchartsSort, getattr(newcls, "_UNKNOWN"))
