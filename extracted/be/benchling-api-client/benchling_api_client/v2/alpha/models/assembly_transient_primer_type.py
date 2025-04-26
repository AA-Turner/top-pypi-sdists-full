from enum import Enum
from functools import lru_cache
from typing import cast

from ..extensions import Enums


class AssemblyTransientPrimerType(Enums.KnownString):
    BULK_ASSEMBLY_TRANSIENT_PRIMER = "BULK_ASSEMBLY_TRANSIENT_PRIMER"

    def __str__(self) -> str:
        return str(self.value)

    @staticmethod
    @lru_cache(maxsize=None)
    def of_unknown(val: str) -> "AssemblyTransientPrimerType":
        if not isinstance(val, str):
            raise ValueError(f"Value of AssemblyTransientPrimerType must be a string (encountered: {val})")
        newcls = Enum("AssemblyTransientPrimerType", {"_UNKNOWN": val}, type=Enums.UnknownString)  # type: ignore
        return cast(AssemblyTransientPrimerType, getattr(newcls, "_UNKNOWN"))
