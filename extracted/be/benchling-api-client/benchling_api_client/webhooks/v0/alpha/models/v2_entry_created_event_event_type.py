from enum import Enum
from functools import lru_cache
from typing import cast

from ..extensions import Enums


class V2EntryCreatedEventEventType(Enums.KnownString):
    V2_ENTRYCREATED = "v2.entry.created"

    def __str__(self) -> str:
        return str(self.value)

    @staticmethod
    @lru_cache(maxsize=None)
    def of_unknown(val: str) -> "V2EntryCreatedEventEventType":
        if not isinstance(val, str):
            raise ValueError(f"Value of V2EntryCreatedEventEventType must be a string (encountered: {val})")
        newcls = Enum("V2EntryCreatedEventEventType", {"_UNKNOWN": val}, type=Enums.UnknownString)  # type: ignore
        return cast(V2EntryCreatedEventEventType, getattr(newcls, "_UNKNOWN"))
