from enum import Enum
from functools import lru_cache
from typing import cast

from ..extensions import Enums


class AssemblyHomologyMethodType(Enums.KnownString):
    HOMOLOGY = "HOMOLOGY"

    def __str__(self) -> str:
        return str(self.value)

    @staticmethod
    @lru_cache(maxsize=None)
    def of_unknown(val: str) -> "AssemblyHomologyMethodType":
        if not isinstance(val, str):
            raise ValueError(f"Value of AssemblyHomologyMethodType must be a string (encountered: {val})")
        newcls = Enum("AssemblyHomologyMethodType", {"_UNKNOWN": val}, type=Enums.UnknownString)  # type: ignore
        return cast(AssemblyHomologyMethodType, getattr(newcls, "_UNKNOWN"))
