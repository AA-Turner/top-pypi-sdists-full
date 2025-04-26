from enum import Enum
from functools import lru_cache
from typing import cast

from ..extensions import Enums


class AssemblySharedAssemblyType(Enums.KnownString):
    CLONING = "CLONING"
    CONCATENATION = "CONCATENATION"

    def __str__(self) -> str:
        return str(self.value)

    @staticmethod
    @lru_cache(maxsize=None)
    def of_unknown(val: str) -> "AssemblySharedAssemblyType":
        if not isinstance(val, str):
            raise ValueError(f"Value of AssemblySharedAssemblyType must be a string (encountered: {val})")
        newcls = Enum("AssemblySharedAssemblyType", {"_UNKNOWN": val}, type=Enums.UnknownString)  # type: ignore
        return cast(AssemblySharedAssemblyType, getattr(newcls, "_UNKNOWN"))
