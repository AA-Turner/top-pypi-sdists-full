from enum import Enum
from functools import lru_cache
from typing import cast

from ..extensions import Enums


class GetFormDefinitionsSort(Enums.KnownString):
    MODIFIEDAT = "modifiedAt"
    MODIFIEDATASC = "modifiedAt:asc"
    MODIFIEDATDESC = "modifiedAt:desc"

    def __str__(self) -> str:
        return str(self.value)

    @staticmethod
    @lru_cache(maxsize=None)
    def of_unknown(val: str) -> "GetFormDefinitionsSort":
        if not isinstance(val, str):
            raise ValueError(f"Value of GetFormDefinitionsSort must be a string (encountered: {val})")
        newcls = Enum("GetFormDefinitionsSort", {"_UNKNOWN": val}, type=Enums.UnknownString)  # type: ignore
        return cast(GetFormDefinitionsSort, getattr(newcls, "_UNKNOWN"))
