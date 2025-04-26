from enum import Enum
from functools import lru_cache
from typing import cast

from ..extensions import Enums


class V2RequestUpdatedStatusEventEventType(Enums.KnownString):
    V2_REQUESTUPDATEDSTATUS = "v2.request.updated.status"

    def __str__(self) -> str:
        return str(self.value)

    @staticmethod
    @lru_cache(maxsize=None)
    def of_unknown(val: str) -> "V2RequestUpdatedStatusEventEventType":
        if not isinstance(val, str):
            raise ValueError(
                f"Value of V2RequestUpdatedStatusEventEventType must be a string (encountered: {val})"
            )
        newcls = Enum("V2RequestUpdatedStatusEventEventType", {"_UNKNOWN": val}, type=Enums.UnknownString)  # type: ignore
        return cast(V2RequestUpdatedStatusEventEventType, getattr(newcls, "_UNKNOWN"))
