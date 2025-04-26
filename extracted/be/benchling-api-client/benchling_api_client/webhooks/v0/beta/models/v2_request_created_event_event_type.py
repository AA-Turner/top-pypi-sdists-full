from enum import Enum
from functools import lru_cache
from typing import cast

from ..extensions import Enums


class V2RequestCreatedEventEventType(Enums.KnownString):
    V2_REQUESTCREATED = "v2.request.created"

    def __str__(self) -> str:
        return str(self.value)

    @staticmethod
    @lru_cache(maxsize=None)
    def of_unknown(val: str) -> "V2RequestCreatedEventEventType":
        if not isinstance(val, str):
            raise ValueError(f"Value of V2RequestCreatedEventEventType must be a string (encountered: {val})")
        newcls = Enum("V2RequestCreatedEventEventType", {"_UNKNOWN": val}, type=Enums.UnknownString)  # type: ignore
        return cast(V2RequestCreatedEventEventType, getattr(newcls, "_UNKNOWN"))
