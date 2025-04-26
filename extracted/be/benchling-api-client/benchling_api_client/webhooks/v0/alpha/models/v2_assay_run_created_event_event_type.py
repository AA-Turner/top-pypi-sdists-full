from enum import Enum
from functools import lru_cache
from typing import cast

from ..extensions import Enums


class V2AssayRunCreatedEventEventType(Enums.KnownString):
    V2_ASSAYRUNCREATED = "v2.assayRun.created"

    def __str__(self) -> str:
        return str(self.value)

    @staticmethod
    @lru_cache(maxsize=None)
    def of_unknown(val: str) -> "V2AssayRunCreatedEventEventType":
        if not isinstance(val, str):
            raise ValueError(
                f"Value of V2AssayRunCreatedEventEventType must be a string (encountered: {val})"
            )
        newcls = Enum("V2AssayRunCreatedEventEventType", {"_UNKNOWN": val}, type=Enums.UnknownString)  # type: ignore
        return cast(V2AssayRunCreatedEventEventType, getattr(newcls, "_UNKNOWN"))
