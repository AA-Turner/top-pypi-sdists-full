from enum import Enum
from functools import lru_cache
from typing import cast

from ..extensions import Enums


class AssemblyGoldenGateMethodType(Enums.KnownString):
    GOLDEN_GATE = "GOLDEN_GATE"

    def __str__(self) -> str:
        return str(self.value)

    @staticmethod
    @lru_cache(maxsize=None)
    def of_unknown(val: str) -> "AssemblyGoldenGateMethodType":
        if not isinstance(val, str):
            raise ValueError(f"Value of AssemblyGoldenGateMethodType must be a string (encountered: {val})")
        newcls = Enum("AssemblyGoldenGateMethodType", {"_UNKNOWN": val}, type=Enums.UnknownString)  # type: ignore
        return cast(AssemblyGoldenGateMethodType, getattr(newcls, "_UNKNOWN"))
