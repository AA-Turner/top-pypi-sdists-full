from enum import Enum
from functools import lru_cache
from typing import cast

from ..extensions import Enums


class ListMoleculesSort(Enums.KnownString):
    CREATEDAT = "createdAt"
    CREATEDATASC = "createdAt:asc"
    CREATEDATDESC = "createdAt:desc"
    MODIFIEDAT = "modifiedAt"
    MODIFIEDATASC = "modifiedAt:asc"
    MODIFIEDATDESC = "modifiedAt:desc"
    NAME = "name"
    NAMEASC = "name:asc"
    NAMEDESC = "name:desc"

    def __str__(self) -> str:
        return str(self.value)

    @staticmethod
    @lru_cache(maxsize=None)
    def of_unknown(val: str) -> "ListMoleculesSort":
        if not isinstance(val, str):
            raise ValueError(f"Value of ListMoleculesSort must be a string (encountered: {val})")
        newcls = Enum("ListMoleculesSort", {"_UNKNOWN": val}, type=Enums.UnknownString)  # type: ignore
        return cast(ListMoleculesSort, getattr(newcls, "_UNKNOWN"))
