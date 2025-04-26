from enum import Enum
from functools import lru_cache
from typing import cast

from ..extensions import Enums


class WellResourceType(Enums.KnownString):
    CONTAINER = "container"

    def __str__(self) -> str:
        return str(self.value)

    @staticmethod
    @lru_cache(maxsize=None)
    def of_unknown(val: str) -> "WellResourceType":
        if not isinstance(val, str):
            raise ValueError(f"Value of WellResourceType must be a string (encountered: {val})")
        newcls = Enum("WellResourceType", {"_UNKNOWN": val}, type=Enums.UnknownString)  # type: ignore
        return cast(WellResourceType, getattr(newcls, "_UNKNOWN"))
