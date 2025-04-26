from enum import Enum
from functools import lru_cache
from typing import cast

from ..extensions import Enums


class AssemblyConstantBinBinType(Enums.KnownString):
    CONSTANT = "CONSTANT"

    def __str__(self) -> str:
        return str(self.value)

    @staticmethod
    @lru_cache(maxsize=None)
    def of_unknown(val: str) -> "AssemblyConstantBinBinType":
        if not isinstance(val, str):
            raise ValueError(f"Value of AssemblyConstantBinBinType must be a string (encountered: {val})")
        newcls = Enum("AssemblyConstantBinBinType", {"_UNKNOWN": val}, type=Enums.UnknownString)  # type: ignore
        return cast(AssemblyConstantBinBinType, getattr(newcls, "_UNKNOWN"))
