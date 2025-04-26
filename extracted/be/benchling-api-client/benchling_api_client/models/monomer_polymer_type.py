from enum import Enum
from functools import lru_cache
from typing import cast

from ..extensions import Enums


class MonomerPolymerType(Enums.KnownString):
    RNA = "RNA"

    def __str__(self) -> str:
        return str(self.value)

    @staticmethod
    @lru_cache(maxsize=None)
    def of_unknown(val: str) -> "MonomerPolymerType":
        if not isinstance(val, str):
            raise ValueError(f"Value of MonomerPolymerType must be a string (encountered: {val})")
        newcls = Enum("MonomerPolymerType", {"_UNKNOWN": val}, type=Enums.UnknownString)  # type: ignore
        return cast(MonomerPolymerType, getattr(newcls, "_UNKNOWN"))
