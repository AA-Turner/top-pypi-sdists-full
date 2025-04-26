from enum import Enum
from functools import lru_cache
from typing import cast

from ..extensions import Enums


class V2EntityRegisteredEventEventType(Enums.KnownString):
    V2_ENTITYREGISTERED = "v2.entity.registered"

    def __str__(self) -> str:
        return str(self.value)

    @staticmethod
    @lru_cache(maxsize=None)
    def of_unknown(val: str) -> "V2EntityRegisteredEventEventType":
        if not isinstance(val, str):
            raise ValueError(
                f"Value of V2EntityRegisteredEventEventType must be a string (encountered: {val})"
            )
        newcls = Enum("V2EntityRegisteredEventEventType", {"_UNKNOWN": val}, type=Enums.UnknownString)  # type: ignore
        return cast(V2EntityRegisteredEventEventType, getattr(newcls, "_UNKNOWN"))
