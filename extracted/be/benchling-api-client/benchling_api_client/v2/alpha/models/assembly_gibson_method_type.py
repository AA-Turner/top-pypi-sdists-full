from enum import Enum
from functools import lru_cache
from typing import cast

from ..extensions import Enums


class AssemblyGibsonMethodType(Enums.KnownString):
    GIBSON = "GIBSON"

    def __str__(self) -> str:
        return str(self.value)

    @staticmethod
    @lru_cache(maxsize=None)
    def of_unknown(val: str) -> "AssemblyGibsonMethodType":
        if not isinstance(val, str):
            raise ValueError(f"Value of AssemblyGibsonMethodType must be a string (encountered: {val})")
        newcls = Enum("AssemblyGibsonMethodType", {"_UNKNOWN": val}, type=Enums.UnknownString)  # type: ignore
        return cast(AssemblyGibsonMethodType, getattr(newcls, "_UNKNOWN"))
