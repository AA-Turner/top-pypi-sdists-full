from enum import Enum
from functools import lru_cache
from typing import cast

from ..extensions import Enums


class ListProjectCollaborationsSort(Enums.KnownString):
    MODIFIEDAT = "modifiedAt"
    MODIFIEDATASC = "modifiedAt:asc"
    MODIFIEDATDESC = "modifiedAt:desc"

    def __str__(self) -> str:
        return str(self.value)

    @staticmethod
    @lru_cache(maxsize=None)
    def of_unknown(val: str) -> "ListProjectCollaborationsSort":
        if not isinstance(val, str):
            raise ValueError(f"Value of ListProjectCollaborationsSort must be a string (encountered: {val})")
        newcls = Enum("ListProjectCollaborationsSort", {"_UNKNOWN": val}, type=Enums.UnknownString)  # type: ignore
        return cast(ListProjectCollaborationsSort, getattr(newcls, "_UNKNOWN"))
