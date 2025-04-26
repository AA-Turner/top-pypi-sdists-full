from enum import Enum
from functools import lru_cache
from typing import cast

from ..extensions import Enums


class ListAppConfigurationItemsSort(Enums.KnownString):
    CREATEDAT = "createdAt"
    CREATEDATASC = "createdAt:asc"
    CREATEDATDESC = "createdAt:desc"
    MODIFIEDAT = "modifiedAt"
    MODIFIEDATASC = "modifiedAt:asc"
    MODIFIEDATDESC = "modifiedAt:desc"

    def __str__(self) -> str:
        return str(self.value)

    @staticmethod
    @lru_cache(maxsize=None)
    def of_unknown(val: str) -> "ListAppConfigurationItemsSort":
        if not isinstance(val, str):
            raise ValueError(f"Value of ListAppConfigurationItemsSort must be a string (encountered: {val})")
        newcls = Enum("ListAppConfigurationItemsSort", {"_UNKNOWN": val}, type=Enums.UnknownString)  # type: ignore
        return cast(ListAppConfigurationItemsSort, getattr(newcls, "_UNKNOWN"))
